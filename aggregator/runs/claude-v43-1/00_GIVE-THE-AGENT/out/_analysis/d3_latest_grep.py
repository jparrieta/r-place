#!/usr/bin/env python3
"""D3: lines whose latest ruling's reason matches a regex, with element, op, decision, kind, pair and leg, and the
reason whole with --reasons. Optional --ids limits to named lines. Counts by element, op and kind at the end.
Writes nothing.

  python3 out/_analysis/d3_latest_grep.py --regex 'successor canvas' [--ops add-step,link] [--ids a-001,b-002] [--reasons]
"""
import argparse
import json
import re
from collections import Counter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regex", default="")
    ap.add_argument("--ops", default="")
    ap.add_argument("--ids", default="")
    ap.add_argument("--reasons", action="store_true")
    a = ap.parse_args()
    ops = {o for o in a.ops.split(",") if o}
    ids = {i for i in a.ids.split(",") if i}
    rx = re.compile(a.regex, re.I) if a.regex else None
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = x
    latest = {}
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            latest[r["adaptation"]] = r
    n = Counter()
    for i in sorted(latest):
        r = latest[i]
        x = meta.get(i, {})
        if ids and i not in ids:
            continue
        if ops and x.get("op") not in ops:
            continue
        if rx and not rx.search(r.get("reason") or ""):
            continue
        kind = r.get("kind") or "-"
        n[(str(x.get("element")), str(x.get("op")), f"{r.get('decision')}/{kind}")] += 1
        row = [i, str(x.get("element")), str(x.get("op")), f"{r.get('decision')}/{kind}", r.get("pair") or "-",
               r.get("leg") or "-"]
        if a.reasons:
            row.append(r.get("reason") or "")
        print(" | ".join(row))
    print("counts:")
    for k, v in sorted(n.items()):
        print("   " + " | ".join(k) + f" | {v}")


if __name__ == "__main__":
    main()
