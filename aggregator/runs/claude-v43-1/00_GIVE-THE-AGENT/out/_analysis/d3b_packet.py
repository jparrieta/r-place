#!/usr/bin/env python3
"""D3b: one packet of the unruled re-check lines of one element (QD3-001: read whole through a helper), in room
order, slice [offset, offset + limit), limit at most 100, optionally one op. Prints the element's statement and
range (as the revised model serves them), then for each line: id, room, op, observation, the source theme and its
label, the lift, condition, statement, relation, how, portable and its hits, each cited concept with its label and
hour, and two context lines: the room's first-return lines on the element (op and last decision), and for an
absent line the room's themes whose placements carry the element (with their labels). Writes the packet to --out.

    python3 out/_analysis/d3b_packet.py --element P24 --op instantiate --offset 0 --limit 100 --out out/_analysis/d3b_pk_P24_i000.txt
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op")
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=100)
ap.add_argument("--ids", help="a jsonl file whose lines name the adaptation ids to take (e.g. the flagged absent list)")
ap.add_argument("--out", required=True)
a = ap.parse_args()
if a.limit > 100:
    raise SystemExit("a packet holds at most 100 lines (stage D3)")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


ruled = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    ruled[r["adaptation"]] = r
take = None
if a.ids:
    take = {json.loads(l)["adaptation"] for l in open(a.ids, encoding="utf-8") if l.strip()}
new = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
       if r.get("element") == a.element and r["id"] not in ruled and (not a.op or r["op"] == a.op)
       and (take is None or r["id"] in take)]
new.sort(key=lambda r: (r["sub"].lower(), r["op"], r["id"]))
page = new[a.offset:a.offset + a.limit]
subs = {r["sub"] for r in page}
lab, tl = {}, {}
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in subs:
        lab[(r["sub"], r["code_id"])] = (r.get("first_order"), r.get("hour"))
for r in jl(os.path.join(ST, "themes.jsonl")):
    if r["sub"] in subs:
        tl[(r["sub"], r["theme_id"])] = r.get("second_order")
els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
ars = {x["id"]: x for x in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
t4m = {r["id"]: set(r.get("members") or []) for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
e = els.get(a.element)
el_t3 = set()
if e:
    tiers = e.get("tier") or []
    tiers = [tiers] if isinstance(tiers, str) else tiers
    for t in tiers:
        el_t3 |= t4m.get(t, set())
place = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    if r["sub"] in subs:
        for t in r.get("third_order") or []:
            if t in el_t3:
                place[r["sub"]].append((r["theme_id"], t))
oldl = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "adaptations.jsonl")):
    if r["sub"] in subs and r.get("element") == a.element:
        d = ruled.get(r["id"], {})
        oldl[r["sub"]].append("%s %s/%s" % (r["op"], d.get("decision"), d.get("kind")))
W = []
if e:
    W.append("element %s (%s, %s): %s" % (a.element, e.get("kind"), e.get("status"), e.get("statement")))
    W.append("range: %s" % e.get("range"))
elif a.element in ars:
    x = ars[a.element]
    W.append("arrow %s (%s to %s; %s): %s" % (a.element, x["from"], x["to"], x.get("strength"), x.get("mechanism")))
W.append("unruled re-check lines on %s%s: %d; this packet [%d, %d)" % (
    a.element, (" (" + a.op + ")") if a.op else "", len(new), a.offset, a.offset + len(page)))
W.append("")
for r in page:
    s = r["sub"]
    src = str(r.get("source") or "")
    t = src.split(":")[-1] if src else ""
    W.append("== %s  %s  %s%s%s" % (r["id"], s, r["op"], (" " + str(r.get("observation"))) if r.get("observation") else "",
                                     "  NONPORTABLE %s" % r.get("nonportable_hits") if r.get("portable") is False else ""))
    if src:
        W.append("   source %s (%s); lift %s" % (t, tl.get((s, t)), r.get("lift")))
    for k in ("condition", "statement", "relation"):
        if r.get(k):
            W.append("   %s: %s" % (k, r[k]))
    W.append("   how: %s" % r.get("how"))
    cs = codes(r)
    if cs:
        W.append("   codes: " + "; ".join("%s %s (h%s)" % (c, (lab.get((s, c)) or ("?", "?"))[0], (lab.get((s, c)) or ("?", "?"))[1]) for c in cs))
    W.append("   first return on %s: %s" % (a.element, ", ".join(oldl.get(s, [])) or "none"))
    if r["op"] == "absent":
        pl = place.get(s, [])
        W.append("   placements carrying it: %s" % ("; ".join("%s %s -> %s" % (th, tl.get((s, th)), t3) for th, t3 in pl) or "none"))
    W.append("")
if os.path.exists(a.out):
    raise SystemExit("refused: %s exists; packets that rulings cite are never overwritten" % a.out)
open(a.out, "w", encoding="utf-8").write("\n".join(W) + "\n")
print("wrote %s: %d lines (of %d)" % (a.out, len(page), len(new)))
