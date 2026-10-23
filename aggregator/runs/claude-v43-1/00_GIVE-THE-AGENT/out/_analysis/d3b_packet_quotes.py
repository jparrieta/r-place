#!/usr/bin/env python3
"""D3b, G1b: a packet read whole with every cited concept quoted, after a draw found an unsupported line. Rebuilds the
packet as d3b_packet.py does (unruled lines of the element and op, room order, the first 100), takes lines
[start, end) of it, and prints each with its how, condition, statement or relation, and every cited concept quoted
through cite.py (each read logged by the verb). Writes the output to --out.

    python3 out/_analysis/d3b_packet_quotes.py --element R01 --op instantiate --start 0 --end 35 --out out/_analysis/d3b_pq_R01_200a.txt
"""
import argparse, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--end", type=int, required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
new = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
       if r.get("element") == a.element and r["op"] == a.op and r["id"] not in ruled]
new.sort(key=lambda r: (r["sub"].lower(), r["op"], r["id"]))
page = new[:100][a.start:a.end]
W = ["%s %s packet, lines [%d, %d) of %d, every concept quoted" % (a.element, a.op, a.start, a.start + len(page),
                                                                   len(new[:100]))]
for r in page:
    W.append("\n== %s  %s  %s%s" % (r["id"], r["sub"], r["op"], "  NONPORTABLE" if r.get("portable") is False else ""))
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
print("wrote %s: %d lines" % (a.out, len(page)))
