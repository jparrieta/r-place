#!/usr/bin/env python3
"""D4a-08: facts about the rooms' coded concepts before the code block is fixed. Read-only.

    python3 out/_analysis/d4a08_codefacts.py
"""
import collections, json, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


t4of3 = {}
for f in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in f.get("members") or []:
        t4of3[m] = f["id"]
dof4 = {}
for d in jl(os.path.join(OUT, "dimensions.jsonl")):
    for m in d.get("members") or []:
        dof4.setdefault(m, d["id"])
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
codes = jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
per = collections.Counter(r["sub"] for r in codes)
st = collections.Counter()
for r in codes:
    t3 = place.get((r["sub"], r.get("theme_id")), [])
    if not t3:
        st["no third-order placement"] += 1
    elif not any(x in t4of3 for x in t3):
        st["third-order only (no fourth-order node)"] += 1
    else:
        st["placed to the fourth order"] += 1
        if len(t3) > 1:
            st["placed under more than one third-order theme"] += 1
print("codes", len(codes), dict(st))
print("codes per room: min %d median %s max %d" % (min(per.values()), statistics.median(per.values()), max(per.values())))
print("third-order themes reached by codes:", len({x for k, v in place.items() for x in v}))
