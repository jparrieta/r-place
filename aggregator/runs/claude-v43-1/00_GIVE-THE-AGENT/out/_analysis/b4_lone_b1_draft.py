#!/usr/bin/env python3
"""B4a-06: build re-rule drafts (for b4_rule_append.py --replace) under the rule chosen after J's answer of 12:28
Berlin on lone B1 themes: in class 4 (both readers agree) a theme only my B1 placed stands against the readers only
with three concepts or more of its own. Each draft line copies the ledger line, drops the weaker lone B1 themes and
their concepts, and resets the taxonomy: a scheme-ambiguous line keeps its field, theme and sentence; a ruling left
empty is unresolved (author-disagrees); a ruling equal to the readers' list is author-error; otherwise
author-disagrees. The why gains one opening sentence; the earlier reasoning follows it.

    python3 out/_analysis/b4_lone_b1_draft.py --packet 1 --out out/_adjudication-B4/rerule-loneb1-B4a-06/packet-01.jsonl
"""
import argparse
import json
import os

NUM = {1: "one concept", 2: "two concepts"}

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
rows = []
for x in open("out/disagreements.jsonl", encoding="utf-8"):
    d = json.loads(x)
    if d.get("packet") != a.packet or d.get("class") != 4 or d.get("unresolved"):
        continue
    if d["taxonomy"] == "item-is-a-bag":
        continue
    readers = set(d["readers"][0]) | set(d["readers"][1])
    sup = d.get("support_by_theme") or {}
    weak = [t for t in d["ruling"] if t not in readers and len(sup.get(t, [])) < 3]
    if not weak:
        continue
    rest = [t for t in d["ruling"] if t not in weak]
    names = ", ".join("%s (%s)" % (t, NUM.get(len(sup.get(t, [])), "%d concepts" % len(sup.get(t, [])))) for t in weak)
    lead = ("Re-ruled at B4a-06 under the rule chosen after J's answer of 12:28 Berlin on lone B1 themes: in class 4 a "
            "theme only my B1 placed stands against the two agreeing readers only with three concepts or more of its "
            "own. My B1's %s %s left out" % (names, "is" if len(weak) == 1 else "are"))
    row = {"n": d["n"], "c": d.get("confidence") or "arguable", "q": d.get("quote")}
    if d.get("boundary_ruling"):
        row["br"] = d["boundary_ruling"]
    if d["taxonomy"] == "scheme-ambiguous":
        row["t"] = "scheme-ambiguous"
        row["f"] = d.get("field")
        row["th"] = d.get("theme")
    if not rest:
        row["r"] = []
        row["u"] = True
        row.setdefault("t", "author-disagrees")
        lead += "; the readers' theme takes no concept by the earlier reading, so no placement stands and the item is carried unresolved."
    else:
        row["r"] = rest
        row["sup"] = {t: sup[t] for t in rest}
        if set(rest) == readers:
            row.setdefault("t", "author-error")
            lead += "; the ruling is the readers' list."
        else:
            row.setdefault("t", "author-disagrees")
            lead += "."
    if d.get("also_present"):
        row["ap"] = d["also_present"]
    row["w"] = lead + " Earlier reasoning: " + (d.get("why") or "")
    rows.append(row)
os.makedirs(os.path.dirname(a.out), exist_ok=True)
with open(a.out, "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("packet %d: wrote %d draft lines to %s" % (a.packet, len(rows), a.out))
