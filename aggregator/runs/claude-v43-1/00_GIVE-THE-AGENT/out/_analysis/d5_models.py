#!/usr/bin/env python3
"""D5: print, for each named room, the paragraphs of rooms/<sub>/model-D.md that name any of the given tags,
and the paragraph holding its grade. Prints text.

    python3 out/_analysis/d5_models.py --subs greece,pokemon,radiohead --tags P05,A07
"""
import argparse, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--subs", required=True)
ap.add_argument("--tags", required=True)
a = ap.parse_args()
tags = [t for t in a.tags.split(",") if t]
for sub in [s for s in a.subs.split(",") if s]:
    p = os.path.join(ROOT, "out", "rooms", sub, "model-D.md")
    t = open(p, encoding="utf-8").read()
    print("=====", sub, len(t.split()))
    paras = [x.strip() for x in re.split(r"\n\s*\n", t) if x.strip()]
    for x in paras:
        if any("[" + g + "]" in x for g in tags) or "grade:" in x or "local_status" in x:
            print(x)
            print("--")
