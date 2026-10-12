#!/usr/bin/env python3
"""B2b-r3-p3: the rechecks the freeze edits (scheme_edits 296 to 302) owe, from `mem.py rechecks --owed`
(out/_analysis/b2_rechecks_owed_freeze.txt).

Each owed item was read against the changed sentences. The items that hold a call, an offer or a build (or
coordinates against a report) were read whole and their concepts counted by act (ITEM below); the others sit
on a theme the changed sentences only name, and hold no such mix (WHY per edit). None moves. The placement
recorded is the item's current one; its concepts come from CODES where the reading changed them, else the
item's latest recheck record, else its own line. Dry run unless --write; --max N slices the calls.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")

WHY = {
 "edit:296": ("T3-002's decide_when_both now counts the concepts of a call for hands, an offer of what to make and "
              "the build; the item holds no such mix, so the count does not touch its placement"),
 "edit:297": ("T3-002's questions against T3-033 and T3-038 now count concepts; the item sits on a theme those "
              "questions only name and holds no call for hands that the count would weigh against an offer or a build"),
 "edit:298": ("T3-033's decide_when_both now counts the concepts of an offer, a call and the build; the item holds "
              "no such mix, so the count does not touch its placement"),
 "edit:299": ("T3-033's questions against T3-002 and T3-038 now count concepts; the item holds no offer of what to "
              "make weighed against a call or a build"),
 "edit:300": ("T3-038's decide_when_both now counts the concepts of the build against a call or an offer, repairs "
              "unchanged; the item holds no such mix"),
 "edit:301": ("T3-038's questions against T3-002 and T3-033 now count concepts, and a new T3-038/T3-070 question "
              "makes a link to the finished work a report; the item holds neither mix"),
 "edit:302": ("the new T3-070/T3-038 question (directions for placers against the work's state reported, a link to "
              "the finished work a report) leaves the item where it is: it reports no build, or gives no directions"),
}
ITEM = {
 "2007scape/t04": ("349 concepts read whole and counted by act: about 44 place the marks or report their progress "
                   "(Gnome Child, A q p W, Connection Lost, Grand Exchange, Buying Gf logs and finishes), about 35 call "
                   "for hands, about 23 give coordinates, guides or colour directions, about 13 propose a mark; T3-038 "
                   "holds the most, so it stays primary under the cluster's count"),
 "signal/t01": ("one opening question (c0001) against two concepts of placing and reporting (c0002, c0003); T3-038 "
                "holds more, and T3-009 stays for the thanks and the final image (c0004)"),
 "n64/t02": ("one opening call (c0010) against three of building and reporting (c0011, c0012, c0014); the link to the "
             "finished logo is a report under the new T3-038/T3-070 question"),
 "Villanova/t01": ("calls for help (c0001, c0009) against the logo placed and reported (c0003, c0005, the half-built "
                   "V of c0009) and its reference fixed (c0011); T3-038 holds at least as many, and a tie goes to T3-038 "
                   "because the logo was placed"),
 "cloud9/t12": ("one call (c0080) and one failed attempt after the end (c0081): a tie, and the swirl was never placed, "
                "so T3-002 stands"),
 "dankmemes/t10": ("three proposals of what to draw (c0182, c0373, c0565) against one call to donate a pixel (c0181); "
                   "T3-033 holds more"),
 "edboxes/t02": ("calls for hands and to spread the word (c0012, c0013, c0022); no concept places or reports the boxes, "
                 "so T3-002 stands"),
 "mindcrack/t03": ("three calls for help (c0027, c0030, c0051) against one start at given coordinates (c0028) and one "
                   "proposal (c0033); T3-002 holds more"),
 "roosterteeth/t03": ("seven concepts place and report the teeth and the rooster (c0003, c0004, c0030, c0036, c0037, "
                      "c0060, c0075) and none calls for hands; T3-038 stands, T3-004 for the surround colour"),
 "GabrielDropout/t03": ("the build's coordinates and size (c0030), the sign located for helpers (c0002) and the source "
                        "and reference images (c0059, c0066) against two reports (c0018, c0038): the directions hold "
                        "more, so T3-070 stands; the closest of these items"),
 "predators/t04": ("a colour-correct logo and a grid image given for all to use (c0012, c0014); nothing placed and "
                   "reported, so T3-070 stands"),
 "furry/t10": ("c0034 ('working on it at (965, 759)') is now a report of where the work stands under the new "
               "T3-038/T3-070 question and leaves T3-070's support; the template and mapping concepts (c0073, c0209, "
               "c0233) still lead, so T3-070 stands with T3-004"),
 "england/t03": ("a placing script with its run command leads (T3-028), and the image and coordinates given are "
                 "directions for helpers (T3-070); no concept reports the flag's progress"),
 "dofus/t01": ("the Emerald offered to the room (c0002, c0003) and one member placing it alone (T3-003); no hands "
               "called and no room build reported, so the count leaves T3-033"),
 "kpop/t04": ("four proposals of what to draw (c0015, c0018, c0019, c0024) and no call or build; T3-033 stands, "
              "T3-136 for the doubt about turnout"),
 "ainbowroad/t07": ("the cluster's count does not touch T3-041's lead (eight concepts); T3-033 stays under "
                    "also_present with three proposals of its own (c0176, c0198, c0240)"),
}
CODES = {"furry/t10": {"T3-070": ["c0073", "c0209", "c0233"], "T3-004": ["c0092", "c0093"]}}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    placed = {}
    for name in ("author_items.jsonl", "gold_items.jsonl"):
        for r in jl(os.path.join(OUT, name)):
            placed[r["item"]] = r
    latest, done = {}, set()
    for d in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        it = "%s/%s" % (d["sub"], d["theme_id"])
        done.add((d["change"], it))
        if it not in latest or d["t"] >= latest[it]["t"]:
            latest[it] = d
    owed, edit = [], None
    for line in open(os.path.join(OUT, "_analysis", "b2_rechecks_owed_freeze.txt"), encoding="utf-8"):
        m = re.match(r"^(edit:\d+)\s", line)
        if m:
            edit = m.group(1)
        m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s+on (\S+)", line)
        if m and edit in WHY:
            owed.append((edit, "%s/%s" % (m.group(1), m.group(2)), tuple(m.group(3).split(","))))
    owed = [o for o in dict.fromkeys(owed) if (o[0], o[1]) not in done]
    calls = []
    for e, it, th in owed:
        r = placed[it]
        sbt = CODES.get(it) or (latest.get(it) or {}).get("support_by_theme") or r.get("support_by_theme") or {}
        parts = []
        for t in th:
            cs = sbt.get(t)
            if not cs:
                cs = [c for c in re.findall(r"c\d{4}", (r.get("why") or {}).get(t, "")) if c in r["support"]] or r["support"]
            parts.append("%s=%s" % (t, ",".join(cs)))
        reason = "unchanged: read against %s's sentence: %s" % (e, ITEM.get(it) or WHY[e])
        calls.append([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "recheck", it.replace("/", ":"),
                      "--change", e, "--theme", ",".join(th), "--codes", ";".join(parts), "--reason", reason, "--stage", "B2"])
    print("owed %d over %d items; to record %d" % (len(owed), len({it for _, it, _ in owed}), len(calls)))
    if "--write" not in sys.argv:
        if calls:
            print(" ".join(calls[0][2:]))
        return
    if "--max" in sys.argv:
        calls = calls[:int(sys.argv[sys.argv.index("--max") + 1])]
    bad = 0
    for c in calls:
        p = subprocess.run(c, capture_output=True, text=True)
        if p.returncode != 0:
            bad += 1
            print("FAILED %s %s: %s" % (c[3], c[5], (p.stdout + p.stderr).strip()[-300:]))
    print("recorded %d, failed %d" % (len(calls) - bad, bad))


if __name__ == "__main__":
    main()
