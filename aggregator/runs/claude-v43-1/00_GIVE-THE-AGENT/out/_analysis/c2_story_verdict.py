#!/usr/bin/env python3
"""C2 section 5: append one verdict line to out/story_rooms-pN.jsonl after a room is read whole against the story.
The room must be in the draw line (the first line, written before any room was opened) and must not already carry a
verdict line. The why_drawn and the rule are copied from the draw line.

    python3 out/_analysis/c2_story_verdict.py --pass 1 --sub ubc --verdict told-with-residue \
        --residue "..." --arrows "A01 holds; A03 holds" [--needs "..."] [--read "room --no-canvas; forest (4 pages)"]
"""
import argparse, json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="pas", type=int, required=True)
ap.add_argument("--sub", required=True)
ap.add_argument("--verdict", required=True, choices=("told", "told-with-residue", "not-told"))
ap.add_argument("--residue", default="")
ap.add_argument("--arrows", default="")
ap.add_argument("--needs", default="")
ap.add_argument("--read", default="room --no-canvas, then the whole forest")
a = ap.parse_args()
path = os.path.join(OUT, "story_rooms-p%d.jsonl" % a.pas)
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
draw = rows[0]
names = dict((d["sub"], d) for d in draw["draw"])
if a.sub not in names:
    sys.exit("%s is not in the pass %d draw" % (a.sub, a.pas))
if any(r.get("sub") == a.sub for r in rows[1:]):
    sys.exit("%s already carries a verdict line" % a.sub)
if a.verdict != "told" and not a.residue:
    sys.exit("a verdict other than told needs its residue or reason clause")
line = {"pass": a.pas, "sub": a.sub, "verdict": a.verdict, "residue": a.residue or None, "arrows_seen": a.arrows,
        "needs": a.needs or None, "read": a.read, "why_drawn": names[a.sub]["why_drawn"], "rule": "pass %d draw, line 1" % a.pas}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print("appended %s: %s; verdict lines now %d of %d drawn" % (a.sub, a.verdict, len(rows), len(names)))
