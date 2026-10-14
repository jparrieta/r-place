#!/usr/bin/env python3
"""C3a: the size of each read-tier shelf work as `mem.py shelf <name>` serves it (lines, bytes, pages), so each can be
read whole in pages under the output limit. Calls mem.py with --limit 1 so no work's text is printed here; mem.py logs
each call. Prints nothing of the works' text.

    python3 out/_analysis/c3a_shelf_sizes.py
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# the method shelf only: the explanation shelf is not served before the log point (stage C3 section 1)
names = sys.argv[1:] or ["eisenhardt-1989", "gioia-corley-hamilton-2013", "grodal-anteby-holm-2021", "langley-1999",
                         "suddaby-2006", "van-de-ven-poole-1990"]
for n in names:
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "shelf", n, "--limit", "1"], cwd=ROOT,
                       capture_output=True, text=True)
    m = re.search(r"\[end: lines (\d+)-(\d+) of (\d+)\]|\[more: lines (\d+)-(\d+) of (\d+)[^\]]*\]", p.stdout)
    tail = [l for l in p.stdout.splitlines() if l.startswith("[")]
    print("%-28s %s" % (n, tail[-1] if tail else p.stdout[-200:].replace("\n", " | ")))
