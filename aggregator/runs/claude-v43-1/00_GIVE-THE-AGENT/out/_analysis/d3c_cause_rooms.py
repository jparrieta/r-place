#!/usr/bin/env python3
"""D3c, for the handback: the adaptation ids a history line names (its 'adaptations'), with each line's room,
element, op and last ruling, and each room's verdict before (first return) and after (re-check), and the room's
re-check lines on the same element with their last rulings. Read-only.

    python3 out/_analysis/d3c_cause_rooms.py --line 136
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--line", type=int, required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


H = jl(os.path.join(OUT, "model", "history.jsonl"))
h = H[a.line - 1]
by_id = {}
for n in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in jl(os.path.join(OUT, n)):
        by_id[l["id"]] = l
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
vr = jl(os.path.join(OUT, "verdicts-D.jsonl"))
rv = jl(os.path.join(OUT, "verdicts-recheck-D.jsonl"))


def verdict(rows, sub, recheck):
    for r in vr:
        if r.get("ruled_by") == "analyst" and r["sub"] == sub and bool(r.get("recheck")) == recheck:
            return r["verdict"] + " (ruled)"
    for r in rows:
        if r["sub"] == sub and not r.get("ruled_by"):
            vs = sorted({e["verdict"] for e in r["readers"]})
            return "/".join(vs)


print("history line %d: %s %s (%s); %d adaptations" % (a.line, h.get("id"), h.get("field"), h.get("leg"),
                                                       len(h.get("adaptations") or [])))
rooms = []
for i in h.get("adaptations") or []:
    l = by_id.get(i, {})
    d = last.get(i, {})
    print("  %s %s %s %s -> %s/%s" % (i, l.get("sub"), l.get("element"), l.get("op"), d.get("decision"), d.get("kind")))
    if l.get("sub") and l["sub"] not in rooms:
        rooms.append(l["sub"])
for s in rooms:
    print("== %s: before %s; after %s" % (s, verdict(vr, s, False), verdict(rv, s, True)))
    for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl")):
        if l["sub"] == s and l.get("element") == h.get("id") and l["op"] != "absent":
            d = last.get(l["id"], {})
            print("   %s %s -> %s/%s | %s" % (l["id"], l["op"], d.get("decision"), d.get("kind"),
                                           (d.get("reason") or "")[:260]))
