"""D3b: the before-and-after of the rooms the re-check returned (stage section 5). Counts only; nothing is written.

Before: the first return (adaptations.jsonl, verdicts-D.jsonl: the readers' agreed verdict, or my ruling where they
split). After: the re-check (adaptations-recheck.jsonl, verdicts-recheck-D.jsonl, rooms/<sub>/model-D-recheck.md).
Reported for the rooms both returns hold: (1) room verdicts before and after; (2) the re-check readers' agreement;
(3) the labelers' local status and grade after; (4) lines by op before and after; (5) lines on the revised and
re-ruled elements by op, before and after; (6) the candidates' lines after, by op; (7) propose lines; (8) how many
re-check lines repeat a first-return line of the same room, element and op with the same cited codes."""
import collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
both = sorted({r["sub"] for r in new})
B = set(both)
old = [r for r in old if r["sub"] in B]
print("rooms in both returns: %d" % len(both))

# (1) verdicts
vb = {}
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst":
        vb[r["sub"]] = r["verdict"]
    elif r["sub"] not in vb:
        vs = {e.get("verdict") for e in r.get("readers", [])}
        vb[r["sub"]] = vs.pop() if len(vs) == 1 else "split"
va, agree = {}, collections.Counter()
for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")):
    vs = [e.get("verdict") for e in r.get("readers", [])]
    s = set(vs)
    va[r["sub"]] = s.pop() if len(s) == 1 else "split:" + "/".join(sorted(set(vs)))
    agree["agree" if len(set(vs)) == 1 else "split"] += 1
print("(1) room verdict before -> after (rooms in both returns with a re-check verdict):")
tr = collections.Counter((vb.get(s), va.get(s)) for s in both if s in va)
for (b, a), n in sorted(tr.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
    print("   %-24s -> %-48s %d" % (b, a, n))
print("(2) re-check readers over all %d verdict rooms: %s" % (sum(agree.values()), dict(agree)))
allr = collections.Counter(e.get("verdict") for r in jl(os.path.join(OUT, "verdicts-recheck-D.jsonl")) for e in r.get("readers", []))
print("    reader lines by verdict:", dict(allr))

# (3) local status and grade
st, gr = collections.Counter(), collections.Counter()
for s in both:
    t = open(os.path.join(OUT, "rooms", s, "model-D-recheck.md"), encoding="utf-8").read()
    m = re.search(r"local_status:\s*(validated|unresolved|insufficient-evidence)", t)
    st[m.group(1) if m else None] += 1
    g = re.findall(r"\b(composes-with-residue|does-not-compose|composes)\b", t[-3000:])
    gr[g[-1] if g else None] += 1
print("(3) labelers' local status after: %s; grade after: %s" % (dict(st), dict(gr)))

# (4) ops
print("(4) lines by op, before -> after:")
ob, oa = collections.Counter(r["op"] for r in old), collections.Counter(r["op"] for r in new)
for op in sorted(set(ob) | set(oa)):
    print("   %-14s %6d -> %6d" % (op, ob[op], oa[op]))
print("   all            %6d -> %6d" % (len(old), len(new)))

# (5) revised and re-ruled elements
for e in ("R01", "P05", "P21", "P22", "A21", "P06", "R02", "K03", "K04", "P19"):
    b = collections.Counter(r["op"] for r in old if r.get("element") == e)
    a = collections.Counter(r["op"] for r in new if r.get("element") == e)
    print("(5) %s: before %s; after %s" % (e, dict(sorted(b.items())), dict(sorted(a.items()))))

# (6) candidates
cand = ["P%d" % n for n in range(23, 35)] + ["K05", "K06", "K07"]
for e in cand:
    a = collections.Counter(r["op"] for r in new if r.get("element") == e)
    rooms = len({r["sub"] for r in new if r.get("element") == e and r["op"] != "absent"})
    print("(6) %s after: %s; rooms with a line that is not absent: %d" % (e, dict(sorted(a.items())), rooms))

# (7) propose
print("(7) propose lines: before %d in %d rooms; after %d in %d rooms" % (
    ob["propose"], len({r["sub"] for r in old if r["op"] == "propose"}),
    oa["propose"], len({r["sub"] for r in new if r["op"] == "propose"})))


# (8) repeats
def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return frozenset(str(c).split(":")[-1] for c in ev)


ok = collections.defaultdict(set)
for r in old:
    ok[(r["sub"], r.get("element"), r["op"])].add(codes(r))
rep_same = sum(1 for r in new if codes(r) in ok.get((r["sub"], r.get("element"), r["op"]), set()))
rep_key = sum(1 for r in new if (r["sub"], r.get("element"), r["op"]) in ok)
print("(8) re-check lines whose room, element and op a first-return line shares: %d; with the same cited codes too: %d; of %d"
      % (rep_key, rep_same, len(new)))
