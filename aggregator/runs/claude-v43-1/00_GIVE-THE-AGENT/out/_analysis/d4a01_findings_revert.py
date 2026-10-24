#!/usr/bin/env python3
"""D4a-01, rule 14 after the revert of moves 198 and 199 (J, QD4-001, option b). F-024's and F-017's
re-examination lines of D4a-01 stay as written (J: keep them). Each finding gets one later line, so that its last
line matches the model as it stands: the statement of the line before D4a-01's (F-024 at D3c; F-017 at D3a-01),
with one added sentence saying that the D4a-01 amendment was reverted and is held as a proposal. Status unchanged.
Without --write it prints the added sentences.

    python3 out/_analysis/d4a01_findings_revert.py [--write]
"""
import argparse, copy, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
rows = [json.loads(l) for l in open(F, encoding="utf-8") if l.strip()]
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
ADD = {
    "F-024": ("At D4a-01 the scope was written into P05's own words (move 198; findings line of D4a-01), and the same "
              "leg reverted it at J's ruling (QD4-001, option b). The scope sentence and the bound naming the six "
              "rooms and the three are a held proposal, never served to the rooms and not re-checked. P05 stands "
              "as frozen at D3 (46384686)."),
    "F-017": ("At D4a-01 A11 was withdrawn (move 199; findings line of D4a-01), and the same leg reverted the "
              "withdrawal at J's ruling (QD4-001, option b). The withdrawal is a held proposal under rule 14, never "
              "served to the rooms and not re-checked; A11 stands as frozen at D3 (46384686)."),
}
new = []
for fid, add in ADD.items():
    mine = [r for r in rows if r["id"] == fid]
    assert mine[-1]["leg"] == "D4a-01", (fid, mine[-1]["leg"])
    before = mine[-2]
    r = copy.deepcopy(mine[-1])
    r.update({"t": t, "stage": "D4", "leg": "D4a-01", "supersedes": fid,
              "statement": before["statement"] + " " + add,
              "why": ("Rule 14: the model change this finding's D4a-01 line followed was reverted in the same leg "
                      "(move 203, J's answer to QD4-001). The D4a-01 line stays as written, at J's word; this line "
                      "restores the statement of the line before it (%s at %s) and records the held proposal. "
                      "Status, bound and refuted_by are unchanged." % (fid, before["leg"]))})
    new.append(r)
    print("%s (status %s): restores the %s statement, adds: %s" % (fid, r["status"], before["leg"], add))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(F, "a", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended %d lines; findings.jsonl now %d lines" % (len(new), sum(1 for l in open(F, encoding="utf-8") if l.strip())))
