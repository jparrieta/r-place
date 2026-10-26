#!/usr/bin/env python3
"""D5: print a branch's propose lines, one arrow's member lines and expectation, and the account's sentence around that arrow.

    python3 out/_analysis/d5_branch_misc.py F17 A20 out/_analysis/d5a17_F17_arrows.json
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

branch, arrow, arrows_file = sys.argv[1], sys.argv[2], sys.argv[3]
b = next(json.loads(l) for l in open(os.path.join(ROOT, "out", "branches.jsonl"), encoding="utf-8") if json.loads(l)["id"] == branch)
ms = set(b["members"])
for l in effective_lines(os.path.join(ROOT, "out"), include_particular=True):
    if l["sub"] in ms and l["op"] == "propose":
        print("PROPOSE", l["sub"], "|", (l.get("how") or "")[:120])
a = json.load(open(arrows_file, encoding="utf-8"))
print([(x["arrow"], x["subs"], x["expected"], x["member_lines"]) for x in a["arrows"] if x["arrow"] == arrow])
t = open(os.path.join(ROOT, "out", "account.md"), encoding="utf-8").read()
i = t.find("[" + arrow)
print(t[max(0, i - 600):i + 150] if i >= 0 else "no mention")
