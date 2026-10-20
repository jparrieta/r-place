#!/usr/bin/env python3
"""D3a-38: write A11-rerule.jsonl from A11-rerule-spec.txt ('id|CLASS|evidence', quotes and hours checked by
d3_spec_quotes.py and d3_spec_hours.py). These lines were found by G43 reading 4's check (d3_a11_reply_check4.py) and
read in the forests: the layout the first ruling named does not answer the talk it named. A restrict line takes its
class's clause from A11-restrict-clauses.json, as d3_arrow_restrict_rulings_v3.py wrote it; the absent line keeps the
reject wording of d3_a11_absent_map.py. Each reason ends with what the line was ruled before.

  python3 out/_analysis/d3_a11_rerule.py
"""
import json

R = "out/_analysis/d3_rulings/"
CL = json.load(open(R + "A11-restrict-clauses.json", encoding="utf-8"))
WAS = {"drugs-010": "the transition, with c0117 as the talk answered",
       "raocow-041": "the transition, with c0038 as the talk answered",
       "reddevils-055": "the transition, with c0041 as the answer to c0033",
       "japan-012": "the transition, with c0140 as an answer",
       "habs-011": "the transition through P04's other forms",
       "foxstevenson-011": "a reject, with c0011 as the talk answered"}
CHECK = "found by G43 reading 4's check (d3_a11_reply_check4.py) and read in the forest"
out = []
for l in open(R + "A11-rerule-spec.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    if cls == "REJ-T":
        reason = (f"re-ruled at D3a-38 under G2, G3 and G43, {CHECK}, quotes read: {ev}; A11's transition is shown, "
                  f"with the mechanism in the members' words, so the claim of absence fails (was: {WAS[aid]})")
        out.append({"adaptation": aid, "decision": "reject", "reason": reason})
    else:
        d, k, clause = CL[cls]
        reason = f"re-ruled at D3a-38 under G43 and G9, {CHECK}: {ev}; {clause.format(el='A11')} (was: {WAS[aid]})"
        out.append({"adaptation": aid, "decision": d, "kind": k, "reason": reason})
assert sorted(r["adaptation"] for r in out) == sorted(WAS), [r["adaptation"] for r in out]
with open(R + "A11-rerule.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote", len(out), "re-rulings to", R + "A11-rerule.jsonl")
