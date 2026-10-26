#!/usr/bin/env python3
"""D4a-07: room forms with the arrow at every level (J, 26 October 2026, 20:35 to 20:37 Berlin); the rule is in
the diary, logged before this ran. Reads the shared ledger lines, model/arrows.jsonl, model/elements.jsonl,
fourth/fourth.jsonl and dimensions.jsonl for the ladder; after the cut, branches.jsonl for the takeover set,
the code store for the check against the codes, and the D4a-06 forms for the Rand index. No canvas, no verdict.
Prints one JSON object.

    python3 out/_analysis/d4a07_room_forms.py > out/_analysis/d4a07_forms.json
"""
import collections, itertools, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import adjusted_rand_score, silhouette_samples

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
LV = (("T3", 1), ("T4", 2), ("dim", 3))
FLOOR = 5
KS = list(range(4, 9))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ARROWS = {r["id"]: r for r in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
ELEM = {r["id"]: r for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}
T4OF3 = {}
for f in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in f.get("members") or []:
        T4OF3[m] = f["id"]
DOF4 = {}
for d in jl(os.path.join(OUT, "dimensions.jsonl")):
    for m in d.get("members") or []:
        DOF4.setdefault(m, d["id"])

ALL = sorted(al.effective_rooms(OUT), key=str.lower)
PLACED = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE and len(r.get("lift") or []) >= 4]
NCH = collections.Counter(r["sub"] for r in PLACED)
CH = sorted(NCH, key=str.lower)
CORE = sorted(set(ALL) - set(CH), key=str.lower)
DEF = [s for s in CH if NCH[s] >= FLOOR]
THIN = [s for s in CH if NCH[s] < FLOOR]
BY = collections.defaultdict(list)
for r in PLACED:
    BY[r["sub"]].append(r)


def t4s(eid):
    out = []
    for a in ELEM.get(eid, {}).get("tier") or []:
        n = a if a.startswith("T4-") else T4OF3.get(a) if a.startswith("T3-") else None
        if n and n not in out:
            out.append(n)
    return out


def end_nodes(eid, lv, ev_t3):
    if lv == "T4":
        return t4s(eid) or [eid]
    if lv == "dim":
        ds = []
        for n in t4s(eid):
            d = DOF4.get(n)
            if d and d not in ds:
                ds.append(d)
        return ds or [eid]
    t3 = [a for a in ELEM.get(eid, {}).get("tier") or [] if a.startswith("T3-")]
    if t3:
        return t3
    if ev_t3 and T4OF3.get(ev_t3) in t4s(eid):
        return [ev_t3]
    return t4s(eid) or [eid]


def features(line, lv, with_links=True, link_ops=True):
    """(column, weight) pairs for one selected line at one level."""
    i = dict(LV)[lv]
    node = line["lift"][i]
    is_arrow = line["element"] in ARROWS
    is_linkop = line["op"] == "link" and not is_arrow and link_ops
    out = []
    if with_links and (is_arrow or is_linkop):
        if is_arrow:
            a = ARROWS[line["element"]]
            src = end_nodes(a["from"], lv, line["lift"][1])
            tgt = end_nodes(a["to"], lv, line["lift"][1])
        else:
            first = node or line["lift"][1]
            src = [first] if first else []
            tgt = end_nodes(line["element"], lv, None)
        pairs = list(itertools.product(src, tgt))
        if pairs:
            for s, t in pairs:
                out.append(("%s>%s" % (s, t), 0.5 / len(pairs)))
            if node:
                out.append((node, 0.5))
            return out
    if node:
        out.append((node, 1.0))
    return out


def build(rooms_def, others, **kw):
    cols = {}
    for lv, _ in LV:
        held = collections.defaultdict(set)
        for s in rooms_def:
            for r in BY[s]:
                for c, w in features(r, lv, **kw):
                    held[c].add(s)
        cols[lv] = sorted(c for c, ss in held.items() if len(ss) > 1)

    def mats(rooms):
        out = {}
        for lv, _ in LV:
            ci = {c: j for j, c in enumerate(cols[lv])}
            m = np.zeros((len(rooms), len(cols[lv])))
            for a, s in enumerate(rooms):
                for r in BY[s]:
                    for c, w in features(r, lv, **kw):
                        if c in ci:
                            m[a, ci[c]] += w
            out[lv] = m
        return out
    return cols, mats(rooms_def), mats(others)


def embed(M):
    blocks = []
    for lv, _ in LV:
        m = M[lv]
        t = m.sum(axis=1, keepdims=True)
        blocks.append(np.sqrt(np.divide(m, t, out=np.zeros_like(m), where=t > 0)) / math.sqrt(2 * len(LV)))
    return np.hstack(blocks)


COLS, MD, MT = build(DEF, THIN)
XD, XT = embed(MD), embed(MT)
Z = linkage(XD, method="ward")
H = Z[:, 2]
gap = {k: {"begins": round(float(H[-k]), 4), "ends": round(float(H[-(k - 1)]), 4),
           "lifetime": round(float(H[-(k - 1)] - H[-k]), 4)} for k in KS}
k_gap = max(KS, key=lambda k: (gap[k]["lifetime"], -k))


def pair_aris(X, rg, npairs):
    n, m = len(X), int(round(0.8 * len(X)))
    res = {k: [] for k in KS}
    for _ in range(npairs):
        a = np.sort(rg.choice(n, m, replace=False))
        b = np.sort(rg.choice(n, m, replace=False))
        Za, Zb = linkage(X[a], method="ward"), linkage(X[b], method="ward")
        common = np.intersect1d(a, b)
        pa = {int(x): i for i, x in enumerate(a)}
        pb = {int(x): i for i, x in enumerate(b)}
        for k in KS:
            la, lb = fcluster(Za, k, criterion="maxclust"), fcluster(Zb, k, criterion="maxclust")
            res[k].append(adjusted_rand_score([la[pa[int(c)]] for c in common], [lb[pb[int(c)]] for c in common]))
    return res


real = pair_aris(XD, np.random.default_rng(0), 100)
nrg = np.random.default_rng(1)
null = {k: [] for k in KS}
for _ in range(20):
    mp = {}
    for lv, _ in LV:
        m = MD[lv].copy()
        for j in range(m.shape[1]):
            m[:, j] = nrg.permutation(m[:, j])
        mp[lv] = m
    r = pair_aris(embed(mp), nrg, 20)
    for k in KS:
        null[k].extend(r[k])
stab = {k: {"real_mean": round(float(np.mean(real[k])), 4), "null_mean": round(float(np.mean(null[k])), 4),
            "null_p95": round(float(np.percentile(null[k], 95)), 4),
            "margin": round(float(np.mean(real[k]) - np.mean(null[k])), 4)} for k in KS}
bm = max(stab[k]["margin"] for k in KS)
k_stab = min(k for k in KS if stab[k]["margin"] >= bm - 0.005)

names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dimn = {r["id"]: r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}


def label(c):
    def one(n):
        return names4.get(n) or third.get(n) or dimn.get(n) or n
    return " > ".join(one(x) for x in c.split(">")) if ">" in c else one(c)


def shares(m):
    t = m.sum(axis=1, keepdims=True)
    return np.divide(m, t, out=np.zeros_like(m), where=t > 0)


SD = {lv: shares(MD[lv]) for lv, _ in LV}
POP = {lv: SD[lv].mean(axis=0) for lv, _ in LV}
IDX = {s: i for i, s in enumerate(DEF)}
XALL = {s: XD[IDX[s]] for s in DEF}
XALL.update({s: XT[i] for i, s in enumerate(THIN)})
T4W = {}
for s in CH:
    w = collections.Counter()
    for r in BY[s]:
        for c, x in features(r, "T4"):
            w[c] += x
    T4W[s] = w
OPS = {s: collections.Counter(r["op"] for r in BY[s]) for s in CH}
ARR = {s: sum(1 for r in BY[s] if r["element"] in ARROWS) for s in CH}


def describe(k):
    lab = fcluster(Z, k, criterion="maxclust")
    order = [c for c, _ in collections.Counter(lab).most_common()]
    letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
    ward = {s: letter[lab[IDX[s]]] for s in DEF}
    forms = sorted(set(ward.values()))
    cent = {f: XD[[IDX[s] for s in DEF if ward[s] == f]].mean(axis=0) for f in forms}
    info, sig = {}, {}
    for f in forms:
        idx = [IDX[s] for s in DEF if ward[s] == f]
        prof = {}
        for lv, _ in LV:
            sh, pres = SD[lv][idx].mean(axis=0), (MD[lv][idx] > 0).mean(axis=0)
            prof[lv] = [{"col": c, "name": label(c), "link": ">" in c, "share": round(float(sh[j]), 4),
                         "pop_share": round(float(POP[lv][j]), 4),
                         "ratio": round(float(sh[j] / POP[lv][j]), 2) if POP[lv][j] > 0 else 0.0,
                         "presence": round(float(pres[j]), 3)} for j, c in enumerate(COLS[lv])]
        s4 = sorted([r for r in prof["T4"] if r["ratio"] >= 1.5 and r["presence"] >= 1 / 3], key=lambda r: -r["share"])
        s3 = sorted([r for r in prof["T3"] if r["ratio"] >= 1.5 and r["presence"] >= 1 / 4], key=lambda r: -r["share"])[:6]
        dd = sorted([r for r in prof["dim"] if not r["link"]], key=lambda r: -r["share"])[:4]
        dl = sorted([r for r in prof["dim"] if r["link"] and r["ratio"] >= 1.5 and r["presence"] >= 1 / 3], key=lambda r: -r["share"])[:3]
        sig[f] = {r["col"] for r in s4}
        info[f] = {"ward_n": len(idx), "sig_T4": s4, "sig_T3": s3, "dims": dd, "dim_links": dl,
                   "mixture": bool(s4) and all(r["presence"] < 0.5 for r in s4), "no_signature": not s4}
    rooms = {}
    for s in CH:
        d = {f: float(np.linalg.norm(XALL[s] - cent[f])) for f in forms}
        mix = ward[s] if s in ward else min(forms, key=lambda f: d[f])
        tot = sum(T4W[s].values())
        on = {f: sum(w for c, w in T4W[s].items() if c in sig[f]) for f in forms}
        top = max(on.values())
        tied = sorted(f for f in forms if abs(on[f] - top) < 1e-9) if top > 0 else []
        lit = (mix if top == 0 else tied[0] if len(tied) == 1 else min(tied, key=lambda f: d[f]))
        rooms[s] = {"form": mix, "literal_form": lit, "moved_by_literal": lit != mix, "defining": s in ward,
                    "changes": NCH[s], "share_own": round(on[mix] / tot, 3) if tot else 0.0,
                    "literal_tied": tied if len(tied) > 1 else [],
                    "secondary": sorted(f for f in forms if f != mix and tot and on[f] / tot >= 0.25),
                    "near_equal_centre": sorted(f for f in forms if f != mix and d[f] <= 1.05 * d[mix])}
    sizes = collections.Counter(r["form"] for r in rooms.values())
    lsizes = collections.Counter(r["literal_form"] for r in rooms.values())
    opmix = {}
    for f in forms:
        c = collections.Counter()
        a = n = 0
        for s, r in rooms.items():
            if r["form"] == f:
                c.update(OPS[s])
                a += ARR[s]
                n += NCH[s]
        opmix[f] = {"restrict": round(c["restrict"] / n, 3), "add-step": round(c["add-step"] / n, 3),
                    "add-condition": round(c["add-condition"] / n, 3), "link": round(c["link"] / n, 3),
                    "on_arrows": round(a / n, 3)}
    # what Ward's own split does to a mixture form
    splits = {}
    for f in forms:
        if info[f]["mixture"] or info[f]["no_signature"]:
            mem = [s for s in DEF if ward[s] == f]
            l2 = fcluster(linkage(XD[[IDX[s] for s in mem]], method="ward"), 2, criterion="maxclust")
            halves = []
            for c in (1, 2):
                idx = [IDX[s] for s, l in zip(mem, l2) if l == c]
                sh, pres = SD["T4"][idx].mean(axis=0), (MD["T4"][idx] > 0).mean(axis=0)
                top3 = sorted(range(len(COLS["T4"])), key=lambda j: -(sh[j] / POP["T4"][j] if POP["T4"][j] > 0 else 0) * (pres[j] >= 1 / 3))[:3]
                halves.append({"n": len(idx), "leading": [{"col": COLS["T4"][j], "name": label(COLS["T4"][j]),
                                                           "ratio": round(float(sh[j] / POP["T4"][j]), 2), "presence": round(float(pres[j]), 3)}
                                                          for j in top3]})
            splits[f] = halves
    return {"k": k, "ward_sizes": dict(sorted(collections.Counter(ward.values()).items())),
            "sizes": dict(sorted(sizes.items())), "ratio": round(max(sizes.values()) / min(sizes.values()), 2),
            "literal_sizes": dict(sorted(lsizes.items())),
            "literal_ratio": round(max(lsizes.values()) / min(lsizes.values()), 2),
            "moved_by_literal": sum(r["moved_by_literal"] for r in rooms.values()),
            "literal_ties": sum(1 for r in rooms.values() if r["literal_tied"]),
            "forms": info, "rooms": rooms, "op_mix": opmix, "mixture_splits": splits, "ward_labels": ward}


cuts = {k_stab: describe(k_stab)}
if k_gap != k_stab:
    cuts[k_gap] = describe(k_gap)

# raiding core
attack = {s: sum(1 for r in BY[s] if r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020") / NCH[s] for s in CH}
core_r = sorted((s for s in DEF if attack[s] >= 0.25), key=str.lower)
from scipy.spatial.distance import pdist, squareform  # noqa: E402
Dm = squareform(pdist(XD))


def group_sil(members):
    lab = np.array([1 if s in members else 0 for s in DEF])
    return float(silhouette_samples(Dm, lab, metric="precomputed")[lab == 1].mean())


real_sil = group_sil(set(core_r))
rg6 = np.random.default_rng(6)
null_sil = [group_sil(set(rg6.choice(DEF, len(core_r), replace=False))) for _ in range(999)]
raid = {"core": core_r, "n": len(core_r), "silhouette": round(real_sil, 4),
        "null_mean": round(float(np.mean(null_sil)), 4), "null_p95": round(float(np.percentile(null_sil, 95)), 4),
        "p": round((1 + sum(1 for x in null_sil if x >= real_sil)) / 1000, 4),
        "by_form": {str(k): dict(collections.Counter(c["rooms"][s]["form"] for s in core_r)) for k, c in cuts.items()},
        "any_attack": len([s for s in CH if attack[s] > 0])}

# sensitivities at the carried k
def ward_k(Xs, k):
    return fcluster(linkage(Xs, method="ward"), k, criterion="maxclust")


k0 = k_stab
base = fcluster(Z, k0, criterion="maxclust")
sens = {}
_, MDa, _ = build(DEF, THIN, link_ops=False)
la = ward_k(embed(MDa), k0)
sens["arrows_only_ari"] = round(adjusted_rand_score(base, la), 3)
_, MDn, _ = build(DEF, THIN, with_links=False)
ln = ward_k(embed(MDn), k0)
sens["no_links_ari"] = round(adjusted_rand_score(base, ln), 3)
saved = dict(BY)
for s in list(BY):
    BY[s] = [r for r in saved[s] if r["op"] != "restrict"]
_, MDr, _ = build(DEF, THIN)
lr = ward_k(embed(MDr), k0)
for s in saved:
    BY[s] = saved[s]
sens["no_restrict_ari"] = round(adjusted_rand_score(base, lr), 3)
sens["no_restrict_sizes"] = sorted(collections.Counter(lr).values(), reverse=True)
sens["no_restrict_rooms_without_changes"] = sum(1 for s in DEF if all(r["op"] == "restrict" for r in saved[s]))

# codes and the D4a-06 forms
t4m = {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in r.get("members") or []:
        t4m[m] = r["id"]
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
cc = collections.Counter()
ncodes = collections.Counter()
for r in jl(os.path.join(STORE, "codes.jsonl")):
    cc[(r["sub"], r.get("theme_id"))] += 1
    ncodes[r["sub"]] += 1
comp = collections.defaultdict(collections.Counter)
for (s, t), n in cc.items():
    ns = [t4m[x] for x in place.get((s, t), []) if x in t4m]
    for node in ns:
        comp[s][node] += n / len(ns)
cn = sorted({k for c in comp.values() for k in c})
prev = {}
for r in jl(os.path.join(OUT, "room-forms-D4a06.jsonl")):
    if r.get("level") == "form":
        for s in r["members"]:
            prev[s] = r["id"]
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
takeover = sorted(B["F02"]["members"], key=str.lower)
for k, cut in cuts.items():
    M = np.array([[comp[s].get(x, 0.0) for x in cn] for s in CH])
    M = np.sqrt(M / np.maximum(M.sum(axis=1, keepdims=True), 1e-12)) / math.sqrt(2)
    forms = sorted(cut["sizes"])
    lab = np.array([forms.index(cut["rooms"][s]["form"]) for s in CH])

    def pf(l):
        g = M.mean(axis=0)
        sst = ((M - g) ** 2).sum()
        ssw = sum(((M[l == c] - M[l == c].mean(axis=0)) ** 2).sum() for c in set(l))
        kk, n = len(set(l)), len(l)
        return ((sst - ssw) / (kk - 1)) / (ssw / (n - kk)), 1 - ssw / sst
    F, r2 = pf(lab)
    rg = np.random.default_rng(3)
    Fn = [pf(rg.permutation(lab))[0] for _ in range(999)]
    cut["codes_check"] = {"pseudo_F": round(float(F), 3), "r2": round(float(r2), 4), "null_F_p95": round(float(np.percentile(Fn, 95)), 3),
                          "perm_p": round((1 + sum(1 for x in Fn if x >= F)) / 1000, 4),
                          "median_codes": {f: float(np.median([ncodes[s] for s in CH if cut["rooms"][s]["form"] == f])) for f in forms},
                          "median_changes": {f: float(np.median([NCH[s] for s in CH if cut["rooms"][s]["form"] == f])) for f in forms}}
    common = [s for s in CH if s in prev]
    cut["ari_vs_D4a06"] = round(adjusted_rand_score([prev[s] for s in common], [cut["rooms"][s]["form"] for s in common]), 3)
    cut["takeover_by_form"] = dict(collections.Counter(cut["rooms"][s]["form"] if s in cut["rooms"] else "K" for s in takeover))

print(json.dumps({"floor": FLOOR, "n_defining": len(DEF), "n_thin": len(THIN), "n_core": len(CORE), "core": CORE,
                  "cols": {lv: {"all": len(COLS[lv]), "links": sum(1 for c in COLS[lv] if ">" in c)} for lv, _ in LV},
                  "gap": gap, "k_gap": k_gap, "stability": stab, "k_stab": k_stab, "agree": k_gap == k_stab,
                  "cuts": {str(k): v for k, v in cuts.items()}, "raiding_core": raid, "sensitivity": sens,
                  "takeover": takeover}, ensure_ascii=False))
