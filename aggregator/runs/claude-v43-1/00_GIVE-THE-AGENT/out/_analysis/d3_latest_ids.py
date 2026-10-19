#!/usr/bin/env python3
"""D3: list the ids of rulings files, by their latest ruling in adjudications.jsonl, under one decision
(and kind, if given). The ids come from the given rulings files; the latest ledger line per id decides.
Writes nothing.

    python3 out/_analysis/d3_latest_ids.py --files out/_analysis/d3_rulings/P09-*.jsonl --decision reject
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--files", nargs="+", required=True)
ap.add_argument("--decision", required=True)
ap.add_argument("--kind")
a = ap.parse_args()

by_file = []
for path in a.files:
    with open(path) as f:
        by_file.append((os.path.basename(path), [json.loads(l)["adaptation"] for l in f if l.strip()]))
want = {i for _, ids in by_file for i in ids}
latest = {}
with open(os.path.join(OUT, "adjudications.jsonl")) as f:
    for line in f:
        r = json.loads(line)
        if r["adaptation"] in want:
            latest[r["adaptation"]] = r
seen, total = set(), 0
for name, ids in by_file:
    hits = []
    for i in ids:
        r = latest.get(i)
        if i in seen or r is None:
            continue
        if r["decision"] == a.decision and (a.kind is None or r.get("kind") == a.kind):
            hits.append(i)
            seen.add(i)
    if hits:
        total += len(hits)
        print("%s: %d: %s" % (name, len(hits), ", ".join(hits)))
print("total %s%s: %d" % (a.decision, (" " + a.kind) if a.kind else "", total))
