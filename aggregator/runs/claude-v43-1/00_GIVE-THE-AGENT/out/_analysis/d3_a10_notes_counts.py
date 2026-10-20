#!/usr/bin/env python3
"""D3a-37: counts for A10's section in notes-D3.md, so no sub-count is typed: absent lines by observation (from the
four packets), the order rooms by the op of the lines that show the order, and the order lines that rest on the
room's earlier doubt in another line (the two-way check), by op.

  python3 out/_analysis/d3_a10_notes_counts.py
"""
import json
import re
from collections import Counter

R = "out/_analysis/d3_rulings/"
obs = Counter()
for o in ("000", "100", "200", "300"):
    for blk in open("out/_analysis/d3_pk_A10_absent_%s.txt" % o, encoding="utf-8").read().split("\n== ")[1:]:
        obs[re.search(r"observation: (\S+)", blk).group(1)] += 1
print("absent lines by observation:", dict(obs))


def room(aid):
    return aid.rsplit("-", 1)[0]


src = {}
for name, op in (("A10-inst-spec.txt", "instantiate"), ("A10-restrict-spec.txt", "restrict")):
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, c, ev = l.rstrip("\n").split("|", 2)
            if c in ("O", "M", "S-O", "S-M"):
                src.setdefault(room(aid), set()).add(op)
for l in open(R + "A10-absent.jsonl"):
    r = json.loads(l)
    if r["decision"] == "reject":
        src.setdefault(room(r["adaptation"]), set()).add("absent")
src.pop("bangladesh", None)
print("order rooms:", len(src), "by the ops of their order lines:", dict(Counter(" + ".join(sorted(s)) for s in src.values())))
earlier = Counter()
for name, op in (("A10-inst-spec.txt", "instantiate"), ("A10-restrict-spec.txt", "restrict")):
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, c, ev = l.rstrip("\n").split("|", 2)
            if c in ("S-O", "S-M") and "the room's first doubt stands in" in ev:
                earlier[op + " " + c] += 1
            if c == "S-MF" and "the room's first move stands in" in ev:
                earlier[op + " " + c] += 1
print("restrict lines ordered by another line's concept (two-way check):", dict(earlier))
