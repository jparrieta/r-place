#!/usr/bin/env python3
"""Wait (up to --max seconds) until a text file holds at least --lines lines, then print its last lines.
Used to wait in the foreground for a check the harness moved to the background.

    python3 out/_analysis/wait_output.py --file <path> --lines 4 --max 540
"""
import argparse, os, time

ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--lines", type=int, default=4)
ap.add_argument("--max", type=int, default=540)
a = ap.parse_args()
t0 = time.time()
n = 0
while time.time() - t0 < a.max:
    if os.path.exists(a.file):
        n = len(open(a.file, encoding="utf-8", errors="replace").read().splitlines())
        if n >= a.lines:
            break
    time.sleep(5)
print("waited %.0f s; lines %d" % (time.time() - t0, n))
print("\n".join(open(a.file, encoding="utf-8", errors="replace").read().splitlines()[-20:]))
