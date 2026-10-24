#!/usr/bin/env python3
"""D3c: the labelers' local status and grade, from both sources: adaptation-returns.jsonl (the ingest's index;
the last line per room and phase) and rooms/<sub>/model-D*.md (the account's own lines). Prints the counts by
phase and source, and the rooms where the two sources differ. Read-only.

    python3 out/_analysis/d3c_local_grades.py
"""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rows = [json.loads(l) for l in open(os.path.join(OUT, "adaptation-returns.jsonl"), encoding="utf-8") if l.strip()]
print("phases and status:", collections.Counter((r.get("phase"), r.get("status"), (r.get("model_version") or "")[:8])
                                                 for r in rows))
lastp = {}
for r in rows:
    lastp[(r["sub"], r.get("phase"))] = r
for ph in sorted({k[1] for k in lastp}, key=str):
    rs = [r for k, r in lastp.items() if k[1] == ph]
    print("index, phase %s: %d rooms; local_status %s; local_grade %s" % (
        ph, len(rs), dict(collections.Counter(r.get("local_status") for r in rs)),
        dict(collections.Counter(r.get("local_grade") for r in rs))))
for ph, fn in (("first", "model-D.md"), ("recheck", "model-D-recheck.md")):
    st, gr = collections.Counter(), collections.Counter()
    diff = []
    for s in sorted(os.listdir(os.path.join(OUT, "rooms"))):
        p = os.path.join(OUT, "rooms", s, fn)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        m = re.search(r"^local_status:\s*(\S+)", t, re.M)
        g = re.search(r"^grade:\s*([a-z-]+)", t, re.M)
        st[m.group(1) if m else None] += 1
        gr[g.group(1) if g else None] += 1
        idx = [r for k, r in lastp.items() if k[0] == s and (k[1] or "").startswith(ph[:5])]
        if idx and g and idx[-1].get("local_grade") != g.group(1):
            diff.append((s, idx[-1].get("local_grade"), g.group(1)))
    print("accounts %s: local_status %s; grade %s; index differs in %d: %s" % (
        fn, dict(st), dict(gr), len(diff), diff[:12]))
