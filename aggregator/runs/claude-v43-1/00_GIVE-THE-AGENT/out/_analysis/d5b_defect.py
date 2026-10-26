#!/usr/bin/env python3
"""D5b: print the defects.jsonl lines for the work_remained re-reading and the four contradicted timings.
Append by redirect.

    python3 out/_analysis/d5b_defect.py >> out/defects.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5b",
    "where": "organizing_end-A1.jsonl, work_remained, the 476 rooms in a branch (for D6 and E1); account.md, 'Which keep the work alive'",
    "what": ("Re-read for every room in a branch from its cited codes, by a rule logged before the reading (files "
             "out/_analysis/d5b_wr_read1.json to d5b_wr_read5.json, three overrides in d5b_survival.py). The field agrees "
             "with the re-reading in 248 of 476. Of 253 'kept', a line at or after hour 72 says the room's work stood in "
             "146; 61 rest on a line before hour 72, 23 are unclear, 20 concern something other than the room's own work, "
             "3 say the work was gone. Of 161 'lost', 40 rest on a line at or after hour 72 saying the work was gone; 54 on "
             "a line before hour 72, 43 on other rooms' work or remarks, 21 unclear, 3 say it stood. 'Silent' agrees in all "
             "62. Read again, the rooms' own words after the close say stood in 149 and gone in 43. The field over-reads "
             "both outcomes, loss more. Where this reading differs from the D5a-33 to D5a-35 counts (lines 95, 97, 99), it "
             "is by the stricter hour rule and supersedes them. The ledger is unchanged; branches-D5.jsonl keeps the field. "
             "The account's paragraph 'Which keep the work alive' (kept 347, lost 218, silent 140 of 705, and its shares) "
             "rests on the field and is a question for D6; prior.md section 5's measured error (25 of 34) understated it "
             "for these rooms. See survival-D5.md section 2."),
    "sure": True}, ensure_ascii=False))
print(json.dumps({
    "stage": "D5", "leg": "D5b",
    "where": "forms/F23, F25, F27, F31 and F32 accounts, section 1 (dated changes against the placements by hour)",
    "what": ("By the D5b timing rule (logged before computing; out/_analysis/d5b_timing.py), the members' placements by "
             "hour contradict four dated timings in the narratives: r/thebluecorner at hour 39 (F23, F25; the call to a "
             "copy of the canvas read as beside it, members' placements fall from 2,404 to 1,396 over four hours); r/hawks "
             "at 61.14 (F27; colour detail announced, 646 to 252); r/faeria at 29.15 (F31; pasture secured, 11 to 4, small "
             "counts and a final-artwork region); r/httyd at 52.45 (F32; marked, then 183 to 118). Questions for the "
             "accounts, not corrections; a timing only. Of 23 checkable acts, 15 corroborated, 4 contradicted, 3 not shown, "
             "1 empty. See survival-D5.md section 6."),
    "sure": False}, ensure_ascii=False))
