#!/usr/bin/env python3
"""C5a-01: the sample for the abductive read of Stigmergy against Grasse (1959) and Heylighen (2016), under the rules
written first in notes-C5.md. For T3-038 and T3-041, 24 records each, drawn with seed 20261015, at most two per room;
for T3-060, every record up to 24. Writes out/_analysis/c5_stigmergy_sample.json (the records, whole) once, and prints
them for reading. Refuses to overwrite the sample.

    python3 out/_analysis/c5_stigmergy_sample.py [--print]
"""
import collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(ROOT, "out", "_analysis", "c5_stigmergy_sample.json")


def records(t):
    out, off = [], 0
    while True:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--third", t, "--json",
                            "--offset", str(off), "--limit", "1000"], cwd=ROOT, capture_output=True, text=True)
        got = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
        out += got
        if len(got) < 1000:
            return out
        off += 1000


if "--print" not in sys.argv:
    if os.path.exists(DEST):
        sys.exit("the sample exists; run with --print to read it")
    rng = random.Random(20261015)
    sample = {}
    for t in ("T3-038", "T3-041", "T3-060"):
        recs = records(t)
        rng.shuffle(recs)
        per, pick = collections.Counter(), []
        for r in recs:
            if per[r["sub"]] < (2 if t != "T3-060" else 99):
                per[r["sub"]] += 1
                pick.append({k: r[k] for k in ("sub", "code_id", "hour", "first_order", "text")})
            if len(pick) == 24:
                break
        sample[t] = {"n_records": len(recs), "drawn": pick}
    json.dump(sample, open(DEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sample = json.load(open(DEST, encoding="utf-8"))
for t, s in sample.items():
    print("== %s: %d records in the store, %d drawn" % (t, s["n_records"], len(s["drawn"])))
    for i, r in enumerate(s["drawn"], 1):
        print("%s.%02d %s/%s h%.2f [%s] %s" % (t, i, r["sub"], r["code_id"], r["hour"], r["first_order"],
                                             r["text"].replace("\n", " ")))
