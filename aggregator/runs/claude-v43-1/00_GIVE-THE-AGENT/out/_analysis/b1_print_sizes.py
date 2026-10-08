"""Print the size of each room's b1_room.py print (lines and bytes) for a stretch of the order,
so a notes section can say which rooms were read in parts under 30 KB.

usage: python3 out/_analysis/b1_print_sizes.py <first order> <last order>
"""
import subprocess
import sys

first, last = int(sys.argv[1]), int(sys.argv[2])
order = subprocess.run(["python3", "tools/saturation.py", "order", "--stage", "B1"],
                       capture_output=True, text=True).stdout
for line in order.splitlines():
    parts = line.split("\t")
    if len(parts) < 2 or not parts[0].strip().isdigit():
        continue
    n, sub = int(parts[0]), parts[1]
    if first <= n <= last:
        out = subprocess.run(["python3", "out/_analysis/b1_room.py", sub],
                             capture_output=True, text=True).stdout
        size = len(out.encode("utf-8"))
        print("%d\t%s\t%d lines\t%d bytes%s" % (n, sub, out.count("\n"), size,
                                                "\tover 30 KB" if size > 30000 else ""))
