#!/usr/bin/env python3
"""D4a-07: what the selected arrow lines and link-op lines hold, before the arrow mapping is fixed. Read-only.

    python3 out/_analysis/d4a07_explore.py
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CH = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in al.shared_lines(OUT) if r.get("op") in CH and len(r.get("lift") or []) >= 4]
arrows = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"))}
el = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(OUT, "model", "elements.jsonl"))}
A = [r for r in L if r["element"] in arrows]
E = [r for r in L if r["element"] not in arrows]
print("selected lines", len(L), "on arrows", len(A), "on elements", len(E))
print("arrow lines by op", collections.Counter(r["op"] for r in A))
print("element lines by op", collections.Counter(r["op"] for r in E))
print("restrict share of all selected", round(sum(1 for r in L if r["op"] == "restrict") / len(L), 3),
      "restrict on arrows", sum(1 for r in A if r["op"] == "restrict"), "on elements", sum(1 for r in E if r["op"] == "restrict"))
print("fields of an arrow line:", sorted(A[0].keys()))
print("relation field on arrow lines:", collections.Counter(type(r.get("relation")).__name__ for r in A))
lk = [r for r in E if r["op"] == "link"]
print("link-op lines", len(lk), "relation types", collections.Counter(type(r.get("relation")).__name__ for r in lk))
for r in lk[:4]:
    print("  link example:", {k: r.get(k) for k in ("sub", "element", "lift", "relation", "condition", "statement")}, "|", (r.get("how") or "")[:160])
# where does an arrow line's evidence sit relative to the arrow's two elements?
t4of3 = {}
for f in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"))):
    for m in f.get("members") or []:
        t4of3[m] = f["id"]


def anchors_t4(eid):
    out = set()
    for n in el.get(eid, {}).get("tier") or []:
        if n.startswith("T4-"):
            out.add(n)
        elif n.startswith("T3-") and n in t4of3:
            out.add(t4of3[n])
    return out


pos = collections.Counter()
for r in A:
    a = arrows[r["element"]]
    t4 = r["lift"][2]
    s, t = anchors_t4(a["from"]), anchors_t4(a["to"])
    pos["evidence under source" if t4 in s else "evidence under target" if t4 in t else "evidence elsewhere"] += 1
print("arrow lines, where the evidence theme sits:", dict(pos))
print("arrow ends without a fourth-order anchor:", sorted({e for a in arrows.values() for e in (a["from"], a["to"]) if not anchors_t4(e)}))
