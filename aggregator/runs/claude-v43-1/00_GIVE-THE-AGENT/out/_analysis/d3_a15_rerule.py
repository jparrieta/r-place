#!/usr/bin/env python3
"""D3a-42: write A15-rerule.jsonl from A15-rerule-spec.txt ('id|CLASS|evidence', quotes and hours checked). These
instantiate lines were written under G47's reading 4 as first worded, which dated an attack continuing from before at
its post's hour; G46 reading 9 places such an attack only before the report. Each reason ends with what the line was
ruled before.

  python3 out/_analysis/d3_a15_rerule.py
"""
import json

R = "out/_analysis/d3_rulings/"
WAS = {"buffalobills-059": "the order, the first attack an act, dated at the report's hour by reading 4",
       "floridagators-043": "the order, the first attack an act, dated at the report's hour by reading 4"}
CLAUSE = {"J": ("reject", "the room's first attack is reported as continuing from before, so it cannot be placed after "
                          "the first call to place (G47, with G45 reading 12 and G46 reading 9); A15's order cannot be "
                          "read, and the census counts the line apart")}
out = []
for l in open(R + "A15-rerule-spec.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    d, clause = CLAUSE[cls]
    out.append({"adaptation": aid, "decision": d,
                "reason": f"re-ruled at D3a-42 under G47 with its reading 4 corrected by G46 reading 9, after this "
                          f"line was written: {ev}; {clause} (was: {WAS[aid]})"})
assert sorted(r["adaptation"] for r in out) == sorted(WAS)
with open(R + "A15-rerule.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", len(out), "re-rulings to", R + "A15-rerule.jsonl")
