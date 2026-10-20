#!/usr/bin/env python3
"""D3a-39: add each line's full 'how' (and its transitions) from packet files (d3_packet.py output) to a reading
window (d3_read_window.py output), since the window's header line cuts the how short. Writes <window>.how.txt beside
the window and prints how many blocks took a how.

  python3 out/_analysis/d3_add_how.py out/_analysis/d3_rw_A12_r567_000.txt out/_analysis/d3_pk_A12_restrict_000.txt
"""
import re
import sys

win, packets = sys.argv[1], sys.argv[2:]
how = {}
for p in packets:
    for blk in open(p, encoding="utf-8").read().split("\n== ")[1:]:
        lines = blk.split("\n")
        aid = lines[0].split()[0]
        keep = [l for l in lines[1:] if l.strip().startswith(("how:", "transitions:", "condition:", "observation:"))]
        how[aid] = keep
HEAD = re.compile(r"^(?:\[\d+\] )?(\S+-\d{3})\s+\S+\s")
out, n = [], 0
for l in open(win, encoding="utf-8"):
    out.append(l.rstrip("\n"))
    m = HEAD.match(l)
    if m and m.group(1) in how:
        n += 1
        out += ["   " + x.strip() for x in how[m.group(1)]]
open(win.replace(".txt", ".how.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("%s: %d blocks took a how" % (win, n))
