#!/usr/bin/env python3
"""C5a-01: serve a list of quotes through cite.py, one call per room/code (each call is logged by cite.py), and print
each quote whole with its hour, for the account. Writes nothing of its own.

    python3 out/_analysis/c5_cite_batch.py room/code [room/code ...]
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for rc in sys.argv[1:]:
    room, code = rc.split("/")
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                       cwd=ROOT, capture_output=True, text=True)
    line = [l for l in p.stdout.splitlines() if l.startswith('"')]
    if not line:
        print("%s: NOT SERVED %s" % (rc, p.stdout.strip()[:200]))
        continue
    m = re.match(r'^(".*")\s+\[(\S+)\]\s+item \S+\s+thread \S+\s+h\+?([\d.]+)', line[0])
    print("%s h%s %s" % (m.group(2), m.group(3), m.group(1)) if m else line[0][:400])
