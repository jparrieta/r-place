#!/usr/bin/env python3
"""B2a-r1: how the author's placements differ from the B1 working grouping: kinds dropped, kinds added,
and whether the primary is among the working kinds. Reads out/author_items.jsonl and out/gold_items.jsonl.
"""
import collections, json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out")
for name in ("author_items.jsonl", "gold_items.jsonl"):
    rows = [json.loads(x) for x in open(os.path.join(OUT, name), encoding="utf-8") if x.strip()]
    c = collections.Counter()
    for r in rows:
        a, w = set(r["third_order"]), set(r["working_B1"])
        dropped, added = len(w - a), len(a - w)
        c["only dropped" if dropped and not added else "only added" if added and not dropped
          else "dropped and added" if added else "same"] += 1
        c["primary among working kinds"] += r["third_order"][0] in w
    print(name, dict(c), "of", len(rows))
