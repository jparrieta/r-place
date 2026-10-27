#!/usr/bin/env python3
"""D6a-09 (J's ruling 1e): form B as a residual grouping with three facets, and its lead after the close by facet. The
facets are the three fourth-order themes of room-form-B-account.md, section 14: the scripts (Workarounds, T4-009), the
chat (Backstage decision-making, T4-010) and the raids (Repertoire of contention, T4-020). A defining member of B holds a
facet where it has a selected change line (d5a37_lines.json, role defining) whose fourth-order theme is the facet's. The
counts reproduce the account's (49, 48, 40; 20 holding none). For each facet, and for the
members in none: the rooms, those that coordinated after hour 73, those whose coordinating ended at 73 or later, the mean
aftermath share and the field's kept share (organizing_end-A1.jsonl). Reads only; prints JSON.

    python3 out/_analysis/d6a09_b_facets.py > out/_analysis/d6a09_b_facets.json
"""
import collections, csv, json, os, statistics

AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
# A line holds a facet by its fourth-order theme (the line's 't4'), as the account counted; the element-based count
# (P14, K05, K06; P23, P33; P09, C02, P33) gives 56, 51 and 30 and does not reproduce the account, so it is not used.
FACETS = {"scripts": "T4-009", "chat": "T4-010", "raids": "T4-020"}
EXPECT = {"scripts": 49, "chat": 48, "raids": 40}
rows = list(csv.DictReader(open(os.path.join(OUT, "room-forms-tree-rooms.tsv"), encoding="utf-8"), delimiter="\t"))
dfn = sorted((r["room"] for r in rows if r["form"] == "B" and r["role"] == "defining"), key=str.lower)
lines = json.load(open(os.path.join(AN, "d5a37_lines.json"), encoding="utf-8"))["lines"]
held = collections.defaultdict(set)
for l in lines:
    if l.get("role") == "defining":
        t4 = l.get("t4") if isinstance(l.get("t4"), list) else [l.get("t4")]
        for f, theme in FACETS.items():
            if theme in t4:
                held[l["sub"]].add(f)
oe = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"), encoding="utf-8")
      if l.strip()}


def block(m):
    aft = [oe[s]["aftermath_share"] for s in m if isinstance(oe[s].get("aftermath_share"), (int, float))]
    ends = [oe[s]["organizing_end_hour"] for s in m if isinstance(oe[s].get("organizing_end_hour"), (int, float))]
    return {"n": len(m), "coordinated_after_73": sum(1 for s in m if oe[s].get("aftermath_coordinating_codes")),
            "ended_73_on": sum(1 for e in ends if e >= 73),
            "aftermath_mean": round(statistics.mean(aft), 4) if aft else None,
            "kept": sum(1 for s in m if oe[s]["work_remained"] == "kept")}


res = {"n_defining": len(dfn), "facets": {}, "expected": EXPECT}
for f in FACETS:
    m = [s for s in dfn if f in held[s]]
    res["facets"][f] = block(m)
none = [s for s in dfn if not held[s]]
res["none"] = block(none)
chat_or_scripts = [s for s in dfn if held[s] & {"chat", "scripts"}]
raids_only = [s for s in dfn if held[s] == {"raids"}]
res["chat_or_scripts"] = block(chat_or_scripts)
res["raids_only"] = block(raids_only)
res["all"] = block(dfn)
res["combos"] = dict(collections.Counter("+".join(sorted(held[s])) or "none" for s in dfn))
after = [s for s in dfn if oe[s].get("aftermath_coordinating_codes")]
res["after_73_rooms_by_combo"] = dict(collections.Counter("+".join(sorted(held[s])) or "none" for s in after))
print(json.dumps(res, ensure_ascii=False))
