"""D3b: how D3a ruled the first return, by op (and by observation for absent lines), and how many re-check lines
repeat a first-return line under four keys. Counts only; nothing is written."""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
prof = collections.Counter()
for l in old:
    d = last.get(l["id"], {})
    key = l["op"] + ((":" + str(l.get("observation"))) if l["op"] == "absent" else "")
    prof[(key, d.get("decision"), d.get("kind"))] += 1
print("D3a rulings by op (absent by observation), decision and kind:")
for k, n in sorted(prof.items(), key=lambda x: (x[0][0], -x[1])):
    print("   %-28s %-11s %-14s %6d" % (k[0], k[1], k[2], n))


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return frozenset(str(c).split(":")[-1] for c in ev)


def txt(r):
    return " ".join(str(r.get(k) or "") for k in ("condition", "statement", "relation")).strip().lower()


idx = collections.defaultdict(list)
for l in old:
    idx[(l["sub"], l.get("element"), l["op"])].append(l)
k_same_codes = collections.Counter()
k_same_all = collections.Counter()
k_obs = collections.Counter()
for r in new:
    cands = idx.get((r["sub"], r.get("element"), r["op"]), [])
    if any(codes(c) == codes(r) for c in cands):
        k_same_codes[r["op"]] += 1
    if any(codes(c) == codes(r) and txt(c) == txt(r) for c in cands):
        k_same_all[r["op"]] += 1
    if r["op"] == "absent" and any(c.get("observation") == r.get("observation") for c in cands):
        k_obs["absent"] += 1
tot = collections.Counter(r["op"] for r in new)
print("re-check lines by op: total; same room, element, op and codes; and the same condition, statement and relation text:")
for op in sorted(tot):
    print("   %-14s %6d %6d %6d" % (op, tot[op], k_same_codes[op], k_same_all[op]))
print("absent lines whose room and element had an absent line with the same observation: %d of %d" % (k_obs["absent"], tot["absent"]))
obs = collections.Counter(r.get("observation") for r in new if r["op"] == "absent")
print("re-check absent lines by observation:", dict(obs))
