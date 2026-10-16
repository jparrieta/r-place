#!/usr/bin/env python3
"""D3: one element group's latest rulings tabulated by op, decision and kind, for the notes' table.
Reads d3_group_rulings.py's output (id | op | decision | kind | pair | reason). A reject is counted
under 'reject' whatever kind the ledger shows; an accept of kind none is an evidence limit.

  python3 out/_analysis/d3_opkind.py --element P16
"""
import argparse
import subprocess
import sys
from collections import Counter, defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    a = ap.parse_args()
    out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", a.element],
                         capture_output=True, text=True).stdout
    table = defaultdict(Counter)
    for ln in out.splitlines():
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 6:
            continue
        op, dec, kind = parts[1], parts[2], parts[3]
        if dec == "reject":
            col = "reject"
        elif dec == "particular":
            col = "particular"
        elif dec == "accept" and kind == "none":
            col = "evidence limit"
        elif dec == "accept":
            col = kind
        else:
            col = dec
        table[op][col] += 1
    cols = ["specification", "elaboration", "correction", "evidence limit", "particular", "reject"]
    extra = sorted({c for t in table.values() for c in t} - set(cols))
    cols += extra
    print("op | lines | " + " | ".join(cols))
    total = Counter()
    for op in sorted(table, key=lambda o: -sum(table[o].values())):
        t = table[op]
        total.update(t)
        print(f"{op} | {sum(t.values())} | " + " | ".join(str(t.get(c, 0)) for c in cols))
    print(f"all | {sum(total.values())} | " + " | ".join(str(total.get(c, 0)) for c in cols))


if __name__ == "__main__":
    main()
