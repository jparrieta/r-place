#!/usr/bin/env python3
"""D4: make one cut (stage D4 section 2): a branch named or a subform declared, from a spec, with its members read
from the ledger's key matrix, never from a list. The spec is a JSON file:
  {"id": "F01", "parent": null | "F..", "level": "third" | "fourth" | "dimension" | "target", "keys": [...],
   "name": "...", "what_it_changes": "...", "move": one of the eight, "why": "...", "ground": "keys" | "keys and material: ..."}
Members: the rooms holding every key in _views/rooms-x-adaptations.<level>.all.tsv (and, for a subform, in the
parent too). The kind field is the majority kind of the members' lines on the keys (adaptation_ledger.shared_lines),
reported and not relied on for add-condition, add-step and restrict (J after the D3c interview). Refuses: an id in
use or not F plus two or three digits; fewer members than the minimum group size (tree-D4.md, else 5); a name
holding a member's name; a key not in the matrix; a parent not declared, or a child key that does not inherit
every parent key. With --write: appends the branch to out/branches.jsonl, appends its stage-D4 line to
out/tier_history.jsonl (tier branch, the move, the leg, the ground), and writes out/forms/<id>.md once (members;
keys with every line's how sentence; elements the members carry unchanged; one representative concept per member
with its ladder; the mention graph among members from _views/relations.tsv). Never overwrites a form.

    python3 out/_analysis/d4_cut.py --spec out/_analysis/d4a01_cut_F01.json --leg D4a-01 [--write]
"""
import argparse, collections, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
V = os.path.join(OUT, "_views")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import distance  # noqa: E402
from adaptation_ledger import shared_lines  # noqa: E402

LEVEL = {"third": "3", "fourth": "4", "dimension": "dim", "target": "target"}
MOVES = {"asking questions", "focusing on puzzles", "dropping", "merging", "splitting", "relating", "contrasting",
         "sequencing", "developing working hypotheses", "dropping working hypotheses"}
HOSTILE = {"attacked-by", "attacked", "destroyed-carelessly"}
COOP = {"negotiated", "asked-help-from", "gave-help-to", "allied"}
ap = argparse.ArgumentParser()
ap.add_argument("--spec", required=True)
ap.add_argument("--leg", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
spec = json.load(open(a.spec, encoding="utf-8"))
for k in ("id", "parent", "level", "keys", "name", "what_it_changes", "move", "why", "ground"):
    if k not in spec:
        sys.exit("spec lacks %s" % k)
if not re.match(r"^F\d{2,3}$", spec["id"]):
    sys.exit("id %r is not F plus two or three digits" % spec["id"])
if spec["move"] not in MOVES:
    sys.exit("move %r is not one of the eight" % spec["move"])
lev = LEVEL[spec["level"]]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


branches = jl(os.path.join(OUT, "branches.jsonl"))
by_id = {b["id"]: b for b in branches}
if spec["id"] in by_id:
    sys.exit("%s is in branches.jsonl already; a recut takes a new id" % spec["id"])
tree = open(os.path.join(OUT, "tree-D4.md"), encoding="utf-8").read() if os.path.exists(os.path.join(OUT, "tree-D4.md")) else ""
m = re.search(r"minimum group size[^\d]{0,60}(\d+)", tree, re.I)
min_size = int(m.group(1)) if m else 5


def matrix(level):
    with open(os.path.join(V, "rooms-x-adaptations.%s.all.tsv" % level), encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")[1:]
        held = collections.defaultdict(set)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            for k, v in zip(head, parts[1:]):
                if v == "1":
                    held[k].add(parts[0])
    return set(head), held


cols, held = matrix(lev)
for k in spec["keys"]:
    if k not in cols:
        sys.exit("key %s is not a column of the level-%s matrix" % (k, lev))
members = set.intersection(*[held[k] for k in spec["keys"]])
t3_t4 = {mm: r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")) for mm in r.get("members") or []}
t4_d = {mm: r["id"] for r in jl(os.path.join(OUT, "dimensions.jsonl")) for mm in r.get("members") or []}
if spec["parent"]:
    par = by_id.get(spec["parent"])
    if not par:
        sys.exit("parent %s is not declared" % spec["parent"])
    members &= set(par["members"])
    for pk in par["keys"]:
        ok = False
        for ck in spec["keys"]:
            po, pt, pn = pk.split(":")
            co, ct, cn = ck.split(":")
            four = t3_t4.get(cn)
            nodes = {cn, "*"} | ({four} if four else set()) | ({t4_d.get(four or cn)} if t4_d.get(four or cn) else set())
            ok = ok or (po == co and pt == ct and pn in nodes)
        if not ok:
            sys.exit("no child key inherits the parent key %s" % pk)
members = sorted(members, key=str.lower)
if len(members) < min_size:
    sys.exit("%d members, below the minimum group size %d" % (len(members), min_size))
for mm in members:
    if mm.lower() in spec["name"].lower():
        sys.exit("the name holds the member %s" % mm)
SL = shared_lines(OUT)
key_lines = collections.defaultdict(list)
for l in SL:
    for k in spec["keys"]:
        op, el, node = k.split(":")
        if l["sub"] in members and l["op"] == op and l["element"] == el and distance.node_at(l, lev) == node:
            key_lines[k].append(l)
kinds = collections.Counter(l["kind"] for ls in key_lines.values() for l in ls)
kind = kinds.most_common(1)[0][0]
branch = {"id": spec["id"], "parent": spec["parent"], "level": spec["level"], "kind": kind, "keys": spec["keys"],
          "members": members, "name": spec["name"], "what_it_changes": spec["what_it_changes"], "since": a.leg,
          "kind_counts": dict(kinds), "kind_note": "majority kind of the members' lines on the keys; not relied on "
                                                 "for add-condition, add-step and restrict (J after the D3c interview)"}
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
th = {"t": t, "stage": "D4", "leg": a.leg, "tier": "branch", "id": spec["id"], "move": spec["move"],
      "event": "subform declared" if spec["parent"] else "branch named", "why": spec["why"], "ground": spec["ground"],
      "level": spec["level"], "keys": spec["keys"], "parent": spec["parent"], "members_n": len(members)}
# the form
LT, heldT = matrix("target")
inst = collections.Counter()
for k, s in heldT.items():
    if k.startswith("instantiate:"):
        inst[k.split(":")[1]] = len(s & set(members))
unchanged = sorted((e for e, n in inst.items() if n >= 0.8 * len(members)), key=lambda e: -inst[e])
rel = collections.defaultdict(collections.Counter)
ms = set(members)
with open(os.path.join(V, "relations.tsv"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("#") or line.startswith("room\t"):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[0] in ms and p[1] in ms and p[0] != p[1]:
            grp = "hostile" if p[3] in HOSTILE else "cooperative" if p[3] in COOP else p[3]
            rel[grp][p[3]] += 1
connected = set()
with open(os.path.join(V, "relations.tsv"), encoding="utf-8") as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[0] in ms and p[1] in ms and p[0] != p[1]:
            connected |= {p[0], p[1]}
F = ["# %s: %s" % (spec["id"], spec["name"]), "",
     "Generated by `_analysis/d4_cut.py` at %s from `branches.jsonl` and the ledger (the current ledger's shared "
     "lines). Level: %s. Parent: %s. Kind: %s (%s; %s). Ground: %s." % (
         a.leg, spec["level"], spec["parent"] or "none (the global model)", kind,
         ", ".join("%s %d" % kv for kv in kinds.most_common()), branch["kind_note"], spec["ground"]), "",
     "**What it changes.** %s" % spec["what_it_changes"], "",
     "## Members (%d)" % len(members), "", ", ".join(members), "", "## Keys, with every member line's how sentence", ""]
for k in spec["keys"]:
    F.append("### %s (%d lines)" % (k, len(key_lines[k])))
    F.append("")
    for l in sorted(key_lines[k], key=lambda x: (x["sub"].lower(), x["id"])):
        F.append("- %s (`%s`, %s, lift %s): %s" % (l["sub"], l["id"], l["kind"], "/".join(str(x) for x in l["lift"]),
                                                  l.get("how") or l.get("condition") or l.get("statement") or ""))
    F.append("")
F += ["## Elements the members carry unchanged", "",
      "Elements that 80%% or more of the members instantiate as specifications (any node): %s." % (
          ", ".join("%s (%d of %d)" % (e, inst[e], len(members)) for e in unchanged) or "none"), "",
      "## Representative concepts, with their ladder", ""]
seen = set()
for k in spec["keys"]:
    for l in sorted(key_lines[k], key=lambda x: (x["sub"].lower(), x["id"])):
        if l["sub"] in seen:
            continue
        codes = (l.get("evidence") or {}).get("codes") or []
        if codes:
            seen.add(l["sub"])
            F.append("- %s/%s: %s" % (l["sub"], codes[0], " -> ".join(str(x) for x in l["lift"])))
F += ["", "## The mention graph among members (`_views/relations.tsv`)", "",
      "%d of %d members name or are named by another member. Edges by kind: %s. Connectivity alone does not "
      "establish a coalition; this is a relational diagnostic only." % (
          len(connected), len(members), "; ".join("%s: %s" % (g, ", ".join("%s %d" % kv for kv in c.items()))
                                                  for g, c in sorted(rel.items())) or "none"), ""]
fp = os.path.join(OUT, "forms", "%s.md" % spec["id"])
print(json.dumps({k: (v if k != "members" else "%d rooms" % len(v)) for k, v in branch.items()}, ensure_ascii=False))
print("members:", ", ".join(members))
print("form: %d lines; unchanged elements: %s; members connected: %d" % (len(F), ", ".join(unchanged), len(connected)))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
if os.path.exists(fp):
    sys.exit("refusing to overwrite %s" % fp)
os.makedirs(os.path.join(OUT, "forms"), exist_ok=True)
with open(os.path.join(OUT, "branches.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(branch, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(th, ensure_ascii=False) + "\n")
open(fp, "w", encoding="utf-8").write("\n".join(F) + "\n")
print("wrote branch %s (%d members), its tier_history line and forms/%s.md" % (spec["id"], len(members), spec["id"]))
