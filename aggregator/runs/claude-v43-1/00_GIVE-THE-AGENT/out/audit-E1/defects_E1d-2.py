#!/usr/bin/env python3
"""E1d: the check leg's third defect line, printed for appending to out/defects.jsonl.

    python3 out/audit-E1/defects_E1d-2.py >> out/defects.jsonl

Found when the first assembly of audit-E1.md failed tools/checks/stage_E1.py (out/_analysis/e1d_validate_E1.txt).
"""
import json

print(json.dumps({
    "stage": "E1", "leg": "E1d",
    "where": "audit-E1/section-01.md lines 57 and 60, audit-E1/section-03.md lines 60 and 86, audit-E1/section-05.md line 40",
    "what": "The analyst's: four passages of audit parts written at E1b-01, E1b-03 and E1b-05 use tokens the close-check "
            "reads as model ids and finds in no ledger (two members' words, a logo name, and a gate rule's number at D3a-55), "
            "and one sentence names the two words the check bars in order to say that no figure is either. The first "
            "assembly of audit-E1.md failed on them (5 errors, 2 shapes). Superseded by copies with the replacements listed "
            "in audit-E1/supersede_parts.py (section-01.e1d.md, section-03.e1d.md, section-05.e1d.md), which audit-E1.md now "
            "joins; the originals and the first assembly (audit-E1/audit-E1.superseded-1.md) are kept. No figure changed.",
    "sure": True}, ensure_ascii=False))
