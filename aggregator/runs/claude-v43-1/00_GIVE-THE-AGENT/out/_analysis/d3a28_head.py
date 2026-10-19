#!/usr/bin/env python3
"""D3a-28's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a28_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-27, 2026-10-19 UTC.", "Last written at D3a-28, 2026-10-19 UTC."),
    ("## The return (D1a to D3a-27)", "## The return (D1a to D3a-28)"),
    ("A21 stands bounded (move 176): the agreement comes first in 114 of 162 rooms.",
     "A21 stands bounded (move 176): the agreement comes first in 114 of 162 rooms. A02 stands uncorrected; "
     "222 rooms start and call in one post."),
    ("and who may commit the room [P21] in 162.", "and who may commit the room [P21] in 163."),
    ("**QC1-003 (the handler, under J's delegation).**", "**QC1-003 (the handler, for J).**"),
    ("Decided order is coded in 46 rooms [C01, F-006]; the return shows it in about 119.",
     "Decided order is coded in 46 rooms [C01, F-006]."),
    ("- **Move 175 (D3a-26, developing working hypotheses).** P21 stands; its frame reads 'dispute, or state the "
     "limits of'.\n- **Move 174 (D3a-06, developing working hypotheses).** P22 stands; its range names one member "
     "correcting a claim.",
     "- **Moves 174 and 175 (D3a-06, D3a-26, developing working hypotheses).** P22's range names one member "
     "correcting a claim; P21's frame reads 'dispute, or state the limits of'."),
    ("`adjudications.jsonl`: 23,334 lines ruled, 24,091 with re-rulings;",
     "`adjudications.jsonl`: 23,980 lines ruled, 24,737 with re-rulings;"),
    ("the stage's notes: G1 to G32 (G20, G21, G23, G25 amended once each)",
     "the stage's notes: G1 to G33 (G20, G21, G23, G25, G33 amended once each)"),
    ("- **From D3a-02 to D3a-27**, to weigh after order tests:",
     "- **From D3a-02 to D3a-28**, to weigh after order tests:"),
    ("  - P15's: its edge with P11 and P03; joins waiting on a visible start (A02);",
     "  - P15's: its edge with P11 and P03; joins waiting on a visible start (criticalrole);\n"
     "  - A02's joint openings, failed by C2's test (D3c);"),
    ("**QC1-002 (J).** Lean to one placement. A second theme needs three concepts or more of its own; J's floor is "
     "three concepts.",
     "**QC1-002 (J).** Lean to one placement; a second theme needs three concepts of its own (J's floor)."),
    ("by G1 to G32 with G13a and G4a;", "by G1 to G33 with G13a and G4a;"),
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
