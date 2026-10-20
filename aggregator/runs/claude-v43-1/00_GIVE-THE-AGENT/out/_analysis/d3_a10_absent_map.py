#!/usr/bin/env python3
"""D3a-37: write A10's absent map (A10-absent-map.json) from the four row files read packet by packet
(d3_a10_absent_rows_1..4.txt), the five not-needed lines' specifications written below, and the NONPORTABLE lines
the packets mark, so each reject carries the doubt and the move it rests on, with their quotes and hours as
d3_absent_cites_A10_1..4.txt and d3_a10_cross_21..24.txt printed them. Each row:
id | O or M | doubt code | quote | hour | move code | quote | hour | note (may be empty; M rows leave the move empty).
A NONPORTABLE line not rejected is a particular (G6); its marker is read from the packet header, not typed.

  python3 out/_analysis/d3_a10_absent_map.py
"""
import json
import re

RULE = "G2, G3 and G42, quotes read"
FILES = ["out/_analysis/d3_a10_absent_rows_%d.txt" % i for i in range(1, 5)]
PACKETS = ["out/_analysis/d3_pk_A10_absent_%s.txt" % o for o in ("000", "100", "200", "300")]
SPEC = {
    "mit-040": f"{RULE}: c0007 'This involves fighting with the active orange banner though...' and c0008 'let's just "
               "defend the small logo.' (h+27.53): doubt about room for a larger work, answered by defending the small "
               "logo, with no loss and no move; the room did not need A10's move, as the line's observation says, and "
               "K02's statement, P02 and P05 hold what it did (G42 reading 3); a specification",
    "neopets-046": f"{RULE}: c0012 'get us off your mango, and restore your mango.' (h+37.48), c0076 'it was originally "
                   "bigger but we were overtaking einstein so we redid it smaller' (h+68.38) and c0085 'We didn't have "
                   "near the man-power as other portions of the canvas, but somehow we made it to the end.' (h+73.81): "
                   "moves and a smaller version made to spare neighbours, P07's, with the low manpower stated after the "
                   "work survived and no move after a loss; A10's move was not needed, as the line's observation says; "
                   "a specification",
    "stlouis-051": f"{RULE}: c0095 'give me a location and I'd be happy to restart the good fight.' (h+82.73) and c0096 "
                   "'Oh... I didn't here place ended.' (h+82.94): a restart sought after the close and dropped on "
                   "learning that placement had ended, with no doubt and no move during the event; acts after the "
                   "close are P13's and P22's (G23's reading on the close), so A10's move was not needed; a "
                   "specification",
    "strangerthings-042": f"{RULE}: c0054, a neighbour's request, 'would you be willing to move it a few pixels up?' "
                          "(h+47.54), c0055 'No we can't do that as we'd be running into /r/LoveLive who already asked "
                          "us to move down, and we refused them as well.' (h+47.56) and c0136 'Tbh I'm surprised we "
                          "lasted until the end.' (h+82.15): a neighbour's request refused, P08's, with no loss, no "
                          "doubt about the room's hands and no move; A10's move was not needed; a specification",
    "truestl-046": f"{RULE}: c0024, a neighbour's request, 'I'd suggest moving it from underneath STRAYA' (h+40.61), and "
                   "c0025 'Okay, we've moved to a new location, sorry for the trouble!' (h+40.74): a move at a "
                   "neighbour's request before any loss, with no doubt, P07's and P08's (G22); A10's move was not "
                   "needed; a specification",
}

rej = {}
for fn in FILES:
    for ln in open(fn, encoding="utf-8"):
        if not ln.strip():
            continue
        aid, form, c1, q1, h1, c2, q2, h2, note = ln.rstrip("\n").split("|")
        assert aid not in rej and aid not in SPEC, aid
        if form == "O":
            assert float(h1) <= float(h2), (aid, h1, h2)
            rej[aid] = (f"{RULE}: {c1} '{q1}' (h+{h1}), the room's first doubt about its numbers or room, then {c2} "
                        f"'{q2}' (h+{h2}), its first move after a loss{note}; the doubt comes before the move, so "
                        f"A10's order is shown and the claim of absence fails")
        else:
            assert form == "M" and not c2, aid
            rej[aid] = (f"{RULE}: {c1} '{q1}' (h+{h1}) judges the room's hands or room too few and then moves, "
                        f"A10's mechanism in one post (G42 reading 1){note}; the doubt comes before the move, so "
                        f"A10's order is shown and the claim of absence fails")
part = {}
for fn in PACKETS:
    for blk in open(fn, encoding="utf-8").read().split("\n== ")[1:]:
        head = blk.split("\n", 1)[0]
        m = re.search(r"NONPORTABLE (\[.*?\])", head)
        aid = head.split()[0]
        if m and aid not in rej:
            part[aid] = (f"G6: the line is marked NONPORTABLE {m.group(1)} and fails portability, a particular; its "
                         f"concepts do not show the room's first doubt before its first move after a loss")
with open("out/_analysis/d3_rulings/A10-absent-map.json", "w", encoding="utf-8") as f:
    json.dump({"reject": rej, "specification": SPEC, "particular": part}, f, ensure_ascii=False, indent=1)
print("wrote", len(rej), "rejects,", len(SPEC), "specifications and", len(part),
      "particulars to out/_analysis/d3_rulings/A10-absent-map.json")
