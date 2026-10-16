#!/usr/bin/env python3
"""D2a: append the split rooms to out/notes-D2.md, grouped by verdict pair, from out/_analysis/d2_verdict_rooms.json
(written by d2_verdicts.py --list), so that no room name is typed. Refuses if the notes already carry the list.

    python3 out/_analysis/d2_notes_split.py
"""
import collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
NOTES = os.path.join(OUT, "notes-D2.md")
MARK = "<!-- split rooms, generated -->"

d = json.load(open(os.path.join(OUT, "_analysis", "d2_verdict_rooms.json")))
text = open(NOTES, encoding="utf-8").read()
if MARK in text:
    sys.exit("notes-D2.md already carries the split list; not appended")
by = collections.defaultdict(list)
for x in d["split"]:
    by[" against ".join(x["pair"])].append(x["sub"])
L = ["", MARK, ""]
for pair, subs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    L.append("**%s** (%d): %s." % (pair, len(subs), ", ".join(sorted(subs, key=str.lower))))
    L.append("")
L.append("Unsupported cannot-tell lines: %d." % len(d["unsupported_cannot_tell"]))
with open(NOTES, "a", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("appended %d split rooms in %d pairs" % (sum(len(v) for v in by.values()), len(by)))
