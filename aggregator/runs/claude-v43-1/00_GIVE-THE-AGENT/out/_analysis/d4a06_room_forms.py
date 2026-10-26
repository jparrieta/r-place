#!/usr/bin/env python3
"""D4a-06: the room forms redone (J, 26 October 2026, 19:50 Berlin); the rule is in the diary, logged before
this ran. Reads the shared ledger lines, then (after the cut) branches.jsonl for the named takeover set,
the code store for the check against the codes and the size of the core's rooms, and the D4a-05 forms for
the Rand index between the two cuts. No canvas field, no verdict. Writes nothing; prints one JSON object.

    python3 out/_analysis/d4a06_room_forms.py > out/_analysis/d4a06_forms.json
"""
import collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import adjusted_rand_score

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
LEVELS = ((1, "T3"), (2, "T4"), (3, "dim"))
FLOOR = 5
KS = list(range(4, 9))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


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

# columns from the defining rooms
COLS = {}
for i, lv in LEVELS:
    held = collections.defaultdict(set)
    for s in DEF:
        for r in BY[s]:
            if r["lift"][i]:
                held[r["lift"][i]].add(s)
    COLS[lv] = sorted(k for k, v in held.items() if not (lv == "T3" and len(v) == 1))
CI = {lv: {k: j for j, k in enumerate(COLS[lv])} for _, lv in LEVELS}


def counts(rooms):
    mats = {}
    for i, lv in LEVELS:
        m = np.zeros((len(rooms), len(COLS[lv])))
        for a, s in enumerate(rooms):
            for r in BY[s]:
                k = r["lift"][i]
                if k in CI[lv]:
                    m[a, CI[lv][k]] += 1
        mats[lv] = m
    return mats


def embed(mats):
    out = []
    for _, lv in LEVELS:
        m = mats[lv]
        t = m.sum(axis=1, keepdims=True)
        out.append(np.sqrt(np.divide(m, t, out=np.zeros_like(m), where=t > 0)) / math.sqrt(2 * len(LEVELS)))
    return np.hstack(out)


MD = counts(DEF)
XD = embed(MD)
XT = embed(counts(THIN))
Z = linkage(XD, method="ward")
H = Z[:, 2]

# (a) the gap between merge heights: the k-group cut lives from H[-k] to H[-(k-1)]
gap = {k: {"begins": round(float(H[-k]), 4), "ends": round(float(H[-(k - 1)]), 4),
           "lifetime": round(float(H[-(k - 1)] - H[-k]), 4),
           "relative": round(float((H[-(k - 1)] - H[-k]) / H[-k]), 4)} for k in KS}
k_gap = max(KS, key=lambda k: (gap[k]["lifetime"], -k))


# (b) matched subsamples without replacement
def pair_aris(X, rg, npairs):
    n = len(X)
    m = int(round(0.8 * n))
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
    for _, lv in LEVELS:
        m = MD[lv].copy()
        for j in range(m.shape[1]):
            m[:, j] = nrg.permutation(m[:, j])
        mp[lv] = m
    r = pair_aris(embed(mp), nrg, 20)
    for k in KS:
        null[k].extend(r[k])
stab = {k: {"real_mean": round(float(np.mean(real[k])), 4), "real_sd": round(float(np.std(real[k])), 4),
            "null_mean": round(float(np.mean(null[k])), 4), "null_p95": round(float(np.percentile(null[k], 95)), 4),
            "margin": round(float(np.mean(real[k]) - np.mean(null[k])), 4)} for k in KS}
best_margin = max(stab[k]["margin"] for k in KS)
k_stab = min(k for k in KS if stab[k]["margin"] >= best_margin - 0.005)

# ---- describe a cut ------------------------------------------------------------------------------
names4 = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dims = {r["id"]: r.get("label") for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
third = {r["id"]: r.get("name") for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}


def shares(m):
    t = m.sum(axis=1, keepdims=True)
    return np.divide(m, t, out=np.zeros_like(m), where=t > 0)


SD = {lv: shares(MD[lv]) for _, lv in LEVELS}
POP = {lv: SD[lv].mean(axis=0) for _, lv in LEVELS}
IDX = {s: i for i, s in enumerate(DEF)}
XALL = {s: XD[IDX[s]] for s in DEF}
XALL.update({s: XT[i] for i, s in enumerate(THIN)})


def t4count(s):
    c = collections.Counter(r["lift"][2] for r in BY[s] if r["lift"][2])
    return c, sum(c.values())


def describe(k):
    lab = fcluster(Z, k, criterion="maxclust")
    order = [c for c, _ in collections.Counter(lab).most_common()]
    letter = {c: "ABCDEFGH"[i] for i, c in enumerate(order)}
    ward = {s: letter[lab[IDX[s]]] for s in DEF}
    forms = sorted(set(ward.values()))
    info, sig = {}, {}
    for f in forms:
        mem = [s for s in DEF if ward[s] == f]
        idx = [IDX[s] for s in mem]
        prof = {}
        for _, lv in LEVELS:
            sh = SD[lv][idx].mean(axis=0)
            pres = (MD[lv][idx] > 0).mean(axis=0)
            rows = []
            for j, node in enumerate(COLS[lv]):
                ratio = sh[j] / POP[lv][j] if POP[lv][j] > 0 else 0
                rows.append({"node": node, "share": round(float(sh[j]), 4), "pop_share": round(float(POP[lv][j]), 4),
                             "ratio": round(float(ratio), 2), "presence": round(float(pres[j]), 3)})
            prof[lv] = rows
        s4 = sorted([dict(r, name=names4.get(r["node"])) for r in prof["T4"] if r["ratio"] >= 1.5 and r["presence"] >= 1 / 3],
                    key=lambda r: -r["share"])
        s3 = sorted([dict(r, name=third.get(r["node"])) for r in prof["T3"] if r["ratio"] >= 1.5 and r["presence"] >= 1 / 4],
                    key=lambda r: -r["share"])[:6]
        dd = sorted([dict(r, name=dims.get(r["node"])) for r in prof["dim"]], key=lambda r: -r["share"])[:4]
        sig[f] = {r["node"] for r in s4}
        info[f] = {"ward_n": len(mem), "sig_T4": s4, "sig_T3": s3, "dims": dd}
    cent = {f: XD[[IDX[s] for s in DEF if ward[s] == f]].mean(axis=0) for f in forms}
    rooms = {}
    for s in CH:
        c, tot = t4count(s)
        on = {f: sum(n for node, n in c.items() if node in sig[f]) for f in forms}
        d = {f: float(np.linalg.norm(XALL[s] - cent[f])) for f in forms}
        mix = ward[s] if s in ward else min(forms, key=lambda f: d[f])
        top = max(on.values())
        tied = sorted(f for f in forms if on[f] == top) if top > 0 else []
        if top == 0:
            place, how = mix, "no change on any signature: by the whole mix"
        elif len(tied) == 1:
            place, how = tied[0], "signature"
        else:
            place, how = min(tied, key=lambda f: d[f]), "signature tie: nearest centre among the tied"
        rooms[s] = {"form": place, "how": how, "mix_form": mix, "moved": place != mix, "defining": s in ward,
                    "changes": NCH[s], "on_signature": on, "share_own": round(on[place] / tot, 3) if tot else 0.0,
                    "tied": tied if len(tied) > 1 else [],
                    "secondary": sorted(f for f in forms if f != place and tot and on[f] / tot >= 0.25),
                    "near_equal_centre": sorted(f for f in forms if f != place and d[f] <= 1.05 * d[place])}
    sizes = collections.Counter(r["form"] for r in rooms.values())
    return {"k": k, "ward_sizes": dict(collections.Counter(ward.values())), "sizes": dict(sorted(sizes.items())),
            "ratio": round(max(sizes.values()) / min(sizes.values()), 2), "forms": info, "rooms": rooms,
            "moved": sum(r["moved"] for r in rooms.values()),
            "moved_defining": sum(r["moved"] for r in rooms.values() if r["defining"]),
            "moved_thin": sum(r["moved"] for r in rooms.values() if not r["defining"]),
            "ties": sum(1 for r in rooms.values() if r["tied"]),
            "no_signature": sum(1 for r in rooms.values() if r["how"].startswith("no change"))}


cuts = {k_stab: describe(k_stab)}
if k_gap != k_stab:
    cuts[k_gap] = describe(k_gap)

# ---- named sets, the core, the codes ---------------------------------------------------------------
raid = sorted({r["sub"] for r in PLACED if r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020"}, key=str.lower)
B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
takeover = sorted(B["F02"]["members"], key=str.lower)
ncodes = collections.Counter(r["sub"] for r in jl(os.path.join(STORE, "codes.jsonl")))
core = sorted(({"sub": s, "codes": ncodes[s]} for s in CORE), key=lambda x: -x["codes"])
pop_codes_median = float(np.median([ncodes[s] for s in ALL]))

t4m = {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in r.get("members") or []:
        t4m[m] = r["id"]
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
cc = collections.Counter()
for r in jl(os.path.join(STORE, "codes.jsonl")):
    cc[(r["sub"], r.get("theme_id"))] += 1
comp = collections.defaultdict(collections.Counter)
for (s, t), n in cc.items():
    ns = [t4m[x] for x in place.get((s, t), []) if x in t4m]
    for node in ns:
        comp[s][node] += n / len(ns)
cn = sorted({k for c in comp.values() for k in c})


def codes_check(cut):
    rooms = [s for s in CH]
    M = np.array([[comp[s].get(k, 0.0) for k in cn] for s in rooms])
    M = np.sqrt(M / np.maximum(M.sum(axis=1, keepdims=True), 1e-12)) / math.sqrt(2)
    forms = sorted(cut["sizes"])
    lab = np.array([forms.index(cut["rooms"][s]["form"]) for s in rooms])

    def pf(l):
        g = M.mean(axis=0)
        sst = ((M - g) ** 2).sum()
        ssw = sum(((M[l == c] - M[l == c].mean(axis=0)) ** 2).sum() for c in set(l))
        kk, n = len(set(l)), len(l)
        return ((sst - ssw) / (kk - 1)) / (ssw / (n - kk)), 1 - ssw / sst
    F, r2 = pf(lab)
    rg = np.random.default_rng(3)
    Fn = [pf(rg.permutation(lab))[0] for _ in range(999)]
    med = {f: float(np.median([ncodes[s] for s in rooms if cut["rooms"][s]["form"] == f])) for f in forms}
    medch = {f: float(np.median([NCH[s] for s in rooms if cut["rooms"][s]["form"] == f])) for f in forms}
    return {"pseudo_F": round(float(F), 3), "r2": round(float(r2), 4), "null_F_p95": round(float(np.percentile(Fn, 95)), 3),
            "perm_p": round((1 + sum(1 for x in Fn if x >= F)) / 1000, 4), "median_codes": med, "median_changes": medch}


prev = {}
p5 = os.path.join(OUT, "room-forms-D4a05.jsonl")
for r in jl(p5):
    if r.get("level") == "form":
        for s in r["members"]:
            prev[s] = r["id"]
for k, cut in cuts.items():
    cut["codes_check"] = codes_check(cut)
    common = [s for s in CH if s in prev]
    cut["ari_vs_D4a05"] = round(adjusted_rand_score([prev[s] for s in common], [cut["rooms"][s]["form"] for s in common]), 3)
    cut["raiding_by_form"] = dict(collections.Counter(cut["rooms"][s]["form"] if s in cut["rooms"] else "K" for s in raid))
    cut["takeover_by_form"] = dict(collections.Counter(cut["rooms"][s]["form"] if s in cut["rooms"] else "K" for s in takeover))

print(json.dumps({"floor": FLOOR, "n_defining": len(DEF), "n_thin": len(THIN), "n_core": len(CORE),
                  "cols": {lv: len(COLS[lv]) for _, lv in LEVELS}, "gap": gap, "k_gap": k_gap, "stability": stab,
                  "k_stab": k_stab, "agree": k_gap == k_stab, "cuts": {str(k): v for k, v in cuts.items()},
                  "raiding": raid, "takeover": takeover, "core": core, "pop_codes_median": pop_codes_median},
                 ensure_ascii=False))
