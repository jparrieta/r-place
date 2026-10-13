#!/usr/bin/env python3
"""Check c1_empties_decisions.json against the empties and summarise the kinds (read-only).

Checks: every empty line is decided once, in c1_empties.py's B1 order; every placement is class 4, chooses a theme
the readers or my B1 placed (J, 13 October), and names concepts of that second-order theme.
Summary: per kind, items, rooms, placed, and the first appearance in B1's reading order; then saturation by kind,
the number of kinds met by each tenth of the reading order and the position of the last new kind.

    python3 out/_analysis/c1_empties_kinds.py [--write]      --write saves c1_empties_kinds.json
"""
import argparse, collections, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "out")

spec = importlib.util.spec_from_file_location("emp", os.path.join(HERE, "c1_empties.py"))
emp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emp)

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()

empties, b3, dis, rev, pos = emp.load()
dec = json.load(open(os.path.join(HERE, "c1_empties_decisions.json"), encoding="utf-8"))
kinds, items = dec["kinds"], dec["items"]

spec2 = importlib.util.spec_from_file_location("bpf", os.path.join(HERE, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(bpf)
store = bpf.pk.Store(ROOT, OUT)

problems = []
if len(items) != len(empties):
    problems.append("%d decisions for %d empties" % (len(items), len(empties)))
seen = set()
for d, r in zip(items, empties):
    key = "%s:%s" % (r["sub"], r["theme_id"])
    if d["item"] != key:
        problems.append("n=%d decided %s, packet order has %s" % (d["n"], d["item"], key))
    if d["item"] in seen:
        problems.append("n=%d %s decided twice" % (d["n"], d["item"]))
    seen.add(d["item"])
    if d["kind"] not in kinds:
        problems.append("n=%d unknown kind %s" % (d["n"], d["kind"]))
    if d["decision"] not in ("empty", "place"):
        problems.append("n=%d decision %s" % (d["n"], d["decision"]))
    if d["decision"] == "place":
        c = b3.get((r["sub"], r["theme_id"])) or {}
        if c.get("class") != 4:
            problems.append("n=%d placed but class %s" % (d["n"], c.get("class")))
        allowed = set((c.get("r1") or []) + (c.get("r2") or []) + (c.get("b1") or []))
        if d["theme"] not in allowed:
            problems.append("n=%d theme %s not among readers' or my B1's %s" % (d["n"], d["theme"], sorted(allowed)))
        th = store.themes.get((r["sub"], r["theme_id"])) or {}
        own = set(th.get("code_ids") or [])
        missing = [x for x in d["codes"].split(",") if x not in own]
        if missing:
            problems.append("n=%d codes %s not in %s" % (d["n"], missing, key))
        if d["theme"] in (c.get("r1") or []) and d["theme"] in (c.get("r2") or []):
            problems.append("n=%d places the readers' own theme %s; the floor revision is about my B1's" % (d["n"], d["theme"]))

print("decisions: %d; problems: %d" % (len(items), len(problems)))
print("\n".join(problems))

n_items = len(empties)
by = collections.defaultdict(list)
for d, r in zip(items, empties):
    by[d["kind"]].append((pos.get(r["sub"]), r["sub"], d))
rows = []
for k in sorted(kinds):
    L = sorted(by.get(k, []), key=lambda x: (x[0], x[1], x[2]["n"]))
    first = L[0] if L else (None, None, None)
    rows.append({"kind": k, "name": kinds[k]["name"], "items": len(L), "rooms": len(set(x[1] for x in L)),
                 "placed": sum(1 for x in L if x[2]["decision"] == "place"),
                 "first_b1_order": first[0], "first_room": first[1],
                 "first_item": first[2]["item"] if first[2] else None, "verdict": kinds[k]["verdict"]})
print("\nkind  items rooms placed  first(B1 order, room)  name")
print("\n".join("%-4s  %5d %5d %6d  %4s %-22s %s" % (x["kind"], x["items"], x["rooms"], x["placed"], x["first_b1_order"],
                                                   x["first_room"], x["name"]) for x in rows))
placed = sum(x["placed"] for x in rows)
print("\nplaced %d; empty after %d of 7844 (%.1f%%)" % (placed, n_items - placed, 100.0 * (n_items - placed) / 7844))

firsts = sorted(x["first_b1_order"] for x in rows if x["first_b1_order"] is not None)
rooms_with_empty = sorted(set(pos.get(r["sub"]) for r in empties))
print("\nsaturation by kind, in B1's reading order (705 rooms):")
print("kinds by first appearance: " + ", ".join("%s@%d" % (x["kind"], x["first_b1_order"]) for x in sorted(rows, key=lambda x: x["first_b1_order"])))
steps = [70, 141, 211, 282, 352, 423, 493, 564, 634, 705]
print("kinds met by each tenth of the order: " + ", ".join("%d:%d" % (s, sum(1 for f in firsts if f <= s)) for s in steps))
print("empties met by each tenth: " + ", ".join("%d:%d" % (s, sum(1 for r in empties if pos.get(r["sub"], 999) <= s)) for s in steps))
print("last new kind at B1 order %d; rooms holding an empty read after it: %d of %d" % (
    firsts[-1], sum(1 for p in rooms_with_empty if p > firsts[-1]), len(rooms_with_empty)))

if a.write:
    pth = os.path.join(HERE, "c1_empties_kinds.json")
    if os.path.exists(pth):
        sys.exit("%s exists" % pth)
    json.dump({"rows": rows, "placed": placed, "empty_after": n_items - placed,
               "firsts": firsts, "problems": problems}, open(pth, "w", encoding="utf-8"), indent=1)
    print("wrote %s" % os.path.relpath(pth, ROOT))
