"""Concepts matching a regular expression (case-blind) in each of several rooms, read from each
room's full concept listing (paged through b1_room_codes.py), so no match hides past a page.

usage: python3 out/_analysis/b1_grep_rooms.py "<regex>" <sub> [<sub> ...]
"""
import re
import subprocess
import sys

rx = re.compile(sys.argv[1], re.I)
for sub in sys.argv[2:]:
    out = subprocess.run(["python3", "out/_analysis/b1_room_codes.py", sub],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if rx.search(line):
            print(line[:300])
