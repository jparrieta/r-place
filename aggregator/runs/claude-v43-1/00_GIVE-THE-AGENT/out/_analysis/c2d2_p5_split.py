#!/usr/bin/env python3
"""C2d-02: count the pass 5 story verdicts (story_rooms-p5.jsonl) by verdict and by why each room was drawn
(within-case, carried from pass 4's residue, fresh), and print pass 4's split beside it for the trend.
Reads the story files only; writes nothing.

    python3 out/_analysis/c2d2_p5_split.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(n):
    with open(os.path.join(ROOT, "out", "story_rooms-p%d.jsonl" % n), encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    draw = dict((d["sub"], d["why_drawn"]) for d in rows[0]["draw"])
    return draw, [r for r in rows[1:] if r.get("sub")]


def group(why):
    if why.startswith("within-case"):
        return "within-case"
    if why.startswith("told-with-residue at pass"):
        return "carried"
    return "fresh"


for n in (4, 5):
    draw, verdicts = load(n)
    total = collections.Counter(v["verdict"] for v in verdicts)
    split = collections.defaultdict(collections.Counter)
    names = collections.defaultdict(list)
    for v in verdicts:
        g = group(draw[v["sub"]])
        split[g][v["verdict"]] += 1
        names[(g, v["verdict"])].append(v["sub"])
    print("pass %d: %d verdicts; told %d, told-with-residue %d, not-told %d" % (
        n, len(verdicts), total["told"], total["told-with-residue"], total["not-told"]))
    for g in ("within-case", "carried", "fresh"):
        c = split[g]
        print("  %-11s told %2d  told-with-residue %2d  not-told %d" % (g, c["told"], c["told-with-residue"], c["not-told"]))
        for verdict in ("told", "told-with-residue", "not-told"):
            if names[(g, verdict)]:
                print("    %s: %s" % (verdict, ", ".join(sorted(names[(g, verdict)], key=str.lower))))
