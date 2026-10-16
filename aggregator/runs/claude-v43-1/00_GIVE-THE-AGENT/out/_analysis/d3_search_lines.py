#!/usr/bin/env python3
"""Search one element's lines (all ops) for a regex in their how, codes and source label, through
d3_packet.py, and print the matching line blocks whole. A search aid for finding a second room;
every ruling still rests on the line as read whole.

  python3 out/_analysis/d3_search_lines.py --element P04 --regex 'truce|neighbo'
"""
import argparse
import re
import subprocess
import sys

OPS = ("absent", "add-condition", "add-step", "instantiate", "link", "restrict", "contradict")


def blocks(element, op):
    head = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element,
                           "--op", op, "--offset", "0", "--limit", "1"],
                          capture_output=True, text=True).stdout
    m = re.search(r"(\d+) lines in all", head)
    total = int(m.group(1)) if m else 0
    for off in range(0, total, 100):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element,
                              "--op", op, "--offset", str(off), "--limit", "100"],
                             capture_output=True, text=True).stdout
        for blk in out.split("\n== ")[1:]:
            yield "== " + blk.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--regex", required=True)
    a = ap.parse_args()
    rx = re.compile(a.regex, re.I)
    n = 0
    for op in OPS:
        for blk in blocks(a.element, op):
            if rx.search(blk):
                n += 1
                print(blk + "\n")
    print(f"[{n} lines match]")


if __name__ == "__main__":
    main()
