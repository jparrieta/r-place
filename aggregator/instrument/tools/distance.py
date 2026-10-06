#!/usr/bin/env python3
"""distance.py — the stage-D4 distance: the ladder walk times the operation agreement
(SCHEMA-adaptations.md §7): d = (1 - S) / 2 with S in [-1, 1], so 0 is identical, 0.5 unrelated,
1 opposite; a room with no lines is 0.5 from every adapted room and 0 from another empty room; the per-level and per-kind key matrices, and the tree-likeness
statistic (the delta score of Holland et al. 2002, averaged over sampled quartets).

    python3 tools/distance.py [--out out] [--ledger out/adaptations.jsonl] [--prior out/prior.md]
                              [--quartets 20000] [--seed 0]

Reads accepted and modified lines (decision in {accept, modify}) whose lift exists; particulars,
pending and rejected lines are excluded. Writes:
  out/_views/rooms-x-adaptations.<level>.<kind>.tsv   level in {3,4,dim,target}; kind in
                                                     {all, specification, elaboration, correction}
  out/_views/distance.tsv                            the combined room-by-room distance
  out/_views/distance.<kind>.tsv                     per kind
  out/_views/tree-likeness.json                      delta score on the combined matrix, the weights
                                                     and grades used and where they came from
  out/_views/delta-by-room.tsv                       each room's delta score, over sampled quartets that
                                                     hold it (Holland et al. 2002's per-taxon delta)
  out/_views/dendrogram.nwk, dendrogram.txt          average linkage (UPGMA) on the combined distance, in
                                                     Newick, and the rooms at 2, 3, 5, 8 and 12 clusters
  out/_views/distance.nex                            the combined distance as a NEXUS distances block, for
                                                     SplitsTree's NeighborNet (drawn outside the run; the
                                                     analyst reads the dendrogram and the deltas here)
Weights and grades come from prior.md §7 (the lines `w = a, b, c, d` and `g = a, b, c, d`); where §7
does not parse, the defaults below are used and tree-likeness.json and the output say so.
"""
import argparse, collections, itertools, json, math, os, random, re, sys
from adaptation_ledger import shared_lines, effective_rooms, ledger_provenance

W_DEFAULT = {"3": 4.0, "4": 2.0, "dim": 1.0, "target": 0.5}
G_DEFAULT = {"same_op": 1.0, "same_kind": 0.5, "diff_kind": 0.0, "opposite": -1.0}
OPPOSITE = {frozenset(["instantiate", "absent"]), frozenset(["add-condition", "contradict"])}
LEVELS = ["3", "4", "dim", "target"]
KINDS = ["specification", "elaboration", "correction"]


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


W_LINE = re.compile(r"w\s*=\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)")
G_LINE = re.compile(r"g\s*=\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)")


def read_prior(p, report=None):
    """(weights, grades) from prior.md §7; report, a dict, records where each came from."""
    w, g = dict(W_DEFAULT), dict(G_DEFAULT)
    src = {"weights": "defaults", "grades": "defaults"}
    txt = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    m = W_LINE.search(txt)
    if re.search(r"\bw\s*=",txt) and not m:raise ValueError("Malformed weight declaration in prior")
    if m:
        w = dict(zip(LEVELS, map(float, m.groups()))); src["weights"] = "prior.md §7"
    m = G_LINE.search(txt)
    if re.search(r"\bg\s*=",txt) and not m:raise ValueError("Malformed grade declaration in prior")
    if m:
        g = dict(zip(["same_op", "same_kind", "diff_kind", "opposite"], map(float, m.groups()))); src["grades"] = "prior.md §7"
    if report is not None:
        report.update(src)
    for k, v in src.items():
        if v == "defaults":
            print("warning: prior.md §7 gives no %s line in the declared form; the defaults are used" % k[:-1], file=sys.stderr)
    if not all(math.isfinite(x) for x in list(w.values()) + list(g.values())) or not (w["3"] > 0 and w["3"] >= w["4"] >= w["dim"] >= w["target"] >= 0) or not all(-1 <= x <= 1 for x in g.values()) or g["same_op"] != 1:
        raise ValueError("Invalid prior: require descending nonnegative weights, positive w3, bounded grades and same_op=1")
    return w, g


def node_at(line, level):
    lift = line.get("lift") or [None, None, None, None]
    if level == "3":
        return lift[1]
    if level == "4":
        return lift[2]
    if level == "dim":
        return lift[3]
    return "*"


def grade(a, b, g):
    if a["op"] == b["op"]:
        return g["same_op"]
    if frozenset([a["op"], b["op"]]) in OPPOSITE:
        return g["opposite"]
    if a["kind"] == b["kind"]:
        return g["same_kind"]
    return g["diff_kind"]


def similarity(lines_i, lines_j, w, g):
    """Per target, the deepest level at which some line of i and some line of j meet, and the
    best grade among the pairs meeting there; S = sum(w * g) / (w3 * |T|)."""
    by_t_i = collections.defaultdict(list)
    by_t_j = collections.defaultdict(list)
    for l in lines_i:
        by_t_i[l["element"]].append(l)
    for l in lines_j:
        by_t_j[l["element"]].append(l)
    T = set(by_t_i) | set(by_t_j)
    if not T:
        return None
    total = 0.0
    for t in T:
        if t not in by_t_i or t not in by_t_j:
            continue
        # Explicit observed absence has no source path: agreement is target-level identity.
        if all(r.get("op") == "absent" for r in by_t_i[t]+by_t_j[t]):
            total += w["3"] * g["same_op"]
            continue
        best = None
        for level in LEVELS:
            pairs = [(a, b) for a in by_t_i[t] for b in by_t_j[t]
                     if node_at(a, level) is not None and node_at(a, level) == node_at(b, level)]
            if pairs:
                best = (w[level], max(grade(a, b, g) for a, b in pairs))
                break
        if best:
            total += best[0] * best[1]
    return total / (w["3"] * len(T))


def delta_score(names, D, n_quartets, seed):
    rnd = random.Random(seed)
    n = len(names)
    if n < 4:
        return None
    idx = list(range(n))
    vals = []
    for _ in range(n_quartets):
        x, y, z, u = rnd.sample(idx, 4)
        s = sorted([D[x][y] + D[z][u], D[x][z] + D[y][u], D[x][u] + D[y][z]])
        if s[2] - s[0] > 1e-12:
            vals.append((s[2] - s[1]) / (s[2] - s[0]))
    return sum(vals) / len(vals) if vals else None


def quartet_diagnostics(names, D, draws, seed):
    if draws < 1: raise ValueError("quartets must be positive")
    if len(names)<4:return {"sampled":0,"unique":0,"nondegenerate":0,"equal_sum":0,"mc_se":None}
    rnd=random.Random(seed);values=[];unique=set()
    for _ in range(draws):
        q=tuple(sorted(rnd.sample(range(len(names)),4)));unique.add(q);x,y,z,u=q
        sums=sorted([D[x][y]+D[z][u],D[x][z]+D[y][u],D[x][u]+D[y][z]])
        if sums[2]-sums[0]>1e-12:values.append((sums[2]-sums[1])/(sums[2]-sums[0]))
    if len(values)>1:
        avg=sum(values)/len(values);se=math.sqrt(sum((x-avg)**2 for x in values)/(len(values)-1)/len(values))
    else:se=None
    return {"sampled":draws,"unique":len(unique),"nondegenerate":len(values),"equal_sum":draws-len(values),"mc_se":se,"interpretation":"Monte Carlo error conditional on this fixed dissimilarity matrix, not sampling uncertainty for cases."}


def delta_by_room(names, D, per_room, seed):
    """Each room's mean delta over sampled quartets that hold it (Holland et al. 2002, per taxon)."""
    rnd = random.Random(seed)
    n = len(names)
    out = {}
    if n < 4:
        return out
    idx = list(range(n))
    for x in idx:
        vals = []
        others = [i for i in idx if i != x]
        for _ in range(per_room):
            y, z, u = rnd.sample(others, 3)
            s = sorted([D[x][y] + D[z][u], D[x][z] + D[y][u], D[x][u] + D[y][z]])
            if s[2] - s[0] > 1e-12:
                vals.append((s[2] - s[1]) / (s[2] - s[0]))
        out[names[x]] = sum(vals) / len(vals) if vals else None
    return out


def upgma(names, D):
    """Average linkage by the nearest-neighbour chain (exact for a reducible linkage). Returns the merges
    [(a, b, height, size)] with clusters as indices, leaves 0..n-1 and merged clusters n, n+1, ..."""
    n = len(names)
    dist = {i: {j: D[i][j] for j in range(n) if j != i} for i in range(n)}
    size = {i: 1 for i in range(n)}
    active, nxt, merges, chain = set(range(n)), n, [], []
    while len(active) > 1:
        if not chain:
            chain.append(next(iter(active)))
        a = chain[-1]
        b = min(dist[a], key=lambda k: (dist[a][k], k))
        if len(chain) > 1 and chain[-2] == b:
            chain.pop(); chain.pop()
            h = dist[a][b]
            c = nxt; nxt += 1
            size[c] = size[a] + size[b]
            dist[c] = {}
            for k in active - {a, b}:
                dk = (size[a] * dist[a][k] + size[b] * dist[b][k]) / size[c]
                dist[c][k] = dk
                dist[k][c] = dk
                del dist[k][a], dist[k][b]
            active -= {a, b}
            active.add(c)
            del dist[a], dist[b]
            merges.append((a, b, h, size[c]))
        else:
            chain.append(b)
    return merges


def newick(names, merges):
    n = len(names)
    if not n:
        return ";"
    node = {i: re.sub(r"[^A-Za-z0-9_]", "_", names[i]) for i in range(n)}
    height = {i: 0.0 for i in range(n)}
    for k, (a, b, h, _s) in enumerate(merges):
        c = n + k
        node[c] = "(%s:%.17g,%s:%.17g)" % (node[a], max(0.0, h / 2 - height[a]), node[b], max(0.0, h / 2 - height[b]))
        height[c] = h / 2
    return node[n + len(merges) - 1] + ";" if merges else node[0] + ";"


def cut(names, merges, k):
    """The rooms in k clusters: undo the k-1 highest merges (the chain does not merge in height order)."""
    n = len(names)
    parent = {}
    drop = set(sorted(range(len(merges)), key=lambda i: (merges[i][2], i))[len(merges) - (k - 1):]) if k > 1 else set()
    for idx, (a, b, _h, _s) in enumerate(merges):
        if idx in drop:
            continue
        parent[a] = parent[b] = n + idx
    def root(i):
        while i in parent:
            i = parent[i]
        return i
    groups = collections.defaultdict(list)
    for i in range(n):
        groups[root(i)].append(names[i])
    return sorted(groups.values(), key=lambda g: (-len(g), g))


def write_tsv(path, rows, header):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="out")
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--prior", default=None)
    ap.add_argument("--quartets", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.ledger and os.path.abspath(a.ledger) != os.path.abspath(os.path.join(a.out,"adaptations.jsonl")):
        raise ValueError("Alternate ledger paths are unsupported: use a complete disposable out directory with its manifest and adjudications")
    src = {}
    w, g = read_prior(a.prior or os.path.join(a.out, "prior.md"), src)
    keep = shared_lines(a.out)
    returns = effective_rooms(a.out)
    root = os.path.dirname(a.out.rstrip("/")) or "."
    dropped = {r.get("sub") for r in jl(os.path.join(a.out, "dropped.jsonl"))}
    unret = set()
    up = os.path.join(root, "DROPS", "D", "UNRETURNED.tsv")
    if os.path.exists(up):
        unret = {l.split("\t")[0].strip() for l in open(up, encoding="utf-8") if l.strip() and not l.startswith(("sub\t", "#"))}
    rooms = sorted((set(returns) | {r["sub"] for r in jl(os.path.join(root, "package", "store", "rooms.jsonl"))})
                   - dropped - unret)   # the analysed set less the unreturned, which are listed apart (D4 section 3)
    unexplained = set(rooms) - set(returns)
    if unexplained:
        raise ValueError("Rooms with neither accepted return nor unreturned record: " + ", ".join(sorted(unexplained)))
    by_room = collections.defaultdict(list)
    for l in keep:
        by_room[l["sub"]].append(l)
    vd = os.path.join(a.out, "_views")
    os.makedirs(vd, exist_ok=True)
    # key matrices
    for level in LEVELS:
        for kind in ["all"] + KINDS:
            keys = collections.defaultdict(set)
            for l in keep:
                if kind != "all" and l["kind"] != kind:
                    continue
                node = node_at(l, level)
                if node is None:
                    continue
                keys[l["sub"]].add("%s:%s:%s" % (l["op"], l["element"], node))
            allk = sorted(set().union(*keys.values())) if keys else []
            rows = [[r] + [1 if k in keys.get(r, set()) else 0 for k in allk] for r in rooms]
            write_tsv(os.path.join(vd, "rooms-x-adaptations.%s.%s.tsv" % (level, kind)), rows, ["room"] + allk)
    # distances
    result = {"weights": w, "grades": g, "weights_from": src.get("weights"), "grades_from": src.get("grades"),
              "rooms": len(rooms), "lines_used": len(keep), "input_sha256": ledger_provenance(a.out), "unreturned": sorted(unret), "seed": a.seed, "quartets_requested": a.quartets, "score_semantics": "Nonmetric best-match dissimilarity; explicit observed absences agree at target; incomplete source paths remain partially comparable."}
    for kind in ["all"] + KINDS:
        n = len(rooms)
        D = [[0.0] * n for _ in range(n)]
        for i, j in itertools.combinations(range(n), 2):
            li = [l for l in by_room[rooms[i]] if kind == "all" or l["kind"] == kind]
            lj = [l for l in by_room[rooms[j]] if kind == "all" or l["kind"] == kind]
            if not li and not lj:
                d = 0.0
            elif not li or not lj:
                d = 0.5
            else:
                S = similarity(li, lj, w, g)
                d = (1.0 - max(-1.0, min(1.0, S))) / 2.0
            D[i][j] = D[j][i] = d
        name = "distance.tsv" if kind == "all" else "distance.%s.tsv" % kind
        write_tsv(os.path.join(vd, name), [[rooms[i]] + ["%.17g" % D[i][j] for j in range(n)] for i in range(n)],
                  ["room"] + rooms)
        if kind == "all":
            result["delta_score"] = delta_score(rooms, D, a.quartets, a.seed)
            result["quartet_diagnostics"] = quartet_diagnostics(rooms,D,a.quartets,a.seed)
            result["delta_note"] = ("Nondegenerate quartet delta ranges from 0 to 1; larger means less additive. "
                                    "Equal-sum quartets are excluded. No 0.5 star or network threshold.")
            per = delta_by_room(rooms, D, max(50, a.quartets // max(1, n)), a.seed)
            write_tsv(os.path.join(vd, "delta-by-room.tsv"),
                      sorted([[r, "%.4f" % v if v is not None else ""] for r, v in per.items()], key=lambda x: x[1], reverse=True),
                      ["room", "delta"])
            merges = upgma(rooms, D) if n > 1 else []
            open(os.path.join(vd, "dendrogram.nwk"), "w", encoding="utf-8").write(newick(rooms, merges) + "\n")
            L = ["# The dendrogram: average linkage on the combined distance (distance.tsv)", ""]
            for k in (2, 3, 5, 8, 12):
                if k <= n:
                    L.append("## %d clusters" % k)
                    L += ["- %d rooms: %s" % (len(gr), ", ".join(gr[:30]) + (" ..." if len(gr) > 30 else ""))
                          for gr in cut(rooms, merges, k)]
                    L.append("")
            open(os.path.join(vd, "dendrogram.txt"), "w", encoding="utf-8").write("\n".join(L))
            nex = ["#NEXUS", "BEGIN taxa;", "  DIMENSIONS ntax=%d;" % n, "  TAXLABELS"]
            nex += ["    %s" % re.sub(r"[^A-Za-z0-9_]", "_", r) for r in rooms] + ["  ;", "END;", "BEGIN distances;",
                    "  DIMENSIONS ntax=%d;" % n, "  FORMAT triangle=both diagonal labels=left;", "  MATRIX"]
            nex += ["    %s %s" % (re.sub(r"[^A-Za-z0-9_]", "_", rooms[i]), " ".join("%.17g" % D[i][j] for j in range(n)))
                    for i in range(n)] + ["  ;", "END;"]
            open(os.path.join(vd, "distance.nex"), "w", encoding="utf-8").write("\n".join(nex) + "\n")
    json.dump(result, open(os.path.join(vd, "tree-likeness.json"), "w"), indent=1)
    from adaptation_tree import generate
    generate(a.out)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
