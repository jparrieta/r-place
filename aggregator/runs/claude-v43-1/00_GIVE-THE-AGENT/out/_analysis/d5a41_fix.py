#!/usr/bin/env python3
"""D5a-41: the corrections found by checking the draft template's claims (diary), applied to d5a41_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a41_fix.py > out/_analysis/d5a41_template2.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a41_template.md"), encoding="utf-8").read()
FIX = [
    # the fill has no placeholder for one arrow's expectation: 2 / 705 * 56
    ("A10's expectation in form F is {{A10_EXP}} (2 within-case", "A10's expectation in form F is 0.159 (2 within-case"),
    # counted for one room only (r/dallasstars started at seven spots: c0025, c0027, c0038, c0044, c0055, c0056, c0097)
    ("Some rooms tried four or five spots.", "One room, r/dallasstars, started at six spots or more."),
    # form C's Collective representation is held by 97.9 per cent; F's ratio, 5.36, is the highest
    ("(share ratio 5.36), the highest presence of any form's signature.", "(share ratio 5.36), the highest ratio of any form's signature."),
    # the quote is from account.md, which the uncited-quote check does not read; said in my words
    ("and it has no loop from the move back to building (the account: \"No loop is grounded\").",
     "and the account grounds no loop from the move back to building."),
    # unmeasured 'seldom'
    ("And the model has a host rule on a guest's request (P19); in these rooms the record holds the request and seldom the ruling.",
     "And the model has a host rule on a guest's request (P19); in the P19 lines here the record holds the request and leaves the "
     "ruling unresolved."),
    # P03 link is 12 members on any theme; the territoriality lines from a move to building are 9 in 8 members (by script)
    ("and building again (12 members link a move back to building). But building again is the least held of the four by the counts: "
     "P03 link is held by 12 of 34.",
     "and building again (in 8 members territoriality lines run from a move back to building; P03 is linked in 12 of 34). Building "
     "again is the least held of the four by these counts."),
    # the reason for cannot tell is not stated in the verdicts
    ("Their records are too short to tell.", "Their records hold 1 or 2 coded concepts each."),
    # the arrow's own words, from model/arrows.jsonl
    ("Its connection and mechanism, as the model states them, are in `model/arrows.jsonl`; the account says that a room that judges "
     "its hands too few moves.",
     "Its connection: \"in a room carrying both, the first doubt about the room's numbers or room comes before the first move after a "
     "loss\". Its mechanism: \"A room that judges it has too few hands to hold its spot stops fighting for it and moves.\""),
    # c0059 answers a call to recolour the Blues logo
    ("A member refused to take another room's spot by force:", "Asked to recolour a rival's logo, a member refused:"),
    # c0038 (thread 62zgrf, h+54.51) and c0066 (thread 6336di, h+56.82) are different efforts
    ("Meanwhile members built a small sign elsewhere: \"I have started just to the right of the Rolling Stones lips, tucked in a small "
     "space that wont be missed, just added the blue so far\" [sips/c0038]. It was up within the hour: \"we did it guys. well done.\" "
     "[sips/c0066].",
     "Meanwhile a member started beside another work: \"I have started just to the right of the Rolling Stones lips, tucked in a small "
     "space that wont be missed, just added the blue so far\" [sips/c0038]. In another thread members squeezed a small sign in "
     "(section 1) and finished it: \"we did it guys. well done.\" [sips/c0066]."),
    # unmeasured comparison with other rooms
    ("and the room was choosing a spot at the close, when most rooms had stopped.",
     "and its record runs to the close with the spot still unsettled."),
    # branch names: F26 and F27 are the telling clause at the border and in keeping; F28 is help at the border
    ("among them F02 (the takeover), F17 and its subforms (the marking provisional), and the three branches of P05's telling clause "
     "shown in keeping or at the border (F26, F27, F28 help at the border).",
     "among them F02 (the takeover), F17 and its subforms (the marking provisional), the telling clause not shown in keeping or at the "
     "border (F27, F26), and help at the border conditional (F28)."),
    # the reason was not measured; the counts are
    ("28 of form F's 56 rooms are in no branch, half the form: these rooms' changes were too few, or too scattered, to fall on the keys "
     "the branches were cut on.",
     "28 of form F's 56 rooms are in no branch, half the form: 18 of them are thin or core rooms, and 10 are defining."),
    # the most frequent thin line is P01 add-step
    ("They lean as the defining members do, to the spot and the move (P27 link, A10 restrict, P03 link).",
     "Among them are the spot and the move (P27 link, A10 restrict, P03 link), as in the defining members."),
    # r/day9 fits the relations; it does not fall outside them
    ("A10's within-case dating r/day9 is such a room in part: the account says it offered terms before any damage and moved within "
     "two hours of a loss.",
     "A10's within-case dating, r/day9, fits the relations: the account says it offered a neighbour terms before any damage, the "
     "agreement broke at hour 48, and the room judged the spot lost and moved."),
    # name the four problems' term
    ("It touches the division of the canvas between rooms, which the four problems do not name as such: space is allocated between "
     "rooms by request, claim and terms.",
     "It touches task division between rooms: the canvas is divided by request, claim and terms."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
