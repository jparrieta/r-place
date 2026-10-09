#!/usr/bin/env python3
"""For episode lines first..last, report listed themes that no listed room holds.

usage: b1_episode_theme_check.py <first> <last>   (episode numbers, e.g. 419 464)
"""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.dirname(here)
first, last = int(sys.argv[1]), int(sys.argv[2])

held = {}
with open(os.path.join(out, "scheme", "scheme_current.jsonl"), encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        for m in d["members"]:
            held.setdefault(m["sub"], set()).add(d["theme"])

problems = 0
with open(os.path.join(out, "episodes-B1.jsonl"), encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        n = int(d["episode"][1:])
        if n < first or n > last:
            continue
        for t in d["themes"]:
            owners = [r for r in d["rooms"] if t in held.get(r, set())]
            if not owners:
                problems += 1
                print(f"{d['episode']} {t}: held by none of {', '.join(d['rooms'])}")
print(f"{problems} themes held by no listed room")
