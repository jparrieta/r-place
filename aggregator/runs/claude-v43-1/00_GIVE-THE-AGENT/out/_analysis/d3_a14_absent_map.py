#!/usr/bin/env python3
"""D3a-41: write A14's absent map (A14-absent-map.json) from A14-absent-rows.txt ('id|REJ or PART|evidence', quotes
and hours checked by d3_spec_quotes.py, d3_spec_hours.py and d3_trunc_check.py), read from the four absent packets and
the ten absent windows with reply context (d3_rw_A14_ab*). A reject is a line whose own concepts show P08's terms
between the room and another room and, after them, help passing between the room and another room, classed by the
first act of each (G46's absent rule, with its readings); a PART line is NONPORTABLE and its concepts do not show that
order, so it is a particular by G6. No absent line is observed-absent or not-needed.

  python3 out/_analysis/d3_a14_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part = {}, {}
for l in open(R + "A14-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part, aid
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G46, quotes read: {ev}; A14's order is shown, P08's terms between the room and another "
                    f"room and after them help passing between the room and another room, so the claim of absence fails")
    else:
        assert cls == "PART", aid
        part[aid] = f"G6 and G46, quotes read: {ev}; the line is NONPORTABLE, so it is a particular"
with open(R + "A14-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": {}, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(part), "particulars to", R + "A14-absent-map.json")
