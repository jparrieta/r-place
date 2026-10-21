#!/usr/bin/env python3
"""D3a-55: one packet of the unattached propose lines, read whole (QD3-001), by lifted node (stage D3 section 3).
Selects every ledger line with op propose, orders them by the source's third-order node (unplaced last), then by
room and id, and prints the slice [offset, offset + limit) with every field whole: id, source and its label, the
lift, the statement, relation, how, portable and its hits, the cited concepts with their labels from the store, the
transitions and the line's current decision. A node header names each third-order node and its fourth-order node
and dimension the first time it appears in the packet. Writes nothing.

    python3 out/_analysis/d3_propose_packet.py --offset 0 --limit 100 [--node T3-017]
"""
import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=100)
ap.add_argument("--node", help="only lines whose source lifts to this third-order node ('none' for unplaced)")
a = ap.parse_args()
if a.limit > 100:
    raise SystemExit("a packet holds at most 100 lines (stage D3)")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def node(l, i):
    lift = l.get("lift") or []
    return lift[i] if len(lift) > i and lift[i] else None


sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("op") == "propose"]
sel.sort(key=lambda l: (node(l, 1) is None, node(l, 1) or "", l["sub"], l["id"]))
if a.node:
    sel = [l for l in sel if (node(l, 1) or "none") == a.node]
page = sel[a.offset:a.offset + a.limit]
subs = {l["sub"] for l in page}
adj = {r.get("adaptation"): r for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
labels, tlabels = {}, {}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        labels[(r["sub"], r["code_id"])] = r.get("first_order")
for l in open(os.path.join(ROOT, "package", "store", "themes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r.get("sub") in subs:
        tlabels[(r["sub"], r.get("theme_id"))] = r.get("second_order") or r.get("label")
names = {}
for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    i = r.get("id") or r.get("theme_id")
    if i and i not in names:
        names[i] = r.get("name") or r.get("label")
counts = collections.Counter(node(l, 1) or "none" for l in sel)
print("propose lines: %d in all%s; packet [%d, %d): %d lines in %d rooms" % (
    len(sel), " (node %s)" % a.node if a.node else "", a.offset, a.offset + len(page), len(page), len(subs)))
print("nodes in the packet: %s" % dict(collections.Counter(node(l, 1) or "none" for l in page)))
seen = set()
for l in page:
    n3 = node(l, 1) or "none"
    if n3 not in seen:
        seen.add(n3)
        print("\n#### node %s (%s): %d lines in all; fourth-order %s; dimension %s" % (
            n3, names.get(n3, "unplaced"), counts[n3], node(l, 2), node(l, 3)))
    d = adj.get(l["id"], {}).get("decision", l.get("decision"))
    print("\n== %s  propose  [%s]%s" % (l["id"], d, "" if l.get("portable", True) else
                                       "  NONPORTABLE %s" % l.get("nonportable_hits")))
    src = l.get("source")
    if src:
        print("   source %s (%s); lift %s" % (src, tlabels.get((l["sub"], src.split(":")[-1])),
                                            " > ".join(str(x) for x in (l.get("lift") or []))))
    for k in ("statement", "relation"):
        if l.get(k):
            print("   %s: %s" % (k, l[k]))
    print("   how: %s" % l.get("how"))
    ev = l.get("evidence") or {}
    print("   codes: %s" % "; ".join("%s %s" % (c, labels.get((l["sub"], c.split(":")[-1]), "?"))
                                     for c in ev.get("codes", [])))
    if ev.get("transitions"):
        print("   transitions: %s" % ", ".join(ev["transitions"]))
