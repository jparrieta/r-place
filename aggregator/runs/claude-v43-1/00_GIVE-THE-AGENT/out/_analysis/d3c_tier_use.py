#!/usr/bin/env python3
"""D3c, for the re-read: each element's tier, fourth and dimension fields, with status; the fourth-order themes
(fourth/fourth.jsonl) that no standing element, and no element at all, uses through 'tier' or 'fourth'; and the
fourth-order themes figure-C5.md names as used by no element. Read-only.

    python3 out/_analysis/d3c_tier_use.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


els = jl(os.path.join(OUT, "model", "elements.jsonl"))
fourth = jl(os.path.join(OUT, "fourth", "fourth.jsonl"))
f_ids = [f.get("id") for f in fourth]
used_all, used_standing = set(), set()
for e in els:
    t = e.get("tier") or []
    t = t if isinstance(t, list) else [t]
    fo = e.get("fourth")
    fo = fo if isinstance(fo, list) else ([fo] if fo else [])
    ids = {x for x in t + fo if str(x).startswith("T4-")}
    used_all |= ids
    if e.get("status") == "standing":
        used_standing |= ids
    if e.get("status") == "candidate" or e["id"] in ("P06", "R02", "K03", "K04", "P19", "P21", "P22"):
        print("%s %s tier %s fourth %s dimension %s" % (e["id"], e.get("status"), t, fo, e.get("dimension")))
print("fourth-order themes:", len(f_ids))
print("used by no standing element:", sorted(set(f_ids) - used_standing))
print("used by no element:", sorted(set(f_ids) - used_all))
fig = open(os.path.join(OUT, "figure-C5.md"), encoding="utf-8").read()
m = re.search(r"Seven fourth-order themes are used by no element[^:]*:([^.]*)\.", fig)
print("figure-C5 names:", m.group(1).strip() if m else None)
