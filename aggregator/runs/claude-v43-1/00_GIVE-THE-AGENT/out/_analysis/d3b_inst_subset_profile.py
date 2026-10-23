#!/usr/bin/env python3
"""D3b: the unruled re-check instantiate lines, by element, sorted into: (a) every cited code is among the codes of
one accepted first-return instantiate line of the same room and element; (b) for a candidate, every cited code is
among the codes of the room's accepted D3a-55 proposal for it; (c) some codes shared with such a line; (d) none.
R01 and P05, revised at D3a, are counted apart. Counts only.

    python3 out/_analysis/d3b_inst_subset_profile.py
"""
import collections, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return frozenset(str(c).split(":")[-1] for c in ev)


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
old = jl(os.path.join(OUT, "adaptations.jsonl"))
oldby = {l["id"]: l for l in old}
acc = collections.defaultdict(list)
for l in old:
    if l["op"] == "instantiate" and last.get(l["id"], {}).get("decision") == "accept":
        acc[(l["sub"], l.get("element"))].append(codes(l))
cands = {c["class"]: c["id"] for c in json.load(open(os.path.join(RD, "propose-candidates.json")))}
for s in glob.glob(os.path.join(RD, "propose-spec-*.txt")):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, c = line.split("|")[:2]
            if c in cands and last.get(i, {}).get("decision") == "accept":
                acc[(oldby[i]["sub"], cands[c])].append(codes(oldby[i]))
new = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl")) if r["op"] == "instantiate" and r["id"] not in last]
by = collections.defaultdict(collections.Counter)
for r in new:
    cs = codes(r)
    m = acc.get((r["sub"], r.get("element")), [])
    k = "subset" if any(cs and cs <= x for x in m) else ("overlap" if any(cs & x for x in m) else "none")
    if r.get("portable") is False:
        k = "nonportable"
    by[r.get("element")][k] += 1
tot = collections.Counter()
for e in sorted(by, key=lambda e: -sum(by[e].values())):
    tot.update(by[e])
    print("%-5s %4d  %s" % (e, sum(by[e].values()), "  ".join("%s=%d" % kv for kv in sorted(by[e].items()))))
print("total", dict(tot))
