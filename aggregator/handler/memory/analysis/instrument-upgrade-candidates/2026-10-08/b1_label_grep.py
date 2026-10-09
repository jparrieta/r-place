"""Print every placed second-order theme whose label matches a regex, with the third-order
themes it is placed in, from scheme/scheme_current.jsonl.

usage: python3 out/_analysis/b1_label_grep.py "<regex>"
"""
import json
import re
import sys

rx = re.compile(sys.argv[1], re.I)
placed = {}
for line in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    for m in r["members"]:
        if rx.search(m["second_order"]):
            key = (m["sub"], m.get("theme_id", ""), m["second_order"])
            placed.setdefault(key, []).append(r["theme"])
for (sub, tid, so), themes in sorted(placed.items()):
    print("%-22s %-4s %-58s %s" % (sub, tid, so[:58], ",".join(sorted(themes))))
print("%d second-order themes" % len(placed))
