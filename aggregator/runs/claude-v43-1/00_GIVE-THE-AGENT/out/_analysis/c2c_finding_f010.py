#!/usr/bin/env python3
"""C2c: supersede F-010 (contract rule 14: a revision is a new line carrying the id it supersedes). The reviewer's
error 5 showed A20's mechanism failing in transformers, where the first line is a member's judgment of the canvas's
worth after the close and names no flood. F-010's statement stands; its bound gains that scope condition.

    python3 out/_analysis/c2c_finding_f010.py [--write]
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
FP = os.path.join(OUT, "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
cur = [r for r in rows if r["id"] == "F-010"][-1]
new = dict(cur)
new.update({
    "stage": "C2", "leg": LEG, "supersedes": "F-010@%s" % cur["leg"], "status": "bounded",
    "bound": cur["bound"] + (" A member's judgment of the canvas's worth after the close answers no flood: in "
                             "transformers (sampled) the order holds and the first line, at h80.40, names no flood, so "
                             "the mechanism does not operate there (the reviewer's error 5, C2c)."),
    "refuted_by": ["a room where the host sub's first line answers no call or flood while the canvas runs"],
    "why": ("C2c, the reviewer's error 5: A20's sampled room transformers was recorded as holding though its first line "
            "names no flood, A20's failure clause; the order holds and the mechanism fails there. The statement stands "
            "on 132 of 155 rooms; the bound is narrowed to lines drawn while the canvas runs."),
    "t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
})
print(json.dumps(new, ensure_ascii=False)[:1600])
if "--write" in sys.argv:
    with open(FP, "a", encoding="utf-8") as f:
        f.write(json.dumps(new, ensure_ascii=False) + "\n")
    print("appended; findings.jsonl now %d lines" % (len(rows) + 1))
