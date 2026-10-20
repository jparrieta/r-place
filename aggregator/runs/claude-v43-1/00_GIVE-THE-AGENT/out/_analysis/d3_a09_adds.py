#!/usr/bin/env python3
"""D3a-36: build A09's add-condition rulings (G4a and G41) from one table, so each id carries its own evidence and
the statement that holds its condition. Every id must be in its packet, and every packet id here. Evidence
paraphrases the packet's code labels without quotation marks; the hours come from d3_cites_A09_adds.txt, and the
room's earlier records from d3_a09_cross_4.txt.

  python3 out/_analysis/d3_a09_adds.py
"""
import json
import subprocess
import sys

# (id, op, decision, kind, rule, evidence, held)
ROWS = [
    ("esperanto-039", "add-condition", "accept", "specification", "G4a (another element) and G41",
     "c0080 a member who loved r/place and will not end the game offering help (h+75.48), c0083 a call for help that "
     "carries forward what the room has seen of flags made larger step by step (h+85.40), c0085 a small plan to "
     "finish first (h+91.59): carrying on after the close, with no record in the line",
     "the condition, that members carry on for the love of the play and with what the room has learned, is held by "
     "K01's statement (the room keyed as April Fools play beside the work) and P13's (the work carried to a later "
     "canvas, G25); A09 orders the first acts and does not claim that a record is the only reason to carry on, so "
     "the condition is not one A09 lacks"),
    ("furry_irl-068", "add-condition", "accept", "specification", "G4a (another element) and G41",
     "c0164 a member calling PlaceTwo a carbon copy instead of a fresh start (h+79.42), c0165 the answer that they "
     "only wanted the logo without its misplaced pixels (h+79.60): carrying on after the close, with no record in "
     "the line",
     "the condition, that a work carried to a later canvas may be corrected rather than copied as it survived, is "
     "held by P05's statement (repair restores the form the keepers know) and P13's (the work remade elsewhere, "
     "G25); A09 names the image carried, not that it is carried unchanged"),
    ("miamidolphins-057", "add-condition", "accept", "specification", "G4a (the element states it) and G41",
     "c0058 the logo to be made in Minecraft (h+33.29) and c0068 a visitor from r/Texans proposing it as flair "
     "(h+44.84), while the room still builds, with no record before them in the room's lines already ruled (G41 "
     "reading 1), then c0123 the end called (h+73.02)",
     "the condition, that reuse can begin before the close, is held by A09's counterexample response (carry first; "
     "it names texans, the room the visitor cites) and by its bound (the emblem planned while building); a "
     "specification, counted in the census as carry first, since the room's first act is the remake"),
    ("reddevils-053", "add-condition", "accept", "specification", "G4a (the element states it) and G41",
     "c0093 a moderator's promise to put the crest in the sidebar if it is completed (h+48.87), while the room "
     "still builds, with no record before it in the room's lines already ruled (G41 reading 1), then c0203 a "
     "request to keep the damaged picture as the sidebar picture (h+76.73)",
     "the condition, that keeping the work as an emblem can be planned before any record, is held by A09's bound "
     "('Where a room planned its next canvas or its emblem while still building, carrying on comes before any "
     "record'); a specification, counted in the census as the bound"),
]


def packet_ids(op):
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A09", "--op", op,
                          "--offset", "0", "--limit", "100"], capture_output=True, text=True).stdout
    return [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]


got = packet_ids("add-condition")
mine = [r[0] for r in ROWS]
assert sorted(got) == sorted(mine) and len(set(mine)) == len(mine), set(got) ^ set(mine)
with open("out/_analysis/d3_rulings/A09-adds.jsonl", "w") as f:
    for aid, op, dec, kind, rule, ev, held in ROWS:
        row = {"adaptation": aid, "decision": dec, "kind": kind}
        tail = held if kind == "none" or "a specification" in held else held + "; a specification"
        row["reason"] = f"{rule}: {ev}; {tail}"
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A09-adds.jsonl")
