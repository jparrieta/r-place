#!/usr/bin/env python3
"""D4a-05: for each form or sub-form, the selected change lines of its members on its signature nodes:
the commonest op and element, with counts, and up to N how sentences (members in case-ignored order,
one line each). Read-only.

    python3 out/_analysis/d4a05_form_lines.py --node A --n 6
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--node", required=True)
ap.add_argument("--n", type=int, default=6)
ap.add_argument("--file", default="d4a05_tree2.json")
a = ap.parse_args()
T = json.load(open(os.path.join(OUT, "_analysis", a.file), encoding="utf-8"))
node = next(n for n in T["nodes"] if n["id"] == a.node)
if a.node in T["forms"]:
    sig4 = [d["node"] for d in T["forms"][a.node]["sig_T4"]]
    sig3 = [d["node"] for d in T["forms"][a.node]["sig_T3"]]
else:
    sig4 = [d["node"] for d in node.get("sig_T4") or []]
    sig3 = [d["node"] for d in node.get("sig_T3") or []]
mem = set(node["members"])
CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE and r["sub"] in mem and len(r.get("lift") or []) >= 4]
on = [r for r in L if r["lift"][2] in sig4[:2] or r["lift"][1] in sig3[:2]]
print(a.node, "members", len(mem), "lines", len(L), "on signature", len(on), "sig4", sig4, "sig3", sig3)
print("op:element", collections.Counter("%s:%s" % (r["op"], r["element"]) for r in on).most_common(8))
seen = set()
for r in sorted(on, key=lambda r: (r["sub"].lower(), r["id"])):
    if r["sub"] in seen:
        continue
    seen.add(r["sub"])
    print("-", r["sub"], r["op"], r["element"], r["lift"][1], "|", (r.get("how") or "").strip())
    if len(seen) >= a.n:
        break
