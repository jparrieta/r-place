#!/usr/bin/env python3
"""D5a-40: the corrections found by checking the draft template's claims (diary), applied to d5a40_template.md.
Each old string must occur exactly once. Prints the corrected template.

    python3 out/_analysis/d5a40_fix.py > out/_analysis/d5a40_template2.md
"""
import os, sys

AN = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(AN, "d5a40_template.md"), encoding="utf-8").read()
FIX = [
    # the fill has no survival placeholder; facts: median_organizing_end_hour 72.045
    ("hour {{SURV_END}} for the 98 members", "hour 72.045 for the 98 members"),
    # quotes with nested quotation marks: keep the part before the nested quote
    ("under a joke law: \"Your post was removed because it contained the [Gacha] Tag, which violates the first commandment of the No "
     "Gacha bible; \"No Gacha!\".\" [battlecats/c0148].",
     "under a joke law: \"Your post was removed because it contained the [Gacha] Tag, which violates the first commandment of the No "
     "Gacha bible\" [battlecats/c0148]."),
    ("- **The fake rule enforced.** \"Your post was removed because it contained the [Gacha] Tag, which violates the first commandment "
     "of the No Gacha bible; \"No Gacha!\".\" [battlecats/c0148].",
     "- **The fake rule enforced.** \"Your post was removed because it contained the [Gacha] Tag, which violates the first commandment "
     "of the No Gacha bible\" [battlecats/c0148]."),
    ("\"HAHA CAN WE REQUEST AN EXTENSION OF APRIL FOOLS DAY BY 364 DAYS, SO WE CAN PRETEND TO BE \"ROBOTS\" ALL THE TIME?\" "
     "[totallynotrobots/c0009].",
     "\"HAHA CAN WE REQUEST AN EXTENSION OF APRIL FOOLS DAY BY 364 DAYS\" [totallynotrobots/c0009]."),
    # buzznights is not shown to be a moderator; c0338 holds a nested quote
    ("In r/MMA a moderator promised, \"It's all good - we'll be able to get it back to normal. No worries.\" [MMA/c0124], kept "
     "screenshots, \"I also have screenshots for the next time someone says \"but let the community decide\" :)\" [MMA/c0338], and "
     "closed with \"Until next year, bby.\" [MMA/c0342].",
     "In r/MMA a member promised, \"It's all good - we'll be able to get it back to normal. No worries.\" [MMA/c0124]. The same "
     "member kept screenshots as \"A glorious reminder.\" [MMA/c0338] and closed with \"Until next year, bby.\" [MMA/c0342]."),
    ("- **The end of the play argued.** \"[SPOILER] To those that think the sub is going \"back to normal\" tomorrow...\" [MMA/c0235].",
     "- **The end of the play argued.** \"April Fools is over. Back to Warframe.\" [warframe/c0197]. \"In Honolulu it's 7 pm\" "
     "[warframe/c0198]."),
    # c0061 asks; it does not show a member who missed the joke
    ("Another, who had a bookmark to the sub, did not: \"IS THIS APRIL'S FOOL???!\" [warframe/c0061].",
     "Another, who had followed a bookmark to the sub, asked: \"IS THIS APRIL'S FOOL???!\" [warframe/c0061]."),
    # D0cR3d is not shown to be a moderator
    ("and a moderator set a price for another theme:", "and a post set a price for another theme:"),
    # c0008 is at h+10.92 and c0122 at h+24.19: thirteen hours, not a day
    ("A day later another call went out, \"Help build", "Later another call went out, \"Help build"),
    # unmeasured comparison replaced by a counted one: warframe holds all three signatures, as 7 of 84 do
    ("What is unrepresentative about it: its play was unusually busy, with a bargain for votes and a wiki to repair, and its canvas work "
     "is better recorded than in most of the form.",
     "What is unrepresentative about it: it holds all three of the form's signature themes, keying, collective memory and direct "
     "information sharing, as 7 of the 84 defining members do (section 14)."),
    # c0055 follows the Scott letters found on the canvas (c0024 to c0026)
    ("And the play reached the canvas back: \"Scott face flair when?\" [fivenightsatfreddys/c0055].",
     "And letters found on the canvas became a request to the sub: \"Scott face flair when?\" [fivenightsatfreddys/c0055]."),
    # the ban was announced as permanent, as the day's joke
    ("Its play was a rule: the moderators banned the sub's own comics for the day.",
     "Its play was a rule: as the day's joke, the moderators banned the sub's own comics."),
    # 23 instantiate K01 without changing keying (r/baylor has neither)
    ("among the rooms where K01 is instantiated and keying is not changed (24 of the 84 defining members here)",
     "among the rooms where K01 is instantiated and keying is not changed (23 of the 84 defining members here)"),
]
for old, new in FIX:
    n = t.count(old)
    if n != 1:
        sys.exit("found %d times: %s" % (n, old[:70]))
    t = t.replace(old, new)
sys.stdout.write(t)
