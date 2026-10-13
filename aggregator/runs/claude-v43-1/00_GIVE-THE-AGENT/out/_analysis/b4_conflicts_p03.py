#!/usr/bin/env python3
"""B4a-03: the conflicts pass (stage B4 section 4) over adjudication packet 3's theme notes alone
(out/_adjudication-B4/packet-03/notes.md), read before the packet's first ruling. Appends one line per conflict to
out/coder_conflicts.jsonl, as b4_conflicts_p02.py did for packet 2: two or more coders describing the same practice in
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
PACKET, LEG = 3, "B4a-03"

C = [
    {"id": "CC-017", "practice": "making the mark and keeping it, named as one building practice",
     "conflict": "Most coders name the mark's whole life, first placing, repair, upkeep and defence, as one 'building' practice; one coder says outright that only the first build was kept and the repair codes were filed apart (asexuality t01). The scheme splits these acts between T3-038 (the first build and its progress), T3-021 (repair and upkeep) and T3-005 (defence).",
     "terms": {"achievement_hunter/t03": "building, maintaining, and remaking AH marks",
               "adventuretime/t04": "building, rebuilding, and keeping the figures alive",
               "brasil/t04": "building, repairing, and maintaining the shared work",
               "catholicism/t05": "Placing, repairing, and defending Catholic marks",
               "faeria/t01": "building, repairing, and rebuilding the Yak together",
               "frc/t04": "building, repairing, and keeping the logo up",
               "denverbroncos/t11": "building, repairing and defending the drawings",
               "skyrim/t03": "building, repairing, and maintaining the mark",
               "asexuality/t01": "kept here only passages about initiating or joining the build, not the later work of keeping it readable"},
     "pairs": ["T3-021|T3-038", "T3-005|T3-038", "T3-038|T3-073"]},
    {"id": "CC-018", "practice": "choosing what to draw and where, in one phrase",
     "conflict": "The same phrase, 'what and where to draw', heads themes whose readings' primaries fall on T3-033 (the proposal), T3-004 (the design) and T3-020 (the spot). The note names three acts the scheme splits and does not say which leads.",
     "terms": {"brasil/t02": "choosing what and where to draw",
               "denverbroncos/t07": "working out what and where to draw",
               "HomestarRunner/t01": "working out what and where to draw",
               "radiohead/t01": "choosing what and where to draw",
               "skyrim/t02": "working out what to draw and where to put it",
               "nightinthewoods/t02": "working out what and where to build",
               "pathofexile/t02": "choosing what and where to draw",
               "KState/t01": "proposing what and where to draw",
               "sadboys/t02": "proposing what and where to draw",
               "sabres/t03": "working out what and where to build",
               "truestl/t02": "working out what and where to draw"},
     "pairs": ["T3-004|T3-020", "T3-004|T3-033", "T3-020|T3-033"]},
    {"id": "CC-019", "practice": "proposing a further piece in the words used for the room's first mark",
     "conflict": "Coders write a proposal of the room's first mark and a proposal of a further piece beside a standing mark in the same words ('proposing what ... should put on the canvas', 'proposing the next ... picture'); only some notes say a mark already stands. T3-041's must_not_show sends the first mark to T3-033, and T3-033's test does not say 'first' (packet 2's reading).",
     "terms": {"2007scape/t03": "Proposing what RuneScape should put on the canvas",
               "suomi/t02": "proposing what to draw together",
               "portal/t02": "proposing the next Portal picture",
               "eagles/t02": "choosing where and what to draw next",
               "gameofthrones/t02": "proposing more pictures and words for the canvas",
               "denmark/t10": "building Kaj, Andrea, ships, and other shared pictures",
               "touhou/t08": "asking what to build or do next",
               "empiredidnothingwrong/t11": "proposing other r/place texts, monuments, and Death Stars",
               "southafrica/t09": "proposing words and pictures beyond the flag"},
     "pairs": ["T3-033|T3-041", "T3-004|T3-041", "T3-033|T3-038"]},
    {"id": "CC-020", "practice": "fitting the design to the hands and space available",
     "conflict": "As CC-013 for packet 2: a design cut down to the hands and space present is written as design work in most rooms, as fitting the hands, as cutting to what can survive, and as reworking against neighbours. Four themes' tests name the act: T3-074's 'designs scaled to the hands at hand', T3-069's 'a design scaled down to fit the hands', T3-042's 'designs scaled to what can be defended', and T3-055's reshaping against tampering.",
     "terms": {"aceattorney/t04": "choosing a picture the group can actually make",
               "corridor/t05": "shrinking the design and building it together",
               "penguins/t03": "shrinking and choosing a Pens image people could finish",
               "seahawks/t07": "settling on a small, defensible design and place",
               "esperanto/t03": "scaling flags and lettering to the people and space available",
               "latin/t03": "fitting the design to the space and hands available",
               "day9/t04": "cutting the design down to what can survive",
               "kingdomhearts/t12": "shrinking and relocating until a design fits",
               "NieR/t08": "reworking Emil to fit the canvas and stop friendly fire",
               "mizzou/t03": "working out a border the group can maintain"},
     "pairs": ["T3-004|T3-069", "T3-004|T3-074", "T3-042|T3-069", "T3-004|T3-055", "T3-004|T3-042"]},
    {"id": "CC-021", "practice": "telling people where the mark is",
     "conflict": "Answering 'where is it?' is written as showing the work, as finding it, and as giving its coordinates. The readings' primaries fall on T3-026, T3-082, T3-070 and T3-038. T3-070's discriminator against T3-038 says a link that only shows where finished work is points to it (T3-026); T3-082 needs members who did not know the mark was there.",
     "terms": {"corridor/t09": "telling latecomers where the logo ended up",
               "furry_irl/t18": "helping people find the finished drawing",
               "gamindustri/t13": "showing people where the finished logos are",
               "haskell/t14": "locating and recognising the finished r/place spot",
               "ethoslab/t05": "finding and showing where the face is",
               "re_zero/t06": "helping people find the Re:Zero drawing",
               "baylor/t05": "helping someone find the tiny BU",
               "riskofrain/t01": "sharing where the Commando is",
               "vietnam/t04": "showing where Viet Nam is on the canvas",
               "funhaus/t07": "sharing where the work is and how it changes"},
     "pairs": ["T3-026|T3-082", "T3-026|T3-070", "T3-026|T3-038"]},
    {"id": "CC-022", "practice": "the sub's name written on the canvas",
     "conflict": "Writing the sub's name is filed as lettering design, as an addition beside the mark, as a sign that directs visitors ('directs lost cubers to the subreddit'), as building a sign, and as a plan dropped. T3-169 takes the name written and the choice whether to write it; T3-044 takes it when bringing visitors in is the stated point; T3-191 takes the name left off on purpose.",
     "terms": {"drawhelix/t05": "settling the lettering and whether to add r/drawhelix",
               "neopets/t14": "fitting and refitting the NEOPETS letters",
               "wine/t08": "fitting and keeping the r/wine name tag inside its space",
               "cubers/t12": "adding and defending the r/cubers tag",
               "greenlattice/t06": "building the r/GreenLattice sign",
               "parrots/t10": "trying and then dropping writing r/parrots",
               "partyparrot/t03": "deciding what to put beside or after the parrot",
               "neu/t02": "trying to expand or label the N after stabilizing it",
               "ss13/t03": "spreading GREYTIDE pixels and the r/ss13 name"},
     "pairs": ["T3-004|T3-169", "T3-041|T3-169", "T3-044|T3-169", "T3-169|T3-191"]},
    {"id": "CC-023", "practice": "political and religious content argued for a national mark",
     "conflict": "Proposals to put political or religious content on a national mark are written as design argument in most rooms: 'arguing what should go on our flag' for Bhagwa, Aryavarta, Akhand Bharat and a Mandir (bakchodi t05), INDIA against national and religious symbols (india t07), a political sign on the German flag (placeDE t10), the Savoy crest on the Italian flag (theitalyplace t10). One coder writes the same act as a political inscription (an anti-Brexit message, unitedkingdom t11); HAYIR on the Turkish flag and the Malvinas on the Argentine one sit between. The scheme reads national politics in T3-130 and national emblems in T3-113, beside T3-004's design.",
     "terms": {"bakchodi/t05": "arguing what should go on our flag",
               "india/t07": "arguing over what the flag should represent",
               "placeDE/t10": "arguing over what belongs on the German flag",
               "theitalyplace/t10": "arguing over what should stay on the flag",
               "unitedkingdom/t11": "Putting anti-Brexit messages on the canvas",
               "turkey/t08": "proposing words, ornaments, and other marks beyond the standard flag",
               "argentina/t07": "putting Argentine names, symbols and jokes on the canvas"},
     "pairs": ["T3-004|T3-130", "T3-004|T3-113", "T3-033|T3-130", "T3-041|T3-130"]},
    {"id": "CC-024", "practice": "arguing whether to grow the mark or hold it",
     "conflict": "The argument over growing the mark is named by one side: expanding (T3-041), holding back (T3-042), or taking more space, sometimes a neighbour's (T3-061). The notes name a debate whose two sides the scheme puts in different themes, so the heading tells a reader which side the coder heard first.",
     "terms": {"argentina/t05": "arguing over expanding or holding ground",
               "criticalrole/t09": "choosing between adding more and defending what they had",
               "hongkong/t08": "expanding, then aborting when people and room run out",
               "placestart/t10": "pressing the taskbar onward and claiming room",
               "parahumans/t15": "calling for taking more canvas space",
               "eagles/t07": "holding back expansion to keep the words and neighbors safe",
               "popheads/t14": "keeping the sax first when other canvas ideas appear",
               "apocalypserising/t04": "arguing over room for the logo and flags"},
     "pairs": ["T3-041|T3-042", "T3-041|T3-061", "T3-042|T3-069"]},
]
RESIDUAL = re.compile(r"belongs with no other|single-code|single code|stands alone|singleton|belongs with nothing|no other practice|no other code|shares no|cannot safely join|lone trace", re.I)


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
    rows.append({"id": "CC-025", "packet": PACKET, "leg": LEG, "pass": "theme_note alone",
                 "practice": "a second-order theme whose note says it holds no shared practice",
                 "conflict": "As CC-008 and CC-016: the coder groups a code by exclusion ('belongs with no other practice', 'single-code theme', 'singleton'), often a surviving title whose body was deleted, so the note gives the scheme nothing to place.",
                 "items": sorted(set(resid)), "subs": sorted({k.split("/")[0] for k in resid}), "terms": {},
                 "pairs_it_may_explain": ["T3-026|T3-033", "T3-026|T3-038", "T3-033|T3-041"]})
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
