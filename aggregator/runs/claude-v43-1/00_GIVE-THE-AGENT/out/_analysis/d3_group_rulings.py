#!/usr/bin/env python3
"""D3: my own rulings for one element, filtered, for writing the stage notes. Reads the element's ledger lines as
`mem.py adaptations --element <id>` selects them and each line's last adjudication, and prints for each line that
passes the filters: id, op, decision, kind, pair and the reason, whole. Writes nothing.

    python3 out/_analysis/d3_group_rulings.py --element P01 [--decision particular] [--op link] [--kind none]
        [--not-op instantiate]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--decision")
ap.add_argument("--op")
ap.add_argument("--not-op")
ap.add_argument("--kind")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") == a.element]
sel.sort(key=lambda l: (l["op"], l["sub"]))
n = 0
for l in sel:
    r = adj.get(l["id"]) or {}
    k = r.get("kind") or l.get("kind") or "-"
    if a.decision and r.get("decision") != a.decision:
        continue
    if a.op and l["op"] != a.op:
        continue
    if a.not_op and l["op"] == a.not_op:
        continue
    if a.kind and k != a.kind:
        continue
    n += 1
    print("%s | %s | %s | %s | pair %s | %s" % (l["id"], l["op"], r.get("decision"), k, r.get("pair") or "-",
                                                 r.get("reason")))
print("[%d lines]" % n)
