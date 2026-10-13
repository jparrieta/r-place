#!/usr/bin/env python3
"""B4a-06: build bag re-rule draft lines (for b4_rule_append.py --replace) from a short spec, taking the concepts of
themes already in the ruling from disagreements.jsonl so they are copied, not retyped.

    python3 out/_analysis/b4_bag_draft.py --packet 5 --spec out/_adjudication-B4/rerule-bag-B4a-06/spec-05.json \
        --out out/_adjudication-B4/rerule-bag-B4a-06/packet-05.jsonl

The spec is a JSON object keyed by item number:
  {"44": {"placed": "T3-006", "add": {"T3-061": ["c0115", ...]}, "drop": ["T3-188"], "move": {"T3-099": "T3-149"},
          "w": "the why"}}
placed: the bag's placed theme (its concepts from the ruling unless "add" gives them);
add: themes for also_present with their concepts (a named theme, or a placed theme the ruling dropped);
drop: ruling themes left out of also_present (fewer than three concepts);
move: rename a ruling theme's concept list to another theme (a relabel stated in the why).
q, br and confidence are kept from the ledger line unless the spec gives "q", "br" or "c".
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
ap.add_argument("--spec", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
spec = json.load(open(a.spec, encoding="utf-8"))
led = {}
for x in open("out/disagreements.jsonl", encoding="utf-8"):
    d = json.loads(x)
    if d.get("packet") == a.packet:
        led[d["n"]] = d
out = []
for key in sorted(spec, key=int):
    s = spec[key]
    d = led[int(key)]
    sup = {t: list(v) for t, v in (d.get("support_by_theme") or {}).items()}
    for old, new in (s.get("move") or {}).items():
        sup[new] = sup.pop(old)
    for t in s.get("drop") or []:
        sup.pop(t, None)
    for t, cs in (s.get("add") or {}).items():
        sup[t] = list(cs)
    placed = s["placed"]
    row = {"n": int(key), "r": [placed], "t": "item-is-a-bag", "c": s.get("c", d.get("confidence") or "arguable"),
           "q": s.get("q", d.get("quote")), "sup": {placed: sup.pop(placed)}, "ap": sup, "w": s["w"]}
    br = s.get("br", d.get("boundary_ruling"))
    if br:
        row["br"] = br
    small = [t for t, v in row["ap"].items() if len(v) < 3]
    if small:
        print("WARNING item %s: also_present themes under three concepts: %s" % (key, small))
    out.append(row)
with open(a.out, "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote %d draft lines to %s" % (len(out), a.out))
