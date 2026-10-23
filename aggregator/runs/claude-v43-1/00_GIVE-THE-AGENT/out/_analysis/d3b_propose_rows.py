#!/usr/bin/env python3
"""D3b, G61 (2): the rulings for one packet of unruled re-check propose lines, read in the packet
d3b_propose_packet.py wrote (rebuilt here: unruled re-check propose lines by lifted node, room and id, the slice
[offset, offset + limit)). Each rows line is id|CLASS|evidence. CLASS decides the ruling (G59, G59a, G61 (2)):
  H-<id>       reject, kind proposal; the element, candidate or arrow named states the act
  NOT          reject, kind proposal; the cited concepts do not show the act
  OUT          particular; outside the model's scope (the sub's own business, its own play, the event as news)
  PART         particular; one room's need, with no second room
  NEW:<pair>   accept, kind proposal, pair another room's propose line; no element, arrow or candidate states the
               act; held for notes-D3.md with no move (G61 (4))
  PEND         pending; the concepts are too thin to show or refute the line
NONPORTABLE lines are particulars by construction (G6) and need no row. Every portable line of the packet must be
named once. Refuses an id outside the packet, an unknown class, an H id that is neither an element nor an arrow, and a
NEW pair that is not a propose line of another room. Writes d3_rulings/<name>.jsonl for d3b_adjudicate_batch.py.

    python3 out/_analysis/d3b_propose_rows.py --offset 0 --limit 100 --packet d3b_pp_000.txt \
        --rows out/_analysis/d3_rulings/propose-000-rows.txt --name recheck-propose-000 [--write]
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ap = argparse.ArgumentParser()
ap.add_argument("--offset", type=int, required=True)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--packet", required=True)
ap.add_argument("--rows", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def node(l, i):
    lift = l.get("lift") or []
    return lift[i] if len(lift) > i and lift[i] else None


ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
rec = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
old = jl(os.path.join(OUT, "adaptations.jsonl"))
sel = [l for l in rec if l.get("op") == "propose" and l["id"] not in ruled]
sel.sort(key=lambda l: (node(l, 1) is None, node(l, 1) or "", l["sub"].lower(), l["id"]))
page = {l["id"]: l for l in sel[a.offset:a.offset + a.limit]}
props = {l["id"]: l for l in old + rec if l.get("op") == "propose"}
els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
arrs = {e["id"]: e for e in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
rows, errs = {}, []
for n, line in enumerate(open(a.rows, encoding="utf-8"), 1):
    line = line.rstrip("\n")
    if not line.strip():
        continue
    parts = line.split("|", 2)
    if len(parts) != 3 or not parts[2].strip():
        errs.append("rows line %d: not id|CLASS|evidence" % n)
        continue
    i, c, ev = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if i not in page:
        errs.append("rows line %d: %s is not in this packet" % (n, i))
        continue
    if i in rows:
        errs.append("rows line %d: %s named twice" % (n, i))
    if page[i].get("portable") is False:
        errs.append("rows line %d: %s is NONPORTABLE, a particular by construction; drop its row" % (n, i))
    if c.startswith("H-"):
        t = c[2:]
        if t not in els and t not in arrs:
            errs.append("rows line %d: %s is neither an element nor an arrow" % (n, t))
    elif c.startswith("NEW:"):
        p = c[4:]
        if p not in props:
            errs.append("rows line %d: pair %s is not a propose line" % (n, p))
        elif props[p]["sub"] == page[i]["sub"]:
            errs.append("rows line %d: pair %s is a line of the same room" % (n, p))
    elif c not in ("NOT", "OUT", "PART", "PEND"):
        errs.append("rows line %d: unknown class %r" % (n, c))
    rows[i] = (c, ev)
for i, l in page.items():
    if l.get("portable") is not False and i not in rows:
        errs.append("%s (portable) is in the packet and has no row" % i)
if errs:
    sys.exit("\n".join(errs))
head = "G61 (2), G59 and G59a, read in %s: " % a.packet
out, tally = [], collections.Counter()
for i, l in page.items():
    if l.get("portable") is False:
        r = {"adaptation": i, "decision": "particular", "kind": "particular",
             "reason": head + "the line is marked NONPORTABLE (%s); a particular by construction (G6)" %
                       ", ".join(l.get("nonportable_hits") or [])}
    else:
        c, ev = rows[i]
        if c.startswith("H-"):
            t = c[2:]
            if t in arrs:
                tail = "the arrow %s states the act by its connection, bound or mechanism, so the proposal adds nothing the model lacks" % t
            elif els[t].get("status") == "candidate":
                tail = "the candidate %s states the act by its statement or range, so the proposal adds nothing the model lacks (G61 (2))" % t
            else:
                tail = "the element %s holds the act by its statement or range, so the proposal adds nothing the model lacks" % t
            r = {"adaptation": i, "decision": "reject", "kind": "proposal", "reason": head + ev + "; " + tail}
        elif c == "NOT":
            r = {"adaptation": i, "decision": "reject", "kind": "proposal",
                 "reason": head + ev + "; the cited concepts do not show the act the line proposes"}
        elif c == "OUT":
            r = {"adaptation": i, "decision": "particular", "kind": "particular",
                 "reason": head + ev + "; outside the model's scope, since here the room did not organize or did something the model is not about (stage section 4); this room's particular"}
        elif c == "PART":
            r = {"adaptation": i, "decision": "particular", "kind": "particular",
                 "reason": head + ev + "; shown in this room only, a locally supported particular with no shared warrant (stage section 1)"}
        elif c.startswith("NEW:"):
            r = {"adaptation": i, "decision": "accept", "kind": "proposal", "pair": c[4:],
                 "reason": head + ev + "; the act is stated by no element's statement or range, no arrow and no candidate, and %s's room shows it; accepted as a proposal, held for notes-D3.md with its rooms and lines, with no move (G61 (4))" % c[4:]}
        else:
            r = {"adaptation": i, "decision": "pending",
                 "reason": head + ev + "; the concepts are too thin to show or refute the line's statement; pending, counted apart"}
    out.append(r)
    tally["%s/%s" % (r["decision"], r.get("kind"))] += 1
print("%s propose packet [%d, %d): %d rulings; %s" % (a.name, a.offset, a.offset + len(page), len(out), dict(tally)))
if a.write:
    p = os.path.join(RD, a.name + ".jsonl")
    if os.path.exists(p):
        sys.exit("%s exists; rulings files are never overwritten" % p)
    open(p, "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    print("wrote %s" % p)
else:
    print("dry run: nothing written")
