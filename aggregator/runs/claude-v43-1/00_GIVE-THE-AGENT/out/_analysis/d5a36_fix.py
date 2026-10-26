#!/usr/bin/env python3
"""D5a-36: the corrections logged after checking the draft template's claims (diary), applied to d5a36_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a36_fix.py > out/_analysis/d5a36_template3.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a36_template.md"), encoding="utf-8").read()
FIX = [
    ("In r/placetardis the organiser drew the line between the picture and its frame:",
     "In r/placetardis a member drew the line between the picture and its frame:"),
    ("Size entered the terms. A r/redhotchilipeppers member told a larger neighbour, \"we only have",
     "Size entered the terms. A neighbour asked r/redhotchilipeppers to move, taking it for the bigger sub. A member answered, \"we only have"),
    ("In r/israel a placer who could not win gave pixels instead:",
     "In r/israel's thread an artist who could not win gave pixels instead:"),
    ("A r/clg member wrote to a neighbour, \"it seems",
     "In r/clg a neighbour's member wrote, \"it seems"),
    ("In the lines I read, at least 27 defining members state that terms or a plan hold only where they reach the placers. "
     "I counted them from the dumps (`_analysis/d5a36_dump_nego.txt`, `d5a36_dump_plan.txt`); it is a reading, not a ledger count.",
     "In the lines I read, 29 defining members state that terms or a plan hold only where they reach the placers. They are listed "
     "with their lines in `_analysis/d5a36_reach_rooms.txt` and counted by script; the list is a reading, not a ledger count."),
    ("The second is held by at least 27 of 135 in the lines I read.",
     "The second is held by 29 of 135 in the lines I read."),
    ("Its members built a prism from a Pink Floyd album cover against a large black faction, the Void. \"We're Taking on the Void! "
     "Join the Fight!\" [FloydVsVoid/c0001]. Their terms ran in several directions at once. They kept a neighbour's colour as a deal:",
     "Its members built a prism and a rainbow against a rival room, the Void, whose members declared the room's resistance futile. "
     "The opening call: \"We're Taking on the Void! Join the Fight!\" [FloydVsVoid/c0001]. Their terms ran in several directions "
     "at once. They made a deal for space:"),
    ("a member repaired the flag himself, \"im using",
     "a member repaired the flag, \"im using"),
    ("What is unrepresentative about it: its rival was a colour faction that offered no terms, and few members of the form fought a "
     "rival of that kind. Its terms with neighbours ran beside a contest that most members did not have.",
     "What is unrepresentative about it: it organized against a rival room as well as with its neighbours, and its record is larger "
     "than most. It holds 205 coded concepts against the form's defining median of 99, and 26 selected changes against 10."),
    ("A neighbour asked the room to leave: \"Considering",
     "A neighbour asked one of its builders to move: \"Considering"),
    ("traded defence for upkeep, \"would you be willing",
     "offered to trade defence for upkeep, \"would you be willing"),
    ("Such rooms exist in the population: A04's within-case datings (r/switzerland, a member here, and r/DestinyTheGame) and the "
     "stage C5 reading behind A05's bound (the first sparing names a border, truce or deal in 17 of 124 rooms).",
     "Such rooms exist in the population: A04's within-case datings, r/switzerland (a member here) and r/DestinyTheGame, are rooms "
     "whose first upkeep came before their first border talk."),
    ("and about their sub's play and its coalitions less.",
     "and about their sub's play, its tribes and its coalitions less."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
