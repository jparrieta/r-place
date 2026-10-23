#!/usr/bin/env python3
"""D3b: list the re-check lines of one element whose latest ruling has one kind (for example correction or
elaboration), with room, op, pair, the ruling's leg and its whole reason. Writes nothing.

    python3 out/_analysis/d3b_kind_list.py --element A21 --kind correction
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--kind", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


new = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r.get("adaptation") in new:
        last[r["adaptation"]] = r
n = 0
for i in sorted(last):
    r = last[i]
    l = new[i]
    if l.get("element") != a.element or r.get("kind") != a.kind:
        continue
    n += 1
    print("== %s  %s  %s  pair=%s  leg=%s" % (i, l.get("room") or l.get("sub"), l.get("op"), r.get("pair"), r.get("leg")))
    print("   " + str(r.get("reason")))
print("[%d lines: %s, kind %s]" % (n, a.element, a.kind))
