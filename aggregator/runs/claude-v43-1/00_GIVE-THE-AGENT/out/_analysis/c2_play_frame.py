#!/usr/bin/env python3
"""C2, pass 2: the play-frame test declared in notes-C2.md (pass 2, before any count). Read-only.

Rooms at held size (items_in_window 156 to 2,770). A room is frame-filled if the play frame (element K01) carries at
least half of its coded concepts before h32, and at least ten of them; the frame carries every coded concept on a
second-order theme whose first placed third-order theme is a play-frame theme (corrected after the first run). The comparison group is every other held room
with any canvas-work concept. The outcome is the hour of the room's first canvas-work concept: the first concept of the
starter (R01), a call (P01), the emblem (P02), building (P03) or the template (P04). The statement: frame-filled rooms
start the canvas work later. Test: the difference of the two groups' medians against 2,000 permutations of the group
labels (seed 20261014), one-sided at 0.05. The share of each group with no canvas concept before h32 is given beside.

    python3 out/_analysis/c2_play_frame.py
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p2.json"), encoding="utf-8"))["elements"])
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
byc = dict(((c["sub"], c["code_id"]), c) for c in codes)
q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", "items_in_window",
                    "--json", "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in q.stdout.splitlines() if l.startswith("{")))
held = set(s for s, v in items.items() if 156 <= v <= 2770)
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]
canvas_themes = set(t for k in ("R01", "P01", "P02", "P03", "P04") for t in els[k]["themes"])
frame_themes = set(els["K01"]["themes"])
frame_ids = collections.defaultdict(set)
canvas_hours = collections.defaultdict(list)
for r in rows:
    for t, ids in (r.get("support_by_theme") or {}).items():
        for i in ids:
            c = byc.get((r["sub"], i))
            if not c or c.get("hour") is None:
                continue
            if t in frame_themes:
                frame_ids[r["sub"]].add(i)
            if t in canvas_themes:
                canvas_hours[r["sub"]].append(c["hour"])
early_all = collections.Counter()
for c in codes:
    if c.get("hour") is not None and c["hour"] < 32:
        early_all[c["sub"]] += 1
# corrected rule (notes-C2.md, pass 2): the frame carries every coded concept on a frame line, a second-order theme
# whose first placed third-order theme is a play-frame theme; the first run counted only cited concepts
# (its output is c2_play_frame-p2.txt; this rule's output is c2_play_frame-p2b.txt)
frame_lines = set((r["sub"], r["theme_id"]) for r in rows if (r.get("third_order") or [None])[0] in frame_themes)
frame_early = collections.Counter(c["sub"] for c in codes if c.get("hour") is not None and c["hour"] < 32
                                  and (c["sub"], c.get("theme_id")) in frame_lines)
filled = sorted(s for s in held if frame_early.get(s, 0) >= 10 and early_all[s] and frame_early[s] / float(early_all[s]) >= 0.5)
others = sorted(s for s in held if s not in filled and canvas_hours.get(s))
fh = [min(canvas_hours[s]) for s in filled if canvas_hours.get(s)]
oh = [min(canvas_hours[s]) for s in others]


def med(x):
    x = sorted(x)
    n = len(x)
    return (x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2.0) if n else float("nan")


obs = med(fh) - med(oh)
pool = fh + oh
rnd = random.Random(20261014)
ge = 0
for _ in range(2000):
    rnd.shuffle(pool)
    if med(pool[:len(fh)]) - med(pool[len(fh):]) >= obs:
        ge += 1
pval = (ge + 1) / 2001.0
print("held rooms: %d; frame-filled: %d (with any canvas concept: %d); comparison rooms with a canvas concept: %d"
      % (len(held), len(filled), len(fh), len(oh)))
print("median first canvas-work hour: frame-filled h%.2f, others h%.2f; difference %.2f hours" % (med(fh), med(oh), obs))
print("one-sided permutation p (2,000 label permutations, seed 20261014): %.4f; grounded at 0.05: %s" % (pval, pval < 0.05))
print("no canvas concept before h32: frame-filled %d of %d (%.2f); others %d of %d (%.2f)" % (
    sum(1 for s in filled if not [h for h in canvas_hours.get(s, []) if h < 32]), len(filled),
    sum(1 for s in filled if not [h for h in canvas_hours.get(s, []) if h < 32]) / float(len(filled) or 1),
    sum(1 for s in others if not [h for h in canvas_hours[s] if h < 32]), len(others),
    sum(1 for s in others if not [h for h in canvas_hours[s] if h < 32]) / float(len(others) or 1)))
print("frame-filled rooms with no canvas concept at all: %s" % ", ".join(s for s in filled if not canvas_hours.get(s)))
print("frame-filled rooms: %s" % ", ".join("%s (h%.1f)" % (s, min(canvas_hours[s])) if canvas_hours.get(s) else s for s in filled))
