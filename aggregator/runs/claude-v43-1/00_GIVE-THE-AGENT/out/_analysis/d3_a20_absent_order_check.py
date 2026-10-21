#!/usr/bin/env python3
"""D3a-47: check the order each A20 absent reject states. For every REJ row of A20-absent-rows.txt, the first two
concept ids that carry an hour ('cNNNN ... (h+N)', as d3_spec_hours.py pairs them) are taken as the first call and the
first line; the row passes if the call's hour is below the line's. A row whose words place the order without the
line's hour (no second hour) is listed apart for a second look. Writes nothing.

  python3 out/_analysis/d3_a20_absent_order_check.py
"""
import re

ok, bad, apart = 0, [], []
for l in open("out/_analysis/d3_rulings/A20-absent-rows.txt", encoding="utf-8"):
    if not l.strip():
        continue
    aid, cls, ev = l.rstrip("\n").split("|", 2)
    if cls != "REJ":
        continue
    toks = list(re.finditer(r"\b(c\d{4})\b", ev))
    hours = []
    for i, t in enumerate(toks):
        end = toks[i + 1].start() if i + 1 < len(toks) else len(ev)
        m = re.search(r"h\+(\d+(?:\.\d+)?)", ev[t.end():end])
        if m:
            hours.append((t.group(1), float(m.group(1))))
    if len(hours) < 2:
        apart.append("%s %s" % (aid, hours))
        continue
    (c1, h1), (c2, h2) = hours[0], hours[1]
    if h1 < h2:
        ok += 1
    else:
        bad.append("%s %s h+%s, %s h+%s" % (aid, c1, h1, c2, h2))
print("rejects whose first call comes before their first line: %d" % ok)
print("rejects out of order: %d" % len(bad))
for b in bad:
    print("  " + b)
print("rejects with fewer than two hours: %d" % len(apart))
for x in apart:
    print("  " + x)
