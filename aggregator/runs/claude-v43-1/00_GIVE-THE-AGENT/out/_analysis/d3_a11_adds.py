#!/usr/bin/env python3
"""D3a-38: build A11's add-condition and add-step rulings (G4a, G9 and G43) from one table, so each id carries its own
evidence and the statement that holds its condition or step. Every id must be in its packet, and every packet id here.
Evidence paraphrases the cited concepts without quotation marks; the hours come from d3_cites_A11_adds.txt. A spec copy
(id|op|evidence) is written beside the rulings so that d3_spec_hours.py can check the hours.

  python3 out/_analysis/d3_a11_adds.py
"""
import json
import subprocess
import sys

OTHER = "G4a (another element) and G43"
OWN = "G4a (the element states it) and G43"
# (id, op, decision, kind, rule, evidence, held)
ROWS = [
    ("ScottPilgrim-015", "add-condition", "accept", "specification", OWN,
     "c0001 a call to draw the head with its reference image (h+4.21), then c0030 a plea to newcomers to follow the "
     "reference everyone uses (h+24.38) and c0037 a colour change made a group effort so that it does not look like "
     "griefing (h+47.62): a reference posted with the first proposal, then contested",
     "the condition, that a reference may come with the first proposal and stay contested while the room builds, is "
     "held by A11's bound ('across rooms the first template often comes before any design talk') and counterexample "
     "response, and the contest that follows by P04's range and P05's statement (G43 reading 3); the condition is not "
     "one A11 lacks; a specification, counted in the census as template first"),
    ("de-046", "add-condition", "accept", "specification", OTHER,
     "c0233 a member at the spot who does not yet see how the work should go (h+21.45), c0234 a better template "
     "promised, with the trousers as a guide meanwhile (h+21.61), c0235 a question whether the work runs into the "
     "room's flag (h+21.63), and c0236 the figure sized in pixels to stay out of it (h+22.03): layouts answering "
     "practical questions and sizing to spare a neighbouring flag",
     "the condition, that templates answer practical questions and do not settle design or claims to space, is held "
     "by P04's range (asking for a layout and asking strays to keep to it) and by P07's and P08's statements for the "
     "sizing that keeps out of the flag (G43 reading 3); the condition is not one A11 lacks"),
    ("luciomains-048", "add-condition", "accept", "specification", OTHER,
     "c0054 the template in use shared for reference (h+52.59), c0056 a helper finding misplaced pixels by it "
     "(h+59.51), and c0089 (h+72.33) and c0090 (h+72.56) welcoming some eye changes while fixing the headband: a layout "
     "kept to, and changes accepted in talk later",
     "the condition, that a shared reference shows mistakes without settling every feature, is held by P04's range "
     "(a layout placers keep to), P05's statement (keepers repair what they know) and P02's range (a design argued "
     "and redone) (G43 reading 3); the condition is not one A11 lacks"),
    ("monero-009", "add-condition", "accept", "specification", OTHER,
     "c0005 a call to follow the drawing plan (h+15.68), c0081 a warning that old scripts left running make helpers "
     "fight each other (h+54.26), and c0130 a member who keeps to the newest version while preferring the first, as "
     "changes make members fight each other's edits (h+54.44): rival versions of a layout, run by hand and by script",
     "the condition, that a template settles the work only when the versions in use agree, is held by P04's range "
     "(an official template against other versions), P14's statement for the scripts and P05's statement for "
     "keepers working from an old version (G43 reading 3); the condition is not one A11 lacks"),
    ("npr-049", "add-condition", "accept", "specification", OTHER,
     "c0016 coordinates and a template just made (h+55.19), then c0023 a plan brought from the chat to shift the logo "
     "two pixels right to give a neighbouring knight room (h+59.86), and c0044 that shift explained as the plan at the "
     "time (h+72.66): a layout revised to spare a neighbour",
     "the condition, that a posted target stays open to shifts of place and design, is held by P04's range, by P07's "
     "and P08's statements for the shift that spares the knight, and by reading 3's P02 range (G43); the condition is "
     "not one A11 lacks"),
    ("placecanada-014", "add-condition", "accept", "specification", OTHER,
     "c0078 a builder who had not seen the last update and turns to the official design on seeing it (h+48.54): a "
     "keeper told of an agreed change",
     "the condition, that a design update settles a builder's choice once the builder receives it, is held by P05's "
     "statement ('A change the room has planned or agreed (P02) is therefore repaired away as damage until its "
     "keepers are told of it') (G43 reading 3); the condition is not one A11 lacks"),
    ("partyparrot-060", "add-step", "accept", "specification", OWN,
     "c0003 a gridded version offered for reference (h+16.28), c0004 a question whether it is accurate (h+16.39), "
     "c0005 the poster conceding that the found image was wrong (h+16.42), and c0006 the design cleaned up and linked "
     "(h+16.54), all in thread 62r2yj: a layout, design talk about it, and a revised layout in answer",
     "the step, that a posted reference is challenged in design talk and revised, is A11's transition as G43 reads "
     "it ('Inside a thread, talk that follows a template and is answered by a revised template is a transition'), and "
     "the line's concepts show it; the step is not one A11 lacks; a specification, counted in the census as the "
     "transition"),
]


def packet_ids(op):
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A11", "--op", op,
                          "--offset", "0", "--limit", "100"], capture_output=True, text=True).stdout
    return [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]


got = packet_ids("add-condition") + packet_ids("add-step")
mine = [r[0] for r in ROWS]
assert sorted(got) == sorted(mine) and len(set(mine)) == len(mine), set(got) ^ set(mine)
with open("out/_analysis/d3_rulings/A11-adds.jsonl", "w") as f, \
        open("out/_analysis/d3_rulings/A11-adds-spec.txt", "w") as g:
    for aid, op, dec, kind, rule, ev, held in ROWS:
        row = {"adaptation": aid, "decision": dec, "kind": kind}
        tail = held if kind == "none" or "a specification" in held else held + "; a specification"
        row["reason"] = f"{rule}: {ev}; {tail}"
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        g.write(f"{aid}|{op}|{ev}\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A11-adds.jsonl and its spec copy")
