#!/usr/bin/env python3
"""C5c-02: the element membership for the order tests after Stigmergy's recut (the three-coder rule, logged before the
tally): T3-041 and T3-060 leave P03 (building and reporting the mark) for P02 (settling what the mark shows), since they
leave Stigmergy (T4-007) for Collective representation (T4-006). Every other element is as in c2_elements_p4.json.
Writes out/_analysis/c2_elements_c5c2.json; refuses to overwrite it.

    python3 out/_analysis/c5c2_elements.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
DEST = os.path.join(AN, "c2_elements_c5c2.json")
if os.path.exists(DEST):
    sys.exit("c2_elements_c5c2.json exists; not rewritten")
src = json.load(open(os.path.join(AN, "c2_elements_p4.json"), encoding="utf-8"))
MOVE = ["T3-041", "T3-060"]
for e in src["elements"]:
    if e["id"] == "P03":
        assert all(t in e["themes"] for t in MOVE)
        e["themes"] = [t for t in e["themes"] if t not in MOVE]
    if e["id"] == "P02":
        e["themes"] = e["themes"] + [t for t in MOVE if t not in e["themes"]]
src["about"] = ("C5c-02 element membership for the order tests (c5c2_elements.py): c2_elements_p4.json with T3-041 and "
                "T3-060 moved from P03 to P02, after Stigmergy's recut by three codings")
json.dump(src, open(DEST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote %s: P03 %s; P02 %s" % (DEST, [e for e in src["elements"] if e["id"] == "P03"][0]["themes"],
                                       [e for e in src["elements"] if e["id"] == "P02"][0]["themes"]))
