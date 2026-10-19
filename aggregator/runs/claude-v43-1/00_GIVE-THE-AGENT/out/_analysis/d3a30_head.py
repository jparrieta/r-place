#!/usr/bin/env python3
"""D3a-30's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a30_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-29, 2026-10-19 UTC.", "Last written at D3a-30, 2026-10-19 UTC."),
    ("## The return (D1a to D3a-29)", "## The return (D1a to D3a-30)"),
    ("A02 and A01 stand uncorrected: 222 rooms start and call in one post; in 142 of 407 the call follows a start.",
     "A02, A01 and A03 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331."),
    ("`adjudications.jsonl`: 24,656 lines ruled, 25,413 with re-rulings;",
     "`adjudications.jsonl`: 25,344 lines ruled, 26,101 with re-rulings;"),
    ("the stage's notes: G1 to G34 (five of them amended once)", "the stage's notes: G1 to G35 (five of them amended once)"),
    ("- **From D3a-02 to D3a-29**, to weigh after order tests:", "- **From D3a-02 to D3a-30**, to weigh after order tests:"),
    ("  - A02's joint openings and A01's bound, at D3c;", "  - the spine's three links (A02, A01, A03), at D3c;"),
    ("by G1 to G34 with G13a and G4a;", "by G1 to G35 with G13a and G4a;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
    print("written", P)
