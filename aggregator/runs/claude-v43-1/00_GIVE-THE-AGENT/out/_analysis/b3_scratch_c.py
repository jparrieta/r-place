#!/usr/bin/env python3
"""B3b, while QB3-003 is open: a scratch root under $TMPDIR in which tools/assemble.py can run on option (c),
the halves left out. The scratch out/ links every entry of the real out/ except batches-B3.jsonl, which links
the record before the split (B0192 and B0927 whole, both in EXHAUSTED.tsv), and the five assembler outputs,
which the tool writes into the scratch only. Nothing in the real out/ is written. Used to build and test the
check leg's scripts; the figures of record come from the real assembly once J rules.

    python3 out/_analysis/b3_scratch_c.py   (prints the scratch root)
"""
import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SKIP = {"batches-B3.jsonl", "assign_raw.jsonl", "assign_pass2.jsonl", "multiplacement_log.jsonl",
        "predicted_confusion-B3.jsonl", "b3_classes.jsonl"}


def main():
    s = os.path.join(os.environ.get("TMPDIR", "/tmp"), "b3_scratch_c")
    os.makedirs(os.path.join(s, "out"), exist_ok=True)
    for name in ("package", "tools"):
        if not os.path.lexists(os.path.join(s, name)):
            os.symlink(os.path.join(ROOT, name), os.path.join(s, name))
    for e in os.listdir(OUT):
        d = os.path.join(s, "out", e)
        if e in SKIP or os.path.lexists(d):
            continue
        os.symlink(os.path.join(OUT, e), d)
    old = sorted(glob.glob(os.path.join(OUT, "batches-B3.superseded-*.jsonl")))[-1]
    d = os.path.join(s, "out", "batches-B3.jsonl")
    if not os.path.lexists(d):
        os.symlink(old, d)
    print(s)


if __name__ == "__main__":
    main()
