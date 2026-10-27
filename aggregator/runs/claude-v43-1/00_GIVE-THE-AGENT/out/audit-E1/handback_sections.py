#!/usr/bin/env python3
"""E1e: the handbacks' sections that the experience is written against, printed whole, stage by stage.

    python3 out/audit-E1/handback_sections.py > out/audit-E1/handback_sections.md

A section is taken whole when its heading names what the stage delivered or claimed, what was not done as the stage
file says, what is wrong with the instrument, what the analyst was sure of or not, what the next stage should know,
the reviewer or readers, or the slips. Every other section is listed by its heading only.
"""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
KEEP = re.compile(r"deliver|claim|did not do|wrong with the instrument|sure of|should know|reviewer|readers|slips|"
                  r"corner|instrument asked", re.I)
ORDER = ["A1", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "C5-p14", "C5", "D1", "D2", "D3", "D4",
         "D5-room-forms", "D5", "D6"]


def main():
    for s in ORDER:
        p = os.path.join(OUT, "handback-%s.md" % s)
        t = open(p, encoding="utf-8").read()
        parts = re.split(r"(?m)^(#{2,3} .+)$", t)
        print("\n# handback-%s.md\n" % s)
        for i in range(1, len(parts), 2):
            head, body = parts[i], parts[i + 1]
            if KEEP.search(head):
                print(head + "\n" + body.strip() + "\n")
            else:
                print(head + " (not printed)\n")


if __name__ == "__main__":
    main()
