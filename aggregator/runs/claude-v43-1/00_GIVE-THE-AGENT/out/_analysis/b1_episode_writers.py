"""For episode lines first..last (by number), say whether each line's evidence names a member writing
in two or more of its rooms, and print the count.

usage: python3 out/_analysis/b1_episode_writers.py 187 233
"""
import json
import re
import sys

first, last = int(sys.argv[1]), int(sys.argv[2])
yes = no = 0
for line in open("out/episodes-B1.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    n = int(r["episode"][1:])
    if not first <= n <= last:
        continue
    ev = r["evidence"]
    shared = bool(re.search(r"writes? in (both|all three|r/\w+ and r/\w+|both rooms)", ev)) and not re.search(r"no member writes in both rooms[;\",]", ev)
    if re.search(r"no member writes in both rooms", ev) and not re.search(r"\w+ writes in (both|r/)", ev.split("no member writes")[0][-200:]):
        shared = False
    print(r["episode"], "shared" if shared else "none")
    if shared:
        yes += 1
    else:
        no += 1
print("lines with a shared writer: %d of %d" % (yes, yes + no))
