#!/usr/bin/env python3
"""C2 section 5: append one line per pass to out/saturation.jsonl, with the story's number, the rooms read against it
and the three counts by name, computed from out/story_rooms-pN.jsonl. Also records what the stopping rule watches for
the pass: tier_history events of stage C2, arrows in model/arrows.jsonl, and whether the story changed. Refuses to
write a second line for a pass already present.

    python3 out/_analysis/c2_saturation_line.py --pass 1 --story-changed "first story" --tier-events 35 --arrows-changed 12
"""
import argparse, collections, json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="pas", type=int, required=True)
ap.add_argument("--story-changed", required=True)
ap.add_argument("--tier-events", type=int, required=True)
ap.add_argument("--arrows-changed", type=int, required=True)
a = ap.parse_args()
dest = os.path.join(OUT, "saturation.jsonl")
if os.path.exists(dest):
    for l in open(dest, encoding="utf-8"):
        if l.strip() and json.loads(l).get("pass") == a.pas:
            sys.exit("saturation.jsonl already has a line for pass %d" % a.pas)
rows = [json.loads(l) for l in open(os.path.join(OUT, "story_rooms-p%d.jsonl" % a.pas), encoding="utf-8") if l.strip()]
v = [r for r in rows if r.get("sub")]
drawn = [d["sub"] for d in rows[0]["draw"]]
if sorted(r["sub"] for r in v) != sorted(drawn):
    sys.exit("not every drawn room carries a verdict")
c = collections.Counter(r["verdict"] for r in v)
line = {"pass": a.pas, "story": "model/story-p%d.md" % a.pas, "rooms": len(v), "room_list": drawn,
        "told": c.get("told", 0), "told-with-residue": c.get("told-with-residue", 0), "not-told": c.get("not-told", 0),
        "stopping_rule": {"tier_history_events": a.tier_events, "arrows_added_bounded_demoted_withdrawn": a.arrows_changed,
                          "story_sentences_changed": a.story_changed}}
with open(dest, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print(json.dumps(line, ensure_ascii=False))
