#!/usr/bin/env python3
"""E1a: a look at the shape of the files the audit scripts read. For each path: lines, the keys of the first and
last records (JSONL or JSON), and the first record cut to --width characters. Reads only; prints.

    python3 out/_analysis/e1a_peek.py out/findings.jsonl out/run_manifest.json --width 300
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("paths", nargs="+")
ap.add_argument("--width", type=int, default=300)
a = ap.parse_args()
for p in a.paths:
    if not os.path.exists(p):
        print("%s: absent" % p)
        continue
    if os.path.isdir(p):
        names = sorted(os.listdir(p))
        print("%s: dir, %d entries; first %s; last %s" % (p, len(names), names[:4], names[-3:]))
        continue
    raw = open(p, encoding="utf-8", errors="replace").read()
    lines = [l for l in raw.splitlines() if l.strip()]
    try:
        obj = json.loads(raw)
        if isinstance(obj, list):
            print("%s: JSON list, %d items; keys first %s; last %s" % (
                p, len(obj), sorted(obj[0]) if obj and isinstance(obj[0], dict) else type(obj[0]).__name__ if obj else "-",
                sorted(obj[-1]) if obj and isinstance(obj[-1], dict) else "-"))
            print("   first:", json.dumps(obj[0], ensure_ascii=False)[:a.width] if obj else "-")
        elif isinstance(obj, dict):
            print("%s: JSON object; keys %s" % (p, sorted(obj)[:40]))
            print("   ", json.dumps(obj, ensure_ascii=False)[:a.width])
        continue
    except ValueError:
        pass
    recs = []
    for l in lines:
        try:
            recs.append(json.loads(l))
        except ValueError:
            recs = None
            break
    if recs:
        keys = sorted(set(k for r in recs if isinstance(r, dict) for k in r))
        print("%s: JSONL, %d lines; keys (all lines) %s" % (p, len(recs), keys[:60]))
        print("   first:", json.dumps(recs[0], ensure_ascii=False)[:a.width])
        print("   last: ", json.dumps(recs[-1], ensure_ascii=False)[:a.width])
    else:
        print("%s: text, %d lines, %d words; first line: %s" % (p, len(raw.splitlines()), len(raw.split()),
                                                              (raw.splitlines() or [""])[0][:a.width]))
