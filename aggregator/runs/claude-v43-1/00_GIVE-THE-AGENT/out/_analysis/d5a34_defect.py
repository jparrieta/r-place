#!/usr/bin/env python3
"""D5a-34: print the defects.jsonl lines for F34 (D6 notes; the work_remained field). Append by redirect.

    python3 out/_analysis/d5a34_defect.py >> out/defects.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5a-34",
    "where": "F34 (name), K02, A10, A16, and the node T4-006",
    "what": ("No renaming proposed: 'the design sized to the hands: scale and detail conditioned on crew, upkeep, space "
             "and colours' holds for 16 of 22 members by its list of conditions and strictly for the 10 whose cited words "
             "name the room's own capacity; six lines condition the design on other things (a poll, a purpose, a "
             "signature's place, a neighbour's figure taken in, designs proposed after the close). For D6: a link from K02 "
             "to P02 (the room's judgment of its hands, upkeep and space sizes the design before any loss), beside A10 "
             "(K02 to the move after a loss); r/evex's room model proposes it as a new element, and r/crystalclear's model "
             "reads the same act as not K02 because K02 is written as a judgment that the room cannot do what it wants. "
             "For D6 on A16: capacity is a reason for refusing an attack (r/palestine, r/aoe2) beside the norm and the cost "
             "the mechanism names. For D6: three branches sit at T4-006 (F07, F33, F34): the design's keepers, its plan, "
             "and what it can be. See notes-D5.md."),
    "sure": False}, ensure_ascii=False))
print(json.dumps({
    "stage": "D5", "leg": "D5a-34",
    "where": "organizing_end-A1.jsonl, work_remained, F34's members (for D5b and E1)",
    "what": ("Read against its cited codes, F34's work_remained field does not hold as a record of the work at the close. "
             "Of 14 'kept', 5 rest on a line at or after the close saying the work stood (crystalclear, farmcarrots, "
             "marvel, nin, starlightstage); 7 on a completion report during the event (bardmains, borderlands, evex, "
             "palestine, rhythmheaven, strangerthings, yugioh); 1 on a line not about the work (aoe2 c0099); 1 on a line "
             "saying a work did not survive (detroitlions c0158). Of 6 'lost', 1 reports a member's own work gone (AyyMD "
             "c0126); 5 do not concern the room's work (penguins c0070, a rival's logo taken over; PORTUGALCARALHO c0051, "
             "a battle between two university groups; nlsscirclejerk c0084, one member's attempt; anaheimducks c0090, "
             "random colours on the logo; 4chan c0195, 'full circle' in a thread on board mergers). Of 2 'silent', "
             "kindafunny's record says the mark stood intact after the close (c0024). With r/india in F33 (line 95), the "
             "field appears to take completion statements, and lines about other rooms, for survival. survival-D5 should "
             "re-read work_remained from each room's codes before reporting it."),
    "sure": True}, ensure_ascii=False))
