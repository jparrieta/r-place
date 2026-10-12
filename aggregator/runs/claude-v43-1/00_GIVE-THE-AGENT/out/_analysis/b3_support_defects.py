#!/usr/bin/env python3
"""B3b: the lines behind the close-check's three refusals on the assembly of record, read one by one. Reads only.

  A  multiplacement records whose support_additional is empty or shares a concept with support_primary
     (checks/stage_B3.py: "no supporting concept of its own")
  B  multi lines whose `support` holds fewer distinct concepts than themes
  C  lines with no `multi` field
For A and B: does the added theme have any concept of its own (its records' support_additional minus the concepts the
records cite for the primary)? If yes, the material is spread and the record is loose; if no, the added
theme rests on the primary's concepts only, and the line is a candidate for reduction to its primary (section 3.1).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    raw = jl(os.path.join(OUT, "assign_raw.jsonl"))
    ml = jl(os.path.join(OUT, "multiplacement_log.jsonl"))
    recs = {}
    for i, m in enumerate(ml, 1):
        recs.setdefault((m["batch"], m["position"]), []).append((i, m))
    lines = {(x["batch"], x["position"]): (i, x) for i, x in enumerate(raw, 1)}
    flagged = {}
    for i, m in enumerate(ml, 1):
        sp, sa = set(m.get("support_primary") or []), set(m.get("support_additional") or [])
        if not sa or sa & sp:
            flagged.setdefault((m["batch"], m["position"]), set()).add("A")
    for (b, p), (i, x) in lines.items():
        s = x.get("third_order") or []
        if "multi" not in x:
            flagged.setdefault((b, p), set()).add("C")
        elif x.get("multi") and len(set(x.get("support") or [])) < len(set(s)):
            flagged.setdefault((b, p), set()).add("B")
    reduce_, loose = [], []
    for (b, p), kinds in sorted(flagged.items()):
        i, x = lines[(b, p)]
        s = x.get("third_order") or []
        out = "%s pos %d (assign_raw line %d) %s/%s %s %s [%s]" % (b, p, i, x["sub"], x["theme_id"], x["copy_kind"], s, "".join(sorted(kinds)))
        if kinds == {"C"}:
            print("C  " + out + ": %d theme(s), no multi field" % len(s)); continue
        rs = recs.get((b, p), [])
        # the primary's concepts are what the records cite for it; the line's `support` may hold every concept
        # cited on the line, the added themes' included, so it is not subtracted
        prim = set()
        for _, m in rs:
            prim |= set(m.get("support_primary") or [])
        own = {}
        for t in s[1:]:
            add = set()
            for _, m in rs:
                if m.get("additional") == t:
                    add |= set(m.get("support_additional") or [])
            own[t] = sorted(add - prim)
        verdict = "added theme(s) with no concept of their own: %s" % [t for t, v in own.items() if not v] if any(not v for v in own.values()) else "every added theme has a concept of its own"
        (reduce_ if any(not v for v in own.values()) else loose).append((b, p))
        print("%s  %s: records %s; support %s; own concepts of added themes %s -> %s" % (
            "".join(sorted(kinds)), out, [j for j, _ in rs], sorted(x.get("support") or []), own, verdict))
    print("lines flagged %d: no own concept (reduce candidates) %d, loose records only %d, no multi field %d" % (
        len(flagged), len(reduce_), len(loose), sum(1 for k in flagged.values() if k == {"C"})))


if __name__ == "__main__":
    main()
