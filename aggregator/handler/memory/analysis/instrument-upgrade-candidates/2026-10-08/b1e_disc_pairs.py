#!/usr/bin/env python3
"""B1e: does each owed discriminator pair appear in both themes' gates (scheme.jsonl)?

Usage: python3 out/_analysis/b1e_disc_pairs.py T3-068/T3-061 T3-010/T3-149 ...
A pair with three ids is checked two by two.
"""
import itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = {}
with open(os.path.join(ROOT, "out", "scheme.jsonl"), encoding="utf-8") as f:
    for x in f:
        r = json.loads(x)
        rows[r["id"]] = {d["vs"] for d in r["discriminators"]}
for arg in sys.argv[1:]:
    ids = arg.split("/")
    for a, b in itertools.combinations(ids, 2):
        print("%s vs %s: %s; %s vs %s: %s" % (a, b, "yes" if b in rows[a] else "NO", b, a, "yes" if a in rows[b] else "NO"))
