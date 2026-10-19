#!/usr/bin/env python3
"""D3a-30: move four A03 instantiate spec lines from J to O after the reading that a concept reporting building
with damage at once, followed by a later act of upkeep, shows the order. Each old line must match exactly once.

  python3 out/_analysis/d3a30_spec_fix.py [--write]
"""
import sys

P = "out/_analysis/d3_rulings/A03-inst-spec.txt"
REPL = [
    ("belgium-037|J|c0003 a member contributing to the flag while people keep defacing it, report and damage together, then c0050 edges cleaned",
     "belgium-037|O|c0003 a member reporting work on the flag while people keep defacing it, then c0050 edges cleaned against the void"),
    ("eagles-039|J|c0012 Eagles being spelled while someone tries to mess it up, building and damage together, then c0017 and c0018 repairs",
     "eagles-039|O|c0012 Eagles reported being spelled while someone tries to mess it up, then c0017 a call after the S becomes an 8 and c0018 the E fought back into shape"),
    ("ethoslab-036|J|c0006 the letters continued while the e disappears, building and damage together, then c0029 a call while the face is overrun",
     "ethoslab-036|O|c0006 the letters reported continued while the e disappears, then c0029 a call for help while the face is overrun"),
    ("europe-042|J|c0048 faster progress, misaligned stars and an attack from the black void in one report, then c0050 defence",
     "europe-042|O|c0048 faster progress and misaligned stars reported with an attack from the black void, then c0050 the flag defended from the black tentacles"),
]
t = open(P).read()
for old, new in REPL:
    n = t.count(old + "\n")
    assert n == 1, (n, old[:40])
    t = t.replace(old + "\n", new + "\n")
print("all %d replacements match once" % len(REPL))
if "--write" in sys.argv:
    open(P, "w").write(t)
    print("written", P)
