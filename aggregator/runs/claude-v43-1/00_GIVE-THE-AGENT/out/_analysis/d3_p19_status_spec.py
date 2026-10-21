#!/usr/bin/env python3
"""D3a-53: write out/_analysis/d3_revision_P19_status.json, the spec for d3_revise_element.py that re-admits P19.
The adaptations are the restrict and add lines that tested P19's statement without correcting it (classes S-SHOW,
S-OTHER, E-PAIR and PART), read from their spec files so that no id is typed. The counts in 'why' are the census's
(d3_p19_census.py, D3a-53). Writes the spec only.

  python3 out/_analysis/d3_p19_status_spec.py
"""
import json

R = "out/_analysis/d3_rulings/"
FILES = ["P19-restrict-spec-all.txt", "P19-addcond-spec.txt", "P19-addstep-spec.txt", "P19-link-spec.txt"]
ids = []
for f in FILES:
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            aid, cls = l.split("|")[:2]
            if cls in ("S-SHOW", "S-OTHER", "E-PAIR", "PART"):
                ids.append(aid)
assert len(ids) == len(set(ids)), "repeat"
WHY = (
    "D3a-01 set that the candidates are decided by their own D2 lines, and that no rule binds them; the arrow rule "
    "decides only what the account may say an element brings about. P19 entered at C2a-03 as a candidate; F-012 "
    "found that hosting follows neither help, coalition nor upkeep, and its bound found the declared order reversed "
    "in 16 of 21 rooms. P19 drew 787 lines in 689 rooms, every one ruled under G57 and its 13 readings (D3a-53). "
    "477 lines show it, in 382 rooms: a host rules on requests (approves, denies, sets conditions, lists or removes "
    "works) in 274, a guest asks the room that holds the space in 221, a small room seeks or is promised a bigger "
    "room's protection in 50, and members dispute who may approve in 57. In 82 rooms the lines show only a request, "
    "with no ruling, protection or dispute; P19's range runs from a single request, so these rooms show it. The room "
    "is the host in 114 rooms and the guest in 273. In 340 of the 382 rooms the room's own members act; in 42 only a "
    "visitor acts for its own room (G18). 10 rooms show it only after the close, and 6 only in NONPORTABLE "
    "particulars. No line corrects P19: the 60 restrict lines narrow it to granted, enforced, lasting or binding "
    "rule, which its range does not claim (G9), so 57 are specifications and 3 evidence limits. Of the 60 add lines, "
    "54 add steps, conditions or links its statement holds, one a link that P13 states, two a paired link (below), "
    "one is a NONPORTABLE particular, one is one room's particular (tokyo-013, a canvas judged too full), and one "
    "is an evidence limit. Of the 217 instantiate lines, 213 show it, 3 do not, and 1 is a NONPORTABLE particular "
    "that shows it. 142 of the 450 absent lines fail because their concepts show it, and 297 stay evidence limits. By reading 13, a request or leave to build beside another room's work stays P08's, so P19 "
    "keeps its edge with borders and deals. Most rooms that show P19 also show P08 (352) and P16 (360), which are "
    "broad, but the acts differ: asking the room that holds the space and its ruling are not a border or help. "
    "No arrow is grounded and none is claimed, so the account may say what guests and hosts did and claims no "
    "effect of P19; F-012 and its bound stand, since P19 claims no order, and two lines show the work laid before "
    "the host was asked (gamindustri-017, puzzleanddragons-041). The census shows one edge, which I carry to the "
    "clustering rather than revise here: the host is a colour faith in 131 rooms, and in 90 of the 274 rooms with a "
    "ruling; 12 of K04's 22 colour-faith rooms are P19 hosts. Two link lines make a host's ruling depend on its "
    "faith (orderofthebluecorner-040, thebluecorner-066), but both are subs of one faction, so the pair is thin as "
    "a second room. This is the head's contrary condition, a faith deciding whom a room admits, and it may make a "
    "cluster branch of P19 beside K04's faith branch. The statement and range stand as written. The words served "
    "to every room in the return are unchanged, so the re-admission rewrites no text a room adapted to; the "
    "re-check scope is set when the re-check is built.")
spec = {"id": "P19", "field": "status", "now": "standing", "move": "developing working hypotheses",
        "event": "candidate re-admitted (stage D3, D3a-01's note on the five candidates; QD3-002): a candidate since "
                 "C2 pass 3 after its order test failed, now shown in the rooms' own lines",
        "why": WHY, "adaptations": ids}
json.dump(spec, open("out/_analysis/d3_revision_P19_status.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote out/_analysis/d3_revision_P19_status.json: %d adaptations; why %d words" % (len(ids), len(WHY.split())))
