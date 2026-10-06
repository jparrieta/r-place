#!/usr/bin/env python3
"""Run one v30 fleet coder in a temporary, validation-bounded Codex session.

The persistent case lead and this process share the managed store lock.  The CLI's
complete JSON event stream, exact prompt, final reply, stderr, and configuration
receipt remain under <store>/audit/.  Nothing is attached to the batch until the
CLI emits a completed turn, passes the authoritative batch check, leaves no
process-group member, and its temporary CODEX_HOME has been removed. A failed
check may receive two same-session correction turns before the attempt ends.

This wrapper deliberately does not check or collect the batch.
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import re
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import uuid


LIFECYCLE = """Execution boundary for this temporary fleet-coder session: Do not launch subagents or other agents. Work only in the run directory named above. Finish every shell command before your final reply; do not leave background processes, servers, or persistent REPL state running. Keep all working state in that run directory, as AGENT.md requires. Do not change the model or tool configuration. Your final reply marks the end of this turn.

Mandatory completion checklist for this entire slice: record exactly one disposition for every slice thread and none outside it; every thread disposed `coded` must have at least one LIVE (not retracted) code; every read out_of_scope thread with at least 10 IN-WINDOW items must carry an exact `excluded_quote` returned by cite.py; make the read.py audit pass; write out/case.md with every required section and an edge tag, at least 500 bytes, and out/notes.md at least 200 bytes. You are a fleet coder: never call emit.close(), and do not create the exported codes/themes/threads/pointers JSONL files or out/_run.json; those do not exist until the lead consolidates. Immediately before your final reply you MUST run `python3 _scheduler_preflight.py` from this run directory and may finish only after it prints PREFLIGHT PASSED. If it reports a missing disposition or other reversible omission, repair it and rerun the full preflight. Journal dispositions are append-only: never append a second disposition to revise one. If an existing disposition is duplicate, outside the slice, or substantively wrong, stop and report that irreversible defect instead of trying to overwrite or countermand it."""


class RunnerError(RuntimeError):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_checkpoints(yard):
    path = yard / "_tools" / "checkpoints.py"
    spec = importlib.util.spec_from_file_location("atlas_yard_checkpoints", path)
    if spec is None or spec.loader is None:
        raise RunnerError("Cannot load " + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(checkpoints, path, value):
    checkpoints.json_write(path, value)


def normalize(args):
    room = Path(args.room).expanduser().resolve()
    if room.name != "room" or room.parent.name != "workspace":
        raise RunnerError("--room must be exactly <store>/workspace/room")
    store = room.parent.parent
    descriptor_path = store / "STORE.json"
    if not descriptor_path.is_file():
        raise RunnerError("Managed store has no STORE.json: " + str(store))
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    if Path(descriptor.get("room", "")).resolve() != room:
        raise RunnerError("STORE.json does not own the requested managed room")
    source_room = Path(descriptor.get("source_room", "")).resolve()
    if source_room.parent.name != "rooms":
        raise RunnerError("STORE.json has no recognizable source room")
    yard = source_room.parent.parent
    batch_number = int(args.batch)
    if batch_number < 1 or batch_number > 99:
        raise RunnerError("--batch must be between 1 and 99")
    batch = "%02d" % batch_number
    batch_dir = room / "run" / "fleet" / ("batch_" + batch)
    return room, store, yard, descriptor, batch, batch_dir


def preflight(room, store, descriptor, batch, batch_dir, model, effort):
    if (store / "RUNNING.json").exists():
        raise RunnerError("A lead operation is unfinished; inspect RUNNING.json first")
    if descriptor.get("model") != model:
        raise RunnerError("Coder model differs from the persistent lead: %r != %r" %
                          (model, descriptor.get("model")))
    if descriptor.get("effort") != effort:
        raise RunnerError("Coder effort differs from the persistent lead: %r != %r" %
                          (effort, descriptor.get("effort")))
    if not batch_dir.is_dir():
        raise RunnerError("Batch has not been dispatched: " + str(batch_dir))
    manifest_path = batch_dir / "_manifest.json"
    if not manifest_path.is_file():
        raise RunnerError("Batch has no _manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("role") != "fleet coder" or str(manifest.get("batch")) != batch:
        raise RunnerError("Batch manifest role/number does not match the request")
    if manifest.get("model") != model:
        raise RunnerError("Batch manifest model differs from --model")

    out = batch_dir / "out"
    transcript = out / "_transcript.jsonl"
    final = out / "final_message.md"
    completed_outputs = []
    if transcript.is_file() and transcript.stat().st_size:
        completed_outputs.append(str(transcript))
    if final.exists():
        completed_outputs.append(str(final))
    for name in ("_run.json", "case.md"):
        path = out / name
        if path.is_file() and path.stat().st_size:
            completed_outputs.append(str(path))
    if completed_outputs:
        raise RunnerError("Refusing a possible double run; completed coder output exists: " +
                          ", ".join(completed_outputs))
    if not transcript.is_file():
        raise RunnerError("Dispatched batch lacks the scaffolded out/_transcript.jsonl")
    return manifest


def process_group_exists(pid):
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return False
    return True


def stop_process_group(proc):
    if not process_group_exists(proc.pid):
        return
    os.killpg(proc.pid, signal.SIGTERM)
    deadline = time.monotonic() + 10
    while process_group_exists(proc.pid) and time.monotonic() < deadline:
        time.sleep(0.1)
    if process_group_exists(proc.pid):
        os.killpg(proc.pid, signal.SIGKILL)


def parse_complete_transcript(path):
    rows = []
    for number, line in enumerate(path.read_bytes().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RunnerError("Non-JSON stdout event at line %d: %s" % (number, exc))
        if not isinstance(row, dict):
            raise RunnerError("Non-object stdout event at line %d" % number)
        rows.append(row)
    types = [row.get("type") for row in rows]
    if not rows:
        raise RunnerError("Codex emitted no JSON events")
    if types.count("thread.started") != 1:
        raise RunnerError("Expected exactly one thread.started event, got %d" %
                          types.count("thread.started"))
    if types.count("turn.completed") != 1 or types[-1] != "turn.completed":
        raise RunnerError("The complete event stream must end in exactly one turn.completed")
    bad = [t for t in types if t == "turn.failed"]
    if bad:
        raise RunnerError("Codex event stream contains failure events: " + repr(bad))
    return rows, types


def session_artifacts(home):
    found = []
    if not home.exists():
        return found
    for path in home.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(home)
        if path.name.startswith("rollout-") or "sessions" in rel.parts or "archived_sessions" in rel.parts:
            found.append(rel.as_posix())
    return sorted(found)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--room", required=True, help="managed <store>/workspace/room")
    parser.add_argument("--batch", required=True, help="fleet batch number, e.g. 01")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--retry-note", help="Mechanical reason for a fresh retry; retained in the prompt receipt")
    parser.add_argument("--timeout", type=int, default=7200)
    args = parser.parse_args(argv)
    if args.timeout < 1:
        raise RunnerError("--timeout must be positive")

    room, store, yard, descriptor, batch, batch_dir = normalize(args)
    checkpoints = load_checkpoints(yard)
    codex = Path(descriptor["codex"]).resolve()
    auth_source = Path(descriptor["auth_source"]).expanduser().resolve()
    expected_runtime = descriptor.get("runtime") or {}
    if not codex.is_file():
        raise RunnerError("Pinned Codex binary is missing: " + str(codex))
    codex_digest = sha256(codex.read_bytes())
    if expected_runtime.get("codex_sha256") != codex_digest:
        raise RunnerError("Pinned Codex binary digest changed")
    if not auth_source.is_file():
        raise RunnerError("Codex file login is missing at auth_source")

    with checkpoints.locked(store):
        checkpoints.require_clean_transaction(store)
        manifest = preflight(room, store, descriptor, batch, batch_dir,
                             args.model, args.effort)

        audit = store / "audit" / ("coder-%s-%d-%s" %
                                   (batch, time.time_ns(), uuid.uuid4().hex[:8]))
        audit.mkdir(parents=True)
        room_message_result = subprocess.run(
            [sys.executable, "-B", str(yard / "_tools" / "room.py"), "message", "coder",
             "--room", str(room), "--batch", batch],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if room_message_result.returncode:
            (audit / "room_message.stdout.txt").write_text(
                room_message_result.stdout, encoding="utf-8")
            (audit / "room_message.stderr.txt").write_text(
                room_message_result.stderr, encoding="utf-8")
            detail = (room_message_result.stderr or room_message_result.stdout).strip()
            raise RunnerError("room.py message failed (stdout/stderr preserved under %s): %s" %
                              (audit, detail))
        room_message = room_message_result.stdout
        helper_source = yard / "_tools" / "coder_preflight.py"
        if not helper_source.is_file():
            raise RunnerError("Coder preflight helper is missing: " + str(helper_source))
        helper_bytes = helper_source.read_bytes()
        helper_target = batch_dir / "_scheduler_preflight.py"
        checkpoints.atomic(helper_target, helper_bytes)
        prompt = room_message.rstrip() + "\n\n" + LIFECYCLE + "\n"
        if args.retry_note:
            prompt += ("\nScheduler retry note (additional context only; it does not reduce or "
                       "replace any part of the full-slice checklist above): " +
                       args.retry_note.strip() + "\n")
        prompt_bytes = prompt.encode("utf-8")
        room_message_bytes = room_message.encode("utf-8")
        (audit / "room_message.txt").write_bytes(room_message_bytes)
        (audit / "prompt.txt").write_bytes(prompt_bytes)

        raw_final = audit / "final_message.raw.md"
        stdout_path = audit / "stdout.jsonl"
        stderr_path = audit / "stderr.txt"
        command = [
            str(codex), "-a", "never", "-s", "workspace-write", "-m", args.model,
            "-c", "model_reasoning_effort=" + json.dumps(args.effort),
            "-c", 'web_search="disabled"',
            "-c", "features.shell_snapshot=false",
            "-c", "sandbox_workspace_write.network_access=false",
            "-c", "sandbox_workspace_write.exclude_tmpdir_env_var=true",
            "-c", "sandbox_workspace_write.exclude_slash_tmp=true",
            "-c", "analytics.enabled=false",
            "--disable", "multi_agent", "--disable", "multi_agent_v2",
            "exec", "--ignore-user-config",
            "--skip-git-repo-check", "--strict-config", "--json", "--color", "never",
            "-C", str(batch_dir), "-o", str(raw_final), "-",
        ]
        receipt = {
            "format": "atlas-temporary-resumable-coder-v2",
            "status": "prepared",
            "created_utc": now(),
            "store": str(store),
            "room": str(room),
            "batch": batch,
            "batch_dir": str(batch_dir),
            "model": args.model,
            "effort": args.effort,
            "manifest_model": manifest.get("model"),
            "codex": str(codex),
            "codex_sha256": codex_digest,
            "argv": command,
            "cwd": str(batch_dir),
            "sandbox": "workspace-write",
            "approval_policy": "never",
            "network_access": False,
            "web_search": "disabled",
            "multi_agent": False,
            "ephemeral": False,
            "session_retention": "temporary until authoritative batch validation, then destroyed",
            "room_message_path": str(audit / "room_message.txt"),
            "room_message_sha256": sha256(room_message_bytes),
            "prompt_path": str(audit / "prompt.txt"),
            "prompt_sha256": sha256(prompt_bytes),
            "retry_note": args.retry_note,
            "scheduler_preflight_path": str(helper_target),
            "scheduler_preflight_sha256": sha256(helper_bytes),
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "raw_final_path": str(raw_final),
            "authentication": "auth.json borrowed into an isolated temporary CODEX_HOME; home destroyed after authoritative validation",
        }
        write_json(checkpoints, audit / "receipt.json", receipt)

        temp_home = Path(tempfile.mkdtemp(prefix="atlas-coder-home-"))
        snapshot_root = Path(tempfile.mkdtemp(prefix="atlas-coder-batch-"))
        snapshot = snapshot_root / "batch"
        shutil.copytree(batch_dir, snapshot)
        proc = None
        artifacts = []
        home_cleaned = snapshot_cleaned = False
        transcript_parts = []
        correction_commands = []
        authoritative_checks = []
        max_corrections = 2
        try:
            shutil.copyfile(auth_source, temp_home / "auth.json")
            (temp_home / "auth.json").chmod(0o600)
            env = {key: value for key, value in os.environ.items()
                   if not key.startswith(("CODEX_", "OPENAI_", "ANTHROPIC_"))}
            env["CODEX_HOME"] = str(temp_home)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            receipt["status"] = "running"
            receipt["started_utc"] = now()
            write_json(checkpoints, audit / "receipt.json", receipt)

            thread_id = None
            next_prompt = prompt_bytes
            next_command = command
            for turn_number in range(1, max_corrections + 2):
                turn_stdout = stdout_path if turn_number == 1 else audit / (
                    "correction-%02d.stdout.jsonl" % (turn_number - 1))
                turn_stderr = stderr_path if turn_number == 1 else audit / (
                    "correction-%02d.stderr.txt" % (turn_number - 1))
                turn_final = raw_final if turn_number == 1 else audit / (
                    "correction-%02d.final.md" % (turn_number - 1))
                if turn_number > 1:
                    prefix = command[:command.index("exec") + 1]
                    next_command = prefix + [
                        "resume", "--ignore-user-config", "--skip-git-repo-check",
                        "--strict-config", "--json", "-o", str(turn_final),
                        thread_id, "-",
                    ]
                    correction_commands.append(next_command)
                with turn_stdout.open("wb") as stdout, turn_stderr.open("wb") as stderr:
                    proc = subprocess.Popen(next_command, cwd=batch_dir, env=env,
                                            stdin=subprocess.PIPE, stdout=stdout,
                                            stderr=stderr, start_new_session=True)
                    receipt["pid"] = proc.pid
                    receipt["turn_number"] = turn_number
                    write_json(checkpoints, audit / "receipt.json", receipt)
                    try:
                        proc.communicate(input=next_prompt, timeout=args.timeout)
                    except subprocess.TimeoutExpired:
                        stop_process_group(proc)
                        proc.wait()
                        raise RunnerError("Coder exceeded timeout; outputs were not attached")
                if proc.returncode != 0:
                    raise RunnerError("Codex exited %r; outputs were not attached" % proc.returncode)
                if process_group_exists(proc.pid):
                    stop_process_group(proc)
                    raise RunnerError("Coder left a process-group member; it was killed and outputs were not attached")

                turn_rows, event_types = parse_complete_transcript(turn_stdout)
                ids = [row.get("thread_id") for row in turn_rows
                       if row.get("type") == "thread.started"]
                if len(ids) != 1 or not ids[0]:
                    raise RunnerError("Coder transcript has no unique thread id")
                if thread_id is None:
                    thread_id = ids[0]
                elif ids[0] != thread_id:
                    raise RunnerError("Coder correction resumed a different thread")
                if not turn_final.is_file() or not turn_final.read_text(encoding="utf-8").strip():
                    raise RunnerError("Codex completed without a non-empty final message")
                transcript_parts.append(turn_stdout.read_bytes())
                transcript_bytes = b"".join(transcript_parts)
                final_text = turn_final.read_text(encoding="utf-8")

                attached_transcript = batch_dir / "out" / "_transcript.jsonl"
                checkpoints.atomic(attached_transcript, transcript_bytes)
                final_result = subprocess.run(
                    [sys.executable, "-B", str(yard / "_tools" / "room.py"),
                     "final", "--room", str(room), "--batch", batch],
                    input=final_text, text=True, capture_output=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
                if final_result.returncode:
                    raise RunnerError("room.py final failed: " +
                                      (final_result.stdout + final_result.stderr).strip())

                checked = subprocess.run(
                    [sys.executable, "-B", str(yard / "_tools" / "room.py"),
                     "check", "--room", str(room), "--batch", batch],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
                check_path = audit / ("authoritative-check-%02d.txt" % turn_number)
                check_path.write_text(checked.stdout, encoding="utf-8")
                authoritative_checks.append({"turn": turn_number,
                                             "returncode": checked.returncode,
                                             "path": str(check_path)})
                print(checked.stdout[-6000:], flush=True)
                if checked.returncode == 0:
                    break
                if turn_number > max_corrections:
                    raise RunnerError("Authoritative batch check still failed after %d same-coder correction turns; see %s"
                                      % (max_corrections, check_path))

                irreversible = ("Journal dispositions are append-only" in checked.stdout or
                                re.search(r"\bB2\b", checked.stdout))
                if irreversible:
                    shutil.rmtree(batch_dir)
                    shutil.copytree(snapshot, batch_dir)
                correction = (
                    "Your authoritative batch validation failed. Continue as the same fleet "
                    "coder and keep the contract unchanged. " +
                    ("The batch filesystem was restored to its clean dispatch state because "
                     "the failure included an append-only disposition defect. Redo the whole "
                     "slice using what you learned, without repeating that defect. "
                     if irreversible else
                     "The batch filesystem is unchanged. Correct every reported reversible "
                     "defect in place. ") +
                    "Run python3 _scheduler_preflight.py immediately before finishing, and "
                    "finish only after it passes. Exact authoritative checker output follows:\n\n" +
                    checked.stdout)
                correction_path = audit / ("correction-%02d.prompt.txt" % turn_number)
                correction_path.write_text(correction, encoding="utf-8")
                next_prompt = correction.encode("utf-8")

            artifacts = session_artifacts(temp_home)
            receipt.update({"ended_utc": now(), "exit_code": 0,
                            "timed_out": False, "process_group_clean": True,
                            "native_session_artifacts_before_cleanup": artifacts,
                            "thread_id": thread_id,
                            "correction_turns": len(transcript_parts) - 1,
                            "correction_argv": correction_commands,
                            "authoritative_checks": authoritative_checks,
                            "event_count": sum(len(parse_complete_transcript(
                                stdout_path if i == 0 else audit / (
                                    "correction-%02d.stdout.jsonl" % i))[0])
                                               for i in range(len(transcript_parts))),
                            "stdout_sha256": sha256(transcript_bytes),
                            "final_message_sha256": sha256(turn_final.read_bytes())})
            receipt["attachment"] = {
                "transcript": str(attached_transcript),
                "transcript_sha256": sha256(attached_transcript.read_bytes()),
                "final_message": str(batch_dir / "out" / "final_message.md"),
                "room_py_output": final_result.stdout.strip(),
            }
            receipt["status"] = "completed-and-attached"
        except BaseException as exc:
            receipt["status"] = "failed-not-attached"
            receipt["error"] = str(exc)
            raise
        finally:
            if proc is not None and process_group_exists(proc.pid):
                stop_process_group(proc)
            try:
                shutil.rmtree(temp_home)
                home_cleaned = not temp_home.exists()
            except OSError as exc:
                receipt["home_cleanup_error"] = str(exc)
            try:
                shutil.rmtree(snapshot_root)
                snapshot_cleaned = not snapshot_root.exists()
            except OSError as exc:
                receipt["snapshot_cleanup_error"] = str(exc)
            receipt["temporary_codex_home_removed"] = home_cleaned
            receipt["temporary_batch_snapshot_removed"] = snapshot_cleaned
            if not home_cleaned or not snapshot_cleaned:
                receipt["status"] = "failed-not-attached"
            write_json(checkpoints, audit / "receipt.json", receipt)

        if not home_cleaned or not snapshot_cleaned:
            raise RunnerError("Temporary coder session or batch snapshot could not be removed")
        print(json.dumps({"status": receipt["status"], "batch": batch,
                          "audit": str(audit),
                          "correction_turns": receipt["correction_turns"],
                          "next": "authoritative batch check passed"}, indent=2))
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RunnerError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print("FAILED: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
