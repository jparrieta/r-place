# handler-side: pull each earlier-coded room's coder output from its batch archive, as written
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from paths import P
import csv, os, re, tarfile, shutil
A = P("layer_a")
OUT = os.path.join(P("work"), "legacy")
rows = list(csv.DictReader(open(os.path.join(A, "40_analysis/coder_version/coder_version.csv"))))
WANT = r"(brief\.md|coder_corpus\.jsonl|out/(case\.md|codes\.jsonl|themes\.jsonl|threads\.jsonl|pointers\.jsonl|notes\.md|_run\.json))"
by_batch = {}
for r in rows: by_batch.setdefault(r["batch"], []).append(r["sub"])
got = {}
for batch, subs in sorted(by_batch.items()):
    subs = set(subs)
    src = os.path.join(A, "50_coding_runs", batch)
    if os.path.isdir(src):
        for s in subs:
            d = os.path.join(src, "runs", "run_" + s)
            if not os.path.isdir(d): d = os.path.join(src, "run_" + s)
            for root, _, fs in os.walk(d):
                for f in fs:
                    rel = os.path.relpath(os.path.join(root, f), d)
                    if re.fullmatch(WANT, rel):
                        dst = os.path.join(OUT, s, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copyfile(os.path.join(root, f), dst); got.setdefault(s, set()).add(rel)
        continue
    tp = src + ".tar.gz"
    with tarfile.open(tp) as t:
        for m in t:
            if not m.isfile(): continue
            mm = re.search(r"(?:^|/)run_([^/]+)/" + WANT + "$", m.name)
            if not mm or mm.group(1) not in subs: continue
            s, rel = mm.group(1), m.name[m.name.index("run_" + mm.group(1) + "/") + len("run_" + mm.group(1)) + 1:]
            dst = os.path.join(OUT, s, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            with t.extractfile(m) as fi, open(dst, "wb") as fo: shutil.copyfileobj(fi, fo)
            got.setdefault(s, set()).add(rel)
    print(batch, "done", flush=True)
import collections
miss = {s for s in (r["sub"] for r in rows) if s not in got}
print("rooms", len(got), "missing", sorted(miss))
print(collections.Counter(f for fs in got.values() for f in fs))
