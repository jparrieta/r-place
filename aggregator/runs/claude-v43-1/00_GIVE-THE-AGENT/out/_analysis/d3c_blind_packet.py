#!/usr/bin/env python3
"""D3c, J's drift check before the freeze: print the lines of the blind re-rule sample whole, as d3_blind_packet.py
prints them, from either ledger (adaptations.jsonl or adaptations-recheck.jsonl), with no decision, kind, pair or
reason of mine. Prints the element's current statement and range once per element, then each line: id, op, source
and its label, the lift, observation, condition, statement, relation, link kind, how, the cited concepts with their
labels and hours, the transitions, and whether the room's placements carry the element. Writes nothing.

    python3 out/_analysis/d3c_blind_packet.py --sample out/_analysis/d3c_blind/sample-D3c.json --offset 0 --limit 25
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
byid = {}
for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
    for l in jl(os.path.join(OUT, name)):
        if l["id"] in want:
            byid[l["id"]] = l
subs = {l["sub"] for l in byid.values()}
labels = {}
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        labels[(r["sub"], r["code_id"])] = (r.get("first_order"), r.get("hour"))
tlabels = {}
for l in open(os.path.join(ROOT, "package", "store", "themes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r.get("sub") in subs:
        tlabels[(r["sub"], r.get("theme_id"))] = r.get("second_order") or r.get("label")
E = {}
for r in jl(os.path.join(OUT, "model", "elements.jsonl")) + jl(os.path.join(OUT, "model", "arrows.jsonl")):
    E[r["id"]] = r
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


def code(sub, c):
    lab = labels.get((sub, c.split(":")[-1]))
    return "%s %s (h%s)" % (c, lab[0] if lab else "?", lab[1] if lab else "?")


shown = set()
print("blind sample lines [%d, %d) of %s" % (a.offset, a.offset + len(S), a.sample))
for n, s in enumerate(S, a.offset):
    el = s["element"]
    if el not in shown:
        shown.add(el)
        e = E.get(el, {})
        text = e.get("statement") or e.get("connection")
        print("\n#### %s (%s): %s | range: %s%s" % (el, e.get("status"), text, e.get("range"),
                                                  (" | bound: %s" % e["bound"]) if e.get("bound") else ""))
    l = byid[s["adaptation"]]
    src = l.get("source")
    print("\n== %d. %s  %s  element %s  population %s%s  %s" % (
        n, l["id"], l["op"], el, s.get("population"), "  FORCED" if s.get("forced") else "",
        "carried" if carried(el, l["sub"]) else "not carried"))
    if src:
        print("   source %s (%s); lift %s" % (src, tlabels.get((l["sub"], src.split(":")[-1])), " > ".join(
            str(x) for x in (l.get("lift") or []))))
    for k in ("observation", "condition", "statement", "relation", "link_kind"):
        if l.get(k):
            print("   %s: %s" % (k, l[k]))
    print("   how: %s" % l.get("how"))
    ev = l.get("evidence") or {}
    print("   codes: %s" % "; ".join(code(l["sub"], c) for c in ev.get("codes", [])))
    if ev.get("transitions"):
        print("   transitions: %s" % ", ".join(str(x) for x in ev["transitions"]))
