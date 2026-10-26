#!/usr/bin/env python3
"""D4a-05: print a template with each line '{{TABLE:name}}' replaced by d4a05_top.py --what md --table name.

    python3 out/_analysis/d4a05_fill.py out/_analysis/d4a05_template.md > out/room-forms-D4a05.md
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for line in open(sys.argv[1], encoding="utf-8").read().split("\n"):
    m = re.fullmatch(r"\{\{TABLE:([a-z]+)\}\}", line.strip())
    if m:
        out = subprocess.run([sys.executable, os.path.join(HERE, "d4a05_top.py"), "--what", "md", "--table", m.group(1)],
                             capture_output=True, text=True, check=True).stdout.rstrip("\n")
        print(out)
    else:
        print(line)
