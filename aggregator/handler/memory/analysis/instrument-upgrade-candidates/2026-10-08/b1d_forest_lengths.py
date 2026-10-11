"""B1d check: how many lines each reread room's forest print has, so that a print cut by
`mem.py forest --limit 5000` is found. Reads the rooms from out/pass2-B1.jsonl (or the rooms given
on the command line) and asks mem.py for one line of each forest, whose page footer gives the total.

usage: python3 out/_analysis/b1d_forest_lengths.py [sub ...]
"""
import json
import re
import subprocess
import sys

subs = sys.argv[1:]
if not subs:
    for l in open("out/pass2-B1.jsonl"):
        l = l.strip()
        if l:
            d = json.loads(l)
            s = d.get("sub") or d.get("room")
            if s and s not in subs:
                subs.append(s)

over = []
for s in subs:
    r = subprocess.run(["python3", "tools/mem.py", "forest", s, "--limit", "1"],
                       capture_output=True, text=True)
    m = re.search(r"lines \d+-\d+ of (\d+)[;\]]", r.stdout + r.stderr)
    n = int(m.group(1)) if m else -1
    flag = "OVER 5000" if n > 5000 else ""
    if n > 5000:
        over.append(s)
    print("%-28s %6d %s" % (s, n, flag))
print("rooms: %d; over 5000 lines: %d %s" % (len(subs), len(over), " ".join(over)))
