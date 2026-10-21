#!/usr/bin/env python3
"""D3a-50, read-only: the pool for P06's order test against P05 (its rules logged before this ran). Selects P05's
accepted lines, as last adjudicated (d3_group_rulings.py), whose reasons match the finding aid, keeps the rooms that
also show P06 (a row in a P06 tag file), and prints for each room its matching P05 rulings whole, then the earliest
hour in its P06-shown spec rows (H_att) and the earliest in rows tagged OM or FF (H_om), with the row giving each.
Also prints the matching rooms that do not show P06. Writes nothing.

  python3 out/_analysis/d3_p06p05_pool.py
"""
import re
import subprocess
import sys
from collections import defaultdict

AID = r"intended|planned|agreed change|once told|are told|told the|until told"
R = "out/_analysis/d3_rulings/"
OPS = ("inst", "restrict", "addcond", "addstep", "link", "absent")
HOUR = re.compile(r"h\+(\d+(?:\.\d+)?)")


def room(aid):
    return aid.rsplit("-", 1)[0]


out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", "P05"],
                     capture_output=True, text=True).stdout
hits = defaultdict(list)
for ln in out.splitlines():
    p = [x.strip() for x in ln.split("|")]
    if len(p) < 6 or p[0] == "id":
        continue
    aid, op, dec, kind, reason = p[0], p[1], p[2], p[3], "|".join(p[5:])
    if dec == "accept" and re.search(AID, reason):
        hits[room(aid)].append((aid, op, kind, reason))

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
for i, t in tags.items():
    shown[room(i)].append(i)

pool = sorted(r for r in hits if r in shown)
print("finding-aid rooms: %d; of them showing P06: %d" % (len(hits), len(pool)))
for r in pool:
    print("\n== %s" % r)
    for aid, op, kind, reason in hits[r]:
        print("  P05 %s %s %s: %s" % (aid, op, kind, reason))
    best = {"att": None, "om": None}
    for i in shown[r]:
        hs = [float(h) for h in HOUR.findall(spec.get(i, ""))]
        if not hs:
            continue
        h = min(hs)
        if best["att"] is None or h < best["att"][0]:
            best["att"] = (h, i)
        if tags[i] & {"OM", "FF"} and (best["om"] is None or h < best["om"][0]):
            best["om"] = (h, i)
    for k in ("att", "om"):
        v = best[k]
        print("  H_%s: %s" % (k, "none" if v is None else "h+%.2f (%s, tags %s)" % (v[0], v[1],
                                                                                   ",".join(sorted(tags[v[1]])))))
print("\nfinding-aid rooms not showing P06: %s" % sorted(r for r in hits if r not in shown))
