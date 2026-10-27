#!/usr/bin/env python3
"""D5a-40, form E: form E's defining rooms set beside form D's part D.2 (form D's notes ask for it), and E's own parts
(E.1, E.2, E.1.1, E.1.2): the share of defining rooms holding named fourth-order change columns, F01's and F02's rooms in
each, the centroid distances between D.2, D and E in the allocation's columns, and each group's rooms nearest its own
centroid. Prints JSON to stdout.

    python3 out/_analysis/d5a40_parts.py > out/_analysis/d5a40_parts.json
"""
import json, os, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

COLS = ["T4-001", "T4-027", "T4-007", "T4-013", "T4-006", "T4-005", "T4-002", "T4-028", "T4-017", "T4-025"]
tl = open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8").read().splitlines()
hd = tl[0].split("\t")
R = [dict(zip(hd, l.split("\t"))) for l in tl[1:]]
br = {json.loads(l)["id"]: set(json.loads(l)["members"]) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
cols = E.CCOLS["T4"]
Pm = E.MCD["T4"] > 0


def group(form, part=None):
    rooms = [r for r in R if r["form"] == form and (part is None or r["address"].split("/")[0] == part
                                                     or r["address"].startswith(part + "."))]
    return rooms


out = {"groups": {}}
cent = {}
for label, form, part in (("E", "E", None), ("E.1", "E", "E.1"), ("E.2", "E", "E.2"), ("E.1.1", "E", "E.1.1"),
                          ("E.1.2", "E", "E.1.2"), ("D", "D", None), ("D.2", "D", "D.2")):
    rooms = group(form, part)
    defs = [r["room"] for r in rooms if r["role"] == "defining"]
    idx = [E.IDX[s] for s in defs]
    cen = E.XD[idx].mean(axis=0)
    cent[label] = cen
    names = {r["room"] for r in rooms}
    out["groups"][label] = {
        "all": len(rooms), "defining": len(defs),
        "shares": {c: round(float(Pm[idx, cols.index(c)].mean()), 3) for c in COLS},
        "holders": {c: int(Pm[idx, cols.index(c)].sum()) for c in COLS},
        "F01_all": len(br["F01"] & names), "F02_all": len(br["F02"] & names),
        "nearest_own_centroid": sorted(defs, key=lambda s: float(np.linalg.norm(E.XD[E.IDX[s]] - cen)))[:5]}
out["centroid_distances"] = {a + "|" + b: round(float(np.linalg.norm(cent[a] - cent[b])), 4)
                             for a, b in (("D.2", "E"), ("D.2", "D"), ("D", "E"), ("E.1", "E.2"))}
# D.2's defining rooms: which form centre is each nearest (the allocation's centres)
d2 = [r["room"] for r in group("D", "D.2") if r["role"] == "defining"]
near = {}
for s in d2:
    d = {g: float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g])) for g in E.CENTRE}
    near[s] = min(d, key=d.get)
out["D.2_defining_nearest_centre"] = {g: sum(1 for s in d2 if near[s] == g) for g in sorted(set(near.values()))}
out["D.2_defining_nearer_E_than_D"] = sorted((s for s in d2 if np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE["E"])
                                              < np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE["D"])), key=str.lower)
json.dump(out, sys.stdout, indent=1)
sys.stdout.write("\n")
