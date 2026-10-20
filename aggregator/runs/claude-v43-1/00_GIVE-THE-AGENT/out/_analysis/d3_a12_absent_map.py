#!/usr/bin/env python3
"""D3a-39: write A12's absent map (A12-absent-map.json) from A12-absent-rows.txt ('id|REJ or SPEC|evidence', quotes
and hours checked by d3_spec_quotes.py and d3_spec_hours.py), read from the two absent packets and the reply context
of the absent window (d3_rw_A12_ab000.txt). A reject is a line whose own concepts show a call answered in its thread
by another member's later written P15 concept (G44's absent rule); the one evidenced line (observed-absent) is a
specification where its concepts show only dispreferred answers. No absent line is NONPORTABLE.

  python3 out/_analysis/d3_a12_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, spec = {}, {}
for l in open(R + "A12-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G44, quotes read: {ev}; A12's pair is shown, a call answered in its thread by another "
                    f"member's written P15 concept, so the claim of absence fails")
    else:
        assert cls == "SPEC", aid
        spec[aid] = (f"G3 and G44, quotes read: marked observed-absent; {ev}: the call gets only dispreferred answers, "
                     f"so no written join answers it, the case A12's bound and the other half of its mechanism state; "
                     f"the evidenced absence holds, a specification")
with open(R + "A12-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": spec, "particular": {}}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(spec), "specifications to", R + "A12-absent-map.json")
