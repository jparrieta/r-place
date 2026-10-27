#!/usr/bin/env python3
"""D6a-16, form F's telling: three rooms, one per act of F's gloss, by the rule logged in the diary before any room was
read (J, 12:25 Berlin: freedom to portray what is representative; nearness to the centre not required).

Acts, each a changed cell of F with its deciding op: asking first (restrict on A04, P19 or P27); moving for the spot
(restrict on A10); building again (link on P03). A defining room holds an act where one of its selected change lines
has that unit and op (room facts from d6a11_form_telling.py --facts over all of F's defining rooms). The triple is one
holder per act, three different rooms, maximising (1) selected changes in sum, (2) F's changed cells shown together,
(3) coded concepts in sum. Reports each room's distance to F's centre, rank among the defining rooms and nearest
centre. Reads no room's record or A1 telling. Prints JSON.

    python3 out/_analysis/d6a16_select_F.py > out/_analysis/d6a16_select_F.json
"""
import csv, itertools, json, os, subprocess, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

F = "F"
rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
dfn = sorted(s for s, r in rows.items() if r["form"] == F and r["role"] == "defining")
facts = json.loads(subprocess.run([sys.executable, os.path.join(AN, "d6a11_form_telling.py"), "--form", F, "--rooms",
                                   ",".join(dfn), "--facts"], capture_output=True, text=True, check=True).stdout)
cells = [c["unit"] for c in facts["cells"]]
assert len(cells) == 14, cells
ACTS = {"asking first": ({"A04", "P19", "P27"}, "restrict"), "moving for the spot": ({"A10"}, "restrict"),
        "building again": ({"P03"}, "link")}


def dist(s, g):
    return float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g]))


order = sorted(dfn, key=lambda s: dist(s, F))
info = {}
for rf in facts["rooms"]:
    s = rf["sub"]
    info[s] = {"sub": s, "distance": round(dist(s, F), 4), "rank_by_distance": order.index(s) + 1,
               "nearest_centre": min(E.CENTRE, key=lambda g: dist(s, g)),
               "selected_changes": int(rows[s]["selected_changes"]), "coded_concepts": int(rows[s]["coded_concepts"]),
               "shows_form_cells": rf["shows_form_cells"],
               "acts": [a for a, (units, op) in ACTS.items()
                        if any(c["unit"] in units and c["op"] == op for c in rf["changes"])]}
holders = {a: sorted(s for s in dfn if a in info[s]["acts"]) for a in ACTS}
acts = [a for a in ACTS if holders[a]]
best = None
for combo in itertools.product(*[holders[a] for a in acts]):
    if len(set(combo)) < len(combo):
        continue
    key = (sum(info[s]["selected_changes"] for s in combo),
           len(set().union(*[set(info[s]["shows_form_cells"]) for s in combo])),
           sum(info[s]["coded_concepts"] for s in combo))
    if best is None or key > best[0]:
        best = (key, combo)
print(json.dumps({"form": F, "defining": len(dfn), "cells": cells,
                  "median_selected_changes": float(np.median([info[s]["selected_changes"] for s in dfn])),
                  "median_distance": round(float(np.median([info[s]["distance"] for s in dfn])), 4),
                  "holders": {a: len(v) for a, v in holders.items()}, "acts_without_holder": [a for a in ACTS
                                                                                              if not holders[a]],
                  "chosen_key": {"selected_changes": best[0][0], "cells_shown_together": best[0][1],
                                 "coded_concepts": best[0][2]},
                  "chosen": [dict(info[s], act=a) for a, s in zip(acts, best[1])],
                  "holders_by_act": {a: [info[s] for s in sorted(v, key=lambda s: -info[s]["selected_changes"])][:6]
                                     for a, v in holders.items()}}, ensure_ascii=False))
