#!/usr/bin/env python3
"""D3b: the before-and-after of the rulings in the rooms the re-check returned (stage section 5: whether the rewrite
fixed what the evidence pointed at). Counts only; nothing is written.

Before: the first return's lines of these rooms (adaptations.jsonl), each with its last ruling (adjudications.jsonl).
After: the re-check's lines (adaptations-recheck.jsonl), each with its last ruling. For each element named: lines by
the last ruling's decision and kind, before and after; accepted corrections (accept or modify, kind correction) with
their rooms, before and after. For each D3a revision (model/history.jsonl, legs D3a-*, the first line of each id and
event that names causes): the cause rooms that the first batch holds, their re-check lines on the element by last
ruling, and the cause rooms whose re-check lines still carry an accepted correction on it. Propose lines before and
after by last ruling, and by the id their reason names as holding the act.

    python3 out/_analysis/d3b_before_after.py --elements R01,P05,P21,P22,A21,P06,R02,K03,K04,P19
"""
import argparse, collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", required=True)
a = ap.parse_args()
want = [e.strip() for e in a.elements.split(",") if e.strip()]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
rooms = {r["sub"] for r in new}
old = [r for r in jl(os.path.join(OUT, "adaptations.jsonl")) if r["sub"] in rooms]
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
print("rooms in the first batch: %d; first-return lines of these rooms %d; re-check lines %d" % (
    len(rooms), len(old), len(new)))


def key(l):
    r = last.get(l["id"])
    if r is None:
        return "unruled"
    return "%s/%s" % (r["decision"], r.get("kind"))


def is_corr(l):
    r = last.get(l["id"])
    return bool(r) and r["decision"] in ("accept", "modify") and r.get("kind") == "correction"


for e in want:
    for label, rows in (("before", old), ("after", new)):
        mine = [l for l in rows if l.get("element") == e]
        c = collections.Counter(key(l) for l in mine)
        corr = sorted({l["sub"] for l in mine if is_corr(l)})
        ncorr = sum(1 for l in mine if is_corr(l))
        print("%s %-6s lines %4d in %3d rooms; %s; accepted corrections %d in %d rooms%s" % (
            e, label, len(mine), len({l["sub"] for l in mine}), dict(sorted(c.items())), ncorr, len(corr),
            (": " + ", ".join(corr)) if corr and len(corr) <= 12 else ""))

print()
print("D3a revisions and their cause rooms in the first batch:")
by_id_old = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl"))}
seen = set()
for h in jl(os.path.join(OUT, "model", "history.jsonl")):
    if not str(h.get("leg", "")).startswith("D3a") or not h.get("adaptations"):
        continue
    k = (h["id"], h.get("event"))
    if k in seen or h["id"] not in want:
        continue
    seen.add(k)
    causes = h["adaptations"]
    croom = sorted({by_id_old[c]["sub"] for c in causes if c in by_id_old})
    inb = [s for s in croom if s in rooms]
    after = [l for l in new if l.get("element") == h["id"] and l["sub"] in set(inb)]
    c = collections.Counter(key(l) for l in after)
    still = sorted({l["sub"] for l in after if is_corr(l)})
    print("%s %s | %s: causes %d in %d rooms, %d in the first batch; their re-check lines on %s: %d, %s; with an "
          "accepted correction: %d%s" % (h.get("leg"), h["id"], h.get("event"), len(causes), len(croom), len(inb),
                                          h["id"], len(after), dict(sorted(c.items())), len(still),
                                          (" (" + ", ".join(still) + ")") if still else ""))

print()
pat = re.compile(r"the (?:element|candidate|arrow) ([A-Z]\d\d) (?:holds|states)")
for label, rows in (("before", old), ("after", new)):
    mine = [l for l in rows if l.get("op") == "propose"]
    c = collections.Counter(key(l) for l in mine)
    held = collections.Counter()
    for l in mine:
        r = last.get(l["id"])
        if r and r["decision"] == "accept" and r.get("kind") == "proposal":
            m = re.search(r"candidate ([A-Z]\d\d)", r.get("reason", ""))
            held["accepted for " + (m.group(1) if m else "?")] += 1
        elif r and r["decision"] == "reject":
            m = pat.search(r.get("reason", ""))
            held["held by " + (m.group(1) if m else "none (not shown)")] += 1
    print("propose %-6s lines %d in %d rooms; %s" % (label, len(mine), len({l["sub"] for l in mine}),
                                                    dict(sorted(c.items()))))
    print("   by id: %s" % dict(held.most_common()))
