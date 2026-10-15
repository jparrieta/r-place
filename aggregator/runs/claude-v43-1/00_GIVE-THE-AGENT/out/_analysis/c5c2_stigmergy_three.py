#!/usr/bin/env python3
"""C5c-02: Stigmergy's cut with three codings, by the rule logged before this tally (diary, C5c-02, kind abductive).
Coders: mine (c5_stigmergy_codes.json, C5a-01), the fleet reader of each member theme (readers-C5/C5-reader-k.jsonl,
C5c-01), and the field analyst (sources-from-J/RETURN-field-C5.jsonl). MP counts as M. Each record takes the code at
least two coders gave; a three-way split is doubtful and the verdict is computed with it as M, P and O. A member joins
what the sources keep apart if P is at least half of its records that are not O. Also pairwise agreement and kappa.
Writes out/_analysis/c5c2_stigmergy_three.json.

    python3 out/_analysis/c5c2_stigmergy_three.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
THEMES = {"T3-038": 1, "T3-041": 2, "T3-060": 3}
mine = json.load(open(os.path.join(OUT, "_analysis", "c5_stigmergy_codes.json"), encoding="utf-8"))["codes"]
fleet = {}
for th, k in THEMES.items():
    r = json.loads(open(os.path.join(OUT, "readers-C5", "C5-reader-%d.jsonl" % k)).read().strip().splitlines()[0])
    fleet[th] = {c["record"]: c["code"] for c in r["codes"]}
field = {}
for l in open(os.path.join(OUT, "sources-from-J", "RETURN-field-C5.jsonl"), encoding="utf-8"):
    l = l.strip()
    if l.startswith("{"):
        o = json.loads(l)
        if "record" in o:
            field[o["record"]] = o["code"]


def m(c):
    return "M" if c == "MP" else c


def kappa(pairs):
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe)


def verdict(codes):
    not_o = [c for c in codes if c != "O"]
    p = sum(1 for c in not_o if c == "P")
    return p, len(not_o), p * 2 >= len(not_o)


res, allpairs = {}, collections.defaultdict(list)
for th in THEMES:
    rows, doubtful = [], []
    for rec in mine[th]:
        a, b, c = m(mine[th][rec]), m(fleet[th].get(rec, "?")), m(field.get(rec, "?"))
        allpairs["mine-fleet"].append((a, b))
        allpairs["mine-field"].append((a, c))
        allpairs["fleet-field"].append((b, c))
        cnt = collections.Counter([a, b, c])
        top, n = cnt.most_common(1)[0]
        maj = top if n >= 2 else None
        if maj is None:
            doubtful.append(rec)
        rows.append({"record": rec, "mine": a, "fleet": b, "field": c, "majority": maj})
    ways = {}
    for as_ in ("M", "P", "O"):
        codes = [r["majority"] or as_ for r in rows]
        ways[as_] = verdict(codes)
    vs = {w[2] for w in ways.values()}
    res[th] = {"rows": rows, "doubtful": doubtful, "verdicts": ways,
               "meets": (list(vs)[0] if len(vs) == 1 else "depends on the doubtful records"),
               "field_alone": verdict([r["field"] for r in rows])}
    print("%s: %d records, %d doubtful %s" % (th, len(rows), len(doubtful), doubtful))
    for w, (p, n, j) in ways.items():
        print("   doubtful as %s: P in %d of %d not O -> meets the rule: %s" % (w, p, n, j))
    p, n, j = res[th]["field_alone"]
    print("   field analyst alone: P in %d of %d not O -> %s" % (p, n, j))
    print("   verdict: %s" % res[th]["meets"])
print("missing field codes:", sorted(r for th in mine for r in mine[th] if r not in field))
for k, pairs in allpairs.items():
    print("%s: agree %d of %d, kappa %.3f" % (k, sum(1 for a, b in pairs if a == b), len(pairs), kappa(pairs)))
res["_pairs"] = {k: {"agree": sum(1 for a, b in v if a == b), "n": len(v), "kappa": round(kappa(v), 3)}
                 for k, v in allpairs.items()}
json.dump(res, open(os.path.join(OUT, "_analysis", "c5c2_stigmergy_three.json"), "w"), indent=1)
