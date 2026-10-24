#!/usr/bin/env python3
"""D4a-01, rule 14: re-examine the findings that touch the two amendments, in the same act. F-024 (P05) and F-017
(A11) each get a new findings.jsonl line, stage D4, leg D4a-01, carrying the bare id it supersedes, copied from its
last line with the changed fields only. F-024: the statement says the scope is now in P05's words, after the
freeze, not re-checked. F-017: its clause '(A11, theorised)' becomes the withdrawal. Refuses if the clause is not
found word for word. Without --write it prints the changed fields.

    python3 out/_analysis/d4a01_findings.py [--write]
"""
import argparse, copy, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
rows = [json.loads(l) for l in open(F, encoding="utf-8") if l.strip()]
last = {}
for r in rows:
    last[r["id"]] = r
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new = []
f24 = copy.deepcopy(last["F-024"])
assert f24["status"] == "bounded" and f24["leg"] == "D3c"
f24.update({"stage": "D4", "leg": "D4a-01", "t": t, "supersedes": "F-024"})
f24["statement"] = last["F-024"]["statement"] + (
    " At D4a-01 the scope is written into P05's own words: its statement gains 'This holds where the keepers can "
    "learn of a planned change only by being told, and no informed member holds it.', its status is bounded, and "
    "its bound names the six rooms and the three. That amendment was made after the D3 freeze (46384686) and is not "
    "re-checked; the frozen statement stands beside it in P05's amendment record.")
f24["why"] = ("Rule 14: P05 was amended at D4a-01 (move 198, contrasting; J after the D3c interview), so the "
              "finding touching it is re-examined in the same act. The claim, the bound and refuted_by are "
              "unchanged; only where the scope is written changes, and the amendment is marked not re-checked.")
new.append(f24)
f17 = copy.deepcopy(last["F-017"])
old_clause = "(A11, theorised)"
if old_clause not in f17["statement"]:
    raise SystemExit("F-017's statement does not carry %r word for word" % old_clause)
f17.update({"stage": "D4", "leg": "D4a-01", "t": t, "supersedes": "F-017"})
f17["statement"] = f17["statement"].replace(old_clause, (
    "(P04; the arrow that a template settles the design argued in a thread, A11, was withdrawn at D4a-01 after the "
    "D3 freeze, not re-checked)"))
f17["why"] = ("Rule 14: A11 was withdrawn at D4a-01 (move 199, dropping working hypotheses; J after the D3c "
              "interview), and F-017 cited it for one artifact stating and dividing the goal. P04 (templates and "
              "coordinates) still states that a layout states the picture and divides it; what is withdrawn is the "
              "claim that the layout settles the design talk. The rest of F-017 does not rest on A11 and is "
              "unchanged, with its status.")
new.append(f17)
for r in new:
    print("%s supersedes %s: status %s; statement ends: ...%s" % (r["id"], r["supersedes"], r["status"],
                                                                  r["statement"][-260:]))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(F, "a", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended %d lines; findings.jsonl now %d lines" % (len(new), sum(1 for l in open(F, encoding="utf-8") if l.strip())))
