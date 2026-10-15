#!/usr/bin/env python3
"""C5c-09: tally the codes of a whole-room read (A05 or A14) against the order in each room. The order is read from the
read file (c2_first_concepts.py output): it holds where the first FROM concept's hour is before the first TO concept's
hour. Applies the rule logged first (diary, C5c-09): the share of the line (or channel) code among line plus tacit (or
channel plus apart), where the order holds and where it fails. Writes nothing.

    python3 out/_analysis/c5c9_order_tally.py c5c9_a05_read.txt c5c9_a05_codes.json L T
    python3 out/_analysis/c5c9_order_tally.py c5c9_a14_read.txt c5c9_a14_codes.json C H
"""
import collections, json, os, re, sys

A = os.path.dirname(os.path.abspath(__file__))
read, codes, yes, no = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
t = open(os.path.join(A, read), encoding="utf-8").read()
hours = {}
for b in re.split(r"^== ", t, flags=re.M)[1:]:
    name = b.splitlines()[0].strip()
    h = re.findall(r"^\s+c\d{4} h([\d.]+) ", b, flags=re.M)
    hours[name] = (float(h[0]), float(h[1])) if len(h) >= 2 else None
c = json.load(open(os.path.join(A, codes), encoding="utf-8"))["codes"]
assert set(c) == set(hours), "coded rooms differ from the read: %s" % sorted(set(c) ^ set(hours))
tab = collections.defaultdict(collections.Counter)
for s, code in c.items():
    f, to = hours[s]
    tab["holds" if f < to else "fails"][code] += 1
for k in ("holds", "fails"):
    n = tab[k]
    base = n[yes] + n[no]
    print("order %s (%d rooms): %s; %s of %s+%s %d of %d (%.2f)" % (k, sum(n.values()), dict(n), yes, yes, no, n[yes],
                                                                     base, n[yes] / base if base else 0))
allc = tab["holds"] + tab["fails"]
print("all (%d rooms): %s; %s of %s+%s %d of %d (%.2f)" % (sum(allc.values()), dict(allc), yes, yes, no, allc[yes],
                                                          allc[yes] + allc[no], allc[yes] / (allc[yes] + allc[no])))
print("rule: at least half where the order holds, the mechanism shows in words; under a third, it is marked theorised")
