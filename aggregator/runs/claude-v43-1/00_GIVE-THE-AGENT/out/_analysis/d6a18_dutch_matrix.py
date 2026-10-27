#!/usr/bin/env python3
"""D6a-18, the Dutch telling: the 14 rooms side by side on every unit of the model. For each unit, how many of the 14
change it (a selected line), carry it as stated, have it absent, or have no line, and which rooms change it. Room facts
from d6a11_form_telling.py --facts (defining and thin rooms' lines). Reads no room's record. Prints JSON.

    python3 out/_analysis/d6a18_dutch_matrix.py > out/_analysis/d6a18_dutch_matrix.json
"""
import collections, json, os, subprocess, sys

AN = os.path.dirname(os.path.abspath(__file__))
DUTCH = {"A": ["cirkeltrek", "indonesia", "placehearts", "mindcrack", "norway", "Goodboye"],
         "B": ["PlaceNL", "norge", "czech", "armenia", "sweden"], "C": ["blackmirror"], "D": ["greece"],
         "E": ["thenetherlands"]}
rooms = {}
for F, subs in DUTCH.items():
    d = json.loads(subprocess.run([sys.executable, os.path.join(AN, "d6a11_form_telling.py"), "--form", F, "--rooms",
                                   ",".join(subs), "--facts"], capture_output=True, text=True, check=True).stdout)
    for rf in d["rooms"]:
        rooms[rf["sub"]] = rf
units = collections.defaultdict(lambda: {"changed": [], "carried": [], "absent": [], "no_line": [], "ledger_only": []})
for s, rf in rooms.items():
    for u in rf["changed_units"]:
        units[u]["changed"].append(s)
    for u in rf["carried_as_stated"]:
        units[u]["carried"].append(s)
    for u in rf["absent"]:
        units[u]["absent"].append(s)
    for u in rf["no_line"]:
        units[u]["no_line"].append(s)
    for u in rf["ledger_changes_not_selected"]:
        units[u]["ledger_only"].append(s)
ops = collections.Counter(c["op"] for rf in rooms.values() for c in rf["changes"])
t4 = collections.Counter(c["t4_name"] for rf in rooms.values() for c in rf["changes"])
print(json.dumps({"rooms": len(rooms), "changes": sum(len(rf["changes"]) for rf in rooms.values()),
                  "ops": dict(ops), "t4": t4.most_common(12),
                  "units": {u: {k: sorted(v) for k, v in x.items()} for u, x in
                            sorted(units.items(), key=lambda kv: -len(kv[1]["changed"]))}}, ensure_ascii=False))
