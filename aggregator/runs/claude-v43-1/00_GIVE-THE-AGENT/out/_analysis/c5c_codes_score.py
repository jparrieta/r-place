#!/usr/bin/env python3
"""C5c-01: the readers' Stigmergy codes against mine (c5_stigmergy_codes.json, coded at C5a-01, before the readers).
Each reader coded the 24 records of one member theme, blind. For each: exact agreement, Cohen's kappa on the four
codes, agreement with MP counted as M (as the decision rule counts it), the cross-table, and the decision rule run on
the reader's codes (a member joins what the sources keep apart if P is at least half of its records that are not O).
Writes out/_analysis/c5c_codes_score.json.

    python3 out/_analysis/c5c_codes_score.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
mine = json.load(open(os.path.join(OUT, "_analysis", "c5_stigmergy_codes.json"), encoding="utf-8"))
THEMES = {1: "T3-038", 2: "T3-041", 3: "T3-060"}
CODES = ["M", "MP", "P", "O"]


def kappa(pairs, cats):
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in cats) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def rule(codes):
    not_o = [c for c in codes if c != "O"]
    p = sum(1 for c in not_o if c == "P")
    return p, len(not_o), p * 2 >= len(not_o)


res = {}
for k, th in THEMES.items():
    r = json.loads(open(os.path.join(OUT, "readers-C5", "C5-reader-%d.jsonl" % k)).read().strip().splitlines()[0])
    theirs = {c["record"]: c["code"] for c in r["codes"]}
    my = mine["codes"][th]
    recs = [x for x in my if x in theirs]
    pairs = [(my[x], theirs[x]) for x in recs]
    fold = [(a.replace("MP", "M"), b.replace("MP", "M")) for a, b in pairs]
    tab = collections.Counter(pairs)
    pm, nm, jm = rule([a for a, _ in pairs])
    pt, nt, jt = rule([b for _, b in pairs])
    diff = [{"record": x, "mine": my[x], "reader": theirs[x]} for x in recs if my[x] != theirs[x]]
    res[th] = {"reader": "C5-reader-%d" % k, "n": len(pairs), "missing": sorted(set(my) - set(theirs)),
               "exact": sum(1 for a, b in pairs if a == b), "kappa4": round(kappa(pairs, CODES), 3),
               "exact_MP_as_M": sum(1 for a, b in fold if a == b), "kappa3": round(kappa(fold, ["M", "P", "O"]), 3),
               "mine_rule": [pm, nm, jm], "reader_rule": [pt, nt, jt], "differ": diff,
               "table": {"%s>%s" % ab: v for ab, v in sorted(tab.items())}}
    print("%s (%s): n %d; exact %d (kappa %.3f); MP as M %d (kappa %.3f)" % (
        th, res[th]["reader"], len(pairs), res[th]["exact"], res[th]["kappa4"], res[th]["exact_MP_as_M"],
        res[th]["kappa3"]))
    print("   rule, mine: P in %d of %d not O (joins: %s); reader: P in %d of %d (joins: %s)" % (pm, nm, jm, pt, nt, jt))
    print("   differ: " + "; ".join("%s mine %s, reader %s" % (d["record"], d["mine"], d["reader"]) for d in diff))
tot_m = sum(v["mine_rule"][1] for v in res.values())
tot_t = sum(v["reader_rule"][1] for v in res.values())
mt = sum(v["mine_rule"][1] - v["mine_rule"][0] for v in res.values())
rt = sum(v["reader_rule"][1] - v["reader_rule"][0] for v in res.values())
print("across the three: trace or marker (M, MP) in %d of %d not O, mine; %d of %d, the readers'" % (mt, tot_m, rt, tot_t))
res["_across"] = {"mine": [mt, tot_m], "readers": [rt, tot_t],
                  "exact": sum(v["exact"] for k, v in res.items() if k != "_across"),
                  "n": sum(v["n"] for k, v in res.items() if k != "_across")}
json.dump(res, open(os.path.join(OUT, "_analysis", "c5c_codes_score.json"), "w"), indent=1)
