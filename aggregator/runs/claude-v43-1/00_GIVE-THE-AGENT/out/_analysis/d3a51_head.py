#!/usr/bin/env python3
"""D3a-51's head update: each replacement must match exactly once, or nothing is written. K03 joins the return's room
counts and the standing elements (move 179), the ledgers move to the close-check's counts, K03's edges join the open
list, and the next comparison drops K03. Move 176's reason loses its last clause to keep the head under 3,000 words;
the notes keep it.

  python3 out/_analysis/d3a51_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-50, 2026-10-21 UTC.", "Written at D3a-51, 2026-10-21 UTC."),
    ("Moves 172 to 178 moved the hash;", "Moves 172 to 179 moved the hash;"),
    ("## The return (D1a to D3a-49)", "## The return (D1a to D3a-51)"),
    ("**D3a-15 to D3a-49.**", "**D3a-15 to D3a-51.**"),
    ("the envoy [R02] 565 (313 by own members).", "the envoy [R02] 565 (313 by own members), old quarrels [K03] 207."),
    ("**Candidates:** K03, K04 and P19. 27 elements stand.", "**Candidates:** K04 and P19. 28 elements stand."),
    ("- **Moves 177 and 178 (D3a-49, developing working hypotheses).** P06 and R02 stand again from their lines; "
     "no arrow is claimed.",
     "- **Moves 177 to 179 (developing working hypotheses).** P06, R02 and K03 stand again from their lines; "
     "no arrow is claimed."),
    ("A21 stands, bounded to the stated limit and the refusal; requests for a leader precede agreements.",
     "A21 stands, bounded to the stated limit and the refusal."),
    ("`adjudications.jsonl`: 38,411 lines ruled, 39,190 with re-rulings; the notes: G1 to G54",
     "`adjudications.jsonl`: 39,104 lines ruled, 39,883 with re-rulings; the notes: G1 to G55"),
    ("model history 152;", "model history 153;"),
    ("elements 30 (27 standing, 3 candidates)", "elements 30 (28 standing, 2 candidates)"),
    ("- **From D3a-02 to D3a-50**, to weigh after order tests:", "- **From D3a-02 to D3a-51**, to weigh after order tests:"),
    ("P05's telling naming P06 (attributions in 7 of 12 tellings).",
     "P05's telling naming P06 (attributions in 7 of 12 tellings); K03's edges (C02, K04)."),
    ("K03, K04, P19 and dimension lines;", "K04, P19 and dimension lines;"),
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
