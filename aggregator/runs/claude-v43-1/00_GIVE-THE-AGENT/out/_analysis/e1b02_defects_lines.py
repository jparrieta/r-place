#!/usr/bin/env python3
"""E1b-02: the two handback counts that disagree with their governing files, as defects.jsonl lines (appended by a
stdout redirect, once).

    python3 out/_analysis/e1b02_defects_lines.py >> out/defects.jsonl

Found by audit-E1/counts_phrases.py and counts_sample_check.py. Nothing earlier is changed (rule 18).
"""
import json

L = [
    {"where": "handback-B1.md line 20",
     "what": "The instrument's: the handback says 107 episode lines whose kinds none of their rooms holds. notes-B1.md line 3108 (written at B2, by out/_analysis/b2_episode_kinds.py) counts 106 (line, kind) pairs over 81 lines of episodes-B1.jsonl, and says the 107 is wrong; the handback was not corrected. Found by audit-E1/counts_sample_check.py (row 3).",
     "sure": True},
    {"where": "handback-C5-p14.md line 45",
     "what": "The instrument's: the handback says the model's history holds 31 lines (12 element, 12 arrow, 5 condition, 1 role, 1 claim). model/history.jsonl holds 45 lines of stage C5 up to pass 14's leg, C5c-11 (16 element, 21 arrow, 5 condition, 1 role, 2 claim), over 30 distinct ids (12, 13, 2, 1, 2). 31 matches neither, and the handback does not say how it counted. Found by audit-E1/counts_sample_check.py (row 20), read by hand.",
     "sure": True},
]
for x in L:
    print(json.dumps({"stage": "E1", "leg": "E1b-02", "where": x["where"], "what": x["what"], "sure": x["sure"]},
                     ensure_ascii=False))
