#!/usr/bin/env python3
"""C5c-08, problem 1 (the unit): a descriptive check, not a test. For the fourth-order themes under the elements whose
actor was restored to the room, the share of concepts whose quoted words use the first person plural (we, us, our,
ours, let's, lets) and the share using the first person singular only (I, me, my, mine, I'm, I'll, I've). A plural
pronoun shows a member speaking as part of a group; it does not show which group, or that the room agreed. Writes
nothing.

    python3 out/_analysis/c5c8_unit_we.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THEMES = {"T4-005": "P01 calls", "T4-007": "P03 building and reporting", "T4-013": "P05 upkeep",
          "T4-016": "P08 border talk", "T4-018": "P17 coalitions", "T4-014": "Territoriality",
          "T4-028": "P13 carrying on", "T4-020": "P09 attack (contrast)"}
WE = re.compile(r"\b(we|us|our|ours|let'?s)\b", re.I)
I = re.compile(r"\b(i|me|my|mine|i'm|i'll|i've|im)\b", re.I)


def codes(t4):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--fourth", t4, "--json",
                        "--limit", "10000000"], cwd=ROOT, capture_output=True, text=True)
    return [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]


print("%-7s %-28s %6s %8s %8s %8s" % ("theme", "element", "n", "plural", "I only", "neither"))
for t, name in THEMES.items():
    rows = codes(t)
    n = len(rows)
    w = sum(1 for r in rows if WE.search(r.get("text") or ""))
    s = sum(1 for r in rows if not WE.search(r.get("text") or "") and I.search(r.get("text") or ""))
    print("%-7s %-28s %6d %7.2f%% %7.2f%% %7.2f%%" % (t, name, n, 100.0 * w / n, 100.0 * s / n,
                                                     100.0 * (n - w - s) / n) if n else "%s: no concepts" % t)
