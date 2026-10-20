#!/usr/bin/env python3
"""D3a-37: turn the double-quoted quotes in spec parts into single-quoted ones, so that d3_spec_quotes.py checks them.

A double-quoted segment starts at a " after a space, '(' or '|' and ends at the next ". It is turned only where its
text holds no apostrophe that d3_spec_quotes.py would read as a closing quote (one followed by a space, a comma, a
semicolon, a full stop, a closing bracket or the segment's end); those are listed and left as they are. Without
--write it prints what it would change; with --write it rewrites each file in place (the rows keep their order).

  python3 out/_analysis/d3_dq_to_sq.py FILE [FILE ...] [--write]
"""
import re
import sys

write = "--write" in sys.argv
files = [f for f in sys.argv[1:] if f != "--write"]
DQ = re.compile(r'(?<=[\s(|])"([^"]+)"')
BAD = re.compile(r"'(?=[\s,;.)]|$)")
turned = kept = 0
for f in files:
    rows = open(f, encoding="utf-8").read().split("\n")
    out = []
    for r in rows:
        def fix(m):
            global turned, kept
            s = m.group(1)
            if BAD.search(s):
                kept += 1
                print("KEPT %s: %s" % (f.rsplit("/", 1)[-1], s[:120]))
                return m.group(0)
            turned += 1
            return "'" + s + "'"
        out.append(DQ.sub(fix, r))
    if write:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out))
print("segments turned: %d; kept double-quoted: %d; written: %s" % (turned, kept, write))
