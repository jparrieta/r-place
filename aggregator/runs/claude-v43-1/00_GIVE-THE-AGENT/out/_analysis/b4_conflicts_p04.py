#!/usr/bin/env python3
"""B4a-04: the conflicts pass (stage B4 section 4) over adjudication packet 4's theme notes alone
(out/_adjudication-B4/packet-04/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p03.py did for packet 3: two or more coders describing the same practice in
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
PACKET, LEG = 4, "B4a-04"

C = [
    {"id": "CC-026", "practice": "keeping the mark against damage, named defence or repair in either order",
     "conflict": "Coders in most rooms name keeping the mark against damage as one practice, 'defending and repairing' or 'repairing and defending', and the order of the words does not follow the readings: 'standing guard and repairing' heads argentina t04, whose readings both put T3-005 first, and romania t04, whose readings both put T3-021 first. The scheme splits the acts: T3-005 when an attack is fought, T3-021 when the work is watched and fixed, and T3-005's decide_when_both makes the side that leads primary. 37 of packet 4's themes have one reading on each.",
     "terms": {"argentina/t04": "standing guard and repairing the bandera",
               "romania/t04": "standing guard and repairing the flag",
               "de/t02": "defending and repairing the flag",
               "serbia/t08": "defending and repairing the flag pixel by pixel",
               "reddevils/t15": "defending and repairing the crest pixel by pixel",
               "palestine/t04": "defending, repairing and holding the flag",
               "pcmasterrace/t09": "repairing and defending the work",
               "harrypotter/t03": "repairing and defending the crest one pixel at a time",
               "nbaspurs/t14": "repairing and defending the Spur",
               "2007scape/t08": "Repairing and defending the work click by click",
               "OnePiece/t02": "repairing and guarding the art one pixel at a time"},
     "pairs": ["T3-005|T3-021", "T3-005|T3-087", "T3-021|T3-073"]},
    {"id": "CC-027", "practice": "putting upkeep before growth, folded into the repair practice",
     "conflict": "Packet 3's coders gave the choice of holding over growing a theme of its own (criticalrole t09, eagles t07, PlaceNL t05, all read as T3-042). Packet 4's coders fold the same choice into the practice of keeping the mark: 'prefer protection over further expansion', 'returning from expansion to maintenance', 'choose maintenance over expansion'. The scheme sets it apart: T3-042 takes 'Upkeep chosen over growth', and T3-021's discriminator asks whether the work is repaired or 'upkeep argued as the room's priority over growth (T3-042)'.",
     "terms": {"frankocean/t10": "prefer protection over further expansion",
               "austria/t05": "returning from expansion to maintenance",
               "2007scape/t08": "decisions to defer expansion because existing pieces need constant upkeep",
               "smashbros/t06": "switch from expansion to keeping existing work intact",
               "gameofthrones/t14": "choose maintenance over expansion",
               "schoolidolfestival/t08": "turn from expansion to keeping shared work intact",
               "madokamagica/t02": "limiting expansion",
               "kingdomhearts/t20": "stop expanding",
               "fireemblem/t03": "refuse expansion",
               "soylent/t03": "choosing vandals over expansion",
               "hentai/t03": "rejecting expansion",
               "rwby/t08": "keep placing and defending without overextending"},
     "pairs": ["T3-021|T3-042", "T3-005|T3-042", "T3-042|T3-069"]},
    {"id": "CC-028", "practice": "a script that keeps the mark, filed as repair or as a script practice",
     "conflict": "A script or bot that repairs or guards the mark is one tool among the repairs in some notes ('a repair script', 'keep repair tools running', 'handing the watch to people and bots') and the heading of the practice in others ('automating overnight flag maintenance', 'running borrowed code to protect the box'). The scheme gives the script to T3-028 (T3-021's discriminator: 'Is it kept by hand (T3-021), or by a script (T3-028)?'), and scripts left running overnight to T3-141.",
     "terms": {"dragonquest/t02": "a repair script",
               "terraria/t02": "distributing and updating scripts",
               "ScottPilgrim/t03": "automate anti-griefing",
               "runescape/t14": "keep repair tools running",
               "mylittlepony/t05": "handing the watch to people and bots",
               "theitalyplace/t01": "through a script",
               "taiwan/t05": "proposing a counter-script",
               "spacexmasterrace/t05": "maintaining and repairing the drawing with pixels and scripts",
               "colombia/t06": "automating overnight flag maintenance",
               "livecounting/t07": "running borrowed code to protect the box",
               "heyyea/t02": "automagically maintaining the heroes",
               "wallstreetbets/t11": "running and repairing scripts to defend fuckboy",
               "rutgers/t15": "automating defense while keeping art human"},
     "pairs": ["T3-021|T3-028", "T3-005|T3-028", "T3-028|T3-141"]},
    {"id": "CC-029", "practice": "running scripts and arguing whether they are fair, as one practice",
     "conflict": "Coders put running scripts and arguing whether scripts are fair in one practice and name it by one side: 'Running and disputing scripts', 'automating and disputing pixel work', 'using scripts while arguing about fairness and creativity', 'arguing over scripts and where they paint'. The scheme splits the sides: T3-028 for scripts run, T3-027 for their fairness argued, with T3-027's decide_when_both making T3-028 primary when the scripts are run and adding T3-027 when the argument has concepts of its own.",
     "terms": {"dota2/t07": "Running and disputing scripts for shared art",
               "monero/t05": "disputing whether scripts are cheating",
               "rpi/t06": "challenging whether botting ruins the event",
               "minnesotavikings/t09": "running, correcting, and arguing over placement scripts",
               "sbu/t02": "arguing over whether scripts are acceptable",
               "italy/t07": "automating and disputing pixel work",
               "texans/t14": "automating protection while questioning and fixing scripts",
               "giantbomb/t07": "taking sides on using scripts and bots",
               "placecanada/t12": "using scripts while arguing about fairness and creativity",
               "TransFlagPlace/t09": "arguing about bots, alts, fair play, and authority",
               "pakistan/t08": "arguing over scripts and where they paint"},
     "pairs": ["T3-027|T3-028", "T3-028|T3-088", "T3-027|T3-087"]},
    {"id": "CC-030", "practice": "sorting attacks from mistakes and friends from attackers",
     "conflict": "Working out whether a changed pixel is an attack, a misclick, a friend's fix or a rogue's act is filed as tracing the attacker ('sorting suspected attacks from mistakes', 'checking who actually changed the pixels'), as friendly fire owned ('sorting mistaken fixes from attacks', 'correcting friendly pixels mistaken for attacks'), and as an organised room disowning rogues ('separating allies from randos and repairing blame'). The scheme splits by what the sorting finds: T3-087's discriminator asks whether 'the culprit [is] sought (T3-087), or found to be a friend or one's own mistake (T3-170)', and T3-188 takes an organised room setting its plan apart from placers it does not control.",
     "terms": {"nyjets/t09": "sorting suspected attacks from mistakes",
               "smite/t07": "sorting attacks, jokes, and mistakes from one another",
               "theitalyplace/t08": "checking who actually changed the pixels",
               "TransFlagPlace/t04": "calling out false flags and sorting out who attacked",
               "monstercat/t08": "checking whether bad pixels came from traitors or display glitches",
               "japan/t13": "sorting mistaken fixes from attacks",
               "norge/t11": "correcting mistaken attacks and fixes",
               "formula1/t15": "correcting friendly pixels mistaken for attacks",
               "SquareSpiral/t11": "separating allies from randos and repairing blame",
               "costa_rica/t07": "sorting out GreenLattice friends, rogues and the hive mind"},
     "pairs": ["T3-087|T3-170", "T3-087|T3-188", "T3-170|T3-188"]},
    {"id": "CC-031", "practice": "the fight named for defence and attack at once",
     "conflict": "Coders name the room's fighting as one practice that holds defending its own work, counterattacks, raids and taking ground: 'Rallying attacks and mounting defence', 'calling the greytide to invade and defend', 'calling fleets to defend, restore, or attack', 'defending green and taking ground from other colours'. The scheme splits by the target: T3-005 for the room's own work defended, T3-006 for another's work attacked, T3-061 for space taken. Declining to strike back is T3-007, and one coder made it a theme (pakistan t17).",
     "terms": {"sweden/t02": "Rallying attacks and mounting defence",
               "ss13/t04": "calling the greytide to invade and defend",
               "eve/t07": "calling fleets to defend, restore, or attack",
               "TheGreatGreenBox/t02": "defending green and taking ground from other colours",
               "AyyMD/t04": "naming attackers and rallying a fight back",
               "stevenuniverse/t06": "war declarations, revenge talk, counterattacks",
               "donaldglover/t07": "fighting canvas obstacles and attackers",
               "2007scape/t06": "Fighting, bargaining, and helping across canvas borders",
               "anarchism/t02": "fighting over flags with ancraps, fash, and /pol/",
               "pakistan/t17": "rejecting retaliation and calling for another flag"},
     "pairs": ["T3-005|T3-006", "T3-005|T3-061", "T3-006|T3-007"]},
    {"id": "CC-032", "practice": "shifts and night watches over the mark",
     "conflict": "Shifts, night watches and hand-offs across time zones head some notes ('holding down the fort across shifts', 'keeping it alive against griefers across shifts', 'standing Nachtwache') and are one detail among the repairs in others ('organized shifts', 'night shifts', 'handoffs across time zones'). T3-141 takes watch kept over the hours most members sleep and work handed to other time zones; T3-021's decide_when_both makes repair primary and adds T3-141 only when the hours and shifts have concepts of their own. No packet 4 theme has a reading that puts T3-141 first.",
     "terms": {"aceattorney/t08": "holding down the fort across shifts",
               "wildhockey/t07": "keeping it alive against griefers across shifts",
               "placeDE/t03": "cleaning the flag and standing Nachtwache",
               "jerma985/t04": "taking shifts to protect and repair the pictures",
               "bostonbruins/t06": "organized shifts",
               "newzealand/t06": "night shifts",
               "taiwan/t05": "handoffs across time zones",
               "ssbpm/t15": "hand off watch",
               "bih/t02": "keeping watch and repairing around work and sleep"},
     "pairs": ["T3-021|T3-141", "T3-005|T3-141"]},
    {"id": "CC-033", "practice": "moving the work, whatever the cause",
     "conflict": "Moving the work is written as one practice whatever made the room move: a loss ('rebuilding or redirecting after a loss'), a neighbour asking ('hearing the other side ask them to move'), permission sought from a host ('seeking permission'), a negotiation ('negotiating a new place after the old spot is gone'), or a choice of better ground ('relocating the R around occupied space'). The scheme splits by the cause: T3-022 after a loss, T3-039 when a neighbour asked, T3-020 for the first choice of a spot, T3-035 for space asked of a host. Several notes do not say the cause.",
     "terms": {"rush/t04": "hearing the other side ask them to move",
               "berkeley/t04": "seeking permission",
               "Dominican/t08": "negotiating a new place after the old spot is gone",
               "rutgers/t04": "relocating the R around occupied space",
               "mordhau/t04": "moving the whole logo up",
               "turkey/t02": "choosing and changing coordinates when flags are lost or crowded",
               "ghibli/t03": "switching pictures and moving to another spot",
               "undertale/t06": "rebuilding or redirecting after a loss"},
     "pairs": ["T3-020|T3-022", "T3-022|T3-039", "T3-022|T3-035"]},
    {"id": "CC-034", "practice": "the end of the event: loss, blame and memory together",
     "conflict": "After the close, coders file grief, blame and the story of what happened as one practice: 'mourning the loss and arguing who ruined it', 'mourning and arguing over how it ended', 'arguing over and remembering Place after it ended', 'settling what Quebec did after the finish'. The scheme splits them: T3-029 for grief, T3-058 for blame laid on a named room after the close, T3-073 for the account of how the work fared, T3-087 for tracing during placement, T3-188 for a room disowning its rogues. T3-058's decide_when_both makes the loss or the blame primary by which leads.",
     "terms": {"frc/t09": "mourning the loss and arguing who ruined it",
               "mexico/t15": "mourning and arguing over how it ended",
               "homestuck/t19": "arguing over and remembering Place after it ended",
               "kilian/t10": "settling what Quebec did after the finish",
               "albania/t14": "settling whether we attacked the Serbian flag",
               "corridor/t11": "saying the ending saved the logo while others tried to ruin art",
               "newzealand/t13": "recounting who damaged what and why"},
     "pairs": ["T3-058|T3-073", "T3-029|T3-058", "T3-058|T3-087", "T3-058|T3-188"]},
    {"id": "CC-035", "practice": "a large neighbouring project that takes art into itself (the taskbar)",
     "conflict": "The r/placestart taskbar's approach is written as an attack to resist ('resisting the taskbar takeover'), as something to meet 'with resistance or a shared window', as a new home to move into ('moving her into the taskbar'), and as labour owed to it ('the labour promised to r/placestart'). The scheme has T3-005 for defence, T3-022 for moving after a loss, T3-071 for the room's work adopted into a neighbour's with consent, T3-068 for art converted by force and T3-137 for joining another group's build. The notes do not say which of these the rooms took the taskbar to be.",
     "terms": {"rocketbeans/t07": "resisting the taskbar takeover",
               "darksouls/t09": "meeting the Taskbar with resistance or a shared window",
               "hatsune/t04": "making Miku smaller and moving her into the taskbar",
               "clubpenguin/t09": "the labour promised to r/placestart",
               "placestart/t14": "defending and repairing the taskbar and incorporated art"},
     "pairs": ["T3-005|T3-071", "T3-022|T3-137", "T3-005|T3-068"]},
]
RESIDUAL = re.compile(r"belongs with no other|single-code|single code|stands alone|singleton|belongs with nothing|no other practice|no other code|shares no|cannot safely join|lone trace|belongs with neither|belongs with no broader|remains its own|This single|isolated code|single placement account|single surviving title|single visitor report|single passage", re.I)


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
    rows.append({"id": "CC-036", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008, CC-016 and CC-025: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme', 'stands alone'), often a surviving title whose body was deleted, so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-005|T3-087", "T3-087|T3-170", "T3-006|T3-192"]})
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
