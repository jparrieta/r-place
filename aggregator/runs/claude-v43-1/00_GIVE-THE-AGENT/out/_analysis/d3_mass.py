#!/usr/bin/env python3
"""D3: where the mass is. Reads out/_views/rooms-x-elements.tsv (the view D3 reads first) for rooms by element and op,
and the ledger by count only (never a line) for the absent lines split by observation (J, 2026-10-16 12:59: every
count of absent lines is split by observation), the lines per element, and each element's fourth-order themes from
model/elements.jsonl (arrows grouped by their ends' themes). Prints the element groups proposed for the legs.

    python3 out/_analysis/d3_mass.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(OUT, "_views", "rooms-x-elements.tsv"), encoding="utf-8")
        if l.strip() and not l.startswith("#")]
cols, rows = rows[0], rows[1:]
view = collections.defaultdict(collections.Counter)
for r in rows:
    for c, cell in zip(cols[1:], r[1:]):
        for op in filter(None, (x.strip() for x in cell.split(","))):
            view[c][op] += 1
E = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8")}
A = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")}
lines = collections.Counter()
nonabs = collections.Counter()
obs = collections.defaultdict(collections.Counter)
for l in open(os.path.join(OUT, "adaptations.jsonl"), encoding="utf-8"):
    d = json.loads(l)
    e = d["element"] or "(propose)"
    lines[e] += 1
    if d["op"] == "absent":
        obs[e][d.get("observation")] += 1
    else:
        nonabs[e] += 1
print("view: %d rooms, %d columns" % (len(rows), len(cols) - 1))
print("%-10s %-10s %6s %6s %6s %6s  %s" % ("id", "status", "lines", "nonabs", "evid", "limits", "rooms by op in the view"))


def status(i):
    return (E.get(i) or A.get(i) or {}).get("status", "dimension" if i.startswith("D") else "-")


for e in sorted(lines, key=lambda x: -nonabs[x]):
    ev = obs[e]["observed-absent"] + obs[e]["not-needed"]
    lim = obs[e]["unobserved"] + obs[e]["not-testable"]
    print("%-10s %-10s %6d %6d %6d %6d  %s" % (e, status(e), lines[e], nonabs[e], ev, lim, dict(view[e].most_common())))
tiers = collections.defaultdict(list)
for i, e in sorted(E.items()):
    t4 = [t for t in (e.get("tier") or []) if str(t).startswith("T4-")] or [str((e.get("tier") or ["(none)"])[0])]
    tiers[t4[0]].append(i)
print("\nelements by first fourth-order theme (or first tier):")
for t, ids in sorted(tiers.items()):
    print("  %-8s %s  non-absent lines %d" % (t, ids, sum(nonabs[i] for i in ids)))
print("arrows: %s  non-absent lines %d" % (sorted(A), sum(nonabs[i] for i in A)))
print("dimension targets: non-absent lines %d" % sum(v for k, v in nonabs.items() if k.startswith("D")))
print("total non-absent %d; absent evidenced %d; absent limits %d; propose %d" % (
    sum(v for k, v in nonabs.items() if k != "(propose)"),
    sum(o["observed-absent"] + o["not-needed"] for o in obs.values()),
    sum(o["unobserved"] + o["not-testable"] for o in obs.values()), lines["(propose)"]))
