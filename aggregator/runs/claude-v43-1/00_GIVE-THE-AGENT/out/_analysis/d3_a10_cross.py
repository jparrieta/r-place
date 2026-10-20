#!/usr/bin/env python3
"""D3a-37, G42's two-way check across lines: for a room and an hour, list the room's accepted lines of K02 and P10
(every op but absent), each with the head of its reason, and every cited concept of those lines whose hour is before
the given hour, quoted whole through cite.py. For a line showing a move first, the given hour is its first move,
and an earlier K02 concept would show the order; for a line showing the order, the given hour is its first doubt,
and an earlier P10 concept would show the move first. Later concepts are only counted. Writes nothing.

    python3 out/_analysis/d3_a10_cross.py korea:25.50 KState:54.69
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


adj = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    adj[r.get("adaptation")] = r
lines = [l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l.get("element") in ("K02", "P10")
         and l.get("op") != "absent"]
for arg in sys.argv[1:]:
    room, h = arg.rsplit(":", 1)
    h = float(h)
    mine = sorted((l for l in lines if l.get("sub") == room and adj.get(l["id"], {}).get("decision") == "accept"),
                  key=lambda l: l["id"])
    print("== %s, before h+%.2f: %d accepted K02 and P10 lines" % (room, h, len(mine)))
    for l in mine:
        print("   %s %s %s: %s" % (l["id"], l["element"], l["op"], adj[l["id"]]["reason"][:240]))
        late = 0
        for c in (l.get("evidence") or {}).get("codes", []):
            code = c.split(":")[-1]
            r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                               cwd=ROOT, capture_output=True, text=True)
            q = [x for x in r.stdout.splitlines() if x.strip()]
            q = q[0] if q else "(no quote) %s/%s" % (room, code)
            m = re.search(r"\bh\+(\d+(?:\.\d+)?)", q)
            if m and float(m.group(1)) < h:
                print("      " + q)
            else:
                late += 1
        print("      (%d concepts at or after h+%.2f)" % (late, h))
