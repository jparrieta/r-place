#!/usr/bin/env python3
"""D6a-02 (QD6-001, option c): the form lines written at D6a-01 into fractal-D6.jsonl, in the shape of their own file,
fractal-forms-D6.jsonl: the room form's letter moves from 'branch' to 'form'; every other field is kept as written.
Only lines with 'level': 'room form' are moved. Prints them; redirect to out/fractal-forms-D6.jsonl.

    python3 out/_analysis/d6a02_move_form_lines.py > out/fractal-forms-D6.jsonl
"""
import json, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# corrections found at D6a-02 by d6_branch_lines.py --dry, applied in the move and recorded on the line
CORRECT = {("P01", "F"): {"branches": [], "corrected": "D6a-02: F09 removed from branches; of F09's rooms in form F only "
                                                      "r/penguins links the call, and not to a move"}}
n = 0
for raw in open(os.path.join(OUT, "fractal-D6.jsonl"), encoding="utf-8"):
    r = json.loads(raw)
    if r.get("level") != "room form":
        continue
    out = {"element": r["element"], "form": r["branch"]}
    for k, v in r.items():
        if k not in ("element", "branch"):
            out[k] = v
    out.update(CORRECT.get((r["element"], r["branch"]), {}))
    print(json.dumps(out, ensure_ascii=False))
    n += 1
assert n == 42, n
