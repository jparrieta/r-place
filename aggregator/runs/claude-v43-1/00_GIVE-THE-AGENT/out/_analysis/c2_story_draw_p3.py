#!/usr/bin/env python3
"""C2 section 5, pass 3: draw the rooms the pass 3 story is read against, by the rule declared in notes-C2.md (pass 3)
before any is opened, and write the rule and the draw as the first line of out/story_rooms-p3.jsonl (verdict lines are
appended one per room as it is read, by c2_story_verdict.py --pass 3). Refuses to run if the file exists.

The rule, in the stage file's order:
1. the three within-case rooms (ubc, ultrahardcore, day9), every time;
2. every room told-with-residue or not-told at pass 2 (story_rooms-p2.jsonl): eighteen;
3. rooms whose form the story does not name: one room, drawn by seed, whose most-placed fourth-order theme (by placed
   lines in assignments_final.jsonl) is one the model does not use (in_model false in fourth.jsonl, as set at pass 3);
4. rooms the canvas may have founded: two rooms drawn by seed from those with an empty pre-event brief
   (c2_empty_brief-p3.json);
5. the contrast side the story has visited least: the late side, two rooms drawn by seed;
6. every sampled_against room marked fails in a pass 3 arrow of model/arrows.jsonl;
7. one room from each quartile of items_in_window over the 705 analysed rooms, drawn by seed;
8. two rooms drawn by seed from the rest.
Apart from 1 and 2, no room drawn at pass 1 or pass 2 is drawn again. Draws are made in that order with
random.Random(20261017) (pass 1 used 20261014, pass 2 20261016), each from its candidate list sorted by name, with every
room already drawn excluded. Rooms are drawn from facts, placements and ledgers only, never notes.

    python3 out/_analysis/c2_story_draw_p3.py
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "story_rooms-p3.jsonl")
SEED = 20261017


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


if os.path.exists(DEST):
    sys.exit("out/story_rooms-p3.jsonl exists; not overwritten")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", "items_in_window",
                    "--json", "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
if len(items) != 705:
    sys.exit("expected 705 rooms from facts, got %d" % len(items))
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
p1, p2 = jl("story_rooms-p1.jsonl"), jl("story_rooms-p2.jsonl")
read_before = set(d["sub"] for d in p1[0]["draw"]) | set(d["sub"] for d in p2[0]["draw"])
residue = sorted(r["sub"] for r in p2[1:] if r.get("sub") and r.get("verdict") in ("told-with-residue", "not-told"))
empty = set(json.load(open(os.path.join(OUT, "_analysis", "c2_empty_brief-p3.json"), encoding="utf-8"))["empty"])
arrows = jl(os.path.join("model", "arrows.jsonl"))
fail_why = collections.defaultdict(list)
for a in arrows:
    if a.get("since") != "C2-pass-3":
        continue
    for x in a.get("sampled_against", []):
        if x.get("found") == "fails":
            fail_why[x["sub"]].append(a["id"])
order = sorted(rooms, key=lambda s: (items[s], s))
n = len(order)
quart = [order[i * n // 4:(i + 1) * n // 4] for i in range(4)]
rnd = random.Random(SEED)
drawn, why = [], {}


def take(sub, reason):
    drawn.append(sub)
    why[sub] = reason


def fresh(x):
    return x not in drawn and x not in read_before


for s in ("ubc", "ultrahardcore", "day9"):
    take(s, "within-case room, read every pass")
for s in residue:
    if s not in drawn:
        take(s, "told-with-residue at pass 2")
    else:
        why[s] += "; told-with-residue at pass 2"
cand = sorted(s for s in rooms if fresh(s) and top.get(s) and all(t in out_of_model for t in top[s]))
s = rnd.choice(cand)
take(s, "form the story does not name: its most-placed fourth-order theme is %s, outside the model (%d candidates)"
     % (", ".join("%s %s" % (t, name4[t]) for t in top[s]), len(cand)))
for i in range(2):
    cand = sorted(x for x in empty if x in items and fresh(x))
    s = rnd.choice(cand)
    take(s, "empty pre-event brief: a room the canvas may have founded (%d candidates)" % len(cand))
for i in range(2):
    cand = sorted(x for x in late if x in items and fresh(x))
    s = rnd.choice(cand)
    take(s, "late side of the onset contrast, the side the story visited least (%d candidates)" % len(cand))
for s in sorted(fail_why):
    if fresh(s):
        take(s, "sampled_against room marked fails for %s" % ", ".join(fail_why[s]))
for i, q in enumerate(quart):
    cand = sorted(x for x in q if fresh(x))
    s = rnd.choice(cand)
    take(s, "items_in_window quartile %d (%d to %d items; %d candidates)" % (i + 1, items[q[0]], items[q[-1]], len(cand)))
for i in range(2):
    cand = sorted(x for x in rooms if fresh(x))
    s = rnd.choice(cand)
    take(s, "drawn by seed from the rest (%d candidates)" % len(cand))
rule = ("Pass 3 story rooms, drawn before any was opened by out/_analysis/c2_story_draw_p3.py with random.Random(20261017), "
        "by the rule declared in notes-C2.md (pass 3): the three within-case rooms; every room told-with-residue or "
        "not-told at pass 2 (eighteen); one room whose most-placed fourth-order theme lies outside the model; two rooms "
        "with an empty pre-event brief; two late-side rooms; every room marked fails in a pass 3 arrow's sampled_against "
        "(%d); one room per quartile of items_in_window over the 705 analysed rooms; two rooms by seed from the rest. "
        "Apart from the within-case and residue rooms, no room drawn at pass 1 or 2 is drawn again. Each room is read "
        "whole (mem.py room --no-canvas, then its forest) against model/story-p3.md and its verdict appended as one line."
        % len(fail_why))
line = {"pass": 3, "rule": rule, "seed": SEED, "quartile_bounds": [[items[q[0]], items[q[-1]]] for q in quart],
        "draw": [{"sub": s, "items_in_window": items[s], "side": "late" if s in late else "early-or-unsided",
                  "empty_brief": s in empty, "why_drawn": why[s]} for s in drawn], "draw_count": len(drawn)}
with open(DEST, "w", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print(rule)
for d in line["draw"]:
    print("%s | %s items | %s | empty brief %s | %s" % (d["sub"], d["items_in_window"], d["side"], d["empty_brief"], d["why_drawn"]))
print("rooms drawn: %d" % len(drawn))
