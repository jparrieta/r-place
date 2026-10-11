#!/usr/bin/env python3
"""B1e: how many second-order themes two third-order themes share, and their labels on request.

Usage: python3 out/_analysis/b1e_pair_overlap.py T3-005 T3-021 [--label sub:tNN ...]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


args = sys.argv[1:]
labels = args[args.index("--label") + 1:] if "--label" in args else []
ids = args[:args.index("--label")] if "--label" in args else args
cur = {r["theme"]: r for r in jl(os.path.join(ROOT, "out", "scheme", "scheme_current.jsonl"))}
if len(ids) == 2:
    a = {(m["sub"], m["second_order"]) for m in cur[ids[0]]["members"]}
    b = {(m["sub"], m["second_order"]) for m in cur[ids[1]]["members"]}
    print("%s %d, %s %d, both %d, either %d, share of either holding both %.3f" % (
        ids[0], len(a), ids[1], len(b), len(a & b), len(a | b), len(a & b) / len(a | b)))
if labels:
    th = {(r["sub"], r["theme_id"]): r["second_order"] for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
    for x in labels:
        s, t = x.split(":")
        print("%s %s: %s" % (s, t, th.get((s, t), "?")))
