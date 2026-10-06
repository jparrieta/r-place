#!/usr/bin/env python3
"""validate.py, v38: the close-check of every leg, and the open-check of every launch.

    python3 tools/validate.py NN <root> <outdir>           # at the CLOSE of a leg (done.sh runs it)
    python3 tools/validate.py --open NN [<root> <outdir>]  # at the OPEN, before any judgement
    python3 tools/validate.py --links [<root> <outdir>]    # every id in the head and questions resolves
    python3 tools/validate.py --self-test [--summary]      # every check fires on its own planted defect;
                                                           # --summary prints only the failures and the count

NN is a stage id: A1, B1 to B4, C1 to C5, D1 to D6, E1, E2. `<root>` is the folder holding `package/`, `trees/`,
`tools/`, `stages/` and `out/`; `<outdir>` is `out/`. Both default to `.` and `out`.

This checks a run, not the instrument: that the files a stage was told to produce exist, parse,
and reconcile against the store and against each other. A judgement can be right and the file
recording it can still not add up, and the file is what every later stage reads. None of these
checks can tell whether a judgement is right; a clean report is not evidence about the analysis.

Exit code 1 if any ERROR. Warnings never fail a leg.

**Coverage.** One handler per stage, in `tools/checks/stage_NN.py`, pinned by name. A stage with
no handler closes unvalidated and the report says so. Each handler is written from the stage
file's Outputs block and its Close section, and from the v37 check it descends from.

**The open-check** reads the stage file's header block: every file the Startup packet and Reads
allowed lines name must exist in the folder root, the package or the output directory; the stage
file itself must be in `stages/`; at B1 and C1 `scheme_current.jsonl` must exist, in `out/scheme/` or
`out/` (or the stage be B1's first leg). It names every declared input with where it was found,
prints the startup counts the standing instructions promise (counts.py's census, dropped,
analysed set, concepts, second-order themes), and runs links.py over the head and the questions:
an id that does not resolve fails the open at every stage.

A check keyed on the analysed set refuses when either file that defines it is absent, the store's
`rooms.jsonl` or stage A1's `dropped.jsonl`, and names what it therefore did not check; an empty
frame passes every membership test, which is the one result this file may not produce.
"""
import glob, importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vlib  # noqa: E402
from vlib import E, W, err, warn, fold  # noqa: E402

STAGE_IDS = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "E1", "E2"]
PACKAGE_FILES = {"HOW-TO-RUN.md", "README-store.md", "METHOD.md", "FLEET.md", "SCHEMA-adaptations.md", "WRITING.md",
                 "STANDING-INSTRUCTIONS.md", "CONTRACT-aggregator.md", "PRIOR-template.md",
                 "codes.jsonl", "themes.jsonl", "items.jsonl", "threads.jsonl", "rooms.jsonl",
                 "transitions.jsonl", "relations.jsonl", "neighbours.jsonl", "pointers.jsonl", "forest.jsonl",
                 "tree_index.json", "artworks.jsonl", "sealed.jsonl"}
TOOL_FILES = {"mem.py", "cite.py", "validate.py", "packets.py", "done.sh", "snap.py", "ingest.py", "prose_check.py",
              "distance.py", "rebuild.py", "gen_views.py", "handoff.py", "probe.py", "links.py",
              "counts.py", "relations.py", "transitions.py", "build_store.py", "fleet.py", "dreturn.py", "saturation.py",
              "steps.py", "vlib.py"}
SKIP = re.compile(r"(-NN\.|<sub>|-pN\.|-k/|_reads-|^_head|^diary|^story-|^handback-|^notes-NN|^RUN\.json$)")


def stage_file(root, stage):
    """The stage's file: the one step.sh named in .stagefile from DROPS/ORDER.tsv; else the one file matching
    STAGE-<stage>-*. Two matches and no .stagefile is refused, never resolved by name order (review 2026-09-29)."""
    try:
        named = open(os.path.join(root, ".stagefile"), encoding="utf-8").read().strip()
    except OSError:
        named = ""
    if named and os.path.basename(named).startswith("STAGE-%s-" % stage) and os.path.exists(os.path.join(root, named)):
        return os.path.join(root, named)
    c = sorted(glob.glob(os.path.join(root, "stages", "STAGE-%s-*.md" % stage)))
    if not c:
        c = sorted(glob.glob(os.path.join(HERE, "..", "stages", "STAGE-%s-*.md" % stage)))
    if len(c) > 1:
        sys.exit("validate.py: stage %s has %d stage files (%s) and no .stagefile names one; the handler "
                 "resolves it, never the order of names" % (stage, len(c), ", ".join(os.path.basename(x) for x in c)))
    return c[0] if c else None


def header_block(txt):
    """The bold header lines at the top of a v38 stage file, joined per key."""
    out, cur = {}, None
    for ln in txt.split("\n"):
        m = re.match(r"^\*\*([A-Za-z ,]+):\*\*\s*(.*)", ln)
        if m:
            cur = m.group(1).split(",")[0].strip().lower()   # "Startup packet, every leg" is the startup packet
            out[cur] = m.group(2)
            continue
        if ln.startswith("## "):
            break
        if cur and ln.strip():
            out[cur] += " " + ln.strip()
        elif not ln.strip():
            cur = None
    return out


def open_check(stage, root, pkg, outdir):
    sf = stage_file(root, stage)
    if not sf:
        err("stage %s's document is not in stages/. Do not reconstruct it from the contract or from "
            "memory: say it is missing and stop." % stage)
        return
    txt = open(sf, encoding="utf-8").read()
    hb = header_block(txt)
    print("stage %s opens: %s" % (stage, os.path.basename(sf)))
    FILE = r"`([A-Za-z0-9_./<>-]+\.(?:jsonl|md|json|tsv|txt|sha256|py))`"
    NEVER = re.compile(r"\(never\s+`[^`]+`\)")               # "(never `assign_final.jsonl`)" names a file not to read
    reads = set(re.findall(FILE, NEVER.sub("", hb.get("reads allowed", ""))))
    packet = set(re.findall(FILE, NEVER.sub("", hb.get("startup packet", "")))) - reads
    declared = reads | packet
    first_leg = not vlib.diary_lines(outdir, stage)
    missing, named = [], []
    for f in sorted(declared):
        b = os.path.basename(f)
        if SKIP.search(f) or b == "this file":
            named.append((f, "not checked here (a per-room, per-stage or harness name)"))
            continue
        if b in PACKAGE_FILES or b in TOOL_FILES:
            named.append((f, "shipped with the package or the tools"))
            continue
        places = (os.path.join(outdir, f), os.path.join(outdir, b), os.path.join(root, f),
                  os.path.join(root, b), os.path.join(pkg, f), os.path.join(pkg, b),
                  os.path.join(root, "handoff", b))
        hit = next((q for q in places if os.path.exists(q) or glob.glob(q)), None)
        if hit is None and f in packet and first_leg:
            # the startup packet's files are the previous leg's; at a stage's first leg some are not
            # written yet (the previous pass's tail, the head at A1), so an absence warns
            warn("stage %s names `%s` in its startup packet and it is absent; this is the stage's first "
                 "leg (no diary line yet), so it is a warning here and an error from the next leg" % (stage, f))
            named.append((f, "absent (first leg: a warning)"))
        elif hit is None:
            missing.append(f)
            named.append((f, "MISSING"))
        else:
            named.append((f, "present: %s" % os.path.relpath(hit, root)))
    for f in missing:
        err("stage %s names `%s` in its startup packet or reads, and it is not in the folder root, the "
            "package or the output directory. The previous stage did not finish, or did not write it."
            % (stage, f))
    if stage == "C1" and not os.path.exists(os.path.join(outdir, "scheme_final.jsonl")):
        err("stage C1: scheme_final.jsonl is not in out/; C1 reads the frozen scheme (stage B2), paged")
    if stage == "B1":
        sc = os.path.join(outdir, "scheme", "scheme_current.jsonl")
        if not os.path.exists(sc):
            sc = os.path.join(outdir, "scheme_current.jsonl")
        if not os.path.exists(sc):
            warn("stage B1: scheme_current.jsonl is not in out/; it is a required startup read at every B1 leg "
                 "after the first mint")
    head = os.path.join(outdir, "_head.md")
    if stage != "A1" and not os.path.exists(head):
        err("_head.md is absent; it is read first at every leg")
    hw = len(vlib.text(outdir, "_head.md").split())
    if hw > 3200:
        err("_head.md is %d words; the ceiling is 3,200 (3,000 and a margin)" % hw)
    d = vlib.diary_lines(outdir, stage)
    print("  %d declared inputs, %d missing; head %d words; %d diary lines for this stage"
          % (len(declared), len(missing), hw, len(d)))
    for f, where in named:
        print("    %-44s %s" % (f, where))
    c, why, fatal = None, "the store holds no rooms (%s)" % os.path.join(pkg, "store", "rooms.jsonl"), True
    try:
        import counts
        c = counts.compute(root, outdir)
    except Exception as e:                  # a copy of validate.py without counts.py beside it
        why, fatal = "counts.py did not run here (%s); run python3 tools/counts.py" % e, False
    if c is None:
        (err if fatal else warn)("stage %s: no startup counts: %s" % (stage, why))
    else:
        print("  counts (counts.py): census %d rooms; dropped %s; analysed %s; concepts %d census, %d in scope; "
              "second-order themes %d census, %d in scope; rooms without a theme %d; scope: %s"
              % (c["census_rooms"], c["dropped"], c["analysed_rooms"], c["concepts"]["census"],
                 c["concepts"]["scope"], c["themes"]["census"], c["themes"]["scope"],
                 len(c["rooms_without_theme"]), c["scope"]))
    links_check(root, outdir)


def links_check(root, outdir):
    try:
        import links
    except ImportError:
        err("tools/links.py is not beside validate.py")
        return
    rc = links.run(root, outdir, quiet=False) if hasattr(links, "run") else os.system(
        "python3 %s --out %s --root %s" % (os.path.join(HERE, "links.py"), outdir, root))
    if rc:
        err("links.py found ids that do not resolve; read its report")


def close_check(stage, root, pkg, outdir):
    ctx = {"package": pkg, "root": root, "outdir": outdir, "stage": stage}
    vlib.rooms(ctx)
    logs = glob.glob(os.path.join(outdir, "_mem_reads-%s.jsonl" % stage)) + \
        glob.glob(os.path.join(outdir, "_cite_reads-%s.jsonl" % stage))
    if not logs:
        warn("no _mem_reads-%s.jsonl or _cite_reads-%s.jsonl: rule 1 says the logs are an output" % (stage, stage))
    if not vlib.diary_lines(outdir, stage):
        err("the diary holds no line for stage %s; you write as you work (rule 20)" % stage)
    if stage != "A1" and not os.path.exists(os.path.join(outdir, "_head.md")):
        err("_head.md is absent; it is read first at every leg")
    leg = (open(os.path.join(root, ".leg"), encoding="utf-8").read().strip()
           if os.path.exists(os.path.join(root, ".leg")) else "")
    for ln in (vlib.text(outdir, "_closes/guard.log") or "").splitlines():   # review 2026-09-29
        try:
            g = json.loads(ln)
        except ValueError:
            continue
        if leg and g.get("leg") == leg and str(g.get("why", "")).startswith("compaction gate opened"):
            warn("leg %s: %s. The recovery was not completed; it is an exception, and the handback says what "
                 "was owed and whether it was done later" % (leg, g["why"]))
    hw = len(vlib.text(outdir, "_head.md").split())
    if hw > 3200:
        err("_head.md is %d words; the ceiling is 3,200 (3,000 and a margin)" % hw)
    try:
        mod = importlib.import_module("checks.stage_%s" % stage)
    except ImportError as e:
        mod = None
        why = str(e)
    if mod is None or not hasattr(mod, "check"):
        err("stage %s has NO close-check (tools/checks/stage_%s.py: %s). Only the common checks ran; "
            "record in the handback that the leg closed unvalidated." % (stage, stage, why if mod is None else "no check()"))
    else:
        print("stage %s:" % stage)
        mod.check(root, outdir, ctx)


def report():
    ef, wf = fold(E), fold(W)
    print()
    for m in ef:
        print("ERROR  %s" % m)
    for m in wf:
        print("warn   %s" % m)
    print("\n%d errors (%d distinct shapes), %d warnings" % (len(E), len(ef), len(W)))
    return 1 if E else 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--self-test":
        import checks.selftest as st
        return st.run(HERE, summary="--summary" in argv[1:])
    mode = "close"
    if argv[0] in ("--open", "--links"):
        mode = argv[0][2:]
        argv = argv[1:]
    stage = argv[0] if mode != "links" else None
    rest = argv[1:] if stage is not None else argv
    root, pkg = vlib.resolve_root(rest[0] if rest else ".")
    outdir = rest[1] if len(rest) > 1 else os.path.join(root, "out")
    if stage is not None:
        stage = stage.upper()
        if stage not in STAGE_IDS:
            print("no such stage: %s (one of %s)" % (stage, ", ".join(STAGE_IDS)))
            return 2
    if mode == "open":
        open_check(stage, root, pkg, outdir)
    elif mode == "links":
        links_check(root, outdir)
    else:
        close_check(stage, root, pkg, outdir)
    return report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
