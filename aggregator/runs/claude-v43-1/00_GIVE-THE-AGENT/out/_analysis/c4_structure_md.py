#!/usr/bin/env python3
"""Stage C4: write out/structure-C4.md, a whole file superseding structure-C3.md (rule 18). It is structure-C3.md with
a section saying what stage C4 changed, and, under each fourth-order theme whose construct block stage C4 amended, the
'What holds it together' line replaced by the amended `prose` read from fourth/fourth.jsonl. The old prose is taken
from the `was` of the C4 tier_history line and must be found exactly once. Nothing was recut. Refuses to overwrite
unless --replace is given.

    python3 out/_analysis/c4_structure_md.py [--replace]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SRC = os.path.join(OUT, "structure-C3.md")
DEST = os.path.join(OUT, "structure-C4.md")
if os.path.exists(DEST) and "--replace" not in sys.argv:
    sys.exit("out/structure-C4.md exists; pass --replace to regenerate it whole")
txt = open(SRC, encoding="utf-8").read()
t4 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8")))
hist = [json.loads(l) for l in open(os.path.join(OUT, "tier_history.jsonl"), encoding="utf-8") if l.strip()]
amended = [h for h in hist if str(h.get("stage")) == "C4" and h.get("event") == "construct_amended"]
HEAD = """# The data structure, stage C4: read against the field

This file supersedes `structure-C3.md` whole (rule 18). Stage C4 recut nothing. The 197 third-order themes, the 28 fourth-order themes and the 8 dimensions, with every member and count, are as stage C3 left them. Stage C4 changed the prose of two construct declarations, where the field's check (`field/check.md`) showed a sentence that the field and my own rooms contradict. Each amendment is a `tier_history.jsonl` line carrying the old line as `was`, with the move (relating or contrasting), the field's items and the rooms' items, snapped as C4-move-relating-51:
%s
No fourth-order theme enters from the field, since no room can answer a grouping. The two tentative entries from the field (P21, P22) sit under Negotiated order and Collective memory; they are in `model-C4.md`, not in this tier. What the field showed is in `field-C4.md`.

The text below is stage C3's, with these amendments written into it.

""" % "".join("- **%s %s.** %s. Field: %s. Rooms: %s.\n" % (
    h["id"], t4[h["id"]]["name"], h["why"][0].upper() + h["why"][1:], "; ".join(h["field_support"]),
    ", ".join(h.get("rooms") or []) or "none beyond my own model's count") for h in amended)
old_title = "# The data structure, stage C3: pass 4's structure read against the literature\n"
if txt.count(old_title) != 1:
    sys.exit("title not found once")
txt = txt.replace(old_title, HEAD + "## From here on, stage C3's text (the data structure, stage C3)\n")
for h in amended:
    old = "- **What holds it together:** %s\n" % h["was"]["prose"]
    if txt.count(old) != 1:
        sys.exit("%s: the old 'What holds it together' line is not found once" % h["id"])
    txt = txt.replace(old, "- **What holds it together (amended at C4a):** %s\n" % t4[h["id"]]["prose"])
with open(DEST, "w", encoding="utf-8") as f:
    f.write(txt)
print("structure-C4.md written: %d words (structure-C3.md %d); amended sections: %s" % (
    len(txt.split()), len(open(SRC, encoding="utf-8").read().split()), ", ".join(h["id"] for h in amended)))
