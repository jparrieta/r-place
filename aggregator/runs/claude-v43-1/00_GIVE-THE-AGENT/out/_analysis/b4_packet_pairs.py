#!/usr/bin/env python3
"""B4a: before a packet's first ruling, count the pairs of primaries on which its items' two readings split, so
that every pair split by five or more items is ruled once (stage B4 section 5). Also counts the items' classes and
the pairs carried by readers' added themes. Reads the packet's index.tsv and b3_classes.jsonl; prints only.

    python3 out/_analysis/b4_packet_pairs.py --packet 2
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    a = ap.parse_args()
    keys = []
    for ln in open(os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet, "index.tsv"), encoding="utf-8").read().splitlines()[1:]:
        n, key, cl, ch, arep = ln.split("\t")
        keys.append(key)
    cls = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in (json.loads(x) for x in open(os.path.join(OUT, "b3_classes.jsonl"), encoding="utf-8") if x.strip())}
    prim = collections.Counter()
    anyp = collections.Counter()
    klass = collections.Counter()
    for k in keys:
        c = cls[k]
        klass[c["class"]] += 1
        r1, r2 = c["r1"] or [], c["r2"] or []
        if r1 and r2 and r1[0] != r2[0]:
            prim[tuple(sorted((r1[0], r2[0])))] += 1
        sym = set(r1) ^ set(r2)
        for x in sorted(sym):
            for y in sorted(set(r1) | set(r2)):
                if x != y:
                    anyp[tuple(sorted((x, y)))] += 1
    print("items %d; classes %s" % (len(keys), dict(sorted(klass.items()))))
    print("primary splits by pair (five or more are ruled once):")
    for p, c in prim.most_common():
        if c >= 3:
            print("  %s|%s %d%s" % (p[0], p[1], c, "  <- rule once" if c >= 5 else ""))


if __name__ == "__main__":
    main()
