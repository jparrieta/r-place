#!/usr/bin/env python3
"""D4a-08: the facts of the earlier room-form cuts (D4a-05 to D4a-08c), read from their own files, for
room-forms-allocation.md. Prints a short text report.

    python3 out/_analysis/d4a08d_history_facts.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


for tag in ("D4a05", "D4a06", "D4a07", "D4a08", "D4a08b", "D4a08c"):
    rows = jl(os.path.join(OUT, "room-forms-%s.jsonl" % tag))
    lv = collections.Counter(r.get("level") for r in rows)
    print("== %s: %d lines, levels %s" % (tag, len(rows), dict(lv)))
    keys = sorted({k for r in rows for k in r})
    print("   keys:", ", ".join(keys))
    for r in rows:
        if r.get("level") not in ("form", None) and r.get("level") != "core":
            continue
        n = r.get("n") or r.get("members_n") or len(r.get("members") or [])
        extra = {k: r[k] for k in ("defining", "thin", "core", "core_placed_by_codes", "ward_n", "weights", "k") if k in r}
        print("   %s | %s | n=%s | %s" % (r.get("id"), r.get("name"), n, extra))
    tsv = os.path.join(OUT, "room-forms-%s.tsv" % tag)
    if os.path.exists(tsv):
        lines = open(tsv, encoding="utf-8").read().splitlines()
        print("   tsv: %d rows; header: %s" % (len(lines) - 1, lines[0]))
for i, r in enumerate(jl(os.path.join(OUT, "departures.jsonl")), 1):
    if i >= 11:
        print("-- departures line %d (%s): %s" % (i, r.get("leg"), r.get("provision")))
