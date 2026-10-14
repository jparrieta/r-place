#!/usr/bin/env python3
"""C2 section 2: write stage C2's fields into fourth/fourth.jsonl in place, one tier_history line per theme carrying the
old line as `was`. Fields: dimension (from dimensions.jsonl), changed and mistaken_for (c2_t4_fields_p1.json), in_model
(true when an element of model/elements.jsonl names the theme or one of its members in its tier), pass. Members are
unchanged. With --write: rewrites the file, appends the history lines, logs one move and snaps it.

    python3 out/_analysis/c2_t4_update.py [--pass 1] [--write]
"""
import argparse, datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--pass", dest="pass_", type=int, default=1)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
leg = open(os.path.join(ROOT, ".leg")).read().strip()
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
dims = jl("dimensions.jsonl")
dim_of = {}
for d in dims:
    for m in d["members"]:
        dim_of.setdefault(m, []).append(d["id"])
fields = json.load(open(os.path.join(OUT, "_analysis", "c2_t4_fields_p1.json"), encoding="utf-8"))["themes"]
els = jl(os.path.join("model", "elements.jsonl"))
used = set()
for e in els:
    for t in (e.get("tier") if isinstance(e.get("tier"), list) else [e.get("tier")]):
        used.add(t)
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
new, hist = [], []
for r in t4:
    f = fields[r["id"]]
    inm = r["id"] in used or bool(set(r["members"]) & used)
    n = dict(r)
    n.update({"dimension": dim_of.get(r["id"], []), "changed": f["changed"], "mistaken_for": f["mistaken_for"],
              "in_model": inm, "pass": a.pass_})
    new.append(n)
    hist.append({"t": t, "stage": "C2", "leg": leg, "tier": "fourth", "id": r["id"], "move": "relating or contrasting",
                 "event": "rescoped", "was": r, "now": [{"id": r["id"], "members": r["members"], "dimension": n["dimension"],
                                                         "in_model": inm}],
                 "prompted_by": "stage C2 section 2: the fields a fourth-order theme gains at C2, and the dimensions cut at pass 1",
                 "why": "members unchanged; the theme related to its dimension (%s), its borrowed or coined name given the sentence on what this material's version cannot do, and its place in the model recorded (in_model %s)" % (
                     ", ".join(n["dimension"]) or "none", inm)})
print("%d themes; in the model %d: %s; not %d: %s" % (len(new), sum(1 for n in new if n["in_model"]),
                                                     ", ".join(n["id"] for n in new if n["in_model"]),
                                                     sum(1 for n in new if not n["in_model"]),
                                                     ", ".join(n["id"] for n in new if not n["in_model"])))
if not a.write:
    sys.exit(0)
with open(os.path.join(OUT, "fourth", "fourth.jsonl"), "w", encoding="utf-8") as f:
    for n in new:
        f.write(json.dumps(n, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
    for h in hist:
        f.write(json.dumps(h, ensure_ascii=False) + "\n")
print("rewrote fourth/fourth.jsonl (%d lines); tier_history.jsonl now %d lines" % (len(new), len(jl("tier_history.jsonl"))))
msg = ("Fourth-order themes given their stage C2 fields in place (section 2), move relating or contrasting: each related to its "
       "dimension, given the sentence on what this material's version cannot do (changed) and what a reader may mistake it "
       "for, and marked in_model (%d of %d: %s); members unchanged; 28 tier_history lines carry the old lines as was." % (
           sum(1 for n in new if n["in_model"]), len(new), ", ".join(n["id"] for n in new if n["in_model"])))
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or "").strip())
if r.returncode:
    sys.exit("log failed")
k = 1 + max([int(m.group(1)) for m in (re.search(r"C2-move-[a-z]+-(\d+)\.sha256$", q)
                                        for q in glob.glob(os.path.join(OUT, "_snap", "C2-move-*.sha256"))) if m] or [0])
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C2", "move-relating-%d" % k], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
