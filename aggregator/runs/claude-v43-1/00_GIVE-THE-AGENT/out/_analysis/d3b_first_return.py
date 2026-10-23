#!/usr/bin/env python3
"""D3b: the first-return lines of some rooms on one element, each with its op, observation, cited codes, its
condition, statement or relation, and its last ruling (decision, kind and reason), so that a re-check line can be
read beside the line the same room returned before. Reads the ledgers only; writes nothing.

    python3 out/_analysis/d3b_first_return.py --element C02 --rooms achievement_hunter,armenia
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--rooms", required=True)
a = ap.parse_args()
rooms = set(a.rooms.split(","))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
for l in jl(os.path.join(OUT, "adaptations.jsonl")):
    if l["sub"] in rooms and l.get("element") == a.element:
        d = last.get(l["id"], {})
        print("== %s  %s %s  codes %s" % (l["id"], l["op"], l.get("observation") or "", ",".join(codes(l))))
        for k in ("condition", "statement", "relation"):
            if l.get(k):
                print("   %s: %s" % (k, l[k]))
        print("   ruling: %s/%s: %s" % (d.get("decision"), d.get("kind"), d.get("reason")))
