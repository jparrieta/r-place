"""Figures for one B1 leg's stretch-end line: rooms placed, second-order themes placed,
placements, new kinds, rule 0 lines and bags, and episode lines written or edited in the leg.

usage: python3 out/_analysis/b1_leg_figures.py <leg>
"""
import json
import sys
from collections import Counter

leg = sys.argv[1]


def lines(path):
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            yield json.loads(line)


placed = [k for k in lines("out/kinds-B1.jsonl") if k.get("leg") == leg and k.get("event") == "placed"]
minted = [k for k in lines("out/kinds-B1.jsonl") if k.get("leg") == leg and k.get("event") != "placed"]
themes = {(k["sub"], k.get("second_order") or k.get("theme_id")) for k in placed}
rooms = Counter(k["sub"] for k in placed)
print("rooms with placements: %d" % len(rooms))
print("placement events: %d" % len(placed))
print("non-placement events: %s" % Counter(k.get("event") for k in minted))
print("keys of a placement event: %s" % sorted(placed[0].keys()) if placed else "none")

mp = [m for m in lines("out/multiplacement_log.jsonl") if m.get("leg") == leg]
bags = [m for m in mp if m.get("item_is_a_bag")]
print("rule 0 lines: %d; bags: %d" % (len(mp) - len(bags), len(bags)))

eps = list(lines("out/episodes-B1.jsonl"))
new = [e["episode"] for e in eps if e.get("leg") == leg]
edited = [e["episode"] for e in eps if e.get("leg") != leg and ("at %s" % leg) in json.dumps(e)]
print("episode lines written: %d (%s to %s)" % (len(new), new[0] if new else "-", new[-1] if new else "-"))
print("episode lines edited: %s" % ", ".join(edited))

disc = [d for d in lines("out/theme_discovery.jsonl") if d.get("leg") == leg]
print("kinds minted: %s" % ", ".join("%s %s (%s)" % (d["theme"], d["label"], d["trigger"]) for d in disc))
