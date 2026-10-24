#!/usr/bin/env python3
"""D3c, for 'Re-read against the amendments': every model/history.jsonl line and tier_history.jsonl line written at
stage D3, in order (line number, id, field, leg, move, the head of the event); the diary's move lines at D3 (number
and head); and, for each element or arrow id the D3 lines touch, its mentions in account.md, figure-C5.md and
data_structure-C5.md, with whether each document carries the start of the history line's 'was' or 'now' text for a
statement, range, connection or bound. Read-only.

    python3 out/_analysis/d3c_amendments.py
"""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


docs = {n: open(os.path.join(OUT, n), encoding="utf-8").read() for n in ("account.md", "figure-C5.md",
                                                                         "data_structure-C5.md")}
H = jl(os.path.join(OUT, "model", "history.jsonl"))
touched = collections.OrderedDict()
print("== history.jsonl lines at D3")
for n, h in enumerate(H, 1):
    if h.get("stage") != "D3":
        continue
    print("%d | %s | %s | %s | %s | %s" % (n, h.get("id"), h.get("field"), h.get("leg"), h.get("move"),
                                            (h.get("event") or "")[:150]))
    touched.setdefault(h.get("id"), []).append(n)
print("== tier_history.jsonl lines at D3")
for n, t in enumerate(jl(os.path.join(OUT, "tier_history.jsonl")), 1):
    if str(t.get("stage") or "").startswith("D3") or str(t.get("leg") or "").startswith("D3"):
        print("%d | %s" % (n, json.dumps(t, ensure_ascii=False)[:260]))
print("== mentions of each touched id")
for i, lines in touched.items():
    pat = re.compile(r"\b%s\b" % re.escape(i or "?"))
    cnt = {n: len(pat.findall(t)) for n, t in docs.items()}
    carry = []
    for n in lines:
        h = H[n - 1]
        if h.get("field") in ("statement", "range", "connection", "bound", "mechanism"):
            for side in ("was", "now"):
                v = h.get(side)
                if isinstance(v, str) and len(v) > 30:
                    probe = v[:40]
                    hits = [d for d, t in docs.items() if probe in t]
                    carry.append("line %d %s %s: %s" % (n, h.get("field"), side, ", ".join(hits) or "in none"))
    print("%s (lines %s): %s | %s" % (i, ",".join(map(str, lines)), cnt, "; ".join(carry)))
