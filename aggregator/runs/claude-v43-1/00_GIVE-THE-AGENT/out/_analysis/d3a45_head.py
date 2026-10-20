#!/usr/bin/env python3
"""D3a-45's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, the next comparison names the stage's rules in place of their list, which 'Where the run stands' keeps. The
count of rules amended once is corrected from a scripted listing of the notes' amendment headings: seven before G50
(G16, G20, G21, G23, G25, G33, G42), so eight with G50.

  python3 out/_analysis/d3a45_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-44, 2026-10-20 UTC.", "Last written at D3a-45, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-44)", "## The return (D1a to D3a-45)"),
    ("A01 to A17 stand uncorrected;", "A01 to A18 stand uncorrected;"),
    ("restraint (319 of 322) and terms (213 of 230) follow an attack.",
     "restraint (319 of 322), terms (213 of 230) and taunts (169 of 177) follow an attack."),
    ("`adjudications.jsonl`: 34,896 lines ruled, 35,669 with re-rulings; the stage's notes: G1 to G49 (six of them "
     "amended once)",
     "`adjudications.jsonl`: 35,543 lines ruled, 36,316 with re-rulings; the stage's notes: G1 to G50 (eight of them "
     "amended once)"),
    ("- **From D3a-02 to D3a-44**, to weigh after order tests:", "- **From D3a-02 to D3a-45**, to weigh after order tests:"),
    ("A17's gloss and bound; P09's:", "A17's and A18's wording; P09's:"),
    ("by G1 to G49 with G13a and G4a;", "by the stage's rules;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
