#!/usr/bin/env python3
"""D3b, second batch: a consistency scan of lines already ruled. Takes the re-check lines of an element and op whose
last ruling has the given decision and kind, quotes every cited concept through cite.py (each read logged by the
verb), and writes those whose quotes match --pattern, with the last ruling's reason. Reads only; rules nothing.

    python3 out/_analysis/d3b2_ruled_scan.py --element P28 --op absent --decision accept --kind none \
        --pattern '(made|created|started|set up)' --out out/_analysis/d3b2_scan_P28_abs_subs.txt
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--decision", required=True)
ap.add_argument("--kind", default="none", help="the last ruling's kind; 'none' matches a ruling with no kind")
ap.add_argument("--pattern", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
if os.path.exists(a.out):
    sys.exit("refused: %s exists" % a.out)
rx = re.compile(a.pattern, re.I)


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
lines = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
         if r.get("element") == a.element and r["op"] == a.op and r["id"] in last]
want = []
for r in lines:
    j = last[r["id"]]
    k = j.get("kind") or "none"
    if j.get("decision") == a.decision and k == a.kind:
        want.append(r)
want.sort(key=lambda r: (r["sub"].lower(), r["id"]))
W = ["%s %s lines whose last ruling is %s/%s: %d scanned; pattern %r" % (a.element, a.op, a.decision, a.kind,
                                                                           len(want), a.pattern)]
hits = 0
for r in want:
    qs = []
    for c in codes(r):
        q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", r["sub"], "--code", c],
                           cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
        qs.append(q[0] if q else "(no quote) %s/%s" % (r["sub"], c))
    if any(rx.search(q) for q in qs):
        hits += 1
        W.append("\n== %s  %s  %s" % (r["id"], r["sub"], r["op"]))
        W.append("   how: %s" % r.get("how"))
        W.append("   ruled: %s" % (last[r["id"]].get("reason") or "")[:300])
        for q in qs:
            W.append("   " + q)
W.insert(1, "%d lines match" % hits)
open(a.out, "w", encoding="utf-8").write("\n".join(W) + "\n")
print("wrote %s: %d of %d lines match" % (a.out, hits, len(want)))
