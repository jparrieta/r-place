#!/usr/bin/env python3
"""D3b: the model's history lines from one stage's legs, one short line each: time, leg, id, event, move, the
first part of the reason, and the adaptation ids that caused it. Reads only.

    python3 out/_analysis/d3b_history_brief.py --leg-prefix D3a [--width 260]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--leg-prefix", required=True)
ap.add_argument("--width", type=int, default=260)
a = ap.parse_args()
n = 0
for line in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8"):
    if not line.strip():
        continue
    d = json.loads(line)
    if not str(d.get("leg", "")).startswith(a.leg_prefix):
        continue
    n += 1
    why = (d.get("why") or "").replace("\n", " ")
    ads = d.get("adaptations") or []
    print("%s %s %s | %s | %s | %s | causes %d: %s" % (
        d.get("t", "")[:16], d.get("leg"), d.get("id"), d.get("event"), d.get("move"), why[:a.width],
        len(ads), ", ".join(ads)))
print("[%d history lines from legs %s*]" % (n, a.leg_prefix))
