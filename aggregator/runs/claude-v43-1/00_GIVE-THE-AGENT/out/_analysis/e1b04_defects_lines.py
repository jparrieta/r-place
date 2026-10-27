#!/usr/bin/env python3
"""E1b-04: the defect the claims audit found, as a defects.jsonl line (appended by a stdout redirect, once).

    python3 out/_analysis/e1b04_defects_lines.py >> out/defects.jsonl

Found by audit-E1/claims_returns.py and the reading of prior.md section 3 (claims-E1.md). Nothing earlier is changed.
"""
import json

print(json.dumps({"stage": "E1", "leg": "E1b-04",
                  "where": "prior.md section 3 ('What each level's verdict will rest on'), against model/arrows.jsonl and propositions.jsonl",
                  "what": "The instrument's: section 3 declared that the population pattern would be supported by a pattern that holds in counts over the analysed set and at held size, with the order of events read against section 4's brackets. No arrow's order test was run at held size, and only A20 is read inside a bracket (before hour 73); the other 19 counts run over the whole record. The one finding tested at held size is F-009. The propositions' pattern evidence is otherwise of its kind (claims-E1.md). Found by audit-E1/claims_returns.py.",
                  "sure": True}, ensure_ascii=False))
