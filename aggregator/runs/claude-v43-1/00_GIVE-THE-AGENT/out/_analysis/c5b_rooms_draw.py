#!/usr/bin/env python3
"""C5b: draw the three readers' rooms (stage C5 section 8) by the rule logged before the draw, and write each drawn
room's page as the verbs serve it: the facts lines of `mem.py room <sub> --no-canvas` (above its thread list), the
whole `mem.py forest <sub>`, and every quote of the room by `cite.py --grep . --room <sub>`. No room note is read.

Pools (from out/_analysis/c5b_room_sizes.json, written by c5b_room_sizes.py):
  1 reached easily   pass 5 story room told with no residue, not cited or named in account.md, >= 8 coded concepts
  2 not told         pass 5 story room told with a residue (none was untold)
  3 late side        first coded turn after hour 48, not cited or named in account.md, not a story room,
                     >= 8 coded concepts
Each pool is cut to rooms whose served material is at most CAP bytes; one room per pool is drawn with
random.Random(SEED), pool by pool in the order above.

    python3 out/_analysis/c5b_rooms_draw.py            print the pools and the draw
    python3 out/_analysis/c5b_rooms_draw.py --write    also write out/_analysis/c5b/rooms.md
"""
import json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
CAP = 4500
SEED = 20261015
FLOOR = 8
sz = json.load(open(os.path.join(OUT, "_analysis", "c5b_room_sizes.json")))
facts = {}
for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        facts[r["sub"]] = r


def run(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=ROOT)
    return "\n".join(x for x in p.stdout.splitlines() if not x.startswith("[end"))


def page(sub):
    room = run([os.path.join(ROOT, "tools", "mem.py"), "room", sub, "--no-canvas"])
    head = room.split("\nthreads (")[0].rstrip()
    forest = run([os.path.join(ROOT, "tools", "mem.py"), "forest", sub]).rstrip()
    words = run([os.path.join(ROOT, "tools", "cite.py"), "--grep", ".", "--room", sub, "--n", "1000"]).rstrip()
    return ("### r/%s\n\n**The room's facts** (`mem.py room %s --no-canvas`, above its thread list):\n\n```\n%s\n```\n\n"
            "**The forest** (`mem.py forest %s`): the threads, who replied to whom, and the coders' labels.\n\n```\n%s\n```"
            "\n\n**The members' words** (`cite.py --grep . --room %s`): every coded passage, verbatim.\n\n```\n%s\n```\n"
            % (sub, sub, head, sub, forest, sub, words))


def ncodes(sub):
    c = facts.get(sub, {}).get("codes")
    return len(c) if isinstance(c, (list, dict)) else (c or 0)


rows = sz["rows"]
pools = {
    1: [r["sub"] for r in rows if r["story"] == "told" and not r["in_account"] and ncodes(r["sub"]) >= FLOOR],
    2: [r["sub"] for r in rows if r["story"] == "told-with-residue"],
    3: [r["sub"] for r in rows if r["side"] == "late" and not r["in_account"] and not r["story"]
        and ncodes(r["sub"]) >= FLOOR],
}
rng = random.Random(SEED)
drawn, pages = {}, {}
for k in (1, 2, 3):
    fit = []
    for s in sorted(pools[k]):
        fb = next(r["forest_bytes"] for r in rows if r["sub"] == s) or 0
        if fb > CAP:
            continue
        pg = page(s)
        if len(pg.encode("utf-8")) <= CAP:
            fit.append(s)
            pages[s] = pg
    print("pool %d: %d rooms, %d fit under %d bytes: %s" % (k, len(pools[k]), len(fit), CAP, ", ".join(
        "%s (%d codes, %d bytes)" % (s, ncodes(s), len(pages[s].encode("utf-8"))) for s in fit)))
    drawn[k] = rng.choice(fit) if fit else None
    print("  drawn: %s" % drawn[k])
if "--write" in sys.argv:
    # the reader is not told which pool a room came from, so that the pool does not steer the reading
    L = ["# The three rooms", "",
         "The same three rooms go to every reader. Each is served whole through the run's read verbs. The canvas is "
         "withheld (`--no-canvas`). Hours run from the canvas's opening; placement ended at hour 73.", ""]
    for k in (1, 2, 3):
        L += [pages[drawn[k]], ""]
    os.makedirs(os.path.join(OUT, "_analysis", "c5b"), exist_ok=True)
    p = os.path.join(OUT, "_analysis", "c5b", "rooms.md")
    open(p, "w", encoding="utf-8").write("\n".join(L))
    json.dump({"seed": SEED, "cap": CAP, "floor": FLOOR, "drawn": drawn, "pools": pools},
              open(os.path.join(OUT, "_analysis", "c5b_rooms_draw.json"), "w"), indent=1)
    print("wrote %s, %d bytes" % (p, os.path.getsize(p)))
