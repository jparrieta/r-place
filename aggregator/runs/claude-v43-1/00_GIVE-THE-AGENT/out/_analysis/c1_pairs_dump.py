#!/usr/bin/env python3
"""C1, read-only on the scheme: for the given themes, every stale or unconfirmed gate pair, each shown side by side by
`mem.py gates T3-a T3-b` (so the view and its read log are the tool's own), written whole into one file to be read in
pages. Prints the pair count.

    python3 out/_analysis/c1_pairs_dump.py --themes T3-002,T3-015 --out out/_analysis/c1_rechecks/pairs-pass3.md
"""
import argparse, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def mem(*args):
    p = subprocess.run([sys.executable, "-W", "ignore", os.path.join(ROOT, "tools", "mem.py")] + list(args) + ["--limit", "400"],
                       cwd=ROOT, capture_output=True, text=True)
    return [l for l in (p.stdout or "").splitlines() if not l.startswith("[end") and not l.startswith("[lines")]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--themes", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pairs = []
    for t in a.themes.split(","):
        for l in mem("gates", t)[1:]:
            m = re.match(r"\s+(T3-\d{3})\s+(\S+)", l)
            if m and m.group(2) != "confirmed":
                pr = tuple(sorted((t, m.group(1))))
                if pr not in pairs:
                    pairs.append(pr)
    L = []
    for x, y in pairs:
        L += [l for l in mem("gates", x, y) if not l.startswith("read both")] + [""]
    p = os.path.join(ROOT, a.out)
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("%d pairs written to %s (%d lines)" % (len(pairs), a.out, len(L)))
    print(";".join("%s|%s" % pr for pr in pairs))


if __name__ == "__main__":
    main()
