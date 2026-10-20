#!/usr/bin/env python3
"""D3a-38: counts only, never a line. For each element (and the unattached propose lines), the ledger's lines and
how many have no adjudication yet, by op, so the next leg's group can be chosen. Elements with every line ruled are
summed at the end.

  python3 out/_analysis/d3_unruled.py
"""
import collections
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ruled = set()
for l in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8"):
    if l.strip():
        ruled.add(json.loads(l)["adaptation"])
tot = collections.Counter()
left = collections.defaultdict(collections.Counter)
for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    e = d.get("element") or "(propose)"
    tot[e] += 1
    if d["id"] not in ruled:
        left[e][d.get("op")] += 1
done = [e for e in tot if not left[e]]
print("elements with unruled lines: %d; fully ruled: %d (%d lines)" % (
    sum(1 for e in tot if left[e]), len(done), sum(tot[e] for e in done)))
for e in sorted((e for e in tot if left[e]), key=lambda e: -sum(left[e].values())):
    print("  %-10s lines %5d  unruled %5d  %s" % (e, tot[e], sum(left[e].values()), dict(left[e])))
