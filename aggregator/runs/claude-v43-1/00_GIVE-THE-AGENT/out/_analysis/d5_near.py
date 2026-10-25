#!/usr/bin/env python3
"""D5, section 2.11: for one branch, Jaccard overlap with every branch outside its own line of descent, and the
cross-links that name it, grouped by the other branch. Prints JSON.

    python3 out/_analysis/d5_near.py --branch F01
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


bs = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
me = bs[a.branch]
kin = {a.branch, me.get("parent")} | {k for k, b in bs.items() if b.get("parent") == a.branch}
ms = set(me["members"])
jac = []
for k, b in bs.items():
    if k in kin:
        continue
    o = set(b["members"])
    shared = ms & o
    jac.append({"branch": k, "parent": b.get("parent"), "n": len(o), "shared": len(shared),
                "jaccard": round(len(shared) / len(ms | o), 4), "shared_rooms": sorted(shared)})
jac.sort(key=lambda x: -x["jaccard"])
links = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "crosslinks.jsonl")):
    if a.branch in r["branches"]:
        others = [x for x in r["branches"] if x != a.branch]
        links[",".join(others)].append(r["sub"])
print(json.dumps({"branch": a.branch, "kin": sorted(x for x in kin if x), "nearest": jac,
                  "crosslinks": {k: sorted(v) for k, v in links.items()},
                  "crosslink_count": sum(len(v) for v in links.values())}, ensure_ascii=False))
