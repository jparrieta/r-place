#!/usr/bin/env python3
"""D5, room-form accounts: run tools/cite.py for a list of room:code pairs and print each quote line (cite.py logs
each read as usual).

    python3 out/_analysis/d5f_cites.py FloydVsVoid:c0088,FloydVsVoid:c0128
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for pair in sys.argv[1].split(","):
    room, code = pair.split(":")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", room, "--code", code],
                       capture_output=True, text=True, cwd=ROOT)
    lines = [l for l in r.stdout.splitlines() if l.startswith('"') or "[%s/%s]" % (room, code) in l]
    print(lines[0] if lines else "NOT FOUND %s/%s %s" % (room, code, r.stdout.strip()[-200:]))
