#!/usr/bin/env python3
"""Print the codes of members who write in two rooms, from dumps made by b1_dump_rooms.py.

Usage: b1_shared_detail.py <dumpdir> <room> <partner> [--width N] [--hours LO HI]

Reads <dumpdir>/d_<room>.txt and <dumpdir>/d_<partner>.txt, finds authors present in both
(AutoModerator and [deleted] ignored), and prints each shared author's codes in both rooms,
sorted by hour, cut to --width characters (default 230). --hours keeps codes inside the window.
Read-only; writes nothing.
"""
import os
import re
import sys

LINE = re.compile(r"^(c\d{4})\s+(\S+)\s+(t\d+)\s+h\s+([+-]?\d+(?:\.\d+)?)\s+(\S+)\s+(\S+)\s+\|(.*)$")
IGNORE = {"AutoModerator", "[deleted]", "-"}


def load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            m = LINE.match(raw)
            if not m:
                continue
            code, room, theme, hour, author, item, rest = m.groups()
            rows.append((float(hour), author, raw))
    return rows


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    ddir, room, partner = argv[1], argv[2], argv[3]
    width = 230
    lo, hi = None, None
    if "--width" in argv:
        width = int(argv[argv.index("--width") + 1])
    if "--hours" in argv:
        i = argv.index("--hours")
        lo, hi = float(argv[i + 1]), float(argv[i + 2])
    a = load(os.path.join(ddir, "d_%s.txt" % room))
    b = load(os.path.join(ddir, "d_%s.txt" % partner))
    shared = sorted(({r[1] for r in a} & {r[1] for r in b}) - IGNORE)
    print("%s and %s: %d shared" % (room, partner, len(shared)))
    for author in shared:
        rows = [r for r in a + b if r[1] == author]
        if lo is not None:
            rows = [r for r in rows if lo <= r[0] <= hi]
        rows.sort(key=lambda r: r[0])
        print("== %s (%d codes)" % (author, len(rows)))
        for r in rows:
            print("  " + r[2][:width])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
