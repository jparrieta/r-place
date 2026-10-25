#!/usr/bin/env python3
"""D5, section 2.6: for one branch, members per element by op in the current ledger (particular lines included),
and lines without an element (propose and the like) by op. Prints JSON.

    python3 out/_analysis/d5_elements.py --branch F01
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()
b = next(json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if json.loads(l)["id"] == a.branch)
ms = set(b["members"])
el = collections.defaultdict(lambda: collections.defaultdict(set))
loose = collections.Counter()
loose_rooms = collections.defaultdict(set)
for l in effective_lines(OUT, include_particular=True):
    if l["sub"] not in ms:
        continue
    e = l.get("element")
    if e:
        el[e][l["op"]].add(l["sub"])
    else:
        loose[l["op"]] += 1
        loose_rooms[l["op"]].add(l["sub"])
rows = {e: {op: len(s) for op, s in d.items()} for e, d in sorted(el.items())}
print(json.dumps({"branch": a.branch, "n": len(ms), "elements": rows, "no_element_lines": dict(loose),
                  "no_element_rooms": {k: len(v) for k, v in loose_rooms.items()}}, ensure_ascii=False))
