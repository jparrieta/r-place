#!/usr/bin/env python3
"""Print each line of notes-D3.md that names an id, with a window of text around the first mention.

  python3 out/_analysis/d3_notes_mentions.py P21 --before 220 --after 200
"""
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--before", type=int, default=220)
    ap.add_argument("--after", type=int, default=200)
    ap.add_argument("--file", default="out/notes-D3.md")
    a = ap.parse_args()
    for i, line in enumerate(open(a.file).read().split("\n"), 1):
        j = line.find(a.id)
        if j >= 0:
            print(i, "|", line[max(0, j - a.before):j + a.after])


if __name__ == "__main__":
    main()
