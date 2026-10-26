#!/usr/bin/env python3
"""D4a-07: the feature mapping of d4a07_room_forms.py as a module (the same code), for the reading helpers:
the selected lines by room (BY) and features(line, level), the nodes and links one line touches."""
import collections, itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
LV = (("T3", 1), ("T4", 2), ("dim", 3))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ARROWS = {r["id"]: r for r in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
ELEM = {r["id"]: r for r in jl(os.path.join(OUT, "model", "elements.jsonl"))}
T4OF3 = {}
for f in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    for m in f.get("members") or []:
        T4OF3[m] = f["id"]
DOF4 = {}
for d in jl(os.path.join(OUT, "dimensions.jsonl")):
    for m in d.get("members") or []:
        DOF4.setdefault(m, d["id"])
PLACED = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE and len(r.get("lift") or []) >= 4]
BY = collections.defaultdict(list)
for r in PLACED:
    BY[r["sub"]].append(r)


def t4s(eid):
    out = []
    for a in ELEM.get(eid, {}).get("tier") or []:
        n = a if a.startswith("T4-") else T4OF3.get(a) if a.startswith("T3-") else None
        if n and n not in out:
            out.append(n)
    return out


def end_nodes(eid, lv, ev_t3):
    if lv == "T4":
        return t4s(eid) or [eid]
    if lv == "dim":
        ds = []
        for n in t4s(eid):
            d = DOF4.get(n)
            if d and d not in ds:
                ds.append(d)
        return ds or [eid]
    t3 = [a for a in ELEM.get(eid, {}).get("tier") or [] if a.startswith("T3-")]
    if t3:
        return t3
    if ev_t3 and T4OF3.get(ev_t3) in t4s(eid):
        return [ev_t3]
    return t4s(eid) or [eid]


def features(line, lv, with_links=True, link_ops=True):
    i = dict(LV)[lv]
    node = line["lift"][i]
    is_arrow = line["element"] in ARROWS
    is_linkop = line["op"] == "link" and not is_arrow and link_ops
    out = []
    if with_links and (is_arrow or is_linkop):
        if is_arrow:
            a = ARROWS[line["element"]]
            src = end_nodes(a["from"], lv, line["lift"][1])
            tgt = end_nodes(a["to"], lv, line["lift"][1])
        else:
            first = node or line["lift"][1]
            src = [first] if first else []
            tgt = end_nodes(line["element"], lv, None)
        pairs = list(itertools.product(src, tgt))
        if pairs:
            for s, t in pairs:
                out.append(("%s>%s" % (s, t), 0.5 / len(pairs)))
            if node:
                out.append((node, 0.5))
            return out
    if node:
        out.append((node, 1.0))
    return out
