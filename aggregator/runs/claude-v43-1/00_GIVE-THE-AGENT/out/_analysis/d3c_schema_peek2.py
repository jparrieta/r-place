#!/usr/bin/env python3
"""D3c: for d3c_exception_report.py. Prints (1) the 'pair' field's shape by last-ruling kind, with examples;
(2) the 'grade' values of verdicts-D.jsonl and verdicts-recheck-D.jsonl readers' lines; (3) the element fields
that could mark the model's top (tier, level, kind, dimension, status) with their values; (4) the element and
arrow ids the ledgers' 'element' field names, counted by prefix. Read-only.

    python3 out/_analysis/d3c_schema_peek2.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
shape = collections.Counter()
ex = {}
for i, r in last.items():
    p = r.get("pair")
    k = (r.get("decision"), r.get("kind"), type(p).__name__)
    shape[k] += 1
    ex.setdefault(k, (i, p))
print("== pair shape by (decision, kind, type)")
for k, n in sorted(shape.items(), key=str):
    print("  ", n, k, "e.g.", ex[k])
for name in ("verdicts-D.jsonl", "verdicts-recheck-D.jsonl"):
    g = collections.Counter(json.dumps(r.get("grade"))[:80] for r in jl(os.path.join(OUT, name)) if not r.get("ruled_by"))
    print("== grade in", name, g.most_common(10))
els = jl(os.path.join(OUT, "model", "elements.jsonl"))
print("== elements", len(els), "keys", sorted({k for e in els for k in e}))
for f in ("tier", "level", "kind", "dimension", "status", "order", "type", "group"):
    vals = collections.Counter(json.dumps(e.get(f))[:40] for e in els)
    if len(vals) > 1 or list(vals)[0] != "null":
        print("  ", f, vals.most_common(12))
print("== elements", " ".join("%s:%s" % (e.get("id"), e.get("status")) for e in els))
arr = jl(os.path.join(OUT, "model", "arrows.jsonl"))
print("== arrows", len(arr), "keys", sorted({k for e in arr for k in e}))
print("   ", " ".join("%s:%s>%s" % (e.get("id"), e.get("from"), e.get("to")) for e in arr))
pref = collections.Counter()
for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in jl(os.path.join(OUT, name)):
        e = l.get("element") or "(none)"
        pref[(name, e[:1] if e != "(none)" else e)] += 1
print("== ledger element prefixes", sorted(pref.items()))
