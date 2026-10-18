#!/usr/bin/env python3
"""QD3-005: the instantiate and restrict lines G4a's second clause could reach, by each line's latest ruling.
Counts, by element and op, the lines whose latest ruling is an accepted elaboration, a particular (split into
particulars by construction, from the reason's words, and particulars on one room's evidence) and the other
rulings, so that the count's scope can be stated before any line is read. Writes nothing.

  python3 out/_analysis/d3_qd3005_population.py [--elements R01,P01] [--list elaboration|particular-one-room]
"""
import argparse
import json
import re
from collections import Counter, defaultdict

OPS = ("instantiate", "restrict")
CONSTRUCTION = re.compile(r"portable false|by construction|rule 5|names the room itself|names the room in|"
                          r"the room itself in|fails portability|failing portability|NONPORTABLE|names particulars",
                          re.I)


def bucket(r, akind):
    dec = r.get("decision")
    kind = r.get("kind") or akind or "-"
    if dec == "particular":
        return "particular, by construction" if CONSTRUCTION.search(r.get("reason", "")) else "particular, one room"
    if dec == "accept" and kind == "elaboration":
        return "elaboration"
    if dec == "accept" and kind == "none":
        return "evidence limit"
    if dec == "accept":
        return str(kind)
    return str(dec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--elements", default="")
    ap.add_argument("--list", default="", help="print the ids, pairs and reasons of one bucket")
    a = ap.parse_args()
    els = {e for e in a.elements.split(",") if e}
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = x
    latest = {}
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            latest[r["adaptation"]] = r
    table = defaultdict(Counter)
    listed = []
    for i, r in latest.items():
        x = meta.get(i, {})
        el, op = x.get("element"), x.get("op")
        if op not in OPS or (els and el not in els):
            continue
        b = bucket(r, x.get("kind"))
        table[(el, op)][b] += 1
        if a.list and b.startswith(a.list):
            listed.append((str(el), str(op), i, r.get("pair") or "-", r.get("leg") or "-", r.get("reason") or ""))
    cols = ["elaboration", "particular, one room", "particular, by construction"]
    other = sorted({b for t in table.values() for b in t} - set(cols))
    print("element | op | lines | " + " | ".join(cols + other))
    tot = Counter()
    for (el, op) in sorted(table, key=lambda k: (str(k[0]), k[1])):
        t = table[(el, op)]
        tot.update(t)
        print(f"{el} | {op} | {sum(t.values())} | " + " | ".join(str(t.get(c, 0)) for c in cols + other))
    print(f"all | | {sum(tot.values())} | " + " | ".join(str(tot.get(c, 0)) for c in cols + other))
    for row in sorted(listed):
        print(" | ".join(row))


if __name__ == "__main__":
    main()
