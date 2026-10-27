#!/usr/bin/env python3
"""D6: write fractal-D6.jsonl lines for one dimension, from d6_fractal.py's output (the rule's relation, counts and evidence)
and my how sentences for the leaning cells (a JSON file keyed "element|form"). Untouched cells get a counted sentence.
The field "branch" holds the room form's letter, as the PI's message reads the stage file ("branch" read as room form);
"branches" lists the D4 branches that explain the form at this element, where any do. Prints the lines; append with >>.

    python3 out/_analysis/d6_fractal_write.py --rule out/_analysis/d6a01_fractal_D01.json \
        --how out/_analysis/d6a01_D01_how.json --leg D6a-01 >> out/fractal-D6.jsonl
"""
import argparse, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--rule", required=True)
ap.add_argument("--how", required=True)
ap.add_argument("--leg", required=True)
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
TAG = {"A": "d5a36", "B": "d5a37", "C": "d5a38", "D": "d5a39", "E": "d5a40", "F": "d5a41"}
names = open(os.path.join(OUT, "room-forms-names.md"), encoding="utf-8").read()
FORM_NAME = {}
for line in names.splitlines():
    m = re.match(r"\| ([A-F]) \| ([^|]+) \|", line)
    if m:
        FORM_NAME[m.group(1)] = m.group(2).strip()
assert len(FORM_NAME) == 6, FORM_NAME
rule = json.load(open(a.rule, encoding="utf-8"))
how = json.load(open(a.how, encoding="utf-8"))
inst = {}
for f in "ABCDEF":
    m = json.load(open(os.path.join(AN, "%s_model.json" % TAG[f]), encoding="utf-8"))
    for r in m["rows"]:
        if r["op"] == "instantiate":
            inst[(r["element"], f)] = (r["form"], m["n_def"], r["pop_share"])
used = set()
for r in rule["rows"]:
    key = "%s|%s" % (r["element"], r["form"])
    line = {"element": r["element"], "branch": r["form"], "level": "room form", "form_name": FORM_NAME[r["form"]],
            "relation": r["relation"], "dimension": rule["dim"], "leg": a.leg}
    if r["relation"] == "untouched":
        assert key not in how, key
        i = inst.get((r["element"], r["form"]))
        tail = (" It is instantiated in %d of %d defining rooms (%.0f per cent of the 558)." % (i[0], i[1], 100 * i[2])) if i else ""
        line["how"] = ("No op on %s meets the rule's lean in form %s (%d or more defining rooms at 1.2 times the 558's share), "
                       "so the form holds it as the model states it.%s" % (r["element"], r["form"], r["floor"], tail))
        line["evidence"] = {"codes": [], "rooms": []}
        line["branches"] = []
    else:
        h = how[key]
        used.add(key)
        line["how"] = h["how"]
        line["evidence"] = {"codes": r["codes"], "rooms": r["best"] + ([r["least"]] if r["least"] else []),
                            "best": r["best"], "least": r["least"], "deciding_ops": r["deciding_ops"],
                            "counts": {op: c["members"] for op, c in r["counts"].items()}}
        line["branches"] = h.get("branches", [])
    line["canvas"] = False
    print(json.dumps(line, ensure_ascii=False))
missing = set(how) - used
assert not missing, missing
