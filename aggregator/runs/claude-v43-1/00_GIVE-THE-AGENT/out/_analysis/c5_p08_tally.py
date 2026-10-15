#!/usr/bin/env python3
"""C5a-02: tally the P08 test's codes (c5_p08_codes.json) against its sample (c5_p08_sample.json), check every drawn
room has one code, apply the rule written first (T at least half of T plus D), and give the result with every doubtful
code turned to D, as a bound on the reading. Writes nothing.

    python3 out/_analysis/c5_p08_tally.py
"""
import collections, json, os

A = os.path.dirname(os.path.abspath(__file__))
s = json.load(open(os.path.join(A, "c5_p08_sample.json"), encoding="utf-8"))
c = json.load(open(os.path.join(A, "c5_p08_codes.json"), encoding="utf-8"))
drawn, codes, doubt = sorted(s["drawn"]), c["codes"], c["doubtful"]
print("drawn %d, coded %d; missing %s; extra %s" % (len(drawn), len(codes), sorted(set(drawn) - set(codes)),
                                                     sorted(set(codes) - set(drawn))))
n = collections.Counter(codes[k] for k in drawn)
print("T %d, D %d, O %d; T %d of %d (T plus D), %.2f; rule met (T at least half): %s" % (
    n["T"], n["D"], n["O"], n["T"], n["T"] + n["D"], n["T"] / (n["T"] + n["D"]), n["T"] >= (n["T"] + n["D"]) / 2))
m = collections.Counter(("D" if (k in doubt and codes[k] == "T") else codes[k]) for k in drawn)
print("every doubtful T turned to D: T %d, D %d (%.2f)" % (m["T"], m["D"], m["T"] / (m["T"] + m["D"])))
