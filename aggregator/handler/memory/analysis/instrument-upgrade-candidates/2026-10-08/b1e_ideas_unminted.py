#!/usr/bin/env python3
"""B1e: ideas in ideas-B1.jsonl that no mint in theme_discovery.jsonl took up.

An idea is taken up when a mint has its label, or a mint has its trigger. Prints the rest with leg
and trigger, so the notes can say why each was not made a kind.

Usage: python3 out/_analysis/b1e_ideas_unminted.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


mints = jl(os.path.join(OUT, "theme_discovery.jsonl"))
labels = {m["label"].strip().lower() for m in mints}
triggers = {m["trigger"] for m in mints}
rest = [i for i in jl(os.path.join(OUT, "ideas-B1.jsonl"))
        if i["label"].strip().lower() not in labels and i["trigger"] not in triggers]
lab2id = {(r["sub"], r["second_order"]): r["theme_id"] for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))}
held = {}
for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
    for m in r["members"]:
        key = "%s:%s" % (m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))
        held.setdefault(key, []).append(r["theme"])
bags = {"%s:%s" % (b["sub"], b["theme_id"]): b.get("would_need") for b in jl(os.path.join(OUT, "multiplacement_log.jsonl")) if b.get("item_is_a_bag")}
print("ideas %d, mints %d, ideas no mint took up %d" % (len(jl(os.path.join(OUT, "ideas-B1.jsonl"))), len(mints), len(rest)))
for i in rest:
    print("%s\t%s\t%s\tholds %s%s" % (i["leg"], i["trigger"], i["label"], ",".join(sorted(held.get(i["trigger"], []))) or "nothing",
                                     "; bag names %s" % ",".join(bags[i["trigger"]]) if i["trigger"] in bags else ""))
