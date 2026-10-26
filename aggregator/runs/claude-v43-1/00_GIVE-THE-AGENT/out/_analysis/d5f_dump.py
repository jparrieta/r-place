#!/usr/bin/env python3
"""D5, room-form accounts: print one form's defining members' selected lines for chosen element:op pairs, one page at a
time (sub|element|op|t4|id|how), for reading.

    python3 out/_analysis/d5f_dump.py --form A --keys P08:add-step,P08:add-condition --page 1
"""
import argparse, json, os

AN = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--keys", required=True)
ap.add_argument("--page", type=int, default=1)
ap.add_argument("--size", type=int, default=70)
ap.add_argument("--role", default="defining")
a = ap.parse_args()
tag = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}[a.form]
d = json.load(open(os.path.join(AN, tag + "_lines.json"), encoding="utf-8"))
keys = [tuple(k.split(":")) for k in a.keys.split(",")]
L = [l for l in d["lines"] if l["role"] == a.role and (l["element"], l["op"]) in keys]
L.sort(key=lambda l: (keys.index((l["element"], l["op"])), l["sub"].lower(), l["id"]))
lo = (a.page - 1) * a.size
print("lines", len(L), "page", a.page, "of", -(-len(L) // a.size))
for l in L[lo:lo + a.size]:
    print("%s|%s|%s|%s|%s|%s" % (l["sub"], l["element"], l["op"], l["t4"], l["id"], l["how"]))
