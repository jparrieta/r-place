#!/usr/bin/env python3
"""Stage C3: write out/structure-C3.md, a whole file superseding structure-p4.md (and structure.md; rule 18). It is
structure-p4.md with a section saying what stage C3 changed, and, under each fourth-order theme whose construct block
stage C3 amended, the amended `mistaken_for` read from fourth/fourth.jsonl. The third-order tier and every count are
pass 4's: nothing was recut. Every anchor must be found exactly once. Refuses to overwrite unless --replace is given.

    python3 out/_analysis/c3_structure_md.py [--replace]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SRC = os.path.join(OUT, "structure-p4.md")
DEST = os.path.join(OUT, "structure-C3.md")
if os.path.exists(DEST) and "--replace" not in sys.argv:
    sys.exit("out/structure-C3.md exists; pass --replace to regenerate it whole")
txt = open(SRC, encoding="utf-8").read()
t4 = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8")))
hist = [json.loads(l) for l in open(os.path.join(OUT, "tier_history.jsonl"), encoding="utf-8") if l.strip()]
amended = [h for h in hist if str(h.get("stage")) == "C3" and h.get("event") == "construct_amended"]
ids = [h["id"] for h in amended]
HEAD = """# The data structure, stage C3: pass 4's structure read against the literature

This file supersedes `structure-p4.md` and `structure.md` whole (rule 18). Stage C3 recut nothing: the 197 third-order themes, the 28 fourth-order themes and the 8 dimensions, with every member and count, are pass 4's. What stage C3 changed is the construct declarations of the fourth-order themes below, where the shelf names a construct each may be mistaken for (stage C3 section 6). Each amendment is a `tier_history.jsonl` line carrying the old line as `was`, with the move (relating or contrasting) and the work:
%s
The third-order themes keep their descriptive names (contract section 1). What each work did to the model is in `literature-C3.md`.

The text below is pass 4's, with these amendments written into it.

""" % "".join("- **%s %s**, prompted by %s: %s\n" % (h["id"], t4[h["id"]]["name"], h["prompted_by"], h["why"])
              for h in amended)
old_title = "# The data structure, stage C2, pass 4 (C2d-01)\n"
if txt.count(old_title) != 1:
    sys.exit("title not found once")
txt = txt.replace(old_title, HEAD + "## From here on, pass 4's text (the data structure, stage C2, pass 4, C2d-01)\n")
for tid in ids:
    head = "### %s %s\n" % (tid, t4[tid]["name"])
    i = txt.find(head)
    if i < 0 or txt.count(head) != 1:
        sys.exit("section for %s not found once" % tid)
    anchor = "- **What this material's version cannot do:**"
    j = txt.find(anchor, i)
    k = txt.find("\n", j)
    nxt = txt.find("\n### ", i + len(head))
    if j < 0 or (nxt >= 0 and j > nxt):
        sys.exit("anchor for %s not found in its section" % tid)
    line = "- **May be mistaken for (amended at C3b):** %s\n" % t4[tid]["mistaken_for"]
    txt = txt[:k + 1] + line + txt[k + 1:]
with open(DEST, "w", encoding="utf-8") as f:
    f.write(txt)
print("structure-C3.md written: %d words (structure-p4.md %d); amended sections: %s" % (
    len(txt.split()), len(open(SRC, encoding="utf-8").read().split()), ", ".join(ids)))
