#!/usr/bin/env python3
"""D6a-17, the second round of room choices and the good-old room (J, 27 Oct 14:03 and 15:23 Berlin), by the rules
logged in the diary before this ran.

Round 2: a defining room shows a form cell where one of its selected change lines has the cell's unit and one of its
deciding ops. B's parts are its three facets (a selected line at T4-010 chat, T4-009 scripts, T4-020 raids); D's are
its three kept leaves (D.1, D.2.1, D.2.2, by address). For B and D the three rooms are one holder per part, three
different rooms; for A, C, E and F any three different defining rooms. The triple maximises (1) the form's cells shown
jointly, (2) the sum of cells shown by each room, (3) the sum of selected changes, (4) the sum of coded concepts.

Good old: candidates hold every column of the form's change signature (the allocation's T4 change columns, d4a08_embed
CC) and lie nearer the form's centre than any other form's; ranked by cells shown, then distance, then selected
changes. If none holds every column, those holding the most columns are the candidates.

Reads no room's record or A1 telling. Prints JSON.

    python3 out/_analysis/d6a17_select_r2.py > out/_analysis/d6a17_select_r2.json
"""
import csv, itertools, json, os, subprocess, sys
import numpy as np

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

rows = {r["room"]: r for r in csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"),
                                              delimiter="\t")}
t4name = {json.loads(l)["id"]: json.loads(l)["name"] for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"),
                                                                       encoding="utf-8") if l.strip()}
t4id = {v: k for k, v in t4name.items()}
alloc = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "room-forms-D4a08c.jsonl"), encoding="utf-8")
         if l.strip()}
ROUND1 = {"A": ["FloydVsVoid", "prequelmemes", "theexpanse"], "B": ["dwarffortress", "uofm", "ockytop"],
          "C": ["suomi", "gatech", "bardmains"], "D": ["rotmg", "bindingofisaac", "romania"],
          "E": ["fivenightsatfreddys", "warframe", "stevenuniverse"], "F": ["sips", "planetside", "nbaspurs"]}
FACETS = {"chat": "T4-010", "scripts": "T4-009", "raids": "T4-020"}
LEAVES = ["D.1", "D.2.1", "D.2.2"]


def dist(s, g):
    return float(np.linalg.norm(E.XD[E.IDX[s]] - E.CENTRE[g]))


def sig_col(name):
    if " > " in name:
        a, b = name.split(" > ")
        return "%s>%s" % (t4id[a], t4id[b])
    return t4id[name]


out = {}
for F in "ABCDEF":
    dfn = sorted(s for s, r in rows.items() if r["form"] == F and r["role"] == "defining")
    facts = json.loads(subprocess.run([sys.executable, os.path.join(AN, "d6a11_form_telling.py"), "--form", F,
                                       "--rooms", ",".join(dfn), "--facts"], capture_output=True, text=True,
                                      check=True).stdout)
    cells = [c["unit"] for c in facts["cells"]]
    bit = {u: 1 << i for i, u in enumerate(cells)}
    order = sorted(dfn, key=lambda s: dist(s, F))
    sig = [sig_col(s["name"]) for s in alloc[F]["change_signature_T4"]]
    info = {}
    for rf in facts["rooms"]:
        s = rf["sub"]
        t4s = {c["t4"] for c in rf["changes"]}
        addr = rows[s]["address"].split("/")[0]
        info[s] = {"sub": s, "distance": round(dist(s, F), 4), "rank_by_distance": order.index(s) + 1,
                   "nearest_centre": min(E.CENTRE, key=lambda g: dist(s, g)),
                   "selected_changes": int(rows[s]["selected_changes"]),
                   "coded_concepts": int(rows[s]["coded_concepts"]),
                   "shows": rf["shows_form_cells"], "n_shows": len(rf["shows_form_cells"]),
                   "mask": sum(bit[u] for u in rf["shows_form_cells"]),
                   "facets": [f for f, t in FACETS.items() if t in t4s] if F == "B" else None,
                   "leaf": next((lf for lf in LEAVES if addr == lf or addr.startswith(lf + ".")), None)
                   if F == "D" else None,
                   "signature_held": [c for c in sig if E.CC[s]["T4"].get(c, 0) > 0]}

    def key(combo):
        m = 0
        for s in combo:
            m |= info[s]["mask"]
        return (bin(m).count("1"), sum(info[s]["n_shows"] for s in combo),
                sum(info[s]["selected_changes"] for s in combo), sum(info[s]["coded_concepts"] for s in combo),
                tuple(sorted((x.lower() for x in combo), reverse=True)))

    if F == "B":
        parts = list(FACETS)
        pools = [[s for s in dfn if p in info[s]["facets"]] for p in parts]
    elif F == "D":
        parts = LEAVES
        pools = [[s for s in dfn if info[s]["leaf"] == p] for p in parts]
    else:
        parts = None
        pools = None
    best = None
    if parts:
        for combo in itertools.product(*pools):
            if len(set(combo)) < 3:
                continue
            k = key(combo)
            if best is None or k > best[0]:
                best = (k, combo)
    else:
        # every triple of the form's defining rooms is scored (at most 135 rooms, about 400,000 triples)
        for combo in itertools.combinations(dfn, 3):
            k = key(combo)
            if best is None or k > best[0]:
                best = (k, combo)
    chosen = [dict(info[s], part=(parts[i] if parts else None)) for i, s in enumerate(best[1])]
    # good old
    nmax = max(len(info[s]["signature_held"]) for s in dfn)
    cand = [s for s in dfn if len(info[s]["signature_held"]) == len(sig) and info[s]["nearest_centre"] == F]
    fallback = False
    if not cand:
        fallback = True
        cand = [s for s in dfn if len(info[s]["signature_held"]) == nmax and info[s]["nearest_centre"] == F]
    cand.sort(key=lambda s: (-info[s]["n_shows"], info[s]["distance"], -info[s]["selected_changes"]))
    out[F] = {"form": F, "defining": len(dfn), "cells": cells, "signature_columns": sig,
              "median_selected_changes": float(np.median([info[s]["selected_changes"] for s in dfn])),
              "median_cells_shown": float(np.median([info[s]["n_shows"] for s in dfn])),
              "parts": parts, "pool_sizes": [len(p) for p in pools] if pools else None,
              "round2": chosen, "round2_key": {"cells_jointly": best[0][0], "cells_summed": best[0][1],
                                               "selected_changes": best[0][2], "coded_concepts": best[0][3]},
              "round2_not_shown": [u for u in cells if not any(u in x["shows"] for x in chosen)],
              "round1": [info[s] for s in ROUND1[F]],
              "round1_cells_jointly": len(set().union(*[set(info[s]["shows"]) for s in ROUND1[F]])),
              "good_old_candidates": len(cand), "good_old_fallback": fallback,
              "good_old": info[cand[0]] if cand else None, "good_old_next": [info[s] for s in cand[1:4]],
              "top_by_cells_shown": [info[s] for s in sorted(dfn, key=lambda s: (-info[s]["n_shows"],
                                                                                   info[s]["distance"]))[:5]]}
    for x in out[F]["round2"] + out[F]["round1"] + out[F]["good_old_next"] + out[F]["top_by_cells_shown"] + (
            [out[F]["good_old"]] if out[F]["good_old"] else []):
        x.pop("mask", None)
print(json.dumps(out, ensure_ascii=False))
