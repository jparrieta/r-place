#!/usr/bin/env python3
"""D3a-47's head update: each replacement must match exactly once, or nothing is written. A20's result joins the
return's list. To stay within 3,000 words, the next comparison names the candidates and dimension lines without
'unruled groups' (d3_unruled_by_element.py finds no arrow with unruled lines), 'leg' and 'Last' drop, and the kappa
takes a comma for 'of'.

  python3 out/_analysis/d3a47_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-46, 2026-10-20 UTC.", "Written at D3a-47, 2026-10-21 UTC."),
    ("## The return (D1a to D3a-46)", "## The return (D1a to D3a-47)"),
    ("A01 to A19 stand uncorrected;", "A01 to A20 stand uncorrected;"),
    ("coalitions follow upkeep, 49 of 67; an attack follows a call",
     "coalitions follow upkeep, 49 of 67; host lines follow calls, 148 of 164; an attack follows a call"),
    ("`adjudications.jsonl`: 36,189 lines ruled, 36,967 with re-rulings; the stage's notes: G1 to G51 (eight of them "
     "amended once)",
     "`adjudications.jsonl`: 36,889 lines ruled, 37,668 with re-rulings; the stage's notes: G1 to G52 (nine of them "
     "amended once)"),
    ("- **From D3a-02 to D3a-46**, to weigh after order tests:", "- **From D3a-02 to D3a-47**, to weigh after order tests:"),
    ("A17's to A19's wording; P09's:", "A17's to A20's wording; P09's:"),
    ("the border coders' kappa of 0.19", "the border coders' kappa, 0.19"),
    ("The unruled groups (A20, candidates, dimension lines), by the stage's rules; then the `propose` lines. "
     "The split and 19 story-miss rooms wait for the verdicts leg.",
     "The candidates and dimension lines, by the stage's rules; then the `propose` lines. "
     "The split and 19 story-miss rooms wait for the verdicts."),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
