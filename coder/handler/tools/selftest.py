#!/usr/bin/env python3
"""selftest.py — run one room through the whole procedure with scripted agents.

No model is called. A scripted coder (simcoder.py) plays every fleet coder; this script plays
the case lead and the brief writer's harness. It exercises: newrun, the gate (branch A or B),
dispatch/collect for every slice, consolidate, emit.close(), the forest, audit_fleet, one theme
pass, emit.close(verdict), close_run for the lead and every coder, and read.py audit on every
directory. Exit 0 only if everything passed. Use it to prove an installation of the yard on a
new machine before any real agent runs, and after any change to the instrument.

    python3 _tools/selftest.py --instrument _instrument/v30 --record <coder_corpus.jsonl> \
        --sub <sub> [--brief brief.md] [--threshold 500] [--budget 500] [--out /tmp/selftest_x]
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd, cwd, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("FAILED:", " ".join(cmd), "\n", r.stdout[-2000:], r.stderr[-2000:])
        sys.exit(1)
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--sub", required=True)
    ap.add_argument("--brief")
    ap.add_argument("--threshold", type=int, default=500)
    ap.add_argument("--budget", type=int, default=500)
    ap.add_argument("--out")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    inst = os.path.abspath(a.instrument)
    out = os.path.abspath(a.out) if a.out else tempfile.mkdtemp(prefix="selftest_")
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    run = os.path.join(out, "run")
    brief = a.brief
    if not brief:
        brief = os.path.join(out, "brief.md")
        os.makedirs(out, exist_ok=True)
        open(brief, "w").write("# Brief: r/%s\n\n(self-test: no brief)\n" % a.sub)
    sh(["python3", os.path.join(inst, "newrun.py"), run, a.sub, os.path.abspath(a.record),
        os.path.abspath(brief), "scripted"], cwd=out)
    print("built", run)
    plan = sh(["python3", "tools/fleet.py", "plan", "--threshold", str(a.threshold),
               "--budget", str(a.budget)], cwd=run)
    gate = json.load(open(os.path.join(run, "out", "_gate.json")))
    branch = gate["branch"]
    print("branch", branch, "slices", len(gate["slices"]))
    sys.path.insert(0, run)
    if branch == "B":
        for s in gate["slices"]:
            b = s["batch"]
            sh(["python3", "tools/fleet.py", "dispatch", "--batch", b, "--model", "scripted"],
               cwd=run)
            bdir = os.path.join(run, "fleet", "batch_%s" % b)
            sh(["python3", os.path.join(HERE, "simcoder.py"), bdir, b], cwd=bdir)
            # the scheduler's pre-consolidation read audit
            aud = json.loads(sh(["python3", "read.py", "corpus.txt", "audit"], cwd=bdir))
            over = [m for m in aud["mismatches"] if m["kind"] == "overstated"]
            assert aud["checked"] and not over, aud
            sh(["python3", "tools/fleet.py", "collect", "--batch", b], cwd=run)
            print("  batch", b, "coded and collected; read audit", aud["source"],
                  aud["declared"], "declared, 0 overstated")
        sh(["python3", "tools/fleet.py", "consolidate"], cwd=run)
        codes_file = "package/codes.jsonl"
    else:
        # branch A: the lead codes the room itself; simcoder plays it as a single reader
        sh(["python3", os.path.join(HERE, "simcoder.py"), run, "00"], cwd=run)
        codes_file = "out/codes.jsonl"
    # the lead's phase 3
    from emit import Emit
    emit = Emit(os.path.join(run, "out"), corpus_path=os.path.join(run, "coder_corpus.jsonl"))
    r1 = emit.close()
    print("close():", "codes", r1["n_codes"], "threads", r1["n_threads"])
    sh(["python3", "tools/tree_builder.py", "--sub", a.sub, "--record", "coder_corpus.jsonl",
        "--codes-file", codes_file, "--out-dir", "."], cwd=run)
    aud = sh(["python3", "tools/audit_fleet.py", "--run", ".", "--sub", a.sub] +
             ([] if branch == "B" else ["--branch", "A"]), cwd=run)
    print(aud.strip().splitlines()[-1])
    assert aud.strip().endswith("PASSED"), aud
    emit.stage("step4_themes")
    ids = [c["code_id"] for c in emit.codes]
    if ids:
        half = max(1, len(ids) // 2)
        emit.theme("scripted theme one", "self-test", ids[:half])
        if ids[half:]:
            emit.theme("scripted theme two", "self-test", ids[half:])
    emit.stage("step5_counter")
    emit.stage("step7_write")
    open(os.path.join(run, "out", "case.md"), "w").write(
        "# r/%s (self-test)\n\n## Chronology\n\nscripted\n\n## Relations — what set off what\n\n"
        "none\n\n## Posts against comments\n\nnone\n\n## Counter-reading\n\nscripted\n\n"
        "## Saturation\n\nscripted\n\n## Selection\n\nscripted\n\n## Absence\n\nscripted\n" % a.sub)
    gate_line = ("branch B; threshold %s; items_in_window %s; chars_by_people %s\n"
                 % (gate.get("threshold"), gate.get("items_in_window"),
                    gate.get("chars_by_people"))) if branch == "B" else "branch A\n"
    open(os.path.join(run, "out", "notes.md"), "w").write("self-test notes\n" + gate_line)
    open(os.path.join(run, "out", "_transcript.jsonl"), "w").write(
        json.dumps({"type": "assistant", "message": {"model": "scripted", "content": "self-test"}}) + "\n")
    r2 = emit.close(verdict="trace")
    print("close(verdict):", r2["verdict"], "themes", r2["n_themes"])
    cr = sh(["python3", "close_run.py", ".", "--role", "lead"], cwd=run, check=False)
    print(cr.strip().splitlines()[-1])
    assert re.search(r"(\d+) of \1 checks passed", cr), cr
    if branch == "B":
        for s in gate["slices"]:
            bdir = os.path.join(run, "fleet", "batch_%s" % s["batch"])
            open(os.path.join(bdir, "out", "_transcript.jsonl"), "w").write(
                json.dumps({"type": "assistant", "message": {"model": "scripted"}}) + "\n")
            cr = sh(["python3", "close_run.py", ".", "--role", "fleet"], cwd=bdir, check=False)
            assert re.search(r"(\d+) of \1 checks passed", cr), (s["batch"], cr)
        print("close_run fleet: every check on every batch")
    print("SELFTEST PASSED", "branch", branch, "slices", len(gate["slices"]), "codes", r2["n_codes"])
    if not a.keep and not a.out:
        shutil.rmtree(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
