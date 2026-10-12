#!/usr/bin/env python3
"""B2a-r3-p2: count the records that belong to the withdrawn split (J, 2026-10-12), file by file, by matching
each record's item against the 56 children of out/recut/themes.jsonl. Reads only."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


kids = {(r["sub"], r["theme_id"]) for r in jl(os.path.join(OUT, "recut", "themes.jsonl"))}
print("children in out/recut/themes.jsonl:", len(kids))
rc = jl(os.path.join(OUT, "rechecks-B2.jsonl"))
hit = [i for i, r in enumerate(rc, 1) if (r.get("sub"), r.get("theme_id")) in kids
       or str(r.get("item", "")).replace(":", "/") in {"%s/%s" % k for k in kids}]
print("rechecks-B2.jsonl: %d records, %d on children, lines %s to %s" % (len(rc), len(hit), hit[0] if hit else "-", hit[-1] if hit else "-"))
print("contiguous:", hit == list(range(hit[0], hit[-1] + 1)) if hit else "-")
fi = jl(os.path.join(OUT, "fleet_ids.jsonl"))
print("fleet_ids.jsonl: %d lines, %d marked split" % (len(fi), sum(1 for r in fi if r.get("split"))))
for name in ("multiplacement_log.jsonl", "tier_history.jsonl", "exemplar_candidates.jsonl", "scheme_edits.jsonl"):
    rows = jl(os.path.join(OUT, name))
    n = sum(1 for r in rows if (r.get("sub"), r.get("theme_id")) in kids
            or any(c in {"%s/%s" % k for k in kids} for c in (r.get("caused_by") or [])))
    print("%s: %d lines, %d on children" % (name, len(rows), n))
for name in ("author_items.jsonl", "gold_items.jsonl", "_analysis/author_items_split_withdrawn.jsonl",
             "_analysis/gold_items_split_withdrawn.jsonl"):
    print("%s: %d lines" % (name, len(jl(os.path.join(OUT, name)))))
