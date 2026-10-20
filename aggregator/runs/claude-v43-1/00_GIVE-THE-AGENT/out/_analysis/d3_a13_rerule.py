#!/usr/bin/env python3
"""D3a-40: write A13-rerule.jsonl from A13-rerule-spec.txt ('id|CLASS|evidence', quotes and hours checked). These
instantiate lines were written before G45 reading 11 was settled (a code in an edited submission cannot be dated by
the submission's hour, so it cannot be the first end named from the room's record). Each reason ends with what the
line was ruled before.

  python3 out/_analysis/d3_a13_rerule.py
"""
import json

R = "out/_analysis/d3_rulings/"
WAS = {"calgaryflames-052": "the order in words with help traded, named from the room's record",
       "spacexmasterrace-054": "the order with help given, named from the room's record"}
CLAUSE = {"J": ("reject", "the room's first upkeep shown cannot be placed before the first help, so the first acts "
                          "cannot be ordered (G45 and its readings 4 and 11); A13's order is not shown, and the census "
                          "counts the line as one act or not orderable")}
out = []
for l in open(R + "A13-rerule-spec.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    d, clause = CLAUSE[cls]
    out.append({"adaptation": aid, "decision": d,
                "reason": f"re-ruled at D3a-40 under G45 and its reading 11, which was settled after this line was "
                          f"written: {ev}; {clause} (was: {WAS[aid]})"})
assert sorted(r["adaptation"] for r in out) == sorted(WAS)
with open(R + "A13-rerule.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", len(out), "re-rulings to", R + "A13-rerule.jsonl")
