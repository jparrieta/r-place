#!/usr/bin/env python3
"""D5: gather, for one branch, what the account's middle sections need. Prints text or JSON.

    python3 out/_analysis/d5_misc2.py --branch F27 --keylines            (JSON: the key lines with ids)
    python3 out/_analysis/d5_misc2.py --branch F27 --arrow A07 --arrow2 A08 --elements P14,P22 --near F24,F22,F07

Text mode prints: the third-order themes the key lines lift through, with glosses; the members among the
held proposals' rooms (parsed from tree-D4.md); the names of the named branches; each arrow's statement
and its subs; the members' current-ledger lines on each arrow (shared and particular), with how and codes;
the named elements' statements; the members' lines on each named branch's keys; the members' propose lines.
"""
import argparse, collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import effective_lines, shared_lines  # noqa: E402


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
ap.add_argument("--keylines", action="store_true")
ap.add_argument("--arrow", default="")
ap.add_argument("--arrow2", default="")
ap.add_argument("--elements", default="")
ap.add_argument("--near", default="")
a = ap.parse_args()

branches = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
b = branches[a.branch]
ms = set(b["members"])
shared = [l for l in shared_lines(OUT) if l["sub"] in ms]


def key_match(l, key):
    op, el, node = key.split(":")
    if l["op"] != op or l["element"] != el:
        return False
    lvl = "3" if node.startswith("T3") else "4" if node.startswith("T4") else "dim" if node.startswith("D") else "*"
    return distance.node_at(l, lvl) == node


def codes(l):
    ev = l.get("evidence") or {}
    return ev.get("codes", []) if isinstance(ev, dict) else []


keys = b["keys"]
kl = [l for l in shared if any(key_match(l, k) for k in keys)]
if a.keylines:
    print(json.dumps([{"sub": l["sub"], "id": l.get("id"), "lift": l.get("lift"), "third": distance.node_at(l, "3"),
                       "how": l.get("how"), "evidence": {"codes": codes(l)}} for l in sorted(kl, key=lambda x: x["sub"].lower())]))
    sys.exit(0)

scheme = {d["id"]: d for d in jl(os.path.join(OUT, "scheme_final.jsonl"))}
c3 = collections.Counter(distance.node_at(l, "3") for l in kl)
for t3, n in c3.most_common():
    s = scheme.get(t3, {})
    print(t3, n, "|", s.get("name"), "|", s.get("gloss"))

tree = open(os.path.join(OUT, "tree-D4.md"), encoding="utf-8").read()
held = tree[tree.find("## The held proposals"):]
p05 = held[held.find("- **P05"):held.find("- **A11")]
p05_rooms = [x.strip() for x in p05[p05.find("Rooms: ") + 7:p05.find(". Lines:")].split(",")]
a11 = held[held.find("- **A11"):]
a11_rooms = [x.strip() for x in a11[a11.find("Rooms (the talk-only rooms of the failure clause):") + 50:a11.find(". Lines (")].split(",")]
print("P05 held rooms", sorted(ms & set(p05_rooms)), "| A11 talk-only", sorted(ms & set(a11_rooms)), "| parsed", len(p05_rooms), len(a11_rooms))

near = [x for x in a.near.split(",") if x]
for x in near:
    print(x, branches[x]["keys"], len(branches[x]["members"]), "|", branches[x]["name"], "| shared", sorted(ms & set(branches[x]["members"]), key=str.lower))

arrows = {d["id"]: d for d in jl(os.path.join(OUT, "model", "arrows.jsonl"))}
eff = [l for l in effective_lines(OUT, include_particular=True) if l["sub"] in ms]
for ar in [x for x in (a.arrow, a.arrow2) if x]:
    d = arrows[ar]
    print(ar, d["from"], d["to"], "| connection:", d.get("connection"), "| mechanism:", d.get("mechanism"), "| bound:", d.get("bound"), "| subs:", d.get("subs"))
    for l in sorted([l for l in eff if l["element"] == ar], key=lambda x: (x["op"], x["sub"].lower())):
        print(" ", ar, l["op"], l["sub"], "|", l.get("how"), "|", codes(l), "| particular" if l.get("particular") else "")

els = {d["id"]: d for d in jl(os.path.join(OUT, "model", "elements.jsonl"))}
for e in [x for x in a.elements.split(",") if x]:
    print(e, "|", els[e]["statement"])

for x in near:
    for k in branches[x]["keys"]:
        for l in [l for l in shared if key_match(l, k)]:
            print(x, k, l["sub"], "|", l.get("how"), "|", codes(l))

for l in eff:
    if l["op"] == "propose":
        print("PROP", l["sub"], "|", l.get("how"))
