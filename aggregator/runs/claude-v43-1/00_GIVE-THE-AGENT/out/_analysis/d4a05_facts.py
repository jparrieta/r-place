#!/usr/bin/env python3
"""D4a-05: facts about the selected changes before the method is fixed. Read-only; prints JSON.

    python3 out/_analysis/d4a05_facts.py
"""
import collections, json, os, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import adaptation_ledger as al  # noqa: E402

CHANGE = {"add-step", "add-condition", "link", "restrict", "contradict"}
L = [r for r in al.shared_lines(OUT) if r.get("op") in CHANGE]
rooms = sorted(al.effective_rooms(OUT), key=str.lower)
nolift = [r for r in L if len(r.get("lift") or []) < 4]
per = collections.Counter(r["sub"] for r in L)
arrow = sum(1 for r in L if (r.get("element") or "").startswith("A"))
out = {"selected_lines": len(L), "on_arrows": arrow, "on_elements": len(L) - arrow, "without_lift": len(nolift),
       "rooms_with_changes": len(per), "rooms_without": len(rooms) - len(per),
       "per_room": {"min": min(per.values()), "median": statistics.median(per.values()), "max": max(per.values()),
                    "q1": sorted(per.values())[len(per) // 4], "q3": sorted(per.values())[3 * len(per) // 4]}}
for i, lv in ((1, "T3"), (2, "T4"), (3, "dim")):
    held = collections.defaultdict(set)
    for r in L:
        lf = r.get("lift") or []
        if len(lf) >= 4:
            held[lf[i]].add(r["sub"])
    single = [k for k, v in held.items() if len(v) == 1]
    out[lv] = {"nodes": len(held), "held_by_one_room": len(single),
               "lines_on_single_nodes": sum(1 for r in L if len(r.get("lift") or []) >= 4 and r["lift"][i] in single),
               "rooms_by_node_top5": sorted(((k, len(v)) for k, v in held.items()), key=lambda x: -x[1])[:5]}
print(json.dumps(out, ensure_ascii=False))
