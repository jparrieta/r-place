#!/usr/bin/env python3
"""D4a-06: facts for the report, read-only. (1) How the Ward cut at k = 5 nests in the cut at k = 8 (defining
rooms). (2) The takeover rooms' share of selected changes on the April Fools frame (T4-001), and the raiding
rooms' share on attack calls (T3-006 or T4-020). (3) The core's rooms: their accepted ledger lines by op.

    python3 out/_analysis/d4a06_facts2.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

T = json.load(open(os.path.join(OUT, "_analysis", "d4a06_forms.json"), encoding="utf-8"))
c5, c8 = T["cuts"]["5"]["rooms"], T["cuts"]["8"]["rooms"]
x = collections.Counter((c5[s]["mix_form"], c8[s]["mix_form"]) for s in c8 if c8[s]["defining"])
print("k5 ward group <- k8 ward forms:", {a: sorted((b, n) for (aa, b), n in x.items() if aa == a) for a in sorted({a for a, _ in x})})
SH = al.shared_lines(OUT)
CH = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in SH if r.get("op") in CH and len(r.get("lift") or []) >= 4]
by = collections.defaultdict(list)
for r in L:
    by[r["sub"]].append(r)


def share(s, pred):
    ls = by.get(s, [])
    return sum(1 for r in ls if pred(r)) / len(ls) if ls else 0.0


tk = [share(s, lambda r: r["lift"][2] == "T4-001") for s in T["takeover"]]
rd = [share(s, lambda r: r["lift"][1] == "T3-006" or r["lift"][2] == "T4-020") for s in T["raiding"]]
print("takeover rooms %d: share of changes on T4-001 median %.3f, max %.3f; rooms with any %d" % (
    len(tk), statistics.median(tk), max(tk), sum(1 for v in tk if v > 0)))
print("raiding rooms %d: share of changes on attack calls median %.3f; rooms with share >= 0.25: %d" % (
    len(rd), statistics.median(rd), sum(1 for v in rd if v >= 0.25)))
hi = [s for s, v in zip(T["raiding"], rd) if v >= 0.25]
print("  of those, by form at k=8:", dict(collections.Counter(c8[s]["form"] for s in hi)))
ops = collections.defaultdict(collections.Counter)
for r in SH:
    if r["sub"] in {c["sub"] for c in T["core"]}:
        ops[r["sub"]][r.get("op")] += 1
for c in T["core"][:6]:
    print("core", c["sub"], c["codes"], "codes;", dict(ops[c["sub"]]))
