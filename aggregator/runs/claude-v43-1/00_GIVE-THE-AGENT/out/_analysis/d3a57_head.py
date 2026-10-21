#!/usr/bin/env python3
"""D3a-57's head update: each replacement must match exactly once, or nothing is written. The re-check handoff
joins the return and the outputs, the hash the re-check is served is named, the re-check's open item names its
scope, and the next comparison is D3b's reading of the re-check's return.

  python3 out/_analysis/d3a57_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-56, 2026-10-21 UTC.", "Written at D3a-57, 2026-10-21 UTC."),
    ("Moves 172 to 196 moved the hash; D3c refreezes it.",
     "Moves 172 to 196 moved the hash; the re-check is served 46384686…; D3c freezes it."),
    ("## The return (D1a to D3a-56)", "## The return (D1a to D3a-57)"),
    ("picturegame is out-of-scope.", "picturegame is out-of-scope. **D3a-57.** All 705 rooms sent to the re-check."),
    ("verdicts 868 (163 rulings);", "verdicts 868;"),
    ("- **From D3a-02 to D3a-56**, to weigh after order tests:", "- **From D3a-02 to D3a-57**, to weigh after order tests:"),
    ("**The re-check:** rooms relying on rewritten R01, P05, P22, P21 and A21 go to it; two R01 elaborations wait for clustering.",
     "**The re-check:** all 705 rooms; two R01 elaborations wait for clustering."),
    ("The re-check (§5): the model's prose, `recheck-scope.json` and the handoff, closed with `--cut packets-out`.",
     "D3b: the re-check's before-and-after ledgers, once returned."),
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
