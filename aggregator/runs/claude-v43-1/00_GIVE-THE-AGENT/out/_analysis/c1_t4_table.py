#!/usr/bin/env python3
"""C1 section 8, read-only: the third-order tier laid out for cutting fourth-order themes. Per family (families.jsonl),
every theme of scheme_v2.jsonl with its tier, its placements in assignments_final.jsonl (any position), as the
line's first theme, and its rooms, then its gloss. With --pairs, the themes most often placed on one line with
each theme (co-placement), and with --fourth, the fourth-order theme each sits in (fourth/fourth.jsonl).

    python3 out/_analysis/c1_t4_table.py [--family G04] [--pairs] [--fourth] [--no-gloss]
"""
import argparse, collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    p = os.path.join(OUT, p)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--family", default="")
ap.add_argument("--pairs", action="store_true")
ap.add_argument("--fourth", action="store_true")
ap.add_argument("--no-gloss", dest="gloss", action="store_false")
a = ap.parse_args()

scheme = jl("scheme_v2.jsonl")
fams = dict((f.get("family") or f.get("id"), f) for f in jl("families.jsonl"))
rows = jl("assignments_final.jsonl")
anyp, first, rooms = collections.Counter(), collections.Counter(), collections.defaultdict(set)
co = collections.defaultdict(collections.Counter)
for r in rows:
    th = r.get("third_order") or []
    for i, t in enumerate(th):
        anyp[t] += 1
        rooms[t].add(r["sub"])
        if i == 0:
            first[t] += 1
        for u in th:
            if u != t:
                co[t][u] += 1
own = {}
for f in jl(os.path.join("fourth", "fourth.jsonl")):
    for m in f.get("members") or []:
        own[m] = f["id"]
names = dict((t["id"], t["name"]) for t in scheme)
by = collections.defaultdict(list)
for t in scheme:
    by[t.get("family")].append(t)
for fam in sorted(by):
    if a.family and fam != a.family:
        continue
    fr = fams.get(fam) or {}
    print("## %s %s (%d themes)" % (fam, fr.get("name") or fr.get("label") or "", len(by[fam])))
    for t in by[fam]:
        i = t["id"]
        print("%s%s %-46s any %4d first %4d rooms %3d%s" % (
            i, " R" if t.get("tier") == "rare" else "  ", t["name"][:46], anyp[i], first[i], len(rooms[i]),
            ("  [%s]" % own[i]) if a.fourth and i in own else ""))
        if a.gloss:
            print("      " + " ".join(str(t.get("gloss") or "").split()))
        if a.pairs and co[i]:
            print("      with: " + "; ".join("%s %s %d" % (u, names.get(u, "")[:28], n) for u, n in co[i].most_common(4)))
    print()
