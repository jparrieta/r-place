#!/usr/bin/env python3
"""Print chosen concepts of one room from the store, label and words whole. Read-only.

    python3 out/_analysis/b4_concepts.py MMA c0181 c0216
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    sub, ids = sys.argv[1], set(sys.argv[2:])
    for ln in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
        c = json.loads(ln)
        if c["sub"] == sub and c["code_id"] in ids:
            print("%s %s | %s | %s" % (c["code_id"], c["theme_id"], c.get("first_order", ""), " ".join(str(c.get("text", "")).split())))


if __name__ == "__main__":
    main()
