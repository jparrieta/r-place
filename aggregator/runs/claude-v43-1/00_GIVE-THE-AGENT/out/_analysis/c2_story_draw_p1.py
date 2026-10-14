#!/usr/bin/env python3
"""C2 section 5, pass 1: draw the rooms the story is read against, by the rule below, before any is opened, and write
the rule and the draw as the first line of out/story_rooms-p1.jsonl (a line with no `sub`; verdict lines are appended
one per room as each is read). Refuses to run if the file exists.

The rule, in the stage file's order:
1. the three within-case rooms (ubc, ultrahardcore, day9), every time;
2. rooms told-with-residue or not-told last pass: none, this is pass 1;
3. rooms whose form the story does not name: one room, drawn by seed, whose most-placed fourth-order theme (by
   placed lines in assignments_final.jsonl) is one the model does not use (in_model false in fourth.jsonl);
4. the contrast side the story has visited least: the late side (contrast.md), two rooms drawn by seed;
5. every sampled_against room marked fails in model/arrows.jsonl;
6. one room from each quartile of items_in_window over the 705 analysed rooms, drawn by seed;
7. one room drawn by seed from the rest.
Draws are made in that order with random.Random(20261014), each from its candidate list sorted by name, with every
room already drawn excluded. Rooms are drawn from facts and placements only, never from notes.

    python3 out/_analysis/c2_story_draw_p1.py
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "story_rooms-p1.jsonl")


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


if os.path.exists(DEST):
    sys.exit("out/story_rooms-p1.jsonl exists; not overwritten")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", "items_in_window",
                    "--json", "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
rooms = sorted(items)
contrast = open(os.path.join(OUT, "contrast.md"), encoding="utf-8").read()
late = set(x.strip() for x in contrast.split("## Members, late side (61)")[1].split("##")[0].replace("\n", " ").split(",") if x.strip())
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
out_of_model = set(r["id"] for r in t4 if not r.get("in_model"))
name4 = dict((r["id"], r["name"]) for r in t4)
per = collections.defaultdict(collections.Counter)
for r in jl("assignments_final.jsonl"):
    for t in set(owner[t] for t in (r.get("third_order") or []) if t in owner):
        per[r["sub"]][t] += 1
top = {}
for s, c in per.items():
    best = max(c.values())
    top[s] = sorted(t for t, n in c.items() if n == best)
arrows = jl(os.path.join("model", "arrows.jsonl"))
fails = sorted(set(x["sub"] for a in arrows for x in a.get("sampled_against", []) if x.get("found") == "fails"))
fail_why = collections.defaultdict(list)
for a in arrows:
    for x in a.get("sampled_against", []):
        if x.get("found") == "fails":
            fail_why[x["sub"]].append(a["id"])
order = sorted(rooms, key=lambda s: (items[s], s))
n = len(order)
quart = [order[i * n // 4:(i + 1) * n // 4] for i in range(4)]
rnd = random.Random(20261014)
drawn, why = [], {}


def take(sub, reason):
    drawn.append(sub)
    why[sub] = reason


for s in ("ubc", "ultrahardcore", "day9"):
    take(s, "within-case room, read every pass")
cand = sorted(s for s in rooms if s not in drawn and top.get(s) and all(t in out_of_model for t in top[s]))
s = rnd.choice(cand)
take(s, "form the story does not name: its most-placed fourth-order theme is %s, outside the model (%d candidates)"
     % (", ".join("%s %s" % (t, name4[t]) for t in top[s]), len(cand)))
for i in range(2):
    cand = sorted(x for x in late if x in items and x not in drawn)
    s = rnd.choice(cand)
    take(s, "late side of the onset contrast, the side the story visited least (%d candidates)" % len(cand))
for s in fails:
    if s not in drawn:
        take(s, "sampled_against room marked fails for %s" % ", ".join(fail_why[s]))
    else:
        why[s] += "; also sampled_against fails for %s" % ", ".join(fail_why[s])
for i, q in enumerate(quart):
    cand = sorted(x for x in q if x not in drawn)
    s = rnd.choice(cand)
    take(s, "items_in_window quartile %d (%d to %d items; %d candidates)" % (i + 1, items[q[0]], items[q[-1]], len(cand)))
cand = sorted(x for x in rooms if x not in drawn)
s = rnd.choice(cand)
take(s, "drawn by seed from the rest (%d candidates)" % len(cand))
rule = ("Pass 1 story rooms, drawn before any was opened by out/_analysis/c2_story_draw_p1.py with random.Random(20261014): "
        "the three within-case rooms; none told-with-residue or not-told last pass (pass 1); one room whose most-placed "
        "fourth-order theme lies outside the model; two late-side rooms (the side the story visited least); every "
        "sampled_against room marked fails; one room per quartile of items_in_window over the 705 analysed rooms; one "
        "room by seed from the rest. Each room is read whole (mem.py room --no-canvas, then its forest) and its verdict "
        "appended as one line.")
line = {"pass": 1, "rule": rule, "seed": 20261014, "quartile_bounds": [[items[q[0]], items[q[-1]]] for q in quart],
        "draw": [{"sub": s, "items_in_window": items[s], "side": "late" if s in late else "early-or-unsided",
                  "why_drawn": why[s]} for s in drawn]}
line["draw_count"] = len(drawn)
with open(DEST, "w", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print(rule)
for d in line["draw"]:
    print("%s | %s items | %s | %s" % (d["sub"], d["items_in_window"], d["side"], d["why_drawn"]))
print("rooms drawn: %d" % len(drawn))
