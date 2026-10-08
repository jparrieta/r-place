"""Writers shared between one room's concept dump and each of several others, with the hours
each wrote in both; dumps come from b1_room_codes.py. Deleted authors and AutoModerator are left out.

usage: python3 out/_analysis/b1_shared_many.py <dump_a> <dump_b> [<dump_c> ...]
"""
import re
import sys
from collections import defaultdict

LINE = re.compile(r"^(c\d{4})\s+(\S+)\s+(t\d+)\s+h\s*\+?\s*([\d.]+)\s+(\S+)\s+@")
SKIP = {"[deleted]", "AutoModerator"}


def read(path):
    out, room = defaultdict(list), None
    for line in open(path, encoding="utf-8"):
        m = LINE.match(line)
        if m and m.group(5) not in SKIP:
            room = m.group(2)
            out[m.group(5)].append("%s h%s" % (m.group(1), m.group(4)))
    return room, out


name_a, a = read(sys.argv[1])
for path in sys.argv[2:]:
    name_b, b = read(path)
    shared = sorted(set(a) & set(b))
    print("%s / %s: %d shared writers" % (name_a, name_b, len(shared)))
    for w in shared:
        print("  %s | %s: %s | %s: %s" % (w, name_a, ", ".join(a[w][:5]), name_b, ", ".join(b[w][:5])))
