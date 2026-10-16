#!/usr/bin/env python3
"""Counts for an element group's notes, from my own rulings (via d3_group_rulings.py).

Prints the op by kind table (accepted lines by kind; particulars and rejects apart), then,
for each --pattern label=regex, the distinct rooms whose ruling reasons match it, with the
ids. Rooms are the id up to its last hyphen.

  python3 out/_analysis/d3_pattern_counts.py --element P05 --pattern keepers='intended|planned change'
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict

COLS = ("specification", "elaboration", "correction", "none", "particular", "reject")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--pattern", action="append", default=[])
    ap.add_argument("--ids", action="store_true", help="print the matching ids")
    a = ap.parse_args()
    out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", a.element],
                         capture_output=True, text=True).stdout
    rows = []
    for ln in out.splitlines():
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 6 or parts[0] == "id":
            continue
        rows.append(dict(id=parts[0], op=parts[1], decision=parts[2], kind=parts[3], pair=parts[4],
                         reason="|".join(parts[5:])))
    table = defaultdict(Counter)
    for r in rows:
        col = r["kind"] if r["decision"] == "accept" else r["decision"]
        table[r["op"]][col] += 1
        table["all"][col] += 1
    print(f"{a.element}: {len(rows)} rulings")
    print("op".ljust(15) + "".join(c.rjust(15) for c in COLS) + "total".rjust(8))
    for op in sorted(k for k in table if k != "all") + ["all"]:
        print(op.ljust(15) + "".join(str(table[op][c]).rjust(15) for c in COLS)
              + str(sum(table[op].values())).rjust(8))
    for spec in a.pattern:
        label, rx = spec.split("=", 1)
        hits = [r for r in rows if re.search(rx, r["reason"])]
        rooms = sorted({r["id"].rsplit("-", 1)[0] for r in hits})
        print(f"\n{label}: {len(rooms)} rooms, {len(hits)} lines")
        if a.ids:
            print("  " + ", ".join(r["id"] for r in hits))


if __name__ == "__main__":
    main()
