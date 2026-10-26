#!/usr/bin/env python3
"""D5a-33: tie data for F33 against its nearest branches, overlap with F15 (the kin key at T4-008), the
representatives' branches, A07 restrict rooms in F33 and across F27, F30, F31 and F33, the aftermath spread
and work_remained in F33, work_remained in the within-size pool (as d5_within.py draws it), survival of
F10, F14 and F15, and the third-order nodes of the key lines. Prints text.

    python3 out/_analysis/d5a33_checks.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines, effective_lines  # noqa: E402

B = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
M = B["F33"]["members"]


def km(l, k):
    op, el, node = k.split(":")
    lv = "3" if node.startswith("T3") else "4"
    return l["op"] == op and l["element"] == el and distance.node_at(l, lv) == node


S = shared_lines(OUT)
print("F15 shared with F33", sorted(set(M) & set(B["F15"]["members"]), key=str.lower), "F15 n", len(B["F15"]["members"]))
p04 = [l for l in S if l["op"] == "add-step" and l["element"] == "P04"]
print("population add-step P04 lines", len(p04), "rooms", len(set(l["sub"] for l in p04)))
print("by fourth-order node", collections.Counter(distance.node_at(l, "4") for l in p04).most_common(8))
print("F33 members' other add-step P04 lines", [(l["sub"], distance.node_at(l, "4")) for l in p04 if l["sub"] in M and not km(l, B["F33"]["keys"][0])])
kl = [l for l in S if l["sub"] in M and km(l, B["F33"]["keys"][0])]
print("key lines", len(kl), "third-order nodes", collections.Counter(distance.node_at(l, "3") for l in kl).most_common())
for nb in ["F14", "F10", "F28", "F29", "F23", "F07"]:
    for r in sorted(set(M) & set(B[nb]["members"]), key=str.lower):
        inb = [b for b in B if r in B[b]["members"]]
        n33 = sum(1 for l in S if l["sub"] == r and km(l, B["F33"]["keys"][0]))
        nn = sum(1 for l in S if l["sub"] == r and km(l, B[nb]["keys"][0]))
        print(nb, r, inb, "F33", n33, nb, nn)
for r in ["kuwait", "mit", "feedthebeast", "india", "tf2"]:
    print(r, [b for b in B if r in B[b]["members"]])
E = effective_lines(OUT, include_particular=True)
a07 = set(l["sub"] for l in E if l["element"] == "A07" and l["op"] == "restrict")
print("A07 restrict in F33", sorted(set(M) & a07, key=str.lower))
u = set()
for b in ["F27", "F30", "F31", "F33"]:
    u |= set(B[b]["members"]) & a07
print("union F27 F30 F31 F33", len(u), "population", len(a07))
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
a = sorted([(oe[s]["aftermath_share"], s) for s in M if isinstance(oe[s].get("aftermath_share"), (int, float))], reverse=True)
print(len(a), a[:4])
print("end hours", sorted([(oe[s].get("organizing_end_hour"), s) for s in M], key=lambda x: (x[0] is None, x[0])))
print("work_remained", sorted([(oe[s].get("work_remained", "silent"), s) for s in M]))
c = collections.Counter(json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"))
med = statistics.median(c[s] for s in M)
pool = {s for s in c if s not in M and c[s] >= med}
print("pool", len(pool), "work_remained", dict(collections.Counter(oe.get(s, {}).get("work_remained", "silent") for s in pool)))
for l in open(os.path.join(OUT, "branches-D5.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if d["branch"] in ("F10", "F14", "F15"):
        print(d["branch"], d["survival"], d["form_or_grouping"])
