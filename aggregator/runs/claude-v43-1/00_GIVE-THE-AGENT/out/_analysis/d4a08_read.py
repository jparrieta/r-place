#!/usr/bin/env python3
"""D4a-08: read a form of the carried cut (d4a08e_forms.json) as rooms: the members' lines on each change-signature
column by op and element, then the best fits (defining rooms, largest share of changes on the change signature,
then most codes) with up to N how sentences, those on the signature first. Read-only.

    python3 out/_analysis/d4a08_read.py --form B --n 2 --lines 1
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--n", type=int, default=2)
ap.add_argument("--lines", type=int, default=1)
ap.add_argument("--k", default="5")
a = ap.parse_args()
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
import d4a07_features as F  # noqa: E402

T = json.load(open(os.path.join(AN, "d4a08e_forms.json"), encoding="utf-8"))
C = T["cuts"][a.k]
f = a.form
sig = [d["col"] for d in C["forms"][f]["sig_T4"]]
mem = [s for s, r in C["rooms"].items() if r["form"] == f]
print("== form", f, "placed", len(mem), "change signature", [d["name"] for d in C["forms"][f]["sig_T4"]])
for col in sig:
    ops, els = collections.Counter(), collections.Counter()
    for s in mem:
        for r in F.BY[s]:
            if any(c == col for c, _ in F.features(r, "T4")):
                ops[r["op"]] += 1
                els[r["element"]] += 1
    print("  column", col, dict(ops), els.most_common(4))
D = [s for s in mem if C["rooms"][s]["defining"]]
for s in sorted(D, key=lambda s: (-C["rooms"][s]["share_own"], -C["rooms"][s]["codes"], s.lower()))[:a.n]:
    r = C["rooms"][s]
    print("  [best] %s: %d changes, %d codes, share on signature %.2f" % (s, r["changes"], r["codes"], r["share_own"]))
    lines = sorted(F.BY[s], key=lambda x: (not any(c in sig for c, _ in F.features(x, "T4")), x["id"]))
    for x in lines[:a.lines]:
        print("     - %s %s %s/%s: %s" % (x["op"], x["element"], x["lift"][1], x["lift"][2], (x.get("how") or "").strip()))
