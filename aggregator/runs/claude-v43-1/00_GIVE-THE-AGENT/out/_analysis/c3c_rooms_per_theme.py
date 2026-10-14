#!/usr/bin/env python3
"""C3c: rooms carrying each given theme (third or fourth order), with its name from structure-C3.md, and the union, via
`mem.py rooms --with`. For the counts in literature-C3.md's four-problems section. Writes nothing.

    python3 out/_analysis/c3c_rooms_per_theme.py T3-xxx [T4-yyy ...]
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
txt = open(os.path.join(ROOT, "out", "structure-C3.md"), encoding="utf-8").read()
names = {}
for line in re.findall(r"- \*\*Members:\*\* (.*?)\. Rooms carrying any member", txt):
    names.update(re.findall(r"(T3-\d{3}) ([^,]+)", line))
names.update(re.findall(r"^### (T4-\d{3}) (.+)$", txt, re.M))
u = set()
for t in sys.argv[1:]:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "rooms", "--with", t, "--limit", "2000"],
                       cwd=ROOT, capture_output=True, text=True)
    n = int(re.search(r"rooms with \S+: (\d+) of", p.stdout).group(1))
    got = set(re.findall(r"^  (\S+)\s*$", p.stdout, re.M))
    if len(got) != n:
        sys.exit("%s: header says %d rooms, parsed %d" % (t, n, len(got)))
    u |= got
    print("%s %-45s %3d rooms" % (t, names.get(t, "?"), n))
print("union: %d of 705" % len(u))
