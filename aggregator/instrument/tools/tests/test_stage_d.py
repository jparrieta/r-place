#!/usr/bin/env python3
"""test_stage_d.py: stage D's plumbing end to end on the D2 self-test fixture (audit 2026-09-29, H10 to H12, M25).

    python3 tools/tests/test_stage_d.py

1. ingest.py D compiles the ledger, the verdicts, the room copies and the RUN.json counts from the drops and
   the verdict fleet's returns, and the D2 close-check then raises nothing: one rule set, two users.
2. a room whose return breaks a rule is marked unreturned by the compile, never edited.
3. the re-check compiles with ids R-<sub>-<content-and-version-digest>-NNN.
4. --relift brings every lift to the placements as they stand, and relift_problems then finds none.
"""
import contextlib, glob, io, json, os, shutil, subprocess, sys, tempfile

T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, T)
import vlib
from checks import selftest, stage_D2
import ingest

FAILS = []


def check(name, cond, got=""):
    print("%s %s" % ("ok  " if cond else "FAIL", name))
    if not cond:
        FAILS.append(name)
        if got:
            print("     ", str(got)[:400])


def run_ingest(root, out, *extra):
    r = subprocess.run([sys.executable, os.path.join(T, "ingest.py"), "D", "--root", root, "--out", out] + list(extra),
                       capture_output=True, text=True)
    if not extra:                          # as step.sh does after the compile
        subprocess.run([sys.executable, os.path.join(T, "gen_views.py"), "D2", "--root", root, "--out", out],
                       capture_output=True, text=True)
    return r


def fixture():
    root = tempfile.mkdtemp(prefix="stage-d-")
    out = selftest.write_fixture(root)
    cwd = os.getcwd()
    os.chdir(root)
    with contextlib.redirect_stdout(io.StringIO()):
        stage_D2.plant_base(out, root)
    os.chdir(cwd)
    aside = os.path.join(root, "_aside")
    os.makedirs(aside)
    for f in ("adaptations.jsonl", "verdicts-D.jsonl", "ingest-D.md"):
        shutil.move(os.path.join(out, f), os.path.join(aside, f))
    for d in glob.glob(os.path.join(out, "rooms", "*")):
        if os.path.isdir(d):
            shutil.move(d, os.path.join(aside, os.path.basename(d)))
    run = json.load(open(os.path.join(root, "RUN.json")))
    run.pop("stage_D2", None)
    json.dump(run, open(os.path.join(root, "RUN.json"), "w"))
    return root, out


def d2_errors(root, out):
    vlib.E.clear(); vlib.W.clear()
    ctx = {"package": os.path.join(root, "package"), "root": root, "outdir": out, "stage": "D2"}
    vlib.rooms(ctx)
    cwd = os.getcwd()
    os.chdir(root)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            stage_D2.check(root, out, ctx)
    finally:
        os.chdir(cwd)
    return [m for m, _s, _w in vlib.E]


def main():
    # 1. the compile, then the D2 check
    root, out = fixture()
    r = run_ingest(root, out)
    check("ingest.py D compiles", r.returncode == 0, r.stdout + r.stderr)
    check("the room copies are beside the notes", all(os.path.exists(os.path.join(out, "rooms", s, f))
          for s in ("denmark", "asoiaf") for f in ("model-D.md", "verdict-D.jsonl")))
    run = json.load(open(os.path.join(root, "RUN.json")))
    check("RUN.json carries the D2 counts", run.get("D2", {}).get("accepted") == 2, run.get("D2"))
    errs = d2_errors(root, out)
    check("the D2 close-check raises nothing on the compiled files", not errs, errs[:3])

    # 2. a rejected room is unreturned, never edited
    root, out = fixture()
    lp = os.path.join(root, "DROPS", "D", "asoiaf", "adaptations.jsonl")
    before = open(lp).read()
    open(lp, "w").write(before.replace('"op": "', '"op": "nonsense-', 1))
    run_ingest(root, out)
    un = open(os.path.join(root, "DROPS", "D", "UNRETURNED.tsv")).read() \
        if os.path.exists(os.path.join(root, "DROPS", "D", "UNRETURNED.tsv")) else ""
    check("a room that breaks a rule is marked unreturned by the compile", "asoiaf\trejected by ingest.py" in un, un)
    check("the return itself is not edited", open(lp).read() == before.replace('"op": "', '"op": "nonsense-', 1))
    errs = d2_errors(root, out)
    check("the D2 close-check passes with a room unreturned", not errs, errs[:3])
    # the readers' ids come from their files, whatever a reader wrote
    root, out = fixture()
    for f in glob.glob(os.path.join(out, "_fleet_raw", "D2v", "*", "r*.jsonl")):
        rows = [json.loads(l) for l in open(f) if l.strip()]
        open(f, "w").write("".join(json.dumps(dict(r, reader="r1")) + "\n" for r in rows))
    run_ingest(root, out)
    errs = d2_errors(root, out)
    check("two readers who both wrote r1 are told apart by their files", not errs, errs[:3])

    # 3. the re-check's ids
    root, out = fixture()
    shutil.copytree(os.path.join(out, "handoff-D"), os.path.join(out, "handoff-D", "recheck"),
                    ignore=shutil.ignore_patterns("recheck", "tasks"))
    os.makedirs(os.path.join(root, "DROPS", "D", "recheck"), exist_ok=True)
    shutil.copytree(os.path.join(root, "DROPS", "D", "denmark"), os.path.join(root, "DROPS", "D", "recheck", "denmark"))
    r = run_ingest(root, out, "--recheck")
    rows = [json.loads(l) for l in open(os.path.join(out, "adaptations-recheck.jsonl"))] \
        if os.path.exists(os.path.join(out, "adaptations-recheck.jsonl")) else []
    check("the re-check's ledger ids are R-<sub>-<content-and-version-digest>-NNN", rows and all(x["id"].startswith("R-denmark-") for x in rows)
          and all(x["origin"] == "recheck" for x in rows), [x.get("id") for x in rows] or r.stdout + r.stderr)

    # 4. the re-lift
    root, out = fixture()
    run_ingest(root, out)
    af = os.path.join(out, "assignments_final.jsonl")
    rows = [json.loads(l) for l in open(af)]
    for x in rows:
        x["third_order"] = ["T3-099"]
    open(af, "w").write("".join(json.dumps(x) + "\n" for x in rows))
    stale = ingest.relift_problems(root, out)
    check("a moved placement leaves the ledger stale", bool(stale), stale)
    r = run_ingest(root, out, "--relift")
    check("--relift re-lifts", r.returncode == 0 and "re-lifted" in r.stdout, r.stdout + r.stderr)
    check("and nothing is stale after it", not ingest.relift_problems(root, out), ingest.relift_problems(root, out))
    print("stage D: %d failed" % len(FAILS))
    return 1 if FAILS else 0


sys.exit(main())
