#!/usr/bin/env python3
"""E1b-06: the defects the ledgers and stories audit found, as defects.jsonl lines (appended by a stdout redirect,
once).

    python3 out/_analysis/e1b06_defects_lines.py >> out/defects.jsonl

Found by audit-E1/ledgers_stories.py, read by hand. Nothing earlier is changed (rule 18).
"""
import json

L = [
    {"where": "account.md",
     "what": "The instrument's: what a reader was given. The account is 3,326 words, not the one to two pages the stage asks; 3 of its 37 cited quotes carry no hour; and it lists the residue of the last story's 19 rooms told in part rather than explaining it. Found by audit-E1/ledgers_stories.py.",
     "sure": True},
    {"where": "departures.jsonl (18 of 21 lines)",
     "what": "The instrument's: 18 of the 21 departures do not state what following the provision would have cost; only 3 carry the field what_following_it_would_have_cost. Found by audit-E1/ledgers_stories.py.",
     "sure": True},
    {"where": "departures.jsonl lines 5 and 21",
     "what": "The instrument's: two departures were acted on before they were written. Line 5 (A1's reading route) says it was logged late, at A1c; line 21 (D6's widened branch-naming rule) says the widened readings were in use from D6a-02, before they were stated at D6a-04 and written at D6a-09 under J's ruling 1d. Found by audit-E1/ledgers_stories.py.",
     "sure": True},
]
for x in L:
    print(json.dumps({"stage": "E1", "leg": "E1b-06", "where": x["where"], "what": x["what"], "sure": x["sure"]},
                     ensure_ascii=False))
