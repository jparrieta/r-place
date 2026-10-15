#!/usr/bin/env python3
"""C5a-03: after a C5 cut is reversed (c5_restore.py), record the reversal on the pass line that made the cut, so the
line stays true and the check (a cut element must not stand) reads it: the element leaves `elements_cut` and goes to
`cut_then_reversed` with the pass that reversed it and why. Changes those two fields of that one line.

    python3 out/_analysis/c5_pass_cut_fix.py --pass N --id ID --reversed-in "pass M (LEG)" --why "..."
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="n", type=int, required=True)
ap.add_argument("--id", required=True)
ap.add_argument("--reversed-in", required=True)
ap.add_argument("--why", required=True)
a = ap.parse_args()
path = os.path.join(ROOT, "out", "account_passes.jsonl")
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
hit = [r for r in rows if r.get("pass") == a.n]
if len(hit) != 1 or a.id not in (hit[0].get("elements_cut") or []):
    sys.exit("pass %d not found once, or it did not cut %s" % (a.n, a.id))
hit[0]["elements_cut"] = [e for e in hit[0]["elements_cut"] if e != a.id]
hit[0].setdefault("cut_then_reversed", []).append({"id": a.id, "reversed_in": a.reversed_in, "why": a.why})
with open(path, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print("pass %d: %s moved from elements_cut to cut_then_reversed" % (a.n, a.id))
