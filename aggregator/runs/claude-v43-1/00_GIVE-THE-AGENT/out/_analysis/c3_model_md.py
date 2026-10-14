#!/usr/bin/env python3
"""Stage C3: write out/model-C3.md, a whole file superseding model-p5.md (rule 18). It is model-p5.md with the stage C3
changes written in: a section saying what stage C3 changed; the decided-order bound (C3a); the mechanisms of A12 and A16
from conversation analysis, read from model/arrows.jsonl, each beside its stage C2 sentence (C3b). Every replaced
passage must be found exactly once. Refuses to overwrite an existing model-C3.md unless --replace is given (a later C3
leg regenerates it whole and says so in its notes).

    python3 out/_analysis/c3_model_md.py [--replace]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SRC = os.path.join(OUT, "model-p5.md")
DEST = os.path.join(OUT, "model-C3.md")
if os.path.exists(DEST) and "--replace" not in sys.argv:
    sys.exit("out/model-C3.md exists; pass --replace to regenerate it whole")
txt = open(SRC, encoding="utf-8").read()
A = dict((r["id"], r) for r in (json.loads(l) for l in open(os.path.join(OUT, "model", "arrows.jsonl"), encoding="utf-8")))
for aid in ("A12", "A16"):
    if A[aid].get("mechanism_source") != "from-literature":
        sys.exit("%s carries no mechanism from the literature" % aid)

C3 = """## What stage C3 changed

This file supersedes `model-p5.md` whole (rule 18). Stage C3 read the pass 5 model against the explanation literature; what each work did is in `literature-C3.md`. Stage C3 changed:
- **A bound on decided order (C3a).** F-006 is superseded by a bounded line, prompted by O'Mahony and Ferraro (2007, verified). Decided order gathers in the small canvas-born factions that govern a territory or rule on guests: 7 of 39 such rooms carry it, against 39 of 666 others, held to room size (p 0.014), and only in the smaller rooms. C01's statement is unchanged.
- **Two mechanisms from a distant field (C3b).** The mechanisms of A12 (the one-line answer to a call) and A16 (an attack call refused inside the room) are taken from conversation analysis (recalled: Schegloff and Sacks 1973; Pomerantz 1984; Levinson 1983). A call is the first part of a pair. Joining is the preferred answer and comes bare; refusing is dispreferred and comes with a reason, which in a refusal of an attack call states the room's norm or the attack's cost. Tested on attack calls (F-014): refusals gave a reason in 23 of 38 read pairs, acceptances in 2 of 14. The stage C2 sentences are kept beside the new ones, in `model/arrows.jsonl` and below.
- **The concept renamed (C3b).** The one-line enrolment is a relabelling of conversation analysis's preferred acceptance (`concept-C3.md`). Its claimed function as the room's head count failed its test (F-015, weak).
- **Two construct declarations amended (C3b).** Stigmergy and Decided order each name a construct from the shelf they may be mistaken for (`structure-C3.md`).

No element was added or withdrawn; no arrow was added, bounded, demoted or withdrawn; no strength or count changed; no tier was recut. The story is not rewritten here; that is stage C5's.

The text below is pass 5's, with these changes written into it.

"""
REPL = [
    ("# The model, stage C2, pass 5 (C2d-02)\n", "# The model, stage C3: pass 5 read against the literature\n"),
    ("Pass 5 is the last closing pass. It worked", C3 + "Pass 5 is the last closing pass. It worked"),
    ("The cheapest answer to a call is a one-line enrolment, \"On it.\", which commits a member and asks for nothing back [A12].",
     "The cheapest answer to a call is one bare line, \"On it.\", which commits a member and asks for nothing back [A12]. "
     "Joining is the answer a call prefers, so it needs no reason; refusing is dispreferred and comes with one "
     "(conversation analysis, recalled; F-014)."),
    ("Decided order, such as a leader, a vote or an oath, is rare (C01; finding F-006).",
     "Decided order, such as a leader, a vote or an oath, is rare (C01; finding F-006). It gathers in the small "
     "canvas-born factions that govern a territory or rule on guests (F-006, bounded at C3a, prompted by O'Mahony and "
     "Ferraro 2007)."),
    ("Mechanism: a call is answered with one line that commits and asks nothing back. Never counted.",
     "Mechanism (from conversation analysis, C3b): %s Stage C2's sentence: %s Fails if: %s Never counted as an order."
     % (A["A12"]["mechanism"], A["A12"]["mechanism_C2"], A["A12"]["mechanism_fails_if"])),
    ("Mechanism: a call to attack another room's work is answered inside the room: members refuse it, rein in their "
     "attackers or apologise to the target. Fails if: restraint comes only before any attack call.",
     "Mechanism (from conversation analysis, C3b): %s Stage C2's sentence: %s Fails if: %s Tested (F-014): refusals of "
     "attack calls gave a reason in 23 of 38 read pairs, acceptances in 2 of 14; refusals were not longer."
     % (A["A16"]["mechanism"], A["A16"]["mechanism_C2"], A["A16"]["mechanism_fails_if"])),
    ("- A12: never counted, on exemplars only.",
     "- A12: never counted, on exemplars only. Since C3b its mechanism is conversation analysis's, tested on attack calls "
     "and not on calls to place."),
]
for old, new in REPL:
    n = txt.count(old)
    if n != 1:
        sys.exit("passage found %d times, not once: %r" % (n, old[:80]))
    txt = txt.replace(old, new)
with open(DEST, "w", encoding="utf-8") as f:
    f.write(txt)
print("model-C3.md written: %d words (model-p5.md %d)" % (len(txt.split()), len(open(SRC, encoding="utf-8").read().split())))
