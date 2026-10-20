#!/usr/bin/env python3
"""D3a-40's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, some nested lists are joined into single lines (no item dropped).

  python3 out/_analysis/d3a40_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-39, 2026-10-20 UTC.", "Last written at D3a-40, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-39)", "## The return (D1a to D3a-40)"),
    ("A01 to A12 stand uncorrected;", "A01 to A13 stand uncorrected;"),
    ("joins come bare, 392 of 411.", "joins come bare, 392 of 411; help follows upkeep, 155 of 197."),
    ("- **D3a outputs:**\n  - `adjudications.jsonl`: 31,569 lines ruled, 32,338 with re-rulings;\n  - the stage's notes: G1 to G44",
     "- **D3a outputs:** `adjudications.jsonl`: 32,227 lines ruled, 32,998 with re-rulings; the stage's notes: G1 to G45"),
    ("Short cohesive sentences.\"\n- Ask Orwell's", "Short cohesive sentences.\" Ask Orwell's"),
    ("six questions.\n- Follow ASD-STE100", "six questions. Follow ASD-STE100"),
    ("the act named.\n- Describe what", "the act named. Describe what"),
    ("\"twenty themes at most\".\n- **The not-flagged bag", "\"twenty themes at most\". **The not-flagged bag"),
    ("my files keep room ids.\n- **Stage B.**", "my files keep room ids. **Stage B.**"),
    ("- **From D3a-02 to D3a-39**, to weigh after order tests:", "- **From D3a-02 to D3a-40**, to weigh after order tests:"),
    ("where the room decides (5);\n  - P13's:", "where the room decides (5); P13's:"),
    ("canvas-born rooms;\n  - P17's: prior ties", "canvas-born rooms; P17's: prior ties"),
    ("A12's reason test and starts joined;",
     "A12's reason test and starts joined; A13's second path, spare-capacity help and edited record ends;"),
    ("(6, A18);\n  - P10's and K02's", "(6, A18); P10's and K02's"),
    ("kin ties, 3);\n  - calls recurring after a loss", "kin ties, 3); calls recurring after a loss"),
    ("reopening calls or design;\n  - neighbours (A04, A13's giver", "reopening calls or design; neighbours (A04, A13's giver"),
    ("as help or as keepers;\n  - P12's records as proof", "as help or as keepers; P12's records as proof"),
    ("takeovers (T4-002);\n  - bare refusals (math-011", "takeovers (T4-002); bare refusals (math-011"),
    ("scripts held in 6;\n  - K01's canvas-call clause", "scripts held in 6; K01's canvas-call clause"),
    ("The unruled groups (other arrows, candidates, dimension lines), by G1 to G44 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G45 with G13a and G4a;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
