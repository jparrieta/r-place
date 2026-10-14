#!/usr/bin/env python3
"""C3b: tally the conversation-analysis read. Joins c3b_ca_sample.json (the seeded pairs) with c3b_ca_codes.json (the
analyst's codes under rules written before reading) and prints, by read stance and by the theme the reply sat under:
pairs counted, the share of replies with an account, the median reply length in words and the median interval in
minutes; and a one-sided Fisher exact test on accounts, refusals against acceptances. Writes nothing.

    python3 out/_analysis/c3b_ca_tally.py
"""
import json, math, os, statistics, sys

A = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sample = json.load(open(os.path.join(A, "c3b_ca_sample.json"), encoding="utf-8"))
codes = json.load(open(os.path.join(A, "c3b_ca_codes.json"), encoding="utf-8"))["codes"]
rows = dict(((k, r["sub"], r["reply"]), r) for k in sample for r in sample[k])
if len(codes) != len(rows) or any((c["kind"], c["sub"], c["reply"]) not in rows for c in codes):
    sys.exit("codes and sample do not match one to one")
joined = [dict(rows[(c["kind"], c["sub"], c["reply"])], **c) for c in codes]
counted = [j for j in joined if j["counted"]]
print("pairs sampled %d; counted (first part calls for or proposes an attack) %d; set aside %d" % (
    len(joined), len(counted), len(joined) - len(counted)))


def line(name, g):
    if not g:
        print("  %-28s none" % name)
        return
    acc = sum(1 for j in g if j["account"])
    print("  %-28s %2d pairs, account %2d (%.2f), median words %.1f, median interval %.0f min" % (
        name, len(g), acc, acc / len(g), statistics.median(j["reply_words"] for j in g),
        statistics.median(j["interval_min"] for j in g)))


print("by read stance:")
for st in ("accept", "refuse", "mixed", "other"):
    line(st, [j for j in counted if j.get("stance") == st])
print("by the theme the reply sat under:")
for k in ("acceptance", "refusal"):
    line("%s (theme)" % k, [j for j in counted if j["kind"] == k])


def fisher_greater(a, b, c, d):
    """P(X >= a) for the top-left cell of [[a, b], [c, d]] with margins fixed (hypergeometric)."""
    n1, n2, k = a + b, c + d, a + c
    def p(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n1 + n2, k)
    return sum(p(x) for x in range(a, min(n1, k) + 1))


ref = [j for j in counted if j.get("stance") == "refuse"]
acc = [j for j in counted if j.get("stance") == "accept"]
a, b = sum(1 for j in ref if j["account"]), sum(1 for j in ref if not j["account"])
c, d = sum(1 for j in acc if j["account"]), sum(1 for j in acc if not j["account"])
print("accounts, refusals %d of %d against acceptances %d of %d; one-sided Fisher p %.4f" % (a, a + b, c, c + d,
                                                                                         fisher_greater(a, b, c, d)))
