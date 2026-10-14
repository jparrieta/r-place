#!/usr/bin/env python3
"""C2 section 2: write structure.md (pass 1) or structure-pN.md from the ledgers, the authored notes and cite.py.

Per third-order theme: what it is and is not, the borderline C1 repaired (its gate amendments), nearest neighbours and
the separating test, what varies, the gate quoted from scheme_v2.jsonl, rule 5's three counts under the declared
opportunity gate, three exemplars through cite.py, and the coder conflicts placed here read another way. Per
fourth-order theme and dimension: id, label, declaration and gloss, what holds it together, the question, what falls
outside with a near case, the member least sure of, and (for a fourth-order theme) its material, three to five quotes
through cite.py --tier 4th as JSON lines. Then what no fourth-order theme picked up, the pairs, and the onset contrast.
Every count is computed from assignments_final.jsonl; room facts come through mem.py facts. Refuses to overwrite.

    python3 out/_analysis/c2_structure_md.py [--out structure.md] [--pass 1]
"""
import argparse, collections, json, os, random, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("--out", default="structure.md")
ap.add_argument("--pass", dest="pass_", type=int, default=1)
ap.add_argument("--notes", default="c2_structure_notes_p1.json", help="authored notes in out/_analysis (pass 2: c2_structure_notes_p2.json)")
ap.add_argument("--fields", default="c2_t4_fields_p1.json", help="fourth-order fields in out/_analysis")
ap.add_argument("--leg", default="C2a-01")
a = ap.parse_args()
dest = os.path.join(OUT, a.out)
if os.path.exists(dest):
    sys.exit("%s exists; a later pass writes structure-pN.md" % a.out)

scheme = jl("scheme_v2.jsonl")
S = dict((t["id"], t) for t in scheme)
fams = dict((f["family"], f["name"]) for f in jl("families.jsonl"))
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r) for r in t4 for m in r["members"])
dims = jl("dimensions.jsonl")
dim_of = dict((m, d) for d in dims for m in d["members"])
rows = jl("assignments_final.jsonl")
gh = jl("gate_history.jsonl")
cc = jl("coder_conflicts.jsonl")
notes = json.load(open(os.path.join(OUT, "_analysis", a.notes), encoding="utf-8"))
f4 = json.load(open(os.path.join(OUT, "_analysis", a.fields), encoding="utf-8"))["themes"]
RET = notes.get("return") or {}


def facts(field):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "facts", "--field", field, "--json",
                        "--limit", "10000"], cwd=ROOT, capture_output=True, text=True)
    return dict((r["sub"], r.get(field)) for r in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))


named = facts("n_subreddits_named")
first_h = facts("onset_first_code_hour")
last_h = facts("onset_last_code_hour")
items = facts("items_in_window")
ALL = set(named)
N = len(ALL)
carries = collections.defaultdict(set)
first_on = collections.defaultdict(set)
line_of = {}
for r in rows:
    line_of[(r["sub"], r["theme_id"])] = r
    th = r.get("third_order") or []
    for i, t in enumerate(th):
        carries[t].add(r["sub"])
        if i == 0:
            first_on[t].add(r["sub"])
work_rooms = set().union(*[carries[t] for t in ("T3-038", "T3-041", "T3-060", "T3-026", "T3-082", "T3-009")])
GATES = {"all": ALL, "work": work_rooms, "other": set(s for s, v in named.items() if (v or 0) > 0),
         "after": set(s for s, v in last_h.items() if v is not None and v > 73),
         "apr1": set(s for s, v in first_h.items() if v is not None and v < 32)}


def gate_of(t):
    g = notes["gate_of_t3"].get(t)
    if g:
        return g
    o = owner.get(t)
    return notes["gate_of_t4"].get(o["id"], "all") if o else "all"


def three(t):
    g = gate_of(t)
    c = carries[t]
    opp = GATES[g] | c
    return g, len(c), len(opp - c), N - len(opp), len(c - GATES[g])


def cite(tier, tid, n, seed):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "cite.py"), "--tier", tier, "--id", tid, "--n", str(n),
                        "--seed", str(seed), "--json"], cwd=ROOT, capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[0]).get("quotes") or []
    except (ValueError, IndexError):
        return []


def third_of(q):
    r = line_of.get((q["sub"], q["theme_id"])) or {}
    for t, ids in (r.get("support_by_theme") or {}).items():
        if q["code_id"] in ids:
            return t, "core"
    th = r.get("third_order") or []
    return (th[0] if th else None), "side"


L = []
P = L.append
P("# The data structure, stage C2, pass %d (%s)" % (a.pass_, a.leg))
P("")
P("Written from the ledgers by `out/_analysis/c2_structure_md.py`: `scheme_v2.jsonl`, `fourth/fourth.jsonl`, `dimensions.jsonl`, "
  "`assignments_final.jsonl`, `gate_history.jsonl`, `coder_conflicts.jsonl`, the room facts through `mem.py facts`, and quotes "
  "through `cite.py`. The authored notes (questions, near cases, least-sure members, opportunity gates, the pairwise "
  "separations) are in `out/_analysis/%s` and `%s`. The data-structure view is "
  "generated (`_views/data-structure`); this file is the account of it." % (a.fields, a.notes))
P("")
# Part A's return
P("## Part A's return, pass %d" % a.pass_)
P("")
P("The next table gives, per dimension, its fourth-order themes and the number of third-order themes each holds.")
P("")
P("| dimension | construct | fourth-order themes (third-order themes each) |")
P("|---|---|---|")
for d in dims:
    P("| %s %s | %s | %s |" % (d["id"], d["label"], d["construct"]["status"],
                             "; ".join("%s %s (%d)" % (m, next(r["name"] for r in t4 if r["id"] == m),
                                                       len(next(r["members"] for r in t4 if r["id"] == m))) for m in d["members"])))
P("")
P("- **Construct status.** Fourth-order themes: %d borrowed, %d adapted, %d coined. Dimensions: %d borrowed, %d adapted, %d coined. "
  "Every borrowed or adapted source is recalled until stage C3." % (
      sum(1 for r in t4 if r["declared"] == "borrowed"), sum(1 for r in t4 if r["declared"] == "adapted"),
      sum(1 for r in t4 if r["declared"] == "coined"), sum(1 for d in dims if d["construct"]["status"] == "borrowed"),
      sum(1 for d in dims if d["construct"]["status"] == "adapted"), sum(1 for d in dims if d["construct"]["status"] == "coined")))
LS = RET.get("least_sure_dims", {"text": "D03 Maintenance and D06 Host framing**, two members each",
                                  "pairs": ["D03|D06", "D03|D04"]})
P("- **The two dimensions I am least sure of: %s. Their separation, from both sides: %s" % (
    LS["text"], " ".join(notes["pairs"][k] for k in LS["pairs"])))
P("- **The alternative grouping rejected.** %s" % RET.get("alternative",
  "A separate contention dimension of Attribution, Repertoire of contention and Rivalry. "
  "Restraint and attack are moves in one order between rooms, the pair test called T3-010's pairs with T3-149 and T3-151 joints, "
  "and pass 1 found no arrow from attribution to either restraint or attack (A-tests in `notes-C2.md`); the rival stays open for "
  "pass 2. At the fourth-order tier no recut was made at pass 1: the forced placements are tested against rooms first."))
nconf = sum(1 for c in cc if any(line_of.get(tuple(i.split("/"))) for i in c.get("items") or []))
P("- **Coder conflicts that reached this file:** %d of %d, under *read another way* in the third-order blocks." % (nconf, len(cc)))
P("- **The fourth-order theme I am least sure of: %s" % RET.get("least_sure_t4",
  "T4-007 Stigmergy.** It rests on two large themes, building and extending, which "
  "could be read as plain production; the construct claims coordination through the trace, and A01 and A03 rest on it."))
P("- **Whether the contrast showed anything:** see the onset contrast at the foot of this file.")
P("")
P("All pairwise separations between dimensions, each written from both sides:")
P("")
for k, v in notes["pairs"].items():
    P("- **%s.** %s" % (k.replace("|", " and "), v))
P("")
# consistency
placed_t3 = set(carries)
unpicked = sorted(t for t in S if t not in owner)
P("## Consistency, computed")
P("")
P("- Every third-order theme placed in `assignments_final.jsonl` is defined in `scheme_v2.jsonl`: %s (%d placed, %d defined)." % (
    placed_t3 <= set(S), len(placed_t3), len(S)))
P("- Every third-order theme sits in a fourth-order theme's members or in the unpicked list (%s): %s." % (
    ", ".join(unpicked), all(t in owner or t in unpicked for t in S)))
P("- Every fourth-order theme sits in a dimension's members: %s (%d of %d)." % (all(r["id"] in dim_of for r in t4),
                                                                           sum(1 for r in t4 if r["id"] in dim_of), len(t4)))
P("- Every dimension used is defined: %s." % all(r.get("dimension") and all(x in [d["id"] for d in dims] for x in r["dimension"]) for r in t4))
bad = [t for t in S if sum(three(t)[1:4]) != N]
P("- The three counts sum to the analysed set (%d, `counts.py`) for every third-order theme: %s." % (N, not bad))
P("")
# dimensions
P("## The dimensions")
P("")
for d in dims:
    cb = d["construct"]
    nd = notes["dimensions"][d["id"]]
    rooms = set().union(*[carries[m] for r in t4 if r["id"] in d["members"] for m in r["members"]])
    P("### %s %s" % (d["id"], d["label"]))
    P("")
    P("- **Declared:** %s%s." % (cb["status"], (", recalled; source: %s" % cb["source"]) if cb.get("source") else ", this corpus's"))
    if cb.get("changed"):
        P("- **What this material's version cannot do, or what was coined:** %s" % cb["changed"])
    P("- **Gloss:** \"%s\" [%s]" % (cb["gloss"], cb["gloss_from"]))
    P("- **The question it answers that no member answers alone:** %s" % d["question"])
    P("- **Membership predicate and gate:** %s" % d["predicate"])
    P("- **May be mistaken for:** %s" % cb["mistaken_for"])
    P("- **Would be disconfirmed elsewhere if:** %s" % cb["disconfirm_elsewhere"])
    P("- **What falls outside:** %s" % nd["outside"])
    P("- **The member I was least sure of:** %s" % nd["least_sure"])
    P("- **Members:** %s. Rooms carrying any member: %d of %d. Confidence: %s." % (
        ", ".join("%s %s" % (m, next(r["name"] for r in t4 if r["id"] == m)) for m in d["members"]), len(rooms), N, d["confidence"]))
    P("")
# fourth-order themes
P("## The fourth-order themes")
P("")
for i, r in enumerate(t4):
    f = f4[r["id"]]
    rooms = set().union(*[carries[m] for m in r["members"]])
    P("### %s %s" % (r["id"], r["name"]))
    P("")
    P("- **Declared:** %s%s. Dimension: %s. In the model: %s." % (
        r["declared"], (", recalled; source: %s" % r["source"]) if r.get("source") else ", this corpus's",
        ", ".join(r.get("dimension") or []), r.get("in_model")))
    P("- **Gloss:** \"%s\" [%s]" % (r["gloss"], r["gloss_from"]))
    P("- **What this material's version cannot do:** %s" % f["changed"])
    P("- **What holds it together:** %s" % r["prose"])
    P("- **The question it answers:** %s" % f["question"])
    P("- **What falls outside:** %s" % f["outside"])
    P("- **The member I was least sure of:** %s" % f["least_sure"])
    P("- **Members:** %s. Rooms carrying any member: %d of %d." % (
        ", ".join("%s %s" % (m, S[m]["name"]) for m in r["members"]), len(rooms), N))
    qs = cite("4th", r["id"], 5, 20261014 + i)
    seen_rooms = set(q["sub"] for q in qs)
    seen_second = set((q["sub"], q["theme_id"]) for q in qs)
    hrs = [q["hour"] for q in qs if q.get("hour") is not None]
    P("- **Material:** %d quotes from %d second-order themes in %d rooms, hours %s to %s (`cite.py --tier 4th --id %s --n 5`, seed "
      "%d)%s." % (len(qs), len(seen_second), len(seen_rooms), "%.1f" % min(hrs) if hrs else "-", "%.1f" % max(hrs) if hrs else "-",
                  r["id"], 20261014 + i, "; every quote from one room" if len(seen_rooms) == 1 else ""))
    P("")
    P("```json")
    for q in qs:
        t3, pos = third_of(q)
        other = [owner[x]["id"] for x in ((line_of.get((q["sub"], q["theme_id"])) or {}).get("third_order") or [])
                 if x in owner and owner[x]["id"] != r["id"]]
        P(json.dumps({"fourth": r["id"], "third": t3, "second_order": q.get("second_order"), "code_id": q["code_id"],
                      "sub": q["sub"], "author": q.get("author"), "created_utc": q.get("created_utc"),
                      "hour_since_open": q.get("hour"), "quote": q["text"], "position": "between" if other else pos,
                      "nearest_neighbour": other[0] if other else None,
                      "why_this_one": "%s, in %s's %s" % (q.get("first_order"), q["sub"], q.get("second_order"))},
                     ensure_ascii=False))
    P("```")
    P("")
# third-order themes
P("## The third-order themes")
P("")
P("Rule 5's three numbers per theme: carries; had the opportunity and does not; had no opportunity. They sum to %d. The gate "
  "for each is named, as declared before counting: %s." % (N, "; ".join("**%s**: %s" % (k, v) for k, v in notes["gates"].items())))
P("")
by_t3_gate = collections.defaultdict(list)
for g in gh:
    by_t3_gate[g["theme"]].append(g)
conf_of = collections.defaultdict(list)
for c in cc:
    for it in c.get("items") or []:
        s, tid = it.split("/")
        r = line_of.get((s, tid))
        for t in (r or {}).get("third_order") or []:
            conf_of[t].append((c, it))
for k, t in enumerate(scheme):
    tid = t["id"]
    o = owner.get(tid)
    g, nc, nn, nno, outside = three(tid)
    P("### %s %s" % (tid, t["name"]))
    P("")
    P("- **What it is:** %s%s" % (t.get("gloss", ""), " Rare tier." if t.get("tier") == "rare" else ""))
    P("- **What it is not:** %s" % t.get("is_not", ""))
    gs = by_t3_gate.get(tid) or []
    P("- **The borderline repaired at C1:** %s" % ("; ".join("%s (%s): %s" % (x["ref"], x["field"], (x["now"] if isinstance(x["now"], str)
                                                                                                    else "discriminators rewritten")[:260]) for x in gs) if gs else "none; the gate stands as frozen at B2."))
    ds = t.get("discriminators") or []
    P("- **Nearest neighbours and the separating test:** %s" % ("; ".join("against %s %s: %s" % (x["vs"], S.get(x["vs"], {}).get("name", ""), x["question"]) for x in ds[:2]) or "none written"))
    P("- **What varies:** %s" % t.get("varies", ""))
    P("- **Gate:** must show: %s Must not show: %s Decide when both: %s" % (t.get("must_show", ""), t.get("must_not_show", ""), t.get("decide_when_both", "")))
    P("- **Three numbers (rule 5), gate %s:** carries %d; had the opportunity and does not %d; had no opportunity %d%s. As first theme in %d rooms. Fourth-order theme: %s." % (
        g, nc, nn, nno, ("; %d carriers fall outside the gate" % outside) if outside else "", len(first_on[tid]),
        ("%s %s" % (o["id"], o["name"])) if o else "none (unpicked)"))
    qs = cite("3rd", tid, 3, 20261014 + 100 + k) if nc else []
    if qs:
        P("- **Exemplars** (`cite.py --tier 3rd --id %s --n 3`):" % tid)
        P("")
        P("```json")
        for q in qs:
            P(json.dumps({"third": tid, "code_id": q["code_id"], "sub": q["sub"], "second_order": q.get("second_order"),
                          "hour_since_open": q.get("hour"), "quote": q["text"]}, ensure_ascii=False))
        P("```")
    else:
        P("- **Exemplars:** none placed at C1's close; the theme travels on the exemplars written into `scheme_v2.md`.")
    cs = conf_of.get(tid) or []
    if cs:
        seen = set()
        P("- **Read another way** (coder conflicts with an item placed here; the count rests on the placement in `assignments_final.jsonl`):")
        for c, it in cs:
            if c["id"] in seen:
                continue
            seen.add(c["id"])
            here = [x for x in c.get("items") or [] if tid in ((line_of.get(tuple(x.split("/"))) or {}).get("third_order") or [])]
            there = [x for x in c.get("items") or [] if x not in here]
            terms = c.get("terms") or {}
            P("  - %s, %s: %s Here: %s. %s" % (
                c["id"], c.get("practice", ""), c.get("conflict", ""),
                "; ".join("%s ('%s')" % (x, terms.get(x, "")) for x in here[:2]),
                ("Elsewhere: %s." % "; ".join("%s ('%s', placed %s)" % (x, terms.get(x, ""), ",".join((line_of.get(tuple(x.split("/"))) or {}).get("third_order") or []) or "empty") for x in there[:2])) if there else "No item placed elsewhere."))
    P("")
# unpicked
P("## What no fourth-order theme picked up")
P("")
mass = dict((t, sum(len((r.get("support_by_theme") or {}).get(t) or []) for r in rows)) for t in unpicked)
P("%d of %d third-order themes: %s. They carry %d placement lines in %d rooms, and %d cited concepts." % (
    len(unpicked), len(S), ", ".join("%s %s" % (t, S[t]["name"]) for t in unpicked),
    sum(1 for r in rows if set(r.get("third_order") or []) & set(unpicked)), len(set().union(*[carries[t] for t in unpicked])),
    sum(mass.values())))
P("")
P("What they are in general: the sub's ordinary business going on beside the event, and one hacked sub recovered. Neither is an act of "
  "organizing the canvas work, and neither should have been a fourth-order theme: gathered, they would make a catch-all of what the "
  "event left untouched. T3-017 is the ground the host community's boundary work protects (Host framing); T3-133 is one room's event.")
P("")
P("```json")
for t in unpicked:
    for q in cite("3rd", t, 2, 20261015):
        P(json.dumps({"third": t, "code_id": q["code_id"], "sub": q["sub"], "second_order": q.get("second_order"),
                      "hour_since_open": q.get("hour"), "quote": q["text"]}, ensure_ascii=False))
P("```")
P("")
# pairs
P("## The pairs (rule 0's doubles), Part C's raw material")
P("")
pairs = collections.defaultdict(list)
for r in rows:
    th = r.get("third_order") or []
    for x in th[1:]:
        pairs[(th[0], x)].append(r)
P("A pair is a placement line that holds two third-order themes, the first as primary. The next table lists the 25 pairs with the "
  "most rooms (rule 4: the community count decides), with the lines, whether the pair crosses a dimension boundary, and one line's "
  "supporting concepts for each side.")
P("")
P("| primary | additional | rooms | lines | crosses dimensions | supporting concepts (one line) |")
P("|---|---|---|---|---|---|")
for (x, y), rs in sorted(pairs.items(), key=lambda kv: (-len(set(r["sub"] for r in kv[1])), -len(kv[1])))[:25]:
    dx = dim_of.get(owner[x]["id"])["id"] if x in owner else "-"
    dy = dim_of.get(owner[y]["id"])["id"] if y in owner else "-"
    r0 = sorted(rs, key=lambda r: (r["sub"].lower(), r["theme_id"]))[0]
    sup = r0.get("support_by_theme") or {}
    P("| %s %s | %s %s | %d | %d | %s | %s:%s %s: %s; %s: %s |" % (
        x, S[x]["name"], y, S[y]["name"], len(set(r["sub"] for r in rs)), len(rs),
        ("yes (%s, %s)" % (dx, dy)) if dx != dy else "no (%s)" % dx, r0["sub"], r0["theme_id"], x,
        ",".join((sup.get(x) or [])[:3]), y, ",".join((sup.get(y) or [])[:3])))
P("")
cross = sum(1 for (x, y), rs in pairs.items() if x in owner and y in owner and dim_of[owner[x]["id"]]["id"] != dim_of[owner[y]["id"]]["id"]
            for _ in rs)
P("Of %d double placements (lines with a second theme), %d cross a dimension boundary: the doubles are where Part C looks for "
  "arrows between dimensions." % (sum(len(v) for v in pairs.values()), cross))
P("")
# onset contrast
contrast = open(os.path.join(OUT, "contrast.md"), encoding="utf-8").read()
early = set(x.strip() for x in contrast.split("## Members, early side (131)")[1].split("##")[0].replace("\n", " ").split(",") if x.strip()) | {"italy"}
late = set(x.strip() for x in contrast.split("## Members, late side (61)")[1].split("##")[0].replace("\n", " ").split(",") if x.strip())
held = contrast.split("## Held size (items_in_window 156 to 2770)")[1]
he = set(x.strip().rstrip(".") for x in held.split("Early, 41:")[1].split("Late, 12:")[0].replace("\n", " ").split(",") if x.strip())
hl = set(x.strip().rstrip(".") for x in held.split("Late, 12:")[1].split("##")[0].replace("\n", " ").split(",") if x.strip())
P("## The onset contrast")
P("")
P("Early side %d rooms, late side %d (`contrast.md`); held size (`items_in_window` 156 to 2,770) %d and %d. The denominator for each "
  "share is the side's room count. The next table gives, per dimension and for the third-order themes the contrast's expectations "
  "name, the share of each side's rooms that carry it." % (len(early), len(late), len(he), len(hl)))
P("")
P("| what | early (n=%d) | late (n=%d) | held early (n=%d) | held late (n=%d) |" % (len(early), len(late), len(he), len(hl)))
P("|---|---|---|---|---|")


def share(rs, group):
    return "%d (%.2f)" % (len(rs & group), len(rs & group) / float(len(group))) if group else "-"


for d in dims:
    rs = set().union(*[carries[m] for r in t4 if r["id"] in d["members"] for m in r["members"]])
    P("| %s %s | %s | %s | %s | %s |" % (d["id"], d["label"], share(rs, early), share(rs, late), share(rs, he), share(rs, hl)))
for t in ("T3-035", "T3-020", "T3-022", "T3-039", "T3-041", "T3-005", "T3-006", "T3-050", "T3-010", "T3-150") + (
        ("T3-011", "T3-151") if a.pass_ >= 2 else ()):
    rs = carries[t]
    P("| %s %s | %s | %s | %s | %s |" % (t, S[t]["name"], share(rs, early), share(rs, late), share(rs, he), share(rs, hl)))
P("")
P("Stage A1 expected late rooms to organize around finding room on a full canvas (asking for space, moving, fitting, treaties to be "
  "let in), early rooms around claiming, enlarging and holding; early rooms to name rivals and keep fights going; and at held size "
  "the first difference to stay and most of the third to go. Read against the table: see `notes-C2.md`, pass %d, where the "
  "verdict is written with the twelve held-size late rooms labelled thin." % a.pass_)
P("")
open(dest, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote %s: %d words; %d third-order, %d fourth-order, %d dimension blocks; bad sums %s" % (
    a.out, len(" ".join(L).split()), len(scheme), len(t4), len(dims), bad[:5]))
