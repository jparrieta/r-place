#!/usr/bin/env python3
"""C5b: draw the three readers' rooms (stage C5 section 8) by the revised rule logged before the draw, and write the
rooms page. Supersedes c5b_rooms_draw.py, whose whole-room cap left pools 1 and 2 empty. No room note is read.

Pools (from out/_analysis/c5b_room_sizes.json, written by c5b_room_sizes.py):
  1 reached easily   pass 5 story room told with no residue, not cited or named in account.md, >= 8 coded passages
  2 not told         pass 5 story room told with a residue (none was untold)
  3 late side        first coded turn after hour 48, not cited or named in account.md, not a story room,
                     >= 8 coded passages
One room per pool, drawn with random.Random(SEED), pool by pool in that order. Each room is served as the facts
lines of `mem.py room <sub> --no-canvas` (above its thread list) and K coded passages drawn by cite.py's own seeded
draw (`--grep . --room <sub> --n K --seed SEED`), verbatim with their citations. The forest is not served.

    python3 out/_analysis/c5b_rooms_draw2.py            print the pools, the draw and the page size
    python3 out/_analysis/c5b_rooms_draw2.py --write    also write out/_analysis/c5b/rooms.md
"""
import json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SEED = 20261015
FLOOR = 8
K = 7   # 10 at first; 7 after the first size report (logged), so the packets fit the ceiling
sz = json.load(open(os.path.join(OUT, "_analysis", "c5b_room_sizes.json")))
facts = {}
for l in open(os.path.join(ROOT, "package", "store", "rooms.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        facts[r["sub"]] = r


def run(args):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=ROOT)
    return "\n".join(x for x in p.stdout.splitlines() if not x.startswith("[end"))


def ncodes(sub):
    c = facts.get(sub, {}).get("codes")
    return len(c) if isinstance(c, (list, dict)) else (c or 0)


def page(sub):
    room = run([os.path.join(ROOT, "tools", "mem.py"), "room", sub, "--no-canvas"])
    head = room.split("\nthreads (")[0].rstrip()
    # the forest is not served, so its summary line is left out; every other facts line is whole
    head = "\n".join(x for x in head.splitlines() if not x.startswith("forest:"))
    words = run([os.path.join(ROOT, "tools", "cite.py"), "--grep", ".", "--room", sub, "--n", str(K),
                 "--seed", str(SEED)]).rstrip()
    return ("### r/%s\n\nFacts (`mem.py room %s --no-canvas`):\n\n```\n%s\n```\n\n"
            "Passages (`cite.py --grep . --room %s --n %d --seed %d`):\n\n```\n%s\n```\n"
            % (sub, sub, head, sub, K, SEED, words))


rows = sz["rows"]
pools = {
    1: sorted(r["sub"] for r in rows if r["story"] == "told" and not r["in_account"] and ncodes(r["sub"]) >= FLOOR),
    2: sorted(r["sub"] for r in rows if r["story"] == "told-with-residue"),
    3: sorted(r["sub"] for r in rows if r["side"] == "late" and not r["in_account"] and not r["story"]
              and ncodes(r["sub"]) >= FLOOR),
}
rng = random.Random(SEED)
drawn = {}
for k in (1, 2, 3):
    drawn[k] = rng.choice(pools[k])
    print("pool %d: %d rooms; drawn %s (%d coded passages)" % (k, len(pools[k]), drawn[k], ncodes(drawn[k])))
pages = {k: page(drawn[k]) for k in (1, 2, 3)}
L = ["# The three rooms", "",
     "Every reader gets these three rooms. Each is shown by its facts and %d of its coded passages, drawn at random "
     "by the run's quoting tool, not chosen by the analyst: a sample of the room's record, not the whole of it. Each "
     "passage carries its citation, thread, hour, author and the coder's theme. The canvas is withheld. Hours run "
     "from the canvas's opening; placement ended at hour 73." % K, ""]
for k in (1, 2, 3):
    L += [pages[k], ""]
text = "\n".join(L)
print("rooms page: %d bytes" % len(text.encode("utf-8")))
if "--write" in sys.argv:
    # the 10-passage page stays as c5b/rooms.md; the served page is c5b/shared/rooms.md
    os.makedirs(os.path.join(OUT, "_analysis", "c5b", "shared"), exist_ok=True)
    p = os.path.join(OUT, "_analysis", "c5b", "shared", "rooms.md")
    open(p, "w", encoding="utf-8").write(text)
    json.dump({"seed": SEED, "floor": FLOOR, "k": K, "drawn": drawn, "pools": pools},
              open(os.path.join(OUT, "_analysis", "c5b_rooms_draw2-k%d.json" % K), "w"), indent=1)
    print("wrote %s" % p)
