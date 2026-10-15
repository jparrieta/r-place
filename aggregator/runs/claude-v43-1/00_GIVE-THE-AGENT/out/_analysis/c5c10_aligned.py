#!/usr/bin/env python3
"""C5c-10, problem 4, 'aligned' (rule logged first, diary C5c-10, abductive): of the rooms carrying calls for hands
(P01), how many carry a report that the work is up (P11, 'When a work is up, the room marks it'), and in how many the
first such report comes after the first call. Cited concepts by hour, as in the order tests (c2_first_concepts.py,
c2_elements_c5c2.json, assignments_final.jsonl). Also by room-size quartile (items_in_window), since a room that writes
more carries more elements. The record, never the canvas. Writes nothing.

    python3 out/_analysis/c5c10_aligned.py
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
els = {e["id"]: e for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json")))["elements"]}
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = {(c["sub"], c["code_id"]): c for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{"))}
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]
rooms = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}


def first(eid):
    out = {}
    themes = set(els[eid]["themes"])
    for r in rows:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in themes:
                for i in ids:
                    c = codes.get((r["sub"], i))
                    if c and c.get("hour") is not None:
                        out[r["sub"]] = min(out.get(r["sub"], 1e9), c["hour"])
    return out


calls, up = first("P01"), first("P11")
both = set(calls) & set(up)
after = {s for s in both if calls[s] < up[s]}
n = len(calls)
print("rooms with calls (P01): %d of 705" % n)
print("  of these, a report that the work is up (P11): %d (%.3f); the first report after the first call: %d (%.3f)" % (
    len(both), len(both) / n, len(after), len(after) / n))
sizes = sorted((rooms[s].get("items_in_window") or 0) for s in rooms)
cut = [sizes[len(sizes) * k // 4] for k in (1, 2, 3)]
q = lambda s: sum((rooms.get(s, {}).get("items_in_window") or 0) >= c for c in cut)
for k in range(4):
    cs = [s for s in calls if q(s) == k]
    a = [s for s in cs if s in after]
    print("  size quartile %d: rooms with calls %d, report after the first call %d (%.3f)" % (
        k + 1, len(cs), len(a), len(a) / len(cs) if cs else 0))
