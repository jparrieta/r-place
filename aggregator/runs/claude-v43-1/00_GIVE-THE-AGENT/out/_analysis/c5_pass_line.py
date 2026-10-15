#!/usr/bin/env python3
"""C5: append one line to account_passes.jsonl for a pass, with its tier events read from tier_history.jsonl and
model/history.jsonl (every line written in the given leg), so the ids are read, not typed. Refuses if the pass number
is already in the file.

    python3 out/_analysis/c5_pass_line.py --pass N --leg LEG --what "..." --sketches K --cut "id,id" --criterion prefer|reject|no-change
"""
import argparse, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="n", type=int, required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--what", required=True)
ap.add_argument("--sketches", type=int, required=True)
ap.add_argument("--cut", default="")
ap.add_argument("--criterion", required=True, choices=["prefer", "reject", "no change"])
a = ap.parse_args()
path = os.path.join(OUT, "account_passes.jsonl")
have = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()] if os.path.exists(path) else []
if any(r.get("pass") == a.n for r in have):
    sys.exit("pass %d is already in account_passes.jsonl" % a.n)
ev = []
for f, tag in (("tier_history.jsonl", "tier_history"), (os.path.join("model", "history.jsonl"), "model/history")):
    for l in open(os.path.join(OUT, f), encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if r.get("leg") == a.leg and r.get("id") and str(r["id"]) not in ev:
                ev.append(str(r["id"]))  # the check resolves a tier event against the ledgers' id or event fields
line = {"pass": a.n, "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "leg": a.leg,
        "what_changed": a.what, "tier_events": ev, "sketches_tried": a.sketches,
        "elements_cut": [x for x in a.cut.split(",") if x], "criterion_says": a.criterion}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print("pass %d written with %d tier events" % (a.n, len(ev)))
