#!/usr/bin/env python3
"""C2, pass 2: write out/_analysis/c2_structure_notes_p2.json, the authored notes for structure-p2.md: pass 1's notes
with D04's text revised after the split, D08 Contention's text, its seven pairwise separations, and pass 2's Part A
return text. Refuses to overwrite.

    python3 out/_analysis/c2_structure_notes_p2_build.py
"""
import json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(OUT, "_analysis", "c2_structure_notes_p2.json")
if os.path.exists(DEST):
    sys.exit("c2_structure_notes_p2.json exists; not overwritten")
n = json.load(open(os.path.join(OUT, "_analysis", "c2_structure_notes_p1.json"), encoding="utf-8"))
n["about"] = "pass 2 notes: pass 1's, with D04 revised after Contention split from it, D08 added, and pass 2's Part A return"
n["dimensions"]["D04"] = {
    "outside": "Moves against a rival and talk with a rival (D08 Contention); canvas-born colour factions (Neo-tribes, in "
               "Collective identity); near case: the void, a body of individual placers rather than a room acting toward rooms.",
    "least_sure": "T4-018 Meta-organization: a body of rooms acting together (inside), or a room hosting other rooms' works on "
                  "its own mark, which reads as one relation with each guest (Reciprocity)."}
n["dimensions"]["D08"] = {
    "outside": "Restraint toward a neighbour, deals and truces (D04 Order without law): an attack call refused or met with a "
               "truce passes there; near case: members reining in their own room's attackers (Live and let live).",
    "least_sure": "T4-021 Rivalry: talk carried on with a rival during and after a contest (inside), or an identity built "
                  "against an out-group (Collective identity)."}
n["pairs"].update({
    "D01|D08": "Critical mass gathers hands for the room's own work; Contention turns hands against a rival's work.",
    "D02|D08": "Coordination without command aligns placers on the room's own picture; Contention aims them at another room's.",
    "D03|D08": "Maintenance keeps a work against any erosion; Contention is the erosion a room aims at another, and the talk around it.",
    "D04|D08": "Order without law is how rooms hold, spare, trade, settle and federate; Contention is how a room wages a contest. "
               "An attack call refused, or met with a truce, passes from the second into the first.",
    "D05|D08": "Collective identity is the membership a room carries; Contention is a contest with a named rival, whether or "
               "not the rivalry comes from that membership.",
    "D06|D08": "Host framing is the community's frame on its own space; Contention is acted on the canvas against another room.",
    "D07|D08": "Imprinting is what a work leaves after the clock; Contention is fought during it, though victory claims and "
               "salutes cross hour 73."})
n["return"] = {
    "least_sure_dims": {"text": "D08 Contention and D03 Maintenance**, two members each (Contention is new at pass 2 and "
                                "arguable)",
                        "pairs": ["D03|D08", "D04|D08"]},
    "alternative": "Keeping Repertoire of contention and Rivalry inside Order without law, pass 1's partition. Rejected at "
                   "pass 2 by the rule written in `_questions/contention-dimension.md` before pass 2 counted: A15 (call then "
                   "attack) and A18 (attack then rivalry talk) run into and out of attack without border talk, and A16 and A17 "
                   "run from the contest into the order between rooms, which the split shows at the dimension level. "
                   "Attribution stays in Maintenance: no arrow joins it to attack (P06 to P09 reversed at pass 1). No "
                   "fourth-order recut at pass 2.",
    "least_sure_t4": "T4-007 Stigmergy.** It rests on two large themes, building and extending, which could be read as plain "
                     "production; the construct claims coordination through the trace, and A01, A03 and A07 rest on it. Next to "
                     "it, T4-021 Rivalry, which has five members and now carries A18."}
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(n, f, ensure_ascii=False, indent=1)
print("dimensions %d, pairs %d" % (len(n["dimensions"]), len(n["pairs"])))
