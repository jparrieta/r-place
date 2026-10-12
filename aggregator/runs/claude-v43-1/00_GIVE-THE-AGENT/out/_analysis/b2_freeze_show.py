#!/usr/bin/env python3
"""B2b-r3-p3: print the named themes of out/scheme.jsonl whole (every field), one after another. Reads only.
    python3 out/_analysis/b2_freeze_show.py T3-002 T3-033 T3-038"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = {r["id"]: r for r in (json.loads(x) for x in open(os.path.join(ROOT, "out", "scheme.jsonl"), encoding="utf-8") if x.strip())}
for t in sys.argv[1:]:
    r = rows[t]
    print("=" * 8, t)
    for k, v in r.items():
        if k == "discriminators":
            for d in v:
                print("  disc vs %s: %s" % (d.get("vs"), d.get("question")))
        else:
            print("  %s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
