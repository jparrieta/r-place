#!/usr/bin/env python3
"""D3c: cannot-tell rooms by threshold, by version. A room's verdict is my ruling where I ruled it (D3a-56 for the
first return, G62 for the re-check), else the readers' agreed verdict; its threshold is the ruling's
cannot_tell_under, else the readers' (both named, or the one named). Prints the counts and the rooms. Read-only.

    python3 out/_analysis/d3c_ct_thresholds.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


vr = jl(os.path.join(OUT, "verdicts-D.jsonl"))
for name, rows, rec in (("first return (e15f9647)", vr, False),
                        ("re-check (46384686)", jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")), True)):
    ruled = {r["sub"]: r for r in vr if r.get("ruled_by") == "analyst" and bool(r.get("recheck")) == rec}
    c, rooms = collections.Counter(), collections.defaultdict(list)
    for r in rows:
        if r.get("ruled_by"):
            continue
        s = r["sub"]
        if s in ruled:
            v, t = ruled[s]["verdict"], ruled[s].get("cannot_tell_under")
        else:
            vs = {e["verdict"] for e in r["readers"]}
            if len(vs) != 1:
                continue
            v = vs.pop()
            ts = sorted({str(e.get("cannot_tell_under")) for e in r["readers"]})
            t = "/".join(ts)
        if v == "cannot-tell":
            c[t] += 1
            rooms[t].append(s + (" (ruled)" if s in ruled else ""))
    print("== %s: %s" % (name, dict(c)))
    for t, rs in rooms.items():
        print("   %s: %s" % (t, ", ".join(sorted(rs, key=str.lower))))
