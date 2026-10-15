#!/usr/bin/env python3
"""C5c-08, problem 1 (the unit): lay out, for reading under the rule logged first (diary, C5c-08, abductive), every
place where an accepted piece of field advice or a later pass may have moved the actor from the room to members.
Writes out/_analysis/c5c8_unit_sweep.txt and prints a summary. Writes nothing else.

  A  every sentence pass 6 replaced (c5c2_decl_spec.json, c5c2_decl_spec2.json), old and new whole, with the
     declaration's accepted lines; flagged '*' where the new sentence names members more, or rooms less, than the old
  B  every element and arrow change of passes 7 and 8 (model/history.jsonl, C5c-03 and C5c-04): the old text and the
     text as it stands now (pass 9 may have changed it again)
  C  the standing element statements and ranges, arrow mechanisms and proposition statements, each
     sentence that names members or a member

    python3 out/_analysis/c5c8_unit_sweep.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
A = os.path.join(OUT, "_analysis")
ROOM = re.compile(r"\b(rooms?|room's|coalitions?|groups?|subs?)\b", re.I)
MEM = re.compile(r"\bmembers?\b|\bmembers'", re.I)


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'\[(])", re.sub(r"\s+", " ", t or "").strip()) if s]


L = []
spec = json.load(open(os.path.join(A, "c5c2_decl_spec.json"), encoding="utf-8"))
spec.update(json.load(open(os.path.join(A, "c5c2_decl_spec2.json"), encoding="utf-8")))
nA = flagged = 0
L.append("== A. pass 6: sentences replaced on accepted advice")
for did in sorted(spec):
    v = spec[did]
    if not v.get("replace"):
        continue
    L.append("\n-- %s; accepted: %s" % (did, " | ".join("%s: %s" % (a["sentence"], a["line"])
                                                          for a in v.get("accepted", []))))
    for i, r in enumerate(v["replace"], 1):
        nA += 1
        o, n = r["old"], r["new"]
        f = len(MEM.findall(n)) > len(MEM.findall(o)) or len(ROOM.findall(n)) < len(ROOM.findall(o))
        flagged += f
        L.append("%s A%02d %s.%s\n   old: %s\n   new: %s" % ("*" if f else " ", nA, did, r["field"], o, n))

L.append("\n== B. passes 7 and 8: element and arrow changes, old and now")
elements = {r["id"]: r for r in jl("model/elements.jsonl")}
arrows = {r["id"]: r for r in jl("model/arrows.jsonl")}
for h in jl("model/history.jsonl"):
    if h.get("leg") not in ("C5c-03", "C5c-04"):
        continue
    w, now = h.get("was") or {}, elements.get(h["id"]) or arrows.get(h["id"]) or {}
    L.append("\n-- %s (%s): %s" % (h["id"], h["leg"], h.get("why", "")))
    for k in ("statement", "range", "mechanism"):
        if k in w and w.get(k) != now.get(k):
            L.append("   %s old: %s\n   %s now: %s" % (k, w.get(k), k, now.get(k)))

L.append("\n== C. the model as it stands: sentences naming members")
nC = 0
for eid, e in sorted(elements.items()):
    if e.get("status") != "standing":
        continue
    for k in ("statement", "range"):
        for s in sentences(e.get(k)):
            if MEM.search(s):
                nC += 1
                L.append("C%02d %s.%s: %s" % (nC, eid, k, s))
for aid, a in sorted(arrows.items()):
    if a.get("status") != "standing":
        continue
    for s in sentences(a.get("mechanism")):
        if MEM.search(s):
            nC += 1
            L.append("C%02d %s.mechanism: %s" % (nC, aid, s))
for p in jl("propositions.jsonl"):   # a proposition's mechanisms are carried from its arrows, read above
    for s in sentences(p.get("statement")):
        if MEM.search(s):
            nC += 1
            L.append("C%02d %s.statement: %s" % (nC, p["id"], s))

open(os.path.join(A, "c5c8_unit_sweep.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("A: %d sentences replaced at pass 6, %d flagged; C: %d model sentences naming members; written to "
      "c5c8_unit_sweep.txt (%d bytes)" % (nA, flagged, nC, len("\n".join(L).encode("utf-8"))))
