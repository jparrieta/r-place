#!/usr/bin/env python3
"""D5, the check beside the theme rule: each member's coded concepts, each theme's largest contributor,
and the ratios with the largest record left out. Counts as d5_themes.py counts them.

    python3 out/_analysis/d5_theme_drop.py --branch F20 [--drop sub]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
ap.add_argument("--drop", default="")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


t4, names = {}, {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    names[r["id"]] = r.get("name")
    for m in r.get("members") or []:
        t4[m] = r["id"]
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
ncodes = collections.Counter()
for r in jl(os.path.join(STORE, "codes.jsonl")):
    ncodes[(r["sub"], r.get("theme_id"))] += 1
room = collections.defaultdict(collections.Counter)
for key, n in ncodes.items():
    nodes = [t4[x] for x in place.get(key, []) if x in t4]
    for node in nodes:
        room[key[0]][node] += n / len(nodes)
b = next(x for x in jl(os.path.join(OUT, "branches.jsonl")) if x["id"] == a.branch)
ms = set(b["members"])
pop = collections.Counter()
for c in room.values():
    pop.update(c)
pt = sum(pop.values())
tot = {s: round(sum(room[s].values()), 1) for s in ms}
print("member totals", sorted(tot.items(), key=lambda x: -x[1]), "branch", round(sum(tot.values()), 1))
drop = a.drop or max(tot, key=tot.get)


def ratios(keep, skip=None):
    br = collections.Counter()
    for s in keep:
        br.update({k: v for k, v in room[s].items() if k != skip})
    bt = sum(br.values())
    pt2 = sum(v for k, v in pop.items() if k != skip)
    out = {}
    for k in sorted(pop):
        if k == skip:
            continue
        ps, bs = pop[k] / pt2, br.get(k, 0) / bt
        out[k] = (round(bs / ps, 3) if ps else None, sum(1 for s in keep if room[s].get(k, 0) > 0), round(ps, 4))
    return out


full = ratios(ms)
less = ratios(ms - {drop})
nokey = ratios(ms, "T4-001")
print("dropped", drop)
for k in sorted(pop):
    big = max(ms, key=lambda s: room[s].get(k, 0))
    share = room[big].get(k, 0) / max(sum(room[s].get(k, 0) for s in ms), 1e-9)
    print(k, names.get(k), "full", full[k][:2], "without", less[k][:2], "keying out", nokey.get(k, ("-",))[0],
          "largest", big, round(share, 3), "pop", full[k][2])
