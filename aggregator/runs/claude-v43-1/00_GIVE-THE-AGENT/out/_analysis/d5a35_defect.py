#!/usr/bin/env python3
"""D5a-35: print the defects.jsonl lines for F35 (renaming, P15 and A12 for D6; the work_remained field).
Append by redirect.

    python3 out/_analysis/d5a35_defect.py >> out/defects.jsonl
"""
import json

print(json.dumps({
    "stage": "D5", "leg": "D5a-35",
    "where": "F35 (name), P15 and A12",
    "what": ("Renaming proposal: the D4 name 'the call made workable: answers ask for a task, and callers supply it' holds "
             "for 'answers ask for a task' in 5 of 18 members and for 'callers supply it' in 5 others as visibility or a "
             "location cue; the question answered with a task is shown in two members' words (r/FlaggyFlag, "
             "r/clashroyale); five lines concern joiners who report a part and renew the call, three calls redirected, "
             "divided or refused. Proposed: 'the call answered beyond a bare yes: questions for a task, reports that renew "
             "the call, and calls made visible'. For D6 on P15: its 'the line asks for nothing back' describes one form of "
             "acceptance; a willing answer that asks for the task, the place or the means is another (r/polyamory's room "
             "model records P15 absent for that reason). P15 is instantiated in 13 of F35's 18 members against 336 of 354 "
             "rooms of their size. A12 (the bare answer after the call) is restricted in 8 of 18 against 83 of 354. "
             "F-023's count (25 of 31 read acceptances bare) stands; F35 shows where the other forms sit. See notes-D5.md."),
    "sure": False}, ensure_ascii=False))
print(json.dumps({
    "stage": "D5", "leg": "D5a-35",
    "where": "organizing_end-A1.jsonl, work_remained, F35's members (for D5b and E1)",
    "what": ("Read against its cited codes, F35's work_remained field: of 9 'kept', 3 rest on a line at or after the close "
             "saying the work stood (TheHulk c0106, purdue c0330, stargate c0056) and 3 on lines that plausibly say so "
             "(lebanon c0212 at h+71.05, littlewitchacademia c0063, wow c0296); 2 on completion reports during the event "
             "(borussiadortmund c0031, starbound c0087); 1 on a post title (hatsune c0060, 'The Ideal Place'). Of 6 'lost', "
             "3 say the room's work was gone (clashroyale c0424, homestuck c0279, raocow c0047); 1 says the room's main flag "
             "stood and a second logo was lost (FlaggyFlag c0028); 1 is a loss during the event (GuildWars2 c0120); 1 is "
             "unclear (seahawks c0153). The 3 'silent' records hold 2 to 10 coded concepts. With lines 95 and 97, the field "
             "should be re-read from the codes before survival-D5 reports it."),
    "sure": True}, ensure_ascii=False))
