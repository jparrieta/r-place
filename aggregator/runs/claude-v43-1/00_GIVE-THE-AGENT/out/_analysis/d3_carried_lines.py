#!/usr/bin/env python3
"""List the ruled lines outside one element's own group whose reasons name that element.

It reads every ruling file in out/_analysis/d3_rulings/ except the element's own (<EL>-*.jsonl),
keeps the lines whose reason names the element, and shows each line's latest ruling in
out/adjudications.jsonl (decision, kind, pair), so carried lines can be read again when the
element's status changes. Lines ruled as evidence limits (kind none) are left out unless --all.

  python3 out/_analysis/d3_carried_lines.py --element P21 [--all] [--width 400]
"""
import argparse
import glob
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--width", type=int, default=400, help="characters of the reason shown")
    a = ap.parse_args()
    pat = re.compile(r"\b" + re.escape(a.element) + r"\b")
    latest = {}
    for ln in open("out/adjudications.jsonl"):
        if ln.strip():
            r = json.loads(ln)
            latest[r.get("adaptation")] = r
    rows = []
    for path in sorted(glob.glob("out/_analysis/d3_rulings/*.jsonl")):
        name = os.path.basename(path)
        if name.startswith(a.element + "-"):
            continue
        for ln in open(path):
            if not ln.strip():
                continue
            r = json.loads(ln)
            if not pat.search(r.get("reason", "")):
                continue
            last = latest.get(r["adaptation"], {})
            if not a.all and last.get("kind") == "none":
                continue
            rows.append((name, r, last))
    seen = {}
    for name, r, last in rows:
        seen.setdefault(r["adaptation"], []).append(name)
    print(f"{a.element}: {len(rows)} lines in {len(seen)} ids name it outside its own files")
    for name, r, last in rows:
        same = "latest = this file" if last.get("reason") == r.get("reason") else "latest differs"
        print(f"\n== {r['adaptation']}  [{name}]  latest: {last.get('decision')}/{last.get('kind', '-')}"
              f" pair {last.get('pair', '-')}  ({same})")
        print("   " + r.get("reason", "")[:a.width])


if __name__ == "__main__":
    main()
