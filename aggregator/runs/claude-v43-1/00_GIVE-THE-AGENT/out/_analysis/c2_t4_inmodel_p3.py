#!/usr/bin/env python3
"""C2, pass 3: set in_model on fourth-order themes from the standing elements of model/elements.jsonl (an element ties
to a fourth-order theme directly or through a third-order member; candidates and withdrawn elements do not count).
Rewrites fourth/fourth.jsonl in place for every line whose in_model changes, with a tier_history.jsonl line each carrying
the old line as was (move relating or contrasting), one diary line and one snap. The pass 2 version is
c2_t4_inmodel_p2.py.

    python3 out/_analysis/c2_t4_inmodel_p3.py [--write]
"""
import datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
write = "--write" in sys.argv
PASS = 3


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


FP = os.path.join(OUT, "fourth", "fourth.jsonl")
t4 = jl(FP)
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
used, by = set(), {}
for e in jl(os.path.join(OUT, "model", "elements.jsonl")):
    if e.get("status") in ("candidate", "withdrawn"):
        continue
    for t in e["tier"]:
        used.add(owner.get(t, t))
        by.setdefault(owner.get(t, t), set()).add(e["id"])
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
leg = open(os.path.join(ROOT, ".leg")).read().strip()
th, changed = [], []
for r in t4:
    now = r["id"] in used
    if bool(r.get("in_model")) != now:
        w = json.loads(json.dumps(r))
        r["in_model"], r["pass"] = now, PASS
        changed.append(r["id"])
        th.append({"t": t, "stage": "C2", "leg": leg, "tier": "fourth", "id": r["id"], "move": "relating or contrasting",
                   "event": "in_model changed", "was": w,
                   "why": ("a standing element now ties to it (pass %d: %s)" % (PASS, ", ".join(sorted(by[r["id"]]))))
                   if now else "no standing element ties to it (pass %d)" % PASS})
n_in = sum(1 for r in t4 if r.get("in_model"))
print("in_model changes: %s; in the model now: %d of %d" % (", ".join(changed) or "none", n_in, len(t4)))
if not write or not changed:
    sys.exit(0)
with open(FP, "w", encoding="utf-8") as f:
    for r in t4:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
    for h in th:
        f.write(json.dumps(h, ensure_ascii=False) + "\n")
msg = ("Fourth-order themes' in_model set from the standing elements (pass %d), move relating or contrasting: %s; %d of %d "
       "in the model; tier_history lines carry the old lines as was." % (
           PASS, "; ".join("%s %s (%s)" % (h["id"], "now in the model" if h["why"].startswith("a standing") else "out of the model",
                                            h["why"]) for h in th), n_in, len(t4)))
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "log", msg, "--kind", "move"], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or "").strip())
n = 1 + max([int(m.group(1)) for m in (re.search(r"C2-move-[a-z]+-(\d+)\.sha256$", p)
                                        for p in glob.glob(os.path.join(OUT, "_snap", "C2-move-*.sha256"))) if m] or [0])
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "snap.py"), "C2", "move-relating-%d" % n], cwd=ROOT,
                   capture_output=True, text=True)
print((r.stdout or r.stderr).strip())
