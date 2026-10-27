#!/usr/bin/env python3
"""D6a-12: the three rooms of form B, one per facet, by the rule logged in the diary before any room was read. A defining
room holds a facet where it has a selected change line (role defining) whose fourth-order theme is the facet's: chat
T4-010, scripts T4-009, raids T4-020. Candidates per facet: B's defining rooms holding that facet only, at or below the
median distance to B's centre, nearer B's centre than any other form's. Rank: selected changes, coded concepts (most
first), distance (nearest first). Fallbacks, in order: rooms holding the facet with another; then no distance limit.
Reads no room's record. Prints JSON.

    python3 out/_analysis/d6a12_select_B.py > out/_analysis/d6a12_select_B.json
"""
import collections, csv, json, os, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

FACETS = {"chat": "T4-010", "scripts": "T4-009", "raids": "T4-020"}
rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
dfn = [s for s, r in rows.items() if r["form"] == "B" and r["role"] == "defining"]
held = collections.defaultdict(set)
for l in json.load(open(os.path.join(AN, "d5a37_lines.json"), encoding="utf-8"))["lines"]:
    if l.get("role") == "defining":
        t4 = l.get("t4") if isinstance(l.get("t4"), list) else [l.get("t4")]
        for f, t in FACETS.items():
            if t in t4:
                held[l["sub"]].add(f)
counts = {f: sum(1 for s in dfn if f in held[s]) for f in FACETS}
assert counts == {"chat": 48, "scripts": 49, "raids": 40}, counts


def dist(s, g):
    return float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g]))


info = {}
for s in dfn:
    info[s] = {"sub": s, "distance": round(dist(s, "B"), 4), "nearest_centre": min(E.CENTRE, key=lambda g: dist(s, g)),
               "selected_changes": int(rows[s]["selected_changes"]), "coded_concepts": int(rows[s]["coded_concepts"]),
               "facets": sorted(held[s])}
order = sorted(info.values(), key=lambda x: x["distance"])
for i, x in enumerate(order, 1):
    x["rank_by_distance"] = i
med = float(np.median([x["distance"] for x in order]))
rank = lambda xs: sorted(xs, key=lambda x: (-x["selected_changes"], -x["coded_concepts"], x["distance"]))  # noqa: E731
out = {"form": "B", "defining": len(dfn), "facet_counts": counts, "median_distance": round(med, 4), "facets": {}}
for f in FACETS:
    steps = [("facet only, nearer half, nearest centre B",
              [x for x in order if x["facets"] == [f] and x["distance"] <= med and x["nearest_centre"] == "B"]),
             ("facet with another, nearer half, nearest centre B",
              [x for x in order if f in x["facets"] and x["distance"] <= med and x["nearest_centre"] == "B"]),
             ("facet, any distance, nearest centre B",
              [x for x in order if f in x["facets"] and x["nearest_centre"] == "B"])]
    for label, cands in steps:
        if cands:
            r = rank(cands)
            out["facets"][f] = {"step": label, "candidates": len(cands), "chosen": r[0], "next": r[1:4]}
            break
print(json.dumps(out, ensure_ascii=False))
