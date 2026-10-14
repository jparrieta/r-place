#!/usr/bin/env python3
"""C3b, abductive read prompted by threshold models of collective behaviour (recalled: Granovetter 1978). Draws, from
`mem.py codes --fourth T4-012 --json` (Collective efficacy, the doubt-about-numbers element's theme), each room's first
concept by hour, then a seeded sample (random.Random(20261014)) of up to 40 rooms, and prints each sampled concept whole
(room, code, hour, the coder's label, the words) for reading. Writes the sample to out/_analysis/c3b_threshold_sample.json.

    python3 out/_analysis/c3b_threshold_sample.py
"""
import json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(ROOT, "out", "_analysis", "c3b_threshold_sample.json")
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--fourth", "T4-012", "--json",
                    "--limit", "10000000"], cwd=ROOT, capture_output=True, text=True)
cs = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
first = {}
for c in cs:
    if c.get("hour") is None:
        continue
    cur = first.get(c["sub"])
    if cur is None or c["hour"] < cur["hour"]:
        first[c["sub"]] = c
rooms = sorted(first)
pick = sorted(random.Random(20261014).sample(rooms, min(40, len(rooms))))
rows = []
for s in pick:
    c = first[s]
    rows.append({"sub": s, "code": c["code_id"], "hour": c["hour"], "label": c.get("first_order") or "",
                 "text": " ".join(str(c.get("text") or "").split())})
json.dump(rows, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("concepts under T4-012: %d in %d rooms; sampled %d rooms" % (len(cs), len(rooms), len(rows)))
for i, r in enumerate(rows, 1):
    print("%d. %s %s h%.2f | %s | %s" % (i, r["sub"], r["code"], r["hour"], r["label"], r["text"]))
