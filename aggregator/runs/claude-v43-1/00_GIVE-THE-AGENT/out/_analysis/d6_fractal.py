#!/usr/bin/env python3
"""D6, fractal-D6.jsonl: the relation of each room form (A to F) to each model element and arrow, by the rule logged at
D6a-01 before it ran. For a dimension, prints one JSON object per element (or arrow) and form with the counts behind the
relation, the leaning ops, the chosen relation, evidence rooms and codes, and the how sentences of the leaning lines (for
reading). The how sentence written into fractal-D6.jsonl is mine, written after reading these.

Rule (D6a-01). On the form's defining rooms' current-ledger selected lines (the D5 facts and lines files of D5a-36 to
D5a-41): an op leans where its holders number max(5, ceil(0.10 x defining rooms)) or more and its share is 1.2 times the
558 defining rooms' share or more. relation = replaces where contradict leans; else restricts where restrict leans and
holds at least as many rooms as any leaning add-step, add-condition or link; else specifies where one of those leans;
else untouched. Evidence: up to three holders of the deciding op nearest the form's centre (best), and the farthest
holder (least), with the codes of their lines. An arrow is placed in the dimension of its consequent ('to') element.

    python3 out/_analysis/d6_fractal.py --dim D01 > out/_analysis/d6a01_fractal_D01.json
"""
import argparse, collections, json, math, os, sys
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--dim", required=True)
ap.add_argument("--add", default="", help="extra units read with this dimension (an element without a dimension, an arrow "
                                         "into it), comma-separated; logged where used")
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.path.insert(0, AN)
import d4a08_embed as E  # noqa: E402

TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
els = [json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8")]
arrows = [json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")]
dim_of = {e["id"]: (e.get("dimension") or []) for e in els}
units = [e["id"] for e in els if a.dim in dim_of[e["id"]]]
units += [x["id"] for x in arrows if a.dim in dim_of.get(x["to"], [])]
units += [u for u in a.add.split(",") if u and u not in units]
no_dim = [e["id"] for e in els if not dim_of[e["id"]]]
OPS_S = ("add-step", "add-condition", "link")
res = {"dim": a.dim, "units": units, "elements_without_dimension": no_dim, "rows": []}
for f in "ABCDEF":
    facts = json.load(open(os.path.join(AN, "%s_facts.json" % TAG[f]), encoding="utf-8"))
    lines = json.load(open(os.path.join(AN, "%s_lines.json" % TAG[f]), encoding="utf-8"))["lines"]
    n_def = facts["n_def"]
    floor = max(5, math.ceil(0.10 * n_def))
    tab = {(r["element"], r["op"]): r for r in facts["elements"]}
    cen = E.CENTRE[f]
    dist = lambda s: float(np.linalg.norm(E.XD[E.IDX[s]] - cen))  # noqa: E731
    for u in units:
        ops = {op: tab.get((u, op)) for op in OPS_S + ("restrict", "contradict")}
        lean = {op: r for op, r in ops.items() if r and r["form_def"] >= floor and (r["ratio"] or 0) >= 1.2}
        s_lean = {op: r for op, r in lean.items() if op in OPS_S}
        if "contradict" in lean:
            rel, deciding = "replaces", ["contradict"]
        elif "restrict" in lean and lean["restrict"]["form_def"] >= max([r["form_def"] for r in s_lean.values()] or [0]):
            rel, deciding = "restricts", ["restrict"]
        elif s_lean:
            rel, deciding = "specifies", sorted(s_lean, key=lambda op: -s_lean[op]["form_def"])
        else:
            rel, deciding = "untouched", []
        dl = [l for l in lines if l.get("role") == "defining" and l["element"] == u and l["op"] in deciding]
        holders = sorted({l["sub"] for l in dl}, key=dist)
        best, least = holders[:3], (holders[-1] if len(holders) > 3 else None)
        codes = []
        for s in best + ([least] if least else []):
            for l in dl:
                if l["sub"] == s and l.get("codes"):
                    codes.append("%s:%s" % (s, l["codes"][0]))
                    break
        res["rows"].append({
            "element": u, "form": f, "relation": rel, "deciding_ops": deciding, "floor": floor, "n_def": n_def,
            "counts": {op: (r and {"members": r["form_def"], "share": r["form_share"], "pop_share": r["pop_share"],
                                   "ratio": r["ratio"]}) for op, r in ops.items() if r},
            "best": best, "least": least, "codes": codes,
            "hows": [{"sub": l["sub"], "op": l["op"], "how": l["how"]} for l in sorted(dl, key=lambda l: dist(l["sub"]))]})
json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
sys.stdout.write("\n")
