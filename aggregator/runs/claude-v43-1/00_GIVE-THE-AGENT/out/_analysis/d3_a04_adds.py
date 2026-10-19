#!/usr/bin/env python3
"""D3a-31: build A04's add-condition and add-step rulings (G4a and G36) from one table, so each id carries its own
evidence and the statement that holds its condition. Every id must be in the add packets, and every packet id here.
A row's last fields set the decision: a specification by default; an elaboration needs a pair.
Evidence paraphrases the packet's code labels; words in quotation marks were read through cite.py.

  python3 out/_analysis/d3_a04_adds.py
"""
import json
import subprocess
import sys

BOUND = ("the condition, that border talk can begin while the mark is being built or before any damage, is held by "
         "A04's own bound (late rooms asking for space before a mark to keep, entry through another room's offer, "
         "neighbours present from the first post, and first border talk that mostly offers terms before any damage)")
A17 = ("the condition, that border talk can answer the room's own encroachment on a neighbour's work, is held by A17 "
       "(the room's act against another room's work before its border talk; encroaching counts as an attack, G20)")
PARTNER = ("the condition, that the talk may be with a room other than the one that eroded the work, is held by A04's "
           "connection as G36 reads it ('The talk need not be with the room that caused the damage')")
ROWS = [
    ("AmericanFlaginPlace-026", "(4)", "c0086 a neighbour told to stop invading, then c0480 a GrowTheTree maintainer in the Road's Discord saying 'Rainbow expansion isn't sanctioned' and trolls 'are trying to blame stuff on Rainbow', and c0482 'This is not a r/ainbowroad project.' (h+67.96 to 68.54)",
     "working out who placed the pixels before treating the erosion as a neighbour's conduct is P06's form, a candidate, so stated nowhere in the model", "elaboration", "ucf-016"),
    ("GrowTheTree-028", "(1)", "c0028 'Negotations are in progress. Protect the foliage.' after the overwriting is named (h+43.25)",
     "the condition, that defence and talk run together in one post, is held by A04's connection as G36 reads one post (the damage named first, then talk)", None, None),
    ("ScottPilgrim-028", "(2)", "c0035 expansion rejected so as not to meet other creations, c0038 a request to spare Telegram, c0039 a compromise sought while most sprite workers cannot be controlled, c0040 an official truce asked",
     A17 + "; the limit on the placers is P21's form, as P21 now stands", None, None),
    ("TsundereSharks-040", "(1)", "c0012 the start moved to be amicable with r/kamenrider, c0017 a request to move elsewhere and c0018 agreement, c0019 another start rejected as still overlapping", BOUND, None, None),
    ("babymetal-032", "(1)", "c0092 r/ManningPlace changing its black ski mask to dark gray 'This way we can keep our face while you don't have to deal with the void', c0093 help asked and c0191 the agreement on Discord (h+71.72 to 72.87)", PARTNER, None, None),
    ("buffalobills-022", "(1)", "c0018 a compromise asked between overlapping keyblade and Bills builders, c0019 coordinates given, c0021 the logo declared done with outlining and protection after", BOUND, None, None),
    ("cirkeltrek-024", "(2)", "c0155 a neighbour asking the Dutch to stop invading Pusheen and c0307 an apology with a ribbon to dam in the westward expansion", A17, None, None),
    ("cmu-020", "(2)", "c0020 the lettering written out beside the Tartan, c0022 a neighbour asking CMU to stop messing with its space ship and c0023 an apology that still writes over the block", A17, None, None),
    ("danganronpa-028", "(2)", "c0128 help asked to place Kirigiri, c0133 a truce asked because the pixel art is destroying Taiwan's flag and c0135 agreement to keep off the flag", A17, None, None),
    ("de-049", "(2)", "c0467 the right part of the flag offered to Spain 'unter der Bedingung , dass sich die Spanier auch um unsere EU-Flagge kümmern', c0455 the same for rebuilding the EU flag, c0276 Sweden helped to take Denmark in return for help keeping the German flag clean",
     "the condition, that space and help are bartered for upkeep, is held by P16's statement (rooms barter help for space or repair) and A14 (border talk before help)", None, None),
    ("detroitredwings-048", "(1)", "c0005 r/unitedkingdom messaged about the border while the room concentrates north and c0007 mutual non-interference relayed despite a corner overlap", BOUND, None, None),
    ("drumcorps-018", "(1)", "c0109 a blob reported blocking the logo's right side and c0110 rust letting the logo build through", BOUND, None, None),
    ("esperanto-034", "(1)", "c0005 a place, enough people and a green team to negotiate with asked for, c0007 a flag started and reported gone", BOUND, None, None),
    ("ethereum-048", "(1)", "c0075 a deal with the Bob Ross people, c0077 and c0078 the sword's boundary claimed, c0080 the deal ended because the design conflicts", BOUND, None, None),
    ("farmcarrots-042", "(1)", "c0131 the farmers asked how the rainbow should pass, c0019 a collaboration on rainbow carrots and c0132 the revised route", BOUND + "; the joint mark is P17's", None, None),
    ("gravityfalls-025", "(1)", "c0037 Bill built and maintained all day, then c0043 r/SSMT's 'I can assure you that we will not mess with the actual bill drawing, and just the two border pixels' and c0044 'Feel free to move forward' (h+58.21 to 58.27)", PARTNER, None, None),
    ("greyblob-021", "(1)", "c0008 preparing for Dutch expansion, c0009 a treaty proposed for a Nail and Gear and c0024 a ceasefire with Armenia", BOUND, None, None),
    ("india-034", "(2)", "c0309 a call to expand India and take over, c0310 a plea not to take more of a squid and c0320 limits coordinated to stop wasting pixels", A17, None, None),
    ("latin-028", "(1)", "c0013 a request to move relayed while another spot is sought and c0018 a warning that green lattice cleans new pixels", BOUND, None, None),
    ("monalisaclan-033", "(1)", "c0092 a request to work around Love, c0093 a promise to keep the words and heart, c0100 an alliance asked around sacred ground and c0101 agreement not to take it", BOUND, None, None),
    ("newzealand-039", "(1)", "c0021 talk with the green-line group proposed, c0023 clear borders agreed, c0026 a warning that green through the flag would be war and c0027 the treaty invoked while watching others",
     BOUND + "; sparing by the settled border is A05's", None, None),
    ("pathofexile-024", "(2)", "c0100 a diplomat's request for a border compromise over the room's proposed extension and c0101 the talk moved to Discord", A17, None, None),
    ("pcmasterrace-034", "(2)", "c0493 'I am in negotiation with the blue corner to provide protection for us' (h+20.21) and c0556 the logo moved where 'They will protect our logo from vanadals' (h+21.44)",
     "the condition, that the room approaches a neighbour for protection rather than the one that eroded it, is held by A04's connection as G36 reads it and by A19 (upkeep before an alliance) and P16", None, None),
    ("pebble-046", "(1)", "c0036 a warning that BABYMETAL protects Kebble, c0037 space asked for a pebble logo, c0038 space suggested and c0043 a shift left with mutual help proposed", BOUND, None, None),
    ("placestart-026", "(2)", "c0031 a taskbar opposed because it would overwrite Starry Night, c0051 Starry Night promised its own window and c0120 Starry.bmp dropped after a compromise with France", A17, None, None),
    ("redhotchilipeppers-028", "(1)", "c0054 a call for help at the build, c0055 a warning that it is in r/greenlattice territory and c0058 an objection that the builders started without asking", BOUND, None, None),
    ("rhythmheaven-046", "(1)", "c0030 a warning that Play-Yan's feet will collide with the build, c0031 the builders asked to move and c0033 a leftward shift proposed", BOUND, None, None),
    ("sooners-017", "(2)", "c0012 a proposal to replace the University of Florida logo, c0013 a warning that TheWhiteVoid will defend it and c0014 a truce asked", A17, None, None),
    ("stlouisblues-032", "(1)", "c0005 a call for help before the blue corner consumes the Note, c0007 a plea to the advancing hearts and c0011 a formal request to build inside the blue corner", BOUND, None, None),
    ("suomi-034", "(3)", "c0095 'Annetaan tuon oikean kulman vihreän munamiehien olla nyt hetki ainakin rauhassa' (h+21.26), then c0105 a proposal that the avocados keep their row 'jos jättävät urkin muuten rauhaan. Edit Suostuivat heti' (h+25.50) and c0106 a check that Kekkonen is not under attack (h+25.63)",
     "the condition is a rule for counting, so the line is ruled by its concepts alone, which show terms offered to keep Urkki before any damage to it: A04's bound", None, None),
    ("taiwan-049", "(2)", "c0019 'people are erasing it' of a border the room is setting up and c0020 a member's apology (h+57.42 to 57.92), then c0065 'they've agreed to not build into our flag, however we need to give up our West wall' (h+70.97)",
     "the condition, that the room's own members erase an intended border, is held by P05's statement as move 173 left it (repair restores the known form, so a change the room plans is repaired away until the keepers are told) and P02's", None, None),
    ("texans-045", "(1)", "c0033 a push to finish through the sticky and c0034 a treaty with r/placehearts proposed", BOUND, None, None),
    ("torontoraptors-026", "(1)", "c0084 the Raptors logo asked to scoot and coexist with the Vikings and c0088 the white outline set on the right", BOUND, None, None),
    ("worldoftanks-025", "(1)", "c0112 the tank asked to move about 20 pixels to avoid a clash and c0113 compromise and overlap proposed; worldoftanks is one of the rooms the bound names", BOUND, None, None),
    ("xcom-044", "(1)", "c0017 XCOM asked to build elsewhere in the Blue Corner's space, c0020 a permitted spot chosen and c0028 constant overwatch called after finishing", BOUND, None, None),
    ("israel-026", "(2)", "c0053 'I have begun the invasion of the pixel pint' (h+21.21), c0059 'As one of the beer mug artists, I am bummed that I am being overwritten.' (h+23.38) and c0060 'If you allow us to build the flag then I'm sure we can work together to restore the beer mug' (h+23.40)",
     "the step, border talk that follows the room's own invasion of a neighbour's work, is held by A17 (the room's act against another room's work before its border talk)", None, None),
]


def packet_ids():
    ids = []
    for op, n in (("add-condition", 35), ("add-step", 1)):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A04", "--op", op,
                              "--offset", "0", "--limit", str(n)], capture_output=True, text=True).stdout
        ids += [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]
    return ids


ids = packet_ids()
mine = [r[0] for r in ROWS]
assert sorted(ids) == sorted(mine) and len(set(mine)) == len(mine), (set(ids) ^ set(mine))
with open("out/_analysis/d3_rulings/A04-adds.jsonl", "w") as f:
    for aid, clause, ev, held, kind, pair in ROWS:
        if kind == "elaboration":
            reason = f"G4a {clause} and G36: {ev}; {held}; a paired elaboration, as {pair} shows"
            row = {"adaptation": aid, "decision": "accept", "kind": "elaboration", "pair": pair, "reason": reason}
        else:
            reason = f"G4a {clause} and G36: {ev}; {held}; a specification"
            row = {"adaptation": aid, "decision": "accept", "kind": "specification", "reason": reason}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A04-adds.jsonl")
