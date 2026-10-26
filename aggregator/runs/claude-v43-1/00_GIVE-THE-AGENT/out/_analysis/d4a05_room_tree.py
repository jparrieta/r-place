#!/usr/bin/env python3
"""D4a-05: the room tree (J's amendment of 26 October 2026; method logged in the diary before this ran).

Reads the shared ledger lines (tools/adaptation_ledger.shared_lines), branches.jsonl (only to map the 35
branches afterwards), the code store and theme placements (only for the check against the codes, after
the tree is cut), and chunk-share-D4.jsonl (for the Rand index against the comparison's clusters).
It reads no canvas field and no verdict. Writes nothing; prints one JSON object.

    python3 out/_analysis/d4a05_room_tree.py > out/_analysis/d4a05_tree.json
"""
import collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, to_tree
from scipy.spatial.distance import pdist, squareform
from scipy.stats import kruskal
from sklearn.metrics import silhouette_score, adjusted_rand_score

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
LEVELS = ((1, "T3"), (2, "T4"), (3, "dim"))
KS = range(4, 9)
MIN_GROUP = 5


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


# ---- the selected changes -----------------------------------------------------------------------
LINES = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE]
ALL_ROOMS = sorted(al.effective_rooms(OUT), key=str.lower)
PLACED = [r for r in LINES if len(r.get("lift") or []) >= 4]
UNPLACED = [r["id"] for r in LINES if len(r.get("lift") or []) < 4]
CHANGED = sorted({r["sub"] for r in PLACED}, key=str.lower)
CORE = sorted(set(ALL_ROOMS) - set(CHANGED), key=str.lower)
IDX = {s: i for i, s in enumerate(CHANGED)}


def count_matrices(lines, drop_single=True):
    mats, cols = {}, {}
    for i, lv in LEVELS:
        held = collections.defaultdict(set)
        for r in lines:
            if r["lift"][i]:  # a residue third-order theme has no fourth-order node or dimension
                held[r["lift"][i]].add(r["sub"])
        keep = sorted(k for k, v in held.items() if not (drop_single and lv == "T3" and len(v) == 1))
        ci = {k: j for j, k in enumerate(keep)}
        m = np.zeros((len(CHANGED), len(keep)))
        for r in lines:
            k = r["lift"][i]
            if k in ci:
                m[IDX[r["sub"]], ci[k]] += 1
        mats[lv], cols[lv] = m, keep
    return mats, cols


def embed(mats):
    blocks = []
    for _, lv in LEVELS:
        m = mats[lv]
        tot = m.sum(axis=1, keepdims=True)
        p = np.divide(m, tot, out=np.zeros_like(m), where=tot > 0)
        blocks.append(np.sqrt(p) / math.sqrt(2 * len(LEVELS)))
    return np.hstack(blocks)


MATS, COLS = count_matrices(PLACED)
X = embed(MATS)
D = squareform(pdist(X))
Z = linkage(X, method="ward")
rng = np.random.default_rng(0)


def ward_labels(Xs, k):
    return fcluster(linkage(Xs, method="ward"), k, criterion="maxclust")


def permuted(mats, idx, rg):
    out = {}
    for _, lv in LEVELS:
        m = mats[lv][idx].copy()
        for j in range(m.shape[1]):
            m[:, j] = rg.permutation(m[:, j])
        out[lv] = m
    return out


# ---- the top: k = 4 to 8 -------------------------------------------------------------------------
top = {}
null_rng = np.random.default_rng(1)
null_sil = {k: [] for k in KS}
for _ in range(20):
    Xn = embed(permuted(MATS, np.arange(len(CHANGED)), null_rng))
    Zn = linkage(Xn, method="ward")
    Dn = squareform(pdist(Xn))
    for k in KS:
        ln = fcluster(Zn, k, criterion="maxclust")
        null_sil[k].append(float(silhouette_score(Dn, ln, metric="precomputed")))
boot_rng = np.random.default_rng(0)
boots = [boot_rng.integers(0, len(CHANGED), len(CHANGED)) for _ in range(100)]
for k in KS:
    lab = fcluster(Z, k, criterion="maxclust")
    sizes = sorted(collections.Counter(lab).values(), reverse=True)
    aris = []
    for b in boots:
        lb = ward_labels(X[b], k)
        first = {}
        for pos, i in enumerate(b):
            first.setdefault(int(i), lb[pos])
        u = sorted(first)
        aris.append(adjusted_rand_score(lab[u], [first[i] for i in u]))
    top[k] = {"sizes": sizes, "ratio": round(sizes[0] / sizes[-1], 2),
              "silhouette": round(float(silhouette_score(D, lab, metric="precomputed")), 4),
              "boot_ari_mean": round(float(np.mean(aris)), 3), "boot_ari_sd": round(float(np.std(aris)), 3),
              "null_sil_mean": round(float(np.mean(null_sil[k])), 4),
              "null_sil_p95": round(float(np.percentile(null_sil[k], 95)), 4),
              "merge_height": round(float(Z[-(k - 1), 2]), 4)}
best = max(KS, key=lambda k: top[k]["silhouette"])
k_chosen = best if top[best]["boot_ari_mean"] >= 0.5 else max(KS, key=lambda k: top[k]["boot_ari_mean"])
LAB = fcluster(Z, k_chosen, criterion="maxclust")

# order the forms by size (largest first) and letter them A, B, ...
order = [c for c, _ in collections.Counter(LAB).most_common()]
letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
FORM = {s: letter[LAB[IDX[s]]] for s in CHANGED}
FORMS = sorted(set(FORM.values()))


# ---- profiles and signatures ----------------------------------------------------------------------
def shares(lv):
    m = MATS[lv]
    tot = m.sum(axis=1, keepdims=True)
    return np.divide(m, tot, out=np.zeros_like(m), where=tot > 0)


SH = {lv: shares(lv) for _, lv in LEVELS}
POP = {lv: SH[lv].mean(axis=0) for _, lv in LEVELS}
names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dims = {r["id"]: r.get("name") or r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
try:
    third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
except Exception:
    third = {}


def profile(members, lv, floor_presence):
    idx = [IDX[s] for s in members]
    sh = SH[lv][idx].mean(axis=0)
    pres = (MATS[lv][idx] > 0).mean(axis=0)
    rows = []
    for j, node in enumerate(COLS[lv]):
        ratio = sh[j] / POP[lv][j] if POP[lv][j] > 0 else None
        rows.append({"node": node, "share": round(float(sh[j]), 4), "pop_share": round(float(POP[lv][j]), 4),
                     "ratio": round(float(ratio), 2) if ratio else None, "presence": round(float(pres[j]), 3)})
    sig = [r for r in rows if r["ratio"] and r["ratio"] >= 1.5 and r["presence"] >= floor_presence]
    return rows, sorted(sig, key=lambda r: -r["share"])


def entropy_dim(i):
    p = SH["dim"][i]
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / math.log(len(COLS["dim"])))


NCH = collections.Counter(r["sub"] for r in PLACED)
NO_NODE = {lv: sum(1 for r in PLACED if not r["lift"][i]) for i, lv in LEVELS}
ZERO_ROW = {lv: [s for s in CHANGED if MATS[lv][IDX[s]].sum() == 0] for _, lv in LEVELS}
form_info = {}
for f in FORMS:
    mem = [s for s in CHANGED if FORM[s] == f]
    r4, sig4 = profile(mem, "T4", 1 / 3)
    r3, sig3 = profile(mem, "T3", 1 / 4)
    rd, sigd = profile(mem, "dim", 1 / 3)
    form_info[f] = {"n": len(mem), "members": mem,
                    "sig_T4": [dict(r, name=names4.get(r["node"])) for r in sig4],
                    "sig_T3": [dict(r, name=third.get(r["node"])) for r in sig3[:8]],
                    "dims": sorted([dict(r, name=dims.get(r["node"])) for r in rd], key=lambda r: -r["share"]),
                    "median_changes": float(np.median([NCH[s] for s in mem])),
                    "mean_dim_entropy": round(float(np.mean([entropy_dim(IDX[s]) for s in mem])), 3)}
pop_entropy = round(float(np.mean([entropy_dim(i) for i in range(len(CHANGED))])), 3)

# ---- fit, counter-examples, secondary forms -------------------------------------------------------
cent = {f: X[[IDX[s] for s in form_info[f]["members"]]].mean(axis=0) for f in FORMS}
room_rows = {}
for s in CHANGED:
    i = IDX[s]
    d = {f: float(np.linalg.norm(X[i] - cent[f])) for f in FORMS}
    own = FORM[s]
    others = sorted((v, f) for f, v in d.items() if f != own)
    t4 = MATS["T4"][i]
    tot4 = t4.sum()
    sig_share = {}
    for f in FORMS:
        nodes = {r["node"] for r in form_info[f]["sig_T4"]}
        sig_share[f] = float(sum(t4[j] for j, n in enumerate(COLS["T4"]) if n in nodes) / tot4) if tot4 else 0.0
    room_rows[s] = {"form": own, "d_own": round(d[own], 4), "nearest_other": others[0][1],
                    "d_other": round(others[0][0], 4), "nearer_other": others[0][0] < d[own],
                    "fits_two": others[0][0] <= 1.05 * d[own],
                    "secondary": sorted(f for f in FORMS if f != own and sig_share[f] >= 0.25),
                    "sig_share_own": round(sig_share[own], 3), "changes": NCH[s],
                    "top_dims": [COLS["dim"][j] for j in np.argsort(-SH["dim"][i])[:2] if SH["dim"][i][j] > 0]}


# ---- below each form ------------------------------------------------------------------------------
def r2_split(Xs, lab):
    tot = ((Xs - Xs.mean(axis=0)) ** 2).sum()
    within = sum(((Xs[lab == c] - Xs[lab == c].mean(axis=0)) ** 2).sum() for c in set(lab))
    return 1 - within / tot if tot > 0 else 0.0


split_rng = np.random.default_rng(2)
stab_rng = np.random.default_rng(4)
STAB_MIN = 0.6
nodes = []
leaf_of = {}


def clusterwise_jaccard(Xs, lab, k, rg, nboot=100):
    """Hennig (2007): for each original cluster, the mean over bootstrap resamples of the best Jaccard
    match among the resample's Ward clusters, computed on the unique resampled rooms."""
    lab = np.asarray(lab)
    orig = {c: set(np.where(lab == c)[0]) for c in sorted(set(lab))}
    acc = {c: [] for c in orig}
    n = len(lab)
    for _ in range(nboot):
        b = rg.integers(0, n, n)
        lb = fcluster(linkage(Xs[b], method="ward"), k, criterion="maxclust")
        first = {}
        for pos, i in enumerate(b):
            first.setdefault(int(i), lb[pos])
        U = set(first)
        groups = collections.defaultdict(set)
        for i, l in first.items():
            groups[l].add(i)
        for c, mem in orig.items():
            cm = mem & U
            if not cm:
                continue
            acc[c].append(max(len(cm & g) / len(cm | g) for g in groups.values()))
    return {int(c): round(float(np.mean(v)), 3) if v else None for c, v in acc.items()}


def newick(members):
    if len(members) == 1:
        return members[0]
    Zs = linkage(X[[IDX[s] for s in members]], method="ward")
    t = to_tree(Zs)

    def rec(n):
        if n.is_leaf():
            return members[n.id]
        return "(%s,%s)" % (rec(n.get_left()), rec(n.get_right()))
    return rec(t)


def split(members, nid, depth):
    rec = {"id": nid, "n": len(members), "depth": depth, "members": members, "kept_split": False}
    nodes.append(rec)
    if len(members) < 2 * MIN_GROUP:
        rec["why_stop"] = "fewer than %d rooms" % (2 * MIN_GROUP)
        for s in members:
            leaf_of[s] = nid
        rec["newick"] = newick(members)
        return
    idx = [IDX[s] for s in members]
    Xs = X[idx]
    lab = fcluster(linkage(Xs, method="ward"), 2, criterion="maxclust")
    sizes = collections.Counter(lab)
    real = r2_split(Xs, lab)
    sub = {lv: MATS[lv][idx] for _, lv in LEVELS}
    nulls = []
    for _ in range(99):
        mp = {}
        for _, lv in LEVELS:
            m = sub[lv].copy()
            for j in range(m.shape[1]):
                m[:, j] = split_rng.permutation(m[:, j])
            mp[lv] = m
        Xn = embed(mp)
        ln = fcluster(linkage(Xn, method="ward"), 2, criterion="maxclust")
        nulls.append(r2_split(Xn, ln))
    p95 = float(np.percentile(nulls, 95))
    rec.update({"split_sizes": sorted(sizes.values(), reverse=True), "r2": round(float(real), 4),
                "null_r2_p95": round(p95, 4), "null_r2_mean": round(float(np.mean(nulls)), 4)})
    why = None
    if min(sizes.values()) < MIN_GROUP:
        why = "a half below %d rooms" % MIN_GROUP
    elif real <= p95:
        why = "split within the null"
    else:
        jac = clusterwise_jaccard(Xs, lab, 2, stab_rng)
        rec["jaccard"] = {str(c): v for c, v in jac.items()}
        rec["child_jaccard"] = {"%s.%d" % (nid, j): jac[int(c)] for j, (c, _) in enumerate(sizes.most_common(), 1)}
        if min(v for v in jac.values() if v is not None) < STAB_MIN:
            why = "a half not stable under resampling (Jaccard below %.1f)" % STAB_MIN
    if why:
        rec["why_stop"] = why
        for s in members:
            leaf_of[s] = nid
        rec["newick"] = newick(members)
        return
    rec["kept_split"] = True
    kids = [c for c, _ in sizes.most_common()]
    for j, c in enumerate(kids, 1):
        split([s for s, l in zip(members, lab) if l == c], "%s.%d" % (nid, j), depth + 1)


for f in FORMS:
    split(form_info[f]["members"], f, 0)
for n in nodes:
    if n["id"] not in FORMS:
        r4, sig4 = profile(n["members"], "T4", 1 / 3)
        r3, sig3 = profile(n["members"], "T3", 1 / 4)
        n["sig_T4"] = [dict(r, name=names4.get(r["node"])) for r in sig4[:5]]
        n["sig_T3"] = [dict(r, name=third.get(r["node"])) for r in sig3[:5]]
        n["median_changes"] = float(np.median([NCH[s] for s in n["members"]]))

# ---- the 35 branches as the level below -----------------------------------------------------------
B = jl(os.path.join(OUT, "branches.jsonl"))
lvl = {"third": 1, "fourth": 2, "dimension": 3}
by_room = collections.defaultdict(list)
for r in PLACED:
    by_room[r["sub"]].append(r)
branch_rows = {}
for b in B:
    op, el, node = b["keys"][0].split(":")
    li = lvl[b["level"]]
    for s in b["members"]:
        cnt = sum(1 for r in by_room.get(s, []) if r["op"] == op and r["element"] == el and r["lift"][li] == node)
        branch_rows.setdefault(s, []).append((b["id"], cnt, b.get("parent")))
primary_branch, secondary_branch = {}, {}
for s, rows in branch_rows.items():
    rows.sort(key=lambda x: (-x[1], 0 if x[2] else 1, int(x[0][1:])))
    primary_branch[s] = rows[0][0]
    secondary_branch[s] = sorted((x[0] for x in rows[1:]), key=lambda z: int(z[1:]))
branch_place = {}
for b in B:
    c = collections.Counter(FORM.get(s, "core") for s in b["members"])
    home, nh = c.most_common(1)[0]
    branch_place[b["id"]] = {"n": len(b["members"]), "home_form": home, "home_share": round(nh / len(b["members"]), 3),
                             "by_form": dict(sorted(c.items())),
                             "primary_members": sum(1 for s in b["members"] if primary_branch.get(s) == b["id"])}

# ---- check against the codes (not used by the tree) -----------------------------------------------
t4m = {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in r.get("members") or []:
        t4m[m] = r["id"]
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
ccount = collections.Counter()
ncodes = collections.Counter()
for r in jl(os.path.join(STORE, "codes.jsonl")):
    ccount[(r["sub"], r.get("theme_id"))] += 1
    ncodes[r["sub"]] += 1
comp = collections.defaultdict(collections.Counter)
for (s, t), n in ccount.items():
    ns = [t4m[x] for x in place.get((s, t), []) if x in t4m]
    for node in ns:
        comp[s][node] += n / len(ns)
cnodes = sorted({k for c in comp.values() for k in c})
C = np.array([[comp[s].get(k, 0.0) for k in cnodes] for s in CHANGED])
C = np.sqrt(C / np.maximum(C.sum(axis=1, keepdims=True), 1e-12)) / math.sqrt(2)
labels = np.array([FORMS.index(FORM[s]) for s in CHANGED])


def pseudo_f(M, lab):
    g = M.mean(axis=0)
    sst = ((M - g) ** 2).sum()
    ssw = sum(((M[lab == c] - M[lab == c].mean(axis=0)) ** 2).sum() for c in set(lab))
    k, n = len(set(lab)), len(lab)
    return ((sst - ssw) / (k - 1)) / (ssw / (n - k)), 1 - ssw / sst


Fr, R2r = pseudo_f(C, labels)
perm_rng = np.random.default_rng(3)
Fn = [pseudo_f(C, perm_rng.permutation(labels))[0] for _ in range(999)]


def loo_nearest(M, lab):
    hit = 0
    for i in range(len(lab)):
        best_c, best_d = None, None
        for c in set(lab):
            sel = (lab == c)
            sel[i] = False
            if not sel.any():
                continue
            d = np.linalg.norm(M[i] - M[sel].mean(axis=0))
            if best_d is None or d < best_d:
                best_c, best_d = c, d
        hit += best_c == lab[i]
    return hit / len(lab)


acc = loo_nearest(C, labels)
acc_null = [loo_nearest(C, perm_rng.permutation(labels)) for _ in range(20)]
code_profiles = {}
popc = C.mean(axis=0) ** 2  # rough share scale for reporting only
Cs = np.array([[comp[s].get(k, 0.0) for k in cnodes] for s in CHANGED])
Cs = Cs / np.maximum(Cs.sum(axis=1, keepdims=True), 1e-12)
popsh = Cs.mean(axis=0)
for f in FORMS:
    sel = labels == FORMS.index(f)
    sh = Cs[sel].mean(axis=0)
    rows = sorted(((cnodes[j], float(sh[j]), float(popsh[j])) for j in range(len(cnodes)) if popsh[j] > 0.005),
                  key=lambda x: -(x[1] / x[2]))
    code_profiles[f] = {"over": [{"node": a, "name": names4.get(a), "share": round(b, 4), "pop_share": round(c, 4),
                                  "ratio": round(b / c, 2)} for a, b, c in rows[:4]],
                        "under": [{"node": a, "name": names4.get(a), "share": round(b, 4), "pop_share": round(c, 4),
                                   "ratio": round(b / c, 2)} for a, b, c in rows[-3:]],
                        "median_codes": float(np.median([ncodes[s] for s in form_info[f]["members"]]))}
kw = kruskal(*[[ncodes[s] for s in form_info[f]["members"]] for f in FORMS])
kw_changes = kruskal(*[[NCH[s] for s in form_info[f]["members"]] for f in FORMS])

# chunk-share clusters
chunk = {}
p = os.path.join(OUT, "chunk-share-D4.jsonl")
if os.path.exists(p):
    for r in jl(p):
        for s in r.get("members") or []:
            chunk[s] = r.get("cluster") or r.get("code") or r.get("id")
common = [s for s in CHANGED if s in chunk]
ari_chunk = adjusted_rand_score([FORM[s] for s in common], [chunk[s] for s in common]) if common else None

# ---- sensitivity ----------------------------------------------------------------------------------
Dmean = np.zeros_like(D)
off = 0
for _, lv in LEVELS:
    w = len(COLS[lv])
    blk = X[:, off:off + w] * math.sqrt(2 * len(LEVELS))
    Dmean += squareform(pdist(blk)) / math.sqrt(2)
    off += w
Dmean /= len(LEVELS)
lab_avg = fcluster(linkage(squareform(Dmean, checks=False), method="average"), k_chosen, criterion="maxclust")
M2, _ = count_matrices(PLACED, drop_single=False)
lab_keep = fcluster(linkage(embed(M2), method="ward"), k_chosen, criterion="maxclust")
sens = {"ari_average_linkage": round(adjusted_rand_score(LAB, lab_avg), 3),
        "average_linkage_sizes": sorted(collections.Counter(lab_avg).values(), reverse=True),
        "ari_single_nodes_kept": round(adjusted_rand_score(LAB, lab_keep), 3)}
jt = clusterwise_jaccard(X, LAB, k_chosen, np.random.default_rng(5))
sens["top_form_jaccard"] = {letter[c]: v for c, v in jt.items()}

print(json.dumps({
    "n_lines": len(LINES), "n_placed": len(PLACED), "unplaced_ids": UNPLACED, "n_changed": len(CHANGED),
    "core": CORE, "cols": {lv: len(COLS[lv]) for _, lv in LEVELS},
    "rooms_without_T3_after_drop": [s for s in CHANGED if MATS["T3"][IDX[s]].sum() == 0],
    "lines_without_node": NO_NODE, "rooms_with_empty_level": ZERO_ROW,
    "top": top, "k_best_silhouette": best, "k_chosen": k_chosen, "pop_dim_entropy": pop_entropy,
    "forms": form_info, "rooms": room_rows, "nodes": nodes, "leaf_of": leaf_of,
    "primary_branch": primary_branch, "secondary_branch": secondary_branch, "branch_place": branch_place,
    "codes_check": {"pseudo_F": round(float(Fr), 3), "r2": round(float(R2r), 4),
                    "perm_p": round((1 + sum(1 for x in Fn if x >= Fr)) / 1000, 4),
                    "null_F_p95": round(float(np.percentile(Fn, 95)), 3),
                    "loo_nearest_acc": round(acc, 3), "loo_null_mean": round(float(np.mean(acc_null)), 3),
                    "loo_null_max": round(float(np.max(acc_null)), 3),
                    "profiles": code_profiles, "kruskal_codes": [round(float(kw.statistic), 2), float(kw.pvalue)],
                    "kruskal_changes": [round(float(kw_changes.statistic), 2), float(kw_changes.pvalue)],
                    "ari_chunk_share": None if ari_chunk is None else round(ari_chunk, 3), "chunk_common": len(common)},
    "sensitivity": sens,
}, ensure_ascii=False, default=str))
