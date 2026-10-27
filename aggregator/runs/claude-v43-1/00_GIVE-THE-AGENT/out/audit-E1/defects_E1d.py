#!/usr/bin/env python3
"""E1d: the check leg's defect lines, printed for appending to out/defects.jsonl.

    python3 out/audit-E1/defects_E1d.py >> out/defects.jsonl

Two lines, both the instrument's, found when the reconstruction returns were validated
(audit-E1/reconstruction_validate.py and its output).
"""
import json

LINES = [
    {"stage": "E1", "leg": "E1d", "where": "tools/packets.py line 64 (the packet trailer) and out/RETURN-E1.md",
     "what": "The instrument's: every E1 packet ends 'Confirm you reached it by returning your lines and then the end "
             "marker the return specification names. END OF PACKET', and RETURN-E1.md, which the analyst wrote at E1c "
             "without reading the trailer, names no end marker and says 'Write nothing else in the file.' Each of the 30 "
             "readers ended its lines with a marker of its own (END OF PACKET 22, END OF RETURN 6, <<< END >>> 1, agent "
             "END OF PACKET 1), and fleet.py judged all 30 returns not JSON and the rooms exhausted after three attempts. "
             "At the principal investigator's instruction (27 October 22:51Z) the returns were validated at E1d from the "
             "newest raw file per room, with the one final marker line dropped and recorded "
             "(audit-E1/reconstruction_validate.py); there was no re-dispatch.",
     "sure": True},
    {"stage": "E1", "leg": "E1d", "where": "out/RETURN-E1.md (the claim and summary templates)",
     "what": "The instrument's, written by the analyst at E1c: the templates give sub as '<room>' and do not say whether "
             "that is the bare name or r/<room>, while the packets name each room as r/<room>. 5 of 30 readers wrote "
             "r/<room> on every line (picturegame, python, ReBoot, tagpro, Madeon) and failed the rule declared before "
             "the check; an amendment made after the first run reads r/<room> as the room, and both counts are reported "
             "(25 valid under the first rule, 30 under the amended one).",
     "sure": True},
]

for line in LINES:
    print(json.dumps(line, ensure_ascii=False))
