#!/usr/bin/env python3
"""D3b: list the re-check lines whose latest ruling is an accept with no kind, by element, with the ruling's leg
and the first 300 characters of its reason. Writes nothing.

    python3 out/_analysis/d3b_kind_missing.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


new = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r.get("adaptation") in new:
        last[r["adaptation"]] = r
by = collections.Counter()
for i in sorted(last):
    r = last[i]
    if r.get("decision") != "accept" or r.get("kind"):
        continue
    l = new[i]
    by[l.get("element")] += 1
    print("== %s  %s  %s  leg=%s" % (i, l.get("element"), l.get("op"), r.get("leg")))
    print("   " + str(r.get("reason"))[:300])
print("[%d accepted re-check lines with no kind: %s]" % (sum(by.values()), dict(by)))
