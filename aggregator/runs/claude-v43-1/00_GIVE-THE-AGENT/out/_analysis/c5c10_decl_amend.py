#!/usr/bin/env python3
"""C5c-10, problem 4: apply the declaration amendments of c5c10_decl_spec.json (Stigmergy renamed for what its records
show; D02's 'aligned' with its count). As c5c8_decl_amend.py, with two kinds of replacement: a part ('old' must occur
exactly once in the field) or a whole field ('whole': true, and the field must begin with 'starts'). Fields are
fourth/fourth.jsonl fields or dimensions.jsonl fields, construct fields as 'construct.x'. For each declaration: the
file rewritten, one tier_history.jsonl line (the declaration's move, event construct_amended, the old line as 'was'),
one diary line (mem.py log --kind move) and one snap (snap.py C5 move-<move>-<n>, n from --first). Stops at the first
failure.

    python3 out/_analysis/c5c10_decl_amend.py                  check, write nothing
    python3 out/_analysis/c5c10_decl_amend.py --write --first N
"""
import copy, datetime, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
spec = json.load(open(os.path.join(OUT, "_analysis", "c5c10_decl_spec.json"), encoding="utf-8"))
WRITE = "--write" in sys.argv
if WRITE and "--first" not in sys.argv:
    sys.exit("--write needs --first N")
n = int(sys.argv[sys.argv.index("--first") + 1]) if "--first" in sys.argv else 0
SHORT = {"developing or dropping working hypotheses": "developing", "relating or contrasting": "relating",
         "merging": "merging", "splitting": "splitting", "dropping": "dropping"}


def get(row, f):
    return row["construct"][f.split(".", 1)[1]] if f.startswith("construct.") else row[f]


def put(row, f, v):
    if f.startswith("construct."):
        row["construct"][f.split(".", 1)[1]] = v
    else:
        row[f] = v


def run(args):
    p = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("failed: %s\n%s" % (" ".join(args), p.stderr[-800:]))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""


for did, s in spec.items():
    path = "dimensions.jsonl" if did.startswith("D") else os.path.join("fourth", "fourth.jsonl")
    rows = [json.loads(l) for l in open(os.path.join(OUT, path), encoding="utf-8") if l.strip()]
    hit = [r for r in rows if r["id"] == did]
    if len(hit) != 1:
        sys.exit("%s not found once in %s" % (did, path))
    was = copy.deepcopy(hit[0])
    for r in s["replace"]:
        t = get(hit[0], r["field"])
        if r.get("whole"):
            if not t.startswith(r["starts"]):
                sys.exit("%s %s does not begin with %r" % (did, r["field"], r["starts"]))
            put(hit[0], r["field"], r["new"])
        else:
            c = t.count(r["old"])
            if c != 1:
                sys.exit("%s %s: old text found %d times: %r" % (did, r["field"], c, r["old"][:70]))
            put(hit[0], r["field"], t.replace(r["old"], r["new"]))
    print("%s: %d replacements check" % (did, len(s["replace"])))
    if not WRITE:
        continue
    open(os.path.join(OUT, path), "w", encoding="utf-8").write(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    now = {f: get(hit[0], f) for f in sorted({r["field"] for r in s["replace"]})}
    line = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "C5", "leg": LEG,
            "tier": "dimension" if did.startswith("D") else "fourth", "id": did, "move": s["move"],
            "event": "construct_amended", "was": was, "now": [dict({"id": did}, **now)], "why": s["why"]}
    with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    run([os.path.join("tools", "mem.py"), "log",
         "%s Move (%s), problem 4, Stigmergy and 'aligned': %d field(s) amended. %s Findings touched: %s." % (
             did, s["move"], len(s["replace"]), s["why"], s.get("findings", "none changed")), "--kind", "move"])
    print("   " + run([os.path.join("tools", "snap.py"), "C5", "move-%s-%d" % (SHORT[s["move"]], n)]))
    n += 1
print("done" if WRITE else "all replacements check; nothing written")
