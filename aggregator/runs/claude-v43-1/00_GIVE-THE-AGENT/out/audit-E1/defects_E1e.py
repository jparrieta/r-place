#!/usr/bin/env python3
"""E1e: the experience leg's defect lines, printed for appending to out/defects.jsonl.

    python3 out/audit-E1/defects_E1e.py >> out/defects.jsonl

Found while writing stage E1's manifest entries (audit-E1/manifest_E1.py) from the dispatch's own record.
"""
import json

LINES = [
    {"stage": "E1", "leg": "E1e", "where": "audit-E1/section-09.md line 9 (in audit-E1.md as assembled at E1d)",
     "what": "The analyst's: the audit's section 4 says the reconstruction readers were deepseek/deepseek-v4.1-flash "
             "'called directly', taken from the principal investigator's message at E1d. The dispatch's own record, "
             "_fleet_raw/E1/arm.json, gives route 'gateway' and reasoning effort medium. The record is right. Superseded by "
             "audit-E1/section-09.e1d.md (the replacement listed in audit-E1/supersede_parts.py), and audit-E1.md "
             "reassembled; the first two assemblies are kept.",
     "sure": True},
    {"stage": "E1", "leg": "E1e", "where": "run_manifest.json",
     "what": "The instrument's: the E1 reconstruction dispatch wrote no manifest entry, so its figures (fidelity, the "
             "readers' cost and tokens) had none until E1e, when the analyst appended one from _fleet_raw/E1/arm.json and "
             "DONE. The arm file records no temperature or top_p, so the entry carries none. The D3 re-check return has no "
             "entry either (audit-E1.md, section 1, part 3).",
     "sure": True},
]

for line in LINES:
    print(json.dumps(line, ensure_ascii=False))
