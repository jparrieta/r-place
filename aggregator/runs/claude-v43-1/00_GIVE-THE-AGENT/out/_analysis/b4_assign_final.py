#!/usr/bin/env python3
"""B4a: out/assign_final.jsonl, every item of the analysed set with its standing placement (stage B4 sections 2 and 7,
J's classes of 12 October). Rewritten whole at each adjudication leg; the earlier file is kept as
assign_final.superseded-<utc>.jsonl.

  class 1   b3_classes.jsonl's placement (the two readers' list, equal to my B1 grouping); source "readers"
  class 2   b3_classes.jsonl's placement (the readers' list, then B1's other themes); source "b1_grouping_kept"
  ruled     the last ruling in disagreements.jsonl: its placement, or third_order [] and unresolved true; source "ruling"
  pending   a contested item (class 3, 4, 5) not yet ruled: third_order [], status "pending_adjudication"
Built from the corpus copies only (the gold placements and duplicates dropped, section 2); no line carries an agent or
a replicate. confidence is the ruling's, else "clear" when both readers were clear, else "arguable". support_by_theme
comes from the ruling, else from replicate 1's line and its records; B1's kept themes on a class-2 line carry no
reader's concepts and are listed under b1_themes_without_reader_support.
"""
import collections, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    cls = jl(os.path.join(OUT, "b3_classes.jsonl"))
    dp = os.path.join(OUT, "disagreements.jsonl")
    last = {}
    for d in (jl(dp) if os.path.exists(dp) else []):
        last["%s/%s" % (d["sub"], d["theme_id"])] = d
    lines = collections.defaultdict(dict)
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x["copy_kind"] == "corpus":
            lines["%s/%s" % (x["sub"], x["theme_id"])][x["replicate"]] = x
    recs = collections.defaultdict(list)
    for m in jl(os.path.join(OUT, "multiplacement_log.jsonl")):
        if m.get("copy_kind") == "corpus":
            recs[(m["batch"], m["position"])].append(m)

    def reader_support(x):
        s = x.get("third_order") or []
        rs = recs.get((x["batch"], x["position"]), [])
        sup = {}
        added = set()
        for m in rs:
            if m.get("additional") in s:
                sup[m["additional"]] = list(m.get("support_additional") or [])
                added |= set(sup[m["additional"]])
        if s:
            sup[s[0]] = [c for c in (x.get("support") or []) if c not in added] or list(x.get("support") or [])
        return sup

    rows, n = [], collections.Counter()
    for c in cls:
        key = "%s/%s" % (c["sub"], c["theme_id"])
        L = lines[key]
        conf = "clear" if all(L[r].get("confidence") == "clear" for r in (1, 2) if r in L) else "arguable"
        base = {"sub": c["sub"], "theme_id": c["theme_id"], "class": c["class"], "read": L[1].get("read") if 1 in L else None}
        if key in last:
            d = last[key]
            row = dict(base, third_order=[] if d["unresolved"] else d["ruling"], unresolved=d["unresolved"],
                       confidence=d["confidence"], source="ruling", taxonomy=d["taxonomy"], leg=d["leg"],
                       support_by_theme=d.get("support_by_theme") or {}, also_present=d.get("also_present") or {})
            n["ruled"] += 1
        elif c["class"] in (1, 2):
            sup = reader_support(L[1])
            row = dict(base, third_order=c["final"], confidence=conf,
                       source="b1_grouping_kept" if c["class"] == 2 else "readers",
                       support_by_theme={t: v for t, v in sup.items() if t in c["final"]},
                       also_present=L[1].get("also_present") or {})
            missing = [t for t in c["final"] if t not in sup]
            if missing:
                row["b1_themes_without_reader_support"] = missing
            n["class %d" % c["class"]] += 1
        else:
            row = dict(base, third_order=[], status="pending_adjudication", confidence=conf, source="pending")
            n["pending"] += 1
        if row.get("read") is None:
            row.pop("read")
        rows.append(row)
    print("assign_final: %d lines; %s" % (len(rows), dict(n)))
    if "--write" in sys.argv:
        p = os.path.join(OUT, "assign_final.jsonl")
        if os.path.exists(p):
            utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            os.rename(p, os.path.join(OUT, "assign_final.superseded-%s.jsonl" % utc))
        with open(p, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
