#!/usr/bin/env python3
"""D5: join a branch account's parts and fill its generated lists (unresolved members, the held proposals as the
tree file states them, the arrows' expectations, the cross-links). Refuses to overwrite an account.

    python3 out/_analysis/d5_assemble.py --branch F01 --parts p1.md p2.md ... [--dry]
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
ap.add_argument("--parts", nargs="+", required=True)
ap.add_argument("--dry", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def rooms(xs):
    return ", ".join("r/%s" % s for s in sorted(xs, key=str.lower))


bs = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
b = bs[a.branch]
ms = b["members"]
local = vlib.local_return_states(OUT)
unres = [s for s in ms if local.get(s, {}).get("local_status", "unresolved") != "validated"]
tree = open(os.path.join(OUT, "tree-D4.md"), encoding="utf-8").read().split("\n")
held = "\n".join(l for l in tree if l.startswith("- **P05, move 198") or l.startswith("- **A11, move 199"))
analysed = {r["sub"] for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
arrows = []
for r in jl(os.path.join(OUT, "model", "arrows.jsonl")):
    k = len(set(r.get("subs") or []) & analysed)
    arrows.append("- %s (%s to %s): %d datings, expected %.3f; not-testable-here" % (
        r["id"], r.get("from"), r.get("to"), k, k / len(analysed) * len(ms)))
subs = sorted(k for k, x in bs.items() if x.get("parent") == a.branch)
own, inner = collections.defaultdict(list), collections.defaultdict(list)
for r in jl(os.path.join(OUT, "crosslinks.jsonl")):
    if a.branch in r["branches"]:
        own[" and ".join(x for x in r["branches"] if x != a.branch)].append(r["sub"])
    elif set(r["branches"]) & set(subs):
        inner[" with ".join(r["branches"])].append(r["sub"])
cl = ["Naming %s, by the other branch:" % a.branch, ""]
cl += ["- %s (%d): %s" % (k, len(v), rooms(v)) for k, v in sorted(own.items())]
if inner:
    cl += ["", "Naming a subform of %s, by pair:" % a.branch, ""]
    cl += ["- %s (%d): %s" % (k, len(v), rooms(v)) for k, v in sorted(inner.items())]
fill = {"@@UNRESOLVED@@": rooms(unres), "@@HELD@@": held, "@@ARROWS@@": "\n".join(arrows), "@@CROSSLINKS@@": "\n".join(cl)}
text = "\n".join(open(p, encoding="utf-8").read().rstrip("\n") for p in a.parts) + "\n"
for k, v in fill.items():
    text = text.replace(k, v)
left = [k for k in fill if k in text]
dest = os.path.join(OUT, "forms", "%s-account.md" % a.branch)
print("unresolved %d of %d; arrows %d; cross-links %d own, %d inner; markers left %s; words %d" % (
    len(unres), len(ms), len(arrows), sum(map(len, own.values())), sum(map(len, inner.values())), left,
    len(text.split())))
if a.dry or left:
    sys.exit(0 if a.dry else 1)
if os.path.exists(dest):
    sys.exit("%s exists; supersede it under a new name" % dest)
open(dest, "w", encoding="utf-8").write(text)
print("wrote", dest)
