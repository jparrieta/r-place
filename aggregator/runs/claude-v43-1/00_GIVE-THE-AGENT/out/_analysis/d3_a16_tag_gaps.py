#!/usr/bin/env python3
"""D3a-43: list A16 lines whose census tags may be missing: rows classed O-A or S-O-A with no RSN or BARE tag, and
P-G6 rows whose text says 'marked PO' with no PO tag. Reads the spec files and the A16-tags files. Writes nothing.

  python3 out/_analysis/d3_a16_tag_gaps.py
"""
import glob

R = "out/_analysis/d3_rulings/"
tags = {}
for f in sorted(glob.glob(R + "A16-tags-*.txt")):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            tags.setdefault(i, set()).update(t.split(","))
rows = []
for f in ("A16-inst-spec.txt", "A16-restrict-spec.txt", "A16-addcond-spec.txt", "A16-addstep-spec.txt",
          "A16-absent-rows.txt"):
    for l in open(R + f, encoding="utf-8"):
        if l.strip():
            i, c, ev = l.rstrip("\n").split("|", 2)
            rows.append((f, i, c, ev))
unmarked = [(f, i) for f, i, c, ev in rows if c in ("O-A", "S-O-A") and not tags.get(i, set()) & {"RSN", "BARE"}]
print("O-A and S-O-A rows with no RSN or BARE tag: %d" % len(unmarked))
for f, i in unmarked:
    print("  %s %s" % (f, i))
po = [(f, i) for f, i, c, ev in rows if c in ("P-G6", "PART") and "marked PO" in ev and "PO" not in tags.get(i, ())]
print("rows that say 'marked PO' with no PO tag: %d" % len(po))
for f, i in po:
    print("  %s %s" % (f, i))
