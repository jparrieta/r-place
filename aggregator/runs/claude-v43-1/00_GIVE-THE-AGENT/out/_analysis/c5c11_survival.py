#!/usr/bin/env python3
"""C5c-11, problem 2, part A (rules logged first, diary C5c-11, abductive): what survives in the coded record of the
replies to a call. For every item carrying a cited concept of the calls element (P01) and of the attack element (P09)
(c2_elements_c5c2.json themes, assignments_final.jsonl support_by_theme), the direct replies by another author
(package/store/items.jsonl, parent_id) by state: coded (text in the coded record), bridge (uncoded, kept for a coded
descendant), collapsed (uncoded, no text), removed; and those whose author is [deleted]. No reply text is read. Writes
c5c11_survival.json; prints the table.

    python3 out/_analysis/c5c11_survival.py
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
els = {e["id"]: e for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json")))["elements"]}
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = {(c["sub"], c["code_id"]): c for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{"))}
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]
items = {}
kids = collections.defaultdict(list)
for l in open(os.path.join(ROOT, "package", "store", "items.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    items[(r["sub"], r["item_id"])] = r
    if r.get("parent_id"):
        kids[(r["sub"], r["parent_id"])].append(r)


def call_items(eid):
    themes, out = set(els[eid]["themes"]), set()
    for r in rows:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in themes:
                for i in ids:
                    c = codes.get((r["sub"], i))
                    if c and c.get("item_id"):
                        out.add((r["sub"], c["item_id"]))
    return out


res = {}
for name, eid in (("calls to place (P01)", "P01"), ("attack calls (P09)", "P09")):
    its = [k for k in call_items(eid) if k in items]
    st, dele, n_rep, with_rep, with_coded = collections.Counter(), 0, 0, 0, 0
    for k in its:
        author = items[k].get("author")
        reps = [r for r in kids[k] if r.get("author") != author]
        n_rep += len(reps)
        with_rep += bool(reps)
        with_coded += any(r["state"] == "coded" for r in reps)
        for r in reps:
            st[r["state"]] += 1
            dele += r.get("author") == "[deleted]" and r["state"] != "coded"
    res[name] = {"items": len(its), "with_reply": with_rep, "with_coded_reply": with_coded, "direct_replies": n_rep,
                 "by_state": dict(st), "uncoded_with_author_deleted": dele}
    print("%s: %d call items; %d with a direct reply by another author, %d with a coded one" % (
        name, len(its), with_rep, with_coded))
    print("   direct replies %d: %s; share coded %.3f; uncoded with author [deleted] %d (%.3f)" % (
        n_rep, dict(st), st["coded"] / n_rep if n_rep else 0, dele, dele / n_rep if n_rep else 0))
json.dump(res, open(os.path.join(OUT, "_analysis", "c5c11_survival.json"), "w", encoding="utf-8"), indent=1)
