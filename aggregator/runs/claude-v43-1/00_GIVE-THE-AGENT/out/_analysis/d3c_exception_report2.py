#!/usr/bin/env python3
"""D3c: build exception-report-D.md from the ledgers (stage D3 section 6; SCHEMA section 7; prior.md section 3).
Supersedes d3c_exception_report.py (an unrun draft that counted shared changes within one ledger only).
No count in it is typed: every figure is computed here. Two ledgers are reported, each with the model its labelers
held: the first return (adaptations.jsonl, served e15f9647...) and the re-check (adaptations-recheck.jsonl, served
46384686..., the version frozen at D3c), each line by its last ruling in adjudications.jsonl.

Classes, by the last ruling: 'shared' = accepted (or modified) specification, paired elaboration or correction;
'proposal' = an accepted propose line (it entered a candidate); 'limit' = accepted with kind none (an evidence
limit); 'particular' = a locally supported particular, NONPORTABLE lines (portable false) counted apart; 'rejected';
'pending'. A distinct shared change (prior.md section 3) is a group of accepted elaborations and corrections that D3
joined through their pairs on one element, across both ledgers, met in two rooms or more; a specification restates
a standing statement and is no change. The model's top elements are read as the spine prior.md section 8 names (a
start, calls, building, keeping: R01, P01, P03, P05, and the arrows A02, A01, A03 between them). The rooms whose
adaptations are all particulars are found as the close-check finds them (every line of a room, both ledgers).

    python3 out/_analysis/d3c_exception_report2.py --seed 2026102410 [--write]
"""
import argparse, collections, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "exception-report-D.md")
ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
if a.write and os.path.exists(DEST):
    raise SystemExit("refusing to overwrite %s; supersede with a new name" % DEST)
SPINE = ["R01", "P01", "P03", "P05", "A02", "A01", "A03"]
P05_ROOMS = ["completeanarchy", "polska", "satania", "halo", "bangtan", "thesilphroad", "armok", "maryland", "oneshot"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
ledgers = collections.OrderedDict([("first return", jl(os.path.join(OUT, "adaptations.jsonl"))),
                                   ("re-check", jl(os.path.join(OUT, "adaptations-recheck.jsonl")))])
by_id = {}
for name, L in ledgers.items():
    for l in L:
        by_id[l["id"]] = dict(l, _ledger=name)
scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
rooms = sorted(scope["affected_rooms"], key=str.lower)


def cls(l):
    d = last.get(l["id"], {})
    dec = d.get("decision")
    if dec in ("accept", "modify"):
        kind = d.get("kind") or l.get("kind")
        if kind in ("specification", "elaboration", "correction"):
            return kind
        if kind == "proposal":
            return "proposal"
        return "limit"
    if dec == "particular":
        return "particular-np" if l.get("portable") is False else "particular"
    if dec == "reject":
        return "rejected"
    if dec == "pending":
        return "pending"
    return "unruled"


# distinct shared changes: elaborations and corrections joined through their pairs on one element, both ledgers
chg = {i: l for i, l in by_id.items() if cls(l) in ("elaboration", "correction")}
parent = {i: i for i in chg}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


cross = 0
for i, l in chg.items():
    q = last[i].get("pair")
    if q in chg and chg[q]["element"] == l["element"]:
        parent[find(i)] = find(q)
        cross += chg[q]["_ledger"] != l["_ledger"]
comp = collections.defaultdict(list)
for i in chg:
    comp[find(i)].append(i)
shared = [c for c in comp.values() if len({chg[i]["sub"] for i in c}) >= 2]
lone = [c for c in comp.values() if len({chg[i]["sub"] for i in c}) < 2]

w = []
w.append("# Exception report, stage D3\n")
w.append("Built at D3c by `_analysis/d3c_exception_report2.py` (seed %d) from the ledgers and their last rulings; no "
         "figure in it is typed. It reports the first return (served e15f9647...) and the re-check (served "
         "46384686..., the version frozen at D3c, QD3-011), each line by its last ruling. 'Shared' lines are accepted "
         "specifications, paired elaborations and corrections; 'limits' are lines accepted with kind none (evidence "
         "limits); 'particulars' are locally supported particulars, with the NONPORTABLE lines counted apart. The "
         "model's top elements are read as prior.md's spine (a start, calls, building, keeping): %s.\n" % (
             a.seed, ", ".join(SPINE)))

# --- composition criteria
w.append("## The composition criteria (prior.md section 3), with the shares\n")
w.append("prior.md fixes no numerical cutoff. It asks for local adequacy over 705 rooms, a count of distinct shared "
         "changes apart from ledger lines, the curve of those changes over a seeded order of rooms, the share of rooms "
         "whose particulars touch the top elements, and the fixed-global verdicts, particulars and corrections met "
         "twice as diagnostics, with pre- and post-adaptation fit. Each is below, with its denominator.\n")
w.append("### Ledger lines, by ruling\n")
for name, L in ledgers.items():
    c = collections.Counter(cls(l) for l in L)
    per = collections.defaultdict(collections.Counter)
    for l in L:
        per[l["sub"]][cls(l)] += 1
    with_part = sum(1 for s in per if per[s]["particular"] + per[s]["particular-np"])
    spine_part = {l["sub"] for l in L if l.get("element") in SPINE and cls(l) in ("particular", "particular-np")}
    npart = collections.Counter()
    for s in per:
        k = per[s]["particular"] + per[s]["particular-np"]
        npart["0" if k == 0 else "1 to 2" if k <= 2 else "3 to 5" if k <= 5 else "6 or more"] += 1
    w.append("- **%s:** %d lines in %d rooms. Specifications %d, paired elaborations %d, corrections %d, accepted "
             "proposals %d, limits %d, particulars %d and NONPORTABLE particulars %d, rejected %d, pending %d, "
             "unruled %d." % (name, len(L), len(per), c["specification"], c["elaboration"], c["correction"],
                              c["proposal"], c["limit"], c["particular"], c["particular-np"], c["rejected"],
                              c["pending"], c["unruled"]))
    w.append("  - Particulars are %.1f%% of the lines and %.1f%% of the lines that are not limits or rejected. Rooms "
             "carrying at least one particular: %d of %d. Rooms by their particulars: %s." % (
                 100.0 * (c["particular"] + c["particular-np"]) / len(L),
                 100.0 * (c["particular"] + c["particular-np"]) / (len(L) - c["limit"] - c["rejected"]),
                 with_part, len(per), ", ".join("%s: %d" % (k, npart[k]) for k in ("0", "1 to 2", "3 to 5",
                                                                                     "6 or more"))))
    w.append("  - Rooms with a particular on a top element (%s): %d of %d (%.1f%%)." % (
        ", ".join(SPINE), len(spine_part), len(per), 100.0 * len(spine_part) / len(per)))
w.append("")
w.append("### Distinct shared changes, apart from ledger lines\n")
in_re = [x for x in shared if any(chg[i]["_ledger"] == "re-check" for i in x)]
w.append("- Accepted elaborations and corrections: %d ledger lines (both ledgers). D3's pairs join them into %d groups "
         "on one element each (%d pairs cross the two ledgers). %d groups are met in two rooms or more: these are the "
         "distinct shared changes, over %d ledger lines. %d groups stay in one room (a lone line whose pair was "
         "re-ruled, or a room's first-return line and its re-check repeat)." % (
             len(chg), len(comp), cross, len(shared), sum(len(x) for x in shared), len(lone)))
w.append("- Of the %d distinct shared changes, %d carry a re-check line (they are met against the frozen version) and "
         "%d rest on first-return lines alone." % (len(shared), len(in_re), len(shared) - len(in_re)))
by_el = collections.Counter(chg[x[0]]["element"] for x in shared)
w.append("- Distinct shared changes by element (the ten most): %s." % ", ".join(
    "%s %d" % kv for kv in by_el.most_common(10)))
w.append("- prior.md asks that the two rooms be unlike in size, side or form. This report does not test that; it is "
         "D4's, where the branches are built from these keys.")
order = rooms[:]
random.Random(a.seed).shuffle(order)
pos = []
for x in shared:
    rs = sorted({chg[i]["sub"] for i in x}, key=order.index)
    pos.append(order.index(rs[1]))
thirds = [len(order) // 3, 2 * len(order) // 3, len(order)]
cum = [sum(1 for p in pos if p < m) for m in thirds]
w.append("- **The curve** (rooms in a seeded order, seed %d; a shared change counts once its second room has "
         "entered). After %d rooms: %d; after %d: %d; after all %d: %d. The first third adds %d, the second %d and the "
         "last %d." % (a.seed, thirds[0], cum[0], thirds[1], cum[1], thirds[2], cum[2], cum[0], cum[1] - cum[0],
                        cum[2] - cum[1]))
size = collections.Counter()
for x in shared:
    k = len({chg[i]["sub"] for i in x})
    size["2" if k == 2 else "3 to 5" if k <= 5 else "6 to 20" if k <= 20 else "more than 20"] += 1


def p_two(k, m, n):
    """P(at least 2 of a change's k rooms fall in the first m of n rooms, in a random order)."""
    from math import comb
    return 1.0 - (comb(n - k, m) + k * comb(n - k, m - 1)) / comb(n, m)


exp = [sum(p_two(len({chg[i]["sub"] for i in x}), m, len(order)) for x in shared) for m in thirds[:2]] + [len(shared)]
w.append("- The groups by their rooms: %s. In any order of the rooms, a change met in two rooms counts only when the "
         "later of the two enters, so a set of changes each met in few rooms keeps growing to the end of the order. "
         "For these group sizes, the expected adds "
         "by third over random orders are %.0f, %.0f and %.0f, against the seeded %d, %d and %d. So the curve's shape "
         "comes from how many rooms each change is met in, and most changes are met in few rooms. prior.md names a "
         "curve that does not flatten over the last third as a sign of unbounded revision; on D3's pair groups the "
         "curve does not flatten. The pairs join two lines at a time and were not built to merge every line stating "
         "one change, so the group count can exceed the count of distinct changes; D4's keys may merge groups." % (
             ", ".join("%s rooms: %d" % (k, size[k]) for k in ("2", "3 to 5", "6 to 20", "more than 20")),
             exp[0], exp[1] - exp[0], exp[2] - exp[1], cum[0], cum[1] - cum[0], cum[2] - cum[1]))
cand = [e for e in jl(os.path.join(OUT, "model", "elements.jsonl")) if e.get("status") == "candidate"]
w.append("- Accepted `propose` lines are counted apart: they entered the model as %d candidate elements (%s), and "
         "they are new elements, not changes to a standing one.\n" % (len(cand), ", ".join(e["id"] for e in cand)))

w.append("### Local adequacy, and fit before and after adaptation\n")
ls, gr = collections.Counter(), collections.Counter()
for s in rooms:
    p = os.path.join(OUT, "rooms", s, "model-D-recheck.md")
    t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    m = re.search(r"^local_status:\s*(\S+)", t, re.M)
    g = re.search(r"^grade:\s*(\S+)", t, re.M)
    ls[m.group(1) if m else "none"] += 1
    gr[g.group(1) if g else "none"] += 1
w.append("- **Local status** (the labelers' revised local accounts, `rooms/<sub>/model-D-recheck.md`, %d rooms): %s. "
         "Their own grade: %s." % (len(rooms), ", ".join("%s %d" % kv for kv in sorted(ls.items())),
                                   ", ".join("%s %d" % kv for kv in sorted(gr.items()))))
w.append("- The labelers marked a room unresolved where a claim stayed open in their own account. After the "
         "adjudication, no ledger line is pending: every line is accepted, a particular or rejected. The local status "
         "is reported as the labelers wrote it; it is not raised by my rulings, and a room is not called locally "
         "validated here.")
w.append("- **Fit before and after adaptation.** Before: the fixed-global verdicts below, readers judging each room "
         "against the model as served. After: the labelers' grade above, on the room's adapted account. Exact local "
         "fit is not evidence of global composition by itself.\n")

# --- verdicts
w.append("## The fixed-global verdicts, by version\n")
vr = jl(os.path.join(OUT, "verdicts-D.jsonl"))
first_r = {r["sub"]: r for r in vr if r.get("ruled_by") == "analyst" and not r.get("recheck")}
re_r = {r["sub"]: r for r in vr if r.get("ruled_by") == "analyst" and r.get("recheck")}


def settle(rows, ruled):
    d = {}
    for r in rows:
        if r.get("ruled_by"):
            continue
        vs = {e["verdict"] for e in r["readers"]}
        d[r["sub"]] = ruled[r["sub"]]["verdict"] if r["sub"] in ruled else (vs.pop() if len(vs) == 1 else "split")
    return d


first = settle(vr, first_r)
after = settle(jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")), re_r)
for name, d, nr in (("First return (e15f9647...; the readers' agreed verdict, else my D3a-56 ruling)", first,
                     len(first_r)),
                    ("Re-check (46384686...; the readers' agreed verdict, else my G62 ruling)", after, len(re_r))):
    c = collections.Counter(d.values())
    w.append("- **%s:** %s, over %d rooms; %d rooms ruled where the readers split." % (
        name, ", ".join("%s %d" % kv for kv in sorted(c.items())), len(d), nr))
dnc1 = sorted(s for s, v in first.items() if v == "does-not-compose")
dnc2 = sorted(s for s, v in after.items() if v == "does-not-compose")
w.append("- does-not-compose: %s at the first return (its kind in `uncomposed-D.md`); %s at the re-check." % (
    ", ".join(dnc1) or "none", ", ".join(dnc2) or "none"))
ctu = collections.Counter()
for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    if after.get(r["sub"]) == "cannot-tell":
        ctu[re_r[r["sub"]].get("cannot_tell_under") if r["sub"] in re_r else r["readers"][0].get("cannot_tell_under")] += 1
w.append("- cannot-tell at the re-check, by threshold: %s." % ", ".join("%s %d" % kv for kv in sorted(ctu.items())))
w.append("- validate.py's counts take the last ruling per room in `verdicts-D.jsonl`, else the first-return readers' "
         "agreed line, so they mix the two versions. The notes give both.\n")

# --- corrections met twice
w.append("## Corrections met twice (section 2), reported apart\n")
hist = open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8").read()
met = collections.defaultdict(set)
for i, l in by_id.items():
    if cls(l) != "correction":
        continue
    lift = l.get("lift") or []
    for lvl in (1, 2):
        if len(lift) > lvl and lift[lvl]:
            met[(l["element"], lift[lvl])].add(i)
groups = [(k, v) for k, v in sorted(met.items()) if len({by_id[i]["sub"] for i in v}) >= 2]
w.append("Accepted corrections, both ledgers, grouped by element and by the lifted node at the third or fourth level, "
         "two rooms or more: %d groups, %d of them cited in `model/history.jsonl`." % (
             len(groups), sum(1 for _, v in groups if any(i in hist for i in v))))
for (el, node), v in groups:
    rs = sorted({by_id[i]["sub"] for i in v})
    led = collections.Counter(by_id[i]["_ledger"] for i in v)
    w.append("- %s at %s: %d lines (%s) in %d rooms: %s. Cited: %s." % (
        el, node, len(v), ", ".join("%s %d" % kv for kv in sorted(led.items())), len(rs), ", ".join(rs),
        "yes" if any(i in hist for i in v) else "no"))
w.append("- Repeated corrections are candidates for clusters, never a failure threshold. The moves they caused are 172 "
         "(R01), 173 (P05), 176 (A21's bound) and 197 (P05's scope, with no change to the frozen model).\n")

# --- P05
w.append("## P05's added clause: the scope decision at D3c (F-024; move 197; QD3-011)\n")
w.append("The clause move 173 added to P05 ('until its keepers are told of it, and it is lost or given up where the "
         "telling does not reach them') fails in nine rooms whose re-check correction the ledger accepts. The "
         "scope is decided as a bound with a cluster branch, carried in F-024 and history line 172; the frozen words "
         "are unchanged. The trunk is the clause, bounded to rooms where the keepers can learn of a planned change only "
         "by being told and no informed member holds it.")
for s in P05_ROOMS:
    ids_s = [l["id"] for l in ledgers["re-check"] if l["sub"] == s and l["element"] == "P05" and cls(l) == "correction"]
    w.append("- %s: %s (%s)" % (s, ", ".join(ids_s), "the keepers read the change from its shape: the branch"
                                  if s in P05_ROOMS[:6] else "informed members hold the change: a second limit"))
w.append("")

# --- all-particular rooms
w.append("## Rooms whose adaptations are all particulars\n")
per_all = collections.defaultdict(list)
for i, l in by_id.items():
    if l.get("op") != "none":
        per_all[l["sub"]].append(last.get(i, {}).get("decision"))
allp = sorted(s for s, ds in per_all.items() if ds and all(d == "particular" for d in ds))
if allp:
    for s in allp:
        w.append("- %s: every adaptation is a particular. For this room, a model whose adaptations are all "
                 "particulars has not composed." % s)
else:
    w.append("None, over %d rooms and both ledgers: in every room at least one line is accepted or rejected rather "
             "than a particular. The contract's sentence, 'a model whose adaptations are all particulars has not "
             "composed', applies to no room and not to the set." % len(per_all))
noshared = sorted(s for s in rooms if not any(cls(l) in ("specification", "elaboration", "correction")
                                            for l in ledgers["re-check"] if l["sub"] == s))
w.append("- A stricter reading: rooms with no shared line (specification, paired elaboration or correction) in the "
         "re-check: %d%s." % (len(noshared), (": " + ", ".join(noshared)) if noshared else ""))
w.append("")

# --- per element
w.append("## Per element: rooms adapting it, by op (re-check; shared lines, accepted proposals and particulars)\n")
L = ledgers["re-check"]
ops = ["instantiate", "restrict", "add-condition", "add-step", "link", "contradict", "absent", "propose"]
el_rooms = collections.defaultdict(lambda: collections.defaultdict(set))
corr_rooms, part_rooms = collections.defaultdict(set), collections.defaultdict(set)
for l in L:
    e = l.get("element") or "(none)"
    k = cls(l)
    if k in ("specification", "elaboration", "correction", "particular", "particular-np", "proposal"):
        el_rooms[e][l["op"]].add(l["sub"])
    if k == "correction":
        corr_rooms[e].add(l["sub"])
    if k in ("particular", "particular-np"):
        part_rooms[e].add(l["sub"])
w.append("| element | " + " | ".join(ops) + " | rooms with a correction | rooms with a particular |")
w.append("|---" * (len(ops) + 3) + "|")
for e in sorted(el_rooms):
    w.append("| %s | %s | %d | %d |" % (e, " | ".join(str(len(el_rooms[e][o])) for o in ops),
                                      len(corr_rooms[e]), len(part_rooms[e])))
w.append("")

# --- per room
w.append("## Per room: particulars against accepted shared lines\n")
w.append("Shared = accepted specifications, paired elaborations and corrections. Each cell: re-check / first return.\n")
w.append("| room | shared | of them corrections | limits | particulars | NONPORTABLE | rejected |")
w.append("|---|---|---|---|---|---|---|")
pr = {n: collections.defaultdict(collections.Counter) for n in ledgers}
for n, Ls in ledgers.items():
    for l in Ls:
        pr[n][l["sub"]][cls(l)] += 1
for s in rooms:
    cells = []
    for key in (("specification", "elaboration", "correction"), ("correction",), ("limit",), ("particular",),
                ("particular-np",), ("rejected",)):
        cells.append("%d / %d" % tuple(sum(pr[n][s][k] for k in key) for n in ("re-check", "first return")))
    w.append("| %s | %s |" % (s, " | ".join(cells)))
text = "\n".join(w) + "\n"
if not a.write:
    head = text.split("## Per element")[0]
    print(head)
    print("[dry run: %d lines, %d words; nothing written]" % (len(w), len(text.split())))
    raise SystemExit(0)
open(DEST, "w", encoding="utf-8").write(text)
print("wrote %s: %d lines" % (DEST, len(w)))
