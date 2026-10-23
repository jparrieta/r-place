#!/usr/bin/env python3
"""D3b, G61 (2): one packet of the unruled re-check propose lines, read whole (QD3-001), by lifted node (stage D3
section 3), as d3_propose_packet.py read the first return's. Selects the re-check lines with op propose and no ruling,
orders them by the source's third-order node (unplaced last), then by room and id, and writes the slice
[offset, offset + limit) with every field whole: id, source and its label, the lift, the statement, relation, how,
portability, and every cited concept quoted through cite.py (each read logged by the verb). Under each line it lists
the room's first-return propose lines with their last ruling (decision, kind, pair and the first 240 characters of the
reason), so that a line repeating one D3a-55 accepted for a candidate can be named (G61 (2)). Writes to --out.

    python3 out/_analysis/d3b_propose_packet.py --offset 0 --limit 100 --out out/_analysis/d3b_pp_000.txt
"""
import argparse, collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--offset", type=int, default=0)
ap.add_argument("--limit", type=int, default=100)
ap.add_argument("--out", required=True)
a = ap.parse_args()
if a.limit > 100:
    raise SystemExit("a packet holds at most 100 lines (stage D3)")
if not os.path.abspath(a.out).startswith(os.path.join(OUT, "_analysis") + os.sep):
    raise SystemExit("--out must be under out/_analysis/")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def node(l, i):
    lift = l.get("lift") or []
    return lift[i] if len(lift) > i and lift[i] else None


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
old = collections.defaultdict(list)
for l in jl(os.path.join(OUT, "adaptations.jsonl")):
    if l.get("op") == "propose":
        old[l["sub"]].append(l)
sel = [l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl")) if l.get("op") == "propose" and l["id"] not in last]
sel.sort(key=lambda l: (node(l, 1) is None, node(l, 1) or "", l["sub"].lower(), l["id"]))
page = sel[a.offset:a.offset + a.limit]
names = {}
for l in open(os.path.join(OUT, "scheme_v2.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    i = r.get("id") or r.get("theme_id")
    if i and i not in names:
        names[i] = r.get("name") or r.get("label")
tlabels = {}
subs = {l["sub"] for l in page}
for l in open(os.path.join(ROOT, "package", "store", "themes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r.get("sub") in subs:
        tlabels[(r["sub"], r.get("theme_id"))] = r.get("second_order") or r.get("label")
counts = collections.Counter(node(l, 1) or "none" for l in sel)
W = ["re-check propose lines unruled: %d; packet [%d, %d): %d lines in %d rooms" % (
    len(sel), a.offset, a.offset + len(page), len(page), len(subs)),
     "nodes in the packet: %s" % dict(collections.Counter(node(l, 1) or "none" for l in page))]
seen = set()
for l in page:
    n3 = node(l, 1) or "none"
    if n3 not in seen:
        seen.add(n3)
        W.append("\n#### node %s (%s): %d unruled lines; fourth-order %s; dimension %s" % (
            n3, names.get(n3, "unplaced"), counts[n3], node(l, 2), node(l, 3)))
    W.append("\n== %s  %s  propose%s" % (l["id"], l["sub"], "" if l.get("portable", True) else
                                         "  NONPORTABLE %s" % l.get("nonportable_hits")))
    src = l.get("source")
    if src:
        W.append("   source %s (%s); lift %s" % (src, tlabels.get((l["sub"], src.split(":")[-1])),
                                                " > ".join(str(x) for x in (l.get("lift") or []))))
    for k in ("statement", "relation"):
        if l.get(k):
            W.append("   %s: %s" % (k, l[k]))
    W.append("   how: %s" % l.get("how"))
    for c in codes(l):
        q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", l["sub"], "--code", c],
                           cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
        W.append("   " + (q[0] if q else "(no quote) %s/%s" % (l["sub"], c)))
    for o in old.get(l["sub"], []):
        r = last.get(o["id"], {})
        W.append("   first return %s: %s/%s pair=%s | %s" % (o["id"], r.get("decision"), r.get("kind"), r.get("pair"),
                                                            str(r.get("reason"))[:240]))
if os.path.exists(a.out):
    sys.exit("refused: %s exists; packets that rulings cite are never overwritten" % a.out)
open(a.out, "w", encoding="utf-8").write("\n".join(W) + "\n")
print("wrote %s: %d lines" % (a.out, len(page)))
