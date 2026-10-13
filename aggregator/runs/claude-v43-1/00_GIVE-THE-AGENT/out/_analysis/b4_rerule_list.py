#!/usr/bin/env python3
"""B4a-05: the work list for J's rulings of 13 October, rule (3): the ruled items in packets 1 to 4 whose ruling
holds a theme that no placement held (neither reading nor my B1 grouping).

Read-only on the ledgers. Writes one work file per packet:
    python3 out/_analysis/b4_rerule_list.py --packet 1 [--write]      (without --write: counts only)

Per item it shows the two readings blinded as A and B in the chunk's seeded order (index.tsv A_is_replicate), each
reading's themes with the concepts that reading cited (as b4_rule_append.py takes them), my B1 grouping, the old
ruling with its concepts per theme, the old why, and each dropped theme's concepts with label and words, whole.
"""
import argparse
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    pdir = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet)
    arep = {}
    for ln in open(os.path.join(pdir, "index.tsv"), encoding="utf-8").read().splitlines()[1:]:
        n, key, cl, ch, ar = ln.split("\t")
        arep[key] = int(ar)
    rows = [d for d in jl(os.path.join(OUT, "disagreements.jsonl")) if d.get("packet") == a.packet]
    lines = collections.defaultdict(dict)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            lines["%s/%s" % (x["sub"], x["theme_id"])][x["replicate"]] = x
    recs = collections.defaultdict(list)
    for m in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if m.get("copy_kind") == "corpus":
            recs[(m["batch"], m["position"])].append(m)
    codes = {}
    for c in jl(os.path.join(ROOT, "package", "store", "codes.jsonl")):
        codes[(c["sub"], c["code_id"])] = c

    def reading(key, rep):
        x = lines[key].get(rep)
        if not x:
            return {}
        s = x.get("third_order") or []
        rs = recs.get((x["batch"], x["position"]), [])
        added, prim = set(), set()
        res = collections.OrderedDict()
        for m in rs:
            added |= set(m.get("support_additional") or [])
            prim |= set(m.get("support_primary") or [])
        if s:
            res[s[0]] = sorted(prim or (set(x.get("support") or []) - added) or set(x.get("support") or []))
        for m in rs:
            t = m.get("additional")
            if t and t not in res:
                res[t] = sorted(set(m.get("support_additional") or []) - set(m.get("support_primary") or []))
        for t in s[1:]:
            res.setdefault(t, [])
        return res

    sel = []
    stats = collections.Counter()
    dropped_themes = collections.Counter()
    for d in rows:
        held = set(d["readers"][0]) | set(d["readers"][1]) | set(d.get("b1") or [])
        drop = [t for t in d["ruling"] if t not in held]
        if not drop:
            continue
        sel.append((d, drop, held))
        keep = [t for t in d["ruling"] if t in held]
        stats["items"] += 1
        if d["ruling"][0] in drop:
            stats["primary dropped"] += 1
        if not keep:
            stats["nothing left"] += 1
        for t in drop:
            dropped_themes[t] += 1
    print("packet %d: %s" % (a.packet, dict(stats)))
    print("dropped themes: %s" % dropped_themes.most_common(20))
    if not a.write:
        return
    wdir = os.path.join(OUT, "_adjudication-B4", "rerule-B4a-05")
    os.makedirs(wdir, exist_ok=True)
    out = []
    w = out.append
    w("# Re-ruling list, packet %d (J's rulings of 13 October, rule 3)\n" % a.packet)
    w("%d items whose ruling holds a theme no placement held. Readings blinded as A and B in the chunk's seeded order.\n" % len(sel))
    for d, drop, held in sel:
        key = "%s/%s" % (d["sub"], d["theme_id"])
        ar = arep.get(key, 1)
        ra, rb = reading(key, ar), reading(key, 3 - ar)
        w("## %d. %s, class %s\n" % (d["n"], key, d["class"]))
        w("- reading A: " + "; ".join("%s [%s]" % (t, " ".join(v)) for t, v in ra.items()))
        w("- reading B: " + "; ".join("%s [%s]" % (t, " ".join(v)) for t, v in rb.items()))
        w("- my B1: " + ", ".join(d.get("b1") or []))
        w("- old ruling: %s | %s%s%s | named_neither %s" % (
            ", ".join("%s (%d)" % (t, len(d["support_by_theme"].get(t, []))) for t in d["ruling"]) or "unresolved",
            d["taxonomy"], (" " + d["field"] + " of " + d["theme"]) if d.get("field") else "",
            (" | br " + d["boundary_ruling"]) if d.get("boundary_ruling") else "", d["named_neither"]))
        for t in d["ruling"]:
            w("  - %s%s: %s" % (t, " (DROPPED)" if t in drop else "", " ".join(d["support_by_theme"].get(t, []))))
        if d.get("also_present"):
            w("- also_present: " + "; ".join("%s [%s]" % (t, " ".join(v)) for t, v in d["also_present"].items()))
        w("- old why: " + str(d.get("why") or ""))
        for t in drop:
            for cid in d["support_by_theme"].get(t, []):
                c = codes.get((d["sub"], cid), {})
                w("  - %s %s | %s | %s" % (t, cid, c.get("first_order", ""), " ".join(str(c.get("text", "")).split())))
        w("")
    p = os.path.join(wdir, "packet-%02d.md" % a.packet)
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("wrote %s (%d lines)" % (os.path.relpath(p, ROOT), len(out)))


if __name__ == "__main__":
    main()
