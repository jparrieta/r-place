#!/usr/bin/env python3
"""D3a-53's head update: each replacement must match exactly once, or nothing is written. P19 joins the return's
room counts and the standing elements (move 181), the ledgers move to the close-check's counts, P19's edges join the
open list, and the next comparison drops P19. To keep the head under 3,000 words, three items leave the open list (a
finished work reopening calls or design; parallel and outside builders; recording after a loss); the notes keep
them.

  python3 out/_analysis/d3a53_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-52, 2026-10-21 UTC.", "Written at D3a-53, 2026-10-21 UTC."),
    ("Moves 172 to 180 moved the hash;", "Moves 172 to 181 moved the hash;"),
    ("## The return (D1a to D3a-52)", "## The return (D1a to D3a-53)"),
    ("**D3a-15 to D3a-52.**", "**D3a-15 to D3a-53.**"),
    ("bodies carried in or colour faiths [K04] 465.",
     "bodies carried in or colour faiths [K04] 465, guests and hosts [P19] 382."),
    ("**Candidate:** P19. 29 elements stand.",
     "**P19** stands: a host rules in 274 of 382 rooms; a colour faith hosts in 131. 30 elements stand."),
    ("P06, R02, K03 and K04 stand again from their lines;", "P06, R02, K03, K04 and P19 stand from their lines;"),
    ("`adjudications.jsonl`: 39,972 lines ruled, 40,757 with re-rulings; the notes: G1 to G56 (ten of them amended "
     "once)",
     "`adjudications.jsonl`: 40,759 lines ruled, 41,544 with re-rulings; the notes: G1 to G57 (ten of them amended "
     "once)"),
    ("model history 154;", "model history 155;"),
    ("elements 30 (29 standing, 1 candidate)", "elements 30 (all standing)"),
    ("- **From D3a-02 to D3a-52**, to weigh after order tests:", "- **From D3a-02 to D3a-53**, to weigh after order tests:"),
    ("P19's form (9; 5 allied host ties);", "P19's request-only rooms (82) and faith hosts (131);"),
    ("parallel and outside builders (P03); recording after a loss (A08); a finished work reopening calls or design; ",
     ""),
    ("P19 and dimension lines;", "Dimension lines;"),
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
