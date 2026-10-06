#!/usr/bin/env python3
"""Run/checkpoint ONLY the case lead using native Codex app-server history.

Every successful turn shuts down the runtime, exports its complete native rollout,
and commits one checkpoint of the managed room, native lead state, and runner state.
Brief writers and fleet coders are external; only their filesystem outputs travel.
Run with --help. See ../CHECKPOINTS.md for the scheduler integration and limits.
"""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid

from checkpoints import (CheckpointError, atomic, capture, digest, encoded, inventory,
                         json_write, load, locked, now, read_json, recover_restore,
                         require_clean_transaction, restore)

HERE = Path(__file__).resolve().parent
DEFAULT_CODEX = shutil.which("codex") or "/Applications/ChatGPT.app/Contents/Resources/codex"
LIFECYCLE = """You are the case lead for this one room. Follow the room's contracts and the scheduler's message. Do not launch subagents or other agents. Work only in your run directory. Finish every shell command before your final reply; do not leave background processes, servers, or persistent REPL state running between replies. Keep necessary working state in files in your run directory. Use normal foreground Python invocations; emit replays its journal. Do not inspect the surrounding project, other rooms, native runtime directories, checkpoints, or scheduler metadata. Do not change your model or tool configuration. Your final reply marks the end of this turn."""


class Server:
    """Small JSON-RPC client. Requests, notifications, errors and raw native events logged.

    Unexpected interactive requests fail closed. Authentication is borrowed at launch,
    never serialized into a checkpoint; no API key or token is printed.
    """
    def __init__(self, store, desc):
        self.store, self.desc = Path(store), desc
        self.home = self.store / "native" / "lead"
        self.home.mkdir(parents=True, exist_ok=True)
        auth = Path(desc["auth_source"]).expanduser()
        if not auth.is_file():
            raise CheckpointError("Codex file login is required at auth_source; log in before running")
        shutil.copyfile(auth, self.home / "auth.json")
        (self.home / "auth.json").chmod(0o600)
        audit = self.store / "audit" / (str(time.time_ns()) + "-" + uuid.uuid4().hex[:8])
        audit.mkdir(parents=True)
        self.audit = audit
        self.stderr = (audit / "server.stderr").open("w")
        self.trace = (audit / "rpc.jsonl").open("w")
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("CODEX_", "OPENAI_", "ANTHROPIC_"))}
        env["CODEX_HOME"] = str(self.home)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        self.p = subprocess.Popen([desc["codex"], "app-server", "--stdio"],
                                  cwd=desc["cwd"], env=env, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=self.stderr,
                                  text=True, bufsize=1, start_new_session=True)
        self.q, self.next_id, self.pending = queue.Queue(), 0, []
        threading.Thread(target=self._reader, daemon=True).start()
        try:
            self.call("initialize", {"clientInfo": {"name": "atlas_yard_lead",
                      "version": "1.0.0", "title": "Atlas yard case lead"},
                      "capabilities": {"experimentalApi": True}})
            self.send({"method": "initialized", "params": {}})
        except BaseException:
            self.close()
            raise

    def _reader(self):
        try:
            for line in self.p.stdout:
                try:
                    self.q.put(json.loads(line))
                except ValueError:
                    self.q.put({"reader_error": "Non-JSON server output"})
        finally:
            self.q.put({"reader_error": "app-server exited"})

    def send(self, msg):
        self.trace.write(json.dumps({"direction": "send", "message": msg}) + "\n")
        self.trace.flush()
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def receive(self, timeout):
        try:
            msg = self.q.get(timeout=max(0.1, timeout))
        except queue.Empty:
            raise CheckpointError("app-server timeout; inspect audit log")
        self.trace.write(json.dumps({"direction": "receive", "message": msg}) + "\n")
        self.trace.flush()
        if "reader_error" in msg:
            raise CheckpointError(msg["reader_error"] + "; inspect " + str(self.audit))
        if "id" in msg and "method" in msg:
            self.send({"id": msg["id"], "error": {"code": -32603,
                       "message": "Interactive action unavailable in checkpoint runner"}})
            raise CheckpointError("Agent requested interactive action: " + msg["method"])
        return msg

    def call(self, method, params, timeout=90):
        self.next_id += 1
        rid = self.next_id
        self.send({"id": rid, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            msg = self.receive(deadline - time.monotonic())
            if msg.get("id") == rid:
                if "error" in msg:
                    raise CheckpointError(method + ": " + json.dumps(msg["error"]))
                return msg["result"]
            self.pending.append(msg)
        raise CheckpointError("RPC timeout: " + method)

    def wait_turn(self, tid, turn_id, timeout):
        deadline = time.monotonic() + timeout
        last_update = time.monotonic()
        while time.monotonic() < deadline:
            if self.pending:
                msg = self.pending.pop(0)
            else:
                try:
                    msg = self.receive(min(30, deadline - time.monotonic()))
                except CheckpointError as ex:
                    if str(ex).startswith("app-server timeout"):
                        print("Case lead is working...", flush=True)
                        continue
                    raise
            if msg.get("method") == "item/completed":
                item = msg.get("params", {}).get("item", {})
                if item.get("type") == "agentMessage" and item.get("phase") != "final_answer":
                    print(item.get("text", "")[:500], flush=True)
            if time.monotonic() - last_update > 45:
                print("Case lead is working...", flush=True)
                last_update = time.monotonic()
            if msg.get("method") == "turn/completed":
                p = msg["params"]
                turn = p["turn"]
                if p.get("threadId") == tid and turn["id"] == turn_id:
                    if turn["status"] != "completed":
                        raise CheckpointError("Turn did not complete: " + json.dumps(turn))
                    return turn
        raise CheckpointError("Lead exceeded turn timeout; no completed checkpoint committed")

    def close(self):
        clean = True
        if getattr(self, "p", None):
            if self.p.poll() is None:
                self.p.stdin.close()
                try:
                    self.p.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    clean = False
                    os.killpg(self.p.pid, signal.SIGTERM)
                    try:
                        self.p.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(self.p.pid, signal.SIGKILL)
                        self.p.wait()
            # A foreground parent can exit while a child it launched keeps running.
            # Never commit a checkpoint while this server's process group survives.
            try:
                os.killpg(self.p.pid, 0)
            except ProcessLookupError:
                pass
            else:
                clean = False
                os.killpg(self.p.pid, signal.SIGKILL)
            clean = clean and self.p.returncode == 0
            self.trace.close()
            self.stderr.close()
        (self.home / "auth.json").unlink(missing_ok=True)
        return clean


def runtime_info(codex):
    return {"codex_sha256": digest(Path(codex).read_bytes()),
            "python": sys.version, "python_executable": sys.executable,
            "platform": sys.platform}


def check_runtime(desc):
    got = runtime_info(desc["codex"])
    if got != desc["runtime"]:
        raise CheckpointError("Runtime changed. Use the original Codex binary and Python runtime; no silent upgrade allowed")


def relocate_runtime(store, desc):
    """Allow a whole yard to move while the case-lead store name stays stable."""
    store = Path(store).resolve()
    room = store / "workspace" / "room"
    relocated = dict(desc)
    relocated.update({"store_path": str(store), "room": str(room),
                      "cwd": str(room / "run")})
    source = store.parent.parent / "rooms" / store.name.rsplit("-gpt56-calibration-v1", 1)[0]
    if source.is_dir():
        relocated["source_room"] = str(source)
    if relocated != desc:
        json_write(store / "STORE.json", relocated)
    runtime = store / "state" / "runtime.json"
    if runtime.exists() and read_json(runtime) != relocated:
        json_write(runtime, relocated)
    lead = store / "state" / "lead.json"
    if lead.exists():
        state = read_json(lead)
        changed = False
        for key in ("configuration", "startup_configuration"):
            if isinstance(state.get(key), dict) and state[key].get("cwd") != relocated["cwd"]:
                state[key]["cwd"] = relocated["cwd"]
                changed = True
        if changed:
            json_write(lead, state)
    return relocated


def config_text(model, effort):
    return ("model = " + json.dumps(model) + "\nmodel_reasoning_effort = " + json.dumps(effort) +
            '\napproval_policy = "never"\nsandbox_mode = "workspace-write"\n'
            'web_search = "disabled"\ncli_auth_credentials_store = "file"\n'
            '[features]\nshell_snapshot = false\n'
            '[sandbox_workspace_write]\nnetwork_access = false\n'
            'exclude_tmpdir_env_var = true\nexclude_slash_tmp = true\n'
            '[analytics]\nenabled = false\n')


def init(store, room, model, effort, codex, auth_source, host_sandbox=False):
    room, store = Path(room).resolve(), Path(store).resolve()
    if store == room or room in store.parents:
        raise CheckpointError("Store must be outside the source room")
    if (store / "STORE.json").exists() or (store / "workspace").exists():
        raise CheckpointError("Managed store already exists")
    if not (room / "brief" / "out" / "brief.md").is_file():
        raise CheckpointError("The source room needs its brief before initializing a case lead")
    if (room / "run").exists():
        raise CheckpointError("Source already has run/. This initializer starts a new reading; use a clean room copy")
    codex = str(Path(codex).resolve())
    dest = store / "workspace" / "room"
    shutil.copytree(room, dest, ignore=shutil.ignore_patterns("snapshots", "forks", "__pycache__", ".DS_Store"))
    if (dest / "run").exists():
        raise CheckpointError("Source already has run/. This initializer starts a new reading; use a clean room copy")
    desc = {"format": "atlas-codex-lead-v1", "source_room": str(room), "store_path": str(store),
            "room": str(dest), "cwd": str(dest / "run"), "model": model, "effort": effort,
            "codex": codex, "auth_source": str(Path(auth_source).expanduser().resolve()),
            "runtime": runtime_info(codex), "created_utc": now(), "lifecycle_instructions": LIFECYCLE,
            "host_sandbox": host_sandbox}
    # The existing builder runs in the COPY. Source room and concurrent briefs stay untouched.
    subprocess.run([sys.executable, str(HERE / "room.py"), "run", "--room", str(dest),
                    "--model", model], check=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    home = store / "native" / "lead"
    home.mkdir(parents=True)
    atomic(home / "config.toml", config_text(model, effort).encode())
    (store / "state").mkdir()
    json_write(store / "STORE.json", desc)
    # Include the descriptor in every checkpoint, as well as the stable top-level copy.
    json_write(store / "state" / "runtime.json", desc)
    cid = capture(store, {"kind": "prepared", "agent": "case-lead"}, "prepared")
    print(json.dumps({"store": str(store), "room": str(dest), "checkpoint": cid}, indent=2))


def launch_params(desc):
    return {"cwd": desc["cwd"], "model": desc["model"], "approvalPolicy": "never",
            "sandbox": "workspace-write", "developerInstructions": desc["lifecycle_instructions"],
            "config": {"model_reasoning_effort": desc["effort"]}, "ephemeral": False}


def config_evidence(result):
    keys = ("cwd", "model", "modelProvider", "reasoningEffort", "approvalPolicy", "sandbox", "instructionSources")
    ev = {k: result.get(k) for k in keys}
    ev["instruction_hashes"] = {p: digest(Path(p).read_bytes()) for p in result.get("instructionSources", [])}
    return ev


def restored_configuration(actual, state, desc):
    """Codex cold-starts externalSandbox sessions with its config-file default.

    No model turn has run at this point. The runner reapplies the recorded external
    policy on EVERY turn/start, and checks it again before committing. Do not accept
    any other policy drift, or any model/instruction/config drift.
    """
    adjusted = dict(actual)
    expected_default = {"type": "workspaceWrite", "writableRoots": [], "networkAccess": False,
                        "excludeTmpdirEnvVar": True, "excludeSlashTmp": True}
    if desc.get("host_sandbox") and actual.get("sandbox") == expected_default:
        adjusted["sandbox"] = {"type": "externalSandbox", "networkAccess": "restricted"}
    if state and adjusted != state["configuration"]:
        raise CheckpointError("Resume/fork changed effective configuration or instruction sources")
    return adjusted


def final_text(thread, turn_id):
    turns = thread.get("turns", [])
    turn = next((t for t in turns if t["id"] == turn_id), None)
    if not turn or turn.get("status") != "completed":
        raise CheckpointError("Completed turn missing from native persisted history")
    if turns[-1]["id"] != turn_id:
        raise CheckpointError("Native history continued beyond checkpoint turn")
    messages = [i for i in turn.get("items", []) if i.get("type") == "agentMessage"]
    finals = [i for i in messages if i.get("phase") == "final_answer"]
    if not finals:
        finals = messages[-1:]
    text = "\n".join(i.get("text", "") for i in finals).strip()
    if not text:
        raise CheckpointError("Completed turn has no final message")
    return text


def assert_no_backgrounds(server, tid):
    result = server.call("thread/backgroundTerminals/list", {"threadId": tid})
    if result.get("data") or result.get("nextCursor"):
        raise CheckpointError("Live terminal state remains; cannot certify a filesystem/session checkpoint")


def native_export(store, thread, turn_id):
    """Export native segments, including ancestors of copy-on-write native forks.

    Resume uses the UNMODIFIED native directory and databases in the checkpoint.
    This concatenated export is for the instrument's transcript audit only; it is
    never imported as replacement history. End-byte offsets preserve native cuts.
    """
    path = Path(thread.get("path") or "")
    home = Path(store) / "native" / "lead"
    if not path.is_file() or home not in path.resolve().parents:
        raise CheckpointError("Native rollout not found in the managed runtime")
    own_data = path.read_bytes()
    segments = []

    def expand(p, limit=None, seen=None):
        seen = set() if seen is None else seen
        if p in seen:
            raise CheckpointError("Cycle in native history ancestry")
        seen.add(p)
        raw = p.read_bytes()
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > len(raw):
                raise CheckpointError("Invalid native history byte boundary")
            raw = raw[:limit]
        if not raw.strip() or not raw.endswith(b"\n"):
            raise CheckpointError("Incomplete native rollout segment")
        records = [json.loads(l) for l in raw.splitlines() if l.strip()]
        meta = records[0].get("payload", {})
        base = meta.get("history_base")
        prefix = b""
        if base:
            parent_id = base.get("thread_id")
            matches = list(home.rglob("rollout-*" + str(parent_id) + ".jsonl"))
            if len(matches) != 1 or "end_byte_offset" not in base:
                raise CheckpointError("Native fork ancestor missing or unsupported history boundary")
            prefix = expand(matches[0], base["end_byte_offset"], seen)
        elif meta.get("forked_from_id") and meta.get("forked_from_ordinal_exclusive"):
            raise CheckpointError("Unsupported native fork lineage encoding")
        segments.append({"path": str(p), "bytes": len(raw), "sha256": digest(raw)})
        return prefix + raw

    data = expand(path)
    rows = [json.loads(l) for l in data.splitlines() if l.strip()]
    # Persisted final task_complete verifies the message was flushed after the turn.
    complete = [r for r in rows if r.get("type") == "event_msg"
                and r.get("payload", {}).get("type") == "task_complete"]
    if not complete or complete[-1]["payload"].get("turn_id") != turn_id:
        raise CheckpointError("Native rollout has no matching persisted task_complete")
    out = Path(store) / "workspace" / "room" / "run" / "out"
    atomic(out / "_transcript.jsonl", data)
    return {"path": str(path), "rollout_sha256": digest(own_data),
            "sha256": digest(data), "bytes": len(data), "segments": segments}


def prompt_from_args(store, a):
    if a.prompt_file:
        return Path(a.prompt_file).read_text()
    if not a.message:
        raise CheckpointError("Supply --message lead|collect|finish or --prompt-file")
    cmd = [sys.executable, str(HERE / "room.py"), "message", a.message,
           "--room", str(Path(store) / "workspace" / "room")]
    if a.batch:
        cmd += ["--batch", a.batch]
    if a.message == "collect":
        if not a.batch:
            raise CheckpointError("Collection requires a batch number")
        # Fleet JSONL exports may not exist until collect replays the journal.
        # Use the checker's journal-derived counts, never guessed export counts.
        checked = subprocess.run(
            [sys.executable, str(HERE / "verify_room.py"), "--room",
             str(Path(store) / "workspace" / "room"), "--batch", str(a.batch)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if checked.returncode:
            raise CheckpointError("Batch check failed before collection:\n" + checked.stdout)
        cmd += ["--summary", checked.stdout.strip()]
    elif a.summary:
        cmd += ["--summary", a.summary]
    return subprocess.check_output(cmd, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def operation(store, kind, a):
    store = Path(store)
    require_clean_transaction(store)
    desc = relocate_runtime(store, read_json(store / "STORE.json"))
    check_runtime(desc)
    label = a.name if kind == "fork" else a.label
    if label:
        from checkpoints import name
        name(label)
        if (store / "refs" / (label + ".json")).exists():
            raise CheckpointError("Checkpoint label already exists: " + label)
    if kind == "fork":
        cid, checkpoint = load(store, a.checkpoint)
        if checkpoint["metadata"].get("kind") not in ("completed", "fork"):
            raise CheckpointError("Only a completed case-lead turn can be forked")
        restore(store, cid)
        desc = relocate_runtime(store, desc)
    statefile = store / "state" / "lead.json"
    state = read_json(statefile) if statefile.exists() else None
    if kind == "fork" and not state:
        raise CheckpointError("No saved case-lead session at that checkpoint")
    if read_json(store / "state" / "runtime.json") != desc:
        raise CheckpointError("Checkpoint runtime descriptor differs from store")
    prompt = prompt_from_args(store, a) if kind == "turn" else None
    started = now()
    json_write(store / "RUNNING.json", {"runner_pid": os.getpid(), "operation": kind, "started": started})
    server = None
    try:
        server = Server(store, desc)
        json_write(store / "RUNNING.json", {"runner_pid": os.getpid(), "server_pid": server.p.pid,
                   "operation": kind, "started": started, "audit": str(server.audit)})
        if kind == "fork":
            parent = server.call("thread/read", {"threadId": state["thread_id"], "includeTurns": True})["thread"]
            final_text(parent, state["turn_id"])
            result = server.call("thread/fork", {"threadId": state["thread_id"],
                                "lastTurnId": state["turn_id"], "ephemeral": False})
            if result["thread"]["turns"] != parent["turns"]:
                raise CheckpointError("Native fork changed inherited turn history")
        elif state:
            result = server.call("thread/resume", {"threadId": state["thread_id"]})
            if state.get("history_sha256") and digest(encoded(result["thread"]["turns"])) != state["history_sha256"]:
                raise CheckpointError("Native resume changed saved turn history")
        else:
            result = server.call("thread/start", launch_params(desc))
        startup_evidence = config_evidence(result)
        evidence = restored_configuration(startup_evidence, state, desc)
        if evidence["model"] != desc["model"] or evidence["cwd"] != desc["cwd"]:
            raise CheckpointError("Runtime changed model or working directory")
        tid = result["thread"]["id"]
        if kind == "turn":
            if state:
                final_text(result["thread"], state["turn_id"])
            params = {"threadId": tid, "input": [{"type": "text", "text": prompt}],
                      "effort": desc["effort"]}
            if desc.get("host_sandbox"):
                # An enclosing sandbox still enforces its filesystem/network permissions.
                # This mode must NEVER be used from an ordinary unsandboxed terminal.
                params["sandboxPolicy"] = {"type": "externalSandbox", "networkAccess": "restricted"}
            tr = server.call("turn/start", params)
            turn_id = tr["turn"]["id"]
            server.wait_turn(tid, turn_id, a.timeout)
        else:
            turn_id = state["turn_id"]
        assert_no_backgrounds(server, tid)
        thread = server.call("thread/read", {"threadId": tid, "includeTurns": True})["thread"]
        final = final_text(thread, turn_id)
        if kind == "turn":
            effective = server.call("thread/resume", {"threadId": tid})
            evidence = config_evidence(effective)
            expected = "externalSandbox" if desc.get("host_sandbox") else "workspaceWrite"
            if evidence.get("sandbox", {}).get("type") != expected:
                raise CheckpointError("Effective sandbox differs from the configured execution mode")
        if kind == "fork" and final != state["final_message"]:
            raise CheckpointError("Fork lost the final message at the saved boundary")
        if kind == "fork" and tid == state["thread_id"]:
            raise CheckpointError("Fork did not create an independent native thread")
        clean = server.close()
        server = None
        if not clean:
            raise CheckpointError("Runtime did not shut down cleanly; no checkpoint committed")
        export = native_export(store, thread, turn_id)
        prior = state["thread_id"] if state else None
        state = {"thread_id": tid, "turn_id": turn_id, "final_message": final,
                 "configuration": evidence, "native_export": export,
                 "startup_configuration": startup_evidence,
                 "history_sha256": digest(encoded(thread["turns"])),
                 "ended_utc": now(), "operation": kind}
        if kind == "fork":
            state["forked_from"] = {"checkpoint": cid, "thread_id": prior}
        json_write(statefile, state)
        atomic(Path(desc["cwd"]) / "out" / "final_message.md", (final + "\n").encode())
        committed = capture(store, {"kind": "fork" if kind == "fork" else "completed",
                                    "agent": "case-lead", **state}, label)
        (store / "RUNNING.json").unlink()
        print(json.dumps({"checkpoint": committed, "thread_id": tid, "turn_id": turn_id,
                          "final_message": final}, indent=2), flush=True)
        return committed
    except BaseException:
        if server:
            server.close()
        # Keep RUNNING.json. An interrupted turn is never mislabeled a restorable boundary.
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", required=True, help="Dedicated managed room store, outside the source room")
    sp = p.add_subparsers(dest="cmd", required=True)
    ap = sp.add_parser("init", help="Copy a room with its brief; build a new lead run")
    ap.add_argument("--room", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--codex", default=DEFAULT_CODEX)
    ap.add_argument("--auth-source", default=str(Path.home() / ".codex" / "auth.json"))
    ap.add_argument("--host-sandbox", action="store_true", help="Only inside an existing host sandbox: use externalSandbox instead of nesting seatbelt")
    ap = sp.add_parser("turn", help="Start/resume the lead, wait for its final reply, checkpoint")
    ap.add_argument("--message", choices=["lead", "collect", "finish"])
    ap.add_argument("--batch")
    ap.add_argument("--summary")
    ap.add_argument("--prompt-file")
    ap.add_argument("--label")
    ap.add_argument("--timeout", type=int, default=7200)
    ap = sp.add_parser("fork", help="Restore a completed checkpoint and persist a native fork; no model turn")
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--name", required=True)
    for cmd in ("restore", "verify"):
        ap = sp.add_parser(cmd)
        ap.add_argument("--checkpoint", default="HEAD")
    sp.add_parser("status")
    sp.add_parser("recover", help="Roll back an interrupted filesystem restore")
    sp.add_parser("recover-run", help="Clear a failed operation after confirming its processes are gone")
    a = p.parse_args()
    with locked(a.store) as store:
        if a.cmd == "init":
            init(store, a.room, a.model, a.effort, a.codex, a.auth_source, a.host_sandbox)
        elif a.cmd in ("turn", "fork"):
            operation(store, a.cmd, a)
        elif a.cmd == "restore":
            require_clean_transaction(store)
            cid, obj = restore(store, a.checkpoint)
            print(json.dumps({"restored": cid, "kind": obj["metadata"]["kind"]}))
        elif a.cmd == "verify":
            cid, obj = load(store, a.checkpoint)
            print(json.dumps({"verified": cid, "entries": len(obj["entries"]),
                              "live_files_match": inventory(store) == obj["entries"]}))
        elif a.cmd == "status":
            print(json.dumps({"store": read_json(store / "STORE.json"),
                 "head": read_json(store / "HEAD.json"),
                 "lead": read_json(store / "state" / "lead.json") if (store / "state" / "lead.json").exists() else None,
                 "unfinished": (store / "RUNNING.json").exists()}, indent=2))
        elif a.cmd == "recover":
            recover_restore(store)
            print("Interrupted restore rolled back; displaced trees retained")
        elif a.cmd == "recover-run":
            path = store / "RUNNING.json"
            info = read_json(path)
            for key in ("runner_pid", "server_pid"):
                pid = info.get(key)
                if not pid:
                    continue
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    continue
                raise CheckpointError("Process %s still exists; inspect it before recovery" % pid)
            dst = store / "audit" / ("failed-" + uuid.uuid4().hex + ".json")
            dst.parent.mkdir(exist_ok=True)
            path.rename(dst)
            print("Failure marker archived. Restore a known checkpoint before retrying")


if __name__ == "__main__":
    try:
        main()
    except (CheckpointError, OSError, subprocess.CalledProcessError) as ex:
        print("FAILED: " + str(ex), file=sys.stderr)
        sys.exit(1)
