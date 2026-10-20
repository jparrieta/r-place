#!/usr/bin/env python3
"""D3a-38: the counts A11's section of notes-D3.md cites, from the rulings files, with the re-rulings of
A11-rerule-spec.txt applied over the first classes: instantiate and restrict lines by class; add lines by census
class (as d3_a11_census.py reads their reasons); absent rulings by decision and form; restrict lines whose packet
'how' line names settling ('settl'); and, with --rows N, the first N spec rows of each restrict class, for quotes.
Writes nothing.

  python3 out/_analysis/d3_a11_notes_counts.py [--rows 2]
"""
import glob
import json
import sys
from collections import Counter

R = "out/_analysis/d3_rulings/"


def spec(name):
    out = {}
    for l in open(R + name, encoding="utf-8"):
        if l.strip():
            aid, cls, ev = l.rstrip("\n").split("|", 2)
            out[aid] = (cls, ev)
    return out


inst, rest, rer = spec("A11-inst-spec.txt"), spec("A11-restrict-spec.txt"), spec("A11-rerule-spec.txt")
for aid, (cls, ev) in rer.items():
    if aid in rest:
        rest[aid] = (cls, ev)
print("instantiate by class:", dict(Counter(c for c, _ in inst.values())))
print("restrict by class, re-rulings applied:", dict(Counter(c for c, _ in rest.values())))
adds = Counter()
for l in open(R + "A11-adds.jsonl"):
    r = json.loads(l)
    if "counted in the census as the transition" in r["reason"]:
        adds["transition"] += 1
    elif "counted in the census as template first" in r["reason"]:
        adds["template first"] += 1
    else:
        adds["held"] += 1
print("add lines by census class:", dict(adds))
ab = Counter()
for l in open(R + "A11-absent.jsonl"):
    r = json.loads(l)
    if r["decision"] == "reject":
        ab["reject, in words" if "mechanism in the members' words" in r["reason"] else "reject, other forms"] += 1
    else:
        ab[r["decision"] + (" " + r["kind"] if r.get("kind") else "")] += 1
print("absent by decision and form:", dict(ab))
settl, n = 0, 0
for f in sorted(glob.glob("out/_analysis/d3_pk_A11_restrict_*.txt")):
    for blk in open(f, encoding="utf-8").read().split("\n== ")[1:]:
        n += 1
        how = [x for x in blk.split("\n") if x.strip().startswith("how:")]
        if how and "settl" in how[0].lower():
            settl += 1
print("restrict blocks read: %d; with 'settl' in the how line: %d" % (n, settl))
if "--rows" in sys.argv:
    k = int(sys.argv[sys.argv.index("--rows") + 1])
    seen = Counter()
    for aid, (cls, ev) in sorted(rest.items()):
        if seen[cls] < k:
            seen[cls] += 1
            print("%s %s: %s" % (cls, aid, ev))
