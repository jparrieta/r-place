#!/usr/bin/env python3
"""D3a-44, read-only: lay out one element's lines in `mem.py adaptations --element <id>` by op. Runs the verb once
over the whole list and prints, for each op, the verb offset of its first line and how many lines it has, counting
the verb's entries in the order it prints them. Writes nothing.

  python3 out/_analysis/d3_verb_offsets.py A17
"""
import re
import subprocess
import sys

el = sys.argv[1]
out = subprocess.run([sys.executable, "tools/mem.py", "adaptations", "--element", el, "--limit", "100000"],
                     capture_output=True, text=True).stdout.splitlines()
OPS = ("absent", "add-condition", "add-step", "instantiate", "restrict", "contradict", "link", "propose")
LINE = re.compile(r"^(\S+-\d{3})\s+(%s)\b" % "|".join(OPS))
seen, first, count = [], {}, {}
idx = 0
for l in out:
    m = LINE.match(l)
    if not m:
        continue
    idx += 1
    op = m.group(2)
    if op not in first:
        first[op] = idx
        seen.append(op)
    count[op] = count.get(op, 0) + 1
print("verb entries counted: %d (offsets count the verb's header line as 0)" % idx)
for op in seen:
    print("  %-14s first at verb offset %d, %d lines" % (op, first[op], count[op]))
