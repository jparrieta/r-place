#!/usr/bin/env python3
"""D3a-56: write verdict rulings (G60, G60a) from a spec file, one row per split room:
    sub|verdict|residue ids (comma-separated, or -)|sentence|reason[|cannot_tell_under]
Refuses the whole file on any failure: the room is not a split room, or is ruled twice in the file or already ruled;
the verdict is not one of the four; a residue id is not a theme or concept a reader named; the line fails the
reader-line rules (dreturn.verdict_problems, with the room's themes and concepts). A ruling line carries sub,
ruled_by analyst, verdict, the themes and concepts it rests on (the union of both readers' lists and the residue),
residue, cannot_tell_under, sentence, reason, changed_from (each reader's verdict), model_version (the served model
the readers held), stage, leg and t. The readers' line stays. With --write it appends to verdicts-D.jsonl and logs
one diary note.

    python3 out/_analysis/d3_verdict_rulings.py --spec out/_analysis/d3_rulings/verdict-spec-000.txt [--write]
"""
import argparse, collections, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import dreturn  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


split = {r["sub"] for r in json.load(open(os.path.join(OUT, "_analysis", "d2_verdict_rooms.json")))["split"]}
rows_v = jl(os.path.join(OUT, "verdicts-D.jsonl"))
readers = {r["sub"]: r["readers"] for r in rows_v if not r.get("ruled_by")}
ruled = {r["sub"] for r in rows_v if r.get("ruled_by") == "analyst"}
spec = []
for line in open(a.spec, encoding="utf-8"):
    line = line.rstrip("\n")
    if line:
        p = line.split("|")
        spec.append(p)
want = {p[0] for p in spec}
rt, rc = collections.defaultdict(set), collections.defaultdict(set)
for r in jl(os.path.join(ROOT, "package", "store", "themes.jsonl")):
    if r["sub"] in want:
        rt[r["sub"]].add(r["theme_id"])
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in want:
        rc[r["sub"]].add(r["code_id"])
leg = open(os.path.join(ROOT, ".leg")).read().strip()
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
errs, out, seen = [], [], collections.Counter(p[0] for p in spec)
for p in spec:
    if len(p) not in (5, 6):
        errs.append("%s: %d fields, not 5 or 6" % (p[0], len(p)))
        continue
    sub, v, res, sent, reason = p[:5]
    ctu = p[5] if len(p) == 6 else None
    if sub not in split:
        errs.append("%s: not a split room" % sub)
        continue
    if seen[sub] > 1 or sub in ruled:
        errs.append("%s: ruled twice" % sub)
    rd = readers[sub]
    named = set()
    for e in rd:
        for k in ("residue", "concepts", "themes"):
            named |= {str(x).split(":")[-1] for x in (e.get(k) or [])}
    residue = [] if res.strip() in ("-", "") else [x.strip() for x in res.split(",")]
    for x in residue:
        if x not in named:
            errs.append("%s: residue %s was named by no reader" % (sub, x))
    themes = sorted({str(x).split(":")[-1] for e in rd for x in (e.get("themes") or [])})
    concepts = sorted({str(x).split(":")[-1] for e in rd for x in (e.get("concepts") or [])}
                      | {x for x in residue if x.startswith("c")})
    mv = {e.get("model_version") for e in rd}
    r = {"sub": sub, "ruled_by": "analyst", "verdict": v, "themes": themes, "concepts": concepts, "residue": residue,
         "cannot_tell_under": ctu, "sentence": sent, "reason": reason,
         "changed_from": {e.get("reader"): e.get("verdict") for e in rd},
         "model_version": sorted(mv)[0] if len(mv) == 1 else sorted(mv), "stage": "D3", "leg": leg, "t": t}
    for prob in dreturn.verdict_problems(r, sub, rt[sub], rc[sub]):
        errs.append("%s: %s" % (sub, prob))
    out.append(r)
if errs or not out:
    print("\n".join(errs or ["the spec holds no row"]))
    sys.exit("refused: nothing written")
counts = collections.Counter(r["verdict"] for r in out)
print("%s: %d rulings checked; %s; leg %s" % (os.path.basename(a.spec), len(out), dict(counts), leg))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
with open(os.path.join(OUT, "verdicts-D.jsonl"), "a", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
note = "verdicts ruled from %s (G60, G60a): %s. Rooms: %s" % (
    os.path.relpath(a.spec, OUT), ", ".join("%s %d" % kv for kv in sorted(counts.items())),
    "; ".join("%s %s (changed from %s)" % (r["sub"], r["verdict"], "/".join(r["changed_from"].values())) for r in out))
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", note, "--kind", "note"], cwd=ROOT,
               check=True, capture_output=True)
n = sum(1 for _ in open(os.path.join(OUT, "verdicts-D.jsonl"), encoding="utf-8"))
print("appended %d rulings; verdicts-D.jsonl now %d lines; one diary note" % (len(out), n))
