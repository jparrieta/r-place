#!/usr/bin/env python3
"""D5, room-form accounts: the restrict lines on arrows held by one form's defining members, in a fixed order (arrow,
room, id), one page at a time, for reading and sorting (rule 4 of D5a-36). With --sort FILE[,FILE...] it joins my sort
(files of {"page": p, "codes": "..."}; F the arrow fails here, R the record cannot show it, B both, N neither) to the
lines and prints the counts by arrow as JSON.

    python3 out/_analysis/d5f_restricts.py --form A --page 1
    python3 out/_analysis/d5f_restricts.py --form A --sort out/_analysis/d5a36_sort_1.json,...
"""
import argparse, collections, json, os

AN = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("--page", type=int, default=0)
ap.add_argument("--size", type=int, default=80)
ap.add_argument("--sort", default="")
a = ap.parse_args()
tag = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}[a.form]
d = json.load(open(os.path.join(AN, tag + "_lines.json"), encoding="utf-8"))
L = sorted([l for l in d["lines"] if l["role"] == "defining" and l["element"].startswith("A") and l["op"] == "restrict"],
           key=lambda l: (int(l["element"][1:]), l["sub"].lower(), l["id"]))
if a.sort:
    codes = {}
    for p in a.sort.split(","):
        s = json.load(open(p, encoding="utf-8"))
        codes[s["page"]] = s["codes"]
    flat = "".join(codes[k] for k in sorted(codes))
    assert len(flat) == len(L), (len(flat), len(L))
    assert set(flat) <= set("FRBN"), set(flat)
    by = collections.defaultdict(collections.Counter)
    for l, c in zip(L, flat):
        by[l["element"]][c] += 1
    tot = collections.Counter(flat)
    print(json.dumps({"lines": len(L), "total": dict(tot), "by_arrow": {k: dict(v) for k, v in sorted(by.items(), key=lambda x: int(x[0][1:]))},
                      "sorted": [{"id": l["id"], "sub": l["sub"], "arrow": l["element"], "code": c} for l, c in zip(L, flat)]}, ensure_ascii=False))
else:
    lo = (a.page - 1) * a.size
    print("lines", len(L), "page", a.page, "of", -(-len(L) // a.size))
    for i, l in enumerate(L[lo:lo + a.size], lo + 1):
        print("%d|%s|%s|%s" % (i, l["element"], l["sub"], l["how"]))
