#!/usr/bin/env python3
"""D3a-33: build A06's add-condition rulings (G4a and G38) from one table, so each id carries its own evidence and the
statement that holds its condition. Every id must be in the add packet, and every packet id here. Evidence
paraphrases the packet's code labels, without quotation marks.

  python3 out/_analysis/d3_a06_adds.py
"""
import json
import subprocess
import sys

MECH = ("the condition, that machine hands follow where upkeep under attack is outrun, is held by A06's own mechanism "
        "('Upkeep under attack outruns what one pixel per interval can hold, and members turn to scripts and spare "
        "accounts to keep up')")
BOUND = ("the condition, that machine hands can serve building or gaining space rather than upkeep, is held by A06's "
         "own bound ('Where a room scripted the building itself from the start, machine hands come before any upkeep. "
         "Spare accounts can also serve an attack before any upkeep')")
ARG = ("the condition, that the turn to machine hands is argued over, refused or adjusted, is held by P14's statement "
       "(the room argues over these machine hands and adjusts them)")
ROWS = [
    ("Dominican-018", "(1)", "c0031 a warning that the heart flag is damaged, c0043 the small heart flag kept intact by hand",
     MECH + ", with P05's range (from one member fixing stray pixels)"),
    ("TsundereSharks-043", "(1)", "c0057 a warning that r/python's scripts may steamroll the shark, c0060 scripts proposed to fight back, c0085 a defence script made because everyone else uses scripts",
     MECH + ", an attack by others' scripts being upkeep under attack"),
    ("aggies-045", "(2)", "c0046 a warning that two scripts may conflict, c0135 old and new scripts found working against each other, c0136 changes stopped to avoid chaos", ARG),
    ("bitcoin-023", "(1)", "c0242 an attack reported and a script that could not run, c0245 the script updated for the France invasion, c0253 a question on running it with twenty alt accounts", MECH),
    ("chelseafc-027", "(2)", "c0168 the crest said to be impossible without bots, c0169 the mockup adapted after alliances were made",
     "the condition, that a room under strain can turn to allies and a changed design instead of bots, is held by A19's mechanism (a room keeping its work against attack joins other rooms facing the same threat), P02's statement (the room settles what its mark will show) and K02's (a work judged outclassed)"),
    ("dallasstars-013", "(1)", "c0091 a move after working against three bot artworks, c0097 a switch from a hand-built logo to a bot after the old location failed",
     MECH + ", the strain being the hand's own, and by P10's statement (moving after the work or the spot is lost)"),
    ("detroitredwings-044", "(1)", "c0060 a move beside the Leafs logo with a script promised, c0064 a script made to work and shared, c0074 a script brought out after three groups took the first space, c0117 a relocation and a bot recounted",
     BOUND + ", rebuilding at a new spot being building, and by P10's statement (moving after the spot is lost)"),
    ("dwarffortress-049", "(2)", "c0110 the fun of script-written art questioned, c0111 scripts defended for keeping work while away, c0130 people recruited to run the DwarfPlacer script",
     "the condition, that machine hands cover the hours members are away, is held by P05's statement and range (the room covers the night; shifts, scripts and calls to defend over many hours) and P14's argument"),
    ("epublica-015", "(2)", "c0016 helpers told to sweep vandalism, c0074 a script doubted as worthwhile with fewer than twenty people, c0075 a script agreed to if guided step by step",
     "the condition, that the turn to machine hands depends on enough runners and guidance, is held by K02's statement (the room judges it has too few hands) and P14's argument"),
    ("ethereum-051", "(3)", "c0076 four accounts dedicated to the drawing, c0113 r/monero's idea of automated maintenance borrowed, c0120 a script shared to keep the existing logo",
     "the condition is a rule for counting, so the line is ruled by its concepts: accounts given to the drawing come first, which A06's bound holds, and the later maintenance script is one act of upkeep and machine hands, as G38 reads G11"),
    ("france-039", "(2)", "c0304 a demand to stop scripts that obstruct the baguette, c0428 a warning that a defence bot freezes the flag and blocks new drawing",
     "the condition, that machine upkeep holds the known form against wanted changes, is held by P05's statement (repair restores the form the keepers know, so a planned change is repaired away until the keepers are told) and P14's adjusting"),
    ("frc-053", "(1)", "c0076 scripts defended as necessary against being overrun, c0152 a manual fix while the script has the same problem, c0040 a claim that bots and alts can take both spaces",
     MECH + "; hand upkeep beside the script is P05's, and scripts taking space are held by A06's bound"),
    ("kamenrider-048", "(2)", "c0047 rival scripts and few people said to make Mighty hard to keep whole",
     "the condition, that machine hands can stay too few against rival scripts, is held by K02's statement (the room judges it has too few hands, a work outclassed)"),
    ("monero-015", "(2)", "c0073 unattended bots gone rogue, c0077 a rogue bot stopped with a member's tip, c0081 differing scripts making helpers fight, c0130 consensus kept while versions conflict", ARG),
    ("mylittlepony-018", "(2)", "c0180 one person running several bots rejected, c0195 scripts said to take away from the event but be needed to compete, c0196 scripts allowed for defence while new art stays organic", ARG),
    ("placestart-010", "(1)", "c0028 a script growing the taskbar while members sleep, c0035 fourteen rows expanded automatically, c0397 a script offered for a working clock",
     BOUND + ", with P05's covering the night"),
    ("purdue-046", "(1)", "c0165 a script asked for because hand defence against Venezuela is hard, c0300 the script moved to cover more ground, c0301 work on the less contested side, c0304 victory declared as scripts gain the letters",
     BOUND + ", and by P09's statement, since encroaching counts as an attack (G20)"),
    ("rust-024", "(1)", "c0144 ruplace run so the Rust logo will be drawn, c0145 the outline tightened to move bot power to the logo", BOUND),
    ("sooners-008", "(1)", "c0023 a script recommended for a pixel-perfect image, c0042 the script run and the work covered with pink",
     BOUND + ", and by P04's statement (the template a bot follows)"),
    ("starlightstage-019", "(2)", "c0071 refreshing before placing and refusing to resort to bots, c0104 the pink line defended by hand for hours",
     "the condition, that a room under strain may refuse machine hands and keep by hand, is held by P14's argument and P05's statement, as G38 reads the falsifier's second clause"),
    ("texans-047", "(1)", "c0105 a script shared to protect the logo, c0112 the resort to the script justified because it was everywhere, c0121 the late resort acknowledged and defended",
     MECH + ", and by P14's argument"),
    ("unturned-017", "(2)", "c0122 scripts rejected for manpower and community, c0123 automation defended as matching the attackers, c0159 scripts called the reason the event is pointless", ARG),
    ("uofmn-037", "(1)", "c0080 a bot asked for against a suspected bot, c0081 bots reported keeping several logos including the room's",
     MECH + ", and by P14's statement as G24 reads a request"),
]


def packet_ids():
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A06", "--op", "add-condition",
                          "--offset", "0", "--limit", "23"], capture_output=True, text=True).stdout
    return [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]


ids = packet_ids()
mine = [r[0] for r in ROWS]
assert sorted(ids) == sorted(mine) and len(set(mine)) == len(mine), (set(ids) ^ set(mine))
with open("out/_analysis/d3_rulings/A06-adds.jsonl", "w") as f:
    for aid, clause, ev, held in ROWS:
        reason = f"G4a {clause} and G38: {ev}; {held}; a specification"
        f.write(json.dumps({"adaptation": aid, "decision": "accept", "kind": "specification", "reason": reason},
                           ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A06-adds.jsonl")
