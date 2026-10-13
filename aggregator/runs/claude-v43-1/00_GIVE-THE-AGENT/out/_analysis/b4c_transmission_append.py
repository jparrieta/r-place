#!/usr/bin/env python3
"""B4c: append the paragraphs on the unanimous items a fresh reader placed elsewhere
(out/_analysis/b4c_unanimous/paragraphs-01.md to -08.md, in order) to out/transmission-after-revision-B4.md, under its
last heading, "The unanimous items a fresh reader placed elsewhere". Refuses if that heading is not the file's last
or if any paragraph is already there. Dry run (counts only) without --write.

    python3 out/_analysis/b4c_transmission_append.py [--write]
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(ROOT, "out", "transmission-after-revision-B4.md")
HEAD = "## The unanimous items a fresh reader placed elsewhere"


def main():
    t = open(P, encoding="utf-8").read()
    heads = re.findall(r"^## .*$", t, re.M)
    if not heads or heads[-1] != HEAD:
        sys.exit("the last heading is not %r" % HEAD)
    parts = [open(p, encoding="utf-8").read().strip() for p in sorted(glob.glob(os.path.join(ROOT, "out", "_analysis", "b4c_unanimous", "paragraphs-0*.md")))]
    items = re.findall(r"^\*\*(\S+/t\d+)\*\* \(class", "\n\n".join(parts), re.M)
    if any("**%s**" % i in t for i in items):
        sys.exit("paragraphs are already in the file")
    print("files %d, paragraphs %d" % (len(parts), len(items)))
    if "--write" in sys.argv:
        open(P, "w", encoding="utf-8").write(t.rstrip("\n") + "\n\n" + "\n\n".join(parts) + "\n")
        print("appended to %s" % os.path.relpath(P, ROOT))


if __name__ == "__main__":
    main()
