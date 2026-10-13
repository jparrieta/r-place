"""Details of one packet's rulings for adjudication_report.md. Read-only.

Prints: the scheme-ambiguous rulings grouped by (theme, field, sentence),
with their items; for class 4, whether the readers' list was taken or a
theme of my B1 grouping was kept; the themes my B1 grouping missed in
author-error rulings and the themes kept against both readers in
author-disagrees rulings.

Usage: python3 out/_analysis/b4_packet_detail.py --packet 3 [--min 2]
"""
import argparse
import collections
import json

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
ap.add_argument("--min", type=int, default=2)
args = ap.parse_args()

rows = [json.loads(l) for l in open("out/disagreements.jsonl")]
rows = [d for d in rows if d.get("packet") == args.packet]

groups = collections.defaultdict(list)
for d in rows:
    if d.get("taxonomy") == "scheme-ambiguous":
        groups[(d.get("theme"), d.get("field"), d.get("quote"))].append(d["sub"] + " " + d["theme_id"])
print("scheme-ambiguous sentences met at least", args.min, "times:")
for key, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    if len(items) >= args.min:
        print(len(items), key[0], key[1], "|", key[2])
        print("   ", ", ".join(items))
print()

c4 = collections.Counter()
missed = collections.Counter()
kept = collections.Counter()
for d in rows:
    if d.get("class") not in (4, 5):
        continue
    readers = set()
    for r in d.get("readers") or []:
        readers |= set(r)
    b1 = set(d.get("b1") or [])
    ruling = set(d.get("ruling") or [])
    b1_kept = ruling & (b1 - readers)
    if not ruling:
        kind = "empty"
    elif b1_kept:
        kind = "a B1 theme kept"
    elif readers <= ruling:
        kind = "readers' list taken"
    else:
        kind = "other"
    c4[(d.get("class"), d.get("taxonomy"), kind)] += 1
    if d.get("taxonomy") == "author-error":
        for t in readers - b1:
            missed[t] += 1
    if d.get("taxonomy") == "author-disagrees":
        for t in b1_kept:
            kept[t] += 1
print("class 4 and 5 by taxonomy and kind:")
for k in sorted(c4, key=str):
    print("  ", k, c4[k])
print("themes the readers chose that my B1 lacked, in author-error:", missed.most_common(12))
print("themes of my B1 kept against both readers, in author-disagrees:", kept.most_common(12))
