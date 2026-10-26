#!/usr/bin/env python3
"""D5a-35: tie data for F35 against F25 and F07, the population's add-step lines on P01 by node, other P01
add-step lines of members, the representatives' branches, the A12 restrict rooms, the aftermath spread, end
hours and work_remained (with its codes) in F35, work_remained in the within-size pool (as d5_within.py draws
it), and survival of F25 and F07. Prints text.

    python3 out/_analysis/d5a35_checks.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines, effective_lines  # noqa: E402

B = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
M = B["F35"]["members"]
KEY = B["F35"]["keys"][0]


def km(l, k):
    op, el, node = k.split(":")
    lv = "3" if node.startswith("T3") else "4"
    return l["op"] == op and l["element"] == el and distance.node_at(l, lv) == node


S = shared_lines(OUT)
p01 = [l for l in S if l["op"] == "add-step" and l["element"] == "P01"]
print("population add-step P01 lines", len(p01), "rooms", len(set(l["sub"] for l in p01)))
print("by third-order node", collections.Counter(distance.node_at(l, "3") for l in p01).most_common(8))
print("members' other add-step P01 lines", [(l["sub"], distance.node_at(l, "3")) for l in p01 if l["sub"] in M and not km(l, KEY)])
for nb in ["F25", "F07"]:
    for r in sorted(set(M) & set(B[nb]["members"]), key=str.lower):
        inb = [b for b in B if r in B[b]["members"]]
        n35 = sum(1 for l in S if l["sub"] == r and km(l, KEY))
        nn = sum(1 for l in S if l["sub"] == r and km(l, B[nb]["keys"][0]))
        print(nb, r, inb, "F35", n35, nb, nn)
for r in ["tenma", "polyamory", "seahawks", "clashroyale", "wow"]:
    print(r, [b for b in B if r in B[b]["members"]])
E = effective_lines(OUT, include_particular=True)
a12 = set(l["sub"] for l in E if l["element"] == "A12" and l["op"] == "restrict")
print("A12 restrict in F35", sorted(set(M) & a12, key=str.lower), "population", len(a12))
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
a = sorted([(oe[s]["aftermath_share"], s) for s in M if isinstance(oe[s].get("aftermath_share"), (int, float))], reverse=True)
print(len(a), a[:4])
print("end hours", sorted([(oe[s].get("organizing_end_hour"), s) for s in M], key=lambda x: (x[0] is None, x[0])))
print("work_remained", sorted([(oe[s].get("work_remained", "silent"), s, oe[s].get("work_remained_codes")) for s in M]))
c = collections.Counter(json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"))
med = statistics.median(c[s] for s in M)
pool = {s for s in c if s not in M and c[s] >= med}
print("pool", len(pool), "work_remained", dict(collections.Counter(oe.get(s, {}).get("work_remained", "silent") for s in pool)))
for l in open(os.path.join(OUT, "branches-D5.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if d["branch"] in ("F25", "F07"):
        print(d["branch"], d["survival"], d["form_or_grouping"])
