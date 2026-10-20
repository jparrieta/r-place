#!/usr/bin/env python3
"""D3a-46: write A19's absent map (A19-absent-map.json) from A19-absent-rows.txt ('id|REJ or PART|evidence', quotes
and hours checked by d3_spec_quotes.py, d3_spec_hours.py, d3_trunc_check.py and d3_a16_seg_gap.py, writers checked by
d3_a19_rej_crosscheck.py), read from the five absent packets and the fifteen absent windows with reply context
(d3_rw_A19_ab*). A reject is a line whose concepts, or the coded posts above them in their reply chain, show the room's
upkeep or defence of its own work and, after it, the room's coalition, by the first act of each (G51's absent rule, with
its readings). A NONPORTABLE line is a particular (G6), marked PO in the census where its concepts show that order.
A19 has no observed-absent or not-needed line. Every other line is an evidence limit, written by d3_absent_rulings.py.

  python3 out/_analysis/d3_a19_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part, spec = {}, {}, {}
for l in open(R + "A19-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part and aid not in spec, aid
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G51, quotes read: {ev}; A19's order is shown, the room's upkeep or defence of its own "
                    f"work and after it the room's coalition, so the claim of absence fails")
    else:
        assert cls == "PART", aid
        part[aid] = f"G6 and G51, quotes read: {ev}; the line is NONPORTABLE, so it is a particular"
with open(R + "A19-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": spec, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects,", len(spec), "specifications and", len(part), "particulars to", R + "A19-absent-map.json")
