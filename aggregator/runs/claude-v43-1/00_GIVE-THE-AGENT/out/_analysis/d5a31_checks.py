#!/usr/bin/env python3
"""D5a-31: tie data for F31 against F24, members' branches, A07 restrict rooms across F27, F30 and F31,
the aftermath spread in F31, and the survival of F24 and F07. Prints text.

    python3 out/_analysis/d5a31_checks.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines, effective_lines  # noqa: E402

B = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}


def km(l, k):
    op, el, node = k.split(":")
    lv = "3" if node.startswith("T3") else "4"
    return l["op"] == op and l["element"] == el and distance.node_at(l, lv) == node


S = shared_lines(OUT)
for r in ["mindcrack", "nbaspurs", "prequelmemes", "uoft"]:
    inb = [b for b in B if r in B[b]["members"]]
    n31 = sum(1 for l in S if l["sub"] == r and km(l, B["F31"]["keys"][0]))
    n24 = sum(1 for l in S if l["sub"] == r and km(l, B["F24"]["keys"][0]))
    print(r, inb, "F31", n31, "F24", n24)
for r in ["foxes", "FloydVsVoid", "prequelmemes"]:
    print(r, [b for b in B if r in B[b]["members"]])
E = effective_lines(OUT, include_particular=True)
a07 = set(l["sub"] for l in E if l["element"] == "A07" and l["op"] == "restrict")
u = set()
for b in ["F27", "F30", "F31"]:
    s = set(B[b]["members"]) & a07
    print(b, len(s), sorted(s, key=str.lower))
    u |= s
print("union", len(u), "population rooms with an A07 restrict line", len(a07))
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8") if l.strip()}
a = sorted([(oe[s]["aftermath_share"], s) for s in B["F31"]["members"] if isinstance(oe[s].get("aftermath_share"), (int, float))], reverse=True)
print(len(a), a[:3])
for l in open(os.path.join(OUT, "branches-D5.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    if d["branch"] in ("F24", "F07"):
        print(d["branch"], d["survival"])
