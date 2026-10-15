#!/usr/bin/env python3
"""C5d: write out/data_structure-C5.md, the six-column table over all five tiers (stage C5 section 9), by the rule logged
before it was built (diary, C5d): one row per third-order theme a fourth-order theme gathers, ordered by dimension,
fourth-order theme and member; each row's quote is a concept cited under its third-order theme (support_by_theme in
assignments_final.jsonl), the k-th member of a fourth-order theme drawn from the k-th room-size quartile (items_in_window,
k mod 4), candidates shuffled by random.Random(20261015), the first of 5 to 40 words with no |, double quote or line
break, from a room not yet used in that fourth-order theme, else the next quartile; failing all, the coder's
second-order theme label, said so. The residue (third-order themes no fourth-order theme gathers) follows the table with
its account from fourth/fourth.md's foot and one quote by the same rule. Quotes enter through cite.py.

    python3 out/_analysis/c5d_data_structure.py            print counts only
    python3 out/_analysis/c5d_data_structure.py --write    write out/data_structure-C5.md and c5d_data_structure.json
"""
import collections, json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
SEED = 20261015


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


scheme = {r["id"]: r for r in jl(os.path.join(OUT, "scheme_v2.jsonl"))}
fourth = {r["id"]: r for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dims = jl(os.path.join(OUT, "dimensions.jsonl"))
rooms = {r["sub"]: r for r in jl(os.path.join(STORE, "rooms.jsonl"))}
sizes = sorted(r.get("items_in_window") or 0 for r in rooms.values())
qb = [sizes[len(sizes) * i // 4] for i in (1, 2, 3)]


def quartile(sub):
    n = rooms.get(sub, {}).get("items_in_window") or 0
    return sum(1 for b in qb if n >= b)  # 0..3


cited = collections.defaultdict(list)   # T3 -> [(sub, code)]
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    for t3, codes in (r.get("support_by_theme") or {}).items():
        for c in codes:
            cited[t3].append((r["sub"], c))
need = {k for v in cited.values() for k in v}
codes = {}
for l in open(os.path.join(STORE, "codes.jsonl"), encoding="utf-8"):
    o = json.loads(l)
    k = (o["sub"], o["code_id"])
    if k in need:
        codes[k] = o
labels = {(r["sub"], r["theme_id"]): r["second_order"] for r in jl(os.path.join(STORE, "themes.jsonl"))}


def ok(k):
    o = codes.get(k)
    if not o:
        return False
    t = o.get("text") or ""
    return 5 <= len(t.split()) <= 40 and not re.search(r"[|\"\n\r]", t)


def choose(t3, k, used):
    cands = sorted(set(cited.get(t3, [])))
    random.Random("%d-%s" % (SEED, t3)).shuffle(cands)
    for step in range(4):
        q = (k + step) % 4
        pool = [c for c in cands if quartile(c[0]) == q and ok(c)]
        fresh = [c for c in pool if c[0] not in used]
        if fresh or pool:
            return (fresh or pool)[0], q
    return (cands[0], None) if cands else (None, None)


def cite(k):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--room", k[0], "--code", k[1], "--json"],
                       capture_output=True, text=True, cwd=ROOT)
    return json.loads(p.stdout)["quotes"][0]


def cell(s):
    return " ".join(str(s or "").replace("|", "/").split())


rows, log = [], []
for d in dims:
    for t4 in d["members"]:
        used = set()
        for k, t3 in enumerate(fourth[t4]["members"]):
            pick, q = choose(t3, k, used)
            if pick is None:
                rows.append(["(no concept is cited under this theme)", "", "", "%s %s" % (t3, scheme[t3]["name"]),
                             "%s %s" % (t4, fourth[t4]["name"]), "%s %s" % (d["id"], d["label"])])
                log.append({"t3": t3, "pick": None})
                continue
            used.add(pick[0])
            qt = cite(pick)
            lab = labels.get((pick[0], qt.get("theme_id")), qt.get("second_order"))
            if q is None:
                first = "the coder's second-order theme label, since no cited quote carries a row: %s (r/%s, %s)" % (
                    cell(lab), pick[0], pick[1])
            else:
                first = '"%s" (r/%s, %s, h%.2f, %s)' % (qt["text"], qt["sub"], cell(qt.get("author")), qt["hour"],
                                                         qt["code_id"])
            rows.append([first, cell(qt.get("first_order")), cell(lab), "%s %s" % (t3, scheme[t3]["name"]),
                         "%s %s" % (t4, fourth[t4]["name"]), "%s %s" % (d["id"], d["label"])])
            log.append({"t3": t3, "t4": t4, "dim": d["id"], "sub": pick[0], "code": pick[1], "quartile": q})
# residue
foot = open(os.path.join(OUT, "fourth", "fourth.md"), encoding="utf-8").read()
members = {m for r in fourth.values() for m in r["members"]}
residue = []
for t3 in sorted(scheme):
    if t3 in members:
        continue
    m = re.search(r"^- %s (.+)$" % re.escape(t3), foot, re.M)
    pick, q = choose(t3, 0, set())
    qt = cite(pick) if pick else None
    residue.append((t3, m.group(1) if m else scheme[t3]["name"], qt))
qn = collections.Counter(x.get("quartile") for x in log if x.get("pick", True) is not None)
print("rows %d; by quartile %s; label rows %d; residue %s" % (len(rows), dict(qn), sum(1 for x in log if x.get("quartile") is None and x.get("sub")), [r[0] for r in residue]))
if "--write" in sys.argv:
    L = ["# The data structure, final (C5d)", "",
         "Target length: one row per third-order theme; long, by the rule. The table runs over all five tiers as they "
         "finally stand after pass 10: the participant's words, the coder's first-order concept, the coder's "
         "second-order theme, the third-order theme it was placed on, the fourth-order theme that gathers it, and the "
         "dimension. There is one row for each of the %d third-order themes that a fourth-order theme gathers, in the "
         "order of the dimensions and their themes. Each quote is a concept cited under its third-order theme, entered "
         "through `cite.py`, with its community, author handle, hour since the canvas opened and concept id. The rows "
         "show the range, not the centre: within each fourth-order theme, members take rooms from the four room-size "
         "quartiles in turn. The rule is written in `notes-C5.md`. The generated view over every concept is "
         "`_views/data-structure.md`; `structure.md` carries the rest." % len(rows), "",
         "| representative quote | first-order concept | second-order theme | third-order theme | fourth-order theme | aggregate dimension |",
         "|---|---|---|---|---|---|"]
    L += ["| %s |" % " | ".join(r) for r in rows]
    L += ["", "## The residue", "",
          "Two third-order themes no fourth-order theme picked up. Each comes with its account from the foot of "
          "`fourth/fourth.md` and one quote by the same rule. Every fourth-order theme sits in a dimension, so no "
          "fourth-order theme is residue.", ""]
    for t3, acc, qt in residue:
        L.append("- **%s %s**" % (t3, acc))
        if qt:
            L.append('  - "%s" (r/%s, %s, h%.2f, %s)' % (qt["text"].replace("\n", " "), qt["sub"], cell(qt.get("author")),
                                                     qt["hour"], qt["code_id"]))
    L += ["", "## Dimensions and fourth-order themes, for the record", ""]
    for d in dims:
        L.append("- **%s %s:** %s." % (d["id"], d["label"], "; ".join("%s %s" % (t, fourth[t]["name"]) for t in d["members"])))
    open(os.path.join(OUT, "data_structure-C5.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"seed": SEED, "quartile_bounds": qb, "rows": log}, open(os.path.join(OUT, "_analysis", "c5d_data_structure.json"), "w"), indent=1)
    print("wrote out/data_structure-C5.md")
