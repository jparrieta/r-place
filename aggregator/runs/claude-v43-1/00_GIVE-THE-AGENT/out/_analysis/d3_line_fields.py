#!/usr/bin/env python3
"""D3: the ledger fields of named adaptation lines, whole (id, element, op, kind, condition, statement, observation,
how, relation, portable, cited concepts), from adaptations.jsonl. Writes nothing.

  python3 out/_analysis/d3_line_fields.py --ids thailand-008,lost-012
"""
import argparse
import json

FIELDS = ("element", "op", "kind", "condition", "statement", "observation", "how", "relation", "portable", "concepts",
          "cites", "evidence")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True)
    a = ap.parse_args()
    ids = [i for i in a.ids.split(",") if i]
    found = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            if x.get("id") in ids:
                found[x["id"]] = x
    for i in ids:
        x = found.get(i)
        if x is None:
            print(f"{i}: not in adaptations.jsonl")
            continue
        print(f"== {i}")
        for f in FIELDS:
            if f in x and x[f] not in (None, "", [], {}):
                print(f"   {f}: {json.dumps(x[f], ensure_ascii=False)}")


if __name__ == "__main__":
    main()
