#!/usr/bin/env python3
"""D5a-32: tie data for F32 against its nearest branches, the representatives' branches, the
aftermath spread and work_remained in F32, work_remained in the within-size pool (as d5_within.py
draws it), survival of F07, F09 and F15, and A07 restrict rooms among F32's members. Prints text.

    python3 out/_analysis/d5a32_checks.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines, effective_lines  # noqa: E402

B = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
M = B["F32"]["members"]


def km(l, k):
    op, el, node = k.split(":")
    lv = "3" if node.startswith("T3") else "4"
    return l["op"] == op and l["element"] == el and distance.node_at(l, lv) == node


S = shared_lines(OUT)
for nb in ["F07", "F15", "F28", "F09", "F23", "F21", "F17"]:
    for r in sorted(set(M) & set(B[nb]["members"]), key=str.lower):
        inb = [b for b in B if r in B[b]["members"]]
        n32 = sum(1 for l in S if l["sub"] == r and km(l, B["F32"]["keys"][0]))
        nn = sum(1 for l in S if l["sub"] == r and km(l, B[nb]["keys"][0]))
        print(nb, r, inb, "F32", n32, nb, nn)
for r in ["luxembourg", "habs", "newzealand", "rickandmorty"]:
    print(r, [b for b in B if r in B[b]["members"]])
E = effective_lines(OUT, include_particular=True)
a07 = set(l["sub"] for l in E if l["element"] == "A07" and l["op"] == "restrict")
print("A07 restrict in F32", sorted(set(M) & a07, key=str.lower))
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
a = sorted([(oe[s]["aftermath_share"], s) for s in M if isinstance(oe[s].get("aftermath_share"), (int, float))], reverse=True)
print(len(a), a[:3])
print("work_remained", sorted([(oe[s].get("work_remained", "silent"), s) for s in M]))
c = collections.Counter(json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"))
med = statistics.median(c[s] for s in M)
pool = {s for s in c if s not in M and c[s] >= med}
print("pool", len(pool), "work_remained", dict(collections.Counter(oe.get(s, {}).get("work_remained", "silent") for s in pool)))
for l in open(os.path.join(OUT, "branches-D5.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if d["branch"] in ("F07", "F09", "F15"):
        print(d["branch"], d["survival"])
