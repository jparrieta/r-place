#!/usr/bin/env python3
"""D5b, section 4: each branch's ending in its own terms.

--themes: per branch, the fourth-order themes of the members' last coordinating codes and of
their aftermath coordinating codes (organizing_end-A1.jsonl), each against the population's,
by the share rule of d5_themes.py (a code split evenly over its nodes). Prints JSON.
--dump: one line per room in a branch with an aftermath coordinating code:
"sub | branches | code | hNN | first_order", sorted by case-ignored name.

    python3 out/_analysis/d5b_endings.py --themes
    python3 out/_analysis/d5b_endings.py --dump
"""
import argparse, collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STORE = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--themes", action="store_true")
ap.add_argument("--dump", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


t4, names = {}, {}
for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl")):
    names[r["id"]] = r.get("name")
    for m in r.get("members") or []:
        t4[m] = r["id"]
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    v = r.get("third_order") or []
    place[(r["sub"], r["theme_id"])] = [v] if isinstance(v, str) else list(v)
codes = {(r["sub"], r["code_id"]): r for r in jl(os.path.join(STORE, "codes.jsonl"))}
oe = {d["sub"]: d for d in jl(os.path.join(OUT, "organizing_end-A1.jsonl"))}
B = jl(os.path.join(OUT, "branches.jsonl"))
of = collections.defaultdict(list)
for b in B:
    for s in b["members"]:
        of[s].append(b["id"])


def nodes(sub, cid):
    c = codes.get((sub, cid))
    if not c:
        return []
    return [t4[x] for x in place.get((sub, c.get("theme_id")), []) if x in t4]


def tally(subs, field):
    c = collections.Counter()
    for s in subs:
        ids = oe[s].get(field) or []
        ids = [ids] if isinstance(ids, str) else ids
        for cid in ids:
            ns = nodes(s, cid)
            for n in ns:
                c[n] += 1 / len(ns)
    return c


if a.themes:
    allsubs = list(oe)
    pop_last, pop_aft = tally(allsubs, "last_coordinating_code"), tally(allsubs, "aftermath_coordinating_codes")
    out = []
    for b in B:
        row = {"branch": b["id"]}
        for key, pop in (("last_coordinating_code", pop_last), ("aftermath_coordinating_codes", pop_aft)):
            br = tally(b["members"], key)
            bt, pt = sum(br.values()), sum(pop.values())
            top = sorted(br.items(), key=lambda kv: -kv[1])[:4]
            row[key] = {"total": round(bt, 2), "top": [
                {"t4": k, "name": names.get(k), "count": round(v, 2), "share": round(v / bt, 3) if bt else None,
                 "pop_share": round(pop.get(k, 0) / pt, 3) if pt else None} for k, v in top]}
        out.append(row)
    print(json.dumps({"pop_last_top": [(k, names.get(k), round(v, 1)) for k, v in pop_last.most_common(5)],
                      "pop_aft_top": [(k, names.get(k), round(v, 1)) for k, v in pop_aft.most_common(5)],
                      "branches": out}, ensure_ascii=False))
if a.dump:
    for s in sorted(of, key=str.lower):
        ids = oe[s].get("aftermath_coordinating_codes") or []
        for cid in ids:
            c = codes.get((s, cid), {})
            print("%s | %s | %s | h%s | %s" % (s, " ".join(of[s]), cid, c.get("hour"), c.get("first_order")))
