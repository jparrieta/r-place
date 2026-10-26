#!/usr/bin/env python3
"""D5: before assembly, check the parts' section order as validate.py reads it.
Headings ('## n.') must name the stage's sections in order; no bold-led line (after an optional '- ')
may carry a section word that belongs to another section, anywhere in the line (validate.py reads the
whole line, so 'doubt' in a paragraph's body before section 13 breaks the order). Written at D5a-24.

    python3 out/_analysis/d5_heading_check.py part1.md part2.md ...
"""
import re
import sys

R = ['narrative|how these rooms organized', 'what the branch does', 'does differently', 'concepts it employs',
     'composition here', 'how the model runs', 'relationship that runs differently|one relationship',
     'over-? ?and under-?represented|over-represented', 'arrows present|not-testable-here',
     'representative members', 'nearest branch', 'form test', 'doubt']
last, flags, heads = -1, 0, 0
for p in sys.argv[1:]:
    for i, l in enumerate(open(p, encoding="utf-8")):
        s = l.strip()
        if s.startswith('- '):
            s = s[2:]
        if not (s.startswith('#') or s.startswith('**')):
            continue
        hits = [j for j, r in enumerate(R) if re.search(r, s.lower())]
        if s.startswith('## '):
            if hits:
                last = min(hits)
                heads += 1
            continue
        bad = [j for j in hits if j != last]
        if bad:
            print('FLAG', p, i + 1, 'section', last, 'carries', [R[j] for j in bad], '|', s[:120])
            flags += 1
print('headings', heads, 'flags', flags)
