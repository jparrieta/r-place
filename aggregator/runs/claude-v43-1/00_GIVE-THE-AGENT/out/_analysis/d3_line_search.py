#!/usr/bin/env python3
"""D3: search one element's adaptation lines (all ops) for a pattern, to find a second room for a form (G4).
Reads the lines whole through d3_packet.py (which runs the verb), paged by 100, and prints the header, how and
codes of each line whose block matches --regex (case-insensitive). Writes nothing.

    python3 out/_analysis/d3_line_search.py --element P09 --regex "pxls|successor"
"""
import argparse, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--regex", required=True)
a = ap.parse_args()
pat = re.compile(a.regex, re.I)


def blocks(offset):
    r = subprocess.run([sys.executable, os.path.join(HERE, "d3_packet.py"), "--element", a.element,
                        "--offset", str(offset), "--limit", "100"], cwd=ROOT, capture_output=True, text=True)
    out, cur = [], []
    for l in r.stdout.splitlines():
        if l.startswith("== "):
            if cur:
                out.append(cur)
            cur = [l]
        elif cur and l.startswith("   "):
            cur.append(l)
    if cur:
        out.append(cur)
    return out


offset, seen, hits = 0, 0, 0
while True:
    bs = blocks(offset)
    if not bs:
        break
    for b in bs:
        seen += 1
        if pat.search("\n".join(b)):
            hits += 1
            print("\n".join(x for x in b if x.startswith("== ") or x.strip().startswith(("how:", "codes:"))))
    offset += 100
print("%s: %d lines searched, %d match /%s/" % (a.element, seen, hits, a.regex))
