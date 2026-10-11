#!/usr/bin/env python3
"""B2: for pairs A->B, print A's name, gloss and must_not_show, and B's name, gloss and must_show (scheme.jsonl).

Usage: python3 out/_analysis/b2_pair_text.py T3-002:T3-044 T3-009:T3-072 ...
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = {r["id"]: r for r in (json.loads(x) for x in open(os.path.join(ROOT, "out", "scheme.jsonl"), encoding="utf-8"))}
for p in sys.argv[1:]:
    a, b = p.split(":")
    print("== %s %s -> %s %s" % (a, S[a]["name"], b, S[b]["name"]))
    print("  %s gloss: %s" % (a, S[a]["gloss"]))
    print("  %s must_not_show: %s" % (a, S[a]["must_not_show"]))
    print("  %s gloss: %s" % (b, S[b]["gloss"]))
    print("  %s must_show: %s" % (b, S[b]["must_show"]))
