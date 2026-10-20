#!/usr/bin/env python3
"""D3a-35's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a35_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-34, 2026-10-20 UTC.", "Last written at D3a-35, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-34)", "## The return (D1a to D3a-35)"),
    ("A01 to A07 stand uncorrected;", "A01 to A08 stand uncorrected;"),
    ("marking follows a report in 131 of 156.", "marking follows a report in 131 of 156, records follow marking in 232 of 240."),
    ("`adjudications.jsonl`: 28,100 lines ruled, 28,860 with re-rulings;",
     "`adjudications.jsonl`: 28,783 lines ruled, 29,543 with re-rulings;"),
    ("the stage's notes: G1 to G39 (five of them amended once)", "the stage's notes: G1 to G40 (five of them amended once)"),
    ("- **From D3a-02 to D3a-34**, to weigh after order tests:", "- **From D3a-02 to D3a-35**, to weigh after order tests:"),
    ("A06's bound, A07's one-act rooms;", "A06's bound, A07's and A08's one-act rooms;"),
    ("by G1 to G39 with G13a and G4a;", "by G1 to G40 with G13a and G4a;"),
    ("Check a claim against its source before writing it, and read a check's format before writing a ledger it reads.",
     "Check a claim against its source, and a check's format, before writing."),
    ("A Bash output above about 30 KB is cut; measure first.", "Bash output above 30 KB is cut; measure first."),
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
