#!/usr/bin/env python3
"""D3a-34's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a34_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-33, 2026-10-19 UTC.", "Last written at D3a-34, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-33)", "## The return (D1a to D3a-34)"),
    ("A01 to A06 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, talk follows keeping in 141 of 265, sparing follows terms in 227 of 295, machine hands follow upkeep in 87 of 144.",
     "A01 to A07 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, talk follows keeping in 141 of 265, sparing follows terms in 227 of 295, machine hands follow upkeep in 87 of 144, marking follows a report in 131 of 156."),
    ("`adjudications.jsonl`: 27,427 lines ruled, 28,184 with re-rulings;",
     "`adjudications.jsonl`: 28,100 lines ruled, 28,860 with re-rulings;"),
    ("the stage's notes: G1 to G38 (five of them amended once)", "the stage's notes: G1 to G39 (five of them amended once)"),
    ("- **From D3a-02 to D3a-33**, to weigh after order tests:", "- **From D3a-02 to D3a-34**, to weigh after order tests:"),
    ("  - the spine's three links, A04's split, A05's theorised mechanism and A06's bound, at D3c;",
     "  - at D3c: the spine's three links, A04's split, A05's mechanism, A06's bound, A07's one-act rooms;"),
    ("by G1 to G38 with G13a and G4a;", "by G1 to G39 with G13a and G4a;"),
    ("- **The store.** `cite.py` takes one code per call.\n", ""),
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
