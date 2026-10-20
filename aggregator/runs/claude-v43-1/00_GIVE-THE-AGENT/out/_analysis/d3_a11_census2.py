#!/usr/bin/env python3
"""A11's test (D3a-38, G43), version 2: d3_a11_census.py's census with the re-rulings of G43 reading 4's check
applied. Each line in A11-rerule-spec.txt ('id|CLASS|evidence') takes its new class over the class it was first
ruled under; the class is checked against the re-ruling's decision and kind in A11-rerule.jsonl. REJ-T is an absent
reject in the members' words, as before. The rules, classes and priority are those logged before the first run.

  python3 out/_analysis/d3_a11_census2.py
"""
import json

src = open("out/_analysis/d3_a11_census.py", encoding="utf-8").read()
head, tail = src.split('print("lines by class:"', 1)
ns = {}
exec(compile(head, "d3_a11_census.py", "exec"), ns)
R, line_class, words, ruled = ns["R"], ns["line_class"], ns["words"], ns["ruled"]
EXPECT, CLASS = ns["EXPECT"], ns["CLASS"]
EXPECT["REJ-T"] = ("reject", None)
CLASS["REJ-T"] = "transition"
rr = {r["adaptation"]: r for r in ns["load"]("A11-rerule.jsonl")}
spec = ns["spec"]("A11-rerule-spec.txt")
assert sorted(rr) == sorted(spec), (sorted(rr), sorted(spec))
moved = []
for i, c in sorted(spec.items()):
    assert i in ruled, i
    d, k = EXPECT[c]
    assert rr[i]["decision"] == d and (k is None or rr[i].get("kind") == k), (i, c)
    if line_class[i] != CLASS[c]:
        moved.append("%s %s -> %s" % (i, line_class[i], CLASS[c]))
    line_class[i] = CLASS[c]
    if c in ("S-T", "REJ-T"):
        words.add(i)
    else:
        words.discard(i)
print("re-rulings applied: %d; census classes moved: %s" % (len(spec), "; ".join(moved) or "none"))
exec(compile('print("lines by class:"' + tail, "d3_a11_census.py", "exec"), ns)
