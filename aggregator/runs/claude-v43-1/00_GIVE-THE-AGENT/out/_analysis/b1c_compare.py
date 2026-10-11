"""B1c: compare a room's fresh placements (out/_analysis/b1c_fresh.psv) with the recorded ones.

usage: python3 out/_analysis/b1c_compare.py <sub> [<sub> ...] [--all]

Recorded kinds come from out/scheme/scheme_current.jsonl; the recorded primary from the last rule 0
line in out/multiplacement_log.jsonl for that theme, or the one kind where there is no such line.
Run it only after the room's fresh lines are written. --all prints the totals over every room in the
fresh file.
"""
import collections
import json
import sys

subs = [a for a in sys.argv[1:] if not a.startswith("--")]
everything = "--all" in sys.argv

fresh = collections.OrderedDict()
with open("out/_analysis/b1c_fresh.psv", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.startswith("sub|") or line.startswith("END|"):
            continue
        p = line.split("|")
        if len(p) < 7:
            print("short line: " + line[:120])
            continue
        add = [x for x in p[3].split(",") if x]
        fresh[(p[0], p[1])] = {"P": p[2], "A": add, "verdict": p[4], "codes": p[5], "why": p[6]}

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

if everything:
    subs = list(collections.OrderedDict((k[0], 1) for k in fresh))

tot = collections.Counter()
for sub in subs:
    keys = [k for k in fresh if k[0] == sub]
    c = collections.Counter()
    if not everything:
        print("== %s: %d fresh lines" % (sub, len(keys)))
    for k in keys:
        fr = fresh[k]
        r = rec.get(k, set())
        rp = prim.get(k) or (sorted(r)[0] if len(r) == 1 else "?")
        fs = {fr["P"]} | set(fr["A"])
        if fr["P"] == rp:
            m = "same primary"
        elif fr["P"] in r:
            m = "fresh primary recorded as additional"
        elif fs & r:
            m = "overlap, fresh primary not recorded"
        else:
            m = "disjoint"
        c[m] += 1
        c["themes"] += 1
        for v in fr["verdict"].split(","):
            c["verdict " + v.strip()] += 1
        if not everything:
            print("%s  fresh %s%s | recorded %s%s | %s | %s" % (
                k[1], fr["P"], ("+" + ",".join(fr["A"])) if fr["A"] else "",
                rp, ("+" + ",".join(sorted(r - {rp}))) if len(r) > 1 else "", m, fr["verdict"]))
            if r - fs:
                print("      recorded, not fresh: %s" % ",".join(sorted(r - fs)))
            if fs - r:
                print("      fresh, not recorded: %s" % ",".join(sorted(fs - r)))
    missing = sorted(k[1] for k in rec if k[0] == sub and k not in fresh)
    if missing and not everything:
        print("recorded themes with no fresh line: %s" % ", ".join(missing))
    if not everything:
        print("summary %s: %s" % (sub, "; ".join("%s %d" % (a, b) for a, b in sorted(c.items()))))
    tot.update(c)
if everything or len(subs) > 1:
    print("total over %d rooms: %s" % (len(subs), "; ".join("%s %d" % (a, b) for a, b in sorted(tot.items()))))
