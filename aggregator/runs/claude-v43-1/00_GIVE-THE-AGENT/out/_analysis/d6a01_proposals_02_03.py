#!/usr/bin/env python3
"""D6a-01: proposals PR-D6-02 (the answer that asks for a task: P15 and A12) and PR-D6-03 (a proposal that is itself the
call: A02's bound), answering the D5 notes of F35 (notes-D5.md, D5a-35) and F32 (D5a-32), with the room forms' fractal
lines of D01 (d6a01_fractal_D01.json). Prints two JSON lines; append with >>.

    python3 out/_analysis/d6a01_proposals_02_03.py >> out/proposals-D6.jsonl
"""
import json, os

AN = os.path.dirname(os.path.abspath(__file__))
rule = json.load(open(os.path.join(AN, "d6a01_fractal_D01.json"), encoding="utf-8"))
cell = {(r["element"], r["form"]): r for r in rule["rows"]}
BASE = "46384686d6173fdeb4c749667478c1363e675bc6b52bb6f4fdc211d387e68525"


def ev(*keys):
    codes, rooms = [], []
    for k in keys:
        r = cell[k]
        assert r["relation"] == "restricts", k
        codes += r["codes"]
        rooms += r["best"] + ([r["least"]] if r["least"] else [])
    return codes, rooms


c2, r2 = ev(("A12", "F"))
a12f = cell[("A12", "F")]["counts"]["restrict"]
p2 = {
    "id": "PR-D6-02",
    "what": "The answer that asks for a task: a member who answers a call can join and ask where, how or what to place, "
            "or give a reason; the bare one-line join is one form of acceptance among others.",
    "change": "P15's range would include a willing answer that asks for a task, and A12's mechanism would read the bare "
              "join as the most common written acceptance, not the only one. F-023's count (25 of 31 read acceptances "
              "bare) stands.",
    "why": "Form F, Moving for the spot, restricts A12 in %d of %d defining rooms (%.0f per cent, against %.0f of the 558); "
           "its lines say answers asked where or how to help, or gave reasons. Branch F35 (the call made workable) states "
           "the same exchange from both ends: A12 restricted in 8 of its 18 members (notes-D5.md, D5a-35)."
           % (a12f["members"], cell[("A12", "F")]["n_def"], 100 * a12f["share"], 100 * a12f["pop_share"]),
    "evidence": {"codes": c2, "fractal_lines": ["A12|F"], "branch_note": "notes-D5.md, D5a-35 (F35)"},
    "affected_rooms": sorted(set(r2), key=str.lower),
    "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-01",
}
c3, r3 = ev(("A02", "D"), ("A02", "E"))
d = cell[("A02", "D")]["counts"]["restrict"]
e = cell[("A02", "E")]["counts"]["restrict"]
p3 = {
    "id": "PR-D6-03",
    "what": "A proposal that is itself the call: a member's start and the room's first call for hands can be one post or "
            "one turn.",
    "change": "A02's bound, which covers a call before the proposal, would also say that the start and the first call can "
              "coincide, so the order A02 states is not observable there; the arrow itself is unchanged.",
    "why": "Forms D, Keeping, with help or carrying on, and E, The sub's play, run as work, restrict A02 in %d and %d "
           "defining rooms; by the D5 restrict sorts, 12 of D's 12 lines and 8 of E's 11 say the start and the call share "
           "one post or turn (the sort's class neither: they coincide). Branch F32 found "
           "the same in 7 of its 8 restricting members (notes-D5.md, D5a-32)." % (d["members"], e["members"]),
    "evidence": {"codes": c3, "fractal_lines": ["A02|D", "A02|E"], "branch_note": "notes-D5.md, D5a-32 (F32)"},
    "affected_rooms": sorted(set(r3), key=str.lower),
    "base_model_version": BASE, "status": "unvalidated", "leg": "D6a-01",
}
print(json.dumps(p2, ensure_ascii=False))
print(json.dumps(p3, ensure_ascii=False))
