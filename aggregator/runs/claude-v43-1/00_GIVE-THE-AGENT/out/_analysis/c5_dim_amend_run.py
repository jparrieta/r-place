#!/usr/bin/env python3
"""C5a-02: run the dimension amendments one after another, each followed by its own diary line (mem.py log --kind
move, the Grodal, Anteby and Holm move named) and its own snap, stopping at the first failure. One dimension, one move,
one snap, in order. Writes through the three tools only.

    python3 out/_analysis/c5_dim_amend_run.py FIRST_SNAP_NUMBER D0n [D0n ...]
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = json.load(open(os.path.join(ROOT, "out", "_analysis", "c5_dim_amend.json"), encoding="utf-8"))
n = int(sys.argv[1])


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    out = "\n".join(l for l in (p.stdout + p.stderr).splitlines() if "Deprecation" not in l and "utcnow" not in l)
    print(out.strip())
    if p.returncode:
        sys.exit("stopped: %s" % " ".join(args))


for did in sys.argv[2:]:
    s = spec[did]
    run([os.path.join("out", "_analysis", "c5_dim_amend.py"), did])
    label = s["move"].split()[0]
    run([os.path.join("tools", "mem.py"), "log", "Move (%s), declaration prose rule extended to the dimensions, %s: "
         "%s rewritten; %s. Findings touched (rule 14): none rests on the dimension's prose; unchanged." % (
             s["move"], did, " and ".join(s["now"]), s["why"]), "--kind", "move", "--ids", did])
    run([os.path.join("tools", "snap.py"), "C5", "move-%s-%d" % (label, n)])
    n += 1
