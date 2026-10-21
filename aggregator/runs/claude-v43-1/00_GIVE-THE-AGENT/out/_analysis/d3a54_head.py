#!/usr/bin/env python3
"""D3a-54's head update: each replacement must match exactly once, or nothing is written. The dimension lines join
the return, the ledgers move to the close-check's counts, the dimension lines' edges join the open list, the reasons
line names move 181, which D3a-53's head left out, and the next comparison is the propose lines. To keep the head
under 3,000 words, three return counts (a layout in-thread, another member answering a call, bare joins) and four
open items (bare refusals against F-014, the chats' split, K01's canvas-call clause, doubt costing uptake) leave the
head; the notes keep them.

  python3 out/_analysis/d3a54_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-53, 2026-10-21 UTC.", "Written at D3a-54, 2026-10-21 UTC."),
    ("## The return (D1a to D3a-53)", "## The return (D1a to D3a-54)"),
    ("guests and hosts [P19] 382.",
     "guests and hosts [P19] 382. **D3a-54.** Dimension lines, 122: no correction; 13 paired elaborations."),
    ("a layout answers design talk in-thread, 111 of 228; another member answers a call in-thread, 430 of 480; "
     "joins come bare, 392 of 411; ", ""),
    ("- **Moves 177 to 180 (developing working hypotheses).**", "- **Moves 177 to 181 (developing working hypotheses).**"),
    ("`adjudications.jsonl`: 40,759 lines ruled, 41,544 with re-rulings; the notes: G1 to G57",
     "`adjudications.jsonl`: 40,881 lines ruled, 41,666 with re-rulings; the notes: G1 to G58"),
    ("- **From D3a-02 to D3a-53**, to weigh after order tests:", "- **From D3a-02 to D3a-54**, to weigh after order tests:"),
    ("P19's request-only rooms (82) and faith hosts (131);",
     "P19's request-only rooms (82) and faith hosts (131); being seen bringing hands, a loop in 5 rooms with no "
     "arrow; dealings bringing members in; D07's returns before hour 73 (27 of 39); T3-016 across the close; the "
     "host's line or strain moving coordination into chats;"),
    ("bare refusals (math-011, wow-050) against F-014; chats (T4-010): sharing split in 19 rooms, scripts held in 6; "
     "K01's canvas-call clause (doubted in 3); doubt costing uptake (9); ", ""),
    ("Dimension lines; then `propose` lines.", "The `propose` lines (1,362), read by lifted node."),
]
t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
    print("wrote", P)
