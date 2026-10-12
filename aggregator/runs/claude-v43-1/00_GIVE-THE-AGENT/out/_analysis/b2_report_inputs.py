#!/usr/bin/env python3
"""B2d: inputs for pilot_report.md. (1) scheme_edits.jsonl grouped by theme: lines per round, by field and by kind,
with the items that caused them; (2) the moved rechecks marked author-error, by item; (3) the DONE records of every
round (readers, valid returns, cost, tokens). Reads only."""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


ed = jl(os.path.join(OUT, "scheme_edits.jsonl"))
print("edits %d; by kind %s; by field %s; by round %s" % (
    len(ed), dict(collections.Counter(e.get("kind") for e in ed)), dict(collections.Counter(e.get("field") for e in ed)),
    dict(collections.Counter(e.get("round") for e in ed))))
by = collections.defaultdict(list)
for e in ed:
    if e.get("kind") != "gate-check":
        by[e["theme"]].append(e)
print("themes edited, mirrors aside: %d" % len(by))
for t in sorted(by):
    es = by[t]
    items = sorted({c for e in es for c in (e.get("caused_by") or [])})
    print("  %s: %d lines (%s); kinds %s; rounds %s; caused by %s" % (
        t, len(es), ", ".join("%s %d" % kv for kv in collections.Counter(e["field"] for e in es).items()),
        ",".join(sorted({e.get("kind") for e in es})), ",".join(sorted({str(e.get("round")) for e in es})), ", ".join(items)))
ae = [e for e in ed if e.get("kind") == "author-error"]
print("author-error lines in scheme_edits: %s" % ["%s %s %s" % (e["theme"], e["field"], e.get("caused_by")) for e in ae])
rc = jl(os.path.join(OUT, "rechecks-B2.jsonl"))
moved = collections.defaultdict(set)
for r in rc:
    if r.get("changed") and "author-error" in str(r.get("why") or r.get("reason") or ""):
        moved["%s/%s" % (r["sub"], r["theme_id"])].add(r.get("source"))
print("rechecks marked author-error and moved: %d items: %s" % (len(moved), ", ".join(sorted(moved))))
for d in sorted(os.listdir(os.path.join(OUT, "_fleet_raw", "B2"))):
    p = os.path.join(OUT, "_fleet_raw", "B2", d, "DONE")
    if os.path.exists(p):
        x = json.load(open(p))
        print("  %s: valid %s, exhausted %s, cost %.4f USD, input %s, output %s tokens" % (
            d, x.get("valid_returns"), x.get("exhausted"), x.get("cost_usd") or 0, x.get("input_tokens"), x.get("output_tokens")))
