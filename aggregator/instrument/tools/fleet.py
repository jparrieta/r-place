#!/usr/bin/env python3
"""fleet.py: the dispatch leg of a fleet stage, run by the operator outside the analyst's session.

    python3 tools/fleet.py NN --packets out/_packets-NN --return out/RETURN-NN.md \
        --raw 00_GIVE-THE-AGENT/out/_fleet_raw/NN[/batch-k] [--readers 2] [--model @preset/cheap] \
        [--shared index.md,G*.md] [--reissue 2] [--max-tokens 16000] [--dry-run] [--only B017]

What it does, and nothing else. For every packet file in --packets (`*.md`, minus the shared
pages), it sends the shared pages, the packet and the return specification to R fresh readers
on the gateway, one call each, collects what comes back into --raw, validates it, reissues a
failed return to a fresh reader id up to --reissue times, and writes DONE. It reads none of the
analyst's files beyond the packets directory and the return specification. It analyses nothing:
no scoring, no adjudication, no reading of the returns beyond the schema. The analyst does that
in the check leg (FLEET.md §1).

The route. OpenRouter's `/api/v1/messages` with the alias in --model (a preset, `@preset/cheap`
by default). The key comes from the macOS Keychain (service `openrouter`, account $USER) or from
$OPENROUTER_KEY, never from a file in the run. Before the first packet the alias is probed once
and its generation record read, so `arm.json` in --raw names the model that served (a preset's
reply says `unknown`; the generation record does not). Refused before any packet leaves: an
alias serving a model whose id contains `opus`, or, for a fleet, any Anthropic model. This is
the validated route of 2026-09-14 (cheap-arm-openrouter-validated.md), without the Claude Code
session in the middle: a script sends the packets, so no orchestrator model spends tokens or
reads a return.

Validation (per return). The reply must end with the end marker the return specification names
(the last line of the fenced example, or `--end-marker`); every non-empty line before it must
parse as one JSON object; when `RETURN-NN.schema.json` sits beside the return specification,
each object must carry its `required` keys and, where the packet manifest gives the packet's
item count (`MANIFEST.json`: {"B017": {"items": 12, "count_key": "position", "count_exclude":
["primary", "revises"]}}), the count of item lines must equal it: with a count_key, a line counts
when it carries that key, none of the excluded keys, and no `pass` other than 1 (so the prediction
line, the multiplacement records and the second pass do not); without one, every line counts.
Required keys from the schema are checked on the counted lines. A return
that fails is not a disagreement and is not kept as data: it is written to `<reader>.failed.txt`
and the packet goes to a fresh reader id, `reissue: 1` or `2`. When reissues are exhausted the
packet is listed in `EXHAUSTED.tsv`, the dispatch goes on with the rest, and exits 2 at the end:
the build leg rebuilds those packets (FLEET.md §1).

Files written under --raw:
    arm.json                 alias, served model, generation id of the probe, utc, readers, reissue policy
    <packet>/<reader>.jsonl  the validated return, one JSON object per line, the end marker removed
    <packet>/<reader>.raw.txt   the reply as received
    <packet>/<reader>.meta.json generation id, served model (from the generation record), tokens,
                                elapsed seconds, reissue number, the packet's sha256
    <packet>/<reader>.failed.txt   a reply that failed validation, with the reason on line 1
    log.jsonl                one line per call
    EXHAUSTED.tsv            packets with no valid return after the reissues
    DONE                     counts, the spend in USD and the tokens, summed from the usage blocks;
                             written only when every packet was tried
Reader ids are r1..rR for the first try and r<R+k> for reissues; no id is reused in one run.

Parts. Packets that MANIFEST.json groups (`"group": "B017", "part": k, "parts": n`, written by
packets.py for a batch over the ceiling) are one unit: the same reader gets part 1 with the shared
pages and the return specification, returns its lines, then gets part 2 as the next turn of the
same conversation, and so on, so one reader reads the whole room (J, 2026-09-25). Each part's reply
is validated against its own item count; the unit's return is the parts' lines concatenated into
`<batch>/<reader>.jsonl`; a failed part sends the whole unit to a fresh reader.

v41: under Claude the operator runs this file (harness/dispatch.sh); under Codex the controller
(rplace/runtime/fleet.py) dispatches and applies the same return validation (validate, counted,
end_marker_of), which must stay identical on both platforms.
"""
import argparse, collections, concurrent.futures, threading, datetime, glob, hashlib, json, os, re, subprocess, sys, time, urllib.request

API = "https://openrouter.ai/api/v1/messages"
GEN = "https://openrouter.ai/api/v1/generation?id="


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def key():
    k = os.environ.get("OPENROUTER_KEY")
    if k:
        return k
    try:
        k = subprocess.run(["security", "find-generic-password", "-s", "openrouter", "-a",
                            os.environ.get("USER", ""), "-w"], capture_output=True, text=True).stdout.strip()
    except OSError:
        k = ""
    if not k:
        sys.exit("no OpenRouter key: set OPENROUTER_KEY or store it in the Keychain (service openrouter)")
    return k


def post(url, body, k, timeout=900, tries=4):
    """One call, retried with backoff on a rate limit (429), a server error (5xx) or a dropped
    connection; any other error, or the last failure, is raised with the gateway's own message."""
    import urllib.error
    last = None
    for n in range(tries):
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers={"Authorization": "Bearer %s" % k, "Content-Type": "application/json",
                                              "anthropic-version": "2023-06-01"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            last = RuntimeError("HTTP %d: %s" % (e.code, msg))
            if e.code != 429 and e.code < 500:
                raise last
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = RuntimeError("connection: %s" % e)
        time.sleep(min(120, 10 * 2 ** n))
    raise last


def cli_send(msgs, sess, a):
    """The cli route: one turn of a reader session run by the Claude Code CLI on the subscription,
    in a scratch folder with its own config directory and every tool refused. The first turn opens
    the session; each later part resumes it. Returns a reply shaped like the gateway's."""
    cmd = ["claude", "-p", "--model", a.model, "--output-format", "json", "--strict-mcp-config",
           "--disallowedTools", "Bash", "Read", "Edit", "Write", "Glob", "Grep", "NotebookEdit",
           "WebFetch", "WebSearch", "Agent", "Task"]
    if sess:
        cmd += ["--resume", sess]
    os.makedirs(a.cli_cwd, exist_ok=True)
    env = dict(os.environ, CLAUDE_CONFIG_DIR=a.cli_config)
    for v in list(env):                          # the cli route is the subscription, never the gateway
        if v.startswith(("ANTHROPIC_", "OPENROUTER_", "CLAUDE_CODE_USE_")) or v in ("CLAUDE_CODE_PROJECT_DIR_NAME",):
            env.pop(v, None)
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    r = subprocess.run(cmd, input=msgs[-1]["content"], capture_output=True, text=True, cwd=a.cli_cwd,
                       env=env, timeout=1800)
    if r.returncode:
        raise RuntimeError("claude -p exited %d: %s" % (r.returncode, (r.stderr or r.stdout)[:300]))
    d = json.loads(r.stdout)
    mu = d.get("modelUsage") or {}
    u = d.get("usage") or {}
    return {"id": d.get("session_id"), "content": [{"type": "text", "text": d.get("result") or ""}],
            "usage": {"cost": d.get("total_cost_usd"), "input_tokens": u.get("input_tokens"),
                      "output_tokens": u.get("output_tokens")},
            "model": ",".join(sorted(mu)) or None}, d.get("session_id")


def get(url, k):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer %s" % k})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def served_model(gid, k):
    for _ in range(8):
        time.sleep(3)
        try:
            g = get(GEN + gid, k)
        except Exception:
            continue
        m = (g.get("data") or {}).get("model") or g.get("model")
        if m:
            return m
    return None


def text_of(reply):
    parts = reply.get("content") or []
    return "".join(p.get("text", "") for p in parts if p.get("type") == "text")


def end_marker_of(spec_text, override):
    if override:
        return override
    # the last line of the last fenced block in the return specification
    blocks = re.findall(r"```[^\n]*\n(.*?)```", spec_text, re.S)
    for b in reversed(blocks):
        lines = [l for l in b.strip().splitlines() if l.strip()]
        if lines:
            return lines[-1].strip()
    return None


def counted(o, rule):
    """Whether a return line counts toward the packet's item count. rule is the MANIFEST entry:
    {"items": n, "count_key": "position", "count_exclude": ["primary", "revises"]}. With no
    count_key every line counts (one line per item)."""
    key = rule.get("count_key")
    if not key:
        return True
    if key not in o:
        return False
    if any(k in o for k in rule.get("count_exclude", [])):
        return False
    return o.get("pass", 1) in (1, "1", None)


def validate(raw, marker, schema, expect_n, rule=None):
    lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
    if marker:
        if not lines or lines[-1] != marker:
            return None, "no end marker %r on the last line" % marker
        lines = lines[:-1]
    # strip a code fence a reader may have added
    lines = [l for l in lines if not l.startswith("```")]
    rows = []
    for i, l in enumerate(lines):
        try:
            o = json.loads(l)
        except ValueError:
            return None, "line %d is not JSON: %s" % (i + 1, l[:80])
        if not isinstance(o, dict):
            return None, "line %d is not an object" % (i + 1)
        rule = rule or {}
        if counted(o, rule):
            for k in (schema or {}).get("required", []):
                if k not in o:
                    return None, "line %d lacks %r" % (i + 1, k)
            for k, spec in ((schema or {}).get("properties") or {}).items():   # an enum the schema sets (dreturn.py)
                if isinstance(spec, dict) and "enum" in spec and k in o and o[k] not in spec["enum"]:
                    return None, "line %d: %s is %r, not one of %s" % (i + 1, k, o[k], spec["enum"])
        rows.append(o)
    n_counted = sum(1 for o in rows if counted(o, rule or {}))
    if expect_n is not None and n_counted != expect_n:
        return None, "%d item lines returned, %d expected: a partial return is not a return" % (n_counted, expect_n)
    if not rows:
        return None, "empty return"
    return rows, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage")
    ap.add_argument("--packets", required=True)
    ap.add_argument("--return", dest="ret", required=True, help="RETURN-NN.md")
    ap.add_argument("--raw", required=True, help="where the returns go (_fleet_raw/NN[/batch-k])")
    ap.add_argument("--readers", type=int, default=2)
    ap.add_argument("--model", default="@preset/cheap")
    ap.add_argument("--shared", default="index.md,G*.md",
                    help="comma-separated globs, relative to --packets, sent with every packet and never as a packet")
    ap.add_argument("--reissue", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=64000)   # a reasoning reader spent 15,719 of 16,000 on thinking (B2 r1)
    ap.add_argument("--end-marker", default=None)
    ap.add_argument("--only", default=None, help="comma-separated packet names")
    ap.add_argument("--allow-anthropic", action="store_true", help="for a reader arm the stage file names as Opus (C2, C5)")
    ap.add_argument("--declared-served", default=None,
                    help="the one model the alias is set to serve, used when the gateway's generation record cannot "
                         "be read (J, 2026-10-11: OpenRouter does not share the model); recorded as unverified")
    ap.add_argument("--reasoning-effort", default=None,
                    help="OpenRouter's reasoning effort for the readers (none, minimal, low, medium, high); J, 2026-10-11: "
                         "a reader spent 63,039 of 64,000 output tokens reasoning and wrote nothing")
    ap.add_argument("--parallel", type=int, default=24, help="readers in flight at once (J, 2026-10-11)")
    ap.add_argument("--dry-run", action="store_true", help="build the messages, send nothing")
    ap.add_argument("--route", choices=["gateway", "cli"], default="gateway",
                    help="gateway: OpenRouter with a preset alias; cli: the Claude Code CLI on the subscription, "
                         "--model a Claude model id (C2 and C5's Opus readers)")
    ap.add_argument("--cli-config", default=None, help="cli route: the readers' own CLAUDE_CONFIG_DIR")
    ap.add_argument("--cli-cwd", default=None, help="cli route: the readers' scratch folder")
    a = ap.parse_args()

    spec = open(a.ret, encoding="utf-8").read()
    marker = end_marker_of(spec, a.end_marker)
    sp = os.path.splitext(a.ret)[0] + ".schema.json"
    schema = json.load(open(sp)) if os.path.exists(sp) else None
    mp = os.path.join(a.packets, "MANIFEST.json")
    manifest = json.load(open(mp)) if os.path.exists(mp) else {}
    shared_files = sorted({p for g in a.shared.split(",") if g.strip()
                           for p in glob.glob(os.path.join(a.packets, g.strip()))})
    ret_abs = os.path.abspath(a.ret)
    packets = sorted(p for p in glob.glob(os.path.join(a.packets, "*.md"))
                     if p not in shared_files and os.path.abspath(p) != ret_abs
                     and not os.path.basename(p).startswith("RETURN-"))
    if a.only:
        want = set(a.only.split(","))
        packets = [p for p in packets if os.path.splitext(os.path.basename(p))[0] in want]
    if not packets:
        sys.exit("no packets in %s" % a.packets)
    shared = "".join("<<< %s >>>\n%s\n\n" % (os.path.basename(p), open(p, encoding="utf-8").read())
                     for p in shared_files)
    os.makedirs(a.raw, exist_ok=True)
    logp = os.path.join(a.raw, "log.jsonl")

    def log(**kw):
        kw["t"] = now()
        with open(logp, "a", encoding="utf-8") as f:
            f.write(json.dumps(kw, ensure_ascii=False) + "\n")

    if a.dry_run:
        for p in packets:
            name = os.path.splitext(os.path.basename(p))[0]
            body = shared + "<<< %s >>>\n%s\n\n<<< RETURN >>>\n%s" % (name, open(p, encoding="utf-8").read(), spec)
            print("%s: %d bytes to each of %d readers; expect %s lines; marker %r"
                  % (name, len(body.encode("utf-8")), a.readers, (manifest.get(name) or {}).get("items"), marker))
        print("dry run: nothing sent; shared pages: %s" % ", ".join(os.path.basename(p) for p in shared_files))
        return 0

    if a.route == "cli":
        if not a.allow_anthropic:
            sys.exit("REFUSING: the cli route serves a Claude model; pass --allow-anthropic, which the stage's "
                     "arm grants only where the stage file names Opus readers (C2, C5)")
        a.cli_config = a.cli_config or os.path.join(a.raw, ".readers-config")
        a.cli_cwd = a.cli_cwd or os.path.join(a.raw, ".readers-cwd")
        k, gid, served = None, None, a.model
        verified = True
    else:
        k = key()
        # ---- the probe: what serves the alias --------------------------------------------------
        probe = post(API, {"model": a.model, "max_tokens": 8,
                           "messages": [{"role": "user", "content": "Reply with the word ok."}]}, k, timeout=120)
        gid = probe.get("id")
        if not gid:
            sys.exit("REFUSING: the probe of %s returned no generation id: %s" % (a.model, json.dumps(probe)[:400]))
        # J, 2026-10-11: /messages answers with a msg_ id the generation endpoint refuses ("Invalid generation
        # ID"); the reply itself names the model that served it, so that is read first
        said = probe.get("model") if probe.get("model") not in (None, "", "unknown") else None
        served = said or (served_model(gid, k) if not str(gid).startswith("msg_") else None)
        verified = bool(served)
        if not served:
            said = probe.get("model") if probe.get("model") not in (None, "", "unknown") else None
            served = said or a.declared_served
            if not served:
                sys.exit("REFUSING: could not read the generation record for the probe (%s), and no model was declared "
                         "for the alias (--declared-served, arm.json readers.declared_served)" % gid)
            print("note: the generation record could not be read; the alias is taken to serve %s (%s), unverified"
                  % (served, "the reply's model field" if said else "declared"))
    low = served.lower()
    if ("opus" in low or "anthropic" in low or "claude" in low) and not a.allow_anthropic:
        sys.exit("REFUSING: %s serves %s, an Anthropic model on a cheap fleet; pass --allow-anthropic only "
                 "for a reader arm the stage file names" % (a.model, served))
    arm = {"stage": a.stage, "route": a.route, "alias": a.model, "served": served, "served_verified": verified,
           "probe_generation": gid, "reasoning_effort": a.reasoning_effort,
           "utc": now(), "readers": a.readers, "reissue": a.reissue, "max_tokens": a.max_tokens,
           "shared": [os.path.basename(p) for p in shared_files], "packets": len(packets),
           "return_spec_sha256": hashlib.sha256(spec.encode("utf-8")).hexdigest()}
    json.dump(arm, open(os.path.join(a.raw, "arm.json"), "w"), indent=1)
    print("arm: %s serves %s; %d packets x %d readers" % (a.model, served, len(packets), a.readers))

    # ---- the packets ----------------------------------------------------------------------------
    # reader ids are never reused in a raw folder, across runs of --only included
    seen = [int(m.group(1)) for f in glob.glob(os.path.join(a.raw, "*", "r*.meta.json"))
            for m in [re.search(r"/r(\d+)\.meta\.json$", f)] if m]
    first_id = (max(seen) if (seen and a.only) else 0)
    # a reissue takes the next id above every reader of this run (J, 2026-10-11: under --only the old start
    # handed the first reissue the id just used, so it sent the same bytes and the cache answered)
    next_id = [max([first_id + a.readers] + seen)]
    exhausted = []
    ok_returns = 0
    spend = 0.0          # gateway spend, USD
    sub_spend = 0.0      # the cli route's notional cost on the subscription, never added to spend
    tokens_in = tokens_out = 0
    # A unit is one packet, or the parts of one batch (MANIFEST "group"), which go to the same
    # reader in one conversation: part 1 with the shared pages, then each next part as the next
    # turn, the reader's earlier replies kept in the thread. Every part's reply is validated on its
    # own; a failed part fails the unit and the whole unit goes to a fresh reader.
    units = collections.OrderedDict()
    for p in packets:
        name = os.path.splitext(os.path.basename(p))[0]
        g = (manifest.get(name) or {}).get("group") or name
        units.setdefault(g, []).append(p)
    for g in units:
        units[g].sort(key=lambda p: (manifest.get(os.path.splitext(os.path.basename(p))[0]) or {}).get("part", 0))
    TAIL = ("\n\nReturn only the lines the return specification asks for, one JSON object per line, then the "
            "end marker on its own line. No prose before, between or after.")
    jobs = []
    for g, plist in units.items():
        d = os.path.join(a.raw, g)
        os.makedirs(d, exist_ok=True)
        parts = []
        for p in plist:
            name = os.path.splitext(os.path.basename(p))[0]
            ptxt = open(p, encoding="utf-8").read()
            parts.append((name, ptxt, hashlib.sha256(ptxt.encode("utf-8")).hexdigest()))
        for r in range(1, a.readers + 1):
            jobs.append((g, d, parts, "r%d" % (first_id + r)))
    lock = threading.Lock()
    acc = {"spend": 0.0, "sub": 0.0, "tin": 0, "tout": 0, "ok": 0}

    def chain(g, d, parts, rid):
        """One reader's unit with its reissues. Readers run side by side, --parallel at a time (J, 2026-10-11:
        v37's fleets ran in parallel; one call at a time made three high-effort readers take over half an hour)."""
        tries = 0
        while True:
            msgs, rows_all, why, raws, metas, sess = [], [], None, [], [], None
            for i, (name, ptxt, psha) in enumerate(parts):
                if i == 0:
                    # the reader's id opens the message (J, 2026-10-11): the return names it as `agent`, and two
                    # readers never send the same bytes, so the gateway's response cache cannot hand one
                    # reader another's reply (B2 round 1: eight reissues got the first reply back, 0 tokens)
                    body = ("<<< READER >>>\nYour reader id is %s; write it as `agent` on every line.\n\n" % rid
                            + shared + "<<< %s >>>\n%s\n\n<<< RETURN >>>\n%s%s" % (name, ptxt, spec, TAIL))
                else:
                    body = "<<< %s >>>\n%s%s" % (name, ptxt, TAIL)
                msgs.append({"role": "user", "content": body})
                t0 = time.time()
                try:
                    if a.route == "cli":
                        reply, sess = cli_send(msgs, sess, a)
                    else:
                        req = {"model": a.model, "max_tokens": a.max_tokens, "messages": msgs}
                        if a.reasoning_effort:
                            req["reasoning"] = {"effort": a.reasoning_effort}
                        reply = post(API, req, k)
                    raw = text_of(reply)
                    gid = reply.get("id")
                    usage = reply.get("usage") or {}
                    err = None
                except Exception as e:                # a transport failure is a failed return
                    raw, gid, usage, err = "", None, {}, "transport: %s" % e
                el = round(time.time() - t0, 1)
                rows, why = (None, err) if err else validate(raw, marker, schema,
                                                              (manifest.get(name) or {}).get("items"),
                                                              manifest.get(name) or {})
                spend_i = float(usage.get("cost") or 0.0)
                with lock:
                    acc["sub" if a.route == "cli" else "spend"] += spend_i
                    acc["tin"] += int(usage.get("input_tokens") or 0)
                    acc["tout"] += int(usage.get("output_tokens") or 0)
                meta = {"packet": name, "group": g, "reader": rid, "reissue": tries, "generation": gid,
                        "served": (reply.get("model") if a.route == "cli" or not verified or
                                   str(gid).startswith("msg_") else served_model(gid, k)) if gid else None,
                        "usage": usage, "elapsed_s": el,
                        "packet_sha256": psha, "valid": rows is not None, "why": why}
                sv = (meta.get("served") or "").lower()
                if rows is not None and a.route != "cli" and not a.allow_anthropic and ("claude" in sv or "anthropic" in sv):
                    rows, why = None, "served by %s: the gateway fell back to an Anthropic model" % meta["served"]
                    meta.update(valid=False, why=why)
                meta["served_matches_probe"] = (not meta.get("served")) or meta["served"] == served
                metas.append(meta)
                raws.append(raw)
                with lock:
                    log(**meta)
                msgs.append({"role": "assistant", "content": raw or "(no reply)"})
                if rows is None:
                    why = "%s: %s" % (name, why)
                    break
                rows_all += rows
            tag = rid
            json.dump(metas if len(parts) > 1 else metas[0], open(os.path.join(d, "%s.meta.json" % tag), "w"), indent=1)
            open(os.path.join(d, "%s.raw.txt" % tag), "w", encoding="utf-8").write(
                "\n\n".join("<<< %s >>>\n%s" % (parts[i][0], x) for i, x in enumerate(raws)) if len(parts) > 1 else raws[0])
            if why is None:
                with open(os.path.join(d, "%s.jsonl" % tag), "w", encoding="utf-8") as f:
                    for o in rows_all:
                        f.write(json.dumps(o, ensure_ascii=False) + "\n")
                with lock:
                    acc["ok"] += 1
                print("%s %s ok (%d lines in %d part(s))" % (g, rid, len(rows_all), len(parts)))
                break
            open(os.path.join(d, "%s.failed.txt" % tag), "w", encoding="utf-8").write("%s\n%s" % (why, "\n\n".join(raws)))
            print("%s %s FAILED: %s" % (g, rid, why))
            if tries >= a.reissue:
                with lock:
                    exhausted.append((g, rid, why))
                break
            tries += 1
            with lock:
                next_id[0] += 1
                rid = "r%d" % next_id[0]                 # a fresh reader id, never reused

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
        for f in [ex.submit(chain, *j) for j in jobs]:
            f.result()
    spend, sub_spend, tokens_in, tokens_out, ok_returns = acc["spend"], acc["sub"], acc["tin"], acc["tout"], acc["ok"]
    if exhausted:
        with open(os.path.join(a.raw, "EXHAUSTED.tsv"), "w", encoding="utf-8") as f:
            f.write("packet\tlast_reader\twhy\n")
            for e in exhausted:
                f.write("\t".join(e) + "\n")
    rec = {"stage": a.stage, "utc": now(), "packets": len(packets), "units": len(units), "readers": a.readers,
           "valid_returns": ok_returns, "exhausted": len(exhausted), "served": served, "only": a.only,
           "cost_usd": round(spend, 6), "subscription_cost_usd": round(sub_spend, 6),
           "input_tokens": tokens_in, "output_tokens": tokens_out}
    # DONE opens the check leg: it is written by a full run only; a run over --only packets leaves
    # a dated PARTIAL record beside the earlier DONE, which it never replaces
    name = "DONE" if not a.only else "PARTIAL-%s.json" % now().replace(":", "")
    with open(os.path.join(a.raw, name), "w") as f:
        f.write(json.dumps(rec) + "\n")
    print("done: %d valid returns, %d exhausted, %.4f USD, %d in / %d out tokens -> %s"
          % (ok_returns, len(exhausted), spend, tokens_in, tokens_out, a.raw))
    return 2 if exhausted else 0


if __name__ == "__main__":
    sys.exit(main())
