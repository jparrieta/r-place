#!/usr/bin/env python3
"""D3a-43: the quote segments that d3_spec_quotes.py does not read (a segment that closes before ':' or ']'), which
d3_trunc_check.py does read. Each such segment is looked up in the cited concept's words in the window's quote file,
and printed with FOUND or NOT FOUND. Writes nothing.

  python3 out/_analysis/d3_a16_seg_gap.py --spec <spec> --quotes <window quote file>
"""
import argparse
import re

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--quotes", required=True)
a = ap.parse_args()

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]')
NARROW = re.compile(r"(?:(?<=[\s(|]))'(.+?)'(?=[\s,;.)]|$)")
BROAD = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)")

words = {}
for l in open(a.quotes, encoding="utf-8"):
    m = QLINE.match(l)
    if m:
        words.setdefault(m.group(2), []).append(m.group(1))

n = 0
for l in open(a.spec, encoding="utf-8"):
    if "|" not in l:
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    room = aid.rsplit("-", 1)[0]
    narrow = set(NARROW.findall(ev))
    for s in BROAD.findall(ev):
        if s in narrow:
            continue
        n += 1
        ok = any(s in w for w in words.get(room, []))
        print("%s %s: '%s'" % ("FOUND" if ok else "NOT FOUND", aid, s))
print("segments the quote check does not read: %d" % n)
