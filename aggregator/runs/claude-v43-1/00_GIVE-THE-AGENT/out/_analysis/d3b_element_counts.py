#!/usr/bin/env python3
"""D3b: for one element (or several, comma-separated), count its re-check lines by op and by the last ruling's
decision and kind, and the lines still unruled, for the element-close note. Reads only.

    python3 out/_analysis/d3b_element_counts.py --element P05
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
a = ap.parse_args()

last = {}
for l in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        last[r["adaptation"]] = r
rows = [json.loads(l) for l in open(os.path.join(OUT, "adaptations-recheck.jsonl"), encoding="utf-8") if l.strip()]
for e in a.element.split(","):
    mine = [r for r in rows if r.get("element") == e]
    by = collections.defaultdict(collections.Counter)
    tot = collections.Counter()
    rooms = set()
    for r in mine:
        rooms.add(r["sub"])
        j = last.get(r["id"])
        key = "unruled" if j is None else "%s/%s" % (j["decision"], j.get("kind"))
        by[r["op"]][key] += 1
        tot[key] += 1
    print("%s: %d re-check lines in %d rooms; %s" % (e, len(mine), len(rooms), dict(sorted(tot.items()))))
    for op in sorted(by):
        print("   %-14s %4d  %s" % (op, sum(by[op].values()), dict(sorted(by[op].items()))))
