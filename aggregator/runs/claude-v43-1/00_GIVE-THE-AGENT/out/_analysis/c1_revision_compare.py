#!/usr/bin/env python3
"""C1, the revision rate (section 3): my re-decisions (out/_analysis/c1_revision/dec-*.json, one entry per sample
item: "codes" {theme: [concepts]} in my order, optional "bag" [themes recorded beside], "note") against the settled
line (assign_final.jsonl) and the current line (assignments_final.jsonl). Checks that every concept belongs to its
item and no concept serves two themes. Reports, against each line: items placed differently (the theme sets differ),
mean Jaccard on sets (notes-B2's agreement), primary agreement, and each difference by kind:
  same set, other order; my set adds a theme the line lacks; the line holds a theme mine lacks; both.
--write records out/_analysis/c1_revision/result.json.

    python3 out/_analysis/c1_revision_compare.py [--write]
"""
import argparse, glob, importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DIR = os.path.join(OUT, "_analysis", "c1_revision")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def jac(a, b):
    a, b = set(a), set(b)
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
    bpf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bpf)
    store = bpf.pk.Store(ROOT, OUT)
    sample = json.load(open(os.path.join(DIR, "sample.json"), encoding="utf-8"))["items"]
    dec = {}
    for p in sorted(glob.glob(os.path.join(DIR, "dec-*.json"))):
        for d in json.load(open(p, encoding="utf-8")):
            if d["item"] in dec:
                sys.exit("%s decided twice" % d["item"])
            if d["item"] not in sample:
                sys.exit("%s is not in the sample" % d["item"])
            s, t = d["item"].split(":")
            own = set(store.themes[(s, t)].get("code_ids") or [])
            seen = set()
            for th, cs in d["codes"].items():
                for c in cs:
                    if c not in own or c in seen:
                        sys.exit("%s: %s %s" % (d["item"], c, "not its concept" if c not in own else "used twice"))
                    seen.add(c)
            dec[d["item"]] = d
    lines = {"settled": {"%s:%s" % (r["sub"], r["theme_id"]): r.get("third_order") or [] for r in jl("assign_final.jsonl")},
             "current": {"%s:%s" % (r["sub"], r["theme_id"]): r.get("third_order") or [] for r in jl("assignments_final.jsonl")}}
    res = {"decided": len(dec), "of": len(sample), "against": {}}
    for name, line in lines.items():
        rows, js, prim, diff = [], [], 0, 0
        for it in sample:
            if it not in dec:
                continue
            mine, theirs = list(dec[it]["codes"]), line[it]
            js.append(jac(mine, theirs))
            prim += (mine[:1] == theirs[:1])
            if set(mine) != set(theirs) or mine[:1] != theirs[:1]:
                add = [x for x in mine if x not in theirs]
                lack = [x for x in theirs if x not in mine]
                kind = ("order" if not add and not lack else "adds" if add and not lack else "lacks" if lack and not add
                        else "both")
                diff += set(mine) != set(theirs)
                rows.append({"item": it, "mine": mine, "line": theirs, "kind": kind, "adds": add, "lacks": lack,
                             "primary_differs": mine[:1] != theirs[:1], "note": dec[it].get("note")})
        n = len(js)
        res["against"][name] = {"n": n, "sets_differ": diff, "rate": round(diff / n, 3) if n else None,
                                "mean_jaccard": round(sum(js) / n, 3) if n else None,
                                "primary_agree": round(prim / n, 3) if n else None, "rows": rows}
        print("against the %s line: %d decided; %d placed differently (%.1f%%); mean Jaccard %.3f; primary agreement %.3f"
              % (name, n, diff, 100.0 * diff / n if n else 0, sum(js) / n if n else 0, prim / n if n else 0))
        for r in rows:
            print("   %-28s %-5s mine %-26s line %-26s%s" % (r["item"], r["kind"], ",".join(r["mine"]) or "-",
                                                         ",".join(r["line"]) or "-", " (primary)" if r["primary_differs"] else ""))
    if a.write:
        json.dump(res, open(os.path.join(DIR, "result.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote out/_analysis/c1_revision/result.json")


if __name__ == "__main__":
    main()
