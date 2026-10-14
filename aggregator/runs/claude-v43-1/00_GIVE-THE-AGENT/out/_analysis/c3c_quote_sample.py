#!/usr/bin/env python3
"""C3c: a seeded sample of coded records for third-order themes, to choose quotes for literature-C3.md's four-problems
section (the remainder, the goal, reward and allocation). Draws from the store through `mem.py codes --third <id>
--json` (the label field is first_order), samples N records per theme with seed 20261014, and prints room/code, the
first-order label and the text whole. A chosen quote is then served through cite.py. Writes nothing.

    python3 out/_analysis/c3c_quote_sample.py [--n N] T3-xxx [T3-yyy ...]
"""
import argparse, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=3)
ap.add_argument("ids", nargs="+")
a = ap.parse_args()
rng = random.Random(20261014)
for t in a.ids:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--third", t, "--json"],
                       cwd=ROOT, capture_output=True, text=True)
    recs = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
    pick = rng.sample(recs, min(a.n, len(recs)))
    print("== %s: %d records" % (t, len(recs)))
    for r in pick:
        print("  %s/%s [%s] %s" % (r["sub"], r["code_id"], r["first_order"], r["text"].replace("\n", " ")))
