#!/usr/bin/env python3
"""D3a-50's head update: each replacement must match exactly once, or nothing is written. The order test's result
joins the open list as a carried item, and the next comparison drops the test.

  python3 out/_analysis/d3a50_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-49, 2026-10-21 UTC.", "Written at D3a-50, 2026-10-21 UTC."),
    ("- **From D3a-02 to D3a-49**, to weigh after order tests:", "- **From D3a-02 to D3a-50**, to weigh after order tests:"),
    ("doubt costing uptake (9).", "doubt costing uptake (9); P05's telling naming P06 (attributions in 7 of 12 tellings)."),
    ("P06's order test against P05; K03, K04, P19 and dimension lines;", "K03, K04, P19 and dimension lines;"),
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
