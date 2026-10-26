#!/usr/bin/env python3
"""D5, sections 6, 7 and 11: within-size comparisons, the section 7 rule and the nearest-branch tie.
Rates count members (and rooms of the comparison pool) with at least one current-ledger line of the op,
particular lines included (effective_lines(include_particular=True)), as at D5a-12 to D5a-20.
The pool: rooms outside the branch with at least the branch's median count of coded concepts.

    python3 out/_analysis/d5_within.py --branch F21 [--near F30]
"""
import argparse, collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import effective_lines, shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
ap.add_argument("--near", default="")
a = ap.parse_args()
OUT = os.path.join(ROOT, "out")
bs = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()}
ms = set(bs[a.branch]["members"])
n = len(ms)
E = list(effective_lines(OUT, include_particular=True))
c = collections.Counter(json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"))
med = statistics.median(c[s] for s in ms)
pool = {s for s in c if s not in ms and c[s] >= med}
print("members", n, "median coded concepts", med, "population median", statistics.median(c.values()), "pool", len(pool))
print("members by coded concepts", sorted(((c[s], s) for s in ms)))
by = collections.defaultdict(set)
for l in E:
    by[(l.get("element"), l["op"])].add(l["sub"])
els = sorted({k[0] for k in by if k[0]})
print("one member", round(1 / n, 3))
rows = []
for el in els:
    if not el.startswith("A"):
        continue
    m, p = len(by[(el, "restrict")] & ms), len(by[(el, "restrict")] & pool)
    rows.append((round(m / n - p / len(pool), 3), el, m, p))
print("section 7 (restrict excess, members, pool):", sorted(rows, reverse=True)[:6])
print("absent in at least a quarter of members (members, pool, excess):")
for el in els:
    m, p = len(by[(el, "absent")] & ms), len(by[(el, "absent")] & pool)
    if m >= n / 4:
        print(" ", el, m, p, round(m / n - p / len(pool), 3))
print("instantiate (members, pool):", [(el, len(by[(el, "instantiate")] & ms), len(by[(el, "instantiate")] & pool)) for el in els if not el.startswith("A")])
print("restrict (members, pool):", [(el, len(by[(el, "restrict")] & ms), len(by[(el, "restrict")] & pool)) for el in els if not el.startswith("A") and by[(el, "restrict")] & ms])
pr = {l["sub"] for l in E if l["op"] == "propose"}
print("propose rooms (members, pool)", len(pr & ms), len(pr & pool), "lines in members", sum(1 for l in E if l["op"] == "propose" and l["sub"] in ms))
if a.near:
    S = list(shared_lines(OUT))
    lev = {"T3": "3", "T4": "4"}

    def count(sub, key):
        op, el, node = key.split(":", 2)
        level = lev.get(node[:2], "dim")
        return sum(1 for l in S if l["sub"] == sub and l["op"] == op and l["element"] == el and distance.node_at(l, level) == node)

    shared = sorted(ms & set(bs[a.near]["members"]), key=str.lower)
    for s in shared:
        here = sum(count(s, k) for k in bs[a.branch]["keys"])
        there = sum(count(s, k) for k in bs[a.near]["keys"])
        other = sorted(b for b, d in bs.items() if s in d["members"] and b not in (a.branch, a.near))
        print("tie", s, "here", here, "there", there, "other branches", len(other), other)
    print(a.near, bs[a.near]["name"], bs[a.near]["keys"], bs[a.near].get("parent"))
