#!/usr/bin/env python3
"""D3 (G25's timing amendment, D3a-20): for one element's lines of one op, whatever their ruling, print each line's
cited concepts with their hours from the store (read as d3_packet.py reads labels), the span, and how many concepts
fall at or after the cut. Selection and order follow d3_packet.py (op, then room). Writes nothing.

    python3 out/_analysis/d3_op_hours.py --element P13 --op add-step --cut 61
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--cut", type=float, required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") == a.element and l.get("op") == a.op]
sel.sort(key=lambda l: (l["op"], l["sub"]))
subs = {l["sub"] for l in sel}
hour = {}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        hour[(r["sub"], r["code_id"])] = r.get("hour")
for l in sel:
    codes = [c.split(":")[-1] for c in (l.get("evidence") or {}).get("codes", [])]
    hrs = [(c, hour.get((l["sub"], c))) for c in codes]
    got = [h for _, h in hrs if h is not None]
    span = "%.1f-%.1f" % (min(got), max(got)) if got else "none"
    late = sum(1 for h in got if h >= a.cut)
    print("%s  h %s  at or after %g: %d/%d  %s" % (l["id"], span, a.cut, late, len(hrs), " ".join(
        "%s:%s" % (c, "?" if h is None else "%.1f" % h) for c, h in hrs)))
print("[%s %s: %d lines]" % (a.element, a.op, len(sel)))
