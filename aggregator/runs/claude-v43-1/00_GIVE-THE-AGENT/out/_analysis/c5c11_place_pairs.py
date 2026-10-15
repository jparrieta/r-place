#!/usr/bin/env python3
"""C5c-11, problem 2, part B (rules logged first, diary C5c-11, abductive): pairs of a call and its reply. In each room,
the first part is the earliest item carrying a cited concept of the calls element (P01) that has a coded direct reply by
another author (package/store/items.jsonl); the reply is the earliest such coded direct reply. Both are given whole as
their coded passages joined in text order (codes through mem.py). 80 rooms drawn with random.Random(20261015) from the
rooms with a pair. Writes c5c11_place_sample.json (refuses to redraw an existing sample; --print reprints it).

    python3 out/_analysis/c5c11_place_pairs.py [--print]
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c5c11_place_sample.json")
if "--print" not in sys.argv:
    if os.path.exists(DEST):
        sys.exit("the sample exists; run with --print")
    els = {e["id"]: e for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json")))["elements"]}
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json",
                        "--limit", "10000000"], cwd=ROOT, capture_output=True, text=True)
    allc = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
    codes = {(c["sub"], c["code_id"]): c for c in allc}
    on_item = collections.defaultdict(list)
    for c in allc:
        if c.get("item_id"):
            on_item[(c["sub"], c["item_id"])].append(c)
    rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]
    items, kids = {}, collections.defaultdict(list)
    for l in open(os.path.join(ROOT, "package", "store", "items.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        items[(r["sub"], r["item_id"])] = r
        if r.get("parent_id"):
            kids[(r["sub"], r["parent_id"])].append(r)
    themes = set(els["P01"]["themes"])
    calls = collections.defaultdict(set)
    for r in rows:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in themes:
                for i in ids:
                    c = codes.get((r["sub"], i))
                    if c and c.get("item_id") and (r["sub"], c["item_id"]) in items:
                        calls[r["sub"]].add(c["item_id"])

    def text(sub, item):
        cs = sorted(on_item[(sub, item)], key=lambda c: (c.get("start") or 0))
        return " | ".join(" ".join(str(c.get("text") or "").split()) for c in cs), [c["code_id"] for c in cs]

    pairs = {}
    for sub, its in calls.items():
        for it in sorted(its, key=lambda i: (items[(sub, i)]["hour"] is None, items[(sub, i)]["hour"] or 0)):
            a = items[(sub, it)]
            if a["hour"] is None:
                continue
            reps = sorted((r for r in kids[(sub, it)] if r["state"] == "coded" and r.get("author") != a.get("author")
                           and r.get("hour") is not None), key=lambda r: r["hour"])
            if reps:
                r = reps[0]
                ft, fc = text(sub, it)
                rt, rc = text(sub, r["item_id"])
                earlier = sum(1 for x in kids[(sub, it)] if x.get("author") != a.get("author") and x.get("hour") is not None
                              and x["hour"] < r["hour"])
                pairs[sub] = {"first_item": it, "first_codes": fc, "first_hour": a["hour"], "first_text": ft,
                              "reply_item": r["item_id"], "reply_codes": rc, "reply_hour": r["hour"],
                              "reply_author": r.get("author"), "reply_text": rt, "uncoded_replies_before": earlier}
                break
    pick = sorted(random.Random(20261015).sample(sorted(pairs), min(80, len(pairs))))
    json.dump({"rooms_with_pair": len(pairs), "seed": 20261015, "drawn": {s: pairs[s] for s in pick}},
              open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.load(open(DEST, encoding="utf-8"))
print("rooms with a pair: %d; drawn: %d" % (s["rooms_with_pair"], len(s["drawn"])))
for i, (sub, r) in enumerate(s["drawn"].items(), 1):
    print("%02d %s %s h%.2f -> %s h%.2f (%d uncoded before)\n   FIRST: %s\n   REPLY: %s" % (
        i, sub, r["first_codes"], r["first_hour"], r["reply_codes"], r["reply_hour"], r["uncoded_replies_before"],
        r["first_text"], r["reply_text"]))
