#!/usr/bin/env python3
"""D5, section 2.8: a branch's pooled share of coded concepts on each fourth-order theme against the population's.
The rule is in the diary (D5a-01). Prints JSON.

    python3 out/_analysis/d5_themes.py --branch F01
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


t4 = {}
names = {}
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
pop, br = collections.Counter(), collections.Counter()
carry = collections.Counter()
for s, c in room.items():
    pop.update(c)
    if s in ms:
        br.update(c)
        carry.update({k for k, v in c.items() if v > 0})
pt, bt = sum(pop.values()), sum(br.values())
rows = []
for k in sorted(pop):
    ps, bs = pop[k] / pt, br.get(k, 0) / bt
    rows.append({"t4": k, "name": names.get(k), "pop_share": round(ps, 4), "branch_share": round(bs, 4),
                 "ratio": round(bs / ps, 3) if ps else None, "members": carry.get(k, 0)})
over = [r["t4"] for r in rows if r["ratio"] and r["ratio"] >= 1.5 and r["members"] >= 5]
under = [r["t4"] for r in rows if r["ratio"] is not None and r["ratio"] <= 0.67 and r["pop_share"] >= 0.01]
print(json.dumps({"branch": a.branch, "n": len(ms), "rooms_pop": len(room), "over": over, "under": under,
                  "rows": rows}, ensure_ascii=False))