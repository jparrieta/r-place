#!/usr/bin/env python3
"""D3: check every single-quoted segment of one G rule's block in notes-D3.md (from its bullet to the next top-level
bullet or heading) against the named arrow's or element's fields, as model/*.jsonl holds them, and against the notes
text above the block (earlier G rules). Prints the segments found in neither. Writes nothing.

  python3 out/_analysis/d3_g_quote_check.py --rule G44 --id A12
"""
import argparse
import json
import re

ap = argparse.ArgumentParser()
ap.add_argument("--rule", required=True)
ap.add_argument("--id", required=True)
a = ap.parse_args()
notes = open("out/notes-D3.md", encoding="utf-8").read()
start = notes.index("- **%s (logged" % a.rule)
m = re.compile(r"\n(- \*\*|## )").search(notes, start + 5)
block = notes[start:m.start() if m else len(notes)]
before = notes[:start]
src = ""
for f in ("out/model/arrows.jsonl", "out/model/elements.jsonl"):
    for l in open(f, encoding="utf-8"):
        if l.strip() and json.loads(l)["id"] == a.id:
            src = json.dumps(json.loads(l), ensure_ascii=False)
SEG = re.compile(r"(?:(?<=[ (|])|^)'(.+?)'(?=[ ,;.)\]:]|$)", re.M)
segs = SEG.findall(block)
miss = [s for s in segs if s not in src and s not in before]
print("%s: %d segments; in %s's fields or earlier notes: %d; not found: %d" % (
    a.rule, len(segs), a.id, len(segs) - len(miss), len(miss)))
for s in miss:
    print("  " + s)
