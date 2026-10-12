#!/usr/bin/env python3
"""B2b-r2-p2: the rechecks round 2's edits (scheme_edits 287 to 295) owe, from `mem.py rechecks --owed`
(out/_analysis/b2_rechecks_owed_r2b.txt, _p2, _p3: three pages).

Each owed item was read against the edit's sentence; none moves (the reasons per edit below). The
placement recorded is the item's current one (the owed list's "on ..."), and its concepts come from the
item's latest recheck record (support_by_theme), else from its own line's why and support. Dry run unless
--write; --max N slices the calls (a record takes about 4.5 seconds).
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")

WHY = {
 "edit:287": ("the T3-002/T3-065 question now says a flag built in a room named for a land is that land's flag; "
              "the item is no flag of a land the room is named for, or is already T3-065"),
 "edit:293": ("the T3-065 questions now say whose flag a flag in a room named for a land is; the item's placement "
              "already follows that reading or holds no such flag"),
 "edit:294": "T3-065's gloss now says a flag built in a room named for a land is that land's flag; the item already sits on T3-065",
 "edit:290": ("the T3-026/T3-065 question now says whose flag a flag in a room named for a land is; the item announces "
              "no such flag as up, or already sits on T3-065"),
 "edit:291": ("the new T3-033/T3-038 question (an idea offered against a mark placed and reported, the side with more "
              "concepts primary) leaves the item where it is: its larger side is the one it is placed on"),
 "edit:292": ("the new T3-038/T3-033 question (a mark placed and reported against an idea offered, the side with more "
              "concepts primary) leaves the item where it is: its larger side is the one it is placed on"),
 "edit:295": ("the new T3-195 questions (an agreement invoked against the work defended or helped, the pledge only "
              "the reason) leave the item where it is: it invokes no agreement, or, like nVade t04, it helps and "
              "defends with the pledge named only as the reason"),
 "edit:288": ("the new T3-005/T3-195 question leaves the item where it is: the room defends its own work and invokes "
              "no agreement as the lead"),
 "edit:289": ("the new T3-011/T3-195 question leaves the item where it is: help is given to another room's work, a "
              "pledge at most its reason"),
}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    placed = {}
    for name in ("author_items.jsonl", "gold_items.jsonl"):
        for r in jl(os.path.join(OUT, name)):
            placed[r["item"]] = r
    latest = {}
    done = set()
    for d in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        it = "%s/%s" % (d["sub"], d["theme_id"])
        done.add((d["change"], it))
        if it not in latest or d["t"] >= latest[it]["t"]:
            latest[it] = d
    owed, edit = [], None
    for name in ("b2_rechecks_owed_r2b.txt", "b2_rechecks_owed_r2b_p2.txt", "b2_rechecks_owed_r2b_p3.txt"):
        for line in open(os.path.join(OUT, "_analysis", name), encoding="utf-8"):
            m = re.match(r"^(edit:\d+)\s", line)
            if m:
                edit = m.group(1)
            m = re.match(r"^\s+owed: ([^:]+):(t\d+)\s+on (\S+)", line)
            if m:
                owed.append((edit, "%s/%s" % (m.group(1), m.group(2)), m.group(3).split(",")))
    owed = [o for o in dict.fromkeys((e, it, tuple(th)) for e, it, th in owed) if (o[0], o[1]) not in done]
    calls, nowhy = [], set()
    for e, it, th in owed:
        if e not in WHY:
            nowhy.add(e)
            continue
        th = list(th)
        sbt = (latest.get(it) or {}).get("support_by_theme") or {}
        r = placed[it]
        parts = []
        for t in th:
            cs = sbt.get(t) or (r.get("support_by_theme") or {}).get(t)
            if not cs:
                cs = [c for c in re.findall(r"c\d{4}", (r.get("why") or {}).get(t, "")) if c in r["support"]] or r["support"]
            parts.append("%s=%s" % (t, ",".join(cs)))
        reason = "unchanged: read against %s's sentence: %s" % (e, WHY[e])
        calls.append([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "recheck", it.replace("/", ":"),
                      "--change", e, "--theme", ",".join(th), "--codes", ";".join(parts), "--reason", reason, "--stage", "B2"])
    print("owed %d over %d items; to record %d; edits without a reason: %s" % (
        len(owed), len({it for _, it, _ in owed}), len(calls), sorted(nowhy) or "none"))
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
