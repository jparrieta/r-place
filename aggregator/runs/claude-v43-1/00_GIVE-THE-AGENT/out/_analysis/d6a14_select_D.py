#!/usr/bin/env python3
"""D6a-14, form D's telling: one room per leaf of D's kept splits (D.1, D.2.1, D.2.2; room-forms-names.md), by the rule
logged in the diary before any room was read. A room's leaf is the prefix of its address in room-forms-tree-rooms.tsv.
Candidates: the leaf's defining rooms at or below the median of D's defining distances to D's centre (the allocation's
columns, d4a08_embed, as D5 measured it), and nearer D's centre than any other form's. Rank: selected changes, coded
concepts (most first), distance (nearest first). If a leaf has no candidate, the distance limit is dropped. Reads no
room's record. Prints JSON.

    python3 out/_analysis/d6a14_select_D.py > out/_analysis/d6a14_select_D.json
"""
import csv, json, os, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
F = "D"
LEAVES = {"D.1": "keeping with the call", "D.2.1": "the play, carried on", "D.2.2": "the play, kept"}
dfn = [s for s, r in rows.items() if r["form"] == F and r["role"] == "defining"]


def dist(s, g):
    return float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g]))


def leaf(s):
    a = rows[s]["address"].split("/")[0]
    return next(lf for lf in LEAVES if a == lf or a.startswith(lf + "."))


info = []
for s in dfn:
    d = dist(s, F)
    info.append({"sub": s, "leaf": leaf(s), "distance": round(d, 4),
                 "nearest_centre": min(E.CENTRE, key=lambda g: dist(s, g)),
                 "selected_changes": int(rows[s]["selected_changes"]),
                 "coded_concepts": int(rows[s]["coded_concepts"])})
info.sort(key=lambda x: x["distance"])
for i, x in enumerate(info, 1):
    x["rank_by_distance"] = i
med = float(np.median([x["distance"] for x in info]))
out = {"form": F, "defining": len(dfn), "median_distance": round(med, 4),
       "q1_distance": round(float(np.percentile([x["distance"] for x in info], 25)), 4),
       "median_selected_changes": float(np.median([x["selected_changes"] for x in info])),
       "leaf_sizes": {lf: sum(1 for x in info if x["leaf"] == lf) for lf in LEAVES}, "leaves": {}}
assert out["leaf_sizes"] == {"D.1": 54, "D.2.1": 27, "D.2.2": 15}, out["leaf_sizes"]
for lf, name in LEAVES.items():
    key = lambda x: (-x["selected_changes"], -x["coded_concepts"], x["distance"])  # noqa: E731
    c = sorted([x for x in info if x["leaf"] == lf and x["distance"] <= med and x["nearest_centre"] == F], key=key)
    fallback = False
    if not c:
        fallback = True
        c = sorted([x for x in info if x["leaf"] == lf and x["nearest_centre"] == F], key=key)
    out["leaves"][lf] = {"name": name, "candidates": len(c), "fallback": fallback, "chosen": c[0] if c else None,
                         "next": c[1:5]}
print(json.dumps(out, ensure_ascii=False))
