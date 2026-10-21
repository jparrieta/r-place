#!/usr/bin/env python3
"""D3a-56's head update: each replacement must match exactly once, or nothing is written. The verdict rulings and
the uncomposed room join the return, the notes reach G60 with its amendment, the verdict ledger and uncomposed-D.md
join the outputs, and the next comparison is the re-check handoff (section 5). To stay under 3,000 words, the
B1 and C1 carried items and T3-017's scope item (now written in uncomposed-D.md) leave the head; the notes keep them.

  python3 out/_analysis/d3a56_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-55, 2026-10-21 UTC.", "Written at D3a-56, 2026-10-21 UTC."),
    ("## The return (D1a to D3a-55)", "## The return (D1a to D3a-56)"),
    ("729 accepted into 15 candidates, 178 held by the model, 455 particulars or not shown.",
     "729 accepted into 15 candidates, 178 held by the model, 455 particulars or not shown. **D3a-56.** Split "
     "verdicts, 163: 61 compose, 102 with residue that the candidates state; picturegame is out-of-scope."),
    ("the notes: G1 to G59 (eleven of them amended once)", "the notes: G1 to G60 (twelve of them amended once)"),
    ("**Ledgers (lines):** tier history 561;", "**Ledgers (lines):** verdicts 868 (163 rulings); tier history 561;"),
    ("- **From D3a-02 to D3a-55**, to weigh after order tests:", "- **From D3a-02 to D3a-56**, to weigh after order tests:"),
    ("the candidates' order tests; T3-017's 251 lines (scope);", "the candidates' order tests;"),
    (" **From C1 and B1:** the form-pass findings; the B1 bag counts.", ""),
    ("The verdicts and the uncomposed rooms (§4), with the 19 story-miss rooms.",
     "The re-check (§5): `MODEL-D3.md`, `recheck-scope.json` and the handoff, closed with `--cut packets-out`."),
]
t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
    print("wrote", P)
