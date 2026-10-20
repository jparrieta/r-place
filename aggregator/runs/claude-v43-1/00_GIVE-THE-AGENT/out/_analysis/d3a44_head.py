#!/usr/bin/env python3
"""D3a-44's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, two counts are folded into one clause (no item dropped).

  python3 out/_analysis/d3a44_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-43, 2026-10-20 UTC.", "Last written at D3a-44, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-43)", "## The return (D1a to D3a-44)"),
    ("A01 to A16 stand uncorrected;", "A01 to A17 stand uncorrected;"),
    ("restraint follows an attack, 319 of 322.", "restraint (319 of 322) and terms (213 of 230) follow an attack."),
    ("`adjudications.jsonl`: 34,246 lines ruled, 35,019 with re-rulings; the stage's notes: G1 to G48",
     "`adjudications.jsonl`: 34,896 lines ruled, 35,669 with re-rulings; the stage's notes: G1 to G49"),
    ("- **From D3a-02 to D3a-43**, to weigh after order tests:", "- **From D3a-02 to D3a-44**, to weigh after order tests:"),
    ("A16's reasons, lone bound and visitors' calls; P09's:",
     "A16's reasons, lone bound and visitors' calls; A17's gloss and bound; P09's:"),
    ("by G1 to G48 with G13a and G4a;", "by G1 to G49 with G13a and G4a;"),
    ("The same room meets the attack call with sparing, refusal or apology [A16] and border talk [A17].",
     "Rooms meet attack calls with restraint [A16] or terms [A17]."),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
