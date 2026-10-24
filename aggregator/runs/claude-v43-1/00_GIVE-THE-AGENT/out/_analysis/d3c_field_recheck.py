#!/usr/bin/env python3
"""D3c: the field's entries (out/sealed/FIELD.jsonl ids) in the re-check ledger, by op: rooms and lines, and the
lines by last ruling (specification, elaboration, correction, limit, particular, rejected), with the element's
status and the leg of its last history line. Read-only.

    python3 out/_analysis/d3c_field_recheck.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ids = [json.loads(l)["id"] for l in open(os.path.join(OUT, "sealed", "FIELD.jsonl"), encoding="utf-8") if l.strip()]
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
st = {e["id"]: e.get("status") for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
st.update({e["id"]: e.get("status") for e in jl(os.path.join(OUT, "model", "arrows.jsonl"))})
H = jl(os.path.join(OUT, "model", "history.jsonl"))


def cls(d):
    if d.get("decision") in ("accept", "modify"):
        return d.get("kind") if d.get("kind") in ("specification", "elaboration", "correction") else "limit"
    return {"particular": "particular", "reject": "rejected"}.get(d.get("decision"), "other")


L = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
for i in ids:
    lines = [l for l in L if l.get("element") == i]
    hl = [n for n, h in enumerate(H, 1) if h.get("id") == i]
    print("== %s: status %s; history lines %s; re-check lines %d in %d rooms" % (
        i, st.get(i), hl, len(lines), len({l["sub"] for l in lines})))
    for op in ("instantiate", "restrict", "add-condition", "add-step", "link", "contradict", "absent"):
        ls = [l for l in lines if l["op"] == op]
        if not ls:
            continue
        c = collections.Counter(cls(last.get(l["id"], {})) for l in ls)
        print("   %s: %d lines in %d rooms; %s" % (op, len(ls), len({l["sub"] for l in ls}), dict(c)))
