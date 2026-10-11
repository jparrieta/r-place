#!/usr/bin/env python3
"""B2a-r2: the rechecks round 1's edits owe the ten biggest bags, appended to author_items.jsonl in this leg
(out/_analysis/b2_rechecks_owed_r2.txt and _p2.txt, from `mem.py rechecks --owed`, two pages).

The ten were placed after the edits, so no edit can have moved a placement made before it. The check
still asks each edit's record; each is recorded after reading the edit's new sentence against the item
(--show prints them). Placement and concepts are the item's own (third_order, support_by_theme); the
reason names what the sentence says and why the item stays. Dry run unless --write; --max N slices.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")

# edit -> why the edited sentence leaves the owed items where they are (filled after reading --show)
_002 = "the new T3-002 question sets members called to place against another mark; no owed item is a call for hands, so none moves"
_010 = ("the new question sets a line or space settled between neighbours (T3-010) against its neighbour; no owed item "
        "settles a line: ainbowroad t11 asks the host room for space or permission (T3-035, which this question names), "
        "ainbowroad t03 calls fights against attackers (T3-005)")
_023 = ("the new question asks whether the sub is turned into something else for the day and played inside (T3-023); "
        "both makeovers are that, and objections, asks to keep the theme and the posting rule are minor parts of them")
WHY = {
 "edit:1": _002, "edit:7": _002, "edit:8": _002, "edit:9": _002,
 "edit:14": ("placing the mark and reporting progress (T3-038) against arguing its look (T3-004): 2007scape t04's "
             "progress logs lead and its corrections serve the build; ainbowroad t07 extends the road rather than arguing its look"),
 "edit:58": ("placing the mark and reporting progress (T3-038) against arguing its look (T3-004): 2007scape t04's "
             "progress logs lead; ainbowroad t04's colour-order fixes are upkeep, which T3-021's must_show names"),
 "edit:15": ("the room's own work defended (T3-005) against another room's work helped (T3-011): ainbowroad t03 defends "
             "the road and its core; ainbowroad t04 repairs, with others' work named under also_present T3-011; "
             "theblackvoid t09 calls attacks and defends nothing"),
 "edit:35": "the room's own work defended (T3-005) against another room's work helped (T3-011): ainbowroad t03 defends the road and its core",
 "edit:21": ("repair where no fight is called goes to T3-021: ainbowroad t03 calls fights (war, fight back, man all "
             "positions) and stays T3-005; ainbowroad t04 is repair with no fight called and stays T3-021"),
 "edit:46": "repair during a raid counts here when the fixing leads and no fight is called; ainbowroad t04's fixing leads",
 "edit:47": ("a mark announced as up (T3-026) against the homeland's flag (T3-065): sweden t01 is the Swedish flag; "
             "2007scape t04's announcements of completion sit inside the building and its reports (T3-038)"),
 "edit:72": "sweden t01 is the flag of the room's own land, called for, built and repaired: T3-065",
 "edit:73": "sweden t01 holds the calls, proportions, spot and repair of the Swedish flag, which the widened must_show names",
 "edit:78": ("what happened to the work told (T3-073) against the finished work celebrated (T3-009): neither leads in "
             "2007scape t04 (building) or ainbowroad t04 (repair)"),
 "edit:239": ("what happened to the work told (T3-073) against a named room blamed after the close (T3-058): neither "
              "leads in 2007scape t04 or ainbowroad t04"),
 "edit:84": "members called to place (T3-002) against another room asked for help (T3-084): ainbowroad t11 is outside rooms asking the host for space or permission, T3-035",
 "edit:281": _010, "edit:275": _010, "edit:276": _010, "edit:278": _010, "edit:280": _010, "edit:282": _010,
 "edit:283": _010, "edit:284": _010, "edit:285": _010, "edit:286": _010,
 "edit:85": "tracing who changed the work (T3-087) against excluding a member (T3-121): ainbowroad t03 does neither as its lead; it calls fights",
 "edit:88": "a lone piece the room takes up goes to T3-038 for the room's build; 2007scape t04 is the room's builds",
 "edit:231": _023, "edit:232": _023, "edit:243": _023, "edit:244": _023,
 "edit:250": ("moderators blamed for a loss (T3-118) against posting rules changed (T3-185): the r/tz and Marc Merrill "
              "posting rules are part of the day's makeover, which T3-023 carries"),
 "edit:237": ("a member's own piece added to a shared mark (T3-060) against converting another room's art (T3-068): "
              "ainbowroad t07's lead is extending the road's strands and features (T3-041); outside pieces are under also_present T3-035"),
 "edit:238": "converting another room's art (T3-068): theblackvoid t09 calls to consume named targets, not to make them the room's sign; T3-006",
 "edit:248": "another room's request refused (T3-115) against a neighbour granted space (T3-012): ainbowroad t11 is the requests themselves, T3-035",
 "edit:273": "a neighbour let onto the room's work (T3-012): ainbowroad t11 is the asking, not the granting; T3-035",
 "edit:257": "calls for swastikas (T3-177) against arguing a political symbol (T3-080): theblackvoid t09 calls attacks on named targets; T3-006",
 "edit:259": ("griefing for fun (T3-192) against pushing into a neighbour's space (T3-061): theblackvoid t09 is the calls "
              "naming targets to consume, which T3-006 carries"),
 "edit:260": ("griefing for fun (T3-192) against pushing into a neighbour's space (T3-061): theblackvoid t09 is calls to "
              "attack (T3-006); ainbowroad t07's push over the American flag is under also_present T3-061 and extension leads"),
 "edit:264": "envoys (T3-194) against alliances (T3-150): theblackvoid t12's lead is professing loyalty to the Void, T3-174",
 "edit:268": "agreements invoked (T3-195) against alliances (T3-150): theblackvoid t12's lead is professing loyalty to the Void, T3-174",
}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    placed = {r["item"]: r for r in jl(os.path.join(OUT, "author_items.jsonl"))}
    edits = jl(os.path.join(OUT, "scheme_edits.jsonl"))
    owed, edit = [], None
    for name in ("b2_rechecks_owed_r2.txt", "b2_rechecks_owed_r2_p2.txt"):
        for line in open(os.path.join(OUT, "_analysis", name), encoding="utf-8"):
            m = re.match(r"^(edit:\d+)\s", line)
            if m:
                edit = m.group(1)
            m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s", line)
            if m:
                owed.append((edit, "%s/%s" % (m.group(1), m.group(2))))
    owed = list(dict.fromkeys(owed))
    done = set()
    for d in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        done.add((str(d.get("change")), str(d.get("item") or "%s/%s" % (d.get("sub"), d.get("theme_id")))))
    owed = [(e, it) for e, it in owed if (e, it) not in done]
    if "--show" in sys.argv:
        for e in dict.fromkeys(e for e, _ in owed):
            x = edits[int(e.split(":")[1]) - 1]
            its = [it for ee, it in owed if ee == e]
            now, was = x.get("now"), x.get("was")
            if isinstance(now, list) and isinstance(was, list):
                now = [d for d in now if d not in was]        # what the edit added or reworded
            print("%s %s %s (%s)\n  changed: %s\n  owes: %s\n" % (e, x.get("theme"), x.get("field"), x.get("kind"),
                  json.dumps(now, ensure_ascii=False),
                  "; ".join("%s on %s" % (it, ",".join(placed[it]["third_order"])) for it in its)))
        return
    calls, nowhy = [], []
    for e, it in owed:
        r = placed[it]
        if e not in WHY:
            nowhy.append(e)
            continue
        th = r["third_order"]
        codes = ";".join("%s=%s" % (t, ",".join(r["support_by_theme"][t])) for t in th)
        reason = ("unchanged: placed at B2a-r2, after %s, and read against its sentence: %s" % (e, WHY[e]))
        calls.append([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "recheck", it.replace("/", ":"),
                      "--change", e, "--theme", ",".join(th), "--codes", codes, "--reason", reason, "--stage", "B2"])
    print("owed %d over %d items; to record %d; edits with no reason yet: %s" % (
        len(owed), len({it for _, it in owed}), len(calls), sorted(set(nowhy)) or "none"))
    if nowhy or "--write" not in sys.argv:
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
