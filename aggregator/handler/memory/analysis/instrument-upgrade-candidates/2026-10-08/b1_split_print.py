"""Cut a member print (b1_theme_members.py output) into part files under a byte limit, breaking
only at member boundaries ('#N' lines); each line is cut at --width characters. Read-only on the
input. usage: python3 out/_analysis/b1_split_print.py <in.txt> <out_prefix> [--limit 27000] [--width 330]
writes <out_prefix>01.txt, 02 ... and prints each part's members, lines and bytes."""
import sys

a = sys.argv[1:]
src, pre = a[0], a[1]
limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 27000
width = int(a[a.index("--width") + 1]) if "--width" in a else 330
blocks, cur = [], []
for l in open(src, encoding="utf-8"):
    l = l.rstrip("\n")
    if l.startswith("note: placements"):
        continue
    if l.startswith("#") and l[1:].isdigit() and cur:
        blocks.append(cur)
        cur = []
    cur.append(l[:width])
if cur:
    blocks.append(cur)
parts, part, size = [], [], 0
for b in blocks:
    n = sum(len(x.encode("utf-8")) + 1 for x in b)
    if part and size + n > limit:
        parts.append(part)
        part, size = [], 0
    part.append(b)
    size += n
if part:
    parts.append(part)
for i, p in enumerate(parts, 1):
    text = "\n".join(x for b in p for x in b) + "\n"
    open("%s%02d.txt" % (pre, i), "w", encoding="utf-8").write(text)
    print("part %02d: %s to %s, %d lines, %d bytes" % (i, p[0][0], p[-1][0], text.count("\n"), len(text.encode("utf-8"))))
