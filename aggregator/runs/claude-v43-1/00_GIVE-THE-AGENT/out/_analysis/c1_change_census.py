#!/usr/bin/env python3
"""C1, read-only: a census of what changed at C1, for scheme_v2.md and the handback. Per gate (gate_history.jsonl):
theme, field, candidates, rechecks done (rechecks-C1.jsonl) and how many changed. Per move entry on
assignments_final.jsonl lines: the keys used, the legs, and a count by leg and by the gate or source the move names.

    python3 out/_analysis/c1_change_census.py [--gates] [--moves]
"""
import argparse, collections, json, os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--gates", action="store_true")
ap.add_argument("--moves", action="store_true")
a = ap.parse_args()

gh = jl("gate_history.jsonl")
rc = jl("rechecks-C1.jsonl")
done = collections.Counter(r.get("change") for r in rc)
moved = collections.Counter(r.get("change") for r in rc if r.get("changed"))
keys = collections.Counter(k for g in gh for k in g)
print("gate_history lines %d; keys %s" % (len(gh), dict(keys)))
print("fields amended: %s" % dict(collections.Counter(g.get("field") for g in gh)))
if a.gates:
    print("ref | leg | theme | field | candidates | owed | rechecked | changed")
    print("\n".join("%s | %s | %s | %s | %s | %s | %d | %d" % (
        g.get("ref"), g.get("leg"), g.get("theme"), g.get("field"), g.get("candidates"),
        g.get("owed") if not isinstance(g.get("owed"), list) else len(g.get("owed")),
        done[g.get("ref")], moved[g.get("ref")]) for g in gh))
rows = jl("assignments_final.jsonl")
mv = [(r["sub"], r["theme_id"], m) for r in rows for m in (r.get("moves") or [])]
print("move entries %d on %d lines; keys %s" % (len(mv), len(set((s, t) for s, t, _ in mv)),
                                               dict(collections.Counter(k for _, _, m in mv for k in m))))
print("by leg: %s" % dict(sorted(collections.Counter(m.get("leg") for _, _, m in mv).items(), key=lambda kv: str(kv[0]))))
if a.moves:
    tag = lambda m: (m.get("change") or (re.search(r"gate:\d+", m.get("why") or "") or [None])[0] or
                     (m.get("why") or "")[:70])
    c = collections.Counter((m.get("leg"), tag(m)) for _, _, m in mv)
    print("\n".join("%s | %s | %d" % (l, t, n) for (l, t), n in sorted(c.items(), key=lambda kv: (str(kv[0][0]), -kv[1]))))
