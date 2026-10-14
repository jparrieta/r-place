#!/usr/bin/env python3
"""C2c, read-only: print named fields of named arrows from out/model/arrows.jsonl, and the last history line.

    python3 out/_analysis/c2c_show_arrows.py A20 A10 [--fields bound,counterexample_response,sampled_against]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="+")
ap.add_argument("--fields", default="strength,bound,counterexample_response,sampled_against,negative_check,"
                                    "mechanism_failure_present")
ap.add_argument("--width", type=int, default=1500)
a = ap.parse_args()
A = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")))
for i in a.ids:
    r = A[i]
    print("===== %s %s -> %s" % (i, r["from"], r["to"]))
    for f in a.fields.split(","):
        v = r.get(f)
        print("  %s: %s" % (f, (json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v)[:a.width]))
H = [json.loads(l) for l in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8")]
print("history lines %d; last: %s" % (len(H), json.dumps(H[-1], ensure_ascii=False)[:a.width]))
