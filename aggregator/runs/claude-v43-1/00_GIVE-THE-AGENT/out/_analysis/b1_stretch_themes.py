"""Codes and second-order themes per room for a stretch of the B1 order, with totals.

usage: python3 out/_analysis/b1_stretch_themes.py <first_order> <last_order>
"""
import re
import subprocess
import sys

first, last = int(sys.argv[1]), int(sys.argv[2])
order = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                       capture_output=True, text=True).stdout.splitlines()
rows = [l.split("\t") for l in order if l.strip()]
codes_total = themes_total = rooms = 0
for r in rows:
    n = int(r[0])
    if n < first or n > last:
        continue
    out = subprocess.run(["python3", "tools/mem.py", "room", r[1], "--size"],
                         capture_output=True, text=True).stdout
    m = re.search(r"codes (\d+)\s+second-order themes (\d+)", out)
    codes, themes = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    codes_total += codes
    themes_total += themes
    rooms += 1
    print("%d\t%s\t%d\t%d" % (n, r[1], codes, themes))
print("rooms %d, codes %d, second-order themes %d" % (rooms, codes_total, themes_total))
