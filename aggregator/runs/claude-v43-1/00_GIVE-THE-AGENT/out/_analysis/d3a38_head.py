#!/usr/bin/env python3
"""D3a-38's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a38_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-37, 2026-10-20 UTC.", "Last written at D3a-38, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-37)", "## The return (D1a to D3a-38)"),
    ("A01 to A10 stand uncorrected;", "A01 to A11 stand uncorrected;"),
    ("moves follow doubt, 112 of 159.",
     "moves follow doubt, 112 of 159; a layout answers design talk in-thread, 111 of 228."),
    ("Attacks [P09] show in 510 of 705 rooms, taunts [P18] in 404, moves after a loss [P10] in 300, too few hands or "
     "room [K02] in 520, machine hands [P14] in 320, carrying on [P13] in 292, the host's line [P20] in 310, "
     "coalitions [P17] in 383, bare answers [P15] in 579, decided order [C01] in 136, an old tie naming the rival "
     "[C02] in 112, and who may commit the room [P21] in 163.",
     "Rooms of 705: attacks [P09] 510, taunts [P18] 404, moves after a loss [P10] 300, too few hands or room [K02] "
     "520, machine hands [P14] 320, carrying on [P13] 292, the host's line [P20] 310, coalitions [P17] 383, bare "
     "answers [P15] 579, decided order [C01] 136, an old tie naming the rival [C02] 112, who may commit the room "
     "[P21] 163."),
    ("`adjudications.jsonl`: 30,144 lines ruled, 30,906 with re-rulings;",
     "`adjudications.jsonl`: 30,822 lines ruled, 31,590 with re-rulings;"),
    ("the stage's notes: G1 to G42 (six of them amended once)", "the stage's notes: G1 to G43 (six of them amended once)"),
    ("- **Questions:** none open.", "- **Questions:** QD3-008 open (A11's 'settled')."),
    ("- **From D3a-02 to D3a-37**, to weigh after order tests:", "- **From D3a-02 to D3a-38**, to weigh after order tests:"),
    ("move-first rooms, two-way checks;", "move-first rooms, two-way checks; A11's template-first rooms;"),
    ("The unruled groups (other arrows, candidates, dimension lines), by G1 to G42 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G43 with G13a and G4a;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
