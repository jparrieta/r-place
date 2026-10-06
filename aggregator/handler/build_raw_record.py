#!/usr/bin/env python3
"""build_raw_record.py: the raw record the quote check at E1 reads, kept inside the run (J, 2026-09-30).

    python3 build_raw_record.py [--only sub1,sub2] [--force]

Handler side. For every room of the frame (package/store/rooms.jsonl), copies the record its coder
read, `coder_corpus.jsonl`, from where the room was coded (aggregator/input/coders/CODERS.tsv, `coded_in`):
a yard room from P("yard_rooms")/<sub>/run/ (unpacked) or run.tar.zst; an earlier room from its
batch in P("layer_a")/50_coding_runs (40_analysis/coder_version/coder_version.csv names the batch).
The sources are read only. Writes aggregator/input/raw/<sub>/coder_corpus.jsonl.gz and
aggregator/input/raw/MANIFEST.tsv (sub, coded_in, source, lines, bytes, sha256 of the uncompressed file);
no full path is written. A room already built is left alone unless --force. check_quotes.py reads
this copy first, so E1's check no longer needs the yard or Layer A on the machine.
"""
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from paths import P
import csv, gzip, hashlib, json, os, subprocess, tarfile
R = P("run"); Y = P("yard_rooms"); A = P("layer_a")
IN = P("input")
OUT = os.path.join(IN, "raw")
args = sys_args = _sys.argv[1:]
only = set(args[args.index("--only") + 1].split(",")) if "--only" in args else None
force = "--force" in args
subs = [json.loads(l)["sub"] for l in open(os.path.join(R, "00_GIVE-THE-AGENT/package/store/rooms.jsonl")) if l.strip()]
coded = {r["sub"]: r for r in csv.DictReader(open(os.path.join(IN, "coders/CODERS.tsv")), delimiter="\t")}
batch = {r["sub"]: r["batch"] for r in csv.DictReader(open(os.path.join(A, "40_analysis/coder_version/coder_version.csv")))}
MEMBER = "run/coder_corpus.jsonl"


def from_yard(sub):
    d = os.path.join(Y, sub)
    p = os.path.join(d, MEMBER)
    if os.path.exists(p):
        return open(p, "rb").read(), "yard: %s/%s" % (sub, MEMBER)
    z = os.path.join(d, "run.tar.zst")
    if os.path.exists(z):
        for cmd in (["tar", "--zstd", "-xOf", z, MEMBER], ["sh", "-c", 'zstd -dc "$0" | tar -xOf - "$1"', z, MEMBER]):
            r = subprocess.run(cmd, capture_output=True)
            if r.returncode == 0 and r.stdout:
                return r.stdout, "yard: %s/run.tar.zst:%s" % (sub, MEMBER)
    return None, "yard: no %s" % MEMBER


_tars = {}
def from_batch(sub):
    b = batch.get(sub)
    if not b:
        return None, "earlier: no batch in coder_version.csv"
    src = os.path.join(A, "50_coding_runs", b)
    for d in (os.path.join(src, "runs", "run_" + sub), os.path.join(src, "run_" + sub)):
        p = os.path.join(d, "coder_corpus.jsonl")
        if os.path.exists(p):
            return open(p, "rb").read(), "Layer A: 50_coding_runs/%s/%s" % (b, os.path.relpath(p, src))
    tp = src + ".tar.gz"
    if os.path.exists(tp):
        if tp not in _tars:     # one pass per batch archive: every wanted room's corpus at once
            want = {s for s, bb in batch.items() if bb == b}
            got = {}
            with tarfile.open(tp) as t:
                for m in t:
                    if m.isfile() and m.name.endswith("/coder_corpus.jsonl") and "/._" not in m.name:
                        parts = m.name.split("/")
                        run = [x for x in parts if x.startswith("run_")]
                        if run and run[-1][4:] in want and parts[-2] == run[-1]:
                            got[run[-1][4:]] = (t.extractfile(m).read(), m.name)
            _tars[tp] = got
        hit = _tars[tp].get(sub)
        if hit:
            return hit[0], "Layer A: 50_coding_runs/%s.tar.gz:%s" % (b, hit[1])
    return None, "earlier: no coder_corpus.jsonl in %s" % b


os.makedirs(OUT, exist_ok=True)
man_p = os.path.join(OUT, "MANIFEST.tsv")
man = {}
if os.path.exists(man_p):
    for r in csv.DictReader(open(man_p), delimiter="\t"):
        man[r["sub"]] = r
todo = [s for s in subs if (only is None or s in only)]
todo.sort(key=lambda s: (coded.get(s, {}).get("coded_in") != "earlier", batch.get(s, ""), s))
missing = []
for i, s in enumerate(todo, 1):
    dst = os.path.join(OUT, s, "coder_corpus.jsonl.gz")
    if os.path.exists(dst) and s in man and not force:
        continue
    where = coded.get(s, {}).get("coded_in", "")
    data, src = from_yard(s) if where == "yard" else from_batch(s)
    if data is None:
        missing.append((s, src)); man[s] = {"sub": s, "coded_in": where, "source": src, "lines": "", "bytes": "", "sha256": ""}
        print("MISSING", s, src, flush=True); continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".part"
    with gzip.open(tmp, "wb", compresslevel=6) as f:
        f.write(data)
    os.replace(tmp, dst)
    man[s] = {"sub": s, "coded_in": where, "source": src, "lines": str(data.count(b"\n")), "bytes": str(len(data)),
              "sha256": hashlib.sha256(data).hexdigest()}
    if i % 25 == 0:
        print(i, "of", len(todo), flush=True)
    with open(man_p + ".part", "w") as f:
        w = csv.DictWriter(f, ["sub", "coded_in", "source", "lines", "bytes", "sha256"], delimiter="\t")
        w.writeheader(); [w.writerow(man[k]) for k in sorted(man)]
    os.replace(man_p + ".part", man_p)
print("built", sum(1 for r in man.values() if r.get("sha256")), "of", len(subs), "; missing", len(missing), missing[:10])
