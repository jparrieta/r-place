#!/usr/bin/env python3
"""C2 section 4, read-only: draw the three within-case rooms by the rules written in notes-C2.md, before any is read.

All three come from the middle half of rooms by items_in_window (156 to 2770, the held-size band of contrast.md), so
size does not pick them. Each is drawn with random.Random(20261014) from its candidate list, sorted by name.
- ordinary: the room's placements reach all four of the most widely reached fourth-order themes (Repair work,
  Completion ritual, Mobilization, Collective representation), and its organizing_end_hour (A1) lies inside the
  corpus's interquartile range.
- unpredicted: the share of the room's placed lines carrying a third-order theme placed in fewer than ten rooms is in
  the top tenth of the band; such a room's form rests on kinds the scheme holds only thinly.
- stopped early: organizing_end_hour before hour 24 with at least five coordinating turns (A1), so there was
  organizing to stop.

    python3 out/_analysis/c2_within_case_pick.py
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", "items_in_window",
                    "--json", "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
band = sorted(s for s, v in items.items() if 156 <= v <= 2770)
end = dict((r["sub"], r) for r in jl("organizing_end-A1.jsonl"))
rows = jl("assignments_final.jsonl")
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
rooms_of = collections.defaultdict(set)
for r in rows:
    for t in r.get("third_order") or []:
        rooms_of[t].add(r["sub"])
sparse = set(t for t, s in rooms_of.items() if len(s) < 10)
reach = collections.defaultdict(set)
lines, sparse_lines = collections.Counter(), collections.Counter()
for r in rows:
    th = r.get("third_order") or []
    if th:
        lines[r["sub"]] += 1
        if set(th) & sparse:
            sparse_lines[r["sub"]] += 1
    for t in th:
        if t in owner:
            reach[r["sub"]].add(owner[t])
spine = {"T4-013", "T4-026", "T4-005", "T4-006"}
ends = sorted(e["organizing_end_hour"] for e in end.values() if e.get("organizing_end_hour") is not None)
q1, q3 = ends[len(ends) // 4], ends[3 * len(ends) // 4]
ordinary = [s for s in band if spine <= reach[s] and end.get(s, {}).get("organizing_end_hour") is not None
            and q1 <= end[s]["organizing_end_hour"] <= q3]
share = dict((s, sparse_lines[s] / float(lines[s])) for s in band if lines[s])
cut = sorted(share.values())[int(0.9 * len(share))]
unpredicted = [s for s in band if share.get(s, 0) >= cut and share.get(s, 0) > 0]
# first rule (end before hour 24) found no room in the band; restated before any room was read: the lowest tenth
d10 = ends[len(ends) // 10]
early = [s for s in band if end.get(s, {}).get("organizing_end_hour") is not None
         and end[s]["organizing_end_hour"] <= d10 and (end[s].get("coordinating_turns") or 0) >= 5]
print("organizing end, lowest tenth of 705 rooms: at or before h%.2f" % d10)
rnd = random.Random(20261014)
print("band (items_in_window 156 to 2770): %d rooms; organizing end IQR %.2f to %.2f; themes in fewer than ten rooms: %d"
      % (len(band), q1, q3, len(sparse)))
for name, cand in (("ordinary", ordinary), ("unpredicted", unpredicted), ("stopped early", early)):
    pick = rnd.choice(cand) if cand else None
    print("%s: %d candidates; drawn: %s" % (name, len(cand), pick))
    if pick:
        e = end.get(pick, {})
        print("   items %s; lines placed %d, on sparse themes %d; fourth-order reach %d; end h%s, coordinating turns %s, work %s"
              % (items[pick], lines[pick], sparse_lines[pick], len(reach[pick]), e.get("organizing_end_hour"),
                 e.get("coordinating_turns"), e.get("work_remained")))
