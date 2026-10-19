#!/usr/bin/env python3
"""D3a-19: counts only, never a line. For every element id in adaptations.jsonl, the lines, the lines with a ruling
in adjudications.jsonl, and the legs that ruled them; then the elements with no ruling at all, ordered by lines.
Used at a leg's start to choose the next element group. Writes nothing.

    python3 out/_analysis/d3_ruled_by_element.py
"""
import collections, json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
elem = {}
for ln in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8"):
    if ln.strip():
        x = json.loads(ln)
        elem[x["id"]] = x.get("element") or "(propose)"
ruled = {}
for ln in open(os.path.join(OUT, "adjudications.jsonl"), encoding="utf-8"):
    if ln.strip():
        y = json.loads(ln)
        ruled[y["adaptation"]] = y.get("leg")
lines = collections.Counter(elem.values())
done = collections.Counter(e for i, e in elem.items() if i in ruled)
legs = collections.defaultdict(collections.Counter)
for i, e in elem.items():
    if i in ruled:
        legs[e][ruled[i]] += 1
status = {}
for ln in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8"):
    if ln.strip():
        z = json.loads(ln)
        status[z["id"]] = z.get("status")
for ln in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8"):
    if ln.strip():
        z = json.loads(ln)
        status[z["id"]] = "arrow" + ("" if z.get("status") in (None, "standing") else " " + z["status"])
print("id | status | lines | ruled | legs (latest ruling)")
for e in sorted(lines, key=lambda k: (-lines[k], k)):
    if done[e]:
        print(f"{e} | {status.get(e, '-')} | {lines[e]} | {done[e]} | {dict(legs[e])}")
print()
print("no ruling at all:")
for e in sorted(lines, key=lambda k: (-lines[k], k)):
    if not done[e]:
        print(f"  {e} | {status.get(e, '-')} | {lines[e]}")
