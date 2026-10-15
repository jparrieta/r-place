#!/usr/bin/env python3
"""C5c-02: the fleet readers' and the field analyst's verdicts on the sentences both judged. The fleet judged 40 sentences
(readers-C5/, `declarations`); the field analyst judged 268 (sources-from-J/RETURN-field-C5.jsonl), numbered in the
field packages. Sentences are matched by text: a fleet sentence matches the field sentence of the same declaration that
contains its first 60 characters, or is contained in it. Prints the agreement and the sentences they split on. Writes
out/_analysis/c5c2_two_readers.json.

    python3 out/_analysis/c5c2_two_readers.py
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
text = {}
for p in glob.glob(os.path.join(OUT, "field-packages-C5", "0[2-9]-*.md")):
    for l in open(p, encoding="utf-8"):
        m = re.match(r"- `([A-Z0-9-]+\.[a-z_]+\.\d+)` (.*)$", l.rstrip("\n"))
        if m:
            text[m.group(1)] = m.group(2)
field = {}
for l in open(os.path.join(OUT, "sources-from-J", "RETURN-field-C5.jsonl"), encoding="utf-8"):
    if l.strip().startswith("{"):
        o = json.loads(l)
        if "sentence" in o:
            field[o["sentence"]] = o["stands"]
pairs, unmatched = [], []
for k in (1, 2, 3):
    r = json.loads(open(os.path.join(OUT, "readers-C5", "C5-reader-%d.jsonl" % k)).read().strip().splitlines()[0])
    for d in r["declarations"]:
        s = d["sentence"].strip()
        cand = [sid for sid, t in text.items() if sid.split(".")[0] == d["id"] and (s[:60] in t or t in s)]
        if not cand:
            unmatched.append((d["id"], s[:80]))
            continue
        pairs.append({"id": d["id"], "fleet_reader": k, "sentence": s, "field_id": cand[0], "fleet": d["stands"],
                      "field": field.get(cand[0])})
agree = sum(1 for p in pairs if p["fleet"] == p["field"])
both_no = sum(1 for p in pairs if not p["fleet"] and not p["field"])
print("matched %d of %d; agree %d (both stand %d, both not %d); split %d" % (
    len(pairs), len(pairs) + len(unmatched), agree, agree - both_no, both_no, len(pairs) - agree))
for p in pairs:
    if p["fleet"] != p["field"]:
        print("  split %s (fleet %s, field %s): %s" % (p["field_id"], p["fleet"], p["field"], p["sentence"][:110]))
for u in unmatched:
    print("  unmatched %s: %s" % u)
json.dump({"pairs": pairs, "unmatched": unmatched}, open(os.path.join(OUT, "_analysis", "c5c2_two_readers.json"), "w"),
          indent=1, ensure_ascii=False)
