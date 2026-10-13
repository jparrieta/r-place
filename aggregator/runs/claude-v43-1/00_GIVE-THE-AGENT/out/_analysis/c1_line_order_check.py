"""Count placed lines whose theme order or second-theme floor departs from rule 0 (read-only).

Rule 0: order the placed themes by concept count, ties by placements; a second or third theme needs three concepts
of its own (QC1-002). For every line of assignments_final.jsonl with two or more themes this counts:
- order: the first theme has fewer counted concepts than another placed theme;
- floor: a theme after the first has fewer than three counted concepts.
Both are broken down by the line's source (readers, ruling, ...) and whether the line has a C1 revision.

    python3 out/_analysis/c1_line_order_check.py [--list order|floor]
"""
import argparse
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

ap = argparse.ArgumentParser()
ap.add_argument("--list", default="")
a = ap.parse_args()


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


rows = jl(os.path.join(OUT, "assignments_final.jsonl"))
rev = set((r["sub"], r["theme_id"]) for r in jl(os.path.join(OUT, "assign_revisions_only.jsonl")))
multi = [r for r in rows if len(r.get("third_order") or []) >= 2]
order, floor = [], []
for r in multi:
    sup = r.get("support_by_theme") or {}
    th = r["third_order"]
    n = [len(sup.get(t) or []) for t in th]
    if n[0] < max(n[1:]):
        order.append(r)
    if any(x < 3 for x in n[1:]):
        floor.append(r)


def by(rs):
    c = collections.Counter("%s%s" % (r.get("source"), " +C1" if (r["sub"], r["theme_id"]) in rev else "") for r in rs)
    return json.dumps(dict(c.most_common()))


print("placed lines %d; with two themes or more %d" % (sum(1 for r in rows if r.get("third_order")), len(multi)))
print("first theme has fewer concepts than another: %d  %s" % (len(order), by(order)))
print("a later theme below three concepts: %d  %s" % (len(floor), by(floor)))
print("multi-theme lines by source: %s" % by(multi))
pick = {"order": order, "floor": floor}.get(a.list)
if pick:
    print("\n".join("%s:%s %s %s" % (r["sub"], r["theme_id"], r.get("source"),
                                    ", ".join("%s(%d)" % (t, len((r.get('support_by_theme') or {}).get(t) or [])) for t in r["third_order"]))
                    for r in pick))
