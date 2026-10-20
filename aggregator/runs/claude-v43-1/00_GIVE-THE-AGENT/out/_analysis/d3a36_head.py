#!/usr/bin/env python3
"""D3a-36's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a36_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-35, 2026-10-20 UTC.", "Last written at D3a-36, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-35)", "## The return (D1a to D3a-36)"),
    ("A01 to A08 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, "
     "talk follows keeping in 141 of 265, sparing follows terms in 227 of 295, machine hands follow upkeep in 87 of "
     "144, marking follows a report in 131 of 156, records follow marking in 232 of 240.",
     "A01 to A09 stand uncorrected; 222 rooms start and call in one post; keeping follows a report, 308 of 331; "
     "talk follows keeping, 141 of 265; sparing follows terms, 227 of 295; machine hands follow upkeep, 87 of 144; "
     "marking follows a report, 131 of 156; records follow marking, 232 of 240; carrying on follows a record, 163 "
     "of 184."),
    ("`adjudications.jsonl`: 28,783 lines ruled, 29,543 with re-rulings;",
     "`adjudications.jsonl`: 29,467 lines ruled, 30,229 with re-rulings;"),
    ("the stage's notes: G1 to G40 (five of them amended once)", "the stage's notes: G1 to G41 (five of them amended once)"),
    ("- **From D3a-02 to D3a-35**, to weigh after order tests:", "- **From D3a-02 to D3a-36**, to weigh after order tests:"),
    ("A06's bound, A07's and A08's one-act rooms;",
     "A06's bound, A07's to A09's one-act and carry-first rooms, two-way order checks;"),
    ("The unruled groups (the other arrows, the candidates, the dimension lines), by G1 to G40 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G41 with G13a and G4a;"),
    ("contest which version of the canvas and of the event is kept [P22]",
     "contest which version of the canvas and event is kept [P22]"),
    ("- **Output limits.** Bash output above 30 KB is cut; measure first.",
     "- **Output.** Bash output above 30 KB is cut; measure first."),
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
