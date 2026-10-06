#!/usr/bin/env python3
"""projections.py, v38: stage D4 §6, projected on afterwards. After the cuts are snapped and the comparison
is built, one line per branch (branches.jsonl) and per cluster (chunk-share-D4.jsonl) into
out/projections-D4.jsonl: the D2 verdicts counted, with the percentile of the group's share of
does-not-compose against a permutation null (random groups of the same size drawn from the analysed set),
and the canvas fields summarised with the contract's sentence on what they measure and the same null for
the median area.

    python3 tools/projections.py [--root .] [--out out] [--permutations 2000] [--seed 0]

A room's verdict is the analyst's ruling at D3 when there is one (ruled_by analyst), else the readers'
verdict when they agree, else "split". Nothing here is read back into a cut (rule 7).
"""
import argparse, collections, json, os, random, statistics, sys

CANVAS_SENTENCE = ("The atlas records what survived the last hour of a 97-hour event; it is not a measure "
                   "of skill, and a large area is not evidence of good organizing (contract section 5).")
VERDICTS = ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")


def jl(p):
    out = []
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                try:
                    out.append(json.loads(l))
                except ValueError:
                    pass
    return out


def final_verdicts(out):
    ruled, readers = {}, collections.defaultdict(list)
    for r in jl(os.path.join(out, "verdicts-D.jsonl")):
        sub = r.get("sub")
        if r.get("ruled_by") == "analyst":
            ruled[sub] = r.get("verdict")
            continue
        for e in (r.get("readers") if isinstance(r.get("readers"), list) else [r]):
            if isinstance(e, dict) and e.get("verdict"):
                readers[sub].append(e["verdict"])
    final = {}
    for sub in set(ruled) | set(readers):
        if sub in ruled:
            final[sub] = ruled[sub]
        elif readers[sub] and len(set(readers[sub])) == 1:
            final[sub] = readers[sub][0]
        else:
            final[sub] = "split"
    return final


def percentile(obs, null):
    if obs is None or not null:
        return None
    # mid-rank: ties count half, so a group equal to most random groups sits near the middle (audit 2026-09-29b)
    less = sum(1 for x in null if x < obs)
    same = sum(1 for x in null if x == obs)
    return round(100.0 * (less + 0.5 * same) / len(null), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--permutations", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    out = a.out or os.path.join(a.root, "out")
    rooms = {r["sub"]: r for r in jl(os.path.join(a.root, "package", "store", "rooms.jsonl"))}
    dropped = {r.get("sub") for r in jl(os.path.join(out, "dropped.jsonl"))}
    analysed = sorted(set(rooms) - dropped)
    verdict = final_verdicts(out)
    groups = [("branch", b.get("id"), b.get("members") or []) for b in jl(os.path.join(out, "branches.jsonl"))]
    groups += [("cluster", c.get("code"), c.get("members") or []) for c in jl(os.path.join(out, "chunk-share-D4.jsonl"))]
    if not groups:
        sys.exit("no branches.jsonl and no chunk-share-D4.jsonl: the projections come after the cuts and the comparison")
    rnd = random.Random(a.seed)

    def dnc_share(members):
        v = [verdict.get(s) for s in members if verdict.get(s)]
        return (sum(1 for x in v if x == "does-not-compose") / len(v)) if v else None

    def med_area(members):
        xs = [rooms[s].get("canvas_area_px") for s in members if isinstance(rooms.get(s, {}).get("canvas_area_px"), (int, float))]
        return statistics.median(xs) if xs else None

    null_cache = {}
    lines = []
    for kind, gid, members in groups:
        members = [s for s in members if s in rooms]
        k = len(members)
        if k not in null_cache and 0 < k <= len(analysed):
            draws = [rnd.sample(analysed, k) for _ in range(a.permutations)]
            null_cache[k] = ([x for x in (dnc_share(d) for d in draws) if x is not None],
                             [x for x in (med_area(d) for d in draws) if x is not None])
        nd, na = null_cache.get(k, ([], []))
        counts = collections.Counter(verdict.get(s) for s in members if verdict.get(s) in VERDICTS)
        share, area = dnc_share(members), med_area(members)
        lines.append({kind: gid, "n": k,
                      "verdicts": {v: counts.get(v, 0) for v in VERDICTS},
                      "split_verdicts": sum(1 for s in members if verdict.get(s) == "split"),
                      "does_not_compose_share": round(share, 3) if share is not None else None,
                      "percentile_does_not_compose": percentile(share, nd),
                      "canvas": {"median_area_px": area,
                                 "rooms_with_artwork": sum(1 for s in members if (rooms.get(s, {}).get("canvas_entries") or 0) > 0),
                                 "percentile_median_area": percentile(area, na),
                                 "what_it_measures": CANVAS_SENTENCE},
                      "permutations": a.permutations, "seed": a.seed})
    with open(os.path.join(out, "projections-D4.jsonl"), "w", encoding="utf-8") as f:
        for l in lines:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    print("projections-D4.jsonl: %d branch line(s), %d cluster line(s)" % (
        sum(1 for g in groups if g[0] == "branch"), sum(1 for g in groups if g[0] == "cluster")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
