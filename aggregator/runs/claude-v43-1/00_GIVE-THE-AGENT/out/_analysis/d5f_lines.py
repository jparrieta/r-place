#!/usr/bin/env python3
"""D5, room-form accounts: one form's selected lines (restrict, add-step, add-condition, link, contradict, with a lift),
with role (defining, thin), element, op, third- and fourth-order node, how and codes; and a table by element and op
(lines and rooms, defining only, against the 558 defining rooms' lines). Prints JSON.

    python3 out/_analysis/d5f_lines.py --form A > out/_analysis/d5a36_lines.json
"""
import argparse, collections, json, os, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
a = ap.parse_args()
sys.argv = [sys.argv[0]]
AN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AN)
import d4a07_features as F  # noqa: E402

OUT = F.OUT


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


forms = {r["id"]: r for r in jl(os.path.join(OUT, "room-forms-D4a08c.jsonl"))}
roles = {}
for line in open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8").read().splitlines()[1:]:
    c = line.split("\t")
    roles[c[0]] = c[2]
mem = set(forms[a.form]["members"])
alldef = {s for s, r in roles.items() if r == "defining"}


def codes(l):
    ev = l.get("evidence") or {}
    return ev.get("codes", []) if isinstance(ev, dict) else []


rows, tab = [], collections.defaultdict(lambda: {"lines": 0, "rooms": set(), "pop_lines": 0, "pop_rooms": set(), "t4": collections.Counter()})
for l in F.PLACED:
    key = (l["element"], l["op"])
    if l["sub"] in alldef:
        tab[key]["pop_lines"] += 1
        tab[key]["pop_rooms"].add(l["sub"])
    if l["sub"] in mem:
        role = roles[l["sub"]]
        rows.append({"id": l.get("id"), "sub": l["sub"], "role": role, "element": l["element"], "op": l["op"],
                     "t3": l["lift"][1], "t4": l["lift"][2], "how": l.get("how"), "codes": codes(l)})
        if role == "defining":
            tab[key]["lines"] += 1
            tab[key]["rooms"].add(l["sub"])
            tab[key]["t4"][l["lift"][2]] += 1
ndef = len(mem & alldef)
fl = sum(v["lines"] for v in tab.values())
pl = sum(v["pop_lines"] for v in tab.values())
table = sorted([{"element": k[0], "op": k[1], "lines": v["lines"], "rooms": len(v["rooms"]), "line_share": round(v["lines"] / fl, 4),
                 "pop_line_share": round(v["pop_lines"] / pl, 4), "ratio": round((v["lines"] / fl) / (v["pop_lines"] / pl), 2) if v["pop_lines"] else None,
                 "t4": dict(v["t4"].most_common(3))} for k, v in tab.items() if v["lines"]], key=lambda r: -r["lines"])
print(json.dumps({"form": a.form, "n_def": ndef, "lines_def": fl, "lines_pop_def": pl, "table": table, "lines": rows}, ensure_ascii=False))
