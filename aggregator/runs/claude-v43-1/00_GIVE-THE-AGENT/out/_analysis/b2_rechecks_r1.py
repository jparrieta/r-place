#!/usr/bin/env python3
"""B2b-r1: the rechecks the round-1 edits owe (out/_analysis/b2_rechecks_owed_r1.txt, from `mem.py rechecks --owed`).

One decision per item: its placement after the edits, the concepts behind each theme, and why. The same
decision is recorded under every edit that owes it, through `mem.py recheck`, with a reason that says
whether the item moved and, if it moved, whether it is an author-error or the edit doing its work.
author_items.jsonl and gold_items.jsonl stay as written. Dry run by default; --write runs the calls.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")

# item: (themes, codes "T3-a=c1,c2;T3-b=c3", kind of move or "", why)
D = {
 "GreenCorner/t03": (["T3-005"], "T3-005=c0014,c0062,c0065,c0068,c0006,c0031", "edit", "repair here happens inside a fought invasion, and the corrected T3-005 must_not_show keeps it with T3-005; the single placement carries it"),
 "england/t03": (["T3-028"], "T3-028=c0005,c0007,c0008,c0025,c0003,c0006", "author-error", "the image and coordinates are the script's inputs; rule 0's second placement on T3-070 was not needed"),
 "nyu/t01": (["T3-020"], "T3-020=c0001,c0004,c0007,c0015", "author-error", "the spot set and moved leads; the detailed template is handed out, not argued, so T3-004 never applied and one placement carries it"),
 "dofus/t01": (["T3-033"], "T3-033=c0002,c0003,c0004,c0015,c0017", "edit", "a piece begun alone and then offered to the room, the offer leading: T3-033 under T3-092's new decide_when_both; T3-003 was an unneeded second placement"),
 "furry/t10": (["T3-070"], "T3-070=c0034,c0073,c0209,c0233,c0092,c0093", "author-error", "coordinates and templates lead; the lettering layout is handed out as a guide; one placement carries it"),
 "flashtv/t13": (["T3-073"], "T3-073=c0212,c0214,c0215,c0216,c0186,c0213", "author-error", "the account of what became of the logo holds most concepts; its closing praise needs no second placement"),
 "signal/t01": (["T3-038"], "T3-038=c0001,c0002,c0003,c0004,c0006", "author-error", "building the mark and reporting it done is one doing; T3-009 was an unneeded second placement"),
 "acecombat/t05": (["T3-010"], "T3-010=c0054,c0056", "author-error", "item-is-a-bag: borders, help asked, a Discord, help traded and thanks to allies; T3-010 placed, also present T3-084 (c0035, c0041), T3-014 (c0030), T3-151 (c0055)"),
 "4chan/t07": (["T3-010"], "T3-010=c0128,c0136,c0138,c0143,c0011", "author-error", "the border talks lead and the restraint (c0011) is part of them; one placement carries it"),
 "stardustcrusaders/t19": (["T3-043"], "T3-043=c0308,c0310,c0304,c0306", "edit", "a thread of thanks to the makers: under the new decide_when_both of T3-009 and T3-043 the thanks are primary and carry the celebration"),
 "megaman/t11": (["T3-087"], "T3-087=c0032,c0042,c0067", "author-error", "who fires the beam is traced and disputed; the one denial of control (c0067) does not need a second placement"),
 "floridagators/t09": (["T3-014"], "T3-014=c0020,c0062,c0091,c0095,c0067", "author-error", "moving coordination to Discord leads; the one relay (c0067) is part of it"),
 "orderofthebluecorner/t08": (["T3-121"], "T3-121=c0009,c0038", "author-error", "a person named as ruining the corner and moderators asked to ban him: exclusion as a sanction, as all three readers placed it"),
 "kpop/t04": (["T3-033"], "T3-033=c0015,c0018,c0019,c0024,c0020,c0022", "author-error", "proposing the mark leads; the turnout doubt is part of deciding whether to propose; one placement carries it"),
 "Goodboye/t03": (["T3-084"], "T3-084=c0026,c0004", "author-error", "item-is-a-bag: help asked of other rooms, outsiders pledging help, help traded and allies thanked; T3-084 placed, also present T3-011 (c0010, c0012, c0035), T3-151 (c0069), T3-072 (c0051)"),
 "simonfraser/t08": (["T3-084"], "T3-084=c0042,c0063,c0029,c0064", "author-error", "help asked between university rooms leads; the help given is the answer to the asking; one placement carries it"),
 "WisconsinBadgers/t04": (["T3-076"], "T3-076=c0029,c0030,c0027", "author-error", "the report of members taking a rival's spot apart is what the restraint answers; T3-006 was an unneeded second placement"),
 "harrypotter/t08": (["T3-017"], "T3-017=c0024,c0025,c0026,c0033,c0309,c0311,c0328", "author-error", "the sub's house-points game leads, the canvas credit given in house points included; one placement carries it"),
 "guatemala/t02": (["T3-065"], "T3-065=c0003,c0004,c0005,c0006,c0007,c0008,c0010", "edit", "the national flag started, timed and announced: under T3-065's widened must_show every step goes here; T3-167 was an unneeded second placement"),
 "russia/t09": (["T3-010"], "T3-010=c0030,c0041,c0101,c0102,c0029", "author-error", "borders and order with neighbours lead; refraining from encroaching (c0029) is part of it"),
 "predators/t04": (["T3-070"], "T3-070=c0012,c0014,c0040", "author-error", "a picture and a grid handed out lead; the one redesign proposal does not need a second placement"),
 "kurdistan/t03": (["T3-010"], "T3-010=c0011,c0013", "author-error", "a deal to share the Hungarian flag's space leads; holding back is part of the same concept"),
}
UNCHANGED_CODES = {}  # filled from the files for items not in D


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    placed = {}
    for name in ("author_items.jsonl", "gold_items.jsonl"):
        for r in jl(os.path.join(OUT, name)):
            placed[r["item"]] = r
    owed = []
    edit = None
    for line in open(os.path.join(OUT, "_analysis", "b2_rechecks_owed_r1.txt"), encoding="utf-8"):
        m = re.match(r"^(edit:\d+)\s", line)
        if m:
            edit = m.group(1)
        m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s", line)
        if m:
            owed.append((edit, "%s/%s" % (m.group(1), m.group(2))))
    done = set()
    rp = os.path.join(OUT, "rechecks-B2.jsonl")
    if os.path.exists(rp):
        for x in open(rp, encoding="utf-8"):
            if x.strip():
                d = json.loads(x)
                done.add((str(d.get("change")), str(d.get("item") or d.get("theme_item") or "%s/%s" % (d.get("sub"), d.get("theme_id")))))
    calls = []
    for ed, it in owed:
        if (ed, it) in done:
            continue
        r = placed[it]
        if it in D:
            th, codes, kind, why = D[it]
            moved = set(th) != set(r["third_order"])
            reason = ("moved from %s to %s (%s): %s" % (",".join(r["third_order"]), ",".join(th),
                      "author-error" if kind == "author-error" else "the edit doing its work", why)) if moved else "unchanged: " + why
        else:
            th = r["third_order"]
            sup = r["support"]
            # concepts per theme: split the support as written, by the why text of each theme
            parts = []
            for t in th:
                cs = [c for c in re.findall(r"c\d{4}", r["why"][t]) if c in sup] or sup
                parts.append("%s=%s" % (t, ",".join(cs)))
            codes = ";".join(parts)
            reason = "unchanged: %s does not move it; %s" % (ed, "; ".join("%s: %s" % (t, r["why"][t]) for t in th))
        calls.append([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "recheck", it.replace("/", ":"),
                      "--change", ed, "--theme", ",".join(th), "--codes", codes, "--reason", reason, "--stage", "B2"])
    items = sorted({it for _, it in owed})
    moved = [it for it in items if it in D and set(D[it][0]) != set(placed[it]["third_order"])]
    print("owed %d over %d items; items moved %d (author-error %d, edit %d)" % (
        len(calls), len(items), len(moved), sum(1 for it in moved if D[it][2] == "author-error"),
        sum(1 for it in moved if D[it][2] == "edit")))
    missing = [it for it in D if it not in items]
    if missing:
        print("decided but owed under no edit: %s" % missing)
    if not write:
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
