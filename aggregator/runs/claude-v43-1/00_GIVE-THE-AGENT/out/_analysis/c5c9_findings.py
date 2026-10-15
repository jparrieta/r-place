#!/usr/bin/env python3
"""C5c-09, problem 3 (thin evidence): append F-019 (the move after doubt, A10) and F-020 (what sparing and help between
rooms rest on, A05 and A14) to out/findings.jsonl, from the whole-room reads coded under rules written first (diary,
C5c-09, abductive). Refuses if either id exists.

    python3 out/_analysis/c5c9_findings.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
have = {json.loads(l)["id"] for l in open(F, encoding="utf-8") if l.strip()}
if have & {"F-019", "F-020"}:
    sys.exit("F-019 or F-020 exists")
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rows = [
    {"stage": "C5", "leg": LEG, "id": "F-019", "tier": "arrow", "warrant": "read", "status": "standing", "t": T,
     "statement": "After a loss, a room that judges its hands too few either moves or gives the work up. Of the 21 rooms "
                  "carrying both doubt about their hands (K02) and a move (P10), read whole, 10 voiced the judgment "
                  "before the move, after a loss or erosion of the spot ('We just don't have the people.' "
                  "[anarcho_capitalism/c0031], then 'Building ancap flag somewhere else would be a good idea' "
                  "[anarcho_capitalism/c0077]); in 10 the loss itself prompted the move, and the judgment came after it "
                  "or inside the move turns; 1 did not move. Of the 36 rooms that voiced such doubt and whose record "
                  "says the work was lost, 10 moved, and of the 26 with no move, 11 gave the work up ('we're not doing "
                  "this anymore don't do it' [raocow/c0062]), 7 voiced the doubt before any loss and 8 otherwise.",
     "evidence": ["out/_analysis/c5c9_a10_read.txt", "out/_analysis/c5c9_a10_codes.json",
                  "out/_analysis/c5c9_a10_rule6.py", "out/_analysis/c5c9_a10_reverse_read.txt",
                  "out/_analysis/c5c9_a10_reverse_codes.json", "anarcho_capitalism:c0031", "anarcho_capitalism:c0077",
                  "greenlattice:c0318", "greenlattice:c0349", "raocow:c0062"],
     "bound": "Coded by the analyst alone under rules written before reading; the first three concepts of each element "
              "in each room. 10 of 20 is at the rule's line; read as a coalition's move, MiamiHurricanes makes it 9 of "
              "20, where the rule does not decide. The judgment speaks for the room in 7 of the 10 and for one member "
              "apart in 3. work_remained is what the room's record says, not the canvas.",
     "refuted_by": ["a second coder, reading the same rooms under the same codes, finding the judgment before the move in "
                    "fewer than a third of the rooms that moved after a loss"],
     "literature": [], "abductive": True,
     "prompted_by": "J's advice on thin evidence (C5c-07): crucial things happen rarely",
     "why": "problem 3 of the serial work (notes-C5.md, C5c-07 and C5c-08): A10 was thin on 21 rooms; every room was "
            "read whole, and the rooms that voiced doubt, lost their work and did not move were read for what they did"},
    {"stage": "C5", "leg": LEG, "id": "F-020", "tier": "arrow", "warrant": "read", "status": "standing", "t": T,
     "statement": "Sparing a neighbour rests mostly on the room's own norm; help between rooms rests on a deal about as "
                  "often as not. Read whole, the first sparing concept names a border, truce, deal, policy or agreement "
                  "in 17 of the 124 rooms where it is the room sparing a neighbour (11 of 81 where border talk comes "
                  "first, 6 of 43 where it does not); the rest state a norm ('Don't ruin other people work' "
                  "[czech/c0062]), refuse a raid or apologise. The first help between rooms names a deal, border, truce, "
                  "alliance, an exchange or the neighbour relation as its ground in 86 of 194 rooms: 63 of 127 where "
                  "border talk comes first, against 23 of 67 where help comes first ('As per the terms, we will help with "
                  "the triangle' [TeamYellowPlace/c0047]).",
     "evidence": ["out/_analysis/c5c9_a05_read.txt", "out/_analysis/c5c9_a05_codes.json",
                  "out/_analysis/c5c9_a14_read.txt", "out/_analysis/c5c9_a14_codes.json",
                  "out/_analysis/c5c9_order_tally.py", "czech:c0062", "starcraft:c0062", "TeamYellowPlace:c0047",
                  "rotmg:c0098", "titanfall:c0203"],
     "bound": "Coded by the analyst alone under rules written before reading; the first concept of each element in "
              "each room. A later sparing or help concept may name a deal the first does not. Kin ties ('brothers') "
              "were counted as help with no ground, since they come from before the canvas. For help, 63 of 127 "
              "(0.496) falls between the half and the third that the rule written first set, so whether the "
              "mechanism shows in words is my judgment, made on the contrast with rooms where help came first.",
     "refuted_by": ["a second coder finding the line named in sparing about as often as the channel in help, or the "
                    "channel named as often where help comes first as where border talk does"],
     "literature": [], "abductive": True,
     "prompted_by": "J's advice on thin evidence (C5c-07): look at the evidence again",
     "why": "problem 3 of the serial work: A05 and A14 were thin by their order counts; every room carrying both "
            "elements was read whole for whether the mechanism shows in the members' words"}]
with open(F, "a", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended F-019 and F-020; findings.jsonl now %d lines" % sum(1 for l in open(F, encoding="utf-8") if l.strip()))
