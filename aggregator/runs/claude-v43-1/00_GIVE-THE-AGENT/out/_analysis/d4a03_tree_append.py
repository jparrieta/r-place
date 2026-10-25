#!/usr/bin/env python3
"""D4a-03: append to out/tree-D4.md the sections built from the comparison and the projections, so that no figure
is typed: the comparison (chunk-share-D4.result.json: status, the k carried with and without the low-information
rows, their stability tables, the sensitivities, the own-data weight, the tier checks, the clusters with their
profiles and best-match branches), the residue shares (QD4-002), the volume check (recomputed here exactly as
d4a03_volume.py does it, same seed), the projections per branch and per cluster (projections-D4.jsonl), what was
drawn and what was not, and the accounting. Refuses if the sections are there. Without --write it prints a summary.

    python3 out/_analysis/d4a03_tree_append.py [--write]
"""
import argparse, collections, json, math, os, random, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
TREE = os.path.join(OUT, "tree-D4.md")
MARK = "## The comparison (section 5), read at D4a-03"
if MARK in open(TREE, encoding="utf-8").read():
    raise SystemExit("the sections are in tree-D4.md already")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


r = json.load(open(os.path.join(OUT, "chunk-share-D4.result.json"), encoding="utf-8"))
B = jl(os.path.join(OUT, "branches.jsonl"))
C = jl(os.path.join(OUT, "chunk-share-D4.jsonl"))
P = jl(os.path.join(OUT, "projections-D4.jsonl"))


def table(part):
    p = r[part]
    by = collections.defaultdict(dict)
    for t in p["tables"]:
        by[t["k"]][t["seed"]] = t
    k = p["carried_k"]
    cells = ["seed %d: silhouette %.3f, real stability mean %.3f and median %.3f, null %.3f and %.3f, margins %+.3f "
             "and %+.3f, null 95th percentile %.3f" % (s, t["silhouette"], t["real"]["mean"], t["real"]["median"],
                                                      t["null"]["mean"], t["null"]["median"], t["mean_margin"],
                                                      t["median_margin"], t["null_95"]) for s, t in sorted(by[k].items())]
    clear = [kk for kk in sorted(by) if all(by[kk][s]["mean_margin"] > 0 and by[kk][s]["median_margin"] > 0 for s in by[kk])]
    sil = max(by[kk][0]["silhouette"] for kk in by)
    sens = p["sensitivities"][str(k)]
    return k, len(p["eligible_indices"]), p["status"], cells, clear, sil, sens, p["own_weight_median"]


w = ["", MARK, "",
     "Run at D4a-03 on `chunk-comparison-v1.1` (engine sha256 %s...), a departure declared before the run "
     "(`departures.jsonl` line 10; QD4-002), with the stage file's command and defaults: a = %s, seeds %s, %d "
     "bootstrap draws and %d permuted copies per seed. It reads the concept store, the placements, the tiers, the "
     "dropped cases and the prior. **No verdict, canvas field or branch entered its feature space.** Its features are "
     "%d fourth-order themes over %d rooms; empty compositions: %d. It is a non-adaptation baseline that shares the "
     "inductive coding structure, not theory-free evidence." % (
         r["engine_sha256"][:12], r["parameters"]["concentration"], r["parameters"]["seeds"],
         r["parameters"]["resamples"], r["parameters"]["permutations"], len(r["columns"]), len(r["rooms"]),
         sum(1 for c in r["case_information"] if not c["placed_concepts"])), ""]
for part, label in (("all_cases", "All rooms"), ("without_low_information", "Without the low-information rows")):
    k, n, st, cells, clear, sil, sens, own = table(part)
    w.append("- **%s** (%d rooms): status `%s`; **k carried %d**. At k %d: %s. The k that clear under both seeds: %s. "
             "The largest silhouette at any k under seed 0 is %.3f. The median own-data weight is %.3f. Against the "
             "carried Ward/CLR labels at k %d, the Jaccard presence and Hellinger share partitions give ARI %.3f and "
             "%.3f, and a/10 and 10a give %.3f and %.3f." % (
                 label, n, st, k, k, "; ".join(cells), ", ".join(map(str, clear)), sil, own, k, sens["jaccard_ari"],
                 sens["hellinger_ari"], sens["concentration_0.1x_ari"], sens["concentration_10x_ari"]))
k4 = str(r["all_cases"]["carried_k"])
low = sum(1 for c in r["case_information"] if c.get("low_information"))
w += ["- **The tier check** (descriptive, not proof of form): at k %s, dimension ARI %.3f and third-tier ARI %.3f. The "
      "third tier has %d columns and %.2f nonzero per room (%.1f per cent), so its profiles are sparse." % (
          k4, r["dimension_ari"][k4], r["third_tier"]["ari"][k4], r["third_tier"]["columns"],
          r["third_tier"]["mean_nonzero_per_case"],
          100 * r["third_tier"]["mean_nonzero_per_case"] / r["third_tier"]["columns"]),
      "- **Low-information rooms** (fewer than five placed themes): %d, kept in the primary run and removed in the "
      "second." % low]
conc = {c["sub"]: c["concepts"] for c in r["case_information"]}
share = {c["sub"]: (c.get("residue_concepts") or 0) / ((c.get("placed_concepts") or 0) + (c.get("residue_concepts") or 0))
         if ((c.get("placed_concepts") or 0) + (c.get("residue_concepts") or 0)) else 0.0 for c in r["case_information"]}
w.append("- **The clusters** (two-letter codes; no mechanism labels; best-match Jaccard against the branches is "
         "descriptive, and ARI against the branches is undefined, since they overlap):")
for c in C:
    m = set(c["members"])
    best = max(B, key=lambda b: len(m & set(b["members"])) / len(m | set(b["members"])))
    top = sorted(c["profile"].items(), key=lambda x: -x[1])[:3]
    w.append("  - %s: %d rooms, %d low-information; largest profile shares %s; median concepts %d; mean residue share "
             "%.3f; best-match branch %s (Jaccard %.3f)." % (
                 c["code"], c["n"], c["n_low_information"], ", ".join("%s %.3f" % kv for kv in top),
                 statistics.median(conc[s] for s in c["members"]), statistics.mean(share[s] for s in c["members"]),
                 best["id"], len(m & set(best["members"])) / len(m | set(best["members"]))))
vals = sorted(share.values())
w += ["", "## The residue share per room (QD4-002)", "",
      "v1.1 counts a second-order theme placed only on the residue themes T3-017 (carrying on ordinary sub talk) and "
      "T3-133 (recovering a hacked sub) with the unplaced concepts, apart from the composition. %d rooms hold residue "
      "concepts (%d themes, %d concepts). The residue share is the room's residue concepts over its placed and residue "
      "concepts: median %.3f, mean %.3f, maximum %.3f. %d rooms are at 0.05 or more, %d at 0.10 or more and %d at "
      "0.30 or more. Rooms at 0.20 or more: %s. For these rooms the composition leaves out a large part of what the "
      "coders coded, the room's own ordinary business." % (
          sum(1 for v in vals if v > 0), sum(c.get("residue_themes") or 0 for c in r["case_information"]),
          sum(c.get("residue_concepts") or 0 for c in r["case_information"]), statistics.median(vals),
          statistics.mean(vals), vals[-1], sum(1 for v in vals if v >= .05), sum(1 for v in vals if v >= .10),
          sum(1 for v in vals if v >= .30),
          ", ".join("%s %.2f" % (s, v) for s, v in sorted(share.items(), key=lambda x: -x[1]) if v >= .2)), ""]
# volume check, as d4a03_volume.py
rng = random.Random(0)
rooms = sorted(conc)
cv = [conc[s] for s in rooms]
q = statistics.quantiles(cv, n=4)
lab = {s: c["code"] for c in C for s in c["members"]}
y = [math.log(conc[s]) for s in rooms]
L = [lab[s] for s in rooms]


def pct(members):
    med = statistics.median(conc[s] for s in members)
    null = [statistics.median(rng.sample(cv, len(members))) for _ in range(2000)]
    return med, 100.0 * sum(1 for x in null if x < med) / len(null) + 50.0 * sum(1 for x in null if x == med) / len(null)


bp = {b["id"]: pct(b["members"]) for b in B}
cp = {c["code"]: pct(c["members"]) for c in C}


def eta2(labels):
    mu = statistics.mean(y)
    tot = sum((v - mu) ** 2 for v in y)
    g = collections.defaultdict(list)
    for v, l in zip(y, labels):
        g[l].append(v)
    return sum(len(v) * (statistics.mean(v) - mu) ** 2 for v in g.values()) / tot


e = eta2(L)
null = []
for _ in range(2000):
    LL = L[:]
    rng.shuffle(LL)
    null.append(eta2(LL))
inb = set(m for b in B for m in b["members"])


def quart(v):
    return 1 if v <= q[0] else 2 if v <= q[1] else 3 if v <= q[2] else 4


ct = collections.Counter((lab[s], quart(conc[s])) for s in rooms)
ct2 = collections.Counter(("a branch" if s in inb else "no branch", quart(conc[s])) for s in rooms)
w += ["## The volume check (section 5), and the size of the rooms", "",
      "The volume field is the comparison's own count of unique concepts per room (median %d; quartile cuts %s). "
      "Percentiles are against random groups of the same size from the 705 rooms (2,000 draws, seed 0)." % (
          statistics.median(cv), ", ".join(str(round(x)) for x in q)),
      "- **The volume verdict for the clusters.** The cluster labels explain %.3f of the variance in log concepts "
      "(eta squared), at the %.1fth percentile of the permutation null (null maximum %.3f). By concept quartile "
      "(smallest first): %s. So the carried partition largely separates rooms by how much the coders coded." % (
          e, 100.0 * sum(1 for x in null if x < e) / len(null), max(null),
          "; ".join("%s %s" % (c["code"], " ".join(str(ct[(c['code'], k)]) for k in (1, 2, 3, 4))) for c in C)),
      "- **Branches and size.** In a branch, by quartile: %s; in no branch: %s. %d of %d branches have a median room "
      "size at or above the 95th percentile, and %d at or below the 5th. A larger room holds more lines and more "
      "keys, so it has more chances to share one; the branches lean to the larger rooms for that reason, at least in "
      "part. A correlation or this null alone cannot show that a branch's difference is independent of size." % (
          " ".join(str(ct2[("a branch", k)]) for k in (1, 2, 3, 4)),
          " ".join(str(ct2[("no branch", k)]) for k in (1, 2, 3, 4)),
          sum(1 for v in bp.values() if v[1] >= 95), len(B), sum(1 for v in bp.values() if v[1] <= 5)), ""]
w += ["## The projections (section 6), after every cut was snapped", "",
      "`python3 tools/projections.py` (2,000 permutations, seed 0) wrote `projections-D4.jsonl`, one line per branch "
      "and per cluster. Its verdict for a room is my last ruling at D3, else the readers' agreed verdict, so the first "
      "return and the re-check are mixed. The canvas sentence it carries: \"The atlas records what survived the last "
      "hour of a 97-hour event; it is not a measure of skill, and a large area is not evidence of good organizing "
      "(contract section 5).\" Each line below gives the verdict counts (composes, with residue, does not compose, "
      "cannot tell), the percentile of the does-not-compose share, the median area in pixels with its percentile, and "
      "the group's median room size with its percentile.", ""]
for p in P:
    key = p.get("branch") or p.get("cluster")
    v = p["verdicts"]
    cv_ = p["canvas"]
    size = bp.get(key) or cp.get(key)
    w.append("- %s: %d, %d, %d, %d; does-not-compose percentile %.1f; median area %s px, percentile %.1f; median "
             "size %d concepts, percentile %.1f." % (
                 key, v.get("composes", 0), v.get("composes-with-residue", 0), v.get("does-not-compose", 0),
                 v.get("cannot-tell", 0), p.get("percentile_does_not_compose"), cv_.get("median_area_px"),
                 cv_.get("percentile_median_area"), size[0], size[1]))
w += ["",
      "**Reading.** The one room that does not compose, picturegame (out-of-scope), lies in F21 and F25, so their "
      "does-not-compose percentiles are high; every other group's is near the middle. The canvas percentiles follow "
      "room size: the groups of large rooms (VA, CH, F11, F23, F29) have large median areas, and IT, the cluster of "
      "small rooms, has the smallest. No cut rests on the canvas or the verdicts; each cut was snapped before these "
      "were computed (rule 7).", "",
      "## What was drawn, and what was not", "",
      "- Drawn as views, from the carried distance: the average-linkage dendrogram (`_views/dendrogram.nwk`), a "
      "chain with no partition, and the leaf-to-root view (`_views/adaptation-tree.html`, `.svg`, `.json`), whose "
      "root is the frozen global model and whose JSON carries the branches and cross-links. Neither is read as a "
      "chronology, an ancestry or a validated hierarchy.",
      "- Not drawn: the NeighborNet (outside the run, if asked), and any tree of forms. The branches overlap (759 "
      "cross-links), so they are not a tree; they are facets of the rooms' adaptations.", "",
      "## The final accounting (stage D4 section 4)", "",
      "Against n_analysed = %d: %d rooms in a branch, 0 in the unadapted group, %d adapted but in no branch, 0 "
      "unreturned; the four sum to %d. The rooms in no branch are named, with their counts, in the accounting at "
      "D4a-02 above; no branch changed since." % (len(rooms), len(inb), len(rooms) - len(inb), len(rooms)), ""]
print("comparison k carried %s (all) and %s (without low-information); eta2 %.3f; branches at >=95th size %d; lines %d" % (
    r["all_cases"]["carried_k"], r["without_low_information"]["carried_k"], e,
    sum(1 for v in bp.values() if v[1] >= 95), len(w)))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(TREE, "a", encoding="utf-8") as f:
    f.write("\n".join(w) + "\n")
print("appended %d lines to tree-D4.md" % len(w))
