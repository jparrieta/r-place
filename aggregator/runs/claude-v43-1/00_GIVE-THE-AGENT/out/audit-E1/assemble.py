#!/usr/bin/env python3
"""E1d: audit-E1.md assembled from its parts, as planned at E1a (notes-E1.md, "The audit sections I plan").

    python3 out/audit-E1/assemble.py > out/audit-E1.md
    python3 out/audit-E1/assemble.py --manifest > out/audit-E1/assemble.json

The parts are joined whole, in the order of the stage file's sections, with no word changed: the preface below;
section-01.md to section-07.md (stage sections 1 to 3, written at E1b-01 to E1b-07); section-09.md and section-10.md
(stage sections 4 and 5, E1d); section-11.md (the composition result, E1d); section-08.md (stage sections 6 and 7,
E1b-08); section-12.md (the methods paragraph, stage section 8, last). The manifest mode prints each part's sha256
and word count.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["section-01.e1d.md", "section-02.md", "section-03.e1d.md", "section-04.md", "section-05.e1d.md", "section-06.md",
         "section-07.md", "section-09.md", "section-10.md", "section-11.md", "section-08.md", "section-12.md"]
# section-01, -03 and -05 enter as the superseding copies of supersede_parts.py (E1d, after the first close-check);
# the originals are unchanged beside them.
PREFACE = """# Audit of the run (stage E1)

Assembled at E1d, 28 October 2026, by `audit-E1/assemble.py` from the parts in `audit-E1/`, joined whole and in this order. Every figure in it comes from a script in `audit-E1/`, with its rule in its docstring and its output beside it, or from a reading by hand that the diary logs. Nothing in it comes from anyone's account of itself, mine included. Where a figure computed here differs from an earlier file, the part says which is wrong.

| part | stage E1 section | written at |
|---|---|---|
| section 1, parts 1 to 5 | 1: scripts over the record | E1b-01 to E1b-05 |
| section 2 | 2: the ledgers, the stories, what a reader was given | E1b-06 |
| section 3 | 3: composition at each level, expectations and contrasts | E1b-07 |
| section 4 | 4: the reconstruction sample | E1d |
| section 5 | 5: versioned judgments, side by side | E1d |
| the composition result | 3 and the closing instruction | E1d |
| sections 6 and 7 | 6: which stage was load-bearing; 7: what the study cannot say | E1b-08 |
| the methods paragraph | 8 | E1d |

The parts written before E1d say that the reconstruction had not yet run. Sections 4 and 5 and the composition result report it. Where section 3 and sections 6 and 7 say the leaf waits on the reconstruction, the composition result gives its outcome.
"""


def main():
    parts = [(n, open(os.path.join(HERE, n), encoding="utf-8").read()) for n in ORDER]
    if "--manifest" in sys.argv:
        print(json.dumps({"order": ORDER, "parts": [{"file": n, "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest(),
                                                     "words": len(t.split())} for n, t in parts],
                          "preface_words": len(PREFACE.split())}, indent=1))
        return
    sys.stdout.write(PREFACE)
    for _n, t in parts:
        sys.stdout.write("\n" + t.rstrip("\n") + "\n")


if __name__ == "__main__":
    sys.exit(main())
