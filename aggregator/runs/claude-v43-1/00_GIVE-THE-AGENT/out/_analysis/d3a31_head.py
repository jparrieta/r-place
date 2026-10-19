#!/usr/bin/env python3
"""D3a-31's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a31_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-30, 2026-10-19 UTC.", "Last written at D3a-31, 2026-10-19 UTC."),
    ("## The return (D1a to D3a-30)", "## The return (D1a to D3a-31)"),
    ("A02, A01 and A03 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331.",
     "A01 to A04 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, talk follows keeping in 141 of 265."),
    ("`adjudications.jsonl`: 25,344 lines ruled, 26,101 with re-rulings;",
     "`adjudications.jsonl`: 26,012 lines ruled, 26,769 with re-rulings;"),
    ("the stage's notes: G1 to G35 (five of them amended once)", "the stage's notes: G1 to G36 (five of them amended once)"),
    ("- **From D3a-02 to D3a-30**, to weigh after order tests:", "- **From D3a-02 to D3a-31**, to weigh after order tests:"),
    ("  - the spine's three links (A02, A01, A03), at D3c;", "  - the spine's three links and A04's split, at D3c;"),
    ("P19's form (9; 5 allied host ties); A04's bound (21); P06's form (14);", "P19's form (9; 5 allied host ties); P06's form (14);"),
    ("by G1 to G35 with G13a and G4a;", "by G1 to G36 with G13a and G4a;"),
    ("## Stage C2, in short", "## Stage C2"),
    ("## Stage C1, in short (carry the rulings)", "## Stage C1 (carry the rulings)"),
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
