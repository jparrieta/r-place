#!/usr/bin/env python3
"""List episode lines that name a room the order marks unread or that is outside it.

usage: b1_episode_read_check.py <read_rooms_file> [first last]
The read-rooms file is one room per line (saturation.py order, unread rows dropped).
"""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.dirname(here)
read = {l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()}
first = int(sys.argv[2]) if len(sys.argv) > 2 else 0
last = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9

bad = 0
with open(os.path.join(out, "episodes-B1.jsonl"), encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        n = int(d["episode"][1:])
        if n < first or n > last:
            continue
        missing = [r for r in d["rooms"] if r not in read]
        if missing:
            bad += 1
            print(f"{d['episode']} ({d['leg']}): not read: {', '.join(missing)}")
print(f"{bad} episode lines name a room not read")
