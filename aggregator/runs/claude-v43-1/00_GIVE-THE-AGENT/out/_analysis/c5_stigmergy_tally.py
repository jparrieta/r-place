#!/usr/bin/env python3
"""C5a-01: tally the codes of the abductive read of Stigmergy (c5_stigmergy_codes.json) against the sample
(c5_stigmergy_sample.json), check that every drawn record has one code, and apply the decision rule written first:
a member joins what the sources keep apart if P is at least half of its records that are not O. Writes nothing.

    python3 out/_analysis/c5_stigmergy_tally.py
"""
import collections, json, os

A = os.path.dirname(os.path.abspath(__file__))
sample = json.load(open(os.path.join(A, "c5_stigmergy_sample.json"), encoding="utf-8"))
codes = json.load(open(os.path.join(A, "c5_stigmergy_codes.json"), encoding="utf-8"))["codes"]
tot = collections.Counter()
for t, s in sample.items():
    drawn = ["%s/%s" % (r["sub"], r["code_id"]) for r in s["drawn"]]
    c = codes[t]
    missing, extra = sorted(set(drawn) - set(c)), sorted(set(c) - set(drawn))
    n = collections.Counter(c[k] for k in drawn if k in c)
    tot.update(n)
    not_o = n["M"] + n["MP"] + n["P"]
    share = n["P"] / not_o if not_o else 0
    print("%s: drawn %d, coded %d (missing %s, extra %s); M %d, MP %d, P %d, O %d; P %d of %d not O (%.2f); "
          "joins what the sources keep apart: %s" % (t, len(drawn), sum(n.values()), missing, extra, n["M"], n["MP"],
                                                     n["P"], n["O"], n["P"], not_o, share, share >= 0.5))
not_o = tot["M"] + tot["MP"] + tot["P"]
print("all three: M %d, MP %d, P %d, O %d; trace or marker %d of %d not O, P %d of %d" % (
    tot["M"], tot["MP"], tot["P"], tot["O"], tot["M"] + tot["MP"], not_o, tot["P"], not_o))
