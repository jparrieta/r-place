#!/usr/bin/env python3
"""D3: read several cited concepts whole, one cite.py call per concept (each read is logged as cite.py logs it).
Prints the quote line of each, whole. Writes nothing.

    python3 out/_analysis/d3_cites.py AcePlace:c0060 Cornwall:c0003
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for arg in sys.argv[1:]:
    room, code = arg.rsplit(":", 1)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                       cwd=ROOT, capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    print(lines[0] if lines else "(no quote) %s/%s" % (room, code))
