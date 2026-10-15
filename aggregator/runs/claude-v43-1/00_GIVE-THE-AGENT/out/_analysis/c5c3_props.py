#!/usr/bin/env python3
"""C5c-03, pass 7: three proposition fields in c5_propositions.json brought into line with pass 6 (the rule logged before,
diary C5c-03): N01's `decides` carries A01's recount without joining lines and its transitions (read from
model/arrows.jsonl and c5c2_arrow_evidence.txt); N03's statement says what F-014 counts; N07's statement and boundary
follow D02's and T4-011's accepted advice. Each `old` must occur once. Writes the spec only; c5_propositions.py --replace
then rewrites propositions.jsonl.

    python3 out/_analysis/c5c3_props.py [--write]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AN = os.path.join(ROOT, "out", "_analysis")
sp = os.path.join(AN, "c5_propositions.json")
spec = json.load(open(sp, encoding="utf-8"))
A = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(ROOT, "out", "model", "arrows.jsonl"), encoding="utf-8")}
wj = A["A01"]["without_joining"]
ev = open(os.path.join(AN, "c5c2_arrow_evidence.txt"), encoding="utf-8").read()
blk = ev.split("== P01 -> P03", 1)[1].split("\n==", 1)[0]
m = re.search(r"transitions: (\d+) in (\d+) rooms", blk)
tr, rooms = int(m.group(1)), int(m.group(2))
R = [
    ("N01", "decides", "the call still comes before the build in 132 of 189 rooms (A01), and in 70 rooms a build report "
                       "replies to a call in the same thread.",
     "the call still comes before the build in %d of %d rooms (A01), and in %d rooms a build report replies to a call in "
     "the same thread (%d transitions)." % (wj["holds"], wj["both"], rooms, tr)),
    ("N03", "statement", "they refuse it with a reason, rein in the attackers or apologise (P07),",
     "they refuse it, usually with a reason (F-014), rein in the attackers or apologise (P07),"),
    ("N07", "statement", "Members align their placing without deciding how they are organized:",
     "Members try to align their placing without deciding how they are organized:"),
    ("N07", "boundary", "The small factions born on the canvas that govern a territory, where decided order gathers "
                        "(F-006's bound).",
     "Rooms that govern a territory for a colour or vet others' requests to build, where decided order is coded more "
     "often, the gap lying in the smaller rooms (F-006's bound)."),
]
for pid, f, old, new in R:
    t = spec[pid][f]
    if t.count(old) != 1:
        sys.exit("%s %s: old text found %d times" % (pid, f, t.count(old)))
    spec[pid][f] = t.replace(old, new)
    print("%s %s: %s" % (pid, f, spec[pid][f][:200]))
if "--write" in sys.argv:
    json.dump(spec, open(sp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("c5_propositions.json written")
