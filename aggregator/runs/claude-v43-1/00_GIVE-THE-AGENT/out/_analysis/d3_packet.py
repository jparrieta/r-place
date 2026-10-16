#!/usr/bin/env python3
"""D3: one packet of one element's ledger lines, read whole (QD3-001, J: yes). Selects exactly what
`mem.py adaptations --element <id>` selects (every line whose element is the id), in the verb's order (op, then room),
and prints the slice [offset, offset + limit) with every field whole: id, op, source and its label, the lift, condition,
statement, observation, how, relation, portable and its hits, the cited concepts with their labels from the store,
the transitions, the line's current decision (the last adjudication), the room's same-session repairs
(DROPS/D/REPAIRS.tsv), and whether the room's placements carry the element (a second-order theme of the room placed on
one of the element's third-order themes, directly or through its fourth-order tiers). Never prints a line of another
element, and writes nothing.

    python3 out/_analysis/d3_packet.py --element R01 --offset 0 --limit 100 [--op instantiate]
"""
import argparse, ast, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=100)
ap.add_argument("--op")
a = ap.parse_args()
if a.limit > 100:
    raise SystemExit("a packet holds at most 100 lines (stage D3)")


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


sel = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") == a.element
       and (not a.op or l.get("op") == a.op)]
sel.sort(key=lambda l: (l["op"], l["sub"]))
page = sel[a.offset:a.offset + a.limit]
subs = {l["sub"] for l in page}
adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
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
t3 = set()
for t in (E.get(a.element, {}).get("tier") or []):
    if str(t).startswith("T3-"):
        t3.add(t)
    elif str(t).startswith("T4-"):
        t3 |= set(fourth.get(t, {}).get("members") or [])
carry = set()
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    if r.get("sub") in subs and set(lst(r.get("third_order"))) & t3:
        carry.add(r["sub"])
print("%s: %d lines in all%s; packet [%d, %d): %d lines; carried through %s" % (
    a.element, len(sel), " (op %s)" % a.op if a.op else "", a.offset, a.offset + len(page), len(page),
    ",".join(sorted(t3)) or "no third-order tier"))
print("ops in the packet: %s" % dict(collections.Counter(l["op"] for l in page)))
for l in page:
    d = adj.get(l["id"], {}).get("decision", l.get("decision"))
    src = l.get("source")
    print("\n== %s  %s  [%s]  repairs %s  %s%s" % (
        l["id"], l["op"], d, rep.get(l["sub"], "?"), "carried" if l["sub"] in carry else "not carried",
        "" if l.get("portable", True) else "  NONPORTABLE %s" % l.get("nonportable_hits")))
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
