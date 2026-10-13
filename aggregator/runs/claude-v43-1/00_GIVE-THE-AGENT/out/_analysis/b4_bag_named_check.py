#!/usr/bin/env python3
"""B4a-06: QB4-002 (J, 09:20 Berlin) makes a theme a reader listed under its own also_present a named theme, so it
may stand in a bag's also_present. My bag test had counted placed themes only. This check counts, per ruled line,
the themes at the three-concept floor once named themes are added.

    python3 out/_analysis/b4_bag_named_check.py [--packets 1,2,3,4,5] [--list]

Read-only. For each ruled line: the ruling's themes with three concepts or more in support_by_theme, the
also_present themes with three or more, and each theme a reader listed under its own also_present (in
assign_raw.jsonl) that is not a placement, with the concepts the readers listed for it that the ruling does not
already use. A line that is not a bag and reaches four themes at the floor is flagged "would be a bag"; a bag with
such a theme is flagged "bag could list". The concepts still need reading against the theme's tests before a ruling
changes; this only finds the lines.
"""
import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packets", default="1,2,3,4,5")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    packets = {int(x) for x in a.packets.split(",") if x.strip()}
    raw = collections.defaultdict(lambda: collections.defaultdict(set))
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x.get("copy_kind") != "corpus":
            continue
        apd = x.get("also_present") or {}
        if isinstance(apd, dict):
            for t, cs in apd.items():
                raw["%s/%s" % (x["sub"], x["theme_id"])][t] |= set(cs or [])
    stat = collections.defaultdict(collections.Counter)
    for d in jl(os.path.join(OUT, "disagreements.jsonl")):
        p = d.get("packet")
        if p not in packets:
            continue
        stat[p]["lines"] += 1
        key = "%s/%s" % (d["sub"], d["theme_id"])
        placed = set(d["readers"][0]) | set(d["readers"][1]) | set(d.get("b1") or [])
        sup = d.get("support_by_theme") or {}
        apd = d.get("also_present") or {}
        used = set()
        for cs in list(sup.values()) + list(apd.values()):
            used |= set(cs)
        floor = [t for t in d["ruling"] if len(sup.get(t, [])) >= 3]
        floor += [t for t in apd if len(apd[t]) >= 3 and t not in floor]
        cand = {}
        for t, cs in raw[key].items():
            if t in placed or t in apd:
                continue
            free = sorted(set(cs) - used)
            if len(free) >= 3:
                cand[t] = free
        if not cand:
            continue
        bag = d["taxonomy"] == "item-is-a-bag"
        if bag:
            kind = "bag could list"
        elif len(floor) + len(cand) >= 4:
            kind = "would be a bag"
        else:
            kind = "named theme at the floor, under four"
        stat[p][kind] += 1
        if a.list and kind != "named theme at the floor, under four":
            print("packet %s item %s %s | %s | %s | ruling %s | floor %s | named-only %s"
                  % (p, d["n"], key, kind, d["taxonomy"], d["ruling"], floor,
                     {t: v for t, v in sorted(cand.items())}))
    for p in sorted(stat):
        print("packet %s: %s" % (p, dict(stat[p])))


if __name__ == "__main__":
    main()
