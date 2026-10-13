#!/usr/bin/env python3
"""B4a-06: the conflicts pass (stage B4 section 4) over adjudication packet 6's theme notes alone
(out/_adjudication-B4/packet-06/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p05.py did for packet 5: two or more coders describing the same practice in
incompatible terms, seen across rooms, with the sibling pairs among the readings it may explain. Item keys are checked
against the store, each quoted term against its note, and the residual list is found from the notes' own words.
Appends once per packet; dry run unless --write."""
import importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
PACKET, LEG = 6, "B4a-06"

C = [
    {"id": "CC-049", "practice": "the room's joking, whatever it is about",
     "conflict": "Coders write the room's joking as one practice whether the joke is about the canvas work, the room's April Fools change, the room's ordinary talk or a rival: 'joking and drifting around the canvas talk', 'keeping April Fools and SpaceX jokes going beside the canvas work', 'Folding ordinary League talk into the April Fools performance'. The scheme splits it: the room's in-jokes carried into canvas talk (T3-031), the sub's ordinary talk with no canvas in it (T3-017), April Fools fakes and changes (T3-001, T3-023), taunts at rivals (T3-050), clashes told as fandom lore (T3-135). T3-031 is both readings' primary in 45 of packet 6's themes; the readings split T3-017|T3-031 in 12, T3-001|T3-031 and T3-023|T3-031 in 7 each, T3-031|T3-050 in 6.",
     "terms": {"purdue/t16": "joking and drifting around the canvas talk",
               "homestuck/t12": "turning canvas mishaps into Homestuck jokes",
               "spacexmasterrace/t12": "keeping April Fools and SpaceX jokes going beside the canvas work",
               "leagueoflegends/t05": "Folding ordinary League talk into the April Fools performance",
               "mexico/t17": "joking through the pixel war",
               "singapore/t04": "joking through the flag fight",
               "dragonquest/t06": "joking in Dragon Quest terms while defending the slime",
               "edmontonoilers/t12": "keeping the Off Day Talk memey despite removals"},
     "pairs": ["T3-017|T3-031", "T3-001|T3-031", "T3-023|T3-031", "T3-031|T3-050", "T3-031|T3-135"]},
    {"id": "CC-050", "practice": "explaining the event as the first step of recruiting",
     "conflict": "Coders join explaining what r/place is with bringing people into the room's work: 'Explaining r/place and bringing newcomers into the work', 'explaining r/place and recruiting more placers', 'explaining r/place and joining the cause'. The scheme splits the acts: the event explained (T3-016), calls to come and place (T3-002), a guide or template for the room's own work (T3-070), placing troubles worked around (T3-074). T3-016 is both readings' primary in 37 themes.",
     "terms": {"2007scape/t11": "Explaining r/place and bringing newcomers into the work",
               "leafs/t07": "explaining r/place and recruiting more placers",
               "metalcore/t05": "explaining r/place and joining the cause",
               "mexico/t11": "explaining r/place and recruiting more hands",
               "gratefuldead/t02": "explaining how to organize enough pixel help",
               "reddevils/t07": "bringing helpers into the badge build",
               "calgaryflames/t02": "showing people how to place a pixel",
               "aoe2/t02": "getting people onto the canvas and showing them how"},
     "pairs": ["T3-002|T3-016", "T3-016|T3-070", "T3-016|T3-074"]},
    {"id": "CC-051", "practice": "making sense of what the canvas shows",
     "conflict": "Coders write looking at the canvas as one practice of making sense of it, whether the event is explained, a detail decoded, a neighbour's picture named or an image recast as a joke: 'reading the canvas and explaining r/place', 'showing and making sense of the canvas result', 'mock-condemning what the canvas image looks like'. The scheme splits it four ways: the event (T3-016), a detail's meaning (T3-018), neighbouring pictures noticed with no meaning worked out (T3-052), jokes about what the room drew (T3-031). The readings split T3-018|T3-031 and T3-018|T3-052 in 6 themes each, T3-016|T3-018 in 4.",
     "terms": {"twice/t10": "reading the canvas and explaining r/place",
               "israel/t08": "asking and explaining what the canvas shows",
               "cmu/t05": "showing and making sense of the canvas result",
               "achievement_hunter/t04": "mock-condemning what the canvas image looks like",
               "rhythmheaven/t11": "reacting to the combined Noseyan picture",
               "thepointing/t06": "recognizing and explaining neighbouring pictures",
               "ghibli/t05": "checking whose mark is on the canvas",
               "serbia/t04": "recasting Pančevo through smoke and the void"},
     "pairs": ["T3-016|T3-018", "T3-018|T3-031", "T3-018|T3-052"]},
    {"id": "CC-052", "practice": "pacts, alliances and help traded written as one practice",
     "conflict": "As CC-037 in packet 5, now in G15's own themes: coders join truces, alliances, help traded and borders as one practice of making deals with neighbours: 'Negotiating borders, truces, and alliances', 'making truces, alliances, and room for neighbours', 'making alliances and trading help'. The scheme separates a pact to stop or avoid attacks between rooms in contact (T3-149), an alliance for defence or a fight (T3-150), help traded case by case (T3-151) and lines settled with no fight (T3-010). The readings' primaries: T3-149 24, T3-151 21, T3-150 18; split T3-010|T3-149 14, T3-150|T3-151 6, T3-010|T3-150 4, T3-010|T3-151 3.",
     "terms": {"ainbowroad/t05": "Negotiating borders, truces, and alliances",
               "denmark/t05": "making truces, alliances, and room for neighbours",
               "sooners/t05": "making peace and trading help",
               "TransFlagPlace/t05": "making alliances and trading help",
               "floridagators/t08": "making treaties and trading spare clicks with neighbors",
               "elitedangerous/t07": "Trading space and protection with canvas neighbours",
               "adventuretime/t06": "making truces, trading help, and sharing space",
               "palestine/t05": "making treaties and promising mutual defense",
               "smite/t08": "making peace and trading help with canvas neighbours"},
     "pairs": ["T3-149|T3-150", "T3-149|T3-151", "T3-150|T3-151", "T3-010|T3-149", "T3-010|T3-150", "T3-010|T3-151"]},
    {"id": "CC-053", "practice": "a deal's whole course: made, invoked, disputed, retold",
     "conflict": "Coders write a deal's course as one practice: making it, invoking it against a breach, disputing how it went and retelling it after the close: 'making, breaching, and repairing border deals', 'using the Mexico deal as a no-damage rule', 'recounting and arguing over who the Empire allied with'. The scheme splits the course: a new deal (T3-010, T3-149, T3-150, T3-151), an agreement invoked so the work goes on (T3-195), an alliance's conduct or worth disputed (T3-030), allies thanked and the alliance's story told after the close (T3-072).",
     "terms": {"AprilKnights/t06": "Posting the Peace Treaty again",
               "giivasunner/t11": "using the Mexico deal as a no-damage rule",
               "weezer/t06": "making, breaching, and repairing border deals",
               "empiredidnothingwrong/t22": "recounting and arguing over who the Empire allied with",
               "PinkUnion/t10": "contesting whether OSU overwrote Pink or only defended",
               "torontoraptors/t14": "arguing over the Vikings treaty through NFL rivalries",
               "hentai/t06": "making the leave-us-alone deal with Brazil hold",
               "wholesomememes/t24": "retelling flag fighting as treaties and coalition"},
     "pairs": ["T3-010|T3-195", "T3-149|T3-195", "T3-030|T3-195", "T3-030|T3-072", "T3-072|T3-149"]},
    {"id": "CC-054", "practice": "the homeland flag's whole life as one practice",
     "conflict": "Coders write the homeland flag's calls, plan, spot, build, repair and defence as one practice: 'calling people to make and keep the Bahraini flag', 'building and repairing Colombia's flag', 'Building, fixing, and defending the Union Jack'. T3-065's must_show takes calls to make the flag, its proportions, its spot and its repair; its siblings take the same acts for any other picture (T3-002 calls, T3-004 design, T3-020 spot, T3-038 placing, T3-021 repair, T3-005 defence), and of these only T3-002 is named in T3-065's must_not_show. T3-065 is both readings' primary in 22 themes; the readings split T3-002|T3-065 and T3-038|T3-065 in 4 each.",
     "terms": {"austria/t01": "calling people in to build together",
               "bahrain/t06": "calling people to make and keep the Bahraini flag",
               "colombia/t01": "building and repairing Colombia's flag",
               "unitedkingdom/t01": "Building, fixing, and defending the Union Jack",
               "armenia/t01": "planning where and how to make Armenian flags and hearts",
               "japan/t03": "placing, clearing, rebuilding and defending the flag",
               "Jamaica/t04": "making the first flag small enough to build and maintain",
               "mexico/t01": "deciding what and where to draw"},
     "pairs": ["T3-002|T3-065", "T3-038|T3-065", "T3-004|T3-065", "T3-020|T3-065", "T3-021|T3-065"]},
    {"id": "CC-055", "practice": "what goes on the flag, written as one choice",
     "conflict": "Coders write the choice of what goes on or beside the flag as one practice, whether the addition is a national emblem, a design detail, a further piece or a political mark: 'arguing over what to put on the flag', 'Choosing which British symbols belong in the display', 'adding Portuguese figures and jokes around the flag'. The scheme splits it: national emblems (T3-113), the look and size (T3-004), a further piece once a mark stands (T3-041), a political symbol argued over (T3-080). The readings split T3-004|T3-113 in 3 themes and T3-041|T3-113 in 2.",
     "terms": {"belgium/t05": "adding Belgian pictures and food to the flag",
               "ukplace/t02": "arguing over what to put on the flag",
               "unitedkingdom/t03": "Choosing which British symbols belong in the display",
               "portugal/t14": "adding Portuguese figures and jokes around the flag",
               "serbia/t10": "proposing lettering, symbols and additions around the flag",
               "colombia/t05": "drawing Colombian and shared marks onto the flag",
               "afip/t03": "putting words, symbols, and borders on the flag"},
     "pairs": ["T3-004|T3-113", "T3-041|T3-113", "T3-080|T3-113"]},
    {"id": "CC-056", "practice": "national rivalry as banter",
     "conflict": "Coders write joking between nations over the flags as one practice of banter: 'turning flags and neighbours into banter', 'turning flag rivalry into nationalist banter', 'turning neighbouring flags into European war jokes'. The scheme splits the joke by its target and frame: taunts at a rival community (T3-050), jokes, insults or slurs aimed at a rival people (T3-142), a fight told in a nation's history of war (T3-081), the room's own in-jokes (T3-031). One note often holds all four.",
     "terms": {"france/t13": "turning flags and neighbours into banter",
               "romania/t16": "turning flag rivalry into nationalist banter",
               "unitedkingdom/t08": "Turning flag wars into banter and self-mockery",
               "belgium/t06": "turning neighbouring flags into European war jokes",
               "southafrica/t03": "joking through the pixel wars",
               "norway/t08": "joking in flags, sovereign land, and displaced migrants",
               "GranColombia/t03": "making belga jokes",
               "malta/t05": "turning lost flags into Malta jokes"},
     "pairs": ["T3-031|T3-050", "T3-050|T3-142", "T3-031|T3-081", "T3-050|T3-081"]},
    {"id": "CC-057", "practice": "the room's own world used to do the canvas work",
     "conflict": "Coders write the room's own register (a game, a film, a crusade, communist history, a mock state) as the way the canvas work is done: 'doing pixel work as EVE operations', 'turning pixel work into a Crusade', 'turning the canvas fight into communist stories'. The scheme reads the register by what it carries: in-jokes with no clash (T3-031), a clash told as fandom lore (T3-135), a fight told as national history (T3-081), the work itself (T3-002, T3-005). Whether a register that recruits or names targets is a joke or the work is left to the reader.",
     "terms": {"eve/t12": "doing pixel work as EVE operations",
               "CKCrusaders/t06": "turning pixel work into a Crusade",
               "fullcommunism/t06": "turning the canvas fight into communist stories",
               "masseffect/t10": "turning canvas conflict into Mass Effect jokes",
               "survivor/t21": "turning border fights into Survivor catchphrases",
               "prequelmemes/t09": "turning pixel work into prequel lines and jokes",
               "enterthegungeon/t13": "carrying pixel defense into Gungeon rituals and run stories",
               "indonesia/t07": "playing president, parliament and war command"},
     "pairs": ["T3-031|T3-135", "T3-081|T3-135", "T3-031|T3-081"]},
    {"id": "CC-058", "practice": "settling what happened after the close",
     "conflict": "After the close, coders write victory, blame, the room's own conduct and the taunt that outlasts the event as one practice of settling what happened: 'celebrating and retelling Dutch conquest', 'settling scores with r/49ers after the end', 'Judging what the room did after placement ended'. The scheme splits it: victory claimed over rivals (T3-154), blame laid after the close (T3-058), an alliance's conduct disputed (T3-030), what happened to the work told (T3-073), taunts (T3-050), the finished work celebrated with no rival (T3-009).",
     "terms": {"PlaceNL/t12": "celebrating and retelling Dutch conquest",
               "gamindustri/t15": "settling scores with r/49ers after the end",
               "croatia/t17": "Judging what the room did after placement ended",
               "russia/t13": "marking what happened to the flags",
               "notredame/t09": "working out what winning meant",
               "falcons/t17": "settling what the finished canvas means",
               "orderofthebluecorner/t10": "celebrating blue prevailing and retaining the corner"},
     "pairs": ["T3-050|T3-154", "T3-058|T3-154", "T3-009|T3-154", "T3-030|T3-073"]},
    {"id": "CC-059", "practice": "politics read from the flags, written as one argument",
     "conflict": "Coders write politics argued from the canvas as one practice: 'arguing over whether the flag is Europe, the EU, or nations', 'turning pixel conflict into arguments about nationalism', 'Arguing Canada and Quebec through the canvas'. The scheme has five neighbours in G17 and G18, split by what is argued: one symbol (T3-080), national politics (T3-130), ideology in general (T3-179), a fight told as national history (T3-081), national belonging (T3-180). One note commonly moves among three of them.",
     "terms": {"europe/t05": "arguing over whether the flag is Europe, the EU, or nations",
               "de/t13": "turning pixel conflict into arguments about nationalism",
               "afip/t06": "keeping party claims off the flag",
               "animalcrossing/t12": "arguing about communism while trying to celebrate the leaf",
               "canada/t08": "Arguing Canada and Quebec through the canvas",
               "quebec/t11": "turning the pixel fight into Québec history and identity",
               "polska/t07": "arguing over what the pixel project means",
               "placesnek/t06": "keeping 'No Step On Snek' while arguing over politics and ownership"},
     "pairs": ["T3-080|T3-130", "T3-080|T3-179", "T3-081|T3-130", "T3-130|T3-180", "T3-046|T3-179"]},
    {"id": "CC-060", "practice": "a colour faction's spreading, faith and purity as one practice",
     "conflict": "Coders write a colour faction's spreading, its defence, its faith and its arguments over purity as one practice of the faction: 'Spreading red and redirecting the fight', 'joining and preaching the lattice', 'defending a pure lattice as art and home'. The scheme splits them: the colour spread as territory (T3-171), loyalty professed in talk (T3-174), a doctrine dispute that divides the faction (T3-190), a rival's work defaced (T3-006), a picture extended into a neighbour's space (T3-061).",
     "terms": {"AprilKnights/t03": "Spreading red and redirecting the fight",
               "GreenCorner/t04": "spreading green and choosing what to build",
               "greyblob/t03": "choosing where the grey should spread",
               "PurplePixels/t02": "claiming and holding the Purple Corner",
               "greenlattice/t02": "joining and preaching the lattice",
               "purplecorner/t01": "rallying around purple as a cause",
               "greenlattice/t15": "defending a pure lattice as art and home",
               "purplecorner/t02": "taking and holding purple ground",
               "fullcommunism/t03": "taking flags and spreading red"},
     "pairs": ["T3-171|T3-174", "T3-171|T3-190", "T3-006|T3-171", "T3-174|T3-190"]},
    {"id": "CC-061", "practice": "offensive material posted, called out and policed, kept as one practice",
     "conflict": "Coders keep offensive material and the answers to it in one theme, written as one practice of pushing or policing a boundary: 'using the day to post offensive and taboo material', 'bringing offensive canvas material into SRS', 'dismissing repair talk with a homophobic slur'. The scheme splits the act: slurs and ethnic jokes at a rival people (T3-142), argument over whether a joke offends (T3-143), bigotry in the room's talk shut down (T3-182), hate symbols on the canvas covered (T3-146), calls to draw swastikas (T3-177), objection to April Fools posts (T3-032).",
     "terms": {"ultrahardcore/t07": "using the day to post offensive and taboo material",
               "shitredditsays/t02": "bringing offensive canvas material into SRS",
               "shitredditsays/t08": "an old, normalized ableist joke",
               "roosterteeth/t08": "condemning Nazi symbols and refusing to vandalise related art",
               "costa_rica/t10": "dismissing repair talk with a homophobic slur",
               "wow/t10": "arguing whether racism belongs in the joke thread",
               "achievement_hunter/t02": "contesting FunHaus space with petitions, fights, and swastika jokes",
               "EraseThePlace/t08": "policing purity, discrimination, and who belongs"},
     "pairs": ["T3-142|T3-143", "T3-143|T3-182", "T3-146|T3-177", "T3-032|T3-142", "T3-032|T3-182"]},
]

RESIDUAL = re.compile(r"belongs with no other|single-code|single code|stands alone|singleton|belongs with nothing|no other practice|no other code|shares no|cannot safely join|lone trace|belongs with neither|belongs with no broader|remains its own|This single|isolated code|isolated title|single surviving title|sole surviving title|single thin code|single ambiguous passage|single visitor report|single visitor request|single passage|is its own practice|Nothing else in the pool", re.I)


def main():
    store = bpf.pk.Store(ROOT, OUT)
    notes = open(os.path.join(OUT, "_adjudication-B4", "packet-%02d" % PACKET, "notes.md"), encoding="utf-8").read().splitlines()
    resid = []
    for ln in notes:
        m = re.match(r"- ([^/\s]+)/(t\d+) \((.*?)\): (.*)$", ln)
        if m and RESIDUAL.search(m.group(4)):
            resid.append("%s/%s" % (m.group(1), m.group(2)))
    rows = []
    for c in C:
        bad = [k for k in c["terms"] if tuple(k.split("/")) not in store.themes]
        if bad:
            sys.exit("%s: not in the store: %s" % (c["id"], bad))
        miss = [k for k, v in c["terms"].items() if not any(ln.startswith("- %s (" % k) and v in ln for ln in notes)]
        if miss:
            sys.exit("%s: term not found in its note: %s" % (c["id"], miss))
        rows.append({"id": c["id"], "packet": PACKET, "leg": LEG, "pass": "theme_note alone", "practice": c["practice"],
                     "conflict": c["conflict"], "items": sorted(c["terms"]), "subs": sorted({k.split("/")[0] for k in c["terms"]}),
                     "terms": c["terms"], "pairs_it_may_explain": c["pairs"]})
    rows.append({"id": "CC-062", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008, CC-016, CC-025, CC-036 and CC-048: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme', 'stands alone'), often a surviving title whose body was deleted or one reply, so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-016|T3-031", "T3-018|T3-052", "T3-031|T3-057"]})
    p = os.path.join(OUT, "coder_conflicts.jsonl")
    if os.path.exists(p) and any(json.loads(x).get("packet") == PACKET for x in open(p, encoding="utf-8") if x.strip()):
        sys.exit("coder_conflicts.jsonl already holds packet %d's conflicts" % PACKET)
    for r in rows:
        print("%s %s: %d items over %d rooms" % (r["id"], r["practice"], len(r["items"]), len(r["subs"])))
    print("residual items: " + ", ".join(sorted(set(resid))))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("coder_conflicts.jsonl now %d lines" % sum(1 for x in open(p, encoding="utf-8") if x.strip()))


if __name__ == "__main__":
    main()
