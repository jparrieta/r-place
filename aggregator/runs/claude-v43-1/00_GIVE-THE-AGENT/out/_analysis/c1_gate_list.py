"""List the amended gates of gate_history.jsonl, numbered as gate:<n> (read-only).

For a discriminators field, only the questions whose text changed are shown.

    python3 out/_analysis/c1_gate_list.py [--theme T3-017,T3-095] [--width 300]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

ap = argparse.ArgumentParser()
ap.add_argument("--theme", default="")
ap.add_argument("--width", type=int, default=300)
a = ap.parse_args()
want = set(x for x in a.theme.split(",") if x)


def clip(s):
    s = " ".join(str(s).split())
    return s if len(s) <= a.width else s[:a.width] + " ..."


with open(os.path.join(OUT, "gate_history.jsonl"), encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

n = 0
while n < len(rows):
    r = rows[n]
    n += 1
    if want and r.get("theme") not in want:
        continue
    print("gate:%d  %s  %s  (%s)" % (n, r.get("theme"), r.get("field"), r.get("leg")))
    was, now = r.get("was"), r.get("now")
    if r.get("field") == "discriminators" and isinstance(was, list) and isinstance(now, list):
        old = dict((d.get("vs"), d.get("question")) for d in was)
        changed = [d for d in now if old.get(d.get("vs")) != d.get("question")]
        print("  changed questions: " + "; ".join("vs %s: %s" % (d.get("vs"), clip(d.get("question"))) for d in changed))
    else:
        print("  now: " + clip(now))
    print("  why: " + clip(r.get("why")))
