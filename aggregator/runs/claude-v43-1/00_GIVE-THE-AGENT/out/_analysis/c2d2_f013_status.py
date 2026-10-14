#!/usr/bin/env python3
"""C2d-02: the close-check (validate.py C2) refuses F-013's status "untested for order", since a finding's status is
standing, bounded or withdrawn. Append a line superseding F-013 (rule 14: a revision is a new line carrying the id it
supersedes) with status "standing" and the field untested "order"; the statement, evidence, bound and refuted_by are
the first line's, unchanged. Refuses to run if F-013 has already been superseded.

    python3 out/_analysis/c2d2_f013_status.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FP = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
f13 = [r for r in rows if r["id"] == "F-013"]
if len(f13) != 1:
    sys.exit("F-013 has %d lines; expected 1, not written" % len(f13))
f = dict(f13[0])
f.update({"leg": LEG, "supersedes": "F-013@%s" % f13[0]["leg"], "status": "standing", "untested": "order", "t": T,
          "why": "the close-check refuses the status 'untested for order'; the finding stands, untested for order, "
                 "as its bound says (pass 5, declaration 3: J's ruling on QC2-002)"})
with open(FP, "a", encoding="utf-8") as out:
    out.write(json.dumps(f, ensure_ascii=False) + "\n")
print("F-013 superseded: status %s, untested %s, supersedes %s" % (f["status"], f["untested"], f["supersedes"]))
