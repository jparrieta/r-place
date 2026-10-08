"""Writers who appear in two concept dumps (from b1_room_codes.py or mem.py codes), with the
concepts each wrote in both. Deleted authors and truncated names ending in an ellipsis are kept
as printed, so a truncated name is matched only against the same truncation.

usage: python3 out/_analysis/b1_shared_authors.py <dump_a> <dump_b>
"""
import re
import sys
from collections import defaultdict

LINE = re.compile(r"^(c\d{4})\s+(\S+)\s+(t\d+)\s+h\s*\+?\s*([\d.]+)\s+(\S+)\s+@")


def read(path):
    out = defaultdict(list)
    for line in open(path, encoding="utf-8"):
        m = LINE.match(line)
        if m and m.group(5) != "[deleted]":
            out[m.group(5)].append("%s %s h%s" % (m.group(2), m.group(1), m.group(4)))
    return out


a, b = read(sys.argv[1]), read(sys.argv[2])
shared = sorted(set(a) & set(b))
for name in shared:
    print("%s\n  %s\n  %s" % (name, "; ".join(a[name][:6]), "; ".join(b[name][:6])))
print("%d shared writers" % len(shared))
