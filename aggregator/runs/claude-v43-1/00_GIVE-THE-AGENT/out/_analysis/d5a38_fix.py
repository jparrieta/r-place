#!/usr/bin/env python3
"""D5a-38: the corrections found by checking the draft template's claims (diary), applied to d5a38_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a38_fix.py > out/_analysis/d5a38_template2.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a38_template.md"), encoding="utf-8").read()
FIX = [
    ("Asked about a darker orange, a r/bardmains organiser answered,",
     "Asked about a darker orange, the member who had started the r/bardmains mask answered,"),
    ("In the lines I read, the form's rooms do not say that telling failed; they say that telling was not enough, or that the "
     "record cannot tell ignorance from dissent.",
     "Each of the 46 lines that restrict P05 restricts its telling clause, and none of them shows a change lost only because its "
     "keepers were not told; they say that telling was not enough, or that the record cannot tell ignorance from dissent."),
    ("Rooms of the first kind exist in the population: A11's within-case datings (r/udub, r/wallstreetbets) and the 98 rooms "
     "where a template came first in the held A11 proposal's census.",
     "Such rooms could be looked for in the population, among rooms with as much design talk; I have not looked for them here. "
     "A11's two within-case datings (r/udub, r/wallstreetbets) show only that design talk came before the template, not that the "
     "design stayed fixed."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
