#!/usr/bin/env python3
"""B2a-r2: the author's placements of the ten biggest bags of notes-B1.md, appended to
out/author_items.jsonl before any round-2 packet exists (head: "their size is not a reason to drop them").

Rule 0 as amended (J, 2026-10-11): one placement; a bag (more than three themes needed) places one theme
and names every other under also_present, each with its own concepts. Lines carry support_by_theme.
The script checks each theme id against scheme.jsonl, each concept against the item's own concepts
(vlib.support_problems, vlib.also_present_problems), that no item is already in author_items.jsonl or
gold_items.jsonl, and takes rank and concept count from notes-B1.md's list. Dry run unless --write.
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

A, C = "arguable", "clear"

# item, primary, why, confidence, support, {also_present theme: (why, codes)}
P = [
 ("leagueoflegends/t02", "T3-023",
  "the moderators' Marc Merrill makeover of the room and members playing inside it: rededication and flairs, hailing, mock news and roleplay (c0085, c0086, c0129, c0138, c0140, c0146). Reactions to Riot's own jokes and objections to the makeover are present, but the takeover carries them",
  A, ["c0085", "c0086", "c0088", "c0129", "c0138", "c0140", "c0146"], {}),
 ("theblackvoid/t09", "T3-006",
  "calls to consume named targets: national flags, the trans ribbon, logos and pictures, with times and coordinates (c0040, c0150, c0152, c0200, c0203, c0234)",
  A, ["c0040", "c0150", "c0152", "c0171", "c0200", "c0203", "c0234"], {}),
 ("ainbowroad/t11", "T3-035",
  "outside rooms address Rainbow Road as host, asking permission or space to build on it (c0242, c0299, c0552, c0619). Pleas for help (T3-084) and pleas not to be run over (T3-139) are present, but the request to the host carries them",
  A, ["c0242", "c0299", "c0552", "c0619", "c0207"], {}),
 ("2007scape/t04", "T3-038",
  "building the room's marks from coordinates, reporting progress logs and declaring them done: Gnome Child, A q p W, Connection Lost, the Grand Exchange (c0042, c0044, c0056, c0488, c0522, c0554, c0586, c0653)",
  A, ["c0042", "c0044", "c0056", "c0488", "c0522", "c0554", "c0586", "c0653"],
  {"T3-005": ("calls to fight back against GreenLattice and to man the pixel stations (c0389, c1004, c1130, c1131)", ["c0389", "c1004", "c1130", "c1131"]),
   "T3-123": ("refusing to give up the top-left corner to Rainbow Road or Night's Edge (c0245, c0246, c0248, c0594, c0595)", ["c0245", "c0246", "c0248", "c0594", "c0595"]),
   "T3-010": ("borders settled with neighbours: white letters for Rainbow Road, the money-stack limit, the Forsen and goose areas (c0497, c0818, c1176, c1209)", ["c0497", "c0818", "c1176", "c1209"]),
   "T3-179": ("the r/The_Donald episode argued as Trump and anti-Trump politics (c0718, c0719, c0777, c0787)", ["c0718", "c0719", "c0777", "c0787"]),
   "T3-157": ("reflecting on what the community can do working together (c0392, c0939, c1191)", ["c0392", "c0939", "c1191"])}),
 ("theblackvoid/t12", "T3-174",
  "professing loyalty to the Void as a colour: hails, creeds, the oath, anthems, 'be the Void' (c0001, c0025, c0046, c0129, c0480, c0833, c0877, c1058, c1664)",
  A, ["c0001", "c0025", "c0046", "c0129", "c0480", "c0833", "c0877", "c1058", "c1664"],
  {"T3-006": ("calls to consume named targets: the EU flag, the trans flag, the American flag, the Square Spiral (c0439, c0485, c1026, c1061, c1350)", ["c0439", "c0485", "c1026", "c1061", "c1350"]),
   "T3-163": ("members leaving Blue for the Void (c0446, c1319, c1859)", ["c0446", "c1319", "c1859"]),
   "T3-190": ("splitting over doctrine: the One True Void and the pure Void (c0720, c0973, c1011, c1109, c1218)", ["c0720", "c0973", "c1011", "c1109", "c1218"]),
   "T3-005": ("defending the cores against attack (c0067, c0427, c1134, c1232)", ["c0067", "c0427", "c1134", "c1232"])}),
 ("ainbowroad/t04", "T3-021",
  "watching and repairing the road: colour order, the core, the portals, the pot of gold (c0013, c0028, c0250, c0565, c0980, c1111, c1235, c1523, c1734)",
  A, ["c0013", "c0028", "c0250", "c0565", "c0980", "c1111", "c1235", "c1523", "c1734"],
  {"T3-139": ("outside rooms pleading with the road not to run over their work (c0058, c0091, c0106, c0203, c0584, c0640, c1096)", ["c0058", "c0091", "c0106", "c0203", "c0584", "c0640", "c1096"]),
   "T3-024": ("members refusing to cover others' art: spare Helix, Snek is protected (c0012, c0120, c0291, c0458, c0837)", ["c0012", "c0120", "c0291", "c0458", "c0837"]),
   "T3-011": ("repairing other rooms' work: Nyan's eyes, Link, the trans flag, the Mona Lisa frame (c0044, c0186, c0189, c0414, c1118)", ["c0044", "c0186", "c0189", "c0414", "c1118"]),
   "T3-084": ("other rooms asking the road for help to defend and rebuild (c0381, c0403, c0630, c0683)", ["c0381", "c0403", "c0630", "c0683"])}),
 ("ainbowroad/t03", "T3-005",
  "alarms and calls to fight attackers, mostly the Void and Blue (c0116, c0184, c0192, c0599, c0645, c0788, c0792, c1148, c1709, c1746, c1988)",
  A, ["c0116", "c0184", "c0192", "c0599", "c0645", "c0788", "c0792", "c1148", "c1709", "c1746", "c1988"],
  {"T3-084": ("other rooms asking the road for help against the Void and Germany (c0521, c0632, c0764, c0923, c1044)", ["c0521", "c0632", "c0764", "c0923", "c1044"]),
   "T3-149": ("truces offered and argued with the Void (c0662, c0945, c1723, c1729, c1875)", ["c0662", "c0945", "c1723", "c1729", "c1875"]),
   "T3-050": ("taunts traded with American-flag builders (c1927, c1928, c1931)", ["c1927", "c1928", "c1931"]),
   "T3-124": ("weighing a fight against keeping out of it or maintaining instead (c0086, c0685, c0739, c1764)", ["c0086", "c0685", "c0739", "c1764"])}),
 ("dota2/t05", "T3-023",
  "the moderators' r/tz makeover and members playing inside it: the rename, the talent tree, the posting rule enforced and bent (c0197, c0198, c0232, c0233, c0258, c0400, c0686). Objections to the joke and asks to keep it are present, but the takeover carries them",
  A, ["c0197", "c0198", "c0232", "c0233", "c0258", "c0400", "c0686"], {}),
 ("ainbowroad/t07", "T3-041",
  "extending the road's strands and adding features to it: expansion calls, endings, the prism, Mario Kart (c0059, c0093, c0222, c0257, c0284, c0514, c1316, c1613)",
  A, ["c0059", "c0093", "c0222", "c0257", "c0284", "c0514", "c1316", "c1613"],
  {"T3-035": ("outside rooms asking the road for space to build (c0835, c1010, c1212, c1293, c1362, c1449, c1956)", ["c0835", "c1010", "c1212", "c1293", "c1362", "c1449", "c1956"]),
   "T3-160": ("the Gilbert Baker memorial road (c0194, c0197, c1796, c1797)", ["c0194", "c0197", "c1796", "c1797"]),
   "T3-033": ("proposing new marks for the road: the Dark Side of the Moon prism (c0176, c0198, c0240)", ["c0176", "c0198", "c0240"]),
   "T3-061": ("pushing the road over the American flag (c1841, c1891)", ["c1841", "c1891"])}),
 ("sweden/t01", "T3-065",
  "building, cleaning and correcting the Swedish flag (c0004, c0005, c0016, c0087, c0266, c0345, c0359, c0415, c0421, c0528, c0623)",
  A, ["c0004", "c0005", "c0016", "c0087", "c0266", "c0345", "c0359", "c0415", "c0421", "c0528", "c0623"],
  {"T3-035": ("outside rooms asking for space on the flag (c0457, c0458, c0569, c0605, c0614, c0632, c0661)", ["c0457", "c0458", "c0569", "c0605", "c0614", "c0632", "c0661"]),
   "T3-012": ("letting smaller art stay on the flag: Arch Linux, Maryland, others who asked (c0380, c0403, c0477)", ["c0380", "c0403", "c0477"]),
   "T3-061": ("pushing over the Danish flag and other neighbours (c0057, c0142, c0308, c0637, c0669)", ["c0057", "c0142", "c0308", "c0637", "c0669"]),
   "T3-113": ("national emblems on the flag: Knugen and the Dala horse (c0551, c0668, c0701)", ["c0551", "c0668", "c0701"]),
   "T3-151": ("bartering space for help: Maryland's night repairs, Baltic help, Madotsuki's repairs (c0351, c0494, c0588)", ["c0351", "c0494", "c0588"])}),
]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ids = {r["id"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
    themes = {(t["sub"], t["theme_id"]): t for t in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
    ct = {}
    for (sub, tid), t in themes.items():
        for c in t.get("code_ids") or []:
            ct[(sub, c)] = tid
    lab2id = {(t["sub"], t["second_order"]): t["theme_id"] for t in themes.values()}
    working = collections.defaultdict(set)
    for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
        for m in r["members"]:
            working[(m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))].add(r["theme"])
    rank = {}
    for line in open(os.path.join(OUT, "notes-B1.md"), encoding="utf-8"):
        m = re.match(r"(\d+)\. (\S+) (t\d+), (\d+) concepts,", line)
        if m and int(m.group(1)) <= 10 and (m.group(2), m.group(3)) not in rank:
            rank[(m.group(2), m.group(3))] = (int(m.group(1)), int(m.group(4)))
    have = {r["item"] for name in ("author_items.jsonl", "gold_items.jsonl") for r in jl(os.path.join(OUT, name))}
    rows, errs = [], []
    for item, prim, why, conf, support, ap in P:
        sub, tid = item.split("/")
        if item in have:
            errs.append("%s is already in author_items.jsonl or gold_items.jsonl" % item)
        if (sub, tid) not in rank:
            errs.append("%s is not on notes-B1.md's list of the ten biggest bags" % item)
        for t in [prim] + list(ap):
            if t not in ids:
                errs.append("%s: %s not in scheme.jsonl" % (item, t))
        sbt = {prim: support}
        errs += ["%s: %s" % (item, p) for p in vlib.support_problems(sbt, [prim], sub, tid, ct)]
        apc = {t: cs for t, (_, cs) in ap.items()}
        errs += ["%s: %s" % (item, p) for p in vlib.also_present_problems(apc, [prim], sub, tid, ct, ids)]
        bag = len(ap) + 1 > 3
        if ap and not bag:
            errs.append("%s names also_present but needs only %d themes; rule 0 places up to three" % (item, len(ap) + 1))
        w = sorted(working.get((sub, tid), []))
        r_, n_ = rank.get((sub, tid), (None, None))
        whyd = {prim: why}
        for t, (y, _) in ap.items():
            whyd[t] = y
        rows.append({"sub": sub, "theme_id": tid, "item": item, "third_order": [prim], "multi": False,
                     "why": whyd, "confidence": conf, "support": support, "support_by_theme": sbt,
                     "item_is_a_bag": bag, "also_present": apc,
                     "source": "biggest-bag", "drawn_as": "notes-B1.md biggest bag %s of 10, %s concepts" % (r_, n_),
                     "concepts": len(themes[(sub, tid)].get("code_ids") or []),
                     "working_B1": w, "differs_from_working": sorted({prim} ^ set(w)),
                     "placed_by": "author", "stage": "B2", "leg": "B2a-r2"})
    for r in rows:
        print("%-22s %s  bag=%s  also_present=%s  concepts=%d  working_B1=%s" % (
            r["item"], r["third_order"][0], r["item_is_a_bag"], ",".join(r["also_present"]) or "-",
            r["concepts"], ",".join(r["working_B1"])))
    if len(rows) != 10 or len(rank) != 10:
        errs.append("expected ten items and ten ranked bags, have %d and %d" % (len(rows), len(rank)))
    for e in errs:
        print("ERROR", e)
    if errs or "--write" not in sys.argv:
        return
    with open(os.path.join(OUT, "author_items.jsonl"), "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("appended %d lines to out/author_items.jsonl" % len(rows))


if __name__ == "__main__":
    main()
