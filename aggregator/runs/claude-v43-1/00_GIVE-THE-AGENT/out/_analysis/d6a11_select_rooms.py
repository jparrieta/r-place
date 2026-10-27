#!/usr/bin/env python3
"""D6a-11 to D6a-16, the form tellings: the three rooms of a form, by the rule logged in the diary at D6a-11 before any
room was read. Candidates: the form's defining rooms whose distance to the form's centre (the allocation's columns, as
D5 measured it through d4a08_embed) is at or below the first quartile of the form's defining distances, and which lie
nearer this form's centre than any other form's. Rank: selected changes (most first), coded concepts (most first),
distance (nearest first). The first three are chosen. Reads no room's record. Prints JSON.

    python3 out/_analysis/d6a11_select_rooms.py --form A > out/_analysis/d6a11_select_A.json
"""
import argparse, csv, json, os, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
f = a.form
dfn = [s for s, r in rows.items() if r["form"] == f and r["role"] == "defining"]
assert all(s in E.IDX for s in dfn)


def dist(s, g):
    return float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g]))


info = []
for s in dfn:
    d = dist(s, f)
    near = min(E.CENTRE, key=lambda g: dist(s, g))
    info.append({"sub": s, "distance": round(d, 4), "nearest_centre": near,
                 "selected_changes": int(rows[s]["selected_changes"]), "coded_concepts": int(rows[s]["coded_concepts"])})
info.sort(key=lambda x: x["distance"])
for i, x in enumerate(info, 1):
    x["rank_by_distance"] = i
q1 = float(np.percentile([x["distance"] for x in info], 25))
cands = [x for x in info if x["distance"] <= q1 and x["nearest_centre"] == f]
cands.sort(key=lambda x: (-x["selected_changes"], -x["coded_concepts"], x["distance"]))
print(json.dumps({"form": f, "defining": len(dfn), "q1_distance": round(q1, 4),
                  "median_distance": round(float(np.median([x["distance"] for x in info])), 4),
                  "median_selected_changes": float(np.median([x["selected_changes"] for x in info])),
                  "candidates": len(cands), "chosen": cands[:3], "next": cands[3:8]}, ensure_ascii=False))
