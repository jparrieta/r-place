#!/usr/bin/env python3
"""D5, section 2.10: the representative members of one branch by the rule in the diary (D5a-01). Prints JSON.

    python3 out/_analysis/d5_reps.py --branch F01
"""
import argparse, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--branch", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def level(node):
    return "4" if node.startswith("T4-") else "3" if node.startswith("T3-") else "dim" if node.startswith("D") else "target"


bs = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}
b = bs[a.branch]
ms = set(b["members"])
t4 = {m: r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")) for m in r.get("members") or []}
op, el, node = b["keys"][0].split(":")
theme = node if node.startswith("T4-") else t4.get(node)
keyn = collections.Counter(l["sub"] for l in shared_lines(OUT) if l["sub"] in ms and l["op"] == op
                           and l["element"] == el and distance.node_at(l, level(node)) == node)
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
room = collections.defaultdict(collections.Counter)
for r in jl(os.path.join(STORE, "codes.jsonl")):
    if r["sub"] in ms:
        nodes = [t4[x] for x in place.get((r["sub"], r.get("theme_id")), []) if x in t4]
        for nd in nodes:
            room[r["sub"]][nd] += 1 / len(nodes)
by = collections.defaultdict(list)
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    by[r["sub"]].append(r)
subs = collections.Counter(s for k, x in bs.items() if x.get("parent") == a.branch for s in x["members"])
rows = []
for s in sorted(ms):
    ruled = [r for r in by[s] if r.get("ruled_by") == "analyst"]
    vs = {e["verdict"] for r in by[s] for e in (r.get("readers") or [])}
    v = ruled[-1]["verdict"] if ruled else (vs.pop() if len(vs) == 1 else None)
    tot = sum(room[s].values())
    rows.append({"sub": s, "verdict": v, "key_lines": keyn[s], "subforms": subs[s], "concepts": round(tot, 1),
                 "fit": round(room[s][theme] / tot, 4) if tot and theme else 0.0})
cand = [r for r in rows if r["verdict"] == "composes" and r["key_lines"] >= 2]
best = max(cand, key=lambda r: (r["fit"], r["key_lines"])) if cand else None
worst = min(rows, key=lambda r: (r["fit"], r["key_lines"]))
length = max(rows, key=lambda r: (r["subforms"], r["key_lines"], r["concepts"]))
print(json.dumps({"branch": a.branch, "key": b["keys"][0], "theme": theme, "best": best, "worst": worst,
                  "length": length, "rows": rows}, ensure_ascii=False))
