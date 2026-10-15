#!/usr/bin/env python3
"""C5c-09: score the field analyst's blind second coding of the 40 border records (sources-from-J/RETURN-border-C5b.jsonl)
against my C5a-02 codes (c5_p08_codes.json), under the rule logged at C5c-07 before the return came back: a record both
coders code alike takes that code; a split record is counted both ways, so T of T plus D is a range; Cohen's kappa is
reported. Low end: T/D -> D, T/O -> O, D/O -> D. High end: T/D -> T, T/O -> T, D/O -> O. Also the result with the
field analyst's codes alone. Writes c5c9_border_score.json; prints the result.

    python3 out/_analysis/c5c9_border_score.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "out", "_analysis")
lines = open(os.path.join(ROOT, "out", "sources-from-J", "RETURN-border-C5b.jsonl"), encoding="utf-8").read().splitlines()
assert lines[-1].strip() == "END-OF-BORDER-RETURN", "no end marker"
field = {}
for l in lines[:-1]:
    r = json.loads(l)
    field[r["record"].split("/")[0]] = r
sample = json.load(open(os.path.join(A, "c5_p08_sample.json"), encoding="utf-8"))
recid = {sub: v["P08"].split()[0] for sub, v in sample["drawn"].items()}
mine = json.load(open(os.path.join(A, "c5_p08_codes.json"), encoding="utf-8"))["codes"]
assert set(field) == set(mine) == set(recid), "record sets differ"
bad = [s for s in field if field[s]["record"] != "%s/%s" % (s, recid[s])]
assert not bad, "citations differ: %s" % bad

rooms = sorted(mine)
agree = [s for s in rooms if mine[s] == field[s]["code"]]
split = [s for s in rooms if mine[s] != field[s]["code"]]
cats = "TDO"
n = len(rooms)
po = len(agree) / n
pm, pf = collections.Counter(mine[s] for s in rooms), collections.Counter(field[s]["code"] for s in rooms)
pe = sum(pm[c] * pf[c] for c in cats) / n ** 2
kappa = (po - pe) / (1 - pe)
LOW = {frozenset("TD"): "D", frozenset("TO"): "O", frozenset("DO"): "D"}
HIGH = {frozenset("TD"): "T", frozenset("TO"): "T", frozenset("DO"): "O"}


def tally(rule):
    c = collections.Counter(mine[s] if mine[s] == field[s]["code"] else rule[frozenset(mine[s] + field[s]["code"])]
                            for s in rooms)
    return c["T"], c["D"], c["O"]


lo, hi = tally(LOW), tally(HIGH)
fc = (pf["T"], pf["D"], pf["O"])
kinds = collections.Counter("%s/%s" % (mine[s], field[s]["code"]) for s in split)
res = {"n": n, "agree": len(agree), "kappa": round(kappa, 3), "mine": dict(pm), "field": dict(pf),
       "splits": dict(kinds), "low": lo, "high": hi, "field_alone": fc,
       "split_rooms": {s: [mine[s], field[s]["code"], field[s]["why"]] for s in split}}
json.dump(res, open(os.path.join(A, "c5c9_border_score.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("records %d; agree %d (%.2f); Cohen's kappa %.3f" % (n, len(agree), po, kappa))
print("mine  T %(T)d D %(D)d O %(O)d" % collections.defaultdict(int, pm))
print("field T %(T)d D %(D)d O %(O)d" % collections.defaultdict(int, pf))
print("splits (mine/field): %s" % dict(kinds))
for name, (t, d, o) in (("low", lo), ("high", hi), ("field alone", fc)):
    print("%-11s T %d, D %d, O %d; T of T+D %d of %d (%.2f)" % (name, t, d, o, t, t + d, t / (t + d)))
for s in split:
    print("  %-22s mine %s, field %s%s: %s" % (s, mine[s], field[s]["code"], " (doubtful)" if field[s]["doubtful"] else "",
                                             field[s]["why"]))
