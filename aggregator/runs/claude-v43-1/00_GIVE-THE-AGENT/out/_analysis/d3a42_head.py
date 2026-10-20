#!/usr/bin/env python3
"""D3a-42's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, some list items are joined into the item before them (no item dropped).

  python3 out/_analysis/d3a42_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-41, 2026-10-20 UTC.", "Last written at D3a-42, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-41)", "## The return (D1a to D3a-42)"),
    ("A01 to A14 stand uncorrected;", "A01 to A15 stand uncorrected;"),
    ("help follows upkeep, 155 of 197, and terms, 179 of 186 (124 more trade in one offer).",
     "help follows upkeep, 155 of 197, and terms, 179 of 186 (124 more trade in one offer); an attack follows a call, "
     "277 of 286 (58 more call over another's work)."),
    ("`adjudications.jsonl`: 32,893 lines ruled, 33,664 with re-rulings; the stage's notes: G1 to G46",
     "`adjudications.jsonl`: 33,549 lines ruled, 34,322 with re-rulings; the stage's notes: G1 to G47"),
    ("- **From D3a-02 to D3a-41**, to weigh after order tests:", "- **From D3a-02 to D3a-42**, to weigh after order tests:"),
    ("A14's one offer beside F-020;", "A14's one offer beside F-020; A15's attacks after the work and one call;"),
    ("by G1 to G46 with G13a and G4a;", "by G1 to G47 with G13a and G4a;"),
    # joins
    ("as you stated them.\"\n- Stage D and every later stage", "as you stated them.\" Stage D and every later stage"),
    ("the eight such lines stand as written.\n- **J, 16 October, 12:59 Berlin:**",
     "the eight such lines stand as written. **J, 16 October, 12:59 Berlin:**"),
    ("its own decision and reason.\n- **QD3-002", "its own decision and reason. **QD3-002"),
    ("says whether it applies backwards.\n- **QD3-003", "says whether it applies backwards. **QD3-003"),
    ("The readers split in 163 rooms.\n- **D3a, by element.**", "The readers split in 163 rooms. **D3a, by element.**"),
    ("in 148 of 190 [A03].\n- **Keeping holds", "in 148 of 190 [A03]. **Keeping holds"),
    ("The head-count claim failed (F-015).\n- **The host", "The head-count claim failed (F-015). **The host"),
    ("coded in 46 rooms [C01, F-006].\n- **Direct information", "coded in 46 rooms [C01, F-006]. **Direct information"),
    ("mostly apart from canvas calls.\n- **Machine hands.**", "mostly apart from canvas calls. **Machine hands.**"),
    ("under strain [A06].\n- **C02**", "under strain [A06]. **C02**"),
    ("names the rival in the attack turn.\n- **Candidates:**", "names the rival in the attack turn. **Candidates:**"),
    ("requests for a leader precede agreements.\n- **Moves 174 and 175",
     "requests for a leader precede agreements. **Moves 174 and 175"),
    ("state the limits of'.\n- **J, 15 October, 01:29 Berlin:**", "state the limits of'. **J, 15 October, 01:29 Berlin:**"),
    ("kappa of 0.19.\n- **Questions:** none open.", "kappa of 0.19. **Questions:** none open."),
    ("go back on what others said\".\n- **J's rulings (06:45", "go back on what others said\". **J's rulings (06:45"),
    ("`also_present` `{}`.\n- **Fleet ids", "`also_present` `{}`. **Fleet ids"),
    ("P21's four forms;\n  - P15's:", "P21's four forms; P15's:"),
    ("recording after a loss (A08);\n  - a finished work", "recording after a loss (A08); a finished work"),
    ("P22's two forms;\n  - the host's moderation", "P22's two forms; the host's moderation"),
    ("against F-014;\n  - chats (T4-010)", "against F-014; chats (T4-010)"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
