#!/usr/bin/env python3
"""D5a-39, form D: the parts of the reading splits (D.1, D.2, D.2.1, D.2.2), with the share of defining rooms holding
each named fourth-order change column, F01's rooms in each part, and the part's defining rooms nearest its own centre.
Prints JSON to stdout.

    python3 out/_analysis/d5a39_parts.py > out/_analysis/d5a39_parts.json
"""
import json, os, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

COLS = ["T4-013", "T4-028", "T4-017", "T4-001", "T4-005", "T4-006", "T4-002", "T4-008", "T4-013>T4-017"]
tl = open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8").read().splitlines()
hd = tl[0].split("\t")
R = [dict(zip(hd, l.split("\t"))) for l in tl[1:]]
f01 = set(next(json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")
               if json.loads(l)["id"] == "F01")["members"])
cols = E.CCOLS["T4"]
Pm = E.MCD["T4"] > 0
names = {}
for c in COLS:
    names[c] = c
out = {}
for part in ("D.1", "D.2", "D.2.1", "D.2.2"):
    rooms = [r for r in R if r["form"] == "D" and (r["address"].split("/")[0] == part or r["address"].startswith(part + "."))]
    defs = [r["room"] for r in rooms if r["role"] == "defining"]
    idx = [E.IDX[s] for s in defs]
    shares = {c: round(float(Pm[idx, cols.index(c)].mean()), 3) for c in COLS if c in cols}
    cen = E.XD[idx].mean(axis=0)
    near = sorted(defs, key=lambda s: float(np.linalg.norm(E.XD[E.IDX[s]] - cen)))[:6]
    out[part] = {"all": len(rooms), "defining": len(defs), "thin": sum(r["role"] == "thin" for r in rooms),
                 "core": sum(r["role"] == "core" for r in rooms), "F01_all": len(f01 & {r["room"] for r in rooms}),
                 "F01_defining": len(f01 & set(defs)), "shares": shares, "nearest_own_centre": near,
                 "defining_rooms": sorted(defs, key=str.lower)}
json.dump(out, sys.stdout, indent=1)
sys.stdout.write("\n")
