#!/usr/bin/env python3
"""B4c, read-only: tally the verdicts of the paragraphs on the unanimous items a fresh reader placed elsewhere
(out/_analysis/b4c_unanimous/paragraphs-0N.md), by class, and check that every item of b4c_figures.json's
unanimous_either_arm has exactly one paragraph and no other item has one.

Verdict words, as written in the paragraphs: "the fleet's shared assumption", "the settled line keeps my B1 theme",
"rule 0 applied differently", "the scheme does not decide", "the fresh reading(s) miss(es) a field".

    python3 out/_analysis/b4c_unanimous_tally.py
"""
import collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
KINDS = (("fleet", r"^the fleet's shared assumption"), ("b1 kept", r"^the settled line keeps my B1 theme"),
         ("rule 0", r"^rule 0 applied differently"), ("undecided", r"^the scheme does not decide"),
         ("fresh miss", r"^the fresh readings? miss"))


def main():
    figs = json.load(open(os.path.join(AN, "b4c_figures.json"), encoding="utf-8"))
    want = set(figs["unanimous_either_arm"])
    seen, tally, rows, errs = collections.Counter(), collections.Counter(), [], []
    for p in sorted(glob.glob(os.path.join(AN, "b4c_unanimous", "paragraphs-0*.md"))):
        for para in open(p, encoding="utf-8").read().split("\n\n"):
            m = re.match(r"^\*\*(\S+/t\d+)\*\* \(class (\d)", para.strip())
            if not m:
                continue
            item, cls = m.group(1), int(m.group(2))
            seen[item] += 1
            v = re.search(r"Verdict: ([^.]*)", para)
            kind = next((k for k, rx in KINDS if v and re.match(rx, v.group(1))), None)
            if not kind:
                errs.append("%s: no verdict in the fixed words" % item)
            tally[(cls, kind)] += 1
            rows.append((item, cls, kind))
    missing = sorted(want - set(seen))
    extra = sorted(set(seen) - want)
    twice = sorted(k for k, n in seen.items() if n > 1)
    print("paragraphs %d; items due %d; missing %s; extra %s; twice %s" % (len(rows), len(want), missing, extra, twice))
    for cls in (1, 2):
        print("class %d: %s" % (cls, {k: tally[(cls, k)] for k, _ in KINDS}))
    print("all: %s" % {k: sum(tally[(c, k)] for c in (1, 2)) for k, _ in KINDS})
    for e in errs:
        print("ERROR " + e)
    if missing or extra or twice or errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
