#!/usr/bin/env python3
"""D5a-37: the second round of corrections, from the checks on the dry fill: quotes cut to substrings that leave out r/
names the room list does not hold in that form (r/Québécois; r/thefarleftside, whose room is r/TheFarLeftSide), and a
watch phrase reworded. Applied to d5a37_template2.md. Prints the corrected template.

    python3 out/_analysis/d5a37_fix2.py > out/_analysis/d5a37_template3.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a37_template2.md"), encoding="utf-8").read()
FIX = [
    ("Its first post proposed the flag: \"Cher /r/Québécois et /r/Québécoises, je ne vous propose rien de moins que de créer "
     "le drapeau du Québec sur /r/place.\" [quebec/c0001].",
     "Its first post proposed the flag: \"je ne vous propose rien de moins que de créer le drapeau du Québec sur /r/place.\" "
     "[quebec/c0001]."),
    ("- **The attack called.** \"can we plzzzz get rid of the commie flag r/thefarleftside\" [AmericanFlaginPlace/c0007].",
     "- **The attack called.** \"can we plzzzz get rid of the commie flag\" [AmericanFlaginPlace/c0007]."),
    ("Members called attacks, \"can we plzzzz get rid of the commie flag r/thefarleftside\" [AmericanFlaginPlace/c0007],",
     "Members called attacks, \"can we plzzzz get rid of the commie flag\" [AmericanFlaginPlace/c0007],"),
    ("- **By the split rule no part stands as a subform.**", "- **By the split rule no part is a subform.**"),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
