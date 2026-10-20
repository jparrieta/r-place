#!/usr/bin/env python3
"""D3a-39's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, nested rule lists are joined into one line each (no rule dropped), and two spent sentences of QC2-002 are cut
and marked.

  python3 out/_analysis/d3a39_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-38, 2026-10-20 UTC.", "Last written at D3a-39, 2026-10-20 UTC."),
    ("- **QD3-007:** A07's bound keeps its words; marking an ended attempt is a P11 subform, for the clustering.",
     "- **QD3-007:** A07's bound keeps its words; marking an ended attempt is a P11 subform, for the clustering.\n"
     "- **QD3-008 (J):** option 2: A11's 'settled' goes to D3c; wording questions without a correction are mine, "
     "logged."),
    ("- **J, 16 October, 19:08 Berlin, on drift (carry it):**\n  - Re-orient",
     "- **J, 16 October, 19:08 Berlin, on drift (carry it):** Re-orient"),
    ("arrows and history.\n  - Make a blind", "arrows and history. Make a blind"),
    ("the handler's kappa.\n  - A ruling rule changes", "the handler's kappa. A ruling rule changes"),
    ("## The return (D1a to D3a-38)", "## The return (D1a to D3a-39)"),
    ("A01 to A11 stand uncorrected;", "A01 to A12 stand uncorrected;"),
    ("a layout answers design talk in-thread, 111 of 228.",
     "a layout answers design talk in-thread, 111 of 228; another member answers a call in-thread, 430 of 480; "
     "joins come bare, 392 of 411."),
    ("`adjudications.jsonl`: 30,822 lines ruled, 31,590 with re-rulings;",
     "`adjudications.jsonl`: 31,569 lines ruled, 32,338 with re-rulings;"),
    ("the stage's notes: G1 to G43 (six of them amended once)", "the stage's notes: G1 to G44 (six of them amended once)"),
    ("- **Questions:** QD3-008 open (A11's 'settled').", "- **Questions:** none open."),
    ("- **J's ruling on QC2-002, verbatim:**", "- **J's ruling on QC2-002 (two spent sentences cut):**"),
    (" Work pass 5 from pass 4's state.", ""),
    (" This is the last closing pass.", ""),
    ("- **Reading rules (`scheme_v2.md`).**\n  - A theme", "- **Reading rules (`scheme_v2.md`).** A theme"),
    ("(the visitor rule).\n  - \"The work\"", "(the visitor rule). \"The work\""),
    ("names another's.\n  - A bare mention", "names another's. A bare mention"),
    ("holds no act.\n  - Help between rooms", "holds no act. Help between rooms"),
    ("- **From D3a-02 to D3a-38**, to weigh after order tests:", "- **From D3a-02 to D3a-39**, to weigh after order tests:"),
    ("A11's template-first rooms;", "A11's template-first rooms; A12's reason test and starts joined;"),
    ("- **Checking.**\n  - Never type", "- **Checking.** Never type"),
    ("check with a script.\n  - Never log", "check with a script. Never log"),
    ("after appending.\n  - Check a claim", "after appending. Check a claim"),
    ("- **Logging.**\n  - There is no", "- **Logging.** There is no"),
    ("log closes as notes.\n  - Log an abductive", "log closes as notes. Log an abductive"),
    ("rules written first.\n  - Log every move", "rules written first. Log every move"),
    ("- **Writing and checks.**\n  - Never put a placeholder", "- **Writing and checks.** Never put a placeholder"),
    ("no-op in a command.\n  - Never put an Edit", "no-op in a command. Never put an Edit"),
    ("check in one turn.\n  - Never run two", "check in one turn. Never run two"),
    ("file in parallel.\n  - Count the head's", "file in parallel. Count the head's"),
    ("- **Ledger formats.**\n  - A superseding", "- **Ledger formats.** A superseding"),
    ("is the bare id.\n  - Every arrow", "is the bare id. Every arrow"),
    ("`negative_check`.\n  - The head never", "`negative_check`. The head never"),
    ("proposition id.\n  - A re-ruling", "proposition id. A re-ruling"),
    ("- **The permission check refuses:**\n  - deleting a file, even a link;\n  - shell variables",
     "- **The permission check refuses** deleting any file or link; shell variables"),
    ("words beginning \"for_\";\n  - `find -exec`", "words beginning \"for_\"; `find -exec`"),
    ("env-var prefixes;\n  - cat or jq on `out/diary/`; `cut -c` after any read, `cite.py` or a helper; `head -n -N`.\n\n"
     "  Write a script", "env-var prefixes; cat or jq on `out/diary/`; `cut` after a read or a helper; `head -n -N`. Write a script"),
    ("The unruled groups (other arrows, candidates, dimension lines), by G1 to G43 with G13a and G4a;",
     "The unruled groups (other arrows, candidates, dimension lines), by G1 to G44 with G13a and G4a;"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
