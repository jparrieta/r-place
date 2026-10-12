#!/usr/bin/env python3
"""B2b-r2-p2: place the children of the split bags (QB2-010) like any item, after the blind window closed.

Each child (out/recut/themes.jsonl) is found by its room and label. One third-order theme where one carries
it; a second only where it has concepts of its own (listed under `second`), never more than three; the
first theme's concepts are the rest. Lines go to author_items.jsonl (children of hard-set bags) or
gold_items.jsonl (children of gold-set bags), with parent, source "split", support_by_theme, item_is_a_bag
false and also_present {}. The parents' lines stay as written. Checks theme ids against scheme.jsonl and
concepts against the child's own (vlib.support_problems). Dry run unless --write.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

A, C = "arguable", "clear"
# (sub, label): (first theme, why, confidence, {second theme: ([codes], why)})
P = {
 ("2007scape", "Proposing what the room should make"): ("T3-033", "ideas for the room's marks offered and argued: Gnome Child, A q p W, the Grand Exchange, Buying gf", C, {}),
 ("2007scape", "Arguing a design's spot, size and look"): ("T3-004", "the marks' size, scale, colours and outline argued and corrected against the plan", A,
     {"T3-020": (["c0024", "c0253", "c0254", "c0476"], "where the mark goes: somewhere not taken, 406,578 against 0,0, too big for its spot")}),
 ("2007scape", "Building the marks and reporting progress"): ("T3-038", "the marks placed, started on time, logged in progress posts and announced complete", C, {}),
 ("2007scape", "Giving coordinates and references"): ("T3-070", "coordinates, canvas links, reference images and a pixel guide given to placers", C, {}),
 ("2007scape", "Fixing misplaced pixels and finding who misplaces them"): ("T3-021", "wrong pixels, stray dots and letters fixed, fixers asked not to undo each other", A,
     {"T3-087": (["c0387", "c0602", "c1007", "c1008"], "tracing who misplaces: clicking tiles to find trolls, the white_cat22 account, a list of traitors")}),
 ("2007scape", "Defending the corner against attackers"): ("T3-005", "alarms and calls to man the pixels and fight back against attackers", C, {}),
 ("2007scape", "Covering other rooms' art for the room's own"): ("T3-061", "neighbours' art in the way cleared or covered for the room's own marks, with talk of conquest", A, {}),
 ("2007scape", "Refusing to give the top-left corner to others"): ("T3-123", "the top-left corner refused to Rainbow Road and Night's Edge", C, {}),
 ("2007scape", "Dealing with neighbouring rooms"): ("T3-010", "deals and limits with neighbours: white letters for Rainbow Road, the money-stack limit, the forsen and goose areas", A,
     {"T3-024": (["c0587", "c0619", "c0673", "c0912"], "the room's own restraint toward others' art: working around it, not stomping pieces, sparing the Mona Lisa")}),
 ("2007scape", "Arguing Trump politics with r/The_Donald"): ("T3-179", "Trump, liberals and brigading argued when r/The_Donald plans a sign over the work", A, {}),
 ("2007scape", "Taking pride in what the room did together"): ("T3-157", "what the community can do together, its persistence and organisation reflected on", A,
     {"T3-009": (["c0510", "c0511", "c0670", "c0722"], "the finished work celebrated: we did it, look at this beauty")}),
 ("2007scape", "Objecting to the flood of r/place posts"): ("T3-075", "too many r/place posts objected to, one thread or a filter asked for", C, {}),
 ("2007scape", "Joking, asking and remarking about the canvas"): ("T3-031", "the room's memes and jokes played about the canvas, with questions and asides", A, {}),
 ("2007scape", "Pushing the posts up for visibility"): ("T3-051", "upvotes and comments to lift the build threads", C, {}),
 ("sweden", "Building, cleaning and holding the Swedish flag"): ("T3-065", "the Swedish flag started, called for, corrected, cleaned and held", C, {}),
 ("sweden", "Defending the flag and calling out those who damage it"): ("T3-005", "alarms when the flag is attacked and calls to defend it", A,
     {"T3-087": (["c0050", "c0252", "c0643", "c0645"], "who damages it named: r/DANMAG, a traitor with a red dot, a classmate putting red dots on the king")}),
 ("sweden", "Taking over the Danish flag and other neighbours"): ("T3-068", "the Danish flag converted into a Swedish one and neighbours' flags covered", A, {}),
 ("sweden", "Adding Swedish emblems to the flag"): ("T3-113", "the king, the Dala horse, Pippi and other Swedish emblems drawn on the flag", C, {}),
 ("sweden", "Other rooms asking for space on or beside the flag"): ("T3-035", "other rooms ask the room holding the flag for space or to be spared", C, {}),
 ("sweden", "Other rooms asking Sweden for help"): ("T3-084", "other rooms ask Sweden, as a group, for help with their flags and logos", C, {}),
 ("sweden", "Settling with neighbours and letting their art stay"): ("T3-012", "neighbours let onto the flag: Arch Linux, Maryland and others who asked", A,
     {"T3-010": (["c0107", "c0157", "c0160", "c0167"], "lines and pacts settled with SilphRoad and Norway")}),
 ("sweden", "Nordic friendship and joint Nordic marks"): ("T3-056", "a joint Nordic picture and Viking ship made with Denmark and Norway", A, {}),
 ("sweden", "Looking back on the canvas and the Maryland friendship"): ("T3-158", "the Maryland friendship carried beyond the canvas in flairs and messages", A,
     {"T3-105": (["c0765", "c0767", "c0788", "c0790", "c0808"], "the final image saved, cleaned, shown in Minecraft and proposed as the banner")}),
 ("sweden", "Off-topic talk and jokes in the threads"): ("T3-017", "the sub's ordinary talk and jokes going on beside the canvas", A, {}),
 ("theblackvoid", "Hailing the Void and professing its creed"): ("T3-174", "hails, creeds, oaths and anthems professing loyalty to the Void", C, {}),
 ("theblackvoid", "Calling the Void to consume named targets"): ("T3-006", "named flags, logos and pictures called to be consumed", C, {}),
 ("theblackvoid", "Keeping and defending the Void's cores"): ("T3-005", "the cores defended against attack", A,
     {"T3-069": (["c0597", "c0675", "c0683", "c0998", "c1092"], "effort kept on the main core rather than spread to new ones")}),
 ("theblackvoid", "Arguing over what the true Void is"): ("T3-190", "the faction split over doctrine: the pure Void, the One True Void", C, {}),
 ("theblackvoid", "Leaving other colours to join the Void"): ("T3-163", "members defect from Blue and other colours to the Void", C, {}),
 ("theblackvoid", "Other rooms dealing with the Void"): ("T3-150", "other rooms offer or seek alliance with the Void, or say they are used by it", A, {}),
 ("theblackvoid", "Critics and taunts against the Void"): ("T3-046", "whether covering others' work is fair argued with critics", A,
     {"T3-050": (["c0852", "c0855", "c0937", "c1007", "c1038"], "insults traded with the Void's critics")}),
 ("theblackvoid", "Looking back on the Void after its end"): ("T3-073", "what became of the Void told after its end", A, {}),
 ("theblackvoid", "Jokes and asides about the Void"): ("T3-031", "the room's jokes and asides about the Void", A, {}),
 ("theblackvoid", "Calling for new cores elsewhere"): ("T3-020", "new places chosen to start cores", A, {}),
 ("ainbowroad", "Raising alarms and fighting the Void's attacks on the road"): ("T3-005", "alarms and calls to fight the Void's attacks on the road and its core", C, {}),
 ("ainbowroad", "Raising alarms about other attacks and collisions"): ("T3-005", "alarms about attacks, breaches and collisions, and calls to positions", C, {}),
 ("ainbowroad", "Calling the road to attack other rooms' work"): ("T3-006", "calls to step on, destroy or cut back other rooms' work", C, {}),
 ("ainbowroad", "War and peace with Blue and other rooms"): ("T3-149", "war argued and truces sought with Blue and other rooms", A,
     {"T3-124": (["c0086", "c0685", "c0739", "c0842"], "whether to fight at all weighed against staying out")}),
 ("ainbowroad", "Dealing with the Void: offers, truces and defectors"): ("T3-149", "the Void's offers of peace, compromise and alliance, accepted or rejected", A,
     {"T3-163": (["c0717", "c0984", "c1019", "c1077", "c1081"], "Void members defecting to the road")}),
 ("ainbowroad", "Other rooms asking the road for help or to be spared"): ("T3-084", "other rooms ask the road, as a group, for help against attackers", A,
     {"T3-139": (["c0921", "c0922", "c1213", "c1234", "c1352"], "other rooms plead with the road to stop attacking or avoid them")}),
 ("ainbowroad", "Routing the road around art and proposing designs"): ("T3-024", "the road routed around others' art by prisms, portals and frames", A,
     {"T3-033": (["c0546", "c1210", "c1250", "c1440", "c1950"], "designs proposed for the road")}),
 ("ainbowroad", "Hostility and insults against the road"): ("T3-050", "curses, threats and hate thrown at the road", A, {}),
 ("ainbowroad", "Repairing the road itself"): ("T3-021", "the road's colours, portals, sign and core watched and repaired", C, {}),
 ("ainbowroad", "Repairing and protecting other rooms' art on the road"): ("T3-011", "other rooms' art on the road repaired and guarded", C, {}),
 ("ainbowroad", "Deciding to spare and share space with neighbours"): ("T3-024", "the room chooses to spare neighbours' art and limit expansion", A,
     {"T3-010": (["c0286", "c0338", "c0390", "c0497", "c1277"], "agreed sizes, treaties and terms for sharing space")}),
 ("ainbowroad", "Other rooms asking the road to spare or help them"): ("T3-139", "other rooms plead with the road not to run over their work", A,
     {"T3-084": (["c0381", "c1872", "c0628", "c0630", "c0683", "c1025"], "other rooms ask the road's help to defend and restore their work")}),
 ("ainbowroad", "Defending the road against attackers"): ("T3-005", "defenders called against attackers on the road", C, {}),
 ("ainbowroad", "Looking back on the road's upkeep"): ("T3-157", "the work of the road reflected on after the close", A, {}),
 ("ainbowroad", "Extending the road and planning its course"): ("T3-041", "the road's strands extended and its course and ending planned", C, {}),
 ("ainbowroad", "Proposing pictures and features for the road"): ("T3-033", "pictures and features proposed for the road", A, {}),
 ("ainbowroad", "Other rooms asking for space on the road"): ("T3-035", "other rooms ask the road for space to build on it", C, {}),
 ("ainbowroad", "Working beside neighbours without harming their art"): ("T3-024", "the road's builders keep off neighbours' art by choice", A, {}),
 ("ainbowroad", "Making the road a memorial to Gilbert Baker"): ("T3-160", "the road recast as a memorial to Gilbert Baker", C, {}),
 ("ainbowroad", "Shards, takeovers and disputes over the road's spread"): ("T3-188", "rogue shards and unplanned forks disowned and cut", A,
     {"T3-061": (["c1841", "c1844", "c1891", "c1406"], "the road pushed over the American flag")}),
 ("dankmemes", "Pointing out drawings on the canvas"): ("T3-052", "drawings on the canvas pointed out and remarked on", A, {}),
 ("dankmemes", "Reporting the build failed and mourning the canvas"): ("T3-029", "the lost work and the closed canvas mourned", A, {}),
}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ids = {r["id"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
    ft = {(r["sub"], r["id"]): r["fleet"] for r in jl(os.path.join(OUT, "fleet_ids.jsonl")) if r["kind"] == "t"}
    kids = jl(os.path.join(OUT, "recut", "themes.jsonl"))
    ct = {}
    for k in kids:
        for c in k["code_ids"]:
            ct[(k["sub"], c)] = k["theme_id"]
    have = {r["item"] for n in ("author_items.jsonl", "gold_items.jsonl") for r in jl(os.path.join(OUT, n))}
    gold_parents = {r["item"] for r in jl(os.path.join(OUT, "gold_items.jsonl"))}
    rows, errs, used = {"author": [], "gold": []}, [], set()
    for k in kids:
        key = (k["sub"], k["second_order"])
        if key not in P:
            errs.append("no placement for %s/%s %s" % (k["sub"], k["theme_id"], k["second_order"])); continue
        used.add(key)
        first, why, conf, second = P[key]
        item = "%s/%s" % (k["sub"], k["theme_id"])
        parent = "%s/%s" % (k["sub"], k["parent"])
        if item in have:
            errs.append("%s already placed" % item)
        sec = {t: cs for t, (cs, _) in second.items()}
        rest = [c for c in k["code_ids"] if c not in {c for cs in sec.values() for c in cs}]
        sbt = {first: rest}
        sbt.update(sec)
        placed = [first] + list(sec)
        for t in placed:
            if t not in ids:
                errs.append("%s: %s not in scheme" % (item, t))
        errs += ["%s: %s" % (item, p) for p in vlib.support_problems(sbt, placed, k["sub"], k["theme_id"], ct)]
        w = {first: "%s (%d concepts)" % (why, len(rest))}
        for t, (cs, y) in second.items():
            w[t] = "%s (%s)" % (y, ", ".join(cs))
        line = {"sub": k["sub"], "theme_id": k["theme_id"], "item": item, "third_order": placed, "multi": len(placed) > 1,
                "why": w, "confidence": conf, "support": [c for t in placed for c in sbt[t]], "support_by_theme": sbt,
                "item_is_a_bag": False, "also_present": {}, "source": "split", "parent": parent,
                "drawn_as": "child of %s, split at B2b-r2-p2 (QB2-010)" % parent, "concepts": len(k["code_ids"]),
                "fleet_theme_id": ft.get((k["sub"], k["theme_id"])), "placed_by": "author", "stage": "B2", "leg": "B2b-r2-p2"}
        rows["gold" if parent in gold_parents else "author"].append(line)
    for key in P:
        if key not in used:
            errs.append("a placement names no child: %s" % (key,))
    for s in ("author", "gold"):
        r = rows[s]
        print("%s: %d children; multi %d; clear %d; themes %s" % (s, len(r), sum(x["multi"] for x in r),
              sum(x["confidence"] == C for x in r), ", ".join(sorted({t for x in r for t in x["third_order"]}))))
    for e in errs:
        print("ERROR", e)
    if errs or "--write" not in sys.argv:
        return
    for s, name in (("author", "author_items.jsonl"), ("gold", "gold_items.jsonl")):
        with open(os.path.join(OUT, name), "a", encoding="utf-8") as f:
            for x in rows[s]:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
    print("appended %d to author_items.jsonl and %d to gold_items.jsonl" % (len(rows["author"]), len(rows["gold"])))


if __name__ == "__main__":
    main()
