#!/usr/bin/env python3
"""D3a-43's head update: each replacement must match exactly once, or nothing is written. To stay within 3,000
words, some list items are joined into the item before them (no item dropped).

  python3 out/_analysis/d3a43_head.py [--write]
"""
import sys

P = "out/_head.md"
REPL = [
    ("Last written at D3a-42, 2026-10-20 UTC.", "Last written at D3a-43, 2026-10-20 UTC."),
    ("## The return (D1a to D3a-42)", "## The return (D1a to D3a-43)"),
    ("A01 to A15 stand uncorrected;", "A01 to A16 stand uncorrected;"),
    ("an attack follows a call, 277 of 286 (58 more call over another's work).\n- **D3a-15 to D3a-26.**",
     "an attack follows a call, 277 of 286 (58 more call over another's work); restraint follows an attack, "
     "319 of 322. **D3a-15 to D3a-26.**"),
    ("`adjudications.jsonl`: 33,549 lines ruled, 34,322 with re-rulings; the stage's notes: G1 to G47",
     "`adjudications.jsonl`: 34,246 lines ruled, 35,019 with re-rulings; the stage's notes: G1 to G48"),
    ("- **From D3a-02 to D3a-42**, to weigh after order tests:", "- **From D3a-02 to D3a-43**, to weigh after order tests:"),
    ("A15's attacks after the work and one call;\n  - P09's:",
     "A15's attacks after the work and one call; A16's reasons, lone bound and visitors' calls; P09's:"),
    ("by G1 to G47 with G13a and G4a;", "by G1 to G48 with G13a and G4a;"),
    # joins
    ("two questions in view.\"\n- **QD1-001", "two questions in view.\" **QD1-001"),
    ("where repairs bear on a ruling.\n- **QD3-001", "where repairs bear on a ruling. **QD3-001"),
    ("bound their understanding.\"\n- **J, 16 October, 19:08", "bound their understanding.\" **J, 16 October, 19:08"),
    ("and border talk [A17].\n- **Loss** (thin).", "and border talk [A17]. **Loss** (thin)."),
    ("No loop is grounded.\n- **The close.**", "No loop is grounded. **The close.**"),
    ("Carrying on stays apart [P13].\n- **The frame**", "Carrying on stays apart [P13]. **The frame**"),
    ("and the field's entries.\n- **Ledgers (lines):**", "and the field's entries. **Ledgers (lines):**"),
    ("arrows 21.\n- **Still open:**", "arrows 21. **Still open:**"),
    ("all 34 count.\n- **Reading rules", "all 34 count. **Reading rules"),
    ("a possible loop;\n  - P20's:", "a possible loop; P20's:"),
    ("(criticalrole);\n  - at D3c:", "(criticalrole); at D3c:"),
    ("after doubt;\n  - P19's form", "after doubt; P19's form"),
    ("(no arrow);\n  - machine hands", "(no arrow); machine hands"),
    ("wait for clustering.\n- **From D1a:**", "wait for clustering. **From D1a:**"),
    ("and snap it.\n- **Writing and checks.**", "and snap it. **Writing and checks.**"),
    ("the earlier line stays.\n- **The permission check refuses**",
     "the earlier line stays. **The permission check refuses**"),
]

t = open(P).read()
for old, new in REPL:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
print("all %d replacements match once; words after: %d" % (len(REPL), len(t.split())))
if "--write" in sys.argv:
    open(P, "w").write(t)
