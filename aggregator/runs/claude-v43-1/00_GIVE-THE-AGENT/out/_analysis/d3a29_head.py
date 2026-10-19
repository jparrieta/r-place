#!/usr/bin/env python3
"""D3a-29's head update: each replacement must match exactly once, or nothing is written.

  python3 out/_analysis/d3a29_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-28, 2026-10-19 UTC. Stages A1 to C5 are done; stage B is frozen.",
     "Last written at D3a-29, 2026-10-19 UTC. Stages A1 to C5 are done."),
    ("## The return (D1a to D3a-28)", "## The return (D1a to D3a-29)"),
    ("A02 stands uncorrected; 222 rooms start and call in one post.",
     "A02 and A01 stand uncorrected: 222 rooms start and call in one post; in 142 of 407 the call follows a start."),
    ("`adjudications.jsonl`: 23,980 lines ruled, 24,737 with re-rulings;",
     "`adjudications.jsonl`: 24,656 lines ruled, 25,413 with re-rulings;"),
    ("the stage's notes: G1 to G33 (G20, G21, G23, G25, G33 amended once each)",
     "the stage's notes: G1 to G34 (five of them amended once)"),
    ("- **From D3a-02 to D3a-28**, to weigh after order tests:",
     "- **From D3a-02 to D3a-29**, to weigh after order tests:"),
    ("  - A02's joint openings, failed by C2's test (D3c);",
     "  - A02's joint openings and A01's bound, at D3c;"),
    ("about 50 lines from closed groups, with the pairs left for the handler's kappa.",
     "about 50 lines, pairs left for the handler's kappa."),
    ("by G1 to G33 with G13a and G4a;", "by G1 to G34 with G13a and G4a;"),
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
