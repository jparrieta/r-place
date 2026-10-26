#!/usr/bin/env python3
"""D5: every arrow's restrict count among a branch's members and the within-size pool (as d5_within.py draws
it: rooms outside the branch with at least the members' median coded concepts), particular lines included.
Prints one line per arrow: arrow, members, pool, excess.

    python3 out/_analysis/d5_arrow_restrict.py --branch F33
"""
import argparse, collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()
OUT = os.path.join(ROOT, "out")
bs = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()}
ms = set(bs[a.branch]["members"])
c = collections.Counter(json.loads(l)["sub"] for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"))
med = statistics.median(c[s] for s in ms)
pool = {s for s in c if s not in ms and c[s] >= med}
by = collections.defaultdict(set)
for l in effective_lines(OUT, include_particular=True):
    if (l.get("element") or "").startswith("A") and l["op"] == "restrict":
        by[l["element"]].add(l["sub"])
for el in sorted(by):
    m, p = len(by[el] & ms), len(by[el] & pool)
    print(el, m, p, round(m / len(ms) - p / len(pool), 3))
