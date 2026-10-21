#!/usr/bin/env python3
"""D3a-48: print the statement and range of elements, or the connection, mechanism and bound of arrows, from
out/model/elements.jsonl and out/model/arrows.jsonl, whole, for the ids given. Writes nothing.

  python3 out/_analysis/d3_statements.py --ids P07 P05 A16
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--ids", nargs="+", required=True)
a = ap.parse_args()
recs = {}
for p in ("out/model/elements.jsonl", "out/model/arrows.jsonl"):
    for l in open(p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            recs[r["id"]] = r
for i in a.ids:
    r = recs.get(i)
    if r is None:
        print("== %s: not found" % i)
        continue
    print("== %s (%s)" % (i, r.get("status", r.get("kind", ""))))
    for k in ("statement", "range", "from", "to", "connection", "mechanism", "bound"):
        if r.get(k):
            print("  %s: %s" % (k, r[k]))
