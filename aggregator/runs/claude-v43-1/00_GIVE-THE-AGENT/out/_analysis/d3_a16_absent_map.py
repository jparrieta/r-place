#!/usr/bin/env python3
"""D3a-43: write A16's absent map (A16-absent-map.json) from A16-absent-rows.txt ('id|REJ, PART or SPEC|evidence', quotes
and hours checked by d3_spec_quotes.py, d3_spec_hours.py, d3_trunc_check.py and d3_a16_seg_gap.py), read from the four
absent packets and the ten absent windows with reply context (d3_rw_A16_ab*). A reject is a line whose concepts, or the
coded posts above them in their reply chain, show the room's call or act against another room's work and, after it,
the room's restraint toward another room's work, by the first act of each (G48's absent rule, with its readings). A
NONPORTABLE line is a particular (G6), marked PO in the census where its concepts show that order. An observed-absent
line whose concepts show an attack with no restraint, restraint with no attack, neither, or restraint first is a
specification. Every other line is an evidence limit, written by d3_absent_rulings.py.

  python3 out/_analysis/d3_a16_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part, spec = {}, {}, {}
for l in open(R + "A16-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part and aid not in spec, aid
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G48, quotes read: {ev}; A16's order is shown, the room's call or act against another "
                    f"room's work and after it the room's restraint toward another room's work, so the claim of "
                    f"absence fails")
    elif cls == "PART":
        part[aid] = f"G6 and G48, quotes read: {ev}; the line is NONPORTABLE, so it is a particular"
    else:
        assert cls == "SPEC", aid
        spec[aid] = (f"G2, G3 and G48, quotes read: {ev}; the observed absence holds, and A16 does not claim its order "
                     f"as universal; a specification")
with open(R + "A16-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": spec, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects,", len(spec), "specifications and", len(part), "particulars to", R + "A16-absent-map.json")
