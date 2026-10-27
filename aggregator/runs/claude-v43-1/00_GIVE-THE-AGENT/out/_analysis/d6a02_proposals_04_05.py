#!/usr/bin/env python3
"""D6a-02: proposals PR-D6-04 (an arrow from P10 to P03: after the move, the room builds again; F09's note, D5a-09)
and PR-D6-05 (a link from K02 to P02: the room sizes its design to its hands before any loss; F34's note, D5a-34), from
the D02 form lines (d6a02_fractal_D02.json) and branch lines (fractal-D6.jsonl). Prints two JSON lines; append with >>.

    python3 out/_analysis/d6a02_proposals_04_05.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
rule = json.load(open(os.path.join(AN, "d6a02_fractal_D02.json"), encoding="utf-8"))
cell = {(r["element"], r["form"]): r for r in rule["rows"]}
bl = [json.loads(l) for l in open(os.path.join(OUT, "fractal-D6.jsonl"), encoding="utf-8")]
BASE = "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525"


def branch_line(el, br, form):
    x = [r for r in bl if r["element"] == el and r["branch"] == br and r["form"] == form]
    assert len(x) == 1, (el, br, form)
    return x[0]


p3f = cell[("P03", "F")]
assert p3f["relation"] == "specifies"
f09 = branch_line("P03", "F09", "F")
link = p3f["counts"]["link"]
p4 = {
    "id": "PR-D6-04",
    "what": "After the move, the room builds again: a new spot or a replacement plan is followed by a new start and reports "
            "of the new work.",
    "change": "An arrow from P10 (the move after a loss) to P03 (building and reporting the mark's state). With PR-D6-01 "
              "(the call returns) it would give the loss, move and building sequence the account calls ungrounded its "
              "return.",
    "why": "Form F, Moving for the spot, specifies P03 by link lines in %d of %d defining rooms (%.0f per cent, against %.0f "
           "of the 558); F09's rooms in F hold %d of them. Branch F09 (the move returns to building) stands on 55 re-check "
           "lines in 54 rooms, with no within-case dating, so the order has not been tested against a null "
           "(notes-D5.md, D5a-09)." % (link["members"], p3f["n_def"], 100 * link["share"], 100 * link["pop_share"],
                                      len(f09["evidence"]["rooms"])),
    "evidence": {"codes": (p3f["codes"] + f09["evidence"]["codes"]), "fractal_lines": ["P03|F", "P03 by F09 in F"],
                 "branch_note": "notes-D5.md, D5a-09 (F09)"},
    "affected_rooms": sorted(set(p3f["best"] + ([p3f["least"]] if p3f["least"] else []) + f09["evidence"]["rooms"]),
                             key=str.lower),
    "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-02",
}
c_ = branch_line("P02", "F34", "C")
e_ = branch_line("P02", "F34", "E")
p5 = {
    "id": "PR-D6-05",
    "what": "The room sizes its design to its hands, its space and its colours before any loss.",
    "change": "A link from K02 (the room judges it has too few hands or too little room) to P02 (the room settles what its "
              "mark shows). The model gives K02 one consequence, A10 (the move after a loss); this would add a second, "
              "before any loss.",
    "why": "Branch F34 (the design sized to the hands) found the judgement coming first and sizing the design in 10 of its "
           "22 members (notes-D5.md, D5a-34). At the form level, F34's rooms hold the P02 lines that specify the design in "
           "form C, The design reopened (%d rooms), and in form E, The sub's play, run as work (%d rooms)."
           % (len(c_["evidence"]["rooms"]), len(e_["evidence"]["rooms"])),
    "evidence": {"codes": c_["evidence"]["codes"] + e_["evidence"]["codes"], "fractal_lines": ["P02|C", "P02|E",
                 "P02 by F34 in C", "P02 by F34 in E"], "branch_note": "notes-D5.md, D5a-34 (F34)"},
    "affected_rooms": sorted(set(c_["evidence"]["rooms"] + e_["evidence"]["rooms"]), key=str.lower),
    "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-02",
}
print(json.dumps(p4, ensure_ascii=False))
print(json.dumps(p5, ensure_ascii=False))
