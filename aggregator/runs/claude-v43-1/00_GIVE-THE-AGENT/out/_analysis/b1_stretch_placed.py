"""Second-order themes placed, placements and unplaced lines for a stretch of the B1 order,
read from scheme/scheme_current.jsonl and unplaced-B1.jsonl.

usage: python3 out/_analysis/b1_stretch_placed.py <first_order> <last_order>
"""
import json
import subprocess
import sys

first, last = int(sys.argv[1]), int(sys.argv[2])
order = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                       capture_output=True, text=True).stdout.splitlines()
subs = [l.split("\t")[1] for l in order if l.strip() and first <= int(l.split("\t")[0]) <= last]

themes, placements = set(), 0
times = {}
per_room = {s: set() for s in subs}
for line in open("out/scheme/scheme_current.jsonl", encoding="utf-8"):
    if not line.strip():
        continue
    t = json.loads(line)
    for m in t["members"]:
        if m["sub"] in per_room:
            placements += 1
            themes.add((m["sub"], m["second_order"]))
            per_room[m["sub"]].add(m["second_order"])
            times[(m["sub"], m["second_order"])] = times.get((m["sub"], m["second_order"]), 0) + 1
unplaced = [json.loads(l) for l in open("out/unplaced-B1.jsonl", encoding="utf-8") if l.strip()]
unplaced = [u for u in unplaced if u["sub"] in per_room]
for s in subs:
    print("%s\t%d" % (s, len(per_room[s])))
print("rooms %d, second-order themes placed %d, placements %d, unplaced %d"
      % (len(subs), len(themes), placements, len(unplaced)))
print("placed once %d, twice %d, three times %d, more %d"
      % tuple(sum(1 for v in times.values() if f(v)) for f in
              (lambda v: v == 1, lambda v: v == 2, lambda v: v == 3, lambda v: v > 3)))
