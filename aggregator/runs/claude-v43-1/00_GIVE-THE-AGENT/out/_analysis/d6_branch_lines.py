#!/usr/bin/env python3
"""D6 (QD6-001, option c): branch lines for fractal-D6.jsonl, in the stage's shape (branch F01 to F35), at the element
where a branch explains a room form. A spec file lists, per line: element, branch, form, the deciding ops, the relation
and my how sentence. Evidence is computed: the form's defining rooms that are members of the branch and hold the deciding
ops on the element (current-ledger selected lines of the D5 lines files), with the code of each room's first such line.
A spec line whose branch has no such room in the form is refused. Prints the lines; append with >>.

    python3 out/_analysis/d6_branch_lines.py --spec out/_analysis/d6a02_D01_branch_spec.json --leg D6a-02 >> out/fractal-D6.jsonl
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--dry", action="store_true", help="print the evidence counts only")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
members = {json.loads(l)["id"]: set(json.loads(l)["members"]) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8")}
lines_of = {}
for s in json.load(open(a.spec, encoding="utf-8")):
    f = s["form"]
    if f not in lines_of:
        lines_of[f] = json.load(open(os.path.join(AN, "%s_lines.json" % TAG[f]), encoding="utf-8"))["lines"]
    held = [l for l in lines_of[f] if l.get("role") == "defining" and l["element"] == s["element"] and l["op"] in s["ops"]
            and l["sub"] in members[s["branch"]]]
    rooms = sorted({l["sub"] for l in held}, key=str.lower)
    if a.dry:
        print(s["element"], s["branch"], f, len(rooms), rooms)
        continue
    assert rooms, (s["element"], s["branch"], f)
    codes = []
    for r in rooms:
        l = next(l for l in held if l["sub"] == r and l.get("codes"))
        codes.append("%s:%s" % (r, l["codes"][0]))
    print(json.dumps({"element": s["element"], "branch": s["branch"], "relation": s["relation"], "how": s["how"],
                      "evidence": {"codes": codes, "rooms": rooms}, "canvas": False, "form": f,
                      "dimension": s["dimension"], "leg": a.leg}, ensure_ascii=False))
