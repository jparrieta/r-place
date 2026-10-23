#!/usr/bin/env python3
"""Append one built file from out/_analysis/ to the end of out/notes-D3.md, unchanged, after a blank line.
Refuses a source outside out/_analysis/ and a source whose first line already sits in the notes (so a table is
never appended twice). Prints the notes' line count before and after.

    python3 out/_analysis/d3b_append_to_notes.py --source out/_analysis/d3b_room_table_v4.md
"""
import argparse, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
NOTES = os.path.join(OUT, "notes-D3.md")
ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True)
a = ap.parse_args()
src = os.path.abspath(a.source)
if not src.startswith(os.path.join(OUT, "_analysis") + os.sep):
    raise SystemExit("--source must be under out/_analysis/")
body = open(src, encoding="utf-8").read()
notes = open(NOTES, encoding="utf-8").read()
lines = body.splitlines()
if lines and lines[0] in notes:
    raise SystemExit("the source's header line is already in notes-D3.md; nothing appended")
before = notes.count("\n")
with open(NOTES, "a", encoding="utf-8") as f:
    if not notes.endswith("\n\n"):
        f.write("\n")
    f.write(body if body.endswith("\n") else body + "\n")
after = open(NOTES, encoding="utf-8").read().count("\n")
print("appended %s (%d lines); notes-D3.md %d -> %d lines" % (os.path.relpath(src, ROOT), len(lines), before, after))
