#!/usr/bin/env python3
"""D3a-55, read-only: the shape of the unattached propose lines, counts only: how many, in how many rooms, the fields
they carry, how many have an unplaced source (no third-order node in the lift), how many are NONPORTABLE, and the
counts by the lift's third-order node, fourth-order node and dimension. Prints no line's content. Writes nothing.

  python3 out/_analysis/d3_propose_shape.py
"""
import json
from collections import Counter

L = [json.loads(l) for l in open("out/adaptations.jsonl", encoding="utf-8") if l.strip()]
P = [l for l in L if l.get("op") == "propose"]
print("propose lines: %d in %d rooms" % (len(P), len({l["sub"] for l in P})))
print("fields:", dict(Counter(k for l in P for k in l if l.get(k) not in (None, "", [], {}))))
lift = lambda l, i: (l.get("lift") or [None] * 4)[i] if len(l.get("lift") or []) > i else None
print("element values:", dict(Counter(str(l.get("element")) for l in P)))
print("source unplaced (no T3): %d; NONPORTABLE: %d; kinds: %s" % (
    sum(1 for l in P if not lift(l, 1)), sum(1 for l in P if l.get("portable") is False),
    dict(Counter(str(l.get("kind")) for l in P))))
c3 = Counter(lift(l, 1) or "none" for l in P)
c4 = Counter(lift(l, 2) or "none" for l in P)
cd = Counter(lift(l, 3) or "none" for l in P)
print("distinct T3 nodes: %d; top 25: %s" % (len(c3), c3.most_common(25)))
print("by T3 count of lines: %s" % dict(sorted(Counter(c3.values()).items())))
print("T4 nodes: %d; %s" % (len(c4), c4.most_common(30)))
print("dimensions: %s" % dict(cd.most_common()))
rooms3 = {}
for l in P:
    rooms3.setdefault(lift(l, 1) or "none", set()).add(l["sub"])
print("T3 nodes with 3+ rooms: %d; with 2 rooms: %d; with 1 room: %d" % (
    sum(1 for v in rooms3.values() if len(v) >= 3), sum(1 for v in rooms3.values() if len(v) == 2),
    sum(1 for v in rooms3.values() if len(v) == 1)))
print("lines per room:", dict(sorted(Counter(Counter(l["sub"] for l in P).values()).items())))
