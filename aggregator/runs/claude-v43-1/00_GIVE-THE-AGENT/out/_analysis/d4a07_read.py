#!/usr/bin/env python3
"""D4a-07: read a form's members as rooms (the carried cut, placed by the whole mix). Prints, for the form's
fourth-order signature columns (nodes and links), the members' lines on each column by op and by element; then
the best fits (defining rooms with the largest share of their changes on the signature) and the misfits
(defining rooms with the smallest share, with the form whose centre is next nearest or whose signature holds a
quarter of their changes), each with up to N how sentences, those on the signature first. Read-only.

    python3 out/_analysis/d4a07_read.py --form A --n 3 --lines 2
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, AN)
sys.argv_saved = list(sys.argv)
ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--n", type=int, default=3)
ap.add_argument("--lines", type=int, default=2)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
import d4a07_features as F  # noqa: E402

T = json.load(open(os.path.join(AN, "d4a07_forms.json"), encoding="utf-8"))
C = T["cuts"][str(T["k_stab"])]
f = a.form
sig = [d["col"] for d in C["forms"][f]["sig_T4"]]
mem = [s for s, r in C["rooms"].items() if r["form"] == f]
print("== form", f, "placed", len(mem), "signature:", [d["name"] for d in C["forms"][f]["sig_T4"]])
for col in sig:
    ops, els = collections.Counter(), collections.Counter()
    for s in mem:
        for r in F.BY[s]:
            if any(c == col for c, _ in F.features(r, "T4")):
                ops[r["op"]] += 1
                els[r["element"]] += 1
    print("  column", col, "lines by op", dict(ops), "by element", els.most_common(4))


def show(s, tag):
    r = C["rooms"][s]
    print("  [%s] %s: %d changes, share on signature %.2f, secondary %s, near-equal %s" % (
        tag, s, r["changes"], r["share_own"], r["secondary"], r["near_equal_centre"]))
    lines = sorted(F.BY[s], key=lambda x: (not any(c in sig for c, _ in F.features(x, "T4")), x["id"]))
    for x in lines[:a.lines]:
        print("     - %s %s %s/%s: %s" % (x["op"], x["element"], x["lift"][1], x["lift"][2], (x.get("how") or "").strip()))


defin = [s for s in mem if C["rooms"][s]["defining"]]
for s in sorted(defin, key=lambda s: (-C["rooms"][s]["share_own"], -C["rooms"][s]["changes"], s.lower()))[:a.n]:
    show(s, "best")
for s in sorted(defin, key=lambda s: (C["rooms"][s]["share_own"], -C["rooms"][s]["changes"], s.lower()))[:a.n]:
    show(s, "misfit")
