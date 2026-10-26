#!/usr/bin/env python3
"""D5a-32: print the defects.jsonl line for F32 (renaming, the link for D6, A07 and A02 notes). Append by redirect.

    python3 out/_analysis/d5a32_defect.py >> out/defects.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5a-32",
    "where": "F32 (name), the link from P11 to P05, A07 beside F27, F30 and F31, and A02",
    "what": ("Renaming proposal: the D4 name 'the marking returns to keeping: celebration followed by renewed defence' "
             "holds for 'celebration followed by' in all 21 members, and for 'renewed defence' in the 11 whose cited words "
             "name defence, protection, an attack or reinforcements; in the others the keeping was maintenance, repair of "
             "a flaw, a watch or a pledge. 'Returns' follows the model's order: in the rooms keeping had often never "
             "stopped (r/newzealand posted a protection checklist at h+18.27 and celebrated with a call to protect at "
             "h+11.95; before r/habs celebrated, a member had spent 'all of my moves so far' keeping the logo). Proposed: 'the "
             "marking does not end the keeping: celebration followed by defence and repair'. For D6, the link the model "
             "lacks: from P11 (the marking) to P05 (keeping), stated in 21 re-check lines in 21 rooms (20 recorded as "
             "sequence, 1 as dependence), with no within-case dating, so its order has not been tested against a null; "
             "beside F09's link from P10 to P03. A narrower reading stands on 10 members (keeping named before any new "
             "damage, 7; a finish corrected, 3); in 7 the keeping followed new damage and may answer the attack, which "
             "P05 already states. For D6 on A07: F32 is the other side of the restriction that ran as section 7 in F27, "
             "F30 and F31: rooms marked the work while keeping went on; A07 is restricted in 3 of F32's 21 members, "
             "against 34 of 259 rooms of their size. For D6 on A02 (F32's section 7, 8 of 21 against 65 of 259): 7 "
             "lines say the start and the call came in one turn; A02's bound covers a call before the proposal, not a "
             "proposal that is itself the call. See notes-D5.md."),
    "sure": False}, ensure_ascii=False))
