#!/usr/bin/env python3
"""D3c: print model/history.jsonl lines in full (id, field, leg, move, was, now) by line number. Read-only.

    python3 out/_analysis/d3c_hist_show.py --lines 135,136
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--lines", required=True)
a = ap.parse_args()
H = [json.loads(l) for l in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8") if l.strip()]
for n in [int(x) for x in a.lines.split(",")]:
    h = H[n - 1]
    print("== line %d: %s %s (%s, %s)" % (n, h.get("id"), h.get("field"), h.get("leg"), h.get("move")))
    for k in ("was", "now"):
        v = h.get(k)
        print("  %s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)[:600]))
