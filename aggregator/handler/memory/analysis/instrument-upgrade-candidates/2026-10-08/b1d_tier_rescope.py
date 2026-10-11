"""Append one tier_history.jsonl line for a third-order theme whose scope is widened: members are added
from other themes or as additional placements, and the label is to change at B1e. Read after the moves
from scheme_current.jsonl (was = now minus the added members).

usage: python3 out/_analysis/b1d_tier_rescope.py --leg B1d-01 --id T3-188 --added polska:t10,PlaceNL:t11
         --prompted "..." --why "..." [--label-to "..."]
"""
import datetime
import json
import sys

argv = sys.argv[1:]


def arg(k, default=None):
    return argv[argv.index(k) + 1] if k in argv else default


rows = {}
for l in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        rows[r["theme"]] = r
tid = arg("--id")
added = arg("--added").split(",")
now = ["%s:%s" % (m["sub"], m["theme_id"]) for m in rows[tid]["members"]]
missing = [x for x in added if x not in now]
if missing:
    sys.exit("PROBLEM: not in %s: %s" % (tid, ", ".join(missing)))
was = [x for x in now if x not in added]
line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"), "stage": "B1",
        "leg": arg("--leg"), "tier": "third", "id": tid, "move": "relating or contrasting", "event": "rescoped",
        "was": {"label": rows[tid]["label"], "members": was},
        "now": [{"id": tid, "label": rows[tid]["label"], "label_at_B1e": arg("--label-to", rows[tid]["label"]),
                 "members": now}],
        "prompted_by": arg("--prompted"), "why": arg("--why")}
with open("out/tier_history.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print("tier_history line written for %s: rescoped, %d members before, %d now" % (tid, len(was), len(now)))
