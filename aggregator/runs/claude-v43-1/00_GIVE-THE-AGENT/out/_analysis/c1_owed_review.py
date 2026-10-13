#!/usr/bin/env python3
"""C1: a review packet for the rechecks the named gate changes owe and have not done (vlib.owed_rechecks), each item
once, with the changes that owe it. Runs c1_review_pack.py on those items, so the packet shows every concept's label
and, whole, the concepts counted for --themes or matching --grep. Prints the items with their changes and line.

    python3 out/_analysis/c1_owed_review.py --changes gate:28,gate:29 --themes T3-031 --grep "..." --name gates-28-29
"""
import argparse, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changes", required=True); ap.add_argument("--themes", default=""); ap.add_argument("--grep", default="")
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    want = [x.strip() for x in a.changes.split(",") if x.strip()]
    by = {}
    found = set()
    for ch in vlib.owed_rechecks(OUT, "C1"):
        if ch["ref"] not in want:
            continue
        found.add(ch["ref"])
        for k in ch["missing"]:
            by.setdefault(k, []).append(ch["ref"])
    if found != set(want):
        sys.exit("no such change: %s" % ", ".join(sorted(set(want) - found)))
    items = sorted(by)
    for k in items:
        print("%s:%s %s" % (k[0], k[1], ",".join(by[k])))
    print("%d items owed by %s" % (len(items), ", ".join(want)))
    if not items:
        return
    cmd = [sys.executable, "-W", "ignore", os.path.join(OUT, "_analysis", "c1_review_pack.py"),
           "--items", ",".join("%s:%s" % k for k in items), "--themes", a.themes, "--grep", a.grep, "--name", a.name]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print((r.stdout or "").strip(), (r.stderr or "").strip()[-300:])


if __name__ == "__main__":
    main()
