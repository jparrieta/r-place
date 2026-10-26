#!/usr/bin/env python3
"""D4a-08, J's ruling of 22:18 Berlin: the six forms of D4a-08c written down to the single rooms, for the figure.
The construction is d4a08c_room_forms.py's, copied unchanged (changes two thirds, codes one third, floor of 5, Ward
on the 558 defining rooms). Placed rooms (thin and core) keep their six-form and descend below it by the same rule
that placed them. The rule is in the diary, logged before this ran. Prints one JSON object, read by d4a08d_write.py.

    python3 out/_analysis/d4a08d_room_tree.py > out/_analysis/d4a08d_tree.json
"""
import collections, json, math, os, sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, is_valid_linkage, is_monotonic

W = 2 / 3
KMAX = 30
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.argv = [sys.argv[0]]
sys.path.insert(0, AN)
sys.setrecursionlimit(20000)
import d4a07_features as F  # noqa: E402
import adaptation_ledger as al  # noqa: E402

LV = ("T3", "T4", "dim")
FLOOR = 5


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


# ---- the construction of d4a08c_room_forms.py, unchanged ----
ALL = sorted(al.effective_rooms(OUT), key=str.lower)
NCH = collections.Counter(r["sub"] for r in F.PLACED)
CH = sorted(NCH, key=str.lower)
CORE = sorted(set(ALL) - set(CH), key=str.lower)
DEF = [s for s in CH if NCH[s] >= FLOOR]
THIN = [s for s in CH if NCH[s] < FLOOR]
PLACE = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    PLACE[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
CODES = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
NCODES = collections.Counter(r["sub"] for r in CODES)


def change_counts(rooms):
    out = {}
    for s in rooms:
        c = {lv: collections.Counter() for lv in LV}
        for r in F.BY.get(s, []):
            for lv in LV:
                for col, w in F.features(r, lv):
                    c[lv][col] += w
        out[s] = c
    return out


def code_counts(rooms):
    rs = set(rooms)
    out = {s: {lv: collections.Counter() for lv in LV} for s in rooms}
    for r in CODES:
        s = r["sub"]
        if s not in rs:
            continue
        t3 = PLACE.get((s, r.get("theme_id")), [])
        for x in t3:
            w = 1.0 / len(t3)
            out[s]["T3"][x] += w
            t4 = F.T4OF3.get(x)
            if t4:
                out[s]["T4"][t4] += w
                d = F.DOF4.get(t4)
                if d:
                    out[s]["dim"][d] += w
    return out


def columns(cd):
    cols = {}
    for lv in LV:
        held = collections.Counter()
        for c in cd.values():
            for k, v in c[lv].items():
                if v > 0:
                    held[k] += 1
        cols[lv] = sorted(k for k, n in held.items() if n > 1)
    return cols


def mats(counts, rooms, cols):
    out = {}
    for lv in LV:
        ci = {k: j for j, k in enumerate(cols[lv])}
        m = np.zeros((len(rooms), len(cols[lv])))
        for i, s in enumerate(rooms):
            for k, v in counts[s][lv].items():
                if k in ci:
                    m[i, ci[k]] += v
        out[lv] = m
    return out


def shares(m):
    t = m.sum(axis=1, keepdims=True)
    return np.divide(m, t, out=np.zeros_like(m), where=t > 0)


def tv(X):
    return float(((X - X.mean(axis=0)) ** 2).sum(axis=1).mean())


CC, KC = change_counts(CH), code_counts(ALL)
CCOLS, KCOLS = columns({s: CC[s] for s in DEF}), columns({s: KC[s] for s in DEF})
MEAN = {lv: shares(mats(KC, ALL, KCOLS)[lv]).mean(axis=0) for lv in LV}
MCD, MKD = mats(CC, DEF, CCOLS), mats(KC, DEF, KCOLS)
ECD = np.hstack([np.sqrt(shares(MCD[lv])) / math.sqrt(6) for lv in LV])
SC = {"c": tv(ECD), **{lv: tv(shares(MKD[lv]) - MEAN[lv]) for lv in LV}}


def code_part(rooms):
    mk = mats(KC, rooms, KCOLS)
    return np.hstack([(shares(mk[lv]) - MEAN[lv]) / math.sqrt(3 * SC[lv]) for lv in LV]) * math.sqrt(1 - W)


def change_part(rooms):
    mc = mats(CC, rooms, CCOLS)
    return np.hstack([np.sqrt(shares(mc[lv])) / math.sqrt(6) for lv in LV]) / math.sqrt(SC["c"]) * math.sqrt(W)


XD = np.hstack([change_part(DEF), code_part(DEF)])
XT = np.hstack([change_part(THIN), code_part(THIN)])
KCORE = code_part(CORE)
nch = ECD.shape[1]
Z = linkage(XD, method="ward")
# ---- end of the copied construction ----

n = len(DEF)
H = Z[:, 2]
KIDS = {n + i: (int(Z[i, 0]), int(Z[i, 1])) for i in range(n - 1)}
SIZE = {i: 1 for i in range(n)}
CENT = {i: XD[i] for i in range(n)}
PARENT = {}
for nid in range(n, 2 * n - 1):
    a, b = KIDS[nid]
    SIZE[nid] = SIZE[a] + SIZE[b]
    CENT[nid] = (SIZE[a] * CENT[a] + SIZE[b] * CENT[b]) / SIZE[nid]
    PARENT[a] = PARENT[b] = nid
ROOTN = 2 * n - 2


def height(nid):
    return 0.0 if nid < n else float(H[nid - n])


def leaves(nid):
    out, st = [], [nid]
    while st:
        x = st.pop()
        if x < n:
            out.append(x)
        else:
            st.extend(KIDS[x])
    return out


# the cuts, top-down: going from k groups to k + 1 undoes the merge that made node 2n - 1 - k
K_FROM, K_TO = {ROOTN: 1}, {}
groups = {ROOTN}
for k in range(1, n):
    u = 2 * n - 1 - k
    assert u in groups
    groups.remove(u)
    K_TO[u] = k
    for c in KIDS[u]:
        K_FROM[c] = k + 1
        groups.add(c)
for i in range(n):
    K_TO[i] = n

# the six forms of D4a-08c, matched to the six groups of the cut by their defining members
D8C = {r["id"]: r for r in jl(os.path.join(OUT, "room-forms-D4a08c.jsonl"))}
FORM_OF = {s: f for f, r in D8C.items() for s in r["members"]}
six = [u for u in K_FROM if K_FROM[u] <= 6 <= K_TO[u]]
assert len(six) == 6
FORMNODE = {}
for u in six:
    fs = {FORM_OF[DEF[i]] for i in leaves(u)}
    assert len(fs) == 1, fs
    FORMNODE[fs.pop()] = u
NODEFORM = {u: f for f, u in FORMNODE.items()}

# labels: above six the merged letters, at six the letter, below a split child takes .1 (larger) or .2
LABEL = {}


def letters(u):
    return sorted({NODEFORM[x] for x in six if set(leaves(x)) <= set(leaves(u))})


for u in sorted(K_FROM, key=lambda x: (K_FROM[x], -x)):
    if K_FROM[u] <= 6:
        if K_TO[u] >= 6 or u in NODEFORM:
            LABEL[u] = "+".join(letters(u))
for k in range(6, n):
    u = 2 * n - 1 - k
    a, b = KIDS[u]
    big, small = (a, b) if (SIZE[a], -a) >= (SIZE[b], -b) else (b, a)
    if K_FROM[u] <= 6 and u not in NODEFORM:
        continue  # a node above the forms: its children are labelled by letters
    LABEL[big], LABEL[small] = LABEL[u] + ".1", LABEL[u] + ".2"
for u in K_FROM:
    if u not in LABEL:
        LABEL[u] = "+".join(letters(u))

# placed rooms: the six-form as placed in D4a-08c, then the nearer child at each split, down to one defining room
IDX = {s: i for i, s in enumerate(DEF)}
VEC = {s: ("whole mix", XT[i]) for i, s in enumerate(THIN)}
VEC.update({s: ("codes", KCORE[i]) for i, s in enumerate(CORE)})


def dist(s, nid):
    how, v = VEC[s]
    c = CENT[nid]
    return float(np.linalg.norm(v - (c if how == "whole mix" else c[nch:])))


# check: the six-form placement recomputed equals D4a-08c's
recheck = {s: min(FORMNODE, key=lambda f: dist(s, FORMNODE[f])) for s in VEC}
mismatch_six = sorted(s for s in VEC if recheck[s] != FORM_OF[s])
assert not mismatch_six, mismatch_six
for s in DEF:
    assert FORM_OF[s] == NODEFORM[[u for u in six if IDX[s] in set(leaves(u))][0]]

DESC, REACH, NEAR_EQ = {}, {}, collections.Counter()
for s in sorted(VEC, key=str.lower):
    u = FORMNODE[FORM_OF[s]]
    path = []
    while u >= n:
        a, b = KIDS[u]
        da, db = dist(s, a), dist(s, b)
        if abs(da - db) <= 0.05 * min(da, db):
            NEAR_EQ[s] += 1
        u = a if da <= db else b
        path.append(u)
    DESC[s] = path
    REACH[s] = u


def path_of(s):
    if s in IDX:
        p, u = [], IDX[s]
        while u in PARENT:
            p.append(u)
            u = PARENT[u]
        p.append(ROOTN)
        return list(reversed(p))
    u, up = FORMNODE[FORM_OF[s]], []
    while u in PARENT:
        up.append(u)
        u = PARENT[u]
    up.append(ROOTN)
    return list(reversed(up)) + DESC[s]


def label_at(path, k):
    for u in path:
        if K_FROM[u] <= k <= K_TO[u]:
            return LABEL[u]
    return None


# check: the top-down cuts equal scipy's fcluster at k = 1 to KMAX
fc_bad = []
for k in range(2, KMAX + 1):
    lab = fcluster(Z, k, criterion="maxclust")
    mine = {}
    for i in range(n):
        mine.setdefault(label_at(path_of(DEF[i]), k), set()).add(i)
    theirs = {}
    for i in range(n):
        theirs.setdefault(lab[i], set()).add(i)
    if sorted(map(sorted, mine.values())) != sorted(map(sorted, theirs.values())):
        fc_bad.append(k)

# the drawable tree over all 705 rooms
ATT = collections.defaultdict(list)
for s, r in REACH.items():
    ATT[r].append(s)
created, top, attach = [], {}, {}
for i in range(n):
    prev, hprev = ("room", DEF[i]), 0.0
    cap = height(PARENT[i])
    for s in sorted(ATT.get(i, []), key=lambda x: (dist(x, i), x.lower())):
        d = dist(s, i)
        h = max(hprev, min(d, cap))
        created.append((prev, ("room", s), h, "placed", ("att", s)))
        attach[s] = {"room": DEF[i], "distance": round(d, 6), "height": round(h, 6), "capped": d > cap}
        prev, hprev = ("att", s), h
    top[i] = prev
for i in range(n - 1):
    a, b = (top[x] if x < n else ("ward", x) for x in KIDS[n + i])
    created.append((a, b, float(H[i]), "ward", ("ward", n + i)))
order = sorted(range(len(created)), key=lambda j: (created[j][2], j))
FID = {("room", s): j for j, s in enumerate(ALL)}
NR = {("room", s): 1 for s in ALL}
rows = []
for pos, j in enumerate(order):
    a, b, h, kind, key = created[j]
    FID[key] = len(ALL) + pos
    NR[key] = NR[a] + NR[b]
    nid = key[1] if key[0] == "ward" else None
    rows.append({"merge": pos + 1, "node": FID[key], "a": FID[a], "b": FID[b], "height": round(h, 6), "rooms": NR[key],
                 "kind": kind, "label": LABEL[nid] if nid is not None else "", "ward_node": nid if nid is not None else "",
                 "k_from": K_FROM[nid] if nid is not None else "", "k_to": K_TO[nid] if nid is not None else "",
                 "placed_room": key[1] if key[0] == "att" else ""})
Zf = np.array([[r["a"], r["b"], r["height"], r["rooms"]] for r in rows], dtype=float)
valid, mono = bool(is_valid_linkage(Zf)), bool(is_monotonic(Zf))

# Newick from the drawable tree
KIDF = {r["node"]: (r["a"], r["b"]) for r in rows}
HF = {r["node"]: r["height"] for r in rows}
LBF = {r["node"]: r["label"] for r in rows}
NAME = {j: s for j, s in enumerate(ALL)}


def nwk(u, hpar):
    if u in NAME:
        return "%s:%.6f" % (NAME[u], hpar)
    a, b = KIDF[u]
    return "(%s,%s)%s:%.6f" % (nwk(a, HF[u]), nwk(b, HF[u]), LBF[u], hpar - HF[u])


rootf = rows[-1]["node"]
a, b = KIDF[rootf]
newick = "(%s,%s)%s;" % (nwk(a, HF[rootf]), nwk(b, HF[rootf]), LBF[rootf])

# the room table
D8T = {}
for line in open(os.path.join(OUT, "room-forms-D4a08c.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    D8T[c[0]] = {"k4": c[3], "k8": c[4]}
KS = list(range(1, KMAX + 1))
table = []
for s in ALL:
    p = path_of(s)
    role = "defining" if s in IDX else "thin" if s in THIN else "core"
    leaf = p[-1]
    row = {"room": s, "leaf_id": FID[("room", s)], "role": role, "selected_changes": NCH.get(s, 0), "coded_concepts": NCODES.get(s, 0),
           "form": FORM_OF[s], "form_name": D8C[FORM_OF[s]]["name"]}
    for k in KS:
        row["k%d" % k] = label_at(p, k)
    row["address"] = LABEL[leaf] + ("" if s in IDX else "/" + s)
    row["placed_by"] = "" if s in IDX else VEC[s][0]
    row["reached_room"] = "" if s in IDX else DEF[leaf]
    row["distance_to_reached"] = "" if s in IDX else attach[s]["distance"]
    row["drawn_height"] = "" if s in IDX else attach[s]["height"]
    row["height_capped"] = "" if s in IDX else ("yes" if attach[s]["capped"] else "no")
    row["near_equal_splits"] = "" if s in IDX else NEAR_EQ.get(s, 0)
    table.append(row)

# check: nested labels at four and eight against the D4a-08c tsv (placed rooms there were placed at each count apart)
diff = {}
for k in (4, 8):
    tomine = {}
    for r in table:
        if r["role"] == "defining":
            tomine.setdefault(D8T[r["room"]]["k%d" % k], set()).add(r["k%d" % k])
    assert all(len(v) == 1 for v in tomine.values()), tomine
    tm = {x: v.pop() for x, v in tomine.items()}
    moved = [r["room"] for r in table if r["role"] != "defining" and tm[D8T[r["room"]]["k%d" % k]] != r["k%d" % k]]
    diff[k] = {"placed_rooms_differing": len(moved), "rooms": moved,
               "thin": sum(1 for s in moved if s in THIN), "core": sum(1 for s in moved if s in CORE)}

sizes = {k: dict(collections.Counter(r["k%d" % k] for r in table)) for k in KS}
facts = {
    "n_rooms": len(ALL), "n_defining": n, "n_thin": len(THIN), "n_core": len(CORE), "lines_placed": sum(NCH.values()),
    "change_columns": {lv: len(CCOLS[lv]) for lv in LV},
    "change_link_columns": {lv: sum(1 for c in CCOLS[lv] if ">" in c) for lv in LV},
    "code_columns": {lv: len(KCOLS[lv]) for lv in LV}, "dims": int(XD.shape[1]), "change_dims": nch,
    "scales": {k: round(v, 6) for k, v in SC.items()},
    "codes_total": len(CODES), "rooms_with_codes": len(NCODES),
    "codes_unplaced": sum(1 for r in CODES if not PLACE.get((r["sub"], r.get("theme_id")))),
    "heights_top": [round(float(x), 4) for x in H[-8:]],
    "gap6": round(float(H[-5] - H[-6]), 4),
}
out = {"w_changes": round(W, 4), "facts": facts,
       "checks": {"six_forms_match_D4a08c": True, "placed_six_recheck_mismatch": mismatch_six, "fcluster_mismatch_k": fc_bad,
                  "full_linkage_valid": valid, "full_linkage_monotone": mono, "merges": len(rows),
                  "capped": sum(1 for v in attach.values() if v["capped"]), "placed": len(attach),
                  "near_equal_rooms": sum(1 for s in VEC if NEAR_EQ.get(s)), "nested_vs_D4a08c": diff},
       "sizes": {str(k): v for k, v in sizes.items()},
       "form_nodes": {f: {"ward_node": u, "height": height(u), "defining": SIZE[u]} for f, u in sorted(FORMNODE.items())},
       "rows": rows, "table": table, "newick": newick}
print(json.dumps(out, ensure_ascii=False))
