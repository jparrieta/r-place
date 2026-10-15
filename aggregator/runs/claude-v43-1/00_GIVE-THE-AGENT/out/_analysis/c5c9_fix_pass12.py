#!/usr/bin/env python3
"""C5c-09: the pass 12 line in account_passes.jsonl named F-019 and F-020 as tier events, and validate.py takes tier
events only from tier_history.jsonl and model/history.jsonl. Rewrites that one line (written this leg) with the two
finding ids removed from tier_events; the findings stay named in what_changed. Refuses unless the last line is pass 12
of C5c-09.

    python3 out/_analysis/c5c9_fix_pass12.py
"""
import json, os, sys

P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "out",
                 "account_passes.jsonl")
rows = [json.loads(l) for l in open(P, encoding="utf-8") if l.strip()]
last = rows[-1]
if last.get("pass") != 12 or last.get("leg") != "C5c-09":
    sys.exit("the last line is not pass 12 of C5c-09")
last["tier_events"] = [e for e in last["tier_events"] if not e.startswith("F-")]
open(P, "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print("pass 12 tier_events now: %s" % last["tier_events"])
