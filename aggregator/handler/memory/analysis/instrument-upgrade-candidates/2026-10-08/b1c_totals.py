"""B1c: totals over the fresh file for saturation-B1.md.

usage: python3 out/_analysis/b1c_totals.py

Per room and overall: themes, fresh verdicts, primaries agreeing with the record, and kinds per theme in
each reading (bare themes and themes unplaced in the record left out of the kind counts).
"""
import collections
import json

fresh = []
with open("out/_analysis/b1c_fresh.psv", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.startswith("sub|") or line.startswith("END|"):
            continue
        p = line.split("|")
        fresh.append((p[0], p[1], p[2], [x for x in p[3].split(",") if x], p[4]))

rec = collections.defaultdict(set)
with open("out/scheme/scheme_current.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            t = json.loads(line)
            for m in t["members"]:
                rec[(m["sub"], m["theme_id"])].add(t["theme"])
prim = {}
with open("out/multiplacement_log.jsonl", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            r = json.loads(line)
            if r.get("sub") and r.get("theme_id") and r.get("primary"):
                prim[(r["sub"], r["theme_id"])] = r["primary"]

rooms = collections.OrderedDict()
tot = collections.Counter()
for sub, tid, P, A, v in fresh:
    c = rooms.setdefault(sub, collections.Counter())
    c["themes"] += 1
    for x in v.split(","):
        c["v " + x.strip()] += 1
    r = rec.get((sub, tid), set())
    if P == "none" or not r:
        c["one side unplaced"] += 1
        continue
    rp = prim.get((sub, tid)) or (sorted(r)[0] if len(r) == 1 else "?")
    c["both placed"] += 1
    c["same primary"] += P == rp
    c["fresh primary in record"] += P in r
    c["any shared kind"] += bool(({P} | set(A)) & r)
    c["fresh kinds"] += 1 + len(A)
    c["recorded kinds"] += len(r)
    c["recorded not fresh"] += len(r - ({P} | set(A)))
    c["fresh not recorded"] += len(({P} | set(A)) - r)

keys = ["themes", "v fits", "v gate fails", "v bare", "both placed", "same primary", "fresh primary in record",
        "any shared kind", "fresh kinds", "recorded kinds", "recorded not fresh", "fresh not recorded"]
print("room\t" + "\t".join(k.replace(" ", "_") for k in keys))
for sub, c in rooms.items():
    print(sub + "\t" + "\t".join(str(c[k]) for k in keys))
    tot.update(c)
print("TOTAL\t" + "\t".join(str(tot[k]) for k in keys))
bp = tot["both placed"]
print("\nboth placed %d: same primary %.1f%%, fresh primary among recorded kinds %.1f%%, any shared kind %.1f%%"
      % (bp, 100.0 * tot["same primary"] / bp, 100.0 * tot["fresh primary in record"] / bp,
         100.0 * tot["any shared kind"] / bp))
print("kinds per theme: fresh %.2f, recorded %.2f" % (tot["fresh kinds"] / bp, tot["recorded kinds"] / bp))
