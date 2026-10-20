#!/usr/bin/env python3
"""D3a-39: print, from a reading window (d3_read_window.py output), only the blocks of the named line ids, so a
second reading can look at candidates without re-reading the whole window. Writes nothing.

  python3 out/_analysis/d3_pick_blocks.py out/_analysis/d3_rw_A12_ab000.txt AcePlace-042 ManningPlace-025
"""
import re
import sys

win, want = sys.argv[1], set(sys.argv[2:])
HEAD = re.compile(r"^(?:\[\d+\] )?(\S+-\d{3})\s+\S+\s")
cur, out, seen = None, [], set()
for l in open(win, encoding="utf-8"):
    m = HEAD.match(l)
    if m:
        cur = m.group(1)
    if cur in want:
        out.append(l.rstrip("\n"))
        seen.add(cur)
print("\n".join(out))
print("blocks found: %d of %d; missing: %s" % (len(seen), len(want), " ".join(sorted(want - seen)) or "none"))
