#!/usr/bin/env python3
"""D3a-47: print one numbered reading of a G-rule from the diary, read through `mem.py diary --grep`.
Only entries whose text holds the rule's readings header ("G52's readings") are read; from each, the text from
"(N) " up to the next "(N+1) " (or the entry's end) is printed. Writes nothing.

    python3 out/_analysis/d3_diary_reading.py --rule G52 --n 28
"""
import argparse
import re
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--rule", required=True)
ap.add_argument("--n", type=int, required=True)
a = ap.parse_args()

head = "%s's readings" % a.rule
out = subprocess.run(["python3", "tools/mem.py", "diary", "--grep", head],
                     capture_output=True, text=True).stdout
start = "(%d) " % a.n
stop = "(%d) " % (a.n + 1)
found = 0
for line in out.splitlines():
    if head not in line or start not in line:
        continue
    i = line.index(start)
    j = line.find(stop, i)
    seg = line[i:] if j < 0 else line[i:j]
    print(line[:40].rstrip())
    print(seg.strip())
    print()
    found += 1
print("entries printed: %d" % found)
