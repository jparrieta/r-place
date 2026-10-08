"""Print each second-order theme of the named rooms with the third-order themes it is placed in,
from scheme/scheme_current.jsonl.

usage: python3 out/_analysis/b1_room_placements.py <sub> [<sub> ...]
"""
import json
import sys

subs = sys.argv[1:]
placed = {}
for line in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    for m in r["members"]:
        if m["sub"] in subs:
            key = (m["sub"], m.get("theme_id", ""), m["second_order"])
            placed.setdefault(key, []).append(r["theme"])
for (sub, tid, so), themes in sorted(placed.items()):
    print("%-22s %-4s %-58s %s" % (sub, tid, so[:58], ",".join(sorted(themes))))
