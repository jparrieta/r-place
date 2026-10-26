#!/usr/bin/env python3
"""D5a-33: print the defects.jsonl lines for F33 (the F15 and F33 family, A07 a fourth time, A11 in room models
against the ledger, and r/india's work_remained field). Append by redirect.

    python3 out/_analysis/d5a33_defect.py >> out/defects.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5a-33",
    "where": "F33 and F15 (one change at two nodes), A07, A11",
    "what": ("No renaming proposed: 'the plan kept current while the design settles' holds for most members (the design "
             "changing in 16 of 23; correction or one current plan in 13). Its strongest objection, for D6: F33 differs "
             "from F15 only in the fourth-order node of the same key (add-step on P04: T4-006 here, T4-008 in F15), and "
             "the two share no room; of the population's 115 add-step P04 lines in 114 rooms, 43 are at T4-008 and 23 at "
             "T4-006. A room's branch follows where its coders placed the theme carrying its template talk. D6 may read "
             "F15 and F33 (65 rooms) as one change. For D6 on A07: it ran as section 7 for the fourth time (F27, F30, F31, "
             "F33; 23 rooms carry an A07 restrict line across them, against 87 in the population); in F33 the marking came "
             "in the same turn as the report, or while the design went on. For D6 on A11: three F33 room models (tf2, "
             "torontoraptors, gatech) say in their own words that a template did not settle the design, yet the ledger "
             "restricts A11 in 11 of 23 members against 221 of 395 rooms of their size; the point may sit in the P04 step "
             "instead. See notes-D5.md."),
    "sure": False}, ensure_ascii=False))
print(json.dumps({
    "stage": "D5", "leg": "D5a-33",
    "where": "organizing_end-A1.jsonl, r/india's work_remained (for D5b and E1)",
    "what": ("r/india's work_remained is 'lost', and its work_remained_codes name c0461, 'And the pakistani flag was gone. "
             ":D', a line about a neighbour's flag. The room's own words at the close say its flag stood: 'Not a single "
             "rogue pixel inside the flag' (c0053, h+73.22) and 'Not a single stray pixel in the end! Great work guys!' "
             "(c0488). The field appears misread; F33's kept count would be 11, not 10, if it is. The field is left as it "
             "is here; D5b's survival file should name it."),
    "sure": True}, ensure_ascii=False))
