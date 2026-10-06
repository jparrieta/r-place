#!/usr/bin/env python3
"""version_log.py — keep every version of the instrument's documents, so a change can be backtracked.

    python3 tools/version_log.py --note "why" FILE [FILE ...]      # from INSTRUMENT/

For each file: if its sha256 differs from the last row for that path in VERSIONS.tsv, copy it to
_versions/<path with / as __>.<UTC stamp>.<ext> and append a row (utc, path, sha256, words, note).
Idempotent: an unchanged file adds nothing.
"""
import argparse, datetime, hashlib, os, shutil, sys

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--note", default="")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    log = os.path.join(a.root, "VERSIONS.tsv")
    vd = os.path.join(a.root, "_versions")
    os.makedirs(vd, exist_ok=True)
    last = {}
    if os.path.exists(log):
        for line in open(log, encoding="utf-8").read().splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 3:
                last[parts[1]] = parts[2]
    else:
        open(log, "w", encoding="utf-8").write("utc\tpath\tsha256\twords\tnote\n")
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    n = 0
    for f in a.files:
        rel = os.path.relpath(f, a.root)
        h = sha(f)
        if last.get(rel) == h:
            continue
        words = len(open(f, encoding="utf-8", errors="replace").read().split())
        base, ext = os.path.splitext(rel.replace("/", "__"))
        shutil.copy2(f, os.path.join(vd, "%s.%s%s" % (base, stamp, ext)))
        with open(log, "a", encoding="utf-8") as L:
            L.write("\t".join([stamp, rel, h, str(words), a.note.replace("\t", " ")]) + "\n")
        n += 1
    print("%d version(s) recorded" % n)

if __name__ == "__main__":
    sys.exit(main())
