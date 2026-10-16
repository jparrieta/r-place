#!/usr/bin/env python3
"""D3: elaboration families for an element group's notes, from my own rulings (via d3_group_rulings.py,
the latest ruling per line). Only accepted lines of the given kind (elaboration by default) are read.
Each --family label=regex is matched against the reason's closing clause (the text after its last '; ').
Prints, per family, lines, distinct rooms and the first ids; then the lines no family matched.

  python3 out/_analysis/d3_family_counts.py --element P03 --family rebuild='builds again'
"""
import argparse
import re
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--kind", default="elaboration")
    ap.add_argument("--family", action="append", default=[])
    ap.add_argument("--show", type=int, default=4, help="ids printed per family")
    a = ap.parse_args()
    out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", a.element,
                          "--kind", a.kind], capture_output=True, text=True).stdout
    rows = []
    for ln in out.splitlines():
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 6 or parts[2] != "accept" or parts[3] != a.kind:
            continue
        reason = "|".join(parts[5:])
        rows.append((parts[0], parts[1], reason.split("; ")[-1]))
    fams = []
    for f in a.family:
        label, _, rx = f.partition("=")
        fams.append((label, re.compile(rx, re.I)))
    seen = set()
    total = 0
    print(f"{a.element}: {len(rows)} accepted {a.kind} lines")
    for label, rx in fams:
        hit = [r for r in rows if rx.search(r[2])]
        rooms = sorted({r[0].rsplit("-", 1)[0] for r in hit})
        ops = {}
        for r in hit:
            ops[r[1]] = ops.get(r[1], 0) + 1
        dup = [r[0] for r in hit if r[0] in seen]
        seen.update(r[0] for r in hit)
        total += len(hit)
        print(f"{label}: lines {len(hit)}, rooms {len(rooms)}, ops {ops}; ids {', '.join(r[0] for r in hit[:a.show])}"
              + (f"; also in an earlier family: {', '.join(dup)}" if dup else ""))
    rest = [r[0] for r in rows if r[0] not in seen]
    print(f"matched lines (with repeats) {total}; unmatched {len(rest)}: {' '.join(rest)}")


if __name__ == "__main__":
    main()
