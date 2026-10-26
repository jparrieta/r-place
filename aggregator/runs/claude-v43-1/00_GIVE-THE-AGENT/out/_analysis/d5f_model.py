#!/usr/bin/env python3
"""D5, room-form accounts, section 6: how the model runs in one form's defining rooms. Per element and arrow, the
defining members with a current-ledger line of each op (particular lines included), against the 558 defining rooms;
propose lines; the thin members' selected lines by element and op; and how many defining members lie nearer another
form's centre. Prints JSON.

    python3 out/_analysis/d5f_model.py --form A > out/_analysis/d5a36_model.json
"""
import argparse, collections, json, os, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

sys.path.insert(0, os.path.join(E.ROOT, "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

MEM = set(E.FORMS[a.form]["members"])
DEFS = [s for s in MEM if s in E.IDX]
dset, aset = set(DEFS), set(E.DEF)
thin = MEM & set(E.THIN)
el = collections.defaultdict(lambda: collections.defaultdict(set))
prop, prop_rooms, pop_prop_rooms = 0, set(), set()
for l in effective_lines(E.OUT, include_particular=True):
    s = l["sub"]
    if l.get("element"):
        el[l["element"]][l["op"]].add(s)
    if l["op"] == "propose":
        if s in aset:
            pop_prop_rooms.add(s)
        if s in dset:
            prop += 1
            prop_rooms.add(s)
rows = []
for e in sorted(el):
    for op, rooms in sorted(el[e].items()):
        rows.append({"element": e, "op": op, "form": len(rooms & dset), "pop": len(rooms & aset),
                     "form_share": round(len(rooms & dset) / len(DEFS), 3), "pop_share": round(len(rooms & aset) / len(aset), 3)})
thin_lines = collections.Counter()
thin_lines_rooms = collections.defaultdict(set)
import d4a07_features as F  # noqa: E402
for l in F.PLACED:
    if l["sub"] in thin:
        thin_lines[(l["element"], l["op"])] += 1
        thin_lines_rooms[(l["element"], l["op"])].add(l["sub"])
C = E.CENTRE
nearer = collections.Counter()
for s in DEFS:
    x = E.XD[E.IDX[s]]
    own = float(np.linalg.norm(x - C[a.form]))
    best = min(C, key=lambda g: float(np.linalg.norm(x - C[g])))
    if best != a.form:
        nearer[best] += 1
print(json.dumps({"form": a.form, "n_def": len(DEFS), "rows": rows, "propose_lines": prop, "propose_rooms": len(prop_rooms),
                  "pop_propose_rooms": len(pop_prop_rooms),
                  "thin_lines": [{"element": k[0], "op": k[1], "lines": v, "rooms": sorted(thin_lines_rooms[k], key=str.lower)}
                                 for k, v in thin_lines.most_common()],
                  "defining_nearer_other_centre": dict(nearer), "defining_nearer_total": sum(nearer.values())}, ensure_ascii=False))
