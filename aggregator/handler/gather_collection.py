#!/usr/bin/env python3
"""gather_collection.py: copy the code that collected and built the data into the repository.

    python3 gather_collection.py --layer "Layer A=<path>" --layer "Layer B=<path>" [--layer "Gioia=<path>"] \
        --out <rplace>/Instrument/COLLECTION [--dry]

Handler side, on the Mac. Walks each layer, skips every data store, and copies the code (.py .sh
.R .ipynb .sql, and the .md, .toml, .yaml beside them) into COLLECTION/<layer>/<same relative path>.
Writes COLLECTION/INVENTORY.tsv (layer, path, bytes, sha1, first line of the docstring or comment)
and COLLECTION/CANDIDATES.md: the scripts whose text names the stores the Manual describes
(raw24, aggregate, users, atlas, tiles, the event window), so the page for each store can link the
script that built it. Never writes in the layers; never deletes. A file above 2 MB is listed and not
copied. Copying is idempotent: a file whose sha1 already matches is left alone.
"""
import argparse, hashlib, os, re, shutil, sys

CODE = {".py", ".sh", ".r", ".R", ".ipynb", ".sql", ".jl"}
SIDE = {".md", ".toml", ".yaml", ".yml", ".cfg", ".txt"}
SKIP_DIRS = {"data", ".data", "raw24", "users", "aggregate", "venue_corpora", "_incoming", "_to_delete", "to delete",
             "__pycache__", ".git", "node_modules", ".venv", "venv", "ship", "renders", "_lead_sessions", "rooms",
             ".cc", "_transcripts", ".obsidian", "zips", "cache", "Cache"}
MAX = 2 * 1024 * 1024
STORES = {
    "raw24 (whole venues, 24 days)": r"raw24",
    "aggregate (placer records by venue)": r"placer accounts only|aggregate/|build_aggregate|by_venue",
    "users (one file per placer)": r"users/|_users\.csv|author_sweep|authors_index",
    "atlas": r"atlas[-_]2017|atlas\.json|placeAtlas",
    "tiles (pixel record)": r"tiles?2017|aperiodic|tile_placements|user_hash",
    "event window": r"rplace_window|OPEN\s*=\s*1490976000|FRZ",
    "arctic-shift collector": r"arctic-shift|arctic_shift|photon-reddit",
}


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def first_line(p):
    try:
        t = open(p, encoding="utf-8", errors="replace").read(4000)
    except Exception:
        return ""
    m = re.search(r'"""(.*?)(?:"""|\n\n)', t, re.S) or re.search(r"^#(?!!)\s*(.+)$", t, re.M)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:160] if m else ""


def keep(name, dirfiles):
    ext = os.path.splitext(name)[1]
    if ext in CODE:
        return True
    return ext in SIDE and any(os.path.splitext(f)[1] in CODE for f in dirfiles)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", action="append", required=True, help='"Name=path"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(argv)
    inv, big, hits = [], [], {k: [] for k in STORES}
    for spec in a.layer:
        name, root = spec.split("=", 1)
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            print("not found: %s" % root, file=sys.stderr)
            continue
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith((".", "_container", "_to_delete"))]
            for f in files:
                if not keep(f, files):
                    continue
                src = os.path.join(d, f)
                rel = os.path.relpath(src, root)
                n = os.path.getsize(src)
                if n > MAX:
                    big.append((name, rel, n))
                    continue
                dst = os.path.join(a.out, name, rel)
                h = sha1(src)
                if not a.dry and not (os.path.exists(dst) and sha1(dst) == h):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                inv.append((name, rel, n, h, first_line(src)))
                if os.path.splitext(f)[1] in CODE:
                    try:
                        t = open(src, encoding="utf-8", errors="replace").read()
                    except Exception:
                        t = ""
                    for k, rx in STORES.items():
                        if re.search(rx, t):
                            hits[k].append("%s/%s" % (name, rel))
    if a.dry:
        print("dry run: %d files, %d above 2 MB" % (len(inv), len(big)))
        return 0
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "INVENTORY.tsv"), "w", encoding="utf-8") as f:
        f.write("layer\tpath\tbytes\tsha1\tfirst_line\n")
        for r in sorted(inv):
            f.write("\t".join(str(x).replace("\t", " ") for x in r) + "\n")
        for r in big:
            f.write("%s\t%s\t%d\t-\tnot copied: above 2 MB\n" % r)
    with open(os.path.join(a.out, "CANDIDATES.md"), "w", encoding="utf-8") as f:
        f.write("# Which scripts touch which store\n\nFound by text search, not by reading: a script listed here names the store; "
                "it may read it rather than build it. The Manual's data page links the builder once a person has checked.\n\n")
        for k, v in hits.items():
            f.write("## %s\n\n%s\n\n" % (k, "\n".join("- `%s`" % x for x in sorted(v)) or "- none found"))
    print("copied or kept %d files into %s; %d above 2 MB listed; candidates in CANDIDATES.md" % (len(inv), a.out, len(big)))
    for k, v in hits.items():
        print("  %-40s %d scripts" % (k, len(v)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
