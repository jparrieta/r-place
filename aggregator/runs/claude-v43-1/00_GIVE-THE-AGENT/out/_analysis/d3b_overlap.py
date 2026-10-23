#!/usr/bin/env python3
"""D3b: for the unruled flagged re-check absent lines of the elements named, the room's accepted or modified lines on
the same element (first return and re-check, instantiate, restrict, add and link ops) that cite any of the same codes,
with each match's id, op, shared codes, decision, kind and reason whole. A line with no match is printed with 'no
accepted line shares a code'. Reads only.

    python3 out/_analysis/d3b_overlap.py --elements A01,A07
"""
import argparse, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--elements", required=True)
a = ap.parse_args()
want = set(a.elements.split(","))


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return set(str(c).split(":")[-1] for c in ev)


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
led = jl(os.path.join(OUT, "adaptations.jsonl")) + jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
flag = {r["adaptation"] for p in sorted(glob.glob(os.path.join(OUT, "_analysis", "d3_rulings", "recheck-absent-flagged*.jsonl")))
        for r in jl(p)}
acc = [l for l in led if l.get("element") in want and l["op"] != "absent"
       and last.get(l["id"], {}).get("decision") in ("accept", "modify")]
for r in sorted((l for l in led if l["id"] in flag and l["id"] not in last and l.get("element") in want),
                key=lambda l: (l.get("element"), l["sub"].lower())):
    cs = codes(r)
    m = [x for x in acc if x["sub"] == r["sub"] and x.get("element") == r.get("element") and codes(x) & cs]
    print("== %s  %s  codes %s" % (r["id"], r.get("element"), ",".join(sorted(cs))))
    if not m:
        print("   no accepted line shares a code")
    for x in m:
        d = last[x["id"]]
        print("   %s %s shares %s: %s/%s: %s" % (x["id"], x["op"], ",".join(sorted(codes(x) & cs)), d["decision"],
                                              d.get("kind"), d.get("reason")))
