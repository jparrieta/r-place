#!/usr/bin/env python3
"""D3b: the named re-check lines with every cited concept quoted, for lines in a packet whose labels do not show the
element plainly. Takes a file of ids (one a line), finds each in adaptations-recheck.jsonl, and prints it with its how,
condition, statement or relation, and every cited concept quoted through cite.py (each read logged by the verb).
Writes the output to --out.

    python3 out/_analysis/d3b_ids_quotes.py --ids out/_analysis/d3b_ids_K05_100.txt --out out/_analysis/d3b_iq_K05_100.txt
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--ids", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


want = [l.strip() for l in open(a.ids, encoding="utf-8") if l.strip()]
byid = {r["id"]: r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl")) if r["id"] in set(want)}
miss = [i for i in want if i not in byid]
if miss:
    sys.exit("not in adaptations-recheck.jsonl: %s" % ", ".join(miss))
W = ["%d named re-check lines, every concept quoted (from %s)" % (len(want), os.path.basename(a.ids))]
for i in want:
    r = byid[i]
    W.append("\n== %s  %s  %s  %s%s" % (r["id"], r["sub"], r.get("element"), r["op"],
                                        "  NONPORTABLE" if r.get("portable") is False else ""))
    for k in ("condition", "statement", "relation"):
        if r.get(k):
            W.append("   %s: %s" % (k, r[k]))
    W.append("   how: %s" % r.get("how"))
    for c in codes(r):
        q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", r["sub"], "--code", c],
                           cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
        W.append("   " + (q[0] if q else "(no quote) %s/%s" % (r["sub"], c)))
if os.path.exists(a.out):
    sys.exit("refused: %s exists; packets that rulings cite are never overwritten" % a.out)
open(a.out, "w", encoding="utf-8").write("\n".join(W) + "\n")
print("wrote %s: %d lines" % (a.out, len(want)))
