#!/usr/bin/env python3
"""D3a-47: write a superseding spec file and tag file before any build. Rows in --rows ('id|CLASS|evidence') replace
the rows of the same ids in --spec-in, in place; every other row is copied unchanged. In the tag file, each replaced
id loses its old tag line and takes the line given in --rows-tags ('id|TAGS'), if any. Refuses an id that --spec-in
lacks, a repeated id, or an output path that already exists. The input files stay.

  python3 out/_analysis/d3_spec_supersede.py --spec-in A.txt --rows R.txt --spec-out A-v2.txt \
      --tags-in T.txt --rows-tags RT.txt --tags-out T-v2.txt
"""
import argparse
import os
import sys

ap = argparse.ArgumentParser()
for k in ("--spec-in", "--rows", "--spec-out", "--tags-in", "--tags-out"):
    ap.add_argument(k, required=True)
ap.add_argument("--rows-tags", default="")
a = ap.parse_args()
for p in (a.spec_out, a.tags_out):
    if os.path.exists(p):
        sys.exit("refused: %s exists" % p)


def rows(path):
    out = []
    for l in open(path, encoding="utf-8"):
        if l.strip():
            out.append((l.split("|", 1)[0], l.rstrip("\n")))
    return out


new = dict(rows(a.rows))
assert len(new) == len(rows(a.rows)), "repeated id in --rows"
spec = rows(a.spec_in)
ids = [i for i, _ in spec]
missing = [i for i in new if i not in ids]
if missing:
    sys.exit("refused: ids not in --spec-in: %s" % missing)
with open(a.spec_out, "w", encoding="utf-8") as f:
    for i, l in spec:
        f.write((new[i] if i in new else l) + "\n")
newtags = dict(rows(a.rows_tags)) if a.rows_tags else {}
kept = [(i, l) for i, l in rows(a.tags_in) if i not in new]
with open(a.tags_out, "w", encoding="utf-8") as f:
    for i, l in kept:
        f.write(l + "\n")
    for i in new:
        if i in newtags:
            f.write(newtags[i] + "\n")
print("replaced %d rows of %d in %s; tags %d lines in %s" % (len(new), len(spec), a.spec_out,
                                                            len(kept) + sum(1 for i in new if i in newtags),
                                                            a.tags_out))
