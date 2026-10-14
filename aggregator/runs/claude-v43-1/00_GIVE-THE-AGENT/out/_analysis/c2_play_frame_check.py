#!/usr/bin/env python3
"""C2, pass 2, read-only: why a room is or is not frame-filled under c2_play_frame.py's rule. Prints, per room named,
its items_in_window, its coded concepts before h32, the play-frame concepts among them (counted two ways: concepts the
assignment lines cite under a play-frame theme, and every coded concept on a line whose placed themes include one),
and the line count per placed theme.

    python3 out/_analysis/c2_play_frame_check.py ultrahardcore totallynotrobots aceattorney
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
subs = sys.argv[1:]
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p2.json"), encoding="utf-8"))["elements"])
frame = set(els["K01"]["themes"])
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
byc = dict(((c["sub"], c["code_id"]), c) for c in codes)
q = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", "items_in_window",
                    "--json", "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
items = dict((r["sub"], r["items_in_window"]) for r in (json.loads(l) for l in q.stdout.splitlines() if l.startswith("{")))
rows = [json.loads(l) for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8") if l.strip()]
keys = sorted(set(k for r in rows if r["sub"] in subs for k in r))
print("assignment line keys: %s" % ", ".join(keys))
for s in subs:
    mine = [r for r in rows if r["sub"] == s]
    early = [c for c in codes if c["sub"] == s and c.get("hour") is not None and c["hour"] < 32]
    cited = set()
    for r in mine:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in frame:
                cited.update(ids)
    cited_early = sum(1 for i in cited if (s, i) in byc and byc[(s, i)].get("hour") is not None and byc[(s, i)]["hour"] < 32)
    print("\n%s: items %s; coded concepts before h32 %d; frame concepts cited before h32 %d" % (s, items.get(s), len(early), cited_early))
    for r in mine:
        sbt = r.get("support_by_theme") or {}
        print("  %s third_order %s; cited per theme %s" % (r.get("theme_id"), r.get("third_order"),
                                                          dict((t, len(v)) for t, v in sbt.items())))
