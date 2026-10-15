#!/usr/bin/env python3
"""C5c-02: carry into account.md the field analyst's advice I accepted on the declarations (c5c2_decl_spec.json), where
the account made the same claim: F-009 as a held-size null result; one pixel per interval and many placements, not many
members; F-014 counted on replies to attack calls, with its numbers; decided order's duration untested; first-concept
orders in the contest; credit nearly all after the work (F-016); curation after hour 73 with the arguing part tentative.
Each replacement must match exactly once.

    python3 out/_analysis/c5c2_account_field.py [--write]
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p = os.path.join(ROOT, "out", "account.md")
t = open(p, encoding="utf-8").read()
R = [
    ("The play did not delay the canvas work: 59 rooms filled with the play started their canvas work at a median of hour "
     "21.8, against hour 20.3 for 275 others of similar size (permutation p 0.43; F-009).",
     "A held-size test found no delay of the canvas work in rooms filled with the play: 59 such rooms started their "
     "canvas work at a median of hour 21.8, against hour 20.3 for 275 others of similar size (permutation p 0.43; F-009)."),
    ("so a picture needed many members placing [P01].",
     "so a picture of many pixels needed many placements: many members placing, members placing for many hours, or "
     "scripts and spare accounts [P01]."),
    ("A call makes an answer due; joining needs no reason, and refusing comes with one (F-014).",
     "A call makes an answer due. In replies to calls for an attack, refusals gave a reason in 23 of 38 and acceptances "
     "in 2 of 14 (F-014); replies to calls to place were not counted this way."),
    ("Each such decision governs one work for some hours.",
     "Each such decision governs one work; how long it held is not tested."),
    ("Members of the same room answer the attack call. In 82 of 104 rooms, the first attack call comes before the first "
     "sparing, refusal or apology [A16]:",
     "Members of the same room meet the attack call with sparing, refusal or apology: in 82 of 104 rooms, the first "
     "attack call comes before the first of these [A16], an order of first concepts, and in replies to attack calls a "
     "refusal usually gives a reason (F-014):"),
    ("Credit names who made the work. It comes after the work, and nothing in the record shows it moving a member to place.",
     "Credit names who made the work, and nearly all of it comes after the work (F-016); whether it moved anyone to "
     "place is not tested."),
    ("After hour 73, members curate the record: they clean, copy, record and argue over which version of the canvas and of "
     "the event is kept.",
     "After hour 73, members curate the record: they clean up, copy and post records of the canvas, and some argue over "
     "which version is kept (P22, tentative)."),
]
for old, new in R:
    n = t.count(old)
    if n != 1:
        sys.exit("%r matches %d times" % (old[:70], n))
    t = t.replace(old, new)
print("%d replacements; %d words" % (len(R), len(t.split())))
if "--write" in sys.argv:
    open(p, "w", encoding="utf-8").write(t)
    print("account.md written")
