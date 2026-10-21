#!/usr/bin/env python3
"""D3a-55's head update: each replacement must match exactly once, or nothing is written. The propose lines join
the return, the fifteen candidates join the account and the reasons, the ledgers move to the close-check's counts,
the open list loses the items the candidates now hold (dealings bringing members in, D07's early returns, T3-016
across the close, canvas-born rooms, what a mark brings back) and gains the candidates' order tests and T3-017's
scope, and the next comparison is the verdicts and the uncomposed rooms. To keep the head under 3,000 words, the
sixteen order counts on the return's lines become one sentence with their range; the notes keep every count and
every item cut.

  python3 out/_analysis/d3a55_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Written at D3a-54, 2026-10-21 UTC.", "Written at D3a-55, 2026-10-21 UTC."),
    ("Moves 172 to 181 moved the hash;", "Moves 172 to 196 moved the hash;"),
    ("## The return (D1a to D3a-54)", "## The return (D1a to D3a-55)"),
    ("A01 to A20 stand uncorrected; 222 rooms start and call in one post; keeping follows a report, 308 of 331; talk "
     "follows keeping, 141 of 265; sparing follows terms, 227 of 295; machine hands follow upkeep, 87 of 144; marking "
     "follows a report, 131 of 156; records follow marking, 232 of 240; carrying on follows a record, 163 of 184; moves "
     "follow doubt, 112 of 159; help follows upkeep, 155 of 197, and terms, 179 of 186; coalitions follow upkeep, 49 of "
     "67; host lines follow calls, 148 of 164; an attack follows a call, 277 of 286; restraint (319 of 322), terms (213 "
     "of 230) and taunts (169 of 177) follow an attack.",
     "A01 to A20 stand uncorrected. On the return's lines each stated order holds in more than half the rooms that "
     "carry both ends, from talk after keeping (141 of 265) to restraint after an attack (319 of 322); the notes give "
     "each count."),
    ("Dimension lines, 122: no correction; 13 paired elaborations.",
     "Dimension lines, 122: no correction; 13 paired elaborations. **D3a-55.** `propose` lines, 1,362: 729 accepted "
     "into 15 candidates, 178 held by the model, 455 particulars or not shown."),
    ("30 elements stand.",
     "30 elements stand. **Fifteen candidates** (P23 to P34, K05 to K07) entered from the `propose` lines: chats, "
     "explaining the canvas, people the work brings in, new jokes, the spot before a loss, rooms the canvas made, "
     "offence, the people the mark shows, fair covering, strain, hidden plans, spite at the room's own mark, members' "
     "time and devices, the site, and members of both rooms."),
    ("- **Moves 177 to 181 (developing working hypotheses).**",
     "- **Moves 182 to 196 (developing working hypotheses).** Fifteen candidates enter; no element or arrow states "
     "them (G59a). **Moves 177 to 181.**"),
    ("`adjudications.jsonl`: 40,881 lines ruled, 41,666 with re-rulings; the notes: G1 to G58 (ten of them amended once)",
     "`adjudications.jsonl`: 42,243 lines ruled, 43,028 with re-rulings; the notes: G1 to G59 (eleven of them amended once)"),
    ("model history 155; findings 37 (23 findings); elements 30 (all standing); arrows 21.",
     "model history 170; findings 37 (23 findings); elements 45 (30 standing, 15 candidates); arrows 21."),
    ("- **From D3a-02 to D3a-54**, to weigh after order tests:", "- **From D3a-02 to D3a-55**, to weigh after order tests:"),
    ("removals sending talk elsewhere; canvas-born rooms;", "removals sending talk elsewhere;"),
    ("being seen bringing hands, a loop in 5 rooms with no arrow; dealings bringing members in; D07's returns before "
     "hour 73 (27 of 39); T3-016 across the close; the host's line or strain moving coordination into chats;",
     "being seen bringing hands (P25, P05; 5 rooms); P20's edge to P23; the candidates' order tests; T3-017's 251 "
     "lines (scope);"),
    ("what a mark brings back; ", ""),
    ("The `propose` lines (1,362), read by lifted node. The split and 19 story-miss rooms await the verdicts.",
     "The verdicts and the uncomposed rooms (§4), with the 19 story-miss rooms."),
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
