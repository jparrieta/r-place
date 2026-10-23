#!/usr/bin/env python3
"""D3b, G61 (1): build the rulings for re-check lines that repeat a first-return line of the same room exactly:
the same element, op, cited codes, condition, statement and relation text, and for an absent line the same
observation state. The line takes the last ruling of the line it repeats; the reason names that line, its decision
and kind; an accepted elaboration keeps its pair. Propose lines are never ruled here (G61 (2)), nor a repeat whose
first-return matches carry different rulings, nor one whose match was modified. Writes rulings files of at most
2,500 lines into d3_rulings/, named recheck-repeat-NN.jsonl, for d3b_adjudicate_batch.py.

    python3 out/_analysis/d3b_repeat_rulings.py [--write]
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
ap.add_argument("--prefix", default="recheck-rep2", help="file name prefix; a new batch takes a new prefix")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return frozenset(str(c).split(":")[-1] for c in ev)


def txt(r):
    return tuple(str(r.get(k) or "").strip() for k in ("condition", "statement", "relation"))


old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
idx = collections.defaultdict(list)
for l in old:
    key = (l["sub"], l.get("element"), l["op"], codes(l), txt(l), l.get("observation") if l["op"] == "absent" else None)
    idx[key].append(l)
rows, why = [], collections.Counter()
for r in new:
    if r["id"] in last:
        why["already ruled"] += 1
        continue
    if r["op"] == "propose":
        why["propose: read (G61 2)"] += 1
        continue
    key = (r["sub"], r.get("element"), r["op"], codes(r), txt(r), r.get("observation") if r["op"] == "absent" else None)
    m = idx.get(key)
    if not m:
        why["no repeat: read (G61 3)"] += 1
        continue
    rul = [last.get(x["id"]) for x in m]
    if any(x is None for x in rul):
        why["match unruled: read"] += 1
        continue
    kinds = {(x["decision"], x.get("kind")) for x in rul}
    if len(kinds) > 1:
        why["ambiguous match: read"] += 1
        continue
    o, d = m[0], rul[0]
    if d["decision"] == "modify":
        why["match modified: read"] += 1
        continue
    obs = (", observation %s" % o.get("observation")) if o["op"] == "absent" else ""
    if d["decision"] == "accept" and r.get("portable") is False:
        reason = ("G61 (1) and G6: repeats %s (the same room, element, op, cited codes and wording%s), whose ruling "
                  "was accept (%s); this re-check line is marked NONPORTABLE, so it is a particular by construction"
                  % (o["id"], obs, d.get("kind")))
        rows.append({"adaptation": r["id"], "decision": "particular", "reason": reason, "kind": "particular"})
        why["repeat of an accepted line, now NONPORTABLE: particular"] += 1
        continue
    reason = ("G61 (1): repeats %s (the same room, element, op, cited codes and wording%s), asked of the revised model; "
              "%s's ruling stands: %s (%s)" % (o["id"], obs, o["id"], d["decision"], d.get("kind")))
    row = {"adaptation": r["id"], "decision": d["decision"], "reason": reason, "kind": d.get("kind")}
    if d.get("pair"):
        row["pair"] = d["pair"]
    rows.append(row)
    why["ruled by reference: %s" % d["decision"]] += 1
print("re-check lines %d" % len(new))
for k, n in sorted(why.items()):
    print("   %-40s %6d" % (k, n))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
n = 0
for i in range(0, len(rows), 2500):
    p = os.path.join(RD, "%s-%02d.jsonl" % (a.prefix, i // 2500 + 1))
    if os.path.exists(p):
        sys.exit("refused: %s exists; never overwrite" % p)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows[i:i + 2500]:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n += 1
print("wrote %d files, %d rows" % (n, len(rows)))
