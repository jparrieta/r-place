#!/usr/bin/env python3
"""D3a-35: build A08's add-condition and add-step rulings (G4a and G40) from one table, so each id carries its own
evidence and the statement that holds its condition. Every id must be in its packet, and every packet id here.
Evidence paraphrases the packet's code labels without quotation marks; the hours come from d3_cites_A08_adds.txt.

  python3 out/_analysis/d3_a08_adds.py
"""
import json
import subprocess
import sys

EARLY = ("the condition, that records can come while the work is still being built or before it stands, is held by "
         "P12's statement (the room records what happened to its work, at any hour), as G40 reads an early record of "
         "an unfinished work; it is not A08's order, and the census counts it apart")
ONE_ACT = ("the condition is a rule for counting, so the line is ruled by its concepts alone (G4a, a counting rule): "
           "they show one act holding a marking and a record (G40 counts it apart), so the order cannot be read; "
           "an evidence limit")

# (id, op, decision, kind, rule, evidence, held)
ROWS = [
    ("GrowTheTree-044", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0019 mourning what looks like the end of the tree (h+35.13) while the tree is still growing, c0053 a "
     "celebration that it survives (h+73.08), c0057 its apples remembered", EARLY),
    ("danganronpa-051", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0013 a Discord group deciding to make Monokuma, c0016 screenshots kept in case the work is taken over",
     EARLY),
    ("dwarffortress-051", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0100 a timelapse shared where both projects appear, c0155 a later piece announced complete", EARLY),
    ("kindafunny-023", "add-condition", "accept", "none", "G4a (a counting rule) and G40",
     "c0024 one post that marks the ended canvas as permanent and celebrates an almost intact mark", ONE_ACT),
    ("naruto-041", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0181 a cheer for a successful defence (h+71.71), c0183 Hakuto mourned (h+73.13), c0184 and c0198 the damage "
     "told as fixed by the close",
     "the condition, that the close makes damage permanent and turns members to mourning, is held by P12's statement "
     "(reports of fate, mourning, the end marked), at any hour; a cheer for a defence is not the marking of a "
     "finished work"),
    ("newzealand-043", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0177 a timelapse of the flag battle (h+24.98), then c0202 a cheer that the room did it (h+34.13) and c0435 the "
     "final version of the canvas (h+76.43)", EARLY + ", the battle being recorded while the flag was still fought "
     "over"),
    ("pokemon-063", "add-condition", "accept", "none", "G4a (a counting rule) and G40",
     "c0506 a list of sprites on the final canvas, c0507 additions invited, c0512 a member's own part claimed, in "
     "one catalogue", ONE_ACT),
    ("rhythmheaven-050", "add-condition", "accept", "specification", "G4a (the element states it) and G40",
     "c0043 thanks for the fun of a first project, then, in the same post, c0044 screenshots taken before the work "
     "is destroyed (h+50.09)",
     "the condition, that a marking is followed by a record kept against loss, is held by A08's own mechanism "
     "(marking the work together turns the room toward keeping it), which one post shows in its words"),
    ("samuraijack-044", "add-condition", "accept", "none", "G4a (a counting rule) and G40",
     "c0226 progress shots taken as Aku changed, c0227 thanks to everybody, in one contribution", ONE_ACT),
    ("stardewvalley-055", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0053 Estonia taking over the ancient fruit recounted, c0054 the lost starfruit mourned",
     "the condition, that a loss is recorded with no marking of a surviving work before it, is held by P12's "
     "statement (reports of fate, mourning) at any hour, as G40 reads the falsifier's second clause inside the "
     "rooms carrying both"),
    ("uofm-046", "add-condition", "accept", "specification", "G4a (another element) and G40",
     "c0003 adding to the M and asking for a snapshot once it is finished, c0005 going bigger from a template",
     EARLY),
    ("wildhockey-054", "add-condition", "accept", "none", "G4a (a counting rule) and G40",
     "c0165 one post that declares victory as the canvas ends and shares the record", ONE_ACT),
    ("satania-056", "add-step", "accept", "none", "G4a (a counting rule) and G40",
     "c0075 one post that celebrates keeping the work clean to the end", ONE_ACT),
    ("sooners-043", "add-step", "accept", "none", "G4a (a counting rule) and G40",
     "c0047 one post with an image that celebrates making it into the final piece", ONE_ACT),
    ("xenoblade_chronicles-049", "add-step", "accept", "none", "G4a (a counting rule) and G40",
     "c0066 one post that claims survival and presents the final product", ONE_ACT),
]


def packet_ids(op):
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A08", "--op", op,
                          "--offset", "0", "--limit", "100"], capture_output=True, text=True).stdout
    return [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]


ids = {op: packet_ids(op) for op in ("add-condition", "add-step")}
for op, got in ids.items():
    mine = [r[0] for r in ROWS if r[1] == op]
    assert sorted(got) == sorted(mine) and len(set(mine)) == len(mine), (op, set(got) ^ set(mine))
with open("out/_analysis/d3_rulings/A08-adds.jsonl", "w") as f:
    for aid, op, dec, kind, rule, ev, held in ROWS:
        row = {"adaptation": aid, "decision": dec, "kind": kind}
        tail = held if kind == "none" else held + "; a specification"
        row["reason"] = f"{rule}: {ev}; {tail}"
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A08-adds.jsonl")
