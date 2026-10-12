#!/usr/bin/env python3
"""B2b-r3-p3: after the second freeze edits, the pairs to read again: those in the new pair list
(b2_pairs_list.json) that were not in the first (b2_pairs_list_first.json), and those touching a theme the second
edits changed (T3-038, T3-070, T3-072, T3-157); printed side by side from out/scheme.jsonl. Reads only."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib

rows, _ = vlib.gate_scheme(OUT)
first = {(a, b) for _, a, b, _, _ in json.load(open(os.path.join(OUT, "_analysis", "b2_pairs_list_first.json")))}
now = [(a, b, k) for _, a, b, k, _ in json.load(open(os.path.join(OUT, "_analysis", "b2_pairs_list.json")))]
changed = {"T3-072", "T3-157"}
again = [(a, b, k) for a, b, k in now if (a, b) not in first or {a, b} & changed or {a, b} == {"T3-038", "T3-070"}]
print("%d new pairs, %d to read again in all" % (sum(1 for a, b, _ in now if (a, b) not in first), len(again)))
for a, b, k in again:
    print("## %s|%s %s%s" % (a, b, k, "  NEW" if (a, b) not in first else ""))
    print("\n".join(vlib.pair_lines(rows, a, b)))
