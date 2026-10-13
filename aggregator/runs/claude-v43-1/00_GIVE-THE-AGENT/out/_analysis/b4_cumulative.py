#!/usr/bin/env python3
"""B4a: the adjudication's figures summed over the ruled packets, for adjudication_report.md (section 9).

    python3 out/_analysis/b4_cumulative.py --packets 1,2

Reads out/disagreements.jsonl and prints, over the packets named: items by class; the taxonomy split by class;
unresolved, named_neither, author-error, author-disagrees; fields by ambiguity; the twelve themes with most
scheme-ambiguous rulings, with their fields; agreement before and after (as b4_packet_summary.py computes it);
and the packet each figure comes from beside the total.
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
TAX = ("genuine-joint", "scheme-ambiguous", "author-error", "author-disagrees", "item-is-a-bag", "reader-error")
FIELDS = ("must_show", "must_not_show", "decide_when_both", "discriminators")


def jac(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def agreement(rows):
    bj, bp, aj, ap = [], [], [], []
    for d in rows:
        r1, r2 = d["readers"]
        bj.append(jac(r1, r2))
        bp.append(1.0 if (r1[:1] == r2[:1] and r1) else 0.0)
        if d["unresolved"]:
            continue
        for r in (r1, r2):
            aj.append(jac(r, d["ruling"]))
            ap.append(1.0 if r[:1] == d["ruling"][:1] else 0.0)
    m = lambda xs: sum(xs) / len(xs) if xs else float("nan")
    return m(bj), m(bp), m(aj), m(ap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packets", required=True)
    a = ap.parse_args()
    want = [int(x) for x in a.packets.split(",")]
    rows = [json.loads(x) for x in open(os.path.join(OUT, "disagreements.jsonl"), encoding="utf-8") if x.strip()]
    rows = [d for d in rows if d.get("packet") in want]
    by_p = collections.defaultdict(list)
    for d in rows:
        by_p[d["packet"]].append(d)
    n = len(rows)
    print("items: %d (%s)" % (n, ", ".join("packet %d %d" % (p, len(by_p[p])) for p in want)))
    cls = collections.Counter(d["class"] for d in rows)
    print("by class: " + ", ".join("class %s %d" % (c, cls[c]) for c in sorted(cls)))
    print("")
    print("| taxonomy | all | " + " | ".join("packet %d" % p for p in want) + " | " +
          " | ".join("class %s" % c for c in sorted(cls)) + " |")
    print("|---|---|" + "---|" * (len(want) + len(cls)))
    for t in TAX:
        allc = sum(1 for d in rows if d["taxonomy"] == t)
        pc = [sum(1 for d in by_p[p] if d["taxonomy"] == t) for p in want]
        cc = [sum(1 for d in rows if d["taxonomy"] == t and d["class"] == c) for c in sorted(cls)]
        print("| %s | %d | " % (t, allc) + " | ".join(map(str, pc)) + " | " + " | ".join(map(str, cc)) + " |")
    print("| total | %d | " % n + " | ".join(str(len(by_p[p])) for p in want) + " | " +
          " | ".join(str(cls[c]) for c in sorted(cls)) + " |")
    print("")
    un = [d for d in rows if d["unresolved"]]
    nn = [d for d in rows if d["named_neither"]]
    print("unresolved: %d (%.1f%%); %s" % (len(un), 100.0 * len(un) / n,
                                          ", ".join("packet %d %d" % (p, sum(1 for d in by_p[p] if d["unresolved"])) for p in want)))
    print("named_neither: %d (%.1f%%); %s" % (len(nn), 100.0 * len(nn) / n,
                                             ", ".join("packet %d %d" % (p, sum(1 for d in by_p[p] if d["named_neither"])) for p in want)))
    nn_ad = sum(1 for d in nn if d["taxonomy"] == "author-disagrees")
    print("named_neither that are author-disagrees: %d" % nn_ad)
    revised = [d for d in rows if d.get("revised")]
    print("corrected in place: %d (%s)" % (len(revised), ", ".join("%s %s" % (d["sub"], d["theme_id"]) for d in revised)))
    print("")
    amb = [d for d in rows if d["taxonomy"] == "scheme-ambiguous"]
    fc = collections.Counter(d["field"] for d in amb)
    print("fields: " + ", ".join("%s %d" % (f, fc.get(f, 0)) for f in FIELDS))
    print("")
    th = collections.Counter(d["theme"] for d in amb)
    thf = collections.defaultdict(collections.Counter)
    for d in amb:
        thf[d["theme"]][d["field"]] += 1
    print("| theme | rulings | " + " | ".join(FIELDS) + " |")
    print("|---|---|" + "---|" * len(FIELDS))
    for t, c in th.most_common(12):
        print("| %s | %d | " % (t, c) + " | ".join(str(thf[t].get(f, 0)) for f in FIELDS) + " |")
    rest = th.most_common()[12:]
    print("themes beyond the twelve: %d, with %d rulings" % (len(rest), sum(c for _, c in rest)))
    print("")
    print("| | mean Jaccard before | primary before | mean Jaccard after | primary after |")
    print("|---|---|---|---|---|")
    for p in want:
        print("| packet %d | %.3f | %.3f | %.3f | %.3f |" % ((p,) + agreement(by_p[p])))
    print("| all | %.3f | %.3f | %.3f | %.3f |" % agreement(rows))


if __name__ == "__main__":
    main()
