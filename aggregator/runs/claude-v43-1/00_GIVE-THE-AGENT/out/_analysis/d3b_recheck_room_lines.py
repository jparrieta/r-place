#!/usr/bin/env python3
"""D3b: the re-check lines of some rooms on one or more elements, each with its op, observation, cited codes, its
condition, statement or relation, and its last ruling (decision and kind, and the reason cut to --reason-chars), so
that an arrow's two-way check can read the room's accepted re-check lines beside its first-return lines (which
d3b_first_return.py prints). Reads the ledgers only; writes nothing.

    python3 out/_analysis/d3b_recheck_room_lines.py --elements K02,P10 --rooms korea,dota2 --reason-chars 400
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", required=True)
ap.add_argument("--rooms", required=True)
ap.add_argument("--reason-chars", type=int, default=400)
a = ap.parse_args()
rooms = set(a.rooms.split(","))
elements = set(a.elements.split(","))


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
rows = [l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
        if l.get("sub") in rooms and l.get("element") in elements]
rows.sort(key=lambda l: (l["sub"], l["element"], l["id"]))
for l in rows:
    d = last.get(l["id"], {})
    print("== %s  %s  %s %s  codes %s" % (l["id"], l["element"], l["op"], l.get("observation") or "",
                                          ",".join(codes(l))))
    for k in ("condition", "statement", "relation"):
        if l.get(k):
            print("   %s: %s" % (k, l[k]))
    reason = (d.get("reason") or "")[:a.reason_chars]
    print("   ruling: %s/%s: %s" % (d.get("decision"), d.get("kind"), reason))
print("[%d lines]" % len(rows))
