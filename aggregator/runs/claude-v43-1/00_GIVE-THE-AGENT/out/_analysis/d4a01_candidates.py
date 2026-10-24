#!/usr/bin/env python3
"""D4a-01, stage D4 section 2: candidate groups, read from the key matrices only (the all-kinds views, since the
kind of add-condition, add-step and restrict lines is not relied on). A change key is a key whose op is add-step,
add-condition, link, restrict or contradict (instantiate and absent specify; they change nothing in the model).
  A. Change keys held by --min rooms or more at level 3: rooms; how many of those rooms hold the key in the
     specification, elaboration and correction views; the ladder: the same op and target at the node's fourth-order
     theme, dimension and the bare target, with the rooms holding each (does the group grow when walked?).
  B. For each key of A: the keys (any op, level 3) held by --min or more of its rooms, ranked by lift
     (share among its rooms over share in all rooms), the top --co, with 'same node' marked where the node is the
     key's own (a co-occurrence partly built by one theme lifting to several elements).
  C. Change keys at level 4 held by --min rooms or more whose rooms no single level-3 change key of A gathers
     (cousins: they meet only at the fourth order), with the largest child at level 3.
  D. Correction keys, at every level, with their rooms.
Read-only.

    python3 out/_analysis/d4a01_candidates.py [--min 5] [--co 6]
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
V = os.path.join(OUT, "_views")
ap = argparse.ArgumentParser()
ap.add_argument("--min", type=int, default=5)
ap.add_argument("--co", type=int, default=6)
a = ap.parse_args()
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}


def load(level, kind="all"):
    with open(os.path.join(V, "rooms-x-adaptations.%s.%s.tsv" % (level, kind)), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")[1:]
        held = collections.defaultdict(set)
        rooms = []
        for line in f:
            parts = line.rstrip("\n").split("\t")
            rooms.append(parts[0])
            for k, v in zip(head, parts[1:]):
                if v == "1":
                    held[k].add(parts[0])
    return held, rooms


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


t3_t4 = {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in r.get("members") or []:
        t3_t4.setdefault(m, r["id"])
t4_d = {}
for r in jl(os.path.join(OUT, "dimensions.jsonl")):
    for m in r.get("members") or []:
        t4_d.setdefault(m, r["id"])
L3, rooms = load("3")
L4, _ = load("4")
LD, _ = load("dim")
LT, _ = load("target")
K3 = {k: load("3", k)[0] for k in ("specification", "elaboration", "correction")}
N = len(rooms)
A = sorted((k for k, s in L3.items() if k.split(":")[0] in CHANGE and len(s) >= a.min), key=lambda k: -len(L3[k]))
print("== A. change keys held by %d rooms or more at level 3: %d" % (a.min, len(A)))
for k in A:
    op, el, node = k.split(":")
    t4 = t3_t4.get(node)
    d = t4_d.get(t4)
    k4, kd, kt = "%s:%s:%s" % (op, el, t4), "%s:%s:%s" % (op, el, d), "%s:%s:*" % (op, el)
    kinds = {kk[:4]: len(L3[k] & K3[kk].get(k, set())) for kk in K3}
    print("%-34s %3d rooms | spec %d elab %d corr %d | ladder: %s %d; %s %d; %s %d" % (
        k, len(L3[k]), kinds["spec"], kinds["elab"], kinds["corr"], k4, len(L4.get(k4, ())), kd, len(LD.get(kd, ())),
        kt, len(LT.get(kt, ()))))
print("\n== B. co-occurring keys (level 3, held by %d or more of the key's rooms), by lift" % a.min)
for k in A:
    S = L3[k]
    node = k.split(":")[2]
    co = []
    for k2, s2 in L3.items():
        if k2 == k:
            continue
        c = len(S & s2)
        if c >= a.min:
            lift = (c / len(S)) / (len(s2) / N)
            co.append((lift, c, k2))
    co.sort(reverse=True)
    print("%s (%d): %s" % (k, len(S), "; ".join("%s %d/%d lift %.1f%s" % (
        k2, c, len(L3[k2]), lift, " same node" if k2.split(":")[2] == node else "") for lift, c, k2 in co[:a.co])))
print("\n== C. change keys at level 4 held by %d rooms or more, not gathered by one level-3 key of A" % a.min)
A_rooms = {k: L3[k] for k in A}
for k4, s4 in sorted(L4.items(), key=lambda x: -len(x[1])):
    op, el, t4 = k4.split(":")
    if op not in CHANGE or len(s4) < a.min:
        continue
    kids = [(len(L3[k3]), k3) for k3 in L3 if k3.split(":")[0] == op and k3.split(":")[1] == el
            and t3_t4.get(k3.split(":")[2]) == t4]
    kids.sort(reverse=True)
    top = kids[0] if kids else (0, "-")
    if top[0] >= a.min and len(L3[top[1]]) >= 0.8 * len(s4):
        continue
    print("%-30s %3d rooms; level-3 children %d, largest %s %d" % (k4, len(s4), len(kids), top[1], top[0]))
print("\n== D. correction keys")
for level, held in (("3", K3["correction"]),):
    for k, s in sorted(held.items(), key=lambda x: -len(x[1])):
        print("level 3 %s: %s" % (k, ", ".join(sorted(s))))
for level in ("4", "dim", "target"):
    held = load(level, "correction")[0]
    for k, s in sorted(held.items(), key=lambda x: -len(x[1])):
        if len(s) >= 2:
            print("level %s %s: %s" % (level, k, ", ".join(sorted(s))))
