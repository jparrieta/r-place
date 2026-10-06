#!/usr/bin/env python3
"""bundle_history.py: every earlier instrument version in one compressed file.

    python3 bundle_history.py --add "coder=<Layer A>/10_instrument" --add "aggregator=<...>/60_aggregator" \
        [--add "sandboxes=<...>/61_sandboxes"] --out <Jail>/rplace-instrument-history.tar.gz [--max-file-mb 50]

Handler side, on the Mac. Packs each folder under its label into one .tar.gz, skipping data stores
(the same list as gather_collection.py), transcripts and any single file above --max-file-mb, and
writes HISTORY-MANIFEST.tsv inside the archive and beside it (label, path, bytes, packed or why not).
The archive goes up as one GitHub release asset if it is under 2 GB, else to the Drive folder; the
Manual carries one link either way. Never writes in the source folders; never deletes.
"""
import argparse, fnmatch, io, os, sys, tarfile, time

SKIP_DIRS = {"data", ".data", "raw24", "users", "aggregate", "venue_corpora", "_incoming", "_to_delete", "to delete",
             "__pycache__", ".git", "node_modules", ".venv", "venv", ".cc", ".obsidian"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", action="append", required=True, help='"label=path"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-file-mb", type=float, default=50)
    ap.add_argument("--exclude", action="append", default=[], help="glob on label/path; a run's output, not an instrument")
    a = ap.parse_args(argv)
    cap = a.max_file_mb * 1024 * 1024
    rows, total = [], 0
    with tarfile.open(a.out, "w:gz", compresslevel=6) as tar:
        for spec in a.add:
            label, root = spec.split("=", 1)
            root = os.path.expanduser(root)
            if not os.path.isdir(root):
                print("not found: %s" % root, file=sys.stderr)
                continue
            for d, dirs, files in os.walk(root):
                dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
                for f in sorted(files):
                    p = os.path.join(d, f)
                    rel = os.path.relpath(p, root)
                    try:
                        n = os.path.getsize(p)
                    except OSError:
                        continue
                    key = "%s/%s" % (label, rel)
                    hit = next((g for g in a.exclude if fnmatch.fnmatch(key, g)), None)
                    if hit:
                        rows.append((label, rel, n, "skipped: %s" % hit))
                        continue
                    if n > cap:
                        rows.append((label, rel, n, "skipped: above %.0f MB" % a.max_file_mb))
                        continue
                    if f.endswith(".jsonl") and "_transcripts" in d:
                        rows.append((label, rel, n, "skipped: transcript"))
                        continue
                    tar.add(p, arcname=os.path.join("instrument-history", label, rel), recursive=False)
                    rows.append((label, rel, n, "packed"))
                    total += n
        man = "label\tpath\tbytes\tstatus\n" + "".join("%s\t%s\t%d\t%s\n" % r for r in rows)
        info = tarfile.TarInfo("instrument-history/HISTORY-MANIFEST.tsv")
        info.size, info.mtime = len(man.encode()), int(time.time())
        tar.addfile(info, io.BytesIO(man.encode()))
    open(os.path.splitext(os.path.splitext(a.out)[0])[0] + "-MANIFEST.tsv", "w", encoding="utf-8").write(man)
    size = os.path.getsize(a.out)
    print("packed %d files (%.1f MB raw) into %s, %.1f MB; skipped %d" % (sum(r[3] == "packed" for r in rows), total / 1e6, a.out,
                                                                      size / 1e6, sum(r[3] != "packed" for r in rows)))
    print("release asset: %s" % ("fits (under 2 GB)" if size < 2e9 else "too big; put it on the Drive"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
