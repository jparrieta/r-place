"""Count phrases in the latest ruling reasons of one group's ruling files.

Files are read in the order given; a later file's ruling for an id replaces an
earlier one (so re-ruling files go last). Each --phrase is "label=regex" and is
counted over the rulings whose decision and kind match --decision and --kind.

  python3 out/_analysis/d3_reason_phrases.py --decision accept --kind specification \
      --phrase "as stated=as stated" --files f1.jsonl f2.jsonl ...
"""
import argparse
import json
import re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--files", nargs="+", required=True)
ap.add_argument("--decision", default="accept")
ap.add_argument("--kind", default="")
ap.add_argument("--phrase", action="append", default=[])
a = ap.parse_args()

latest = {}
for path in a.files:
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                r = json.loads(line)
                latest[r["adaptation"]] = r

sel = [r for r in latest.values()
       if r["decision"] == a.decision and (not a.kind or r.get("kind", "") == a.kind)]
print(f"ids ruled in these files: {len(latest)}; {a.decision}"
      f"{'/' + a.kind if a.kind else ''}: {len(sel)}")
for spec in a.phrase:
    label, rx = spec.split("=", 1)
    hits = [r["adaptation"] for r in sel if re.search(rx, r["reason"])]
    print(f"{label}: {len(hits)}")
named = Counter()
for r in sel:
    for m in re.findall(r"naming ((?:[A-Z]\d\d)(?: and [A-Z]\d\d)?)", r["reason"]):
        for x in m.split(" and "):
            named[x] += 1
print("statements named:", dict(sorted(named.items())))
