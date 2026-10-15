#!/usr/bin/env python3
"""C5c-08, problem 1 (the unit): apply the declaration amendments of c5c8_decl_spec.json, each restoring the room or a
group of rooms as the actor under the rule logged first (diary, C5c-08, abductive). As c5c2_decl_amend.py, but each
declaration carries its own `why`: every `old` must occur exactly once in its field (fourth/fourth.jsonl fields, or
dimensions.jsonl construct fields as `construct.x`); the replacements are applied, the file rewritten, one
tier_history.jsonl line appended (move developing or dropping working hypotheses, event construct_amended, the old line
as `was`), then one diary line (mem.py log --kind move) and one snap (snap.py C5 move-developing-<n>, from --first).
Stops at the first failure.

    python3 out/_analysis/c5c8_decl_amend.py                  check every replacement, write nothing
    python3 out/_analysis/c5c8_decl_amend.py --write --first N
"""
import copy, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
spec = json.load(open(os.path.join(OUT, "_analysis", "c5c8_decl_spec.json"), encoding="utf-8"))
WRITE = "--write" in sys.argv
if WRITE and "--first" not in sys.argv:
    sys.exit("--write needs --first N, the first snap number")
n = int(sys.argv[sys.argv.index("--first") + 1]) if "--first" in sys.argv else 0


def load(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def get(row, field):
    return row["construct"][field.split(".", 1)[1]] if field.startswith("construct.") else row[field]


def put(row, field, v):
    if field.startswith("construct."):
        row["construct"][field.split(".", 1)[1]] = v
    else:
        row[field] = v


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("failed: %s\n%s" % (" ".join(args), p.stderr[-800:]))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""


for did, s in spec.items():
    path = "dimensions.jsonl" if did.startswith("D") else os.path.join("fourth", "fourth.jsonl")
    rows = load(path)
    hit = [r for r in rows if r["id"] == did]
    if len(hit) != 1:
        sys.exit("%s not found once in %s" % (did, path))
    was = copy.deepcopy(hit[0])
    for r in s["replace"]:
        t = get(hit[0], r["field"])
        c = t.count(r["old"])
        if c != 1:
            sys.exit("%s %s: old text found %d times: %r" % (did, r["field"], c, r["old"][:70]))
        put(hit[0], r["field"], t.replace(r["old"], r["new"]))
    print("%s: %d replacements check" % (did, len(s["replace"])))
    if not WRITE:
        continue
    open(os.path.join(OUT, path), "w", encoding="utf-8").write(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    now = {f: get(hit[0], f) for f in sorted({r["field"] for r in s["replace"]})}
    line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "C5", "leg": LEG,
            "tier": "dimension" if did.startswith("D") else "fourth", "id": did,
            "move": "developing or dropping working hypotheses", "event": "construct_amended", "was": was,
            "now": [dict({"id": did}, **now)], "why": s["why"]}
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    run([os.path.join("tools", "mem.py"), "log",
         "%s Move (developing or dropping working hypotheses), problem 1, the unit: %d sentence(s) take the room or a "
         "group of rooms as the actor. %s Findings touched: none changed." % (did, len(s["replace"]), s["why"]),
         "--kind", "move"])
    print("   " + run([os.path.join("tools", "snap.py"), "C5", "move-developing-%d" % n]))
    n += 1
print("done" if WRITE else "all replacements check; nothing written")
