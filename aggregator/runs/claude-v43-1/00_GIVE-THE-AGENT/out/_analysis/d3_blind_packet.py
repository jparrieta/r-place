#!/usr/bin/env python3
"""D3, J's drift check: print the lines of a blind re-rule sample whole, as d3_packet.py prints them, but with no
decision, kind, pair or reason of mine. Prints the element's current statement and range once per element, then each
line: id, op, source and its label, the lift, observation, condition, statement, relation, link kind, how, the cited
concepts with their labels, the transitions, repairs, and whether the room's placements carry the element.
Writes nothing.

    python3 out/_analysis/d3_blind_packet.py --sample out/_analysis/d3_blind/sample.json --offset 0 --limit 25
"""
import argparse, ast, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--sample", required=True)
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=25)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def lst(v):
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.strip():
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            return [v]
    return []


S = json.load(open(a.sample, encoding="utf-8"))["sample"][a.offset:a.offset + a.limit]
want = {s["adaptation"] for s in S}
byid = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l["id"] in want}
subs = {l["sub"] for l in byid.values()}
labels = {}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        labels[(r["sub"], r["code_id"])] = r.get("first_order")
tlabels = {}
for l in open(os.path.join(ROOT, "package", "store", "themes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r.get("sub") in subs:
        tlabels[(r["sub"], r.get("theme_id"))] = r.get("second_order") or r.get("label")
rep = {}
rp = os.path.join(ROOT, "DROPS", "D", "REPAIRS.tsv")
if os.path.exists(rp):
    for l in open(rp, encoding="utf-8"):
        c = l.rstrip("\n").split("\t")
        if len(c) >= 2 and not l.startswith(("#", "sub\t")):
            rep[c[0]] = c[1]
E = {r["id"]: r for r in jl(os.path.join(OUT, "model", "elements.jsonl")) + jl(os.path.join(OUT, "model", "arrows.jsonl"))}
fourth = {r["id"]: r for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
assign = jl(os.path.join(OUT, "assignments_final.jsonl"))


def carried(el, sub):
    t3 = set()
    for t in (E.get(el, {}).get("tier") or []):
        if str(t).startswith("T3-"):
            t3.add(t)
        elif str(t).startswith("T4-"):
            t3 |= set(fourth.get(t, {}).get("members") or [])
    return any(r.get("sub") == sub and set(lst(r.get("third_order"))) & t3 for r in assign)


shown = set()
print("blind sample lines [%d, %d) of %s" % (a.offset, a.offset + len(S), a.sample))
for s in S:
    el = s["element"]
    if el not in shown:
        shown.add(el)
        e = E.get(el, {})
        print("\n#### %s (%s): %s | range: %s" % (el, e.get("status"), e.get("statement"), e.get("range")))
    l = byid[s["adaptation"]]
    src = l.get("source")
    print("\n== %s  %s  element %s  repairs %s  %s" % (
        l["id"], l["op"], el, rep.get(l["sub"], "?"), "carried" if carried(el, l["sub"]) else "not carried"))
    if src:
        print("   source %s (%s); lift %s" % (src, tlabels.get((l["sub"], src.split(":")[-1])), " > ".join(
            str(x) for x in (l.get("lift") or []))))
    for k in ("observation", "condition", "statement", "relation", "link_kind"):
        if l.get(k):
            print("   %s: %s" % (k, l[k]))
    print("   how: %s" % l.get("how"))
    ev = l.get("evidence") or {}
    print("   codes: %s" % "; ".join("%s %s" % (c, labels.get((l["sub"], c.split(":")[-1]), "?")) for c in ev.get("codes", [])))
    if ev.get("transitions"):
        print("   transitions: %s" % ", ".join(ev["transitions"]))
