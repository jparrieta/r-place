#!/usr/bin/env python3
"""D3a-32's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a32_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-31, 2026-10-19 UTC. Stages A1 to C5 are done. The return",
     "Last written at D3a-32, 2026-10-19 UTC. The return"),
    ("## The return (D1a to D3a-31)", "## The return (D1a to D3a-32)"),
    ("- **D3a, by element.** All 25 standing elements are ruled whole. R01 and P05",
     "- **D3a, by element.** R01 and P05"),
    ("A01 to A04 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, talk follows keeping in 141 of 265.",
     "A01 to A05 stand uncorrected; 222 rooms start and call in one post; keeping follows a report in 308 of 331, talk follows keeping in 141 of 265, sparing follows terms in 227 of 295."),
    ("`adjudications.jsonl`: 26,012 lines ruled, 26,769 with re-rulings;",
     "`adjudications.jsonl`: 26,719 lines ruled, 27,476 with re-rulings;"),
    ("the stage's notes: G1 to G36 (five of them amended once)", "the stage's notes: G1 to G37 (five of them amended once)"),
    ("- **From D3a-02 to D3a-31**, to weigh after order tests:", "- **From D3a-02 to D3a-32**, to weigh after order tests:"),
    ("  - the spine's three links and A04's split, at D3c;",
     "  - the spine's three links, A04's split and A05's theorised mechanism, at D3c;"),
    ("by G1 to G36 with G13a and G4a;", "by G1 to G37 with G13a and G4a;"),
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
