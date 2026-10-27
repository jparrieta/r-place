#!/usr/bin/env python3
"""D5a-39: the corrections found by checking the draft template's claims (diary), applied to d5a39_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a39_fix.py > out/_analysis/d5a39_template2.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a39_template.md"), encoding="utf-8").read()
FIX = [
    # only four forms are read; E and F are not
    ("Form D is the first of the six whose split below the form reads as a split (section 14).",
     "Form D is the first form read so far whose split below the form reads as a split (section 14)."),
    ("It is the first of the six forms whose split reads.",
     "It is the first form read so far whose split reads."),
    # K01 is instantiated in 64 of 96 defining members
    ("In about two fifths of the rooms the subreddit was also playing April Fools with its own members.",
     "In two thirds of the defining rooms the subreddit also played April Fools with its own members."),
    # c0125 is a later reply in the thread, not shown to answer c0124
    ("Another answered, \"Night shift for some,", "Another wrote, \"Night shift for some,"),
    # c0123 is in another thread (62wm03) than the lattice request c0087 (62tmhm)
    ("A member agreed: \"(Obviously our flag takes priority). Lets give them a hand.\" [OnePiece/c0123].",
     "In another thread a member wrote, \"(Obviously our flag takes priority). Lets give them a hand.\" [OnePiece/c0123]."),
    ("In r/OnePiece a member put the room's own flag first and then helped (section 1).",
     "In r/OnePiece a member put the room's own flag first before giving help (section 1)."),
    # the lines read, counted by script (d5a39_lines.json table): 82 + 67 + 20 + 15
    ("149 lines on carrying on, keeping, help, the April Fools frame, the host's line, the marking and the call)",
     "184 lines on carrying on, keeping, help, the April Fools frame, the host's line, the marking, the call and machine hands)"),
    # 21 of the 24 K01 add-step rooms are in D.2 (denverbroncos, terraria, yuyuyu are in D.1)
    ("These rooms sit in D.2 (section 14).", "21 of the 24 rooms with these lines sit in D.2 (section 14)."),
    # unmeasured 'seldom'
    ("Where a room under strain asks, the record holds the request and seldom the help.",
     "Where a room under strain asks, 14 of the 33 lines on A13 say the record cannot show that help arrived, or that the shortage caused it."),
    ("or owed, and where a room in need asks, the record does not show the help arriving.",
     "or owed, and where a room in need asks, the record often cannot show the help arriving or its cause."),
    ("where a room in need asks, the record does not show the help arriving. Carrying on",
     "where a room in need asks, the record often cannot show the help arriving or its cause. Carrying on"),
    # P27 and A05: say what the counts say
    ("These rooms chose their spot less than the population did, and kept what they had.",
     "Fewer of these rooms record choosing a spot before any loss, or sparing others' work by their own norm."),
    # P05 restrict is 30 members (31 per cent against 37), more than its add-step (21); A11 restrict 38 (40 against 48)
    ("Neither held proposal bears on this form's lean. The form restricts A11 in 38 members (section 7), as every form does, and its P05 "
     "lines add steps to keeping more than they restrict the telling clause.",
     "Neither held proposal bears on this form's lean. A11 is restricted by 38 defining members (40 per cent, against 48 of the 558) and "
     "P05 by 30 (31 per cent, against 37); both are below the population's share."),
    # A13 is not the only arrow with R over F (A15, A19, A20, A21); it is the only one among those with 20 lines or more
    ("It is the one arrow here where the record cannot show it outnumbers the arrow failing: 14 lines against 12.",
     "Of the seven arrows with 20 restrict lines or more here, it is the only one where the record cannot show it outnumbers the arrow "
     "failing: 14 lines against 12."),
    ("A12 in 14 of 26;", "A12 (a call, then a one-line pledge) in 14 of 26;"),
    # A20's lines concern a flood of calls; A08 is near even (F 8, R 7)
    ("The record cannot show that a call turned members against a rival (A15, 6 of 6 lines), that the host's line followed the calls for "
     "a reason (A20, 6 of 10), or that a record followed from the celebration (A08, 7 of 17).",
     "The record cannot show that a call turned members against a rival (A15, 6 of 6 lines), or that a flood of calls led the host to "
     "draw its line (A20, 6 of 10). On A08 (the marking, then the record) the two readings are near even: the arrow fails in 8 lines and "
     "the record cannot show it in 7."),
    # the context of c0066 is dated, not assumed
    ("The arrow's side. In r/denmark, during fighting with Swedish and Norwegian placers, a member asked,",
     "The arrow's side. In r/denmark a member reported, \"Norge angriber nu!\" [denmark/c0047] (Norway is attacking now). Forty minutes "
     "later, in another thread, a member asked,"),
    ("To a second request from the same neighbour a member answered,",
     "To a second request from the same neighbouring room a member answered,"),
    # c0160 is at h+74.55, after the close
    ("Near the close a member opened another canvas, \"New Place Area Created",
     "After the close a member posted another canvas, \"New Place Area Created"),
    # c0166 is a viewer asking, after the close
    ("When the logos were up, members pointed helpers on phones to them: \"I'm on mobile, gonna need someone to point me in the direction "
     "of the logo.\" [gamindustri/c0166].",
     "After the close a member on a phone asked where the logo was: \"I'm on mobile, gonna need someone to point me in the direction of "
     "the logo.\" [gamindustri/c0166]."),
    ("After the close the room started again on another canvas (section 1). The same member, in an edited reply, reported a loss:",
     "The room started again on another canvas (section 1). The member who started Lastation there reported a loss in an edited reply:"),
    ("which P05's telling clause predicts and few rooms show.", "which P05's telling clause predicts."),
    # F14 leans more to form C (3 of 7, ratio 2.42)
    ("The family of carrying on leans here more than to any form read so far.",
     "Four of the five lean here more than to any form read so far; F14 leans more to form C (3 of 7)."),
    # branch membership is not a claim about what a room did
    ("No room of F06, F10 or F26 is in form D: no room here asked that the joke be kept, carried out a deal as work, or contested the "
     "terms at a border.",
     "No room of F06 (the joke kept), F10 (a deal carried out as work) or F26 (informed members contest the terms at the border) is in "
     "form D."),
    ("They lean to keeping and the record, as the defining members lean to keeping.",
     "The most frequent touch keeping (P05) and the record (P12), as the defining members' lines touch keeping."),
    # FinalFantasy's A13 line reports strain and allied rescue; no claim of rarity
    ("such rooms are what A13 predicts, and the 12 lines where A13 fails here say they are rare in this form.",
     "such rooms are what A13 predicts."),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
