#!/usr/bin/env python3
"""D3a-34: build A07's add-condition, add-step and contradict rulings (G4a, G9 and G39) from one table, so each id
carries its own evidence and the statement that holds its condition. Every id must be in its packet, and every
packet id here. Evidence paraphrases the packet's code labels without quotation marks; the hours come from
d3_cites_A07_adds.txt.

  python3 out/_analysis/d3_a07_adds.py
"""
import json
import subprocess
import sys

BOUND2 = ("the condition, that a work the close cut unfinished is marked as an attempt, is held by A07's own bound, "
          "read in its words (QD3-007): 'Where hour 73 cut the work unfinished, the room marks the attempt instead'")
EARLY = ("the condition, that a marking can come while building, upkeep or changes go on, is held by P11's statement "
         "as G16 reads it (the room marks a work as up or achieved, at any hour, on its own word), as G39's corrected "
         "reading 1 reads an early marking")
ONE_ACT = ("the condition is a rule for counting, so the line is ruled by its concepts alone (G4a, a counting rule): "
           "they show one act holding the report and the marking (G39 counts it apart), so the order cannot be read; "
           "an evidence limit")
FAM = ("no part of the model states the condition: the room marks an attempt that ended before the close without a "
       "finished work standing, the family D3a-13 left as a paired elaboration of P11 (G4a, nothing states it)")

# (id, op, decision, kind, rule, evidence, held, pair)
ROWS = [
    ("SwissNeutralityZone-046", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0035 a celebration while the rainbow curve goes on", EARLY, None),
    ("Thegreatblackhole-041", "add-condition", "accept", "elaboration", "G4a (nothing states it) and G39",
     "c0056 bots said to have killed the void and everything else (h+72.19), c0077 pride in the work the members "
     "accomplished, in the same post", FAM + "; a paired elaboration, as mizzou-022 shows", "mizzou-022"),
    ("Villanova-021", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0014 a completed place announced, c0016 a call again for a black border around the V, c0017 obstacles to the "
     "border named", EARLY + ", and by P02's statement (the room adds to its mark)", None),
    ("anarcho_capitalism-057", "add-condition", "accept", "none", "G4a (a counting rule) and G39",
     "c0053 one announcement of a completed flag that shares credit", ONE_ACT, None),
    ("babymetal-051", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0043 the art announced finished, c0044 a celebration after fighting off attackers, c0063 vandalism fixed "
     "after completion, c0123 the mural called perfect, c0125 upkeep chosen",
     "the condition, that upkeep goes on after the marking, is held by A03's connection (the first build report "
     "comes before the first act of upkeep) and P05's statement (the room keeps its placed work)", None),
    ("bulgaria-048", "add-condition", "accept", "specification", "G4a (the element states it) and G39",
     "c0081 the coat of arms not placed and the flag smeared at the end, the member still satisfied (h+74.06), c0083 "
     "a pleasure to work together", BOUND2, None),
    ("canada-047", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0324 a perfect flag found on waking, c0333 a call for help under attack, c0355 upkeep with pride",
     EARLY + ", and by P05's statement (the room rallies to defend its work)", None),
    ("columbia-051", "add-condition", "accept", "elaboration", "G4a (nothing states it) and G39",
     "c0044 hours of work paved over by a blue blob (h+79.84), c0046 pride in the attempt (h+83.50)",
     FAM + "; a paired elaboration, as foxes-048 shows", "foxes-048"),
    ("corridor-052", "add-condition", "accept", "specification", "G4a (the element states it) and G39",
     "c0038 the logo almost finished in the last moments of the canvas (h+73.20), c0039 the result judged good for "
     "a smaller sub", BOUND2, None),
    ("fullcommunism-038", "add-condition", "particular", None, "G6",
     "the line is marked NONPORTABLE ['lost']", "it fails portability, a particular (G6)", None),
    ("gameattack-024", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0028 the logo announced done with praise, c0030 work on a black border with a call for help, c0032 work on "
     "the G and cleanup", EARLY + ", by P02's statement (the room adds to its mark) and by P05's (upkeep)", None),
    ("gravityfalls-045", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0002 a member's own part on a doodle, finished by others while away (h+4.55), c0037 Bill built and kept all "
     "day, c0041 money stacks turned into Bill",
     EARLY + ", P11's statement naming members' own parts, and by P05's statement (upkeep)", None),
    ("kindafunny-022", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0009 the logo praised with thanks to its maker, c0010 an expansion to the left begun, c0020 another expansion "
     "proposed", EARLY + ", and by P02's statement (the room adds to its mark or enlarges it)", None),
    ("kpop-049", "add-condition", "accept", "specification", "G4a (the element states it) and G39",
     "c0025 a member typing words in pink at a given place, with a call for help (h+25.13), then c0035 pride that "
     "the words are still there (h+37.77)",
     "the condition, that the sequence is shown without a separate proof of its cause, restates A07's connection, "
     "an order counted inside each room, which the concepts show", None),
    ("nintendo-049", "add-condition", "accept", "none", "G4a (a counting rule) and G39",
     "c0101 one post saying the larger logo was never built and the original was kept by many (h+48.75)",
     ONE_ACT, None),
    ("polska-050", "add-condition", "accept", "none", "G4a (a counting rule) and G39",
     "c0011 a celebration that the room did it, c0136 the end announced with the result shown", ONE_ACT, None),
    ("qotsa-032", "add-condition", "accept", "specification", "G4a (the element states it) and G39",
     "c0022 help as the logo takes shape, c0037 the relocated icon posted with its coordinates (h+70.81), c0046 the "
     "logo said not to have made the cut before the end (h+76.89)",
     "the condition, that marking needs a work finished before the close, is held by A07's connection (the marking "
     "of the finished work) and by A07's own bound, read in its words (QD3-007): 'Where hour 73 cut the work "
     "unfinished, the room marks the attempt instead'", None),
    ("sheffield-045", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0042 the colour change reverted to green by someone (h+70.28), c0053 the work there at the end, about halfway "
     "through the colour change (h+73.05), c0056 thanks to everyone who helped",
     "the condition, that a marking can come while a planned redesign stays unfinished, is held by P05's statement "
     "(a change the room has planned is repaired away as damage until its keepers are told) and by A07's own bound, "
     "read in its words (QD3-007), the close cutting the change", None),
    ("stardustcrusaders-060", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0239 a celebration that the room did something, c0240 help filling the black sides, c0242 thanks while the "
     "hands may be too few to go bigger", EARLY + ", and by K02's statement (the room judges its hands too few)", None),
    ("timbers-037", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0041 the corner announced finished, c0042 different ideas for the star, c0043 a vote on the star and its "
     "defence, c0046 happiness at the work, c0048 three wrong pixels after defending",
     EARLY + ", by P02's statement (the room argues its design) and by P05's (defence)", None),
    ("touhou-049", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0090 a move from the finished point item to the bomb, c0102 a celebration of Marisa with Reimu set as the "
     "next goal",
     "the condition, that a marked work sends members to the next piece, is held by P02's statement (the room "
     "adds to its mark or enlarges it)", None),
    ("traaaaaaannnnnnnnnns-048", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0034 a celebration of flags appearing, c0035 a celebration of the flag reaching the edge, c0085 pride in "
     "fighting for hours to extend it", EARLY + ", and by P02's statement (the room enlarges its mark)", None),
    ("yugioh-058", "add-condition", "accept", "specification", "G4a (another element) and G39",
     "c0128 thanks for the Kuriboh, c0131 a celebration of four hours of work, c0117 the border almost finished, "
     "c0119 the Kuriboh announced finished and the turn to protection", EARLY, None),
    ("uofmn-047", "add-step", "accept", "none", "G4a (a counting rule) and G39",
     "c0010 a cheer that the M is completed (h+12.58), c0013 the M and the border done with a call to start the "
     "next words (h+27.26), each a marking that states the work done", ONE_ACT, None),
    ("warthunder-059", "contradict", "accept", "specification", "G9 and G39",
     "c0080 an edit reporting the left wing completed and the fuselage under way, c0081 a last edit saying the "
     "canvas ended halfway through the job, calling the plane a wreck and thanking all who helped (one item, "
     "h+58.89)",
     "the condition, that a work the close cut halfway is credited, is held by A07's own bound, read in its words "
     "(QD3-007): 'Where hour 73 cut the work unfinished, the room marks the attempt instead'; it is not one A07 "
     "lacks, so the line is no correction", None),
]


def packet_ids(op):
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A07", "--op", op,
                          "--offset", "0", "--limit", "100"], capture_output=True, text=True).stdout
    return [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]


ids = {op: packet_ids(op) for op in ("add-condition", "add-step", "contradict")}
for op, got in ids.items():
    mine = [r[0] for r in ROWS if r[1] == op]
    assert sorted(got) == sorted(mine) and len(set(mine)) == len(mine), (op, set(got) ^ set(mine))
with open("out/_analysis/d3_rulings/A07-adds.jsonl", "w") as f:
    for aid, op, dec, kind, rule, ev, held, pair in ROWS:
        row = {"adaptation": aid, "decision": dec}
        if kind:
            row["kind"] = kind
        if pair:
            row["pair"] = pair
        tail = held if kind in ("none", "elaboration") or dec == "particular" else held + "; a specification"
        row["reason"] = f"{rule}: {ev}; {tail}"
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A07-adds.jsonl")
