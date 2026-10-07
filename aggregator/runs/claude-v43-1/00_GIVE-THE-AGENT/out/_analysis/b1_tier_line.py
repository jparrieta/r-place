"""Append one tier_history.jsonl line for a move that took second-order themes out of an existing
third-order theme into another, read after the move from scheme_current.jsonl (was = now + moved).

usage: python3 out/_analysis/b1_tier_line.py --leg B1b-02 --id T3-048 --to T3-095 --moved chess:t02,leagueoflegends:t15
         --move splitting --event split --prompted "..." --why "..."
"""
import datetime
import json
import sys

argv = sys.argv[1:]


def arg(k):
    return argv[argv.index(k) + 1]


rows = {}
for l in open("out/scheme/scheme_current.jsonl"):
    r = json.loads(l)
    rows[r["theme"]] = r
src, dst = arg("--id"), arg("--to")
moved = arg("--moved").split(",")
mem = lambda t: ["%s:%s" % (m["sub"], m["theme_id"]) for m in rows[t]["members"]]
for x in moved:
    if x in mem(src) or x not in mem(dst):
        sys.exit("PROBLEM: %s is still in %s or not in %s" % (x, src, dst))
line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"), "stage": "B1",
        "leg": arg("--leg"), "tier": "third", "id": src, "move": arg("--move"), "event": arg("--event"),
        "was": {"label": rows[src]["label"], "members": mem(src) + moved},
        "now": [{"id": src, "members": mem(src)}, {"id": dst, "label": rows[dst]["label"], "members": mem(dst)}],
        "prompted_by": arg("--prompted"), "why": arg("--why")}
with open("out/tier_history.jsonl", "a") as f:
    f.write(json.dumps(line) + "\n")
print("tier_history line written for %s (%d moved to %s)" % (src, len(moved), dst))
