#!/usr/bin/env python3
"""D3a-41: flag quoted segments in a spec file ('id|CLASS|evidence', segments as d3_spec_quotes.py finds them) that
stop where the source quote goes on with an apostrophe followed by a letter (a word such as don't cut short), in
the given quote files (window or cites output). Writes nothing.

  python3 out/_analysis/d3_trunc_check.py --spec out/_analysis/d3_rulings/A14-restrict-spec-2.txt --quotes F1 F2
"""
import argparse
import re

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)")
ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--quotes", nargs="+", required=True)
a = ap.parse_args()
quotes = []
for f in a.quotes:
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes.append(m.group(1))
n, bad = 0, []
for l in open(a.spec, encoding="utf-8"):
    if not l.strip():
        continue
    aid, ev = l.split("|", 1)[0], l.rstrip("\n").split("|", 2)[2]
    for s in SEG.findall(ev):
        n += 1
        for q in quotes:
            i = q.find(s)
            while i >= 0:
                rest = q[i + len(s):]
                if len(rest) >= 2 and rest[0] == "'" and rest[1].isalpha():
                    bad.append((aid, s))
                    break
                i = q.find(s, i + 1)
print("%d segments checked; cut at an apostrophe followed by a letter: %d" % (n, len(bad)))
for aid, s in bad:
    print("  %s | %s" % (aid, s))
