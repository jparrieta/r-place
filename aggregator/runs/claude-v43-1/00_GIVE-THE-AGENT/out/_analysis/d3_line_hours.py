#!/usr/bin/env python3
"""For one element's packet, print each line's concepts with their hours (from tools/cite.py),
so a rule that turns on time (G13: P22 only after hour 73) can be applied line by line.
Prints: id, then code:hour pairs, then the earliest and latest hour and how many codes fall
after the --after hour.

  python3 out/_analysis/d3_line_hours.py --element P22 --op restrict --offset 0 --limit 76
"""
import argparse
import re
import subprocess
import sys


def hour(room, code):
    out = subprocess.run([sys.executable, "tools/cite.py", "--room", room, "--code", code],
                         capture_output=True, text=True).stdout
    m = re.search(r"h\+(\d+(?:\.\d+)?)", out)
    return float(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--op", required=True)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--after", type=float, default=73.0)
    a = ap.parse_args()
    out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", a.element,
                          "--op", a.op, "--offset", str(a.offset), "--limit", str(a.limit)],
                         capture_output=True, text=True).stdout
    for blk in out.split("\n== ")[1:]:
        lid = blk.split()[0]
        room = lid.rsplit("-", 1)[0]
        m = re.search(r"codes: (.*)", blk)
        codes = re.findall(r"\b(c\d{4})\b", m.group(1)) if m else []
        hrs = [(c, hour(room, c)) for c in codes]
        got = [h for _, h in hrs if h is not None]
        late = sum(1 for h in got if h > a.after)
        span = f"{min(got):.1f}-{max(got):.1f}" if got else "none"
        print(f"{lid}  h {span}  after {a.after:g}: {late}/{len(hrs)}  "
              + " ".join(f"{c}:{h:.1f}" if h is not None else f"{c}:?" for c, h in hrs))


if __name__ == "__main__":
    main()
