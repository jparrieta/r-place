#!/usr/bin/env python3
"""B1e: which entries of out/running-A1.md the scheme drops, and why (section 7).

The running file is the A1 reader's prior, not a source. An entry is dropped from the third-order
scheme when it is not a doing a second-order theme can carry. Five reasons, tested in this order:

  canvas   a fact from the canvas record (linked artworks, writers' shares, placements before hour 0,
           the atlas): measured from pixels, not told in the rooms' words; the canvas fields carry it
  record   a remark about the A1 reading itself (block markers, sides of a block, corrections,
           notes the account weakened, accounts that disagree): about the record, not a doing
  share    a share of a room's coded record (April Fools filling most turns, one member writing most):
           a proportion, which the store's facts and stage C1's counts carry
  brief    the room's week before the canvas (the brief) as the source of a word, mark or habit:
           outside the window B1 places; T3-031 or T3-033 carry the canvas talk that uses it
  sequence an order of events over the week (late, then, after h73, first coded turn): sequencing,
           which stage C takes up; the doings inside it are placed on their own kinds

Every other entry names a doing, and the kinds whose gates take it carry it.
Writes out/_analysis/b1e_running_dropped.tsv (line, reason, entry) and prints the counts.
"""
import collections, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "out", "running-A1.md")
DST = os.path.join(ROOT, "out", "_analysis", "b1e_running_dropped.tsv")

RULES = [
    ("canvas", re.compile(r"canvas fields?|canvas link|canvas linking|the canvas (keeps|keeping|names|links)|linked (artwork|region|work)|"
                          r"writers placed|writers' share|before hour 0|before h0|\batlas\b|region placed|placed from the first hours|"
                          r"predates the room's first call|artwork had placements|art was placed from hour 1|no canvas line|"
                          r"with art placed long before|already on the canvas at the room's first turn", re.I)),
    ("record", re.compile(r"block \d+ begins|early-side rooms|late-side rooms|^\(supersedes|correction to the|none new in block|"
                          r"case\.md corrects|weaken the note's not-this line|coded slices missed|work the note missed|"
                          r"different end than the note held|the note read as restrained|beside a note that stressed|"
                          r"accounts of the same act disagreed|accounts disagreed", re.I)),
    ("brief", re.compile(r"the brief shows|in the brief before the canvas|drew on something in the brief|"
                         r"the room's own week shaped|a sub's own week shaped|joke the room had before the canvas|"
                         r"already running in the room that week", re.I)),
    ("share", re.compile(r"fills? (most|more) coded turns|fill early turns|filling early turns|first days|one member runs most|"
                         r"one coded turn, one deleted author|led by one author|does most of the posting", re.I)),
    ("sequence", re.compile(r"after h73 only|the goal widens late|ally appears only late|then breaks near the end|"
                            r"unanswered for many hours, then|first coded turn announces|late onset room on the canvas|"
                            r"who started the work changed", re.I)),
]
RULES[1] = ("record", re.compile(RULES[1][1].pattern + r"|^(late|early) rooms \(first coded", re.I))
RULES[0] = ("canvas", re.compile(RULES[0][1].pattern.replace(r"\batlas\b", r"the atlas (names|lists)"), re.I))
RULES[0], RULES[1] = RULES[1], RULES[0]   # a remark about the reading is tested first


def main():
    out, counts = [], collections.Counter()
    with open(SRC, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.startswith("- "):
                continue
            entry = line[2:].strip()
            body = re.sub(r"^catch-up block \d+: ", "", entry)
            reason = next((name for name, rx in RULES if rx.search(body)), None)
            counts[reason or "kept"] += 1
            if reason:
                out.append((i, reason, entry))
    with open(DST, "w", encoding="utf-8") as f:
        f.write("line\treason\tentry\n")
        for i, r, e in out:
            f.write("%d\t%s\t%s\n" % (i, r, e.replace("\t", " ")))
    total = sum(counts.values())
    print("entries %d; kept %d; dropped %d: %s" % (total, counts["kept"], total - counts["kept"],
                                                  ", ".join("%s %d" % (k, counts[k]) for k in ("canvas", "record", "share", "brief", "sequence"))))


if __name__ == "__main__":
    main()
