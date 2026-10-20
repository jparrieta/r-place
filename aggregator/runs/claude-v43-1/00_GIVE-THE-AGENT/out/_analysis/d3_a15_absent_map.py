#!/usr/bin/env python3
"""D3a-42: write A15's absent map (A15-absent-map.json) from A15-absent-rows.txt ('id|REJ, PART or SPEC|evidence', quotes
and hours checked by d3_spec_quotes.py, d3_spec_hours.py and d3_trunc_check.py), read from the five absent packets and the
thirteen absent windows with reply context (d3_rw_A15_ab*). A reject is a line whose own concepts show the room's call to
place for its own work and, after it, the room's call or act against another room's work, classed by the first act of
each (G47's absent rule, with its readings); a NONPORTABLE line whose concepts show that order is rejected too (G45
reading 10). The one observed-absent line (mit-045) is a specification, since its concepts show calls to place with no
attack. Every other line is an evidence limit, written by d3_absent_rulings.py.

  python3 out/_analysis/d3_a15_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part, spec = {}, {}, {}
for l in open(R + "A15-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part and aid not in spec, aid
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G47, quotes read: {ev}; A15's order is shown, the room's call to place for its own "
                    f"work and after it the room's call or act against another room's work, so the claim of absence fails")
    elif cls == "PART":
        part[aid] = f"G6 and G47, quotes read: {ev}; the line is NONPORTABLE, so it is a particular"
    else:
        assert cls == "SPEC", aid
        spec[aid] = (f"G2, G3 and G47, quotes read: {ev}; the observed absence holds, a call to place with no attack, "
                     f"which A15 does not claim as universal; a specification")
with open(R + "A15-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": spec, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects,", len(spec), "specifications and", len(part), "particulars to", R + "A15-absent-map.json")
