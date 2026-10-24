#!/usr/bin/env python3
"""D4a-01, stage D4 section 1: the key frequencies, read before any cut. For each of the sixteen views
_views/rooms-x-adaptations.<level>.<kind>.tsv (level 3, 4, dim, target; kind all, correction, elaboration,
specification): the number of keys and of rooms holding at least one; the keys by how many rooms hold them
(1, 2 to 4, 5 to 19, 20 to 99, 100 or more); the rooms that hold no key of that kind; and the top keys by rooms,
with the element and op. Also, at level 3 by kind: per element, keys held by five rooms or more (the default
minimum group size). Read-only; writes nothing.

    python3 out/_analysis/d4a01_key_freq.py [--top 12]
"""
import argparse, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = os.path.join(ROOT, "out", "_views")
ap = argparse.ArgumentParser()
ap.add_argument("--top", type=int, default=12)
a = ap.parse_args()


def load(level, kind):
    p = os.path.join(V, "rooms-x-adaptations.%s.%s.tsv" % (level, kind))
    with open(p, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")[1:]
        rows = {}
        for line in f:
            parts = line.rstrip("\n").split("\t")
            rows[parts[0]] = [k for k, v in zip(head, parts[1:]) if v not in ("", "0")]
    return head, rows


def band(n):
    return "1" if n == 1 else "2-4" if n < 5 else "5-19" if n < 20 else "20-99" if n < 100 else "100+"


per_el = {}
for level in ("3", "4", "dim", "target"):
    for kind in ("all", "correction", "elaboration", "specification"):
        head, rows = load(level, kind)
        cnt = collections.Counter(k for ks in rows.values() for k in ks)
        empty = sorted(s for s, ks in rows.items() if not ks)
        bands = collections.Counter(band(n) for n in cnt.values())
        print("== level %s, kind %s: %d keys (columns %d), %d rooms in the view, %d hold a key, %d hold none" % (
            level, kind, len(cnt), len(head), len(rows), len(rows) - len(empty), len(empty)))
        print("   keys by rooms holding them: %s" % ", ".join("%s: %d" % (b, bands[b]) for b in
                                                           ("1", "2-4", "5-19", "20-99", "100+")))
        if kind in ("correction",) or (kind == "elaboration" and level == "3"):
            print("   rooms with none: %d%s" % (len(empty), "" if len(empty) > 40 else " (" + ", ".join(empty) + ")"))
        print("   top: %s" % "; ".join("%s %d" % kv for kv in cnt.most_common(a.top)))
        if level == "3" and kind != "all":
            pe = collections.Counter()
            for k, n in cnt.items():
                if n >= 5:
                    pe[k.split(":")[1]] += 1
            per_el[kind] = pe
for kind, pe in per_el.items():
    print("== level 3, %s: keys held by 5 rooms or more, by element: %s" % (
        kind, ", ".join("%s %d" % kv for kv in sorted(pe.items(), key=lambda x: (-x[1], x[0])))))
