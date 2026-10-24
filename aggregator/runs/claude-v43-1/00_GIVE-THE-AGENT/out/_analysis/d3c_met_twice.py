#!/usr/bin/env python3
"""D3c: list every 'corrections met twice' group as stage_D3.py's close-check forms it (accepted corrections, by
last ruling, grouped by element and by the lift's third- and fourth-order node, two rooms or more), and say whether
model/history.jsonl cites any of the group's ids. For each id: its room, ledger, op and the head of its last
ruling's reason. Read-only.

    python3 out/_analysis/d3c_met_twice.py [--all]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--all", action="store_true", help="print the cited groups too")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


by_id = {}
for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in jl(os.path.join(OUT, name)):
        by_id[l["id"]] = dict(l, _ledger=name)
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
hist_blob = open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8").read()
met = collections.defaultdict(set)
for i, d in last.items():
    l = by_id.get(i)
    if not l or d.get("decision") not in ("accept", "modify") or (d.get("kind") or l.get("kind")) != "correction":
        continue
    lift = l.get("lift") or [None] * 4
    for lvl in (1, 2):
        if len(lift) > lvl and lift[lvl]:
            met[(l.get("element"), lift[lvl])].add(i)
n_uncited = 0
for (el, node), ids in sorted(met.items()):
    if len({by_id[i]["sub"] for i in ids}) < 2:
        continue
    cited = [i for i in ids if i in hist_blob]
    if cited and not a.all:
        continue
    n_uncited += 0 if cited else 1
    print("== %s at %s: %d lines in %d rooms; cited in history.jsonl: %s" % (
        el, node, len(ids), len({by_id[i]["sub"] for i in ids}), ", ".join(sorted(cited)) or "none"))
    for i in sorted(ids):
        l = by_id[i]
        print("   %s  %s  %s  %s | %s" % (i, l["sub"], l["_ledger"], l["op"], (last[i].get("reason") or "")[:160]))
print("groups met twice with no history citation: %d" % n_uncited)
