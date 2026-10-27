#!/usr/bin/env python3
"""D5a-39: the corrections the checks on the dry fill found (diary), applied to d5a39_template2.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a39_fix2.py > out/_analysis/d5a39_template3.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a39_template2.md"), encoding="utf-8").read()
FIX = [
    # d5_quote_check: the quote of c0087 names a room not analysed
    ("A member proposed help to earn space: \"It looks like r/GreenLattice doesn't approve of that logo, so if we help them with removing "
     "it we should have plenty of space for Lastation.\" [gamindustri/c0087].",
     "A member proposed helping the neighbour remove a logo it did not want, and gave the reason: \"If they don't, then at least cleaning "
     "that area up will maybe earn us some good will with them, allowing us to place something there in the future.\" "
     "[gamindustri/c0088]."),
    # d5f_quote_check2: my own words, put in italics rather than quotation marks
    ("The name says \"and\" where the members show \"or\".", "The name says *and* where the members show *or*."),
    ("that stage D6 read the name as \"keeping, with traded help or carrying on\".",
     "that stage D6 read the name as *keeping, with traded help or carrying on*."),
    # pronoun grep: a game character, named plainly
    ("A member started him:", "A member started the figure:"),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
