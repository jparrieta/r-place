#!/usr/bin/env python3
"""D3a-48's head update: each replacement must match exactly once, or nothing is written. P06's result joins the
return's list of rooms, its settled carried item ('P06's form') leaves the open list, and the next comparison names
P06's order test against P05 before the other candidates. To stay within 3,000 words, the moves' parenthetical ids
drop from the first line (the return's list names them), and 'wait for the' becomes 'await the'.

  python3 out/_analysis/d3a48_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-47, 2026-10-21 UTC.", "Written at D3a-48, 2026-10-21 UTC."),
    ("Moves 172 to 176 (R01, P05, P22, P21, A21) moved the hash;", "Moves 172 to 176 moved the hash;"),
    ("## The return (D1a to D3a-47)", "## The return (D1a to D3a-48)"),
    ("**D3a-15 to D3a-26.** Rooms of 705:", "**D3a-15 to D3a-48.** Rooms of 705:"),
    ("who may commit the room [P21] 163.",
     "who may commit the room [P21] 163, attribution [P06, a candidate] 563 (225 with coordinating answers)."),
    ("`adjudications.jsonl`: 36,889 lines ruled, 37,668 with re-rulings; the stage's notes: G1 to G52 (nine of them "
     "amended once)",
     "`adjudications.jsonl`: 37,724 lines ruled, 38,503 with re-rulings; the notes: G1 to G53 (nine of them "
     "amended once)"),
    ("- **From D3a-02 to D3a-47**, to weigh after order tests:", "- **From D3a-02 to D3a-48**, to weigh after order tests:"),
    ("P06's form (14); ", ""),
    ("The candidates and dimension lines, by the stage's rules; then the `propose` lines. "
     "The split and 19 story-miss rooms wait for the verdicts.",
     "P06's order test against P05; R02, K03, K04, P19 and dimension lines; then `propose` lines. "
     "The split and 19 story-miss rooms await the verdicts."),
]
t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
