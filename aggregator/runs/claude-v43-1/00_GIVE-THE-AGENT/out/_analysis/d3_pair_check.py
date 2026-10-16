#!/usr/bin/env python3
"""Check that every `pair` in the given rulings files names a line of the same element (any op),
and list pairs that point to a line not yet ruled in these files, so it can be ruled to match.

  python3 out/_analysis/d3_pair_check.py --element P04 --files out/_analysis/d3_rulings/P04-*.jsonl
"""
import argparse
import json
import re
import subprocess
import sys

OPS = ("absent", "add-condition", "add-step", "instantiate", "link", "restrict", "contradict")


def element_ids(element):
    ids = set()
    for op in OPS:
        head = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element,
                               "--op", op, "--offset", "0", "--limit", "1"],
                              capture_output=True, text=True).stdout
        m = re.search(r"(\d+) lines in all", head)
        total = int(m.group(1)) if m else 0
        for off in range(0, total, 100):
            out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element,
                                  "--op", op, "--offset", str(off), "--limit", "100"],
                                 capture_output=True, text=True).stdout
            ids.update(re.findall(r"^== (\S+)", out, re.M))
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--files", nargs="+", required=True)
    a = ap.parse_args()
    known = element_ids(a.element)
    ruled, pairs = set(), []
    for fn in a.files:
        for ln in open(fn):
            if ln.strip():
                r = json.loads(ln)
                ruled.add(r["adaptation"])
                if r.get("pair"):
                    pairs.append((r["adaptation"], r["pair"]))
    bad = [(x, p) for x, p in pairs if p not in known]
    unruled = sorted({p for _, p in pairs if p in known and p not in ruled})
    print(f"{a.element}: {len(known)} lines; {len(ruled)} ruled in these files; {len(pairs)} pairs")
    print(f"pairs naming no {a.element} line: {bad if bad else 'none'}")
    print(f"pairs naming a line not yet ruled here: {unruled if unruled else 'none'}")


if __name__ == "__main__":
    main()
