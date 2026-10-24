#!/usr/bin/env python3
"""D3c: one room's re-check, for uncomposed-D.md's re-check note: the re-check readers' verdicts and sentences
(verdicts-recheck-D.jsonl), any analyst ruling on it (verdicts-D.jsonl), and its re-check ledger lines with their
last rulings (element, op, decision, kind, the head of the statement). Read-only.

    python3 out/_analysis/d3c_room_recheck.py --sub picturegame
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--sub", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    if r["sub"] == a.sub:
        for e in r["readers"]:
            print("re-check reader %s: %s (cannot_tell_under %s; version %s) | %s | residue %s" % (
                e.get("reader"), e.get("verdict"), e.get("cannot_tell_under"), (e.get("model_version") or "")[:8],
                e.get("sentence"), e.get("residue")))
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r["sub"] == a.sub and r.get("ruled_by"):
        print("analyst ruling (%s, recheck %s): %s" % (r.get("leg"), r.get("recheck"), r.get("verdict")))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
n = 0
for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl")):
    if l["sub"] != a.sub:
        continue
    n += 1
    d = last.get(l["id"], {})
    print("%s %s %s -> %s/%s | %s" % (l["id"], l.get("element"), l["op"], d.get("decision"), d.get("kind"),
                                     (l.get("statement") or l.get("observation") or "")[:150]))
print("re-check lines: %d" % n)
p = os.path.join(OUT, "rooms", a.sub, "model-D-recheck.md")
if os.path.exists(p):
    t = open(p, encoding="utf-8").read()
    i = t.find("local_status:")
    print("account tail:", t[i:i + 700].replace("\n", " "))
