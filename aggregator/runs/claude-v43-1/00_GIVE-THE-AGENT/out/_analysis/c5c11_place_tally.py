#!/usr/bin/env python3
"""C5c-11, problem 2, part B: tally c5c11_place_codes.json against its sample (c5c11_place_sample.json): every drawn
room coded once; pairs set aside; stance counts; reasons by stance; one-sided Fisher's exact test (refusals give a reason
more often than acceptances), computed from the hypergeometric distribution. Writes nothing.

    python3 out/_analysis/c5c11_place_tally.py
"""
import collections, json, os
from math import comb

A = os.path.dirname(os.path.abspath(__file__))
s = json.load(open(os.path.join(A, "c5c11_place_sample.json"), encoding="utf-8"))["drawn"]
c = json.load(open(os.path.join(A, "c5c11_place_codes.json"), encoding="utf-8"))["codes"]
assert set(s) == set(c), "coded rooms differ from the drawn rooms: %s" % sorted(set(s) ^ set(c))
kept = {k: v for k, v in c.items() if not v.get("set_aside")}
st = collections.Counter(v["stance"] for v in kept.values())
acc = collections.Counter(v["stance"] for v in kept.values() if v["account"])
print("drawn %d; set aside %d; kept %d: %s" % (len(c), len(c) - len(kept), len(kept), dict(st)))
for k in ("accept", "refuse", "mixed", "other"):
    print("  %s: %d of %d give a reason" % (k, acc[k], st[k]))
a, b = acc["refuse"], st["refuse"] - acc["refuse"]
cc, d = acc["accept"], st["accept"] - acc["accept"]
N, K, n = a + b + cc + d, a + cc, a + b
p = sum(comb(K, x) * comb(N - K, n - x) for x in range(a, min(K, n) + 1)) / comb(N, n)
print("Fisher one-sided (refusals with a reason more often than acceptances): refuse %d of %d, accept %d of %d, p %.4f"
      % (a, a + b, cc, cc + d, p))
lengths = [len(s[k]["reply_text"].split()) for k, v in kept.items() if v["stance"] == "accept" and not v["account"]]
print("bare acceptances: %d; median words %s" % (len(lengths), sorted(lengths)[len(lengths) // 2] if lengths else None))
