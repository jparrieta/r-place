#!/usr/bin/env python3
"""D3b, G1b as G61's reading 5 sets it: the seeded draw of one packet of unruled re-check lines of one element and op.
Rebuilds the packet as d3b_packet.py does (unruled lines of the element and op, room order, offset 0, limit 100: the
lines still unruled when the packet is read), draws K of its lines by random.Random(SEED + N), where N is the packet's
label (000, 100, 200 ... in the order the element's packets are read), and prints each drawn line with every cited
concept quoted whole through cite.py (so each read is logged by the verb). Writes nothing.

    python3 out/_analysis/d3b_inst_draw.py --element P24 --op instantiate --label 0 [--k 10]
"""
import argparse, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", default="instantiate")
ap.add_argument("--label", type=int, required=True)
ap.add_argument("--k", type=int, default=10)
ap.add_argument("--seed", type=int, default=20261016)
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
page = new[:100]
rng = random.Random(a.seed + a.label)
draw = rng.sample(page, min(a.k, len(page)))
print("%s %s packet label %03d: %d lines; drawn %d by seed %d+%d" % (a.element, a.op, a.label, len(page), len(draw),
                                                                      a.seed, a.label))
for r in draw:
    print("\n== %s  %s  %s" % (r["id"], r["sub"], r["op"]))
    for k in ("condition", "statement", "relation"):
        if r.get(k):
            print("   %s: %s" % (k, r[k]))
    print("   how: %s" % r.get("how"))
    for c in codes(r):
        q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", r["sub"], "--code", c],
                           cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
        print("   " + (q[0] if q else "(no quote) %s/%s" % (r["sub"], c)))
