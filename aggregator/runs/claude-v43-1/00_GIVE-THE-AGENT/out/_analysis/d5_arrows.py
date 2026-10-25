#!/usr/bin/env python3
"""D5, rule 6: for one branch, each arrow's expectation (its subs over the 705 analysed rooms times n), the members
among its subs, and the members with an accepted current-ledger line on the arrow, by op (description only); then each
proposition with the arrows it rests on and whether any reaches an expectation of one. Prints JSON.

    python3 out/_analysis/d5_arrows.py --branch F01
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


b = next(x for x in jl(os.path.join(OUT, "branches.jsonl")) if x["id"] == a.branch)
ms = set(b["members"])
n = len(ms)
rooms = {r["sub"] for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
lines = collections.defaultdict(collections.Counter)
for l in shared_lines(OUT):
    if l["sub"] in ms and str(l.get("element", "")).startswith("A"):
        lines[l["element"]][l["op"]] += 1
arrows = []
for r in jl(os.path.join(OUT, "model", "arrows.jsonl")):
    subs = set(r.get("subs") or []) & rooms
    exp = len(subs) / len(rooms) * n
    arrows.append({"arrow": r["id"], "from": r.get("from"), "to": r.get("to"), "subs": len(subs),
                   "expected": round(exp, 3), "members_in_subs": sorted(subs & ms),
                   "member_lines": dict(lines.get(r["id"], {}))})
exp = {x["arrow"]: x["expected"] for x in arrows}
props = [{"id": p["id"], "rests_on": p.get("rests_on"), "max_expected": max(exp.get(x, 0) for x in p.get("rests_on") or [])}
         for p in jl(os.path.join(OUT, "propositions.jsonl"))]
print(json.dumps({"branch": a.branch, "n": n, "analysed": len(rooms), "arrows": arrows, "propositions": props},
                 ensure_ascii=False))
