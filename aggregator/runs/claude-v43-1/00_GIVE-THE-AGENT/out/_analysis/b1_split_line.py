"""Append one tier_history.jsonl line for a split of an existing third-order theme into itself and
several new ones, read after the moves from scheme_current.jsonl. `was` is the source's members now
plus those taken out of it (--moved); `now` lists the source and every new theme with its members.
Members that stayed in the source and were also placed in a new theme show in both.

usage: python3 out/_analysis/b1_split_line.py --leg B1b-06 --id T3-010 --to T3-149,T3-150,T3-151
         --moved rutgers:t14,lakers:t12 --move splitting --prompted "..." --why "..."
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
src, dsts = arg("--id"), arg("--to").split(",")
moved = arg("--moved").split(",")
mem = lambda t: ["%s:%s" % (m["sub"], m["theme_id"]) for m in rows[t]["members"]]
for x in moved:
    if x in mem(src) or not any(x in mem(d) for d in dsts):
        sys.exit("PROBLEM: %s is still in %s or in none of %s" % (x, src, ",".join(dsts)))
line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"), "stage": "B1",
        "leg": arg("--leg"), "tier": "third", "id": src, "move": arg("--move"), "event": "split",
        "was": {"label": rows[src]["label"], "members": mem(src) + moved},
        "now": [{"id": src, "members": mem(src)}] +
               [{"id": d, "label": rows[d]["label"], "members": mem(d)} for d in dsts],
        "prompted_by": arg("--prompted"), "why": arg("--why")}
with open("out/tier_history.jsonl", "a") as f:
    f.write(json.dumps(line) + "\n")
print("tier_history split line written for %s: %d stay, %d moved out, new %s" %
      (src, len(mem(src)), len(moved), ", ".join("%s (%d)" % (d, len(mem(d))) for d in dsts)))
