#!/usr/bin/env python3
"""D3a-50, read-only: the second finding aid for P06's order test pool (logged before any stop hour was read).
As d3_p06p05_pool.py, with the stop-word aid; it prints only the rooms the first aid did not match, since those were
read from d3_p06p05_pool.txt. Writes nothing.

  python3 out/_analysis/d3_p06p05_pool_v2.py
"""
import re
import subprocess
import sys
from collections import defaultdict

AID1 = r"intended|planned|agreed change|once told|are told|told the|until told"
AID2 = (r"apolog|stands? down|ceas|stop(s|ped)? (repair|refill|fix|undo)|switch(es|ed)? once|once told"
        r"|turn(s|ed)? to help")
R = "out/_analysis/d3_rulings/"
OPS = ("inst", "restrict", "addcond", "addstep", "link", "absent")
HOUR = re.compile(r"h\+(\d+(?:\.\d+)?)")


def room(aid):
    return aid.rsplit("-", 1)[0]


out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", "P05"],
                     capture_output=True, text=True).stdout
hits, first = defaultdict(list), set()
for ln in out.splitlines():
    p = [x.strip() for x in ln.split("|")]
    if len(p) < 6 or p[0] == "id":
        continue
    aid, op, dec, kind, reason = p[0], p[1], p[2], p[3], "|".join(p[5:])
    if dec != "accept":
        continue
    if re.search(AID1, reason):
        first.add(room(aid))
    if re.search(AID2, reason):
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

new = sorted(r for r in hits if r not in first)
pool = [r for r in new if r in shown]
print("second-aid rooms: %d; not matched by the first aid: %d; of them showing P06: %d" % (len(hits), len(new),
                                                                                          len(pool)))
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
print("\nnew second-aid rooms not showing P06: %s" % [r for r in new if r not in shown])
