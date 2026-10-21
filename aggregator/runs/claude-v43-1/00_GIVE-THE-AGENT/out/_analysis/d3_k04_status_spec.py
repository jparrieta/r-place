#!/usr/bin/env python3
"""D3a-52: write out/_analysis/d3_revision_K04_status.json, the spec for d3_revise_element.py that re-admits K04.
The adaptations are the restrict and add lines that tested K04's statement without correcting it (classes S-SHOW,
S-OTHER and PART), read from their spec files so that no id is typed. The counts in 'why' are the census's
(d3_k04_census.py, D3a-52). Writes the spec only.

  python3 out/_analysis/d3_k04_status_spec.py
"""
import json

R = "out/_analysis/d3_rulings/"
FILES = ["K04-restrict-spec.txt", "K04-addcond-spec.txt", "K04-addstep-spec.txt", "K04-link-spec.txt"]
ids = []
for f in FILES:
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            aid, cls = l.split("|")[:2]
            if cls in ("S-SHOW", "S-OTHER", "PART"):
                ids.append(aid)
assert len(ids) == len(set(ids)), "repeat"
WHY = (
    "D3a-01 set that the candidates are decided by their own D2 lines, and that no rule binds them; the arrow rule "
    "decides only what the account may say an element brings about (account.md, pass 15; the corrections at "
    "D3a-49). K04 entered at C2a-03 as a candidate, and its one test, membership carried in before the attack, "
    "failed (F-011: 52 of 126 rooms, below the null). K04 drew 868 lines in 697 rooms, every one ruled under G56, "
    "its amendment G56a and its 33 readings (D3a-52). 570 lines show it, in 465 rooms: the community's own jokes, "
    "lore, catchphrases or ideology in canvas talk in 339, the nation's history, belonging or politics beyond its "
    "flag in 115, a quarrel from before the canvas in 84, a faith in a colour in 22, and belonging in a body that "
    "is not a nation, the paired elaboration of its lead clause, in 35 (11 of them with no other form). In 457 of "
    "the 465 rooms the room's own members act; in 8 only a visitor acts for its own room, which shows K04 in that "
    "room's record (G18). 40 rooms show it only after the close, and 22 only in NONPORTABLE particulars. In 61 "
    "rooms a canvas fight is told as the body's history or lore, the order that F-011's bound names and did not "
    "test. No line corrects K04: the 72 restrict lines add that the joke, lore or body comes from before the canvas "
    "and that the room, not one member, acts, which its statement holds (G9); G56a narrowed the ruling rule for "
    "the faith to the room acting, as the statement says, and was applied backwards to 5 lines. Of the 42 add "
    "lines, 29 add a condition, step or link its statement and range hold, 3 add help, alliance or the record that "
    "P16, P17 and P12 state, and one link, a colour faith's reading deciding whom the room admits, is one room's "
    "particular (TeamYellowPlace-023). 88 instantiate lines and 55 restrict and add lines show canvas-born jokes, "
    "one member's outside commitment, the picture's reason (P02), April Fools play (K01) or help with no tie named, "
    "and do not show it; 16 of the 170 absent lines fail because their concepts show it, and 149 stay evidence "
    "limits. No arrow is grounded and none is claimed, so the account may say what members did as the body they "
    "were before the canvas, or as a faith in a colour, and claims no effect of K04. The census shows two edges, "
    "which I carry to the clustering rather than revise here. First, the faith in a colour sits apart from the "
    "bodies carried in: 19 of its 22 rooms show no body from before the canvas, and only 3 show both, so the "
    "statement's two branches may be two elements or two cluster branches; the head's most threatening room is a "
    "faith of this kind. Second, the sub's quarrel overlaps K03, which shows 68 of the 84 rooms with that form and "
    "all 5 rooms whose only form it is. 137 of the 152 rooms that C02 shows by its accepted or rejected-absent "
    "lines also show K04, none of them through the faith. The statement and range stand as written: its 'or' "
    "already names the faith as a separate form and claims no co-occurrence, and no room's line asked for a split. "
    "F-011 stands, since the re-admission claims no order. The words served to every room in the return are "
    "unchanged, so the re-admission rewrites no text a room adapted to; the re-check scope is set when the "
    "re-check is built.")
spec = {"id": "K04", "field": "status", "now": "standing", "move": "developing working hypotheses",
        "event": "candidate re-admitted (stage D3, D3a-01's note on the five candidates; QD3-002): a candidate since "
                 "C2 pass 3 after its one test failed, now shown in the rooms' own lines",
        "why": WHY, "adaptations": ids}
json.dump(spec, open("out/_analysis/d3_revision_K04_status.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote out/_analysis/d3_revision_K04_status.json: %d adaptations; why %d words" % (len(ids), len(WHY.split())))
