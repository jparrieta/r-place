#!/usr/bin/env python3
"""D3a-36: check the hours typed in a spec file against the quote files. For every concept id in a row's evidence,
the first 'h+N' after it and before the next concept id is compared with the hour cite.py printed for that concept
in the quote files (lines as d3_spec_quotes.py reads them). An hour given for a concept that a row cites from
another line (no quote in the files) is listed apart. Writes nothing.

    python3 out/_analysis/d3_spec_hours.py --spec out/_analysis/d3_rulings/A09-restrict-spec.txt --quotes F1 F2
"""
import argparse, re

QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\].*?\bh\+(\d+(?:\.\d+)?)')
ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--quotes", nargs="+", required=True)
a = ap.parse_args()
H = {}
for f in a.quotes:
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            H[(m.group(2), m.group(3))] = m.group(4)
checked, bad, other = 0, [], []
for l in open(a.spec, encoding="utf-8"):
    if not l.strip():
        continue
    aid, _, ev = l.rstrip("\n").split("|")[:3]
    room = aid.rsplit("-", 1)[0]
    toks = list(re.finditer(r"\b(c\d{4})\b", ev))
    for i, t in enumerate(toks):
        end = toks[i + 1].start() if i + 1 < len(toks) else len(ev)
        m = re.search(r"h\+(\d+(?:\.\d+)?)", ev[t.end():end])
        if not m:
            continue
        want = H.get((room, t.group(1)))
        if want is None:
            other.append("%s %s h+%s" % (aid, t.group(1), m.group(1)))
        elif float(want) != float(m.group(1)):
            bad.append("%s %s typed h+%s, cite.py h+%s" % (aid, t.group(1), m.group(1), want))
        else:
            checked += 1
print("hours checked and matching: %d; mismatches: %d; hours for concepts not in the quote files: %d" % (
    checked, len(bad), len(other)))
for x in bad:
    print("MISMATCH " + x)
for x in other:
    print("NOT IN FILES " + x)
