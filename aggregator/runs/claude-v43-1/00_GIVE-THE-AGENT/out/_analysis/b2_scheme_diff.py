#!/usr/bin/env python3
"""Compare two scheme files theme by theme and field by field; print the themes and fields that differ. Reads only.
    python3 out/_analysis/b2_scheme_diff.py out/_analysis/scheme_round3.jsonl out/scheme.jsonl"""
import json, sys

a, b = ({r["id"]: r for r in (json.loads(x) for x in open(p, encoding="utf-8") if x.strip())} for p in sys.argv[1:3])
print("ids only in the first: %s; only in the second: %s" % (sorted(set(a) - set(b)), sorted(set(b) - set(a))))
n = 0
for t in sorted(set(a) & set(b)):
    fs = sorted(k for k in set(a[t]) | set(b[t]) if a[t].get(k) != b[t].get(k))
    if fs:
        n += 1
        print("%s: %s" % (t, ", ".join(fs)))
print("%d themes differ" % n)
