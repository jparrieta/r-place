#!/usr/bin/env python3
"""D3a-30: build A03's add-condition and add-step rulings (G4a and G35) from one table, so each id carries its own
evidence and the statement that holds its condition. Every id must be in the add packets, and every packet id here.

  python3 out/_analysis/d3_a03_adds.py
"""
import json
import subprocess
import sys

OVERLAP = ("the condition, that upkeep can begin on placed parts while building continues, is held by A03's own "
           "connection (a build report, G15, not a completion) and mechanism ('a finished part is something to lose')")
ROWS = [
    ("EraseThePlace-036", "(2)", "c0228 a forward base fortified before expansion, c0249 the triangle nearly finished and c0176 defence and cleaning put first", "the condition, upkeep put before growth, is held by P05's statement ('puts upkeep before growth')", "P05"),
    ("Rainbow6-019", "(1)", "c0195 'Its done :D', c0196 a switch to maintaining, and c0511 a call to finish and maintain a sign", OVERLAP, "A03"),
    ("SwissNeutralityZone-042", "(1)", "c0003 red called for around the stable cross and c0063 the flag, cheese and mountains defended", OVERLAP, "A03"),
    ("anime-019", "(1)", "c0202 Emilia progress reported, c0203 a backdrop directed and c0204 a call to protect Emilia", OVERLAP, "A03"),
    ("azerbaijan-012", "(2)", "c0004 the flag one Azeri could do shown and c0008 'r/place is over'", "the condition, that upkeep follows a report only while placing is open, is held by P12's statement ('the end marked') and P03 read only before hour 73 (G15)", "P12"),
    ("babymetal-020", "(1)", "c0017 clean-up put before advancing the drawing, c0043 the art announced finished and c0063 odd vandalism fixed after it", OVERLAP, "A03"),
    ("bobross-054", "(1)", "c0001 a chibi made, c0002 a call to protect Bob, then c0003 and c0004 an easel added", OVERLAP, "A03"),
    ("bostonbruins-044", "(1)", "c0054 the B kept against repeated attacks and c0058 builders told to ignore griefers and complete the B", OVERLAP, "A03"),
    ("catholicism-020", "(2)", "c0066 a call to defend the vandalised cross heart and c0123 the spot secured before adding to it", "the condition, keeping put before additions, is held by P05's statement ('puts upkeep before growth')", "P05"),
    ("cirkeltrek-018", "(1)", "c0029 a petition to continue the anthem while fixing the missing space", OVERLAP, "A03"),
    ("danganronpa-020", "(1)", "c0075 a mostly finished sprite with repairs noted, c0076 slow rebuilding under griefing and c0077 the last pixel claimed", OVERLAP, "A03"),
    ("drumcorps-014", "(1)", "c0109 a blob reported blocking the logo's right side and c0111 overnight work redirected to borders and stray squares", OVERLAP, "A03"),
    ("dwarffortress-046", "(1)", "c0004 a dwarf head built with a request to help maintain it and c0005 efforts spent keeping it clean", OVERLAP, "A03"),
    ("ethereum-047", "(1)", "c0074 a plan to divide the work, then enlarge and defend, c0105 a logo rejected without proper maintenance and c0134 newcomers told to fix stray pixels", "the condition, building planned before defence, is A03's own order, held by its connection", "A03"),
    ("finland-038", "(1)", "c0063 the coat-of-arms border started, c0064 its pixels reported removed and c0065 a call for more people", OVERLAP, "A03"),
    ("fullcommunism-034", "(2)", "c0014 a hammer and sickle reported with an anarchy symbol added, and c0015 'clean, defend, then spell FALGSC'", "the condition, further lettering after cleaning and defence, is held by P05's statement ('puts upkeep before growth')", "P05"),
    ("furry-022", "(1)", "c0027 the work celebrated while trolls are fought, c0219 a completed Snoo shown and c0220 the Snoo protected", OVERLAP, "A03"),
    ("futurama-036", "(1)", "c0021 a call to build and maintain Bender, c0086 a call to restore him and c0114 an account of pixels, border work and fighting", OVERLAP, "A03"),
    ("gorillaz-023", "(1)", "c0046 'We Need More Help on /r/place making 2-D and Noodle'", OVERLAP, "A03"),
    ("gravityfalls-017", "(1)", "c0037 a member building and maintaining Bill all day", OVERLAP, "A03"),
    ("kpop-045", "(1)", "c0025 the words begun, c0027 a wrong colour, then c0030 a border around the finished words and c0031 overwriting held off", "the condition, building before border and defence, is A03's own order, held by its connection", "A03"),
    ("latin-019", "(1)", "c0029 vandals fought before the work is declared perfect and c0003 completion celebrated with a call for upkeep", OVERLAP, "A03"),
    ("lsu-041", "(1)", "c0051 red pixels fixed with a call to defend, then c0052 a defender switching to building by the pipe", "the condition, that a defender may turn back to building, is consistent with A03's connection, which orders only the first report and the first upkeep", "A03"),
    ("metalgearsolid-021", "(1)", "c0051 work redirected from the border to defending Snake's head and c0061 a small box built", OVERLAP, "A03"),
    ("monalisaclan-022", "(1)", "c0091 filling put before fixing small mistakes and c0257 an account of building, defending and perfecting her", OVERLAP, "A03"),
    ("monsterhunter-018", "(2)", "c0158 and c0172 calls to protect the potion, then c0159 and c0173 its defenders told it is no longer in the plan", "the condition, that keeping lasts while the piece stays in the agreed plan, is held by P05's statement as move 173 left it (a change the room agrees is repaired away until the keepers are told, and given up where they are) and P02's", "P05 and P02"),
    ("necrodancer-017", "(1)", "c0015 a warning that the foot is being taken, c0016 the face finished first and c0019 'they did it'", OVERLAP, "A03"),
    ("nlsscirclejerk-034", "(1)", "c0061 a call to repair so others can build, c0071 the build declared done and c0029 griefing warned of while expanding", OVERLAP, "A03"),
    ("polska-045", "(1)", "c0011 r/Polska celebrated as having done it and c0012 'Właśnie poprawiłem piksela.'", OVERLAP, "A03"),
    ("purplecorner-045", "(1)", "c0109 five hours of maintaining and expanding the lattice reported and c0022 a push to complete the text", OVERLAP, "A03"),
    ("qotsa-012", "(2)", "c0022 a member chipping in as the logo takes shape, then c0046 and c0048 the icon too late before Place ended", "the condition, that building can end at the close before any upkeep, is held by P12's statement ('the end marked') and P03 read only before hour 73 (G15)", "P12"),
    ("ravens-021", "(1)", "c0048 coordinates with a call for clean-up, c0053 a warning about r/steelers and c0063 the unfinished logo lamented at the close", OVERLAP, "A03"),
    ("sakuragakuin-013", "(1)", "c0002 'We've completed the banner and logo, now it's just cleanup around the logo and defence', then c0044 a new logo started", OVERLAP, "A03"),
    ("sixers-046", "(1)", "c0015 TRUST THE PROCESS begun with a call to keep it clean, c0025 TTP completed and c0085 upkeep here and there", OVERLAP, "A03"),
    ("splatoon-037", "(1)", "c0053 a call to build a green squiddy and c0055 building while someone keeps making a box", OVERLAP, "A03"),
    ("stlouisblues-021", "(1)", "c0045 a plan to keep the work after completion and c0075 the skyline shifted and the Note cleaned", OVERLAP, "A03"),
    ("streetfighter-017", "(2)", "c0019 a white dot placed and c0027 the dot immediately replaced", "the condition, that keeping needs a placement the room can hold, is held by K02's statement (too little room or too few hands)", "K02"),
    ("the_pack-020", "(1)", "c0049 correct text before a border, c0052 a job repairing the sign and building MFER, and c0077 a repair that makes vandalism harder", OVERLAP, "A03"),
    ("timbers-033", "(1)", "c0041 the Portland corner announced finished, c0043 one star voted correct and defended, and c0048 the crest defended to the end", OVERLAP, "A03"),
    ("touhou-019", "(1)", "c0147 'Good work team! Now back to defense!', c0090 a move onto the bomb and c0102 Reimu set as the next goal", OVERLAP, "A03"),
    ("uofm-016", "(1)", "c0004 the M grown while borders are protected, c0243 the finished picture reported ruined and c0116 protectors asked for", OVERLAP, "A03"),
    ("yugioh-020", "(1)", "c0103 the yellow outline placed, c0107 pieces reported overwritten, c0119 the Kuriboh finished and c0129 pieces fixed", OVERLAP, "A03"),
    ("reddevils-046", "(2)", "c0104 an intruding symbol erased to distract its makers while others finish the crest, and c0154 the crest declared complete and the points held", "the step, defence by erasing an intruder's pixels during building, is held by P05's statement (the room rallies to defend under attack)", "P05"),
]


def packet_ids():
    ids = []
    for op, n in (("add-condition", 42), ("add-step", 1)):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", "A03", "--op", op,
                              "--offset", "0", "--limit", str(n)], capture_output=True, text=True).stdout
        ids += [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]
    return ids


ids = packet_ids()
mine = [r[0] for r in ROWS]
assert sorted(ids) == sorted(mine) and len(set(mine)) == len(mine), (set(ids) ^ set(mine))
with open("out/_analysis/d3_rulings/A03-adds.jsonl", "w") as f:
    for aid, clause, ev, held, name in ROWS:
        reason = f"G4a {clause} and G35: {ev}; {held}; a specification naming {name}"
        f.write(json.dumps({"adaptation": aid, "decision": "accept", "kind": "specification", "reason": reason},
                           ensure_ascii=False) + "\n")
print("wrote", len(ROWS), "rulings to out/_analysis/d3_rulings/A03-adds.jsonl")
