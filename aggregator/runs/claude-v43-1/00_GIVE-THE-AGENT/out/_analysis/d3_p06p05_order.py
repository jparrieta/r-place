#!/usr/bin/env python3
"""D3a-50, read-only: P06's order test against P05 under the rules logged before it ran. For each pooled room in
d3_p06p05_stops.txt (room|stop code|what the stop is), H_stop is the stop concept's hour as cite.py printed it in
d3_p06p05_stop_cites.txt; H_att is the earliest hour in the room's P06-shown spec rows, and H_om the earliest in rows
tagged OM or FF. Prints each room's order and the counts: before (H_att earlier), tie (equal hours) and after.
Writes nothing.

  python3 out/_analysis/d3_p06p05_order.py
"""
import re
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = ("inst", "restrict", "addcond", "addstep", "link", "absent")
HOUR = re.compile(r"h\+(\d+(?:\.\d+)?)")
QLINE = re.compile(r'^"(.*)"  \[([^/\]]+)/(c\d{4})\].*?h\+(\d+(?:\.\d+)?)')


def room(aid):
    return aid.rsplit("-", 1)[0]


cite = {}
for l in open("out/_analysis/d3_p06p05_stop_cites.txt", encoding="utf-8"):
    m = QLINE.match(l)
    if m:
        cite[(m.group(2), m.group(3))] = float(m.group(4))
tags, spec = {}, {}
for op in OPS:
    for l in open(R + "P06-tags-%s.txt" % op, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            tags[i] = set(t.split(","))
    for l in open(R + "P06-%s-spec.txt" % op, encoding="utf-8"):
        if l.strip():
            i, _, ev = l.rstrip("\n").split("|")[:3]
            spec[i] = ev
shown = defaultdict(list)
for i in tags:
    shown[room(i)].append(i)

count = {"att": Counter(), "om": Counter()}
for l in open("out/_analysis/d3_p06p05_stops.txt", encoding="utf-8"):
    if not l.strip():
        continue
    r, code, what = l.rstrip("\n").split("|")
    hs = cite[(r, code)]
    best = {"att": None, "om": None}
    for i in shown[r]:
        hours = [float(h) for h in HOUR.findall(spec.get(i, ""))]
        if not hours:
            continue
        h = min(hours)
        if best["att"] is None or h < best["att"][0]:
            best["att"] = (h, i)
        if tags[i] & {"OM", "FF"} and (best["om"] is None or h < best["om"][0]):
            best["om"] = (h, i)
    out = []
    for k in ("att", "om"):
        v = best[k]
        if v is None:
            res = "none"
        else:
            res = "before" if v[0] < hs else ("tie" if v[0] == hs else "after")
            out.append("H_%s h+%.2f (%s) %s" % (k, v[0], v[1], res))
        count[k][res] += 1
    print("%-12s stop %s h+%.2f (%s); %s" % (r, code, hs, what, "; ".join(out)))
for k in ("att", "om"):
    print("H_%s against H_stop: %s" % (k, dict(sorted(count[k].items()))))
