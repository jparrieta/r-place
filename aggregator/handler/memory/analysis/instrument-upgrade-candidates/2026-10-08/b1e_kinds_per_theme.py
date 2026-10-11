#!/usr/bin/env python3
"""B1e: kinds per placed second-order theme, overall and by whether a theme touches the deal families.

Usage: python3 out/_analysis/b1e_kinds_per_theme.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEAL = {"G13", "G14", "G15"}


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
kinds = collections.defaultdict(set)
for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
    for m in r["members"]:
        kinds[(m["sub"], m["second_order"])].add(r["theme"])
dist = collections.Counter(len(v) for v in kinds.values())
n = len(kinds)
print("placed second-order themes %d, placements %d" % (n, sum(len(v) for v in kinds.values())))
print("kinds per theme: " + ", ".join("%d: %d (%.1f%%)" % (k, dist[k], 100.0 * dist[k] / n) for k in sorted(dist)))
deal = [v for v in kinds.values() if {fam[x] for x in v} & DEAL]
other = [v for v in kinds.values() if not ({fam[x] for x in v} & DEAL)]
for name, vs in (("touching G13, G14 or G15", deal), ("touching none of them", other)):
    single = sum(1 for v in vs if len(v) == 1)
    print("%s: %d themes, single %d (%.1f%%), mean kinds %.2f" % (name, len(vs), single, 100.0 * single / len(vs),
                                                               sum(len(v) for v in vs) / len(vs)))
# the grain of the second-order theme: concepts under it against kinds placed on it
lab2id = {(r["sub"], r["second_order"]): r["theme_id"] for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
nc = collections.Counter()
for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl")):
    if c.get("theme_id"):
        nc[(c["sub"], c["theme_id"])] += 1
bands = collections.defaultdict(list)
for (sub, so), v in kinds.items():
    k = nc.get((sub, lab2id.get((sub, so), so)), 0)
    b = "1-5" if k <= 5 else "6-10" if k <= 10 else "11-20" if k <= 20 else "21-40" if k <= 40 else "41+"
    bands[b].append(len(v))
print("concepts under the second-order theme -> themes, share single, mean kinds")
for b in ("1-5", "6-10", "11-20", "21-40", "41+"):
    vs = bands[b]
    if vs:
        print("  %s: %d, %.1f%%, %.2f" % (b, len(vs), 100.0 * sum(1 for x in vs if x == 1) / len(vs), sum(vs) / len(vs)))
