import os, sys, tarfile, hashlib, json, io, time
# snap.py OUT.tar.gz SRC ARCNAME --prune a,b,c --only x,y --max MB
out, src, arc = sys.argv[1:4]
opts = dict(zip(sys.argv[4::2], sys.argv[5::2]))
prune = [p for p in opts.get("--prune", "").split(",") if p]
only = [p for p in opts.get("--only", "").split(",") if p]
mx = float(opts.get("--max", "20")) * 1e6
NAMES = {"__pycache__", ".git", ".cc", "_to_delete", ".DS_Store", "snapshots", "interview-workspaces", "node_modules"}
rows = []; skipped = []
with tarfile.open(out, "w:gz") as t:
    for d, dirs, files in os.walk(src):
        rel = os.path.relpath(d, src)
        keep = []
        for x in sorted(dirs):
            r = os.path.normpath(os.path.join(rel, x))
            if x in NAMES or any(r == p or r.startswith(p + "/") for p in prune): continue
            if only and rel == "." and x not in only: continue
            keep.append(x)
        dirs[:] = keep
        for f in sorted(files):
            if f in NAMES or f.endswith(".pyc"): continue
            r = os.path.normpath(os.path.join(rel, f))
            if only and rel == "." and f not in only and not f.endswith(".md"): continue
            if any(r == p for p in prune): continue
            p = os.path.join(d, f)
            if os.path.islink(p): continue
            s = os.path.getsize(p)
            if s > mx: skipped.append((r, s)); continue
            t.add(p, arcname=os.path.join(arc, r), recursive=False)
            rows.append((r, s, hashlib.sha256(open(p, "rb").read()).hexdigest()))
    m = "path\tbytes\tsha256\n" + "".join("%s\t%d\t%s\n" % x for x in rows)
    ti = tarfile.TarInfo(os.path.join(arc, "_MANIFEST.tsv")); b = m.encode(); ti.size = len(b); ti.mtime = time.time()
    t.addfile(ti, io.BytesIO(b))
print(json.dumps({"files": len(rows), "bytes": sum(r[1] for r in rows), "skipped_over_max": skipped[:20], "n_skipped": len(skipped)}))
