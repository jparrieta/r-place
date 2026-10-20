#!/usr/bin/env python3
"""D3a-46's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, the next comparison names A20 in place of 'other arrows' (d3_unruled_by_element.py finds A20 the only arrow
with unruled lines) and joins its last sentence, and the label of J's QC2-002 ruling drops its description; J's words
are kept whole.

  python3 out/_analysis/d3a46_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-45, 2026-10-20 UTC.", "Last written at D3a-46, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-45)", "## The return (D1a to D3a-46)"),
    ("A01 to A18 stand uncorrected;", "A01 to A19 stand uncorrected;"),
    ("(124 more trade in one offer); an attack follows a call",
     "(124 more trade in one offer); coalitions follow upkeep, 49 of 67; an attack follows a call"),
    ("`adjudications.jsonl`: 35,543 lines ruled, 36,316 with re-rulings; the stage's notes: G1 to G50 (eight of them "
     "amended once)",
     "`adjudications.jsonl`: 36,189 lines ruled, 36,967 with re-rulings; the stage's notes: G1 to G51 (eight of them "
     "amended once)"),
    ("- **From D3a-02 to D3a-45**, to weigh after order tests:", "- **From D3a-02 to D3a-46**, to weigh after order tests:"),
    ("A17's and A18's wording; P09's:", "A17's to A19's wording; P09's:"),
    ("- **J's ruling on QC2-002 (two spent sentences cut):**", "- **J's ruling on QC2-002:**"),
    ("The unruled groups (other arrows, candidates, dimension lines), by the stage's rules; then the `propose` lines. "
     "The split rooms and the 19 story-miss rooms wait for the verdicts leg.",
     "The unruled groups (A20, candidates, dimension lines), by the stage's rules; then the `propose` lines. "
     "The split and 19 story-miss rooms wait for the verdicts leg."),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
