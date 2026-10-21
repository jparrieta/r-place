#!/usr/bin/env python3
"""D3a-52's head update: each replacement must match exactly once, or nothing is written. K04 joins the return's room
counts and the standing elements (move 180), the ledgers move to the close-check's counts, K04's edges join the open
list, and the next comparison drops K04. To keep the head under 3,000 words, four parentheticals leave the return's
list (P06's coordinating answers, R02's own members, A14's one offer and A15's calls over another's work); the notes
keep them.

  python3 out/_analysis/d3a52_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-51, 2026-10-21 UTC.", "Written at D3a-52, 2026-10-21 UTC."),
    ("Moves 172 to 179 moved the hash;", "Moves 172 to 180 moved the hash;"),
    ("## The return (D1a to D3a-51)", "## The return (D1a to D3a-52)"),
    ("**D3a-15 to D3a-51.**", "**D3a-15 to D3a-52.**"),
    ("attribution [P06] 563 (225 with coordinating answers), the envoy [R02] 565 (313 by own members), "
     "old quarrels [K03] 207.",
     "attribution [P06] 563, the envoy [R02] 565, old quarrels [K03] 207, bodies carried in or colour faiths "
     "[K04] 465."),
    ("and terms, 179 of 186 (124 more trade in one offer);", "and terms, 179 of 186;"),
    ("an attack follows a call, 277 of 286 (58 more call over another's work);",
     "an attack follows a call, 277 of 286;"),
    ("**Candidates:** K04 and P19. 28 elements stand.",
     "**K04** stands; its colour faith sits apart (19 of 22). **Candidate:** P19. 29 elements stand."),
    ("- **Moves 177 to 179 (developing working hypotheses).** P06, R02 and K03 stand again from their lines; "
     "no arrow is claimed.",
     "- **Moves 177 to 180 (developing working hypotheses).** P06, R02, K03 and K04 stand again from their lines; "
     "no arrow is claimed."),
    ("`adjudications.jsonl`: 39,104 lines ruled, 39,883 with re-rulings; the notes: G1 to G55 (nine of them amended "
     "once)",
     "`adjudications.jsonl`: 39,972 lines ruled, 40,757 with re-rulings; the notes: G1 to G56 (ten of them amended "
     "once)"),
    ("model history 153;", "model history 154;"),
    ("elements 30 (28 standing, 2 candidates)", "elements 30 (29 standing, 1 candidate)"),
    ("- **From D3a-02 to D3a-51**, to weigh after order tests:", "- **From D3a-02 to D3a-52**, to weigh after order tests:"),
    ("K03's edges (C02, K04).", "K03's and K04's edges (C02; the faith apart)."),
    ("K04, P19 and dimension lines;", "P19 and dimension lines;"),
]
t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
    print("wrote", P)
