#!/usr/bin/env python3
"""D3a-46, read-only: count the adaptations lines that have no ruling in adjudications.jsonl, by element (a dimension,
a candidate, or none for `propose` lines) and op, so that the head's next comparison names the groups still open.
Prints counts only. Writes nothing.

  python3 out/_analysis/d3_unruled_by_element.py
"""
import json
from collections import Counter

ruled = set()
for l in open("out/adjudications.jsonl", encoding="utf-8"):
    if l.strip():
        ruled.add(json.loads(l)["adaptation"])
by_el, by_op, total = Counter(), Counter(), 0
for l in open("out/adaptations.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    d = json.loads(l)
    total += 1
    if d["id"] in ruled:
        continue
    by_el[d.get("element") or "(none)"] += 1
    by_op[d["op"]] += 1
print("adaptations lines: %d; ruled: %d; unruled: %d" % (total, total - sum(by_el.values()), sum(by_el.values())))
print("unruled by op:", dict(sorted(by_op.items())))
print("unruled by element:", dict(sorted(by_el.items(), key=lambda x: (-x[1], x[0]))))
