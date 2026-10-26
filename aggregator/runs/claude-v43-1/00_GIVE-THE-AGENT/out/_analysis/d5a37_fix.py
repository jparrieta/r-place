#!/usr/bin/env python3
"""D5a-37: the corrections found by checking the draft template's claims (diary), applied to d5a37_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a37_fix.py > out/_analysis/d5a37_template2.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a37_template.md"), encoding="utf-8").read()
FIX = [
    ("In r/ohio the first calls were to attack and to build, three minutes apart:",
     "In r/ohio the first calls were to attack and to build, two minutes apart:"),
    ("A r/quebec organiser warned that everyone running a script",
     "A r/quebec member warned that everyone running a script"),
    ("For a mixture the centre lies between its patterns, so the rooms nearest it are those that hold more than one.",
     "For a mixture the centre lies between its patterns: nine of the ten nearest rooms change two or three of the form's "
     "signature themes."),
    ("first-return verdict composes, re-check grade composes with residue; in F28 and F29). It holds all three of the form's parts.",
     "first-return verdict composes, re-check grade composes with residue; in F28 and F29). Its selected changes hold the chat "
     "and the scripts, and its record holds an attack call as well."),
    ("An organiser set an official design,", "A member proposed an official design,"),
    ("A member opened the chat and asked for a script:", "A member pointed the room to its chat and asked for a script:"),
    ("It touches the chat once. It holds no script and no attack line.",
     "Its lines touch the chat twice and hold no script and no attack call."),
    ("It holds the chat and the scripts, and its record holds attack calls and their refusal.",
     "Its selected changes hold the chat and the scripts, and its record holds attack calls and their refusal."),
    ("and it holds all three parts at once, where most members hold one or two.",
     "and its record holds all three parts at once, where most members' changes hold one or two."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
