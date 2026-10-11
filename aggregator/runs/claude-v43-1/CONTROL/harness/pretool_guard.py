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
From 2026-10-11 (J): reads of placement files are refused in a blind window (mem.py blind); no column cut
after mem.py, cite.py or a helper; awk without system(); pipes after mem.py and cite.py are recorded.
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
    # J, 7 October 2026: the form's writing rules (length, quoting) are guides the analyst judges;
    # only errors (pass/fail) refuse. Warnings come back as advice and the note stands.
    errs = [x for x in probs if x[0] == "err"]
    if not errs:
        import json
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext":
              "rooms/%s.md stands; advice only, your judgement:\n%s" % (m.group(1), "\n".join("- " + x[1] for x in probs))}}))
        return 0
    print("rooms/%s.md, fix it now:\n%s" % (m.group(1), "\n".join("- " + x[1] for x in errs)), file=sys.stderr)
    return 2


def rel(p):
    if not p:
        return ""
    try:
        return os.path.relpath(os.path.join(BASE, p), BASE).replace(os.sep, "/")
    except ValueError:
        return p


QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
SHELL_RM = re.compile(r"(^|[;&|\s(])(rm|rmdir|unlink)(\s|$)")


def deletes(cmd):
    """A delete in a Bash command. The shell words rm, rmdir and unlink count only outside quoted text, so a
    quotation that holds the letters is not a delete (J, 2026-10-06, after A1b-15's false block); text quoted
    for a shell that runs it (sh -c, bash -c, zsh -c, eval) is still read, and Python's file deletes are read
    everywhere."""
    if re.search(r"shutil\.rmtree|os\.(remove|unlink|rmdir)\(", cmd):
        return True
    bare = QUOTED.sub(" '' ", cmd)
    if SHELL_RM.search(bare):
        return True
    if re.search(r"\b(ba|z)?sh\s+-c\b|\beval\b", bare):
        return any(SHELL_RM.search(q[1:-1]) for q in QUOTED.findall(cmd))
    return False


# ---- J, 2026-10-11: blind windows, whole room reads, read-only awk, and the record of pipes ---------------
# Files that hold placements, the analyst's own or the readers'. While a blind window is open
# (out/_blind.json, written by mem.py blind) a direct read of any of them is refused; the scheme is read
# through `mem.py scheme <id>` and `mem.py gates`, which withhold members and exemplars in the window.
BLIND_FILES = re.compile(
    r"(scheme_current|scheme_final|scheme_v2|scheme|assignments_final|assign_final|assign_raw|assign_pass2|"
    r"assign_revisions_only|multiplacement_log|tier_history|author_items|gold_items|pilot_rounds|scheme_edits|"
    r"disagreements|findings|gate_history|gate_checks|theme_discovery)\.jsonl|kinds-[A-E]\d\.jsonl|unplaced-[A-E]\d\.jsonl|"
    r"episodes-[A-E]\d\.jsonl|rechecks-[A-E]\d\.jsonl|scheme(_final|_v2)?\.md|confusions\.md|notes-[A-E]\d\.md|"
    r"handback-[A-E]\d\.md|saturation-[A-E]\d\.md|_fleet_raw/|out/diary/|_views/|_wiki/|_mem_reads-")
READERS = re.compile(r"\b(mem|cite)\.py\b|out/_analysis/")


def blind_open():
    try:
        d = json.load(open(os.path.join(BASE, "out", "_blind.json"), encoding="utf-8"))
        return isinstance(d, dict) and d.get("on") is True
    except Exception:
        return False


def blind_reads(tool, inp, call):
    if not blind_open():
        return
    if tool in ("Read", "Grep", "Glob"):
        target = " ".join(str(inp.get(k) or "") for k in ("file_path", "path", "pattern", "glob"))
    elif tool == "Bash":
        target = inp.get("command") or ""
        if re.search(r"mem\.py\s+blind\b", target):
            return
    else:
        return
    m = BLIND_FILES.search(target)
    if m:
        block("a blind window is open (mem.py blind): %s holds placements and is not read until mem.py blind off. Read "
              "the items through mem.py theme and codes --sub, the gates through mem.py scheme <id> and mem.py gates."
              % m.group(0), call)


def pipes(cmd, call):
    """Room reads are read whole (J, 2026-10-11): no cut by column after mem.py, cite.py or a helper in
    out/_analysis/; mem.py --width clips and the read log records it. awk reads; it does not run commands.
    Every pipe after mem.py or cite.py is recorded in out/_mem_pipes-<stage>.jsonl, so the record says what
    reached the screen."""
    bare = QUOTED.sub(" '' ", cmd)
    segs = re.split(r"(?<!\|)\|(?!\|)", cmd)
    if READERS.search(cmd) and len(segs) > 1:
        if re.search(r"(^|[|;&]\s*)(cut\s+[^|;&]*-[a-z]*[cb]|colrm\b)", bare):
            block("room reads are read whole (J, 2026-10-11): no cut -c, cut -b or colrm after mem.py, cite.py or a "
                  "helper. To narrow a page, pass --width N to mem.py: it clips and the read log records it.", call)
        try:
            d = os.path.join(BASE, "out")
            with open(os.path.join(d, "_mem_pipes-%s.jsonl" % (_read(".stage") or "xx")), "a", encoding="utf-8") as f:
                f.write(json.dumps({"t": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"), "leg": _read(".leg"),
                                    "cmd": cmd[:2000]}) + "\n")
        except Exception:
            pass
    if re.search(r"(^|[|;&]\s*)awk\b", bare) and re.search(r"\bsystem\s*\(", cmd):
        block("awk is allowed for reading: system() runs commands and is refused. Use python3 in out/_analysis/.", call)


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
    blind_reads(tool, inp, call)
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
        if deletes(cmd):
            block("never delete a file: supersede it with a new name (STANDING-INSTRUCTIONS §2).", call)
        pipes(cmd, call)
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
