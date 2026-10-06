#!/usr/bin/env python3
"""pretool_guard.py: the analyst's PreToolUse hook. Reads the tool call as JSON on stdin; exit 2
blocks the call and the message on stderr goes back to the analyst. It enforces three standing
rules that were asked of the model and nothing else:
  - never delete a file (rm, rmdir, unlink, shutil.rmtree, os.remove in out/ and the folders
    the analyst reads); supersede it with a new name;
  - the instrument's own folders (tools/, stages/, package/, trees/, shelves/, .claude/) are read
    only;
  - the diary is written only through mem.py.
Two more, added 2026-09-28 from the v37 interviews (the rules were asked and not kept):
  - after a compaction (after_compact.sh writes CONTROL/.compact-gate.json), every call is refused
    until out/_head.md and the stage file have been Read and `mem.py diary` run; the gate lifts at
    the next `mem.py log`, or opens after five refusals, logged;
  - at stage A1 a room note (out/rooms/<sub>.md) is refused until that room's concepts were read
    (`mem.py codes --sub <sub>` or `cite.py --room <sub>`).
With --post it is the PostToolUse hook: after a room note is written it runs the note's form check
and returns what is wrong at once, instead of at the block's close.
A string guard over Bash is a tripwire, never a wall: the sandbox's denyWrite is the wall for the
folders above. Every block is appended to out/_closes/guard.log for the audit.
"""
import json, os, re, sys, datetime

RO = ("tools/", "stages/", "package/", "trees/", "shelves/", ".claude/")


def block(msg, call):
    try:
        d = os.path.join(BASE, "out", "_closes")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "guard.log"), "a") as f:
            f.write(json.dumps({"t": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                "tool": call.get("tool_name"), "why": msg}) + "\n")
    except Exception:
        pass
    print(msg, file=sys.stderr)
    sys.exit(2)


BASE = os.getcwd()
CONTROL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(CONTROL, ".compact-gate.json")
GATE_LIMIT = 5
NOTE = re.compile(r"^out/rooms/([^/_][^/]*)\.md$")


def _stamp():
    return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def _read(name):
    try:
        return open(os.path.join(BASE, name), encoding="utf-8").read().strip()
    except OSError:
        return ""


def _canon(s):
    s = str(s or "").strip()
    return (s[2:] if s.lower().startswith("r/") else s).lower()


def _audit(msg, call):
    try:
        d = os.path.join(BASE, "out", "_closes")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "guard.log"), "a") as f:
            f.write(json.dumps({"t": _stamp(), "leg": _read(".leg"), "tool": call.get("tool_name"), "why": msg}) + "\n")
    except Exception:
        pass


def gate(tool, inp, call):
    """After a compaction: the head, the stage file and the diary before anything else."""
    if not os.path.exists(GATE):
        return
    try:
        g = json.load(open(GATE, encoding="utf-8"))
    except Exception:
        g = {}
    if not isinstance(g, dict):
        g = {}
    leg = _read(".leg")
    if g.get("leg") and leg and g["leg"] != leg:          # a gate left by another leg
        os.replace(GATE, GATE.replace(".json", ".%s.stale.json" % _stamp()))
        return
    nn = g.get("stage") or _read(".stage")
    done = set(g.get("done") or [])
    ok = False
    if tool == "Read":
        f = rel(inp.get("file_path"))
        whole = not inp.get("offset") and not inp.get("limit")   # a part of the file is not the file (review 2026-09-29)
        sf = _read(".stagefile")
        if f == "out/_head.md":
            if whole:
                done.add("head")
            ok = True
        elif (f == sf if sf else (f.startswith("stages/STAGE-%s-" % nn) and f.endswith(".md"))):
            if whole:
                done.add("stage")
            ok = True
        elif f.startswith("stages/"):
            ok = True
    elif tool == "Bash":
        cmd = inp.get("command") or ""
        if re.search(r"mem\.py\s+diary\b", cmd):
            done.add("diary"); ok = True
        elif re.search(r"mem\.py\s+log\b", cmd) and {"head", "stage", "diary"} <= done:
            os.replace(GATE, GATE.replace(".json", ".%s.lifted.json" % _stamp()))
            return
    g["done"] = sorted(done)
    if ok:
        json.dump(g, open(GATE, "w", encoding="utf-8"))
        return
    need = [x for x, k in (("Read out/_head.md in full", "head"),
                           ("Read your stage file stages/STAGE-%s-*.md" % (nn or "?"), "stage"),
                           ("run python3 tools/mem.py diary --last 5", "diary")) if k not in done]
    if not need:
        need = ["log the reconciliation: python3 tools/mem.py log \"compacted; head reconciled\" --kind note"]
    g["refused"] = int(g.get("refused") or 0) + 1
    if g["refused"] > GATE_LIMIT:
        os.replace(GATE, GATE.replace(".json", ".%s.opened-by-limit.json" % _stamp()))
        _audit("compaction gate opened after %d refusals; still owed: %s" % (g["refused"], "; ".join(need)), call)
        return
    json.dump(g, open(GATE, "w", encoding="utf-8"))
    block("Your context was compacted. Before any other step: %s. (The summary of the compacted context is not "
          "the record; the head and the diary are.)" % "; then ".join(need), call)


def concepts_first(p, call):
    """Stage A1: a room's note is written after its concepts were read."""
    m = NOTE.match(p)
    if not m or _read(".stage") != "A1":
        return
    sub = _canon(m.group(1))
    for name, key, verb in (("_mem_reads-A1.jsonl", "sub", "codes"), ("_cite_reads-A1.jsonl", "room", None)):
        try:
            lines = open(os.path.join(BASE, "out", name), encoding="utf-8").read().splitlines()
        except OSError:
            continue
        for line in lines:                   # one bad line is skipped, never the file
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if not isinstance(r, dict) or r.get("refused") or (verb and r.get("verb") != verb):
                continue
            if _canon((r.get("opts") or {}).get(key)) == sub:
                return
    block("read r/%s's concepts before its note: python3 tools/mem.py codes --sub %s (stage A1 section 4 reads "
          "the concepts before the account, and the note after both)" % (m.group(1), m.group(1)), call)


def post(call):
    """PostToolUse: a room note just written is checked in the fixed form of stage A1 section 4."""
    tool = call.get("tool_name", "")
    inp = call.get("tool_input") or {}
    if tool not in ("Write", "Edit", "MultiEdit"):
        return 0
    m = NOTE.match(rel(inp.get("file_path")))
    if not m:
        return 0
    try:
        sys.path.insert(0, os.path.join(BASE, "tools"))
        from checks.stage_A1 import note_problems
        t = open(os.path.join(BASE, "out", "rooms", m.group(1) + ".md"), encoding="utf-8", errors="replace").read()
        probs = note_problems(m.group(1), t)
    except Exception as e:
        print("the note check could not run: %s" % e, file=sys.stderr)
        return 0
    if not probs:
        return 0
    print("rooms/%s.md, fix it now:\n%s" % (m.group(1), "\n".join("- " + x[1] for x in probs)), file=sys.stderr)
    return 2


def rel(p):
    if not p:
        return ""
    try:
        return os.path.relpath(os.path.join(BASE, p), BASE).replace(os.sep, "/")
    except ValueError:
        return p


def main():
    global BASE
    try:
        call = json.load(sys.stdin)
    except Exception:
        return 0
    BASE = call.get("cwd") or BASE
    if "--post" in sys.argv[1:]:
        return post(call)
    tool = call.get("tool_name", "")
    inp = call.get("tool_input") or {}
    try:
        gate(tool, inp, call)
    except SystemExit:
        raise
    except Exception as e:                   # a broken gate file never switches the other rules off
        try:
            os.replace(GATE, GATE.replace(".json", ".%s.broken.json" % _stamp()))
        except OSError:
            pass
        _audit("compaction gate set aside, unreadable: %s" % e, call)
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        p = rel(inp.get("file_path") or inp.get("notebook_path"))
        if p.startswith(RO):
            block("%s is read only: the instrument's folders are not yours to change. Write in out/." % p, call)
        if p.startswith("out/diary/"):
            block("the diary is written only through python3 tools/mem.py log.", call)
        if (p.startswith("out/_closes/") or p.startswith("out/sealed/") or p.startswith("out/_answers/")
                or p in ("out/seed.txt", "out/kinds-B1.jsonl", "out/asks.jsonl")
                or re.match(r"^out/stopping-[A-E]\d-decision\.jsonl$", p)):
            block("%s is written by the tools (done.sh, handoff.py, saturation.py, mem.py), never by hand." % p, call)
        concepts_first(p, call)
    if tool == "Bash":
        cmd = inp.get("command") or ""
        if re.search(r"(^|[;&|\s(])(rm|rmdir|unlink)\s", cmd) or re.search(r"shutil\.rmtree|os\.(remove|unlink|rmdir)\(", cmd):
            block("never delete a file: supersede it with a new name (STANDING-INSTRUCTIONS §2).", call)
        RO_RX = r"(tools|stages|package|trees|shelves|\.claude)/"
        if re.search(r"(>>?|\btee(\s+-a)?)\s*(\S*/)?" + RO_RX, cmd) \
                or re.search(r"\bsed\s+-i\S*\s[^|;&]*\s(\S*/)?" + RO_RX, cmd) \
                or re.search(r"\b(mv|cp)\b[^|;&]*\s(\S*/)?" + RO_RX + r"\S*\s*($|[|;&])", cmd):
            block("the instrument's folders are read only; write in out/.", call)
        if re.search(r"(>>?|\btee(\s+-a)?)\s*\S*out/(_closes/|sealed/|_answers/|asks\.jsonl|seed\.txt|kinds-B1\.jsonl|stopping-[A-E]\d-decision)", cmd) \
                or re.search(r"\bsed\s+-i\S*\s[^|;&]*\sout/(_closes/|sealed/|_answers/|asks\.jsonl|seed\.txt|kinds-B1\.jsonl|stopping-[A-E]\d-decision)", cmd) \
                or re.search(r"\b(mv|cp)\b[^|;&]*\s\S*out/(_closes/|sealed/|_answers/|asks\.jsonl|seed\.txt|kinds-B1\.jsonl|stopping-[A-E]\d-decision)\S*\s*($|[|;&])", cmd):
            block("out/_closes/, out/sealed/, out/seed.txt, the kinds ledger, the questions and their answers, and the "
                  "PI's decisions are written by the tools or the principal investigator, never by hand.", call)
        if re.search(r"(>|>>|\btee\b|\bmv\b|\bcp\b)\s*[^|;&]*\bout/diary/", cmd):
            block("the diary is written only through python3 tools/mem.py log.", call)
        if re.search(r"saturation\.py\b[^|;&]*\bdecide\b", cmd):
            block("saturation.py decide is the PI's: write the report, log it, and close with done.sh B1 --pause "
                  "(stage B1, when to stop).", call)
    return 0


if __name__ == "__main__":
    sys.exit(main())
