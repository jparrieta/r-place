#!/usr/bin/env python3
"""snap.py — the record of what existed when.

    python3 tools/snap.py NN <label> [--out out]

Writes `out/_snap/NN-<label>.sha256`: one line per file under `out/`, its sha256, its size in
bytes and the time of the snap, so every working file is versioned as it stood, and beside it a copy of
`model/elements.jsonl`, `model/arrows.jsonl` and `scheme_v2.jsonl` in `out/_snap/NN-<label>/`, which
`mem.py diff-model NN-<label>` and `diff-scheme NN-<label>` compare against. `validate.py NN`
runs it at every close (`NN-close`); you run it yourself before any step whose order a reader
will press on. Four orderings are proved by it and by nothing else (the standing instructions):
at stages D5 and 17 the names file is snapped before batch 2 is opened (`12 names`, `17 names`);
at 11 and 16 the cut is snapped before anything is projected onto it (`11 cut`, `16 cut`); at 17
the activation paragraphs are snapped before the canvas blocks are opened (`17 activation`).

A snap is written once under its name. A second snap with the same stage and label refuses,
because a snap that can be rewritten proves nothing; take a new label. The snap records the
files as they are and does not judge them.

    python3 tools/snap.py --verify out/_snap/D5-names.sha256 [--out out]

prints, for every file the snap lists, whether it is unchanged, changed or gone since the snap.
Stage 18 uses it for the four orderings. Exit 1 if anything changed or is gone.
"""
import datetime
import hashlib
import os
import shutil
import sys

SKIP_DIRS = {"_snap"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def listing(out):
    rows = []
    for d, dirs, files in os.walk(out):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, out)
            rows.append((rel, sha(p), os.path.getsize(p)))
    return rows


def snap(stage, label, out):
    stage = str(stage).upper()
    if not label or any(ch in label for ch in " /\\"):
        sys.exit("label must be one word, e.g. names, cut, activation, close")
    d = os.path.join(out, "_snap")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "%s-%s.sha256" % (stage, label))
    if os.path.exists(p):
        sys.exit("REFUSING: %s exists. A snap is written once; take a new label." % p)
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = listing(out)
    with open(p, "w", encoding="utf-8") as f:
        f.write("# snap %s %s at %s over %s: %d files\n" % (stage, label, t, out, len(rows)))
        for rel, h, n in rows:
            f.write("%s  %d  %s  %s\n" % (h, n, t, rel))
    # a copy of the model and the scheme beside the listing, for mem.py diff-model and diff-scheme
    cp = os.path.join(d, "%s-%s" % (stage, label))
    for rel in ("model/elements.jsonl", "model/arrows.jsonl", "scheme_v2.jsonl"):
        if os.path.exists(os.path.join(out, rel)):
            os.makedirs(os.path.dirname(os.path.join(cp, rel)), exist_ok=True)
            shutil.copy2(os.path.join(out, rel), os.path.join(cp, rel))
    own = sha(p)
    print("snap %s-%s: %d files at %s -> %s (sha256 %s)" % (stage, label, len(rows), t,
                                                             os.path.relpath(p), own[:16]))
    return 0


def verify(snap_path, out):
    if not os.path.exists(snap_path):
        sys.exit("no such snap: %s" % snap_path)
    bad = 0
    for line in open(snap_path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        h, n, t, rel = line.rstrip("\n").split("  ", 3)
        p = os.path.join(out, rel)
        if not os.path.exists(p):
            print("gone       %s" % rel); bad += 1
        elif sha(p) != h:
            print("changed    %s  (%d -> %d bytes)" % (rel, int(n), os.path.getsize(p))); bad += 1
        else:
            print("unchanged  %s" % rel)
    print("%d file(s) changed or gone since %s" % (bad, os.path.basename(snap_path)))
    return 1 if bad else 0


def main(argv):
    out = "out"
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        del argv[i:i + 2]
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if argv[0] == "--verify":
        return verify(argv[1], out)
    if len(argv) < 2:
        print(__doc__)
        return 2
    return snap(argv[0], argv[1], out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
