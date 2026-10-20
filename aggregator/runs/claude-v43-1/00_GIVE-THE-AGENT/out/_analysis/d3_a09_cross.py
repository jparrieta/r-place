#!/usr/bin/env python3
"""D3a-36, G41 reading 1: for a room whose A09 line shows carrying on before any record, list the room's earlier
records in lines already ruled (A08's and P12's, every op but absent): each cited concept quoted whole through
cite.py, with the line's id, op and last decision, where its hour is before the given hour. Later concepts are
only counted. Writes nothing.

    python3 out/_analysis/d3_a09_cross.py Temple:74.51 anime:74.65
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
lines = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") in ("A08", "P12")
         and l.get("op") != "absent"]
for arg in sys.argv[1:]:
    room, h = arg.rsplit(":", 1)
    h = float(h)
    mine = sorted((l for l in lines if l.get("sub") == room), key=lambda l: l["id"])
    seen, early, late = set(), [], 0
    for l in mine:
        d = adj.get(l["id"], {}).get("decision", "unruled")
        for c in (l.get("evidence") or {}).get("codes", []):
            code = c.split(":")[-1]
            if code in seen:
                continue
            seen.add(code)
            r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                               cwd=ROOT, capture_output=True, text=True)
            q = [x for x in r.stdout.splitlines() if x.strip()]
            q = q[0] if q else "(no quote) %s/%s" % (room, code)
            m = re.search(r"\bh\+(\d+(?:\.\d+)?)", q)
            hh = float(m.group(1)) if m else None
            if hh is not None and hh < h:
                early.append((hh, "%s %s %s %s: %s" % (l["id"], l["element"], l["op"], d, q)))
            else:
                late += 1
    print("== %s, before h+%.2f: %d of %d concepts in %d A08 and P12 lines (%s)" % (
        room, h, len(early), len(seen), len(mine), ", ".join(l["id"] for l in mine) or "none"))
    for hh, s in sorted(early):
        print("   " + s)
