#!/usr/bin/env python3
"""C5c-02: apply the declaration amendments of c5c2_decl_spec.json, the field analyst's advice (QC5-001) accepted under
the rule logged before any amendment (diary, C5c-02-p2). For each declaration, in the spec's order: every `old` must
occur exactly once in its field (fourth/fourth.jsonl fields, or dimensions.jsonl construct fields as `construct.x`); the
replacements are applied, the file rewritten, one tier_history.jsonl line appended (move developing or dropping working
hypotheses, event construct_amended, the old line as `was`, the advice accepted and kept, each with its line), then one
diary line (mem.py log --kind move) and one snap (snap.py C5 move-developing-<n>). Stops at the first failure.

    python3 out/_analysis/c5c2_decl_amend.py            check every replacement, write nothing
    python3 out/_analysis/c5c2_decl_amend.py --write    apply, log and snap, numbering snaps from --first (96)
"""
import copy, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
SPEC = sys.argv[sys.argv.index("--spec") + 1] if "--spec" in sys.argv else "c5c2_decl_spec.json"
spec = json.load(open(os.path.join(OUT, "_analysis", SPEC), encoding="utf-8"))
FIRST = int(sys.argv[sys.argv.index("--first") + 1]) if "--first" in sys.argv else 96
WRITE = "--write" in sys.argv
WHY = ("the field analyst's second reading of the declarations (QC5-001; sources-from-J/RETURN-field-C5.jsonl), read as "
       "advice to improve (J, 11:02 Amsterdam), accepted or kept under the rule logged before any amendment")


def load(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def save(p, rows):
    open(os.path.join(OUT, p), "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def get(row, field):
    return row["construct"][field.split(".", 1)[1]] if field.startswith("construct.") else row[field]


def put(row, field, v):
    if field.startswith("construct."):
        row["construct"][field.split(".", 1)[1]] = v
    else:
        row[field] = v


def apply(row, reps):
    for r in reps:
        t = get(row, r["field"])
        n = t.count(r["old"])
        if n != 1:
            return "%s %s: old text found %d times: %r" % (row["id"], r["field"], n, r["old"][:70])
        t = t.replace(r["old"], r["new"]).replace("  ", " ").strip()
        put(row, r["field"], t)
    return None


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("failed: %s\n%s" % (" ".join(args), p.stderr[-800:]))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""


n = FIRST
for did, s in spec.items():
    reps = s.get("replace") or []
    if not reps:
        continue
    path = "dimensions.jsonl" if did.startswith("D") else os.path.join("fourth", "fourth.jsonl")
    rows = load(path)
    hit = [r for r in rows if r["id"] == did]
    if len(hit) != 1:
        sys.exit("%s not found once in %s" % (did, path))
    was = copy.deepcopy(hit[0])
    e = apply(hit[0], reps)
    if e:
        sys.exit(e)
    print("%s: %d replacements check" % (did, len(reps)))
    if not WRITE:
        continue
    save(path, rows)
    now = {f: get(hit[0], f) for f in sorted({r["field"] for r in reps})}
    line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "C5", "leg": LEG,
            "tier": "dimension" if did.startswith("D") else "fourth", "id": did,
            "move": "developing or dropping working hypotheses", "event": "construct_amended", "was": was,
            "now": [dict({"id": did}, **now)], "why": WHY, "accepted": s.get("accepted", []), "kept": s.get("kept", [])}
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    acc = "; ".join("%s: %s" % (a["sentence"], a["line"]) for a in s.get("accepted", []))
    kept = "; ".join("%s: %s" % (k["sentence"], k["line"]) for k in s.get("kept", [])) or "none"
    run([os.path.join("tools", "mem.py"), "log",
         "%s Move (developing or dropping working hypotheses), the field analyst's advice on the declaration (QC5-001): "
         "%d sentence(s) rewritten. Accepted: %s. Kept: %s. Findings touched: none changed." % (did, len(reps), acc, kept),
         "--kind", "move"])
    print("   " + run([os.path.join("tools", "snap.py"), "C5", "move-developing-%d" % n]))
    n += 1
print("done" if WRITE else "all replacements check; nothing written")
