#!/usr/bin/env python3
"""D5: count my reading of a branch's key lines. The reading file maps room:theme (the line's lift) to facet letters
and names the letters; the script checks every key line is read and counts members per facet. Prints JSON.

    python3 out/_analysis/d5_facets.py --branch F03 --reading out/_analysis/d5a03_F03_reading.json
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
ap.add_argument("--reading", required=True)
a = ap.parse_args()
rd = json.load(open(a.reading, encoding="utf-8"))
b = next(json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if json.loads(l)["id"] == a.branch)
op, el, node = b["keys"][0].split(":")
lvl = "4" if node.startswith("T4-") else "3" if node.startswith("T3-") else "dim" if node.startswith("D") else "target"
lines = [l for l in shared_lines(OUT) if l["sub"] in set(b["members"]) and l["op"] == op and l["element"] == el
         and distance.node_at(l, lvl) == node]
keys = {(l.get("lift") or [""])[0] for l in lines}
room = collections.defaultdict(set)
for k, v in rd["read"].items():
    room[k.split(":")[0]].update(v)
by = {f: sorted((s for s, fs in room.items() if f in fs), key=str.lower) for f in rd["labels"]}
print(json.dumps({"branch": a.branch, "lines": len(lines), "lifts": len(keys), "missing": sorted(keys - set(rd["read"])),
                  "extra": sorted(set(rd["read"]) - keys), "members": len(room),
                  "by_facet": {f: [rd["labels"][f], len(v), v] for f, v in by.items()},
                  "facets_per_member": dict(collections.Counter(len(fs) for fs in room.values()))}, ensure_ascii=False))
