"""Split a packet's named_neither rulings by where the unchosen themes came from.

For each ruling flagged named_neither, the themes no reader chose are sorted
into two kinds: themes in my B1 grouping, and themes no placement held (not
in either reader's set and not in B1). Also counts how often the ruling's
primary is a theme neither reader chose, and ranks the themes no placement
held. Read-only.

Usage: python3 out/_analysis/b4_named_neither_split.py --packet 3
"""
import argparse
import collections
import json

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
args = ap.parse_args()

rows = [json.loads(l) for l in open("out/disagreements.jsonl")]
rows = [d for d in rows if d.get("packet") == args.packet]

nn = [d for d in rows if d.get("named_neither")]
only_b1 = 0
some_none = 0
none_themes = collections.Counter()
b1_themes = collections.Counter()
primary_unchosen = 0
primary_none = 0
by_tax = collections.Counter()
by_count = collections.Counter()
for d in nn:
    readers = set()
    for r in d.get("readers") or []:
        readers |= set(r)
    b1 = set(d.get("b1") or [])
    ruling = d.get("ruling") or []
    unchosen = [t for t in ruling if t not in readers]
    from_b1 = [t for t in unchosen if t in b1]
    from_none = [t for t in unchosen if t not in b1]
    by_tax[d.get("taxonomy")] += 1
    by_count[len(ruling)] += 1
    if from_none:
        some_none += 1
    else:
        only_b1 += 1
    for t in from_none:
        none_themes[t] += 1
    for t in from_b1:
        b1_themes[t] += 1
    if ruling and ruling[0] not in readers:
        primary_unchosen += 1
        if ruling[0] not in b1:
            primary_none += 1

print("packet", args.packet, "rulings", len(rows), "named_neither", len(nn))
print("only themes from my B1 grouping:", only_b1)
print("a theme no placement held:", some_none)
print("primary chosen by neither reader:", primary_unchosen, "of which held by no placement:", primary_none)
print("by taxonomy:", dict(by_tax))
print("by number of placed themes:", dict(sorted(by_count.items())))
print("themes no placement held, top 15:", none_themes.most_common(15))
print("themes from my B1 only, top 15:", b1_themes.most_common(15))

added = collections.Counter()
for d in rows:
    added[len(d.get("ruling") or [])] += 1
print("all rulings by number of placed themes:", dict(sorted(added.items())))
