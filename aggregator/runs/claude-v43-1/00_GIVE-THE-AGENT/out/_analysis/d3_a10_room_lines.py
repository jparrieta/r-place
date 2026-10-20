#!/usr/bin/env python3
"""For each room given, list every K02 and P10 line with its latest ruling (any decision).

Used at D3a-37 to see whether a room with no accepted K02 or P10 line had one rejected,
before an A10 restrict line is classed as move only or held.
Usage: python3 out/_analysis/d3_a10_room_lines.py room [room ...]
"""
import json
import os
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def jl(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


adj = {}
for a in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[a["adaptation"]] = a
rooms = set(sys.argv[1:])
rows = [l for l in jl(os.path.join(OUT, "adaptations.jsonl"))
        if l.get("element") in ("K02", "P10") and l.get("sub") in rooms]
for room in sys.argv[1:]:
    mine = sorted((l for l in rows if l.get("sub") == room), key=lambda l: l["id"])
    print("== %s: %d K02 and P10 lines" % (room, len(mine)))
    for l in mine:
        a = adj.get(l["id"], {})
        print("   %s %s %s %s: %s" % (l["id"], l["element"], l.get("op"), a.get("decision", "unruled"),
                                     a.get("reason", "")[:220]))
