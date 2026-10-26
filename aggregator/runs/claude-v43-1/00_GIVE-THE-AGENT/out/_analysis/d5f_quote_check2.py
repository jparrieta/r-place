#!/usr/bin/env python3
"""D5, room-form accounts: check the quotes that carry no [room/code] citation. Each must be a substring of one of: a
selected line's how sentence (any room), a room model (model-D-recheck.md or model-D.md of a room the account names),
the model's arrows and elements, tree-D4.md, departures.jsonl, or the room-forms files. Prints the quotes not found.

    python3 out/_analysis/d5f_quote_check2.py --form A out/_analysis/d5a36_account_dry.md
"""
import argparse, glob, json, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("--form", required=True)
ap.add_argument("path")
a = ap.parse_args()
AN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(AN)
sys.path.insert(0, os.path.join(os.path.dirname(OUT), "tools"))
from adaptation_ledger import effective_lines  # noqa: E402

text = open(a.path, encoding="utf-8").read()
src = [l.get("how") or "" for l in effective_lines(OUT, include_particular=True)]
for s in set(re.findall(r"\br/([A-Za-z0-9_]+)", text)):
    for f in ("model-D-recheck.md", "model-D.md"):
        p = os.path.join(OUT, "rooms", s, f)
        if os.path.exists(p):
            src.append(open(p, encoding="utf-8").read())
for f in ["model/arrows.jsonl", "model/elements.jsonl", "tree-D4.md", "departures.jsonl", "room-forms-D4a08c.jsonl",
          "room-forms-D4a08b.jsonl", "room-forms-allocation.md"]:
    src.append(open(os.path.join(OUT, f), encoding="utf-8").read())
named = set(re.findall(r"\br/([A-Za-z0-9_]+)", text))
for l in open(os.path.join(os.path.dirname(OUT), "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in named:
        src.append(r.get("text") or "")
blob = "\n".join(src)
blob_n = blob.replace("“", '"').replace("”", '"')
# the one nested quotation in the members' words, then every cited quote, are taken out before pairing quote marks
work = text.replace('isn\'t "content"', "isn't content")
work = re.sub(r'"[^"\n]*"\s*\[[A-Za-z0-9_]+/c\d+\]', "", work)
quotes = re.findall(r'"([^"\n]{12,})"', work)
bad = [q for q in quotes if q not in blob and q not in blob_n]
print("uncited quotes checked:", len(quotes), "not found:", len(bad))
for q in bad:
    print("  ", q[:140])
