#!/usr/bin/env python3
"""Wait, up to a limit in seconds, until a text file contains a given string; then print the file's last lines.

    python3 out/_analysis/d6a13_wait_for.py <file> <string> <seconds>
"""
import sys, time

path, needle, limit = sys.argv[1], sys.argv[2], float(sys.argv[3])
t0 = time.time()
text = ""
while time.time() - t0 < limit:
    text = open(path, encoding="utf-8", errors="replace").read()
    if needle in text:
        break
    time.sleep(5)
print("\n".join(text.splitlines()[-15:]))
print("found" if needle in text else "not found after %.0f s" % limit)
