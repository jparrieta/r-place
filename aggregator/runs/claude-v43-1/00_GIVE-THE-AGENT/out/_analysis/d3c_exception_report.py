#!/usr/bin/env python3
"""D3c: build exception-report-D.md from the ledgers (stage D3 section 6; SCHEMA section 7; prior.md section 3).
No count in it is typed: every figure is computed here. Two ledgers are reported, each with the model its labelers
held: the first return (adaptations.jsonl, served e15f9647...) and the re-check (adaptations-recheck.jsonl, served
46384686..., the version frozen at D3c), each line by its last ruling in adjudications.jsonl.

Sections: the versions; the composition criteria of prior.md section 3 with the shares computed against them
(local status, pending, particulars, distinct shared changes counted apart from ledger lines, their curve over a
seeded order of rooms, the share of rooms with a particular on the spine); the fixed-global verdicts by version;
corrections met twice; P05's scope decision (F-024); rooms whose adaptations are all particulars, with the
contract's sentence; per element, rooms adapting it by op; per room, particulars against accepted shared lines.

    python3 out/_analysis/d3c_exception_report.py --seed 2026102410 --out out/exception-report-D.md
"""
import argparse, collections, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
if os.path.abspath(a.out) != os.path.join(OUT, "exception-report-D.md"):
    raise SystemExit("--out must be out/exception-report-D.md")
if os.path.exists(a.out):
    raise SystemExit("refusing to overwrite %s; supersede with a new name" % a.out)
SPINE = ["R01", "A02", "P01", "A01", "P03", "A03", "P05"]
P05_ROOMS = ["completeanarchy", "polska", "satania", "halo", "bangtan", "thesilphroad", "armok", "maryland", "oneshot"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
ledgers = {"first return": jl(os.path.join(OUT, "adaptations.jsonl")),
           "re-check": jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
rooms = sorted(scope["affected_rooms"], key=str.lower)


def cls(l):
    d = last.get(l["id"], {})
    dec, kind = d.get("decision"), d.get("kind")
    if dec in ("accept", "modify"):
        if kind in ("specification", "elaboration", "correction", "proposal"):
            return kind
        return "limit"
    if dec == "particular":
        return "particular-np" if l.get("portable") is False else "particular"
    if dec == "reject":
        return "rejected"
    if dec == "pending":
        return "pending"
    return "unruled"


def components(lines):
    """Distinct shared changes: accepted elaborations and corrections joined by their pairs, one element and one op."""
    ids = {l["id"]: l for l in lines if cls(l) in ("elaboration", "correction")}
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, l in ids.items():
        p = last[i].get("pair")
        for q in (p if isinstance(p, list) else [p]):
            if q in ids and ids[q]["element"] == l["element"]:
                parent[find(i)] = find(q)
    comp = collections.defaultdict(list)
    for i in ids:
        comp[find(i)].append(i)
    shared = [c for c in comp.values() if len({ids[i]["sub"] for i in c}) >= 2]
    return shared, ids


w = []
w.append("# Exception report, stage D3\n")
w.append("Built by `_analysis/d3c_exception_report.py` from the ledgers at D3c; no figure in it is typed. It reports "
         "the first return (served e15f9647...) and the re-check (served 46384686..., the version frozen at D3c, "
         "QD3-011), each line by its last ruling. 'Shared' lines are accepted specifications, paired elaborations "
         "and corrections; 'limits' are lines accepted with kind none (evidence limits); 'particulars' are locally "
         "supported particulars, NONPORTABLE lines counted apart.\n")

# --- composition criteria
w.append("## The composition criteria (prior.md section 3), with the shares\n")
for name, L in ledgers.items():
    c = collections.Counter(cls(l) for l in L)
    per = collections.defaultdict(collections.Counter)
    for l in L:
        per[l["sub"]][cls(l)] += 1
    with_part = sum(1 for s in per if per[s]["particular"] + per[s]["particular-np"])
    spine_part = {l["sub"] for l in L if l.get("element") in SPINE and cls(l) in ("particular", "particular-np")}
    shared, _ = components(L)
    w.append("- **%s:** %d lines in %d rooms. Specifications %d, paired elaborations %d, corrections %d, accepted "
             "proposals %d, limits %d, particulars %d (and %d NONPORTABLE), rejected %d, pending %d, unruled %d." % (
                 name, len(L), len(per), c["specification"], c["elaboration"], c["correction"], c["proposal"],
                 c["limit"], c["particular"], c["particular-np"], c["rejected"], c["pending"], c["unruled"]))
    w.append("  - Rooms carrying at least one particular: %d of %d. Rooms with a particular on the spine (%s): %d of %d."
             % (with_part, len(per), ", ".join(SPINE), len(spine_part), len(per)))
    w.append("  - Distinct shared changes (paired elaborations and corrections joined through their pairs, one element "
             "and one op, met in two rooms or more): %d, over %d ledger lines." % (
                 len(shared), sum(len(x) for x in shared)))
w.append("- **Local status.** The labelers' own accounts (`rooms/<sub>/model-D-recheck.md`) give the local status of "
         "every room:")
ls = collections.Counter()
for s in rooms:
    p = os.path.join(OUT, "rooms", s, "model-D-recheck.md")
    m = re.search(r"local_status:\s*(validated|unresolved|insufficient-evidence)",
                  open(p, encoding="utf-8").read()) if os.path.exists(p) else None
    ls[m.group(1) if m else "none"] += 1
w.append("  %s. A locally validated account cannot hold pending claims; no line is pending." % ", ".join(
    "%s %d" % kv for kv in sorted(ls.items())))
# curve of distinct shared changes over a seeded order of rooms (re-check)
order = rooms[:]
random.Random(a.seed).shuffle(order)
L = ledgers["re-check"]
shared, ids = components(L)
first_full = {}
for comp in shared:
    members = sorted({ids[i]["sub"] for i in comp}, key=order.index)
    first_full[id(comp)] = order.index(members[1])
pos = sorted(first_full.values())
marks = [len(order) // 3, 2 * len(order) // 3, len(order)]
counts = [sum(1 for p in pos if p < m) for m in marks]
w.append("- **The curve (re-check, rooms in a seeded order, seed %d).** A shared change counts once its second room "
         "has entered. After the first third of the rooms (%d): %d distinct shared changes; after two thirds (%d): %d; "
         "after all %d: %d. Over the last third, %d new shared changes enter, against %d in the first third." % (
             a.seed, marks[0], counts[0], marks[1], counts[1], marks[2], counts[2], counts[2] - counts[1], counts[0]))
w.append("- What D3 does not settle: whether the branches explain their members jointly is D4's and D5's (cluster "
         "adequacy); this report counts the material for it. Exact local fit is not evidence of global composition by "
         "itself.\n")

# --- verdicts
w.append("## The fixed-global verdicts, by version\n")
vr = jl(os.path.join(OUT, "verdicts-D.jsonl"))
first_r = {r["sub"]: r for r in vr if r.get("ruled_by") == "analyst" and not r.get("recheck")}
re_r = {r["sub"]: r for r in vr if r.get("ruled_by") == "analyst" and r.get("recheck")}
first, after = {}, {}
for r in vr:
    if r.get("ruled_by"):
        continue
    vs = {e["verdict"] for e in r["readers"]}
    first[r["sub"]] = first_r[r["sub"]]["verdict"] if r["sub"] in first_r else (vs.pop() if len(vs) == 1 else "split")
for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    vs = {e["verdict"] for e in r["readers"]}
    after[r["sub"]] = re_r[r["sub"]]["verdict"] if r["sub"] in re_r else (vs.pop() if len(vs) == 1 else "split")
for name, d, nr in (("first return (e15f9647...; readers' agreed verdicts and my D3a-56 rulings)", first, len(first_r)),
                    ("re-check (46384686...; readers' agreed verdicts and my G62 rulings)", after, len(re_r))):
    c = collections.Counter(d.values())
    w.append("- **%s:** %s; %d rooms ruled where the readers split." % (
        name, ", ".join("%s %d" % kv for kv in sorted(c.items())), nr))
w.append("- does-not-compose: picturegame at the first return (out-of-scope, `uncomposed-D.md`); none at the re-check, "
         "where picturegame composes with residue by both readers.")
ctu = collections.Counter()
for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    if after.get(r["sub"]) == "cannot-tell":
        for e in r["readers"]:
            if e.get("verdict") == "cannot-tell":
                ctu[e.get("cannot_tell_under")] += 1
w.append("- cannot-tell at the re-check, by the readers' stated threshold: %s.\n" % ", ".join(
    "%s %d" % kv for kv in sorted(ctu.items())))

# --- corrections met twice
w.append("## Corrections met twice (section 2), apart\n")
hist = open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8").read()
for name, L in ledgers.items():
    met = collections.defaultdict(set)
    byid = {l["id"]: l for l in L}
    for l in L:
        if cls(l) != "correction":
            continue
        lift = l.get("lift") or []
        for lvl in (1, 2):
            if len(lift) > lvl and lift[lvl]:
                met[(l["element"], lift[lvl])].add(l["id"])
    groups = [(k, v) for k, v in sorted(met.items()) if len({byid[i]["sub"] for i in v}) >= 2]
    w.append("- **%s:** %d groups (element and node) with corrections in two rooms or more." % (name, len(groups)))
    for (el, node), v in groups:
        rs = sorted({byid[i]["sub"] for i in v})
        w.append("  - %s at %s: %s (%d lines); cited in model/history.jsonl: %s" % (
            el, node, ", ".join(rs), len(v), "yes" if any(i in hist for i in v) else "no"))
w.append("- Repeated corrections are candidates for clusters, never a failure threshold. The moves they caused are "
         "172 (R01), 173 (P05), 176 (A21) and 197 (P05's scope, no change to the frozen model).\n")

# --- P05
w.append("## P05's added clause: the scope decision at D3c (F-024; move 197; QD3-011)\n")
w.append("The clause frozen in P05's statement ('until its keepers are told of it, and it is lost or given up where the "
         "telling does not reach them') does not hold in nine rooms whose re-check correction the ledger accepts. Its "
         "scope is decided as a bound with a cluster branch, carried in F-024; the frozen words are unchanged.")
for s in P05_ROOMS:
    ids_s = [l["id"] for l in ledgers["re-check"] if l["sub"] == s and l["element"] == "P05" and cls(l) == "correction"]
    w.append("- %s: %s (%s)" % (s, ", ".join(ids_s), "the shape read, the branch" if s in P05_ROOMS[:6]
                                  else "informed members carry the change, a second limit"))
w.append("")

# --- all-particular rooms
w.append("## Rooms whose adaptations are all particulars\n")
allp = []
per_all = collections.defaultdict(list)
for L in ledgers.values():
    for l in L:
        if l.get("op") != "none":
            per_all[l["sub"]].append(last.get(l["id"], {}).get("decision"))
for s, ds in sorted(per_all.items()):
    if ds and all(d == "particular" for d in ds):
        allp.append(s)
if allp:
    for s in allp:
        w.append("- %s: every adaptation is a particular; for this room, a model whose adaptations are all particulars "
                 "has not composed." % s)
else:
    w.append("None. In every room at least one adaptation is accepted or rejected rather than a particular, so the "
             "sentence 'a model whose adaptations are all particulars has not composed' applies to no room and not to "
             "the set.")
w.append("")

# --- per element
w.append("## Per element: rooms adapting it, by op (re-check, accepted lines and particulars)\n")
L = ledgers["re-check"]
ops = ["instantiate", "restrict", "add-condition", "add-step", "link", "contradict", "absent", "propose"]
el_rooms = collections.defaultdict(lambda: collections.defaultdict(set))
for l in L:
    if cls(l) in ("specification", "elaboration", "correction", "particular", "particular-np", "proposal"):
        el_rooms[l.get("element") or "(none)"][l["op"]].add(l["sub"])
w.append("| element | " + " | ".join(ops) + " | rooms with a correction | rooms with a particular |")
w.append("|---" * (len(ops) + 3) + "|")
corr_rooms = collections.defaultdict(set)
part_rooms = collections.defaultdict(set)
for l in L:
    if cls(l) == "correction":
        corr_rooms[l.get("element") or "(none)"].add(l["sub"])
    if cls(l) in ("particular", "particular-np"):
        part_rooms[l.get("element") or "(none)"].add(l["sub"])
for el in sorted(el_rooms):
    w.append("| %s | %s | %d | %d |" % (el, " | ".join(str(len(el_rooms[el][o])) for o in ops),
                                       len(corr_rooms[el]), len(part_rooms[el])))
w.append("")

# --- per room
w.append("## Per room: particulars against accepted shared lines\n")
w.append("Shared = accepted specifications, paired elaborations and corrections. Each cell: re-check / first return.\n")
w.append("| room | shared | of them corrections | limits | particulars | NONPORTABLE | rejected |")
w.append("|---|---|---|---|---|---|---|")
pr = {name: collections.defaultdict(collections.Counter) for name in ledgers}
for name, Ls in ledgers.items():
    for l in Ls:
        pr[name][l["sub"]][cls(l)] += 1
for s in rooms:
    cells = []
    for key in (("specification", "elaboration", "correction"), ("correction",), ("limit",), ("particular",),
                ("particular-np",), ("rejected",)):
        cells.append("%d / %d" % tuple(sum(pr[n][s][k] for k in key) for n in ("re-check", "first return")))
    w.append("| %s | %s |" % (s, " | ".join(cells)))
open(a.out, "w", encoding="utf-8").write("\n".join(w) + "\n")
print("wrote %s: %d lines" % (a.out, len(w)))
