#!/usr/bin/env python3
"""B4a-05: the conflicts pass (stage B4 section 4) over adjudication packet 5's theme notes alone
(out/_adjudication-B4/packet-05/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p04.py did for packet 4: two or more coders describing the same practice in
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
PACKET, LEG = 5, "B4a-05"

C = [
    {"id": "CC-037", "practice": "every dealing with a neighbour written as one practice",
     "conflict": "116 of packet 5's themes have T3-010 as a reading's primary, and their coders join borders, truces, alliances, help traded and help given under one practice of dealing with neighbours: 'making and keeping deals with neighbours', 'working out borders, truces, and help with neighbours', 'making treaties and trading help across borders'. The scheme splits these acts across G14 and G15: borders settled with no fight to end (T3-010), a truce between rooms already in contact (T3-149), an alliance for defence or a fight (T3-150), help traded case by case (T3-151), help sent with nothing asked (T3-011). One note often holds four of them.",
     "terms": {"aoe2/t06": "making and keeping deals with neighbours",
               "bisexual/t05": "working out borders, truces, and help with neighbours",
               "europe/t03": "bargaining over borders and sharing pixel help",
               "uiuc/t11": "negotiating borders truces and mutual protection",
               "placestart/t08": "making treaties and trading help across borders",
               "sweden/t03": "Making peace, bargains, and room for neighbours",
               "hawks/t06": "making deals and helping canvas neighbours",
               "radiohead/t04": "making peace and trading help with neighbours",
               "NieR/t11": "working out help and borders with neighboring communities",
               "mylittlepony/t07": "making peace and trading watch with canvas neighbors",
               "formula1/t10": "making deals and helping canvas neighbours",
               "uwaterloo/t07": "bargaining over borders and mutual help"},
     "pairs": ["T3-010|T3-149", "T3-010|T3-150", "T3-010|T3-151", "T3-010|T3-011", "T3-011|T3-151", "T3-149|T3-150"]},
    {"id": "CC-038", "practice": "making room for a neighbour, whatever the reason",
     "conflict": "Coders name 'making room' as one practice whether the room holds back by its own choice, settles a border, yields to a neighbour's request or grants space in its own design: 'finding room without wrecking neighbours', 'moving over and making room with neighbours', 'moving the logo after being asked off the bi flag'. The scheme splits it four ways: restraint with no request (T3-024), a border settled (T3-010), yielding when asked (T3-039), and granting a neighbour room on or beside the work (T3-012). 17 themes have T3-010 and T3-024 as their two readings' primaries.",
     "terms": {"49ers/t05": "finding room without wrecking neighbours",
               "riskofrain/t04": "finding room without taking over creations",
               "starcraft/t10": "working out overlaps without wrecking neighbors",
               "theexpanse/t04": "making room with neighbors and helping their work",
               "bangtan/t05": "making room around the logo",
               "truestl/t03": "moving over and making room with neighbours",
               "TsundereSharks/t05": "making room with the neighbours",
               "pebble/t03": "moving Pebble away from guarded neighbours",
               "qotsa/t05": "moving the logo after being asked off the bi flag",
               "rocketbeans/t08": "making room for neighbouring pictures",
               "asexual/t07": "making room with nearby pictures"},
     "pairs": ["T3-010|T3-024", "T3-010|T3-039", "T3-024|T3-039", "T3-010|T3-012", "T3-012|T3-039"]},
    {"id": "CC-039", "practice": "taking a neighbour's ground, written as one practice",
     "conflict": "Coders write raiding, annexing, converting and spreading a colour as one practice of taking: 'calling for orange attacks and annexations', 'spreading red and taking over rival marks', 'taking over and sabotaging other flags'. The scheme asks what the taking is for: destroying or erasing another room's work (T3-006), growing the room's own work over a neighbour's space (T3-061), turning another's art into the room's sign (T3-068), or a colour faction spreading (T3-171). T3-006's must_not_show sends the second and third away and does not name the fourth.",
     "terms": {"cirkeltrek/t07": "calling for orange attacks and annexations",
               "denmark/t04": "overwriting rivals and expanding Danish work",
               "TheFarLeftSide/t04": "spreading red and taking over rival marks",
               "minecraft/t10": "Pushing Minecraft art through other people's work",
               "dankmemes/t11": "Raiding and taking spots on the canvas",
               "PlaceNL/t06": "expanding, attacking, and claiming orange ground",
               "kurdistan/t02": "taking over and sabotaging other flags",
               "torontoraptors/t07": "looking for logos and images to take over",
               "ice_poseidon/t07": "Expanding purple territory and attacking blue",
               "norge/t02": "fighting for more canvas and defending it",
               "palestine/t02": "turning other flags and symbols into Palestine"},
     "pairs": ["T3-006|T3-061", "T3-006|T3-068", "T3-006|T3-171", "T3-061|T3-068", "T3-061|T3-171"]},
    {"id": "CC-040", "practice": "a call to attack and its refusal kept as one practice",
     "conflict": "Coders keep a call to attack and the replies that refuse it in one theme, as one practice of deciding whether to attack: 'proposing raids and talking each other out of them', 'weighing attacks and taunts against maintaining Ohio', 'deciding whether to attack or keep the peace'. serbia t03's note says disagreement 'is part of the theme, not evidence of one settled position'. The scheme places the call (T3-006) apart from members told to stop an attack (T3-076), restraint before any attack (T3-024), an attack refused because the room cannot hold more (T3-042) and the argument whether covering is fair (T3-046). A reader may place the call, the refusal, or both.",
     "terms": {"mexico/t02": "proposing raids and talking each other out of them",
               "ohio/t06": "weighing attacks and taunts against maintaining Ohio",
               "leafs/t06": "deciding whether to attack rival pictures",
               "tampabaylightning/t12": "deciding whether to join attacks on rival marks",
               "serbia/t03": "arguing over attacking other people's canvas work",
               "vegan/t13": "counterattacking and deciding when not to escalate",
               "cloud9/t06": "arguing over attacking neighbours' art",
               "Temple/t05": "deciding whether to attack or keep the peace",
               "predators/t16": "weighing attacks against keeping their own logo",
               "WisconsinBadgers/t04": "arguing over sabotaging neighbors or protecting their own",
               "farmcarrots/t11": "arguing over whether farmers should attack",
               "portugal/t17": "deciding whether to attack neighbouring flags"},
     "pairs": ["T3-006|T3-076", "T3-006|T3-042", "T3-006|T3-024", "T3-006|T3-046", "T3-024|T3-076", "T3-042|T3-076"]},
    {"id": "CC-041", "practice": "the argument over taking another's work, folded into the act",
     "conflict": "Coders write an argument over whether taking another room's work is right as the same practice as the room's restraint, its borders or its attacks: 'arguing for peace instead of stomping over others', 'arguing over how much neighbour art to overwrite', 'arguing whether Place meant conquest or drawing together'. The scheme gives the argument its own theme (T3-046, 'an open canvas where anything goes, or a wrong done to others' effort') and places restraint (T3-024), members told to stop (T3-076), borders (T3-010) and attacks (T3-006) apart. The 'arguing over' labels do not say whether the argument or the act it settles leads.",
     "terms": {"kingdomhearts/t22": "arguing for peace instead of stomping over others",
               "malaysia/t06": "arguing over how much neighbour art to overwrite",
               "PlaceNL/t17": "arguing whether Place meant conquest or drawing together",
               "sooners/t04": "arguing over taking someone else's logo",
               "canucks/t33": "arguing that rival vandalism was harmless rivalry",
               "slovenia/t04": "arguing where their pixels should stop",
               "FaroeIslands/t04": "arguing over taking, sharing and leaving other flags alone",
               "bostonceltics/t08": "arguing over attacking, whitening and truce",
               "osugame/t07": "Arguing over size, scripts, and whose art counted"},
     "pairs": ["T3-024|T3-046", "T3-046|T3-076", "T3-010|T3-046", "T3-006|T3-046"]},
    {"id": "CC-042", "practice": "an old rivalry carried onto the rival's mark",
     "conflict": "Sports, school and fandom rooms carry an old rivalry onto the rival's mark: 'taking the rivalry onto other logos', 'turning Michigan rivalry into canvas attacks', 'putting 42-39 by Penn State'. The coders write attack, taunt and conversion as one practice. The scheme splits them: an attack meant to destroy (T3-006), a taunt (T3-050), the rival's mark turned into the room's sign (T3-068) and the community's own rivalry carried onto the canvas (T3-086). T3-050's must_not_show sends the sub's own quarrel to T3-086, and T3-086's sends taunts to T3-050.",
     "terms": {"floridagators/t07": "taking the rivalry onto other logos",
               "cardinals/t05": "attacking and joking with the Cubs logo",
               "greenbaypackers/t15": "turning attention and pixels against the Bears",
               "osu/t02": "turning Michigan rivalry into canvas attacks",
               "pitt/t04": "putting 42-39 by Penn State",
               "sabres/t05": "changing rival marks into Buffalo jokes and targets",
               "lakers/t08": "covering Celtics green with purple and gold",
               "edmontonoilers/t01": "calling to replace or recolour Calgary's logo",
               "muse/t06": "turning band rivalry into attacks, retreats, and jokes",
               "utaustin/t03": "taking rivals' space and changing their marks"},
     "pairs": ["T3-006|T3-086", "T3-006|T3-050", "T3-006|T3-068", "T3-050|T3-086"]},
    {"id": "CC-043", "practice": "help between rooms, whichever way it runs",
     "conflict": "Coders name help between rooms as one practice whichever way it runs: 'asking for, offering, and trading help', 'giving and receiving help across community boundaries', 'helping Hoodr and accepting Hoodr's help'. The scheme splits by direction and terms: help sent, or the room called to send it (T3-011); a request from the room to another (T3-084); help traded for help (T3-151); calls carried into other subs' membership (T3-062); an alliance (T3-150). A theme holding a request received and the help sent meets T3-011's 'or called to' and T3-084's 'asking for help' at once.",
     "terms": {"msu/t05": "asking for, offering, and trading help",
               "czech/t05": "asking neighbours for help and paying help back",
               "furry_irl/t13": "giving and receiving help across community boundaries",
               "epublica/t12": "helping Hoodr and accepting Hoodr's help",
               "uofmn/t06": "calling Big Ten neighbours to help one another",
               "europe/t10": "calling national subreddits into flag work",
               "parrots/t05": "sending help between parrot efforts",
               "monalisaclan/t12": "answering calls to help other pictures",
               "chicubs/t12": "asking Cubs users to help other teams' marks",
               "uvic/t02": "Helping west coast schools stick together"},
     "pairs": ["T3-011|T3-084", "T3-011|T3-151", "T3-084|T3-151", "T3-011|T3-062", "T3-084|T3-150"]},
    {"id": "CC-044", "practice": "a host's admission and a guest's request, written from each side",
     "conflict": "Large rooms that host others' art (the Green Lattice, PlaceNL, placehearts, the Italian flag) and the small rooms that ask them for room describe one exchange from two sides. Hosts' coders write it as ruling on admission ('ruling on what may be built inside', 'assigning orange space to displaced groups'); askers' coders as asking for room and help ('asking bigger neighbours for room and protection'). The scheme splits the host's ruling (T3-162), the request for space (T3-035), reliance on a bigger neighbour (T3-099), room granted (T3-012) and help asked (T3-084).",
     "terms": {"greenlattice/t11": "ruling on what may be built inside",
               "PlaceNL/t09": "assigning orange space to displaced groups",
               "placehearts/t10": "setting rules for which hearts stay and who maintains them",
               "greenlattice/t09": "building and protecting admitted art",
               "theitalyplace/t11": "answering outsiders asking for pixels or help",
               "gameboy/t06": "warning that green lattice covers unapproved art",
               "Jamaica/t06": "asking other communities for room and help",
               "malta/t03": "asking bigger neighbours for room and protection",
               "yumenikki/t03": "asking Sweden and its diplomacy channel for room",
               "hongkong/t05": "getting permission, protection and room beside others"},
     "pairs": ["T3-035|T3-162", "T3-010|T3-162", "T3-011|T3-162", "T3-012|T3-162", "T3-035|T3-084", "T3-035|T3-099"]},
    {"id": "CC-045", "practice": "putting right the damage the room did to a neighbour",
     "conflict": "Coders name apology, restitution and repair after the room damaged a neighbour as one practice of putting it right: 'repairing harm to neighbouring pictures', 'owning mistakes and trying to put them right', 'reckoning with art the flag displaced'. leagueoflegends t19's note keeps restitution apart 'because restitution, not building or attacking, is the practice'. The scheme splits the apology (T3-040), repair by those who attacked (T3-119), a quarrel closed (T3-047), restraint (T3-024) and friendly damage recognised (T3-170).",
     "terms": {"armenia/t11": "repairing harm to neighbouring pictures",
               "straya/t09": "owning mistakes and trying to put them right",
               "leagueoflegends/t19": "Offering to repair pictures the League mark displaced",
               "nVade/t06": "apologising for the Scotland mix-up and repairing the invaders",
               "liquicity/t06": "making peace after overlapping logos",
               "AmericanFlaginPlace/t08": "reckoning with art the flag displaced",
               "PlaceNL/t08": "sparing and rebuilding nearby artwork",
               "monsterhunter/t04": "working around neighbours and repairing art Rathalos displaced",
               "sonicthehedgehog/t10": "apologizing for Tails and disputing the blame"},
     "pairs": ["T3-040|T3-119", "T3-040|T3-047", "T3-024|T3-040", "T3-040|T3-170"]},
    {"id": "CC-046", "practice": "who was there first, written with the blame and its fairness",
     "conflict": "Disputes over who held a spot first are written together with the blame for the damage and the argument over its fairness: 'arguing over who crossed the border and who was responsible', 'arguing over who was there first and what changing pixels allows', 'claiming turf and taking over other flags'. The scheme splits first-arrival claims (T3-045), tracing who changed the work (T3-087), whether covering is fair (T3-046), borders (T3-010) and taking a neighbour's space (T3-061).",
     "terms": {"archlinux/t05": "arguing over who crossed the border and who was responsible",
               "liquicity/t07": "claiming and contesting canvas space",
               "romania/t19": "arguing over whose space is being griefed",
               "worldpowers/t04": "arguing over who was there first and what changing pixels allows",
               "seolhyun/t03": "arguing over wiping out and stealing the Jets logo",
               "utahjazz/t04": "working around neighbors while claiming a spot",
               "russia/t05": "claiming turf and taking over other flags"},
     "pairs": ["T3-045|T3-046", "T3-045|T3-087", "T3-010|T3-045", "T3-045|T3-061"]},
    {"id": "CC-047", "practice": "who speaks for the room, kept inside the deal",
     "conflict": "Several notes say no one voice speaks for the room: placetardis t06 ('no fixed leader versus diplomats'), seolhyun t05 ('there is no single settled community voice at first'), uoft t10 ('whether they can represent others'), nuclearthrone t04 ('who speaks for Ireland'). The coders keep the question of authority inside the negotiation. The scheme places an envoy's errand (T3-194), an organised room disowning rogue placers (T3-188) and members told to stop (T3-076) apart from the deal itself (T3-010, T3-149).",
     "terms": {"placetardis/t06": "negotiating multi-way arrangements",
               "uoft/t10": "negotiating borders, peace, and moves with neighbours",
               "maryland/t03": "negotiating room and permission with Sweden",
               "winnipegjets/t04": "working out who gets which canvas space",
               "seolhyun/t05": "working out how Korea can fit around the heart",
               "nuclearthrone/t04": "making room with Ireland",
               "uiuc/t14": "calling rogue placers and scripts back into line",
               "czech/t07": "making, doubting and repairing pacts with neighbours"},
     "pairs": ["T3-010|T3-194", "T3-010|T3-188", "T3-076|T3-188", "T3-149|T3-188"]},
]

RESIDUAL = re.compile(r"belongs with no other|single-code|single code|stands alone|singleton|belongs with nothing|no other practice|no other code|shares no|cannot safely join|lone trace|belongs with neither|belongs with no broader|remains its own|This single|isolated code|single placement account|single surviving title|single visitor report|single visitor request|single passage|Nothing else in the pool", re.I)


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
    rows.append({"id": "CC-048", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008, CC-016, CC-025 and CC-036: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme', 'stands alone'), often one visitor's request or a surviving title whose body was deleted, so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-006|T3-192", "T3-011|T3-084", "T3-035|T3-084"]})
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
