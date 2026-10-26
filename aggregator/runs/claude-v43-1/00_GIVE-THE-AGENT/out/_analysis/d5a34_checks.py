#!/usr/bin/env python3
"""D5a-34: tie data for F34 against F07 and F21, the population's add-condition lines on P02 by node, other
P02 add-condition lines of members, the key lines' third-order nodes, the representatives' branches, the A16
restrict rooms, the aftermath spread, end hours and work_remained in F34, work_remained in the within-size pool
(as d5_within.py draws it), and survival of F07, F21 and F33. Prints text.

    python3 out/_analysis/d5a34_checks.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines, effective_lines  # noqa: E402

B = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
M = B["F34"]["members"]
KEY = B["F34"]["keys"][0]


def km(l, k):
    op, el, node = k.split(":")
    lv = "3" if node.startswith("T3") else "4"
    return l["op"] == op and l["element"] == el and distance.node_at(l, lv) == node


S = shared_lines(OUT)
p02 = [l for l in S if l["op"] == "add-condition" and l["element"] == "P02"]
print("population add-condition P02 lines", len(p02), "rooms", len(set(l["sub"] for l in p02)))
print("by fourth-order node", collections.Counter(distance.node_at(l, "4") for l in p02).most_common(8))
print("members' other add-condition P02 lines", [(l["sub"], distance.node_at(l, "4")) for l in p02 if l["sub"] in M and not km(l, KEY)])
kl = [l for l in S if l["sub"] in M and km(l, KEY)]
print("key lines", len(kl), "third-order nodes", collections.Counter(distance.node_at(l, "3") for l in kl).most_common())
for nb in ["F07", "F21", "F10", "F33"]:
    for r in sorted(set(M) & set(B[nb]["members"]), key=str.lower):
        inb = [b for b in B if r in B[b]["members"]]
        n34 = sum(1 for l in S if l["sub"] == r and km(l, KEY))
        nn = sum(1 for l in S if l["sub"] == r and km(l, B[nb]["keys"][0]))
        print(nb, r, inb, "F34", n34, nb, nn)
for r in ["crystalclear", "borderlands", "detroitlions", "4chan", "aoe2"]:
    print(r, [b for b in B if r in B[b]["members"]])
E = effective_lines(OUT, include_particular=True)
a16 = set(l["sub"] for l in E if l["element"] == "A16" and l["op"] == "restrict")
print("A16 restrict in F34", sorted(set(M) & a16, key=str.lower), "population", len(a16))
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
    if d["branch"] in ("F07", "F21", "F33"):
        print(d["branch"], d["survival"], d["form_or_grouping"])
