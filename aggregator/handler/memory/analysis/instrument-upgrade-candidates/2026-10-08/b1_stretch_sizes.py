"""Sizes of the next rooms in the B1 order (codes plus second-order themes, not the forest),
with a running total, to declare a stretch of about 1 MB.

usage: python3 out/_analysis/b1_stretch_sizes.py <first_order> <last_order>
"""
import re
import subprocess
import sys

first, last = int(sys.argv[1]), int(sys.argv[2])
order = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                       capture_output=True, text=True).stdout.splitlines()
rows = [l.split("\t") for l in order if l.strip()]
total = 0
for r in rows:
    n = int(r[0])
    if n < first or n > last:
        continue
    out = subprocess.run(["python3", "tools/mem.py", "room", r[1], "--size"],
                         capture_output=True, text=True).stdout
    m = re.search(r"codes (\d+)\s+second-order themes (\d+)", out)
    size = int(m.group(1)) + int(m.group(2)) if m else 0
    total += size
    print("%d\t%s\t%s\t%d\t%d" % (n, r[1], r[2] if len(r) > 2 else "", size, total))
