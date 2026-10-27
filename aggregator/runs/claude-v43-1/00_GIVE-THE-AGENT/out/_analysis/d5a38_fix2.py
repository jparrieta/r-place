#!/usr/bin/env python3
"""D5a-38: the second round, from the checks on the dry fill: r/gatech's quote cut to leave out '/r/Place'; two phrases of
mine taken out of quotation marks; r/cubers' recalled agreement quoted in two clean fragments (its nested quotation broke
the contraction check). Applied to d5a38_template2.md. Prints the corrected template.

    python3 out/_analysis/d5a38_fix2.py > out/_analysis/d5a38_template3.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a38_template2.md"), encoding="utf-8").read()
FIX = [
    ("A r/gatech member celebrated, \"We Did It Guys! /r/Place will Forever have our Mark!\" [gatech/c0070],",
     "A r/gatech member celebrated that the canvas \"will Forever have our Mark!\" [gatech/c0070],"),
    ("And the line between \"the template did not settle the design\" and \"it settles only for those who recognize it\" is a "
     "judgement in many A11 lines.",
     "And the line between *the template did not settle the design* and *it settles only for those who recognize it* is a "
     "judgement in many A11 lines."),
    ("- **A change refused by those who knew of it.** \"supposedly we had agreed to with Bulgaria. I even posed a mockup but then "
     "at least one person was like \"we don't want it like that\" so I gave up and deleted the posts.\" [cubers/c0309].",
     "- **A change refused by those who knew of it.** A member recalled a design agreed with a neighbour, \"I even posed a mockup\", "
     "refused by at least one member of the room, \"so I gave up and deleted the posts.\" [cubers/c0309]."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
