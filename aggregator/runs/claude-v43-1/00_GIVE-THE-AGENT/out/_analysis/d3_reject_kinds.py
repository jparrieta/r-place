#!/usr/bin/env python3
"""D3: sort the latest rejects of the ids in given rulings files into kinds by regex over their latest reasons, first
match wins, and print counts and ids per kind. Writes nothing.

    python3 out/_analysis/d3_reject_kinds.py --files out/_analysis/d3_rulings/P18-inst-*.jsonl \
        --kind "visitor=visitor|outsider" --kind "record=P12's"
"""
import argparse, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--files", nargs="+", required=True)
ap.add_argument("--kind", action="append", default=[])
a = ap.parse_args()
kinds = [(k.split("=", 1)[0], re.compile(k.split("=", 1)[1], re.I)) for k in a.kind]
want = []
for p in a.files:
    with open(p) as f:
        want += [json.loads(l)["adaptation"] for l in f if l.strip()]
latest = {}
with open(os.path.join(OUT, "adjudications.jsonl")) as f:
    for line in f:
        r = json.loads(line)
        if r["adaptation"] in set(want):
            latest[r["adaptation"]] = r
out = {k: [] for k, _ in kinds}
out["(none)"] = []
for i in dict.fromkeys(want):
    r = latest.get(i)
    if not r or r["decision"] != "reject":
        continue
    for k, rx in kinds:
        if rx.search(r["reason"]):
            out[k].append(i)
            break
    else:
        out["(none)"].append(i)
for k, ids in out.items():
    print("%s: %d: %s" % (k, len(ids), ", ".join(ids)))
print("total rejects: %d" % sum(len(v) for v in out.values()))
