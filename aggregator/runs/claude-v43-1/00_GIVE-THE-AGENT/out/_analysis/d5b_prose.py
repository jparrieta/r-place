#!/usr/bin/env python3
"""D5b: WRITING.md checks on my own prose: em and en dashes, contractions and 'serves as' outside quoted text.
Quoted text (between straight double quotes) is removed before the contraction check.

    python3 out/_analysis/d5b_prose.py out/waterfall-D5.md ...
"""
import re, sys

CON = re.compile(r"\b(can't|don't|isn't|it's|won't|aren't|doesn't|didn't|i'm|we're|they're|that's|there's|wasn't|weren't)\b", re.I)
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8").read()
    bare = re.sub(r'"[^"\n]*"', '""', t)
    dashes = [(i + 1, l[:70]) for i, l in enumerate(t.split("\n")) if "—" in l or "–" in l]
    cons = [(i + 1, m.group(0)) for i, l in enumerate(bare.split("\n")) for m in CON.finditer(l)]
    serves = [(i + 1, l[:70]) for i, l in enumerate(bare.split("\n")) if re.search(r"\bserves? as\b|\bserved as\b", l)]
    print(p, "dashes", len(dashes), dashes[:5], "contractions", len(cons), cons[:8], "serves as", len(serves), serves[:3])
