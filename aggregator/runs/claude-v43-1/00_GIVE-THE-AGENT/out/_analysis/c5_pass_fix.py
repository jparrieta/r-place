#!/usr/bin/env python3
"""C5a-01: rewrite the tier_events of one pass line in account_passes.jsonl as the ids the ledgers carry (the check
resolves an event against the id or event fields of tier_history.jsonl and model/history.jsonl). The line was first
written with 'ledger:id:event' strings. Changes that one field of that one line.

    python3 out/_analysis/c5_pass_fix.py --pass N --leg LEG
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="n", type=int, required=True)
ap.add_argument("--leg", required=True)
a = ap.parse_args()
ev = []
for f in ("tier_history.jsonl", os.path.join("model", "history.jsonl")):
    for l in open(os.path.join(OUT, f), encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if r.get("leg") == a.leg and r.get("id") and str(r["id"]) not in ev:
                ev.append(str(r["id"]))
path = os.path.join(OUT, "account_passes.jsonl")
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
hit = [r for r in rows if r.get("pass") == a.n]
if len(hit) != 1:
    sys.exit("pass %d not found once" % a.n)
hit[0]["tier_events"] = ev
with open(path, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print("pass %d: %d tier events (%s)" % (a.n, len(ev), ", ".join(ev)))
