#!/usr/bin/env python3
"""D3 (G25's timing amendment, D3a-20): for one element's lines whose current ruling is accept with kind
specification, print the lines whose cited concepts fall on both sides of an hour cut (--mode mixed), or only
before it (--mode early). Each concept is printed with its hour and its first-order label from the store, read
as d3_packet.py reads them. Selection and order follow d3_packet.py (op, then room). Writes nothing.

    python3 out/_analysis/d3_mixed_hours.py --element P13 --cut 61 --mode mixed --ops instantiate,restrict,contradict
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--cut", type=float, required=True)
ap.add_argument("--mode", choices=["mixed", "early"], required=True)
ap.add_argument("--ops", required=True)
a = ap.parse_args()
ops = set(a.ops.split(","))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") == a.element and l.get("op") in ops]
sel.sort(key=lambda l: (l["op"], l["sub"]))
adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
subs = {l["sub"] for l in sel}
info = {}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        info[(r["sub"], r["code_id"])] = (r.get("hour"), r.get("first_order"))
n_spec = n_shown = 0
for l in sel:
    r = adj.get(l["id"], {})
    if r.get("decision") != "accept" or r.get("kind") != "specification":
        continue
    n_spec += 1
    codes = [c.split(":")[-1] for c in (l.get("evidence") or {}).get("codes", [])]
    hrs = [(c,) + info.get((l["sub"], c), (None, "?")) for c in codes]
    got = [h for _, h, _ in hrs if h is not None]
    if not got:
        continue
    early = min(got) < a.cut
    late = max(got) >= a.cut
    if (a.mode == "mixed" and early and late) or (a.mode == "early" and early and not late):
        n_shown += 1
        print("== %s  %s" % (l["id"], l["op"]))
        for c, h, lab in hrs:
            print("   %s %s  %s" % (c, "h?" if h is None else "h%.1f" % h, lab))
print("[%s %s: %d accepted specifications read; %d shown (cut %g, mode %s)]" % (
    a.element, a.ops, n_spec, n_shown, a.cut, a.mode))
