"""B1e: exemplar candidates for one third-order theme.

Sources, printed in this order:
1. the concepts the rule 0 lines name for the theme as an added kind (multiplacement_log.jsonl, lines whose
   `additional` is the theme): up to --r0 lines, chosen with seed "b1e-r0:<T3>", up to three codes each,
   each quoted with `cite.py --room <sub> --code <id>`;
2. the theme's concepts from `mem.py codes --third <T3>` (every concept under its members), shuffled with
   seed "<seed>:<T3>"; with --pat, only concepts whose label or words match the pattern (case-blind), a
   filter that grounds the gate's wording and does not choose rooms (rule 2); --n lines shown, from --skip.

Every exemplar chosen from (2) is then quoted through cite.py (b1e_cite.py) before it is written.

usage: python3 out/_analysis/b1e_cands.py T3-001 [--n 30] [--skip 0] [--seed 20261011] [--r0 3] [--pat "re"]
"""
import json
import random
import re
import subprocess
import sys

argv = sys.argv[1:]


def arg(key, default):
    if key in argv:
        i = argv.index(key)
        v = argv[i + 1]
        del argv[i:i + 2]
        return v
    return default


n = int(arg("--n", "30"))
skip = int(arg("--skip", "0"))
seed = arg("--seed", "20261011")
r0 = int(arg("--r0", "3"))
pat = arg("--pat", None)
t = argv[0]


def run(*a):
    return subprocess.run(["python3", *a, "--stage", "B1"], capture_output=True, text=True).stdout


if r0 > 0:
    rows = [json.loads(x) for x in open("out/multiplacement_log.jsonl", encoding="utf-8") if x.strip()]
    adds = [r for r in rows if not r.get("item_is_a_bag") and r.get("additional") == t]
    rng = random.Random("b1e-r0:" + t)
    pick = adds if len(adds) <= r0 else rng.sample(adds, r0)
    print("== %s: %d rule 0 lines add it; %d shown" % (t, len(adds), len(pick)))
    for r in pick:
        for c in (r.get("codes") or [])[:3]:
            for q in run("tools/cite.py", "--room", r["sub"], "--code", c).splitlines():
                if q.startswith('"'):
                    print("R0 " + q[:330])
lines = [x for x in run("tools/mem.py", "codes", "--third", t, "--limit", "200000").splitlines()
         if re.match(r"^c\d{4}\s", x)]
if pat:
    rx = re.compile(pat, re.I)
    lines = [x for x in lines if rx.search(x.split("|", 1)[-1])]
random.Random("%s:%s" % (seed, t)).shuffle(lines)
print("-- concepts (seed %s%s): %d; shown %d to %d" % (seed, ", pattern " + pat if pat else "", len(lines), skip + 1,
                                                       min(len(lines), skip + n)))
for x in lines[skip:skip + n]:
    x = re.sub(r"\s+h\s+[+-][\d.]+\s+\S+\s+@\S+\s+", " ", x)
    print(x[:300])
