#!/usr/bin/env python3
"""D3a-47, read-only: for every A20 order row (O-A, O-H, S-O-A, S-O-H) in the given spec files, list the concepts of
the line (from its block in A20's window quote files) and the concepts its evidence names (from A20's quote and
cites files) whose words name a megathread, a sticky, a pinned, existing, ongoing, official or chosen thread, or
something already made, so that G52's reading 23 (a pointer to a line made at an hour the line does not show) can be
applied to each. Prints the row, the class and each matching concept whole, with its hour. Writes nothing.

  python3 out/_analysis/d3_a20_pointer_scan.py --specs A20-inst-spec.txt A20-restrict-spec.txt A20-addcond-spec.txt
"""
import argparse
import glob
import re

ap = argparse.ArgumentParser()
ap.add_argument("--specs", nargs="+", required=True)
a = ap.parse_args()
R = "out/_analysis/d3_rulings/"
QLINE = re.compile(r'^\s*"(.*)"  \[([^/\]]+)/(c\d{4})\]\s+item \S+\s+thread \S+\s+h\+([\d.]+)')
HEAD = re.compile(r"^\[\d+\] (\S+-\d{3})\s")
quote, blocks = {}, {}
for f in sorted(glob.glob("out/_analysis/d3_wq_A20_*.txt")):
    cur = None
    for l in open(f, encoding="utf-8"):
        h = HEAD.match(l)
        if h:
            cur = h.group(1)
            blocks.setdefault(cur, set())
            continue
        m = QLINE.match(l)
        if m:
            quote[(m.group(2), m.group(3))] = (m.group(4), m.group(1))
            if cur:
                blocks[cur].add(m.group(3))
for f in sorted(glob.glob("out/_analysis/d3_cites_A20_*.txt")):
    for l in open(f, encoding="utf-8"):
        m = QLINE.match(l)
        if m:
            quote[(m.group(2), m.group(3))] = (m.group(4), m.group(1))
PAT = re.compile(r"mega ?-?thread|sticky|stickied|pinned|already|existing|ongoing|official thread|chosen thread", re.I)
n_rows = n_hit = 0
for s in a.specs:
    for l in open(R + s, encoding="utf-8"):
        if not l.strip():
            continue
        aid, cls, ev = l.rstrip("\n").split("|", 2)
        if cls not in ("O-A", "O-H", "S-O-A", "S-O-H"):
            continue
        n_rows += 1
        room = aid.rsplit("-", 1)[0]
        codes = sorted(blocks.get(aid, set()) | set(re.findall(r"\bc\d{4}\b", ev)))
        hits = [(c,) + quote[(room, c)] for c in codes if (room, c) in quote and PAT.search(quote[(room, c)][1])]
        if hits:
            n_hit += 1
            print("%s %s (%s)" % (aid, cls, s))
            for c, h, q in hits:
                print("   %s h+%s %s" % (c, h, q))
print("order rows scanned: %d; rows with a matching concept: %d" % (n_rows, n_hit))
