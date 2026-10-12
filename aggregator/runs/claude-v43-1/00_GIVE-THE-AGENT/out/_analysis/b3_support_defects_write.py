#!/usr/bin/env python3
"""B3b: append to out/defects.jsonl one line per assign_raw line behind the close-check's three refusals on the
assembly of record (QB3-005): loose multiplacement support (support_additional sharing a concept with
support_primary), a multi line whose `support` lists fewer concepts than themes, a line with no `multi` field. Each
added theme has a concept of its own (b3_support_defects.py), so none is reduced to its primary. Appends once."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
KIND = {"A": "multiplacement support_additional shares a concept with support_primary",
        "B": "multi line whose support lists fewer distinct concepts than themes",
        "C": "line with no multi field"}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    raw = jl(os.path.join(OUT, "assign_raw.jsonl"))
    ml = jl(os.path.join(OUT, "multiplacement_log.jsonl"))
    flag = {}
    for m in ml:
        sp, sa = set(m.get("support_primary") or []), set(m.get("support_additional") or [])
        if not sa or sa & sp:
            flag.setdefault((m["batch"], m["position"]), set()).add("A")
    for x in raw:
        if "multi" not in x:
            flag.setdefault((x["batch"], x["position"]), set()).add("C")
        elif x.get("multi") and len(set(x.get("support") or [])) < len(set(x.get("third_order") or [])):
            flag.setdefault((x["batch"], x["position"]), set()).add("B")
    rows = []
    for i, x in enumerate(raw, 1):
        k = flag.get((x["batch"], x["position"]))
        if not k:
            continue
        rows.append({"stage": "B3", "leg": "B3b", "kind": "reader's record slip: " + "; ".join(KIND[c] for c in sorted(k)),
                     "assign_raw_line": i, "batch": x["batch"], "agent": x["agent"], "replicate": x["replicate"],
                     "position": x["position"], "item": "%s/%s" % (x["sub"], x["theme_id"]), "copy_kind": x["copy_kind"],
                     "third_order": x.get("third_order"), "reduced_to_primary": False,
                     "note": "every added theme has a concept of its own; kept as given; waiver asked at QB3-005"})
    p = os.path.join(OUT, "defects.jsonl")
    if any(str(d.get("kind", "")).startswith("reader's record slip") for d in jl(p)):
        sys.exit("defects.jsonl already holds these lines")
    print("%d lines" % len(rows))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("defects.jsonl now %d lines" % len(jl(p)))


if __name__ == "__main__":
    main()
