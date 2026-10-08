"""Check every concept id named in a leg's bag records (multiplacement_log.jsonl, item_is_a_bag)
against the second-order theme the bag is for, reading each room's full concept listing.
Ranges written as 'c0014 to c0020' are checked at both ends only.

usage: python3 out/_analysis/b1_check_bags.py <leg> [<sub> ...]
"""
import json
import re
import subprocess
import sys

leg = sys.argv[1]
only = set(sys.argv[2:])
bags = []
for line in open("out/multiplacement_log.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    r = json.loads(line)
    if r.get("leg") == leg and r.get("item_is_a_bag") and (not only or r["sub"] in only):
        bags.append(r)

theme_of = {}
for sub in sorted({b["sub"] for b in bags}):
    out = subprocess.run(["python3", "out/_analysis/b1_room_codes.py", sub],
                         capture_output=True, text=True).stdout
    for row in out.splitlines():
        parts = row.split()
        if len(parts) >= 3 and re.match(r"^c\d{4}$", parts[0]):
            theme_of[(sub, parts[0])] = parts[2]

problems = 0
for b in bags:
    for cid in sorted(set(re.findall(r"c\d{4}", b.get("why_not_one", "")))):
        t = theme_of.get((b["sub"], cid))
        if t != b["theme_id"]:
            problems += 1
            print("PROBLEM %s %s: %s is under %s" % (b["sub"], b["theme_id"], cid, t))
print("%d bags checked, %d problems" % (len(bags), problems))
