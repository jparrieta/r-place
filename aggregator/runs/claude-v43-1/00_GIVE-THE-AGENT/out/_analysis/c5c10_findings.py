#!/usr/bin/env python3
"""C5c-10, problem 4: append F-021 (rooms that called for hands and reported a work up after the call; the count behind
'aligned') and F-022 (reports of the work's state and templates are carried largely apart) to out/findings.jsonl.
Counts from c5c10_aligned.py and from assignments_final.jsonl (cited concepts). Refuses if either id exists.

    python3 out/_analysis/c5c10_findings.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
have = {json.loads(l)["id"] for l in open(F, encoding="utf-8") if l.strip()}
if have & {"F-021", "F-022"}:
    sys.exit("F-021 or F-022 exists")
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rows = [
    {"stage": "C5", "leg": LEG, "id": "F-021", "tier": "dimension", "warrant": "inferred", "status": "standing", "t": T,
     "statement": "Most rooms that called for hands report a work up after the call. Of 370 rooms carrying calls for "
                  "hands (P01), 284 carry a report that a work is up (P11), and in 233 (0.630) the first such report "
                  "comes after the first call. The share rises with the room's size: 24 of 60 rooms with calls in the "
                  "smallest quarter by items in the window, 55 of 90, 74 of 110, and 80 of 110 in the largest.",
     "evidence": ["out/_analysis/c5c10_aligned.py", "out/assignments_final.jsonl", "out/_analysis/c2_elements_c5c2.json"],
     "bound": "First cited concepts by hour, as in the order tests; no null is drawn, so this is a share, not an order "
              "beating chance. A report that the work is up is the room's own word in its record; it does not show who "
              "placed the pixels, and much of a room's artwork was placed by people who never wrote in it. The canvas is "
              "not evidence (rule 7). A room that writes more carries more elements, which the size gradient may partly "
              "reflect.",
     "refuted_by": ["a reading of the reports that finds most of them announce a work begun or planned rather than one "
                    "up"],
     "literature": ["Okhuysen and Bechky 2009"], "abductive": False,
     "prompted_by": "J's guidance on 'aligned' (C5c-07); Okhuysen and Bechky 2009, p. 469: across definitions, "
                    "coordination means that 'a goal, task, or piece of work is achieved'",
     "why": "problem 4 of the serial work: whether D02 and the alignment proposition may say that rooms aligned many "
            "hands, or only that members tried; the rule logged first said 'aligned' of the rooms whose record reports "
            "the work built after the call, with its count"},
    {"stage": "C5", "leg": LEG, "id": "F-022", "tier": "fourth", "warrant": "inferred", "status": "standing", "t": T,
     "statement": "Reports of the work's state and templates are carried largely apart. Building and reporting the mark "
                  "(T3-038) is carried by 237 rooms and the members of Standardization of output (T4-008) by 237; 89 "
                  "carry both, about what independence would give (80), and 385 carry either. So 148 rooms report the "
                  "state of their mark with no template or coordinates coded, and 148 share templates with no report "
                  "coded.",
     "evidence": ["out/assignments_final.jsonl", "out/fourth/fourth.jsonl"],
     "bound": "Rooms carrying a theme's cited concepts. A room in which no report was coded may still have reported its "
              "work in talk the coders placed elsewhere; the counts say what the coded record carries.",
     "refuted_by": ["a recount in which most rooms that share templates also report the state of their mark"],
     "literature": ["Okhuysen and Bechky 2009", "Moffett et al. 2021"], "abductive": False,
     "prompted_by": "the weighing of option (d) at C5c-10: whether reports and templates are one coordinating route",
     "why": "problem 4 of the serial work: a merge of Stigmergy and Standardization of output would join two routes that "
            "the coded rooms carry apart and that the C3 mapping assigns to different universal problems"}]
with open(F, "a", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended F-021 and F-022; findings.jsonl now %d lines" % sum(1 for l in open(F, encoding="utf-8") if l.strip()))
