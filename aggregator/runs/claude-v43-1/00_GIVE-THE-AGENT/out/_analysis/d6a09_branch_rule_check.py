#!/usr/bin/env python3
"""D6a-09 (J's ruling 1d): which reading of the branch-naming rule each branch line of fractal-D6.jsonl stands on. The
rule as stated at D6a-02: a branch is named at a cell where it leans to the form at 1.5 or more, holds two or more of the
cell's holders, and its own key matches the cell. Readings, in order:
  'key element'       the key's element is the cell's element (the rule as stated);
  'key theme'         the key's fourth-order theme is a theme of the cell's element;
  'arrow end'         the cell is an arrow and the key's element is one of its ends;
  'antecedent theme'  the cell is an arrow and the key's fourth-order theme is a theme of its antecedent;
  'change text'       none of these: the line stands on the branch's own words of change (dict below).
A third-order key theme is lifted to its fourth-order theme by the C5 data structure (data_structure-C5.md).
Reads only; prints JSON.

    python3 out/_analysis/d6a09_branch_rule_check.py > out/_analysis/d6a09_branch_rule_check.json
"""
import collections, json, os, re

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
lines = [json.loads(l) for l in open(os.path.join(OUT, "fractal-D6.jsonl"), encoding="utf-8")]
br = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
arrows = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")}
els = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8")}
ds = open(os.path.join(OUT, "data_structure-C5.md"), encoding="utf-8").read()
T3_T4 = {m.group(1): m.group(2) for m in re.finditer(r"(T3-\d{3}) [^|]*\| (T4-\d{3})", ds)}
CHANGE_TEXT = {
    ("F11", "P01"): "F11's change: on another canvas the room recruits, builds and defends again",
    ("F12", "P01"): "F12's change: on a successor canvas the spine runs again: recruiting, choosing a site, building",
    ("F08", "P05"): "F08's change: a stale target undoes the room's own new design",
    ("F08", "A05"): "F08's change: a revision must reach the operator and the target file, not only the people",
}


def t4s(element):
    return {t if t.startswith("T4") else T3_T4.get(t) for t in (els.get(element, {}).get("tier") or [])}


out = []
for i, l in enumerate(lines, 1):
    b, cell = l["branch"], l["element"]
    keys = br[b]["keys"]
    kel = {k.split(":")[1] for k in keys}
    kt4 = {(k.split(":")[2] if k.split(":")[2].startswith("T4") else T3_T4.get(k.split(":")[2])) for k in keys}
    if cell in kel:
        how = "key element"
    elif cell in els and kt4 & t4s(cell):
        how = "key theme"
    elif cell in arrows and kel & {arrows[cell]["from"], arrows[cell]["to"]}:
        how = "arrow end"
    elif cell in arrows and kt4 & t4s(arrows[cell]["from"]):
        how = "antecedent theme"
    elif (b, cell) in CHANGE_TEXT:
        how = "change text"
    else:
        how = "UNREAD"
    out.append({"line": i, "branch": b, "cell": cell, "form": l.get("form"), "dimension": l.get("dimension"),
                "leg": l.get("leg"), "key": keys, "key_t4": sorted(x for x in kt4 if x), "reading": how,
                "note": CHANGE_TEXT.get((b, cell))})
before = [o for o in out if o["leg"] in ("D6a-01", "D6a-02", "D6a-03")]
print(json.dumps({"lines": len(out), "by_reading": dict(collections.Counter(o["reading"] for o in out)),
                  "before_D6a-04_by_reading": dict(collections.Counter(o["reading"] for o in before)),
                  "not_key_element": [o for o in out if o["reading"] != "key element"]}, ensure_ascii=False))
