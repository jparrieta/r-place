#!/usr/bin/env python3
"""D3a-38: write A11's absent map (A11-absent-map.json) from the four row files read packet by packet
(d3_a11_absent_rows_1..4.txt) and the NONPORTABLE lines the packets mark, so each reject carries the design talk and
the P04 concept that answers it in its thread, with their quotes and hours as d3_absent_cites_A11_1..4.txt printed
them. Each row: id | T or TO | talk code | quote | hour | answer code | quote | hour | note (may be empty).
A NONPORTABLE line not rejected is a particular (G6); its marker is read from the packet header, not typed. A11's
absent lines are all unobserved or not-testable, so no specification is named.

  python3 out/_analysis/d3_a11_absent_map.py
"""
import json
import re

RULE = "G2, G3 and G43, quotes read"
FILES = ["out/_analysis/d3_a11_absent_rows_%d.txt" % i for i in range(1, 5)]
PACKETS = ["out/_analysis/d3_pk_A11_absent_%s.txt" % o for o in ("000", "100", "200", "300")]

rej = {}
for fn in FILES:
    for ln in open(fn, encoding="utf-8"):
        if not ln.strip():
            continue
        aid, form, c1, q1, h1, c2, q2, h2, note = ln.rstrip("\n").split("|")
        assert aid not in rej, aid
        assert float(h1) <= float(h2), (aid, h1, h2)
        if form == "T":
            what = "a layout posted after it"
            how = "A11's transition is shown, with the mechanism in the members' words"
        else:
            assert form == "TO", aid
            what = "P04's coordinates, a pointer to the layout or a request for one"
            how = "A11's transition is shown through P04's other forms (G43 reading 1)"
        rej[aid] = (f"{RULE}: {c1} '{q1}' (h+{h1}), design talk, is answered by {c2} '{q2}' (h+{h2}), {what}{note}; "
                    f"{how}, so the claim of absence fails")
part = {}
for fn in PACKETS:
    for blk in open(fn, encoding="utf-8").read().split("\n== ")[1:]:
        head = blk.split("\n", 1)[0]
        m = re.search(r"NONPORTABLE (\[.*?\])", head)
        aid = head.split()[0]
        if m and aid not in rej:
            part[aid] = (f"G6: the line is marked NONPORTABLE {m.group(1)} and fails portability, a particular; its "
                         f"concepts do not show design talk answered by a layout in one thread")
with open("out/_analysis/d3_rulings/A11-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": {}, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects and", len(part), "particulars to out/_analysis/d3_rulings/A11-absent-map.json")
