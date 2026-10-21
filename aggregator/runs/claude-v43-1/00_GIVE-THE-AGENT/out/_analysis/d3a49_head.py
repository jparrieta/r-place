#!/usr/bin/env python3
"""D3a-49's head update: each replacement must match exactly once, or nothing is written. P06 and R02 stand again
(moves 177, 178); R02's result joins the return's list of rooms; the candidates line, the ledgers and the counts follow;
the reasons for the last revisions name moves 177 and 178, and the older reasons for moves 174 and 175 leave the head
(the return's list and notes-D3.md keep them) so that it stays within 3,000 words; the next comparison drops R02.

  python3 out/_analysis/d3a49_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-48, 2026-10-21 UTC.", "Written at D3a-49, 2026-10-21 UTC."),
    ("Moves 172 to 176 moved the hash;", "Moves 172 to 178 moved the hash;"),
    ("## The return (D1a to D3a-48)", "## The return (D1a to D3a-49)"),
    ("**D3a-15 to D3a-48.** Rooms of 705:", "**D3a-15 to D3a-49.** Rooms of 705:"),
    ("attribution [P06, a candidate] 563 (225 with coordinating answers).",
     "attribution [P06] 563 (225 with coordinating answers), the envoy [R02] 565 (313 by own members)."),
    ("**Candidates:** P06, R02, K03, K04 and P19. 25 elements stand.",
     "**Candidates:** K03, K04 and P19. 27 elements stand."),
    ("- **Move 176 (D3a-27, developing working hypotheses).** A21 stands, bounded to the stated limit and the refusal; "
     "requests for a leader precede agreements. **Moves 174 and 175 (D3a-06, D3a-26, developing working hypotheses).** "
     "P22's range names one member correcting a claim; P21's frame reads 'dispute, or state the limits of'.",
     "- **Moves 177 and 178 (D3a-49, developing working hypotheses).** P06 and R02 stand again from their lines; "
     "no arrow is claimed. **Move 176 (D3a-27).** "
     "A21 stands, bounded to the stated limit and the refusal; requests for a leader precede agreements."),
    ("`adjudications.jsonl`: 37,724 lines ruled, 38,503 with re-rulings; the notes: G1 to G53 (nine of them "
     "amended once)",
     "`adjudications.jsonl`: 38,411 lines ruled, 39,190 with re-rulings; the notes: G1 to G54 (nine of them "
     "amended once)"),
    ("model history 150;", "model history 152;"),
    ("elements 30 (25 standing, 5 candidates)", "elements 30 (27 standing, 3 candidates)"),
    ("- **From D3a-02 to D3a-48**, to weigh after order tests:", "- **From D3a-02 to D3a-49**, to weigh after order tests:"),
    ("P06's order test against P05; R02, K03, K04, P19 and dimension lines;",
     "P06's order test against P05; K03, K04, P19 and dimension lines;"),
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
