#!/usr/bin/env python3
"""D3b: run d3b_adjudicate_batch.py over several rulings files. Without --write, a dry run of each. With --write, a dry
run of every file first; only if all pass is each file written, in the order given (each write is checked again by the
batch adjudicator). Prints each file's line. Stops at the first failure.

    python3 out/_analysis/d3b_adjudicate_many.py out/_analysis/d3_rulings/a.jsonl out/_analysis/d3_rulings/b.jsonl [--write]
"""
import os, subprocess, sys

AN = os.path.dirname(os.path.abspath(__file__))
args = [x for x in sys.argv[1:] if x != "--write"]
write = "--write" in sys.argv[1:]
if not args:
    sys.exit("name at least one rulings file")


def run(f, w):
    cmd = [sys.executable, os.path.join(AN, "d3b_adjudicate_batch.py"), "--file", f] + (["--write"] if w else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print(out)
    if r.returncode:
        sys.exit("stopped at %s" % f)


for f in args:
    run(f, False)
if write:
    for f in args:
        run(f, True)
