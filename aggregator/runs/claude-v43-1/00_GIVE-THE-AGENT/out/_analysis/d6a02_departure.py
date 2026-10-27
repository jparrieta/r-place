#!/usr/bin/env python3
"""D6a-02: departures.jsonl line 20, the amendment QD6-001's answer asks for (one amendment for both changes, citing J's
18:01 ruling); it supersedes line 19's scope, and line 19 stays as written. Prints one JSON line; append with >>.

    python3 out/_analysis/d6a02_departure.py >> out/departures.jsonl
"""
import json

print(json.dumps({
    "stage": "D6", "leg": "D6a-02", "date": "2026-10-27",
    "provision": "J's ruling of 26 October, 18:01 Berlin (stage D6 builds on the room forms, with the 35 branches as the level "
                 "below), carried out as QD6-001's answer and the principal investigator's message of 27 October 03:57 UTC "
                 "(the handler's view, on J's instruction of 25 October 21:39 Berlin; J has not seen it)",
    "why": "The stage's close-check reads fractal-D6.jsonl as branch lines and treats retelling-D6.md as present only at the "
           "last leg (tools/checks/stage_D6.py, lines 35 to 36 and 72 to 79). J's ruling puts the room forms first. Two "
           "files keep both: the forms' lines in a file of their own, the branch lines in the stage's file.",
    "applies_backwards": "True, to D6a-01's outputs: its 42 form lines are moved, not rewritten, and its section is moved, "
                         "not deleted.",
    "scope": "(1) out/fractal-forms-D6.jsonl holds one line per element and room form (A to F), the form's letter in 'form'; "
             "it is the primary product of the stage as J ruled. out/fractal-D6.jsonl holds branch lines only, in the "
             "stage's shape (branch F01 to F35), at least one per branch by D6b, at the element where the branch explains "
             "its form. (2) retelling-D6.md is not kept during the dimension legs: D6a-01's file is moved to "
             "out/retelling-D6-parts/D01.md, each later dimension is written to out/retelling-D6-parts/<dimension>.md, and "
             "D6b assembles retelling-D6.md with the figure and the handback. The dimension legs close with done.sh D6 "
             "where validate passes. Supersedes line 19's scope; amendments-D6.jsonl stays empty, as the stage requires "
             "for the model.",
}, ensure_ascii=False))
