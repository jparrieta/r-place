#!/usr/bin/env python3
"""D3: print the current statements of named elements and arrows from out/model/, for G4a rulings.
Elements: statement and range. Arrows: from, to, connection, and any bound or mechanism fields. Writes nothing.

    python3 out/_analysis/d3_statements.py --ids P09 A15 A16 P22
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--ids", nargs="+", required=True)
a = ap.parse_args()
want = set(a.ids)
seen = set()
for name in ("elements.jsonl", "arrows.jsonl"):
    with open(os.path.join(OUT, "model", name)) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("id") not in want:
                continue
            seen.add(r["id"])
            print("== %s (%s, %s)" % (r["id"], r.get("kind"), r.get("status", "")))
            if name == "arrows.jsonl":
                print("   %s -> %s" % (r.get("from"), r.get("to")))
            for k in ("statement", "range", "connection", "bound", "mechanism", "scope"):
                if r.get(k):
                    print("   %s: %s" % (k, r[k]))
print("missing: %s" % sorted(want - seen))
