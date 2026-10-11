#!/usr/bin/env python3
"""B1e: the stranger test's draw (section 7).

Draws five second-order themes held by any of the three themes named, from rooms the second pass
did not reread (out/pass2-chosen-B1.txt) and that are not exemplar rooms of the three, seeded.
Prints only <sub> <tNN>. With --reveal, prints the kinds each one holds in scheme_current.jsonl.

Usage: python3 out/_analysis/b1e_stranger_draw.py T3-005 T3-021 T3-087 [--reveal]
"""
import json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


ids = [a for a in sys.argv[1:] if a.startswith("T3-")]
chosen = set()
with open(os.path.join(OUT, "pass2-chosen-B1.txt"), encoding="utf-8") as f:
    for x in f:
        x = x.strip()
        if x and not x.startswith("#"):
            chosen.add(x.split()[0])
ex = {e["sub"] for r in jl(os.path.join(OUT, "scheme.jsonl")) if r["id"] in ids for e in r["exemplars"]}
lab2id = {(r["sub"], r["second_order"]): r["theme_id"] for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
kinds = {}
for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
    for m in r["members"]:
        key = (m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))
        kinds.setdefault(key, set()).add(r["theme"])
cand = sorted(k for k, v in kinds.items() if v & set(ids) and k[0] not in chosen and k[0] not in ex)
random.Random("b1e-stranger:" + ",".join(ids)).shuffle(cand)
for k in cand[:5]:
    if "--reveal" in sys.argv:
        print("%s %s\t%s" % (k[0], k[1], ",".join(sorted(kinds[k]))))
    else:
        print("%s %s" % k)
print("(drawn from %d candidates)" % len(cand))
