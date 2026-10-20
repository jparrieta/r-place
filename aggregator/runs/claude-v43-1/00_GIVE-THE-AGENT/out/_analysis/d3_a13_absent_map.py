#!/usr/bin/env python3
"""D3a-40: write A13's absent map (A13-absent-map.json) from A13-absent-rows.txt ('id|REJ or PART|evidence', quotes
and hours checked by d3_spec_quotes.py and d3_spec_hours.py), read from the four absent packets and the absent
windows with reply context (d3_rw_A13_ab001_*). A reject is a line whose own concepts show the room's own upkeep or
defence and, after it, help passing between the room and another room (G45's absent rule, with its readings); a PART
line is NONPORTABLE and its concepts do not show that order, so it is a particular by G6. No absent line is
observed-absent or not-needed.

  python3 out/_analysis/d3_a13_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part = {}, {}
for l in open(R + "A13-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G45, quotes read: {ev}; A13's order is shown, the room's own upkeep and after it help "
                    f"passing between the room and another room, so the claim of absence fails")
    else:
        assert cls == "PART", aid
        part[aid] = f"G6 and G45, quotes read: {ev}; a particular"
with open(R + "A13-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": {}, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(part), "particulars to", R + "A13-absent-map.json")
