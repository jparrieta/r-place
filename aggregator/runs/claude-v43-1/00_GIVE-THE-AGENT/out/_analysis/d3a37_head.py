#!/usr/bin/env python3
"""D3a-37's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a37_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-36, 2026-10-20 UTC.", "Last written at D3a-37, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-36)", "## The return (D1a to D3a-37)"),
    ("A01 to A09 stand uncorrected;", "A01 to A10 stand uncorrected;"),
    ("carrying on follows a record, 163 of 184.",
     "carrying on follows a record, 163 of 184; moves follow doubt, 112 of 159."),
    ("`adjudications.jsonl`: 29,467 lines ruled, 30,229 with re-rulings;",
     "`adjudications.jsonl`: 30,144 lines ruled, 30,906 with re-rulings;"),
    ("the stage's notes: G1 to G41 (five of them amended once)", "the stage's notes: G1 to G42 (six of them amended once)"),
    ("- **From D3a-02 to D3a-36**, to weigh after order tests:", "- **From D3a-02 to D3a-37**, to weigh after order tests:"),
    ("A07's to A09's one-act and carry-first rooms, two-way order checks;",
     "A07's to A10's one-act, carry-first and move-first rooms, two-way checks;"),
    ("P10's and K02's (A10, F-019): copies before a loss; doubt before a move or a smaller design; giving up after doubt;",
     "P10's and K02's (A10, F-019): copies before a loss; no move (40) or giving up (12) after doubt;"),
    ("K01's canvas-call clause (doubted in 3 rooms); doubt costing uptake (9 rooms).",
     "K01's canvas-call clause (doubted in 3); doubt costing uptake (9)."),
    ("The unruled groups (other arrows, candidates, dimension lines), by G1 to G41 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G42 with G13a and G4a;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
