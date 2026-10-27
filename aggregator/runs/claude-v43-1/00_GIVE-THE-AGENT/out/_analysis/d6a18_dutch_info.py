#!/usr/bin/env python3
"""D6a-18, the Dutch telling: J's 14 rooms side by side. For each: form, role, selected changes, coded concepts, distance
to the form's centre in the allocation's columns (defining rooms from d4a08_embed XD; thin rooms from XT, the same
space), rank among the form's defining rooms, nearest form centre, the defining room a thin room was placed beside, and
the form's changed cells the room shows. Reads no room's record. Prints JSON.

    python3 out/_analysis/d6a18_dutch_info.py > out/_analysis/d6a18_dutch_info.json
"""
import csv, json, os, subprocess, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

DUTCH = {"A": ["cirkeltrek", "indonesia", "placehearts", "mindcrack", "norway", "Goodboye"],
         "B": ["PlaceNL", "norge", "czech", "armenia", "sweden"], "C": ["blackmirror"], "D": ["greece"],
         "E": ["thenetherlands"]}
rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
TIDX = {s: i for i, s in enumerate(E.THIN)}


def vec(s):
    return E.XD[E.IDX[s]] if s in E.IDX else E.XT[TIDX[s]]


out = []
for F, subs in DUTCH.items():
    dfn = [s for s, r in rows.items() if r["form"] == F and r["role"] == "defining"]
    dd = sorted(float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[F])) for s in dfn)
    facts = json.loads(subprocess.run([sys.executable, os.path.join(AN, "d6a11_form_telling.py"), "--form", F,
                                       "--rooms", ",".join(subs), "--facts"], capture_output=True, text=True,
                                      check=True).stdout)
    ncells = len(facts["cells"])
    for rf in facts["rooms"]:
        s = rf["sub"]
        d = float(np.linalg.norm(vec(s) - E.CENTRE[F]))
        out.append({"sub": s, "form": F, "role": rows[s]["role"], "selected_changes": int(rows[s]["selected_changes"]),
                    "coded_concepts": int(rows[s]["coded_concepts"]), "distance": round(d, 4),
                    "rank_among_defining": (dd.index(d) + 1) if s in E.IDX else None,
                    "would_rank": sum(1 for x in dd if x < d) + 1, "defining_in_form": len(dfn),
                    "nearest_centre": min(E.CENTRE, key=lambda g: float(np.linalg.norm(vec(s) - E.CENTRE[g]))),
                    "reached_room": rows[s]["reached_room"] if rows[s]["role"] == "thin" else None,
                    "cells_shown": rf["shows_form_cells"], "n_cells": ncells,
                    "changes_counted": len(rf["changes"])})
print(json.dumps(out, ensure_ascii=False))
