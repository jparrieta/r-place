#!/usr/bin/env python3
"""C1a-08: a reading packet for the placements the pair test carried (c1_pair_carried.json): for each item its line
(themes with the concepts counted for each, also_present, class, confidence, source), the readers' and my B1's
placements, the concern carried, and every concept of the second-order theme with its quote and the theme it counts for.

    python3 out/_analysis/c1_carried_pack.py      writes out/_analysis/c1_carried_pack.md (refuses to overwrite)
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "out")

spec = importlib.util.spec_from_file_location("bpf", os.path.join(HERE, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
store = bpf.pk.Store(ROOT, OUT)


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


rows = dict(("%s:%s" % (r["sub"], r["theme_id"]), r) for r in jl(os.path.join(OUT, "assignments_final.jsonl")))
b3 = dict(("%s:%s" % (r["sub"], r["theme_id"]), r) for r in jl(os.path.join(OUT, "b3_classes.jsonl")))
car = json.load(open(os.path.join(HERE, "c1_pair_carried.json"), encoding="utf-8"))["items"]

L = ["# The placements the pair test carried (c1_pair_carried.json), read whole", ""]
for i, c in enumerate(car, 1):
    it = c["item"]
    s, t = it.split(":")
    r, k = rows[it], b3.get(it) or {}
    sup = r.get("support_by_theme") or {}
    where = {}
    for th, cs in sup.items():
        for x in cs:
            where.setdefault(x, []).append(th)
    L.append("## C%02d  %s  (pair %s; class %s; %s; source %s; leg %s)" % (i, it, c["pair_n"], k.get("class"), r.get("confidence"),
                                                                        r.get("source"), r.get("leg")))
    L.append("line: %s; also_present %s" % (", ".join("%s (%d)" % (z, len(sup.get(z) or [])) for z in r.get("third_order") or []),
                                             json.dumps(r.get("also_present") or {})))
    L.append("readers at B3: r1 %s; r2 %s; my B1 %s" % (k.get("r1"), k.get("r2"), k.get("b1")))
    L.append("carried: %s now in %s; %s" % (c["concepts"], c["now"], c["field"]))
    th = store.themes.get((s, t)) or {}
    L.append("label: %s" % th.get("second_order"))
    L.append("note: %s" % " ".join(str(th.get("theme_note") or "").split()))
    for cid in th.get("code_ids") or []:
        cd = store.codes.get((s, cid)) or {}
        L.append("- %s [%s] %s" % (cid, ",".join(where.get(cid, [])) or "-", cd.get("first_order") or ""))
        L.append("    \"%s\"" % " ".join(str(cd.get("text") or "").split()))
    L.append("")

pth = os.path.join(HERE, "c1_carried_pack.md")
if os.path.exists(pth):
    sys.exit("%s exists" % pth)
open(pth, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote %s: %d bytes, %d lines" % (os.path.relpath(pth, ROOT), os.path.getsize(pth), len(L)))
