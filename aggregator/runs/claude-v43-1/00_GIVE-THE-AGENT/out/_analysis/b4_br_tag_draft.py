"""Write a --replace draft that adds a boundary tag to ruled items, ruling unchanged.

Copies each item's ledger row back into the draft keys b4_rule_append.py reads
(r, t, c, q, f, th, sup, ap, u, w), sets br to the pair given, and adds one
sentence to the why saying the tag was added. Writes the draft only; the
correction itself goes through b4_rule_append.py --replace.

Usage: python3 out/_analysis/b4_br_tag_draft.py --packet 3 --leg B4a-03 \
          --pair T3-002|T3-038 --items 247,248 --out <draft.jsonl> [--append]
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--packet", type=int, required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--pair", required=True)
ap.add_argument("--items", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--append", action="store_true")
args = ap.parse_args()

want = [int(x) for x in args.items.split(",")]
rows = {}
for line in open("out/disagreements.jsonl"):
    d = json.loads(line)
    if d.get("packet") == args.packet and d.get("n") in want:
        rows[d["n"]] = d

missing = [n for n in want if n not in rows]
if missing:
    raise SystemExit("not ruled in packet %d: %s" % (args.packet, missing))

note = " Boundary tag %s added at %s; the ruling is unchanged." % (args.pair, args.leg)
out = []
for n in want:
    d = rows[n]
    if d.get("boundary_ruling"):
        raise SystemExit("item %d already carries %s" % (n, d["boundary_ruling"]))
    draft = {"n": n, "r": d.get("ruling") or [], "t": d.get("taxonomy"), "c": d.get("confidence"),
             "q": d.get("quote") or "", "br": args.pair, "sup": d.get("support_by_theme") or {},
             "w": (d.get("why") or "") + note}
    if d.get("field"):
        draft["f"] = d["field"]
    if d.get("theme"):
        draft["th"] = d["theme"]
    if d.get("also_present"):
        draft["ap"] = d["also_present"]
    if d.get("unresolved"):
        draft["u"] = True
    out.append(draft)

with open(args.out, "a" if args.append else "w", encoding="utf-8") as fh:
    for draft in out:
        fh.write(json.dumps(draft, ensure_ascii=False) + "\n")
print("wrote %d draft lines to %s" % (len(out), args.out))
