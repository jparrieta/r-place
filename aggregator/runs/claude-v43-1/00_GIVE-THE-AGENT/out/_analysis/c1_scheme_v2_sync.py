#!/usr/bin/env python3
"""C1: write out/scheme_v2.jsonl as scheme_final.jsonl with every stage-C1 gate change of out/gate_history.jsonl
applied in order (theme, field, now), field for field (section 9). Themes created, split, merged, retired or moved to
rare at C1 are applied from out/_analysis/c1_tier_ops.jsonl when that file exists (each op also has its
tier_history.jsonl line). Deterministic: the file is rebuilt whole from the frozen scheme every time.

Prints what differs from scheme_final.jsonl. Dry run without --write.

    python3 out/_analysis/c1_scheme_v2_sync.py [--write]
"""
import copy, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    p = os.path.join(OUT, p)
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()] if os.path.exists(p) else []


def main():
    fz = jl("scheme_final.jsonl")
    rows = [copy.deepcopy(r) for r in fz]
    by = {r["id"]: r for r in rows}
    applied = []
    for g in jl("gate_history.jsonl"):
        if str(g.get("stage")) != "C1":
            continue
        r = by.get(g["theme"])
        if r is None:
            sys.exit("gate_history names %s, which the scheme lacks" % g["theme"])
        r[g["field"]] = g["now"]
        applied.append("%s.%s" % (g["theme"], g["field"]))
    for op in jl(os.path.join("_analysis", "c1_tier_ops.jsonl")):
        kind = op["op"]
        if kind == "create":
            if op["row"]["id"] in by:
                sys.exit("create: %s exists" % op["row"]["id"])
            rows.append(op["row"]); by[op["row"]["id"]] = op["row"]
        elif kind == "set":
            by[op["id"]][op["field"]] = op["value"]
        elif kind == "retire":
            rows = [r for r in rows if r["id"] != op["id"]]; by.pop(op["id"], None)
        else:
            sys.exit("unknown op %s" % kind)
        applied.append("%s %s" % (kind, op.get("id") or op["row"]["id"]))
    fkeys = set().union(*[set(r) for r in fz])
    filled = []
    for r in rows:
        for k in sorted(fkeys - set(r)):     # the 14 rare themes of scheme_final carry no floor: null, so every line has every field
            r[k] = None
            filled.append("%s.%s" % (r["id"], k))
    print("fields filled with null so every line carries every field: %d (%s)" % (len(filled), ", ".join(filled[:20])))
    fby = {x["id"]: x for x in fz}
    diff = [r["id"] for r in rows if r["id"] not in fby
            or {k: v for k, v in r.items() if not (v is None and k not in fby[r["id"]])} != fby[r["id"]]]
    print("scheme_v2: %d themes; changes applied %d (%s); themes differing from scheme_final %d (%s)" % (
        len(rows), len(applied), ", ".join(applied) or "none", len(diff), ", ".join(diff) or "none"))
    if "--write" in sys.argv:
        with open(os.path.join(OUT, "scheme_v2.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("wrote out/scheme_v2.jsonl")


if __name__ == "__main__":
    main()
