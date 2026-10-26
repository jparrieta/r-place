#!/usr/bin/env python3
"""D5b: the re-check readers' verdicts (rooms/<sub>/verdict-D-recheck.jsonl) for every room: rooms where any
reader said cannot-tell or does-not-compose, and whether each is in a branch. Prints JSON.

    python3 out/_analysis/d5b_recheck_uncomposed.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
inb = {}
for b in B:
    for s in b["members"]:
        inb.setdefault(s, []).append(b["id"])
rows = {}
for sub in sorted(os.listdir(os.path.join(OUT, "rooms")), key=str.lower):
    p = os.path.join(OUT, "rooms", sub, "verdict-D-recheck.jsonl")
    if not os.path.isfile(p):
        continue
    vs = [json.loads(l).get("verdict") for l in open(p, encoding="utf-8") if l.strip()]
    if any(v in ("cannot-tell", "does-not-compose") for v in vs):
        rows[sub] = {"readers": vs, "branches": inb.get(sub, [])}
print(json.dumps({"rooms": len(rows), "in_a_branch": {k: v for k, v in rows.items() if v["branches"]},
                  "both_readers_cannot_tell": sorted(k for k, v in rows.items() if v["readers"] and all(x == "cannot-tell" for x in v["readers"]))},
                 ensure_ascii=False))
