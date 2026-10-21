#!/usr/bin/env python3
"""D3a-47: write A20's absent map (A20-absent-map.json) from A20-absent-rows.txt ('id|REJ or PART|evidence', quotes
and hours checked by d3_spec_quotes.py, d3_spec_hours.py, d3_trunc_check.py and d3_a16_seg_gap.py, order checked by
d3_a20_absent_order_check.py), read from the five absent packets and the thirteen absent windows with reply context
(d3_rw_A20_ab*). A reject is a line whose concepts, or the coded posts above them in their reply chain, show a call
posted in the room and, after it, the host sub's line around canvas talk, by the first act of each (G52's absent rule,
with amendment 1 and its readings). A NONPORTABLE line is a particular (G6), marked PO in the census where its concepts
show that order. A20 has no observed-absent or not-needed line. Every other line is an evidence limit, written by
d3_absent_rulings.py.

  python3 out/_analysis/d3_a20_absent_map.py
"""
import json

R = "out/_analysis/d3_rulings/"
rej, part, spec = {}, {}, {}
for l in open(R + "A20-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    assert aid not in rej and aid not in part and aid not in spec, aid
    if cls == "REJ":
        rej[aid] = (f"G2, G3 and G52, quotes read: {ev}; A20's order is shown, a call posted in the room and after it "
                    f"the host sub's line around canvas talk, so the claim of absence fails")
    else:
        assert cls == "PART", aid
        part[aid] = f"G6 and G52, quotes read: {ev}; the line is NONPORTABLE, so it is a particular"
with open(R + "A20-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": spec, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects,", len(spec), "specifications and", len(part), "particulars to", R + "A20-absent-map.json")
