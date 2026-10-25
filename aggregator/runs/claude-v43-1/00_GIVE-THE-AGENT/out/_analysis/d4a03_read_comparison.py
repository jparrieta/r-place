#!/usr/bin/env python3
"""D4a-03: read chunk-share-D4.result.json (the comparison, chunk-comparison-v1.1) and print the figures stage D4's
final message asks for, with and without the low-information rows: status and the k carried; per k and seed the
silhouette, the real and null stability means and medians, both margins and the null 95th percentile, and whether
k clears (both margins positive under both seeds); the sensitivities (Jaccard and Hellinger ARI against the Ward/CLR
labels, a/10 and 10a); the median own-data weight; the dimension and third-tier ARI at every k, the third tier's
columns and mean nonzero count; the accounting (empties, low-information rooms, unplaced and residue concepts); each
cluster's code, size, low-information count, over- and under-represented themes and volume fields; and the residue
share per room (residue concepts over placed plus residue concepts), summarized, with the rooms of 30 per cent or
more. After it, best-match Jaccard between each cluster and the branches (descriptive; ARI is undefined, since the
branches overlap). Read-only; prints only.

    python3 out/_analysis/d4a03_read_comparison.py
"""
import collections, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
r = json.load(open(os.path.join(OUT, "chunk-share-D4.result.json"), encoding="utf-8"))
print("format", r["format"], "engine", r["engine_sha256"][:12], "parameters", r["parameters"])
for part in ("all_cases", "without_low_information"):
    p = r[part]
    print("\n== %s: status %s; carried k %s; eligible rooms %d; median own-data weight %.4f" % (
        part, p["status"], p["carried_k"], len(p["eligible_indices"]), p["own_weight_median"]))
    by = collections.defaultdict(dict)
    for t in p["tables"]:
        by[t["k"]][t["seed"]] = t
    for k in sorted(by):
        cells = []
        clears = True
        for s in sorted(by[k]):
            t = by[k][s]
            cells.append("seed %d: sil %.3f real %.3f/%.3f null %.3f/%.3f margins %+.3f/%+.3f null95 %.3f" % (
                s, t["silhouette"], t["real"]["mean"], t["real"]["median"], t["null"]["mean"], t["null"]["median"],
                t["mean_margin"], t["median_margin"], t["null_95"]))
            clears = clears and t["mean_margin"] > 0 and t["median_margin"] > 0
        worst = min(min(by[k][s]["mean_margin"], by[k][s]["median_margin"]) for s in by[k])
        print("k %2d %s | worst margin %+.3f | %s" % (k, "CLEARS" if clears else "      ", worst, " | ".join(cells)))
    print("sensitivities (ARI against the carried Ward/CLR labels at each k):")
    for k, v in sorted(p["sensitivities"].items(), key=lambda x: int(x[0])):
        print("  k %s: %s" % (k, ", ".join("%s %.3f" % (kk, vv) for kk, vv in v.items())))
print("\n== tiers: dimension ARI %s" % ", ".join("k%s %.3f" % kv for kv in sorted(r["dimension_ari"].items(), key=lambda x: int(x[0]))))
tt = r["third_tier"]
print("third tier: %d columns, mean nonzero per case %.2f; ARI %s" % (tt["columns"], tt["mean_nonzero_per_case"], ", ".join(
    "k%s %.3f" % kv for kv in sorted(tt["ari"].items(), key=lambda x: int(x[0])))))
ci = r["case_information"]
keys = sorted({k for c in ci for k in c})
print("case_information keys:", keys)
low = [c["sub"] for c in ci if c.get("low_information")]
empty = [c["sub"] for c in ci if not c.get("placed_concepts")]
print("empty compositions: %d %s; low-information rooms: %d" % (len(empty), empty, len(low)))
share = {}
for c in ci:
    rc = c.get("residue_concepts", 0) or 0
    pc = c.get("placed_concepts", 0) or 0
    share[c["sub"]] = rc / (pc + rc) if (pc + rc) else 0.0
withres = [s for s, v in share.items() if v > 0]
vals = sorted(share.values())
print("residue: %d rooms with residue concepts (%d themes, %d concepts in all); share per room: median %.4f, "
      "mean %.4f, max %.4f; rooms at 0.05 or more %d, 0.10 or more %d, 0.30 or more %d" % (
          len(withres), sum(c.get("residue_themes", 0) or 0 for c in ci), sum(c.get("residue_concepts", 0) or 0 for c in ci),
          statistics.median(vals), statistics.mean(vals), vals[-1], sum(1 for v in vals if v >= .05),
          sum(1 for v in vals if v >= .10), sum(1 for v in vals if v >= .30)))
print("rooms at 0.20 or more: %s" % ", ".join("%s %.2f" % (s, v) for s, v in sorted(share.items(), key=lambda x: -x[1]) if v >= .2))
print("\n== clusters")
B = [json.loads(l) for l in open(os.path.join(OUT, "branches.jsonl"), encoding="utf-8") if l.strip()]
for c in r["clusters"]:
    m = set(c["members"])
    best = max(B, key=lambda b: len(m & set(b["members"])) / len(m | set(b["members"])))
    jac = len(m & set(best["members"])) / len(m | set(best["members"]))
    extra = {k: v for k, v in c.items() if k not in ("members", "profile")}
    print("%s: n %d, low-information %s; over %s; under %s; nearest %s; volume %s; best branch %s (Jaccard %.3f); "
          "mean residue share %.4f; keys %s" % (c["code"], len(c["members"]), c.get("n_low_information"),
                                                c.get("over"), c.get("under"), c.get("nearest"), c.get("volume"),
                                                best["id"], jac, statistics.mean(share[s] for s in c["members"]),
                                                sorted(extra)))
