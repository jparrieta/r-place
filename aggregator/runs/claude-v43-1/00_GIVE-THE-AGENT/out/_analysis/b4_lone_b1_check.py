#!/usr/bin/env python3
"""Read-only. J's answer (12:28 Berlin) on lone B1 themes: the agent chooses. This lists the class 4 rulings (both
readers agree) that keep a theme only my B1 placed, with its concept count, and what the ruling becomes if such a
theme needs three concepts or more of its own to stand against the two agreeing readers.

    python3 out/_analysis/b4_lone_b1_check.py [--packets 1,2,3,4,5,6] [--list] [--class 4]
"""
import argparse
import collections
import json

ap = argparse.ArgumentParser()
ap.add_argument("--packets", default="1,2,3,4,5,6")
ap.add_argument("--list", action="store_true")
ap.add_argument("--class", dest="cls", type=int, default=4)
a = ap.parse_args()
packets = {int(x) for x in a.packets.split(",")}
stat = collections.Counter()
for x in open("out/disagreements.jsonl", encoding="utf-8"):
    d = json.loads(x)
    if d.get("packet") not in packets or d.get("class") != a.cls or d.get("unresolved"):
        continue
    stat["lines"] += 1
    readers = set(d["readers"][0]) | set(d["readers"][1])
    sup = d.get("support_by_theme") or {}
    lone = [t for t in d["ruling"] if t not in readers]
    weak = [t for t in lone if len(sup.get(t, [])) < 3]
    if not lone:
        continue
    stat["keeps a lone B1 theme"] += 1
    if not weak:
        stat["lone B1 theme has 3+ concepts"] += 1
        continue
    rest = [t for t in d["ruling"] if t not in weak]
    if d["taxonomy"] == "item-is-a-bag":
        kind = "bag placing a weak lone theme"
    elif not rest:
        kind = "would be unresolved"
    elif set(rest) == readers:
        kind = "would become the readers' list"
    else:
        kind = "would still differ from the readers"
    stat[kind] += 1
    if a.list:
        print("packet %s item %s %s/%s | %s | readers %s | ruling %s | weak %s | -> %s %s"
              % (d["packet"], d["n"], d["sub"], d["theme_id"], d["taxonomy"], sorted(readers), d["ruling"],
                 {t: len(sup.get(t, [])) for t in weak}, kind, rest))
for k, v in stat.items():
    print("%s: %d" % (k, v))
