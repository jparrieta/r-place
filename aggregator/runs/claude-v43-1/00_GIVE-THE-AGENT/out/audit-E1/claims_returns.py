#!/usr/bin/env python3
"""E1 section 1, claims against their evidence (E1b-04): the return's verdicts on the arrows each proposition rests
on, which claims.py (E1a) did not give, and the brackets each arrow's order test was read against. Prints JSON.

    python3 out/audit-E1/claims_returns.py > out/audit-E1/claims_returns.json

The rule, declared before the run (E1b-04):
- The return's lines on an arrow: every line of adaptations.jsonl and adaptations-recheck.jsonl whose `element` is the
  arrow, with its op; the ruling is the last line of adjudications.jsonl for that line id (`adaptation`), and its
  `decision`. Counted per arrow: lines, rooms, and accepted lines by op.
- Per proposition: its arrows, and the sum over them.
- The brackets: for each arrow, whether its record reads the order test against prior.md section 4's brackets (a
  `before_h73` field), against the onset contrast (an `early_late` field), and at held size (any field naming size).
"""
import collections, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def main():
    last = {}
    for a in jl("adjudications.jsonl"):
        last[a.get("adaptation")] = a.get("decision")
    lines = collections.defaultdict(list)
    for f in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
        for r in jl(f):
            if r.get("element"):
                lines[r["element"]].append((f, r.get("id"), r.get("sub"), r.get("op"), last.get(r.get("id"))))
    arrows = {a["id"]: a for a in jl("model/arrows.jsonl")}
    per = {}
    for aid, a in sorted(arrows.items()):
        L = lines.get(aid, [])
        acc = collections.Counter(op for _f, _i, _s, op, d in L if d == "accept")
        per[aid] = {"lines": len(L), "rooms": len({s for _f, _i, s, _o, _d in L}),
                    "decisions": dict(collections.Counter(str(d) for *_x, d in L)),
                    "accepted_by_op": dict(acc),
                    "bracket_h73": a.get("before_h73") is not None, "onset": a.get("early_late") is not None,
                    "held_size": any("size" in json.dumps(v).lower() for v in a.values())}
    props = []
    for p in jl("propositions.jsonl"):
        ids = [r if isinstance(r, str) else r.get("id") for r in (p.get("rests_on") or [])]
        ids = [i for i in ids if i in arrows]
        tot = collections.Counter()
        for i in ids:
            tot.update(per[i]["accepted_by_op"])
        props.append({"id": p["id"], "carried_by": p.get("carried_by"), "arrows": ids, "accepted_by_op": dict(tot),
                      "lines": sum(per[i]["lines"] for i in ids)})
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-04):")[1].strip(),
                      "arrows": per, "propositions": props}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
