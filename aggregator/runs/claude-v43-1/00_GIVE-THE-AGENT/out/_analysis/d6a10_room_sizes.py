#!/usr/bin/env python3
"""D6a-10: two size measures per room, for the size-held test (J, 27 Oct 09:27 Berlin).
  coded_concepts   the room's coded concepts in package/store/codes.jsonl (the measure the room-form tree carries);
  canvas_concepts  the room's coded concepts whose second-order theme is placed (assignments_final.jsonl,
                   'third_order') under a fourth-order theme of dimensions D01 to D04 (Critical mass, Coordination
                   without command, Maintenance, Order without law), by fourth/fourth.jsonl and dimensions.jsonl.
A concept whose theme carries several third-order placements counts as canvas work if any of them lies under D01 to
D04. Prints JSON: per room, and a summary with checks against room-forms-tree-rooms.tsv.

    python3 out/_analysis/d6a10_room_sizes.py > out/_analysis/d6a10_room_sizes.json
"""
import collections, csv, json, os, statistics

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
ROOT = os.path.dirname(OUT)
CANVAS = {"D01", "D02", "D03", "D04"}
t3_t4 = collections.defaultdict(set)
for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8"):
    x = json.loads(l)
    for m in x["members"]:
        t3_t4[m].add(x["id"])
t4_d = collections.defaultdict(set)
for l in open(os.path.join(OUT, "dimensions.jsonl"), encoding="utf-8"):
    x = json.loads(l)
    for t in x["members"]:
        t4_d[t].add(x["id"])
placed = {}
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    a = json.loads(l)
    placed[(a["sub"], a["theme_id"])] = a.get("third_order") or []
total = collections.Counter()
canvas = collections.Counter()
by_dim = collections.Counter()
no_theme = 0
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    c = json.loads(l)
    total[c["sub"]] += 1
    t3s = placed.get((c["sub"], c.get("theme_id")))
    if t3s is None:
        no_theme += 1
        continue
    dims = set()
    for t3 in t3s:
        for t4 in t3_t4.get(t3, ()):
            dims.update(t4_d.get(t4, ()))
    if dims & CANVAS:
        canvas[c["sub"]] += 1
    for d in dims:
        by_dim[d] += 1
rows = list(csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"), delimiter="\t"))
mismatch = [r["room"] for r in rows if int(r["coded_concepts"]) != total.get(r["room"], 0)]
summary = {"codes": sum(total.values()), "codes_without_theme_assignment": no_theme, "codes_by_dimension": dict(by_dim),
           "t3_in_several_t4": sum(1 for v in t3_t4.values() if len(v) > 1),
           "rooms": len(rows), "coded_concepts_mismatch_with_tree_tsv": mismatch, "by_form": {}}
for f in "ABCDEF":
    dfn = [r["room"] for r in rows if r["form"] == f and r["role"] == "defining"]
    summary["by_form"][f] = {"defining": len(dfn), "median_coded": statistics.median(total[s] for s in dfn),
                             "median_canvas": statistics.median(canvas[s] for s in dfn),
                             "canvas_share": round(sum(canvas[s] for s in dfn) / sum(total[s] for s in dfn), 3)}
print(json.dumps({"summary": summary,
                  "rooms": {r["room"]: {"coded": total.get(r["room"], 0), "canvas": canvas.get(r["room"], 0)}
                            for r in rows}}, ensure_ascii=False))
