#!/usr/bin/env python3
"""D3a-39: write A12-rerule.jsonl from A12-rerule-spec.txt ('id|CLASS|evidence', quotes and hours checked). These
instantiate lines were written before G44 reading 7 was settled (an answer that only sets a condition or asks back is
not P15 by G28, so it does not show the pair). Each reason ends with what the line was ruled before.

  python3 out/_analysis/d3_a12_rerule.py
"""
import json

R = "out/_analysis/d3_rulings/"
WAS = {"bretagne-032": "the pair with a bare join"}
CLAUSE = {"COND": ("reject", "the call gets only a conditional or asking reply, which G28 does not count as P15 (G44 "
                             "reading 7), so A12's pair is not shown, and the census counts the line as a conditional "
                             "answer")}
out = []
for l in open(R + "A12-rerule-spec.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    d, clause = CLAUSE[cls]
    out.append({"adaptation": aid, "decision": d,
                "reason": f"re-ruled at D3a-39 under G44 and its reading 7, which was settled after this line was "
                          f"written: {ev}; {clause} (was: {WAS[aid]})"})
assert sorted(r["adaptation"] for r in out) == sorted(WAS)
with open(R + "A12-rerule.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", len(out), "re-rulings to", R + "A12-rerule.jsonl")
