"""For each named third-order theme, print its label, the number of second-order themes and of rooms
placed in it, and the rooms in placement order, from scheme/scheme_current.jsonl.

usage: python3 out/_analysis/b1_kind_rooms.py T3-147 T3-177 ...
"""
import json
import sys

want = sys.argv[1:]
for line in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    if r["theme"] in want:
        rooms = []
        for m in r["members"]:
            if m["sub"] not in rooms:
                rooms.append(m["sub"])
        print("%s %s: %d second-order themes in %d rooms: %s" % (
            r["theme"], r["label"], len(r["members"]), len(rooms), ", ".join(rooms)))
