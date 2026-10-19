#!/usr/bin/env python3
"""D3a-33: check that every single-quoted segment in a spec file ('id|CLASS|evidence') is an exact substring of a
quote that cite.py printed for that line's room, in the given quote files (window or cites output). A segment starts
at a ' after a space, '(' or '|', and ends at the first ' followed by a space, a comma, a semicolon, a full stop, a
closing bracket or the line's end; so an apostrophe inside a word does not end it. Prints each segment not found.
Writes nothing.

  python3 out/_analysis/d3_spec_quotes.py --spec out/_analysis/d3_rulings/A06-inst-spec.txt \
      --quotes out/_analysis/d3_wq_A06_492_000.txt out/_analysis/d3_wq_A06_492_020.txt
"""
import argparse
import re
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--quotes", nargs="+", required=True)
a = ap.parse_args()

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
quotes = defaultdict(list)
for f in a.quotes:
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quotes[m.group(2)].append(m.group(1))

SEG = re.compile(r"(?:(?<=[\s(|]))'(.+?)'(?=[\s,;.)]|$)")
lines = segs = bad = 0
for l in open(a.spec, encoding="utf-8"):
    if not l.strip():
        continue
    lines += 1
    aid, _cls, ev = l.rstrip("\n").split("|", 2)
    room = aid.rsplit("-", 1)[0]
    for s in SEG.findall(ev):
        segs += 1
        if not any(s in q for q in quotes.get(room, [])):
            bad += 1
            print("NOT FOUND %s: '%s'" % (aid, s))
print("%d lines, %d quoted segments, %d not found" % (lines, segs, bad))
