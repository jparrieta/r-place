#!/usr/bin/env python3
"""D6a-17: print whole sections of a room's A1 telling, read through the verb (mem.py case), for citing moments.
By default the Chronology and the Relations sections; every line printed whole.

    python3 out/_analysis/d6a17_case_sections.py --sub monalisaclan
"""
import argparse, os, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--sub", required=True)
ap.add_argument("--sections", default="Chronology,Relations")
a = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
text = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "case", a.sub], capture_output=True,
                      text=True, cwd=ROOT).stdout
want = [s.strip() for s in a.sections.split(",")]
keep = False
for line in text.splitlines():
    if line.startswith("## "):
        keep = any(line[3:].startswith(w) for w in want)
    if keep:
        print(line)
