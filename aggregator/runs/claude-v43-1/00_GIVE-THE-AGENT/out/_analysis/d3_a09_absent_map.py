#!/usr/bin/env python3
"""D3a-36: write A09's absent map (A09-absent-map.json) from the six row files read packet by packet
(d3_a09_absent_rows_1..6.txt) and the seventh from the guard's second look (d3_a09_absent_rows_7.txt), so each reject
carries the record and the act of carrying on it rests on, with their quotes and hours as d3_absent_cites_A09_1..7.txt
printed them. Each row:
id | record code | record quote | hour | carrying code | carrying quote | hour | note (may be empty).
The four NONPORTABLE lines whose concepts do not show the order are particulars (G6).

  python3 out/_analysis/d3_a09_absent_map.py
"""
import json

FILES = ["out/_analysis/d3_a09_absent_rows_%d.txt" % i for i in range(1, 8)]
PART = {
    "nightinthewoods-053": "G6: the line is marked NONPORTABLE ['lost'] and fails portability, a particular; its record "
                           "(c0075, h+79.63) and its act of carrying on (c0085, h+79.63) come at the same hour, so the "
                           "order is not shown",
    "runescape-053": "G6: the line is marked NONPORTABLE ['minecraft'] and fails portability, a particular; its "
                     "Minecraft rendering records the logo and remakes it in one act (c0538), so the order is not shown",
    "southpark-052": "G6: the line is marked NONPORTABLE ['lost'] and fails portability, a particular; it shows a "
                     "record with nothing carried on",
    "vietnam-044": "G6: the line is marked NONPORTABLE ['lost'] and fails portability, a particular; it shows a "
                   "record with nothing carried on",
}

rej = {}
for fn in FILES:
    for ln in open(fn, encoding="utf-8"):
        if not ln.strip():
            continue
        aid, rc, rq, rh, cc, cq, ch, note = ln.rstrip("\n").split("|")
        assert aid not in rej and aid not in PART, aid
        assert float(rh) <= float(ch), (aid, rh, ch)
        rej[aid] = (f"G2, G3 and G41, quotes read: {rc} '{rq}' (h+{rh}), then {cc} '{cq}' (h+{ch}){note}; a record of "
                    f"what happened to the room's work comes first and an act of carrying the work on follows it, so "
                    f"A09's order is shown and the claim of absence fails")
with open("out/_analysis/d3_rulings/A09-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": {}, "particular": PART}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(PART), "particulars to out/_analysis/d3_rulings/A09-absent-map.json")
