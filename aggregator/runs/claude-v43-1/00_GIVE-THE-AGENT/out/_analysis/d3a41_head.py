#!/usr/bin/env python3
"""D3a-41's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, some list items are joined into the item before them (no item dropped).

  python3 out/_analysis/d3a41_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-40, 2026-10-20 UTC.", "Last written at D3a-41, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-40)", "## The return (D1a to D3a-41)"),
    ("A01 to A13 stand uncorrected;", "A01 to A14 stand uncorrected;"),
    ("help follows upkeep, 155 of 197.",
     "help follows upkeep, 155 of 197, and terms, 179 of 186 (124 more trade in one offer)."),
    ("`adjudications.jsonl`: 32,227 lines ruled, 32,998 with re-rulings; the stage's notes: G1 to G45",
     "`adjudications.jsonl`: 32,893 lines ruled, 33,664 with re-rulings; the stage's notes: G1 to G46"),
    ("- **From D3a-02 to D3a-40**, to weigh after order tests:", "- **From D3a-02 to D3a-41**, to weigh after order tests:"),
    ("A13's second path, spare-capacity help and edited record ends;",
     "A13's second path, spare-capacity help and edited record ends; A14's one offer beside F-020;"),
    ("The unruled groups (other arrows, candidates, dimension lines), by G1 to G45 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G46 with G13a and G4a;"),
    # joins
    ("run at xhigh effort.\n- \"Keep the room", "run at xhigh effort. \"Keep the room"),
    ("more than one dimension.\n- **QD2-001", "more than one dimension. **QD2-001"),
    ("restrict lines.\n- **QD3-007:**", "restrict lines. **QD3-007:**"),
    ("for the clustering.\n- **QD3-008 (J):**", "for the clustering. **QD3-008 (J):**"),
    ("and why.\"\n- **Pass 1 (C2a-01).**", "and why.\" **Pass 1 (C2a-01).**"),
    ("over the whole scheme.\n- **QC1-002", "over the whole scheme. **QC1-002"),
    ("(J's floor).\n- **QC1-003", "(J's floor). **QC1-003"),
    ("the separate concept that carries it.\n- **also_present", "the separate concept that carries it. **also_present"),
    ("count in the bag test.\n- **Lone B1 themes", "count in the bag test. **Lone B1 themes"),
    ("each with three concepts of its own.\n- **The bound (J, 13:47).**",
     "each with three concepts of its own. **The bound (J, 13:47).**"),
    ("before writing.\n- **Logging.**", "before writing. **Logging.**"),
    ("before the closing line.\n- **Ledger formats.**", "before the closing line. **Ledger formats.**"),
    ("instead.\n- **Output.**", "instead. **Output.**"),
    ("measure first.\n- **Files.**", "measure first. **Files.**"),
    ("misses the host rooms.\n- **From C3:**", "misses the host rooms. **From C3:**"),
    ("the four declined reads.\n- **From C2:**", "the four declined reads. **From C2:**"),
    ("the claim untested for order.\n- **From C1 and B1:**", "the claim untested for order. **From C1 and B1:**"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
