"""Build c1_reassign_list.py's plan from the empties decisions (C1a-08): one entry per 'place' item.

    python3 out/_analysis/c1_empties_plan.py      writes out/_analysis/c1_empties_moves.json (refuses to overwrite)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
dec = json.load(open(os.path.join(HERE, "c1_empties_decisions.json"), encoding="utf-8"))
plan = {}
places = [d for d in dec["items"] if d["decision"] == "place"]
plan = dict((d["item"], {"theme": d["theme"], "codes": "%s=%s" % (d["theme"], d["codes"]),
                         "reason": "C1a-08 empties pass (B4 ruling re-read): " + d["basis"]}) for d in places)
pth = os.path.join(HERE, "c1_empties_moves.json")
if os.path.exists(pth):
    sys.exit("%s exists" % pth)
json.dump(plan, open(pth, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote %s: %d items" % (os.path.basename(pth), len(plan)))
