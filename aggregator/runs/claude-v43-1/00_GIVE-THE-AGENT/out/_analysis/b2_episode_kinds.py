#!/usr/bin/env python3
"""B2b-r1: episode lines (episodes-B1.jsonl) naming a kind that none of the line's rooms holds in scheme_current.jsonl.
Counts (line, kind) pairs and the lines they fall on. Writes nothing.
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
held = collections.defaultdict(set)
for r in (json.loads(x) for x in open(os.path.join(OUT, "scheme", "scheme_current.jsonl"), encoding="utf-8")):
    for m in r["members"]:
        held[m["sub"].lower()].add(r["theme"])
pairs, lines = 0, set()
for x in open(os.path.join(OUT, "episodes-B1.jsonl"), encoding="utf-8"):
    e = json.loads(x)
    rooms = [s.lower() for s in e.get("rooms") or []]
    for t in e.get("themes") or []:
        if not any(t in held[s] for s in rooms):
            pairs += 1
            lines.add(e["episode"])
print("episode lines %d; (line, kind) pairs with no room holding the kind: %d, over %d lines" % (
    sum(1 for _ in open(os.path.join(OUT, "episodes-B1.jsonl"))), pairs, len(lines)))
