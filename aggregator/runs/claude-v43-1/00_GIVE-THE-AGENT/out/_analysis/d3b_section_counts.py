#!/usr/bin/env python3
"""D3b: the counts for notes-D3.md's D3b section, from the ledgers. Reads only; writes the list of corrections and
paired elaborations to --appendix (under out/_analysis/).

(1) The re-check lines by last ruling's decision and kind, and by op. (2) Rulings of this leg with a pair. (3) P05's
re-check lines accepted with kind none whose reason cites G61's reading 3 (the clause move 173 added, untested). (4)
The rooms whose D3a-56 verdict residue names a candidate (recheck-scope.json, 'verdict residue X'): in the first batch
or not; verdict before and re-check readers; whether the re-check names each residue candidate (an accepted line on it,
not absent, of kind specification, elaboration or correction). (5) The 18 contrasting rooms: the same, for any
candidate. (6) Appendix: every accepted re-check correction and paired elaboration, by element, with room, op, pair,
lifted fourth-order node and the line's statement.

    python3 out/_analysis/d3b_section_counts.py --appendix out/_analysis/d3b_appendix_elab.md
"""
import argparse, collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--appendix", required=True)
a = ap.parse_args()
if not os.path.abspath(a.appendix).startswith(os.path.join(OUT, "_analysis") + os.sep):
    raise SystemExit("--appendix must be under out/_analysis/")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
first = {r["sub"] for r in new}
adj = jl(os.path.join(OUT, "adjudications.jsonl"))
last = {}
for r in adj:
    last[r["adaptation"]] = r
els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
cands = {i for i, e in els.items() if e.get("status") == "candidate"}

# (1)
c, byop = collections.Counter(), collections.defaultdict(collections.Counter)
for l in new:
    r = last.get(l["id"])
    k = "%s/%s" % (r["decision"], r.get("kind")) if r else "unruled"
    c[k] += 1
    byop[l["op"]][k] += 1
print("(1) re-check lines %d by last ruling: %s" % (len(new), dict(sorted(c.items()))))
for op in sorted(byop):
    print("    %-14s %5d %s" % (op, sum(byop[op].values()), dict(sorted(byop[op].items()))))

# (2)
ids = {l["id"] for l in new}
paired = [r for r in adj if r.get("leg") == "D3b" and r.get("pair")]
print("(2) D3b rulings with a pair: %d (distinct re-check lines %d)" % (len(paired), len({r["adaptation"] for r in paired})))

# (3)
p05 = [l for l in new if l.get("element") == "P05"]
lim3 = [l for l in p05 if last.get(l["id"]) and last[l["id"]]["decision"] == "accept"
        and last[l["id"]].get("kind") in (None, "none") and "reading 3" in (last[l["id"]].get("reason") or "")]
print("(3) P05 re-check lines accepted as limits under G61's reading 3: %d in %d rooms (by op %s)" % (
    len(lim3), len({l["sub"] for l in lim3}), dict(collections.Counter(l["op"] for l in lim3))))

# verdicts
vb = {}
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst":
        vb[r["sub"]] = r["verdict"]
    elif r["sub"] not in vb:
        vs = {e.get("verdict") for e in r.get("readers", [])}
        vb[r["sub"]] = vs.pop() if len(vs) == 1 else "split"
va = {}
for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    vs = sorted({e.get("verdict") for e in r.get("readers", [])})
    va[r["sub"]] = vs[0] if len(vs) == 1 else "split " + "/".join(vs)


def names(s, x):
    for l in new:
        if l["sub"] == s and l.get("element") == x and l.get("op") != "absent":
            r = last.get(l["id"])
            if r and r["decision"] in ("accept", "modify") and r.get("kind") in ("specification", "elaboration", "correction"):
                return True
    return False


scope = json.load(open(os.path.join(OUT, "recheck-scope.json"), encoding="utf-8"))
res = {}
for s, items in scope["relying"].items():
    xs = sorted(i.split()[-1] for i in items if i.startswith("verdict residue "))
    if xs:
        res[s] = xs
inb = [s for s in res if s in first]
print("(4) rooms whose D3a-56 residue names a candidate: %d; in the first batch %d; pending %d" % (
    len(res), len(inb), len(res) - len(inb)))
tr = collections.Counter((vb.get(s), va.get(s)) for s in inb)
for (b, x), n in sorted(tr.items(), key=lambda t: str(t)):
    print("    %s -> %s: %d" % (b, x, n))
pairs = [(s, x) for s in inb for x in res[s]]
named = [(s, x) for s, x in pairs if names(s, x)]
print("    residue candidates in first-batch rooms: %d; named by the re-check: %d; not named: %s" % (
    len(pairs), len(named), ", ".join("%s %s" % p for p in pairs if p not in named) or "none"))

# (5)
con = scope["contrasting_cases"]
cb = [s for s in con if s in first]
print("(5) contrasting rooms: %d; in the first batch %d (%s); pending: %s" % (
    len(con), len(cb), ", ".join(cb), ", ".join(s for s in con if s not in first) or "none"))
for s in cb:
    xs = sorted(x for x in cands if names(s, x))
    print("    %s: verdict %s -> %s; candidates named: %s" % (s, vb.get(s), va.get(s), " ".join(xs) or "none"))

# (6)
rows = collections.defaultdict(list)
for l in new:
    r = last.get(l["id"])
    if not r or r["decision"] not in ("accept", "modify") or r.get("kind") not in ("correction", "elaboration"):
        continue
    lift = l.get("lift") or []
    text = next((t for t in (l.get("statement"), l.get("condition"), l.get("how")) if t and not re.fullmatch(r"t\d+|T\d-\d+", t)), "")
    rows[l["element"]].append((r["kind"], l["sub"], l["id"], l["op"], r.get("pair") or "", lift[2] if len(lift) > 2 else "",
                               text.replace("|", "/").replace("\n", " ")[:160]))
out = ["| Element | Kind | Room | Line | Op | Pair | Fourth-order node | The line's statement, condition or how |",
       "|---|---|---|---|---|---|---|---|"]
for e in sorted(rows):
    for k, s, i, op, p, n, st in sorted(rows[e], key=lambda t: (t[0], t[1].lower(), t[2])):
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (e, k, s, i, op, p, n, st))
open(a.appendix, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("(6) appendix: %d rows over %d elements (%s); wrote %s" % (
    len(out) - 2, len(rows), ", ".join("%s %d" % (e, len(v)) for e, v in sorted(rows.items())), a.appendix))
