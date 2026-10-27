#!/usr/bin/env python3
"""E1 section 3 (E1b-07): EXPECTATIONS.jsonl against the ledger and the verdicts; the field's entries; the onset
contrast's counts; the composition diagnostics. Prints JSON.

    python3 out/audit-E1/expectations.py > out/audit-E1/expectations.json

The rule, declared before the run (E1b-07):
- A room's evidence on an element: its return lines on that element (adaptations.jsonl and adaptations-recheck.jsonl),
  each with the last ruling in adjudications.jsonl; only accepted lines count. Taken up: an accepted instantiate,
  restrict, add-condition, add-step or link line. Contradicted: an accepted contradict line. Absent: an accepted absent
  line and nothing taken up. No line: none of these.
- An expectation to instantiate is met where the room took the element up; it fails where the room's only accepted
  word on it is absent (the first failure). An expectation of absence is met where the room did not take it up; it
  fails where it did (the second failure). No line is counted apart, as untested.
- The replication score: met over met and failed, by branch (branches.jsonl members; rooms in no branch apart) and by
  the first return's verdict (both readers' verdicts when they agree, else "split").
- The field's entries (sealed/FIELD.jsonl): rooms that took each up, contradicted it, left it absent or have no
  line, beside the same shares over the model's other standing elements and arrows.
- The onset contrast: each arrow's early_late counts as model/arrows.jsonl holds them, both sides' denominators first.
- Composition diagnostics: the first return's and the re-check's verdicts (verdicts-D.jsonl and the rooms'
  verdict-D-recheck.jsonl, by room folder); accepted particular lines and the rooms holding them; distinct shared
  changes, an accepted change (op other than instantiate or absent) on one element met in two or more rooms; their
  count as rooms are added in the A1 seeded reading order (out/_analysis/a1_order output if present, else by name),
  by thirds.
"""
import collections, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
TAKE = {"instantiate", "restrict", "add-condition", "add-step", "link", "specify"}


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def main():
    last = {}
    for a in jl("adjudications.jsonl"):
        last[a.get("adaptation")] = a.get("decision")
    ev = collections.defaultdict(lambda: collections.defaultdict(set))
    particular = collections.Counter()
    changes = collections.defaultdict(set)
    for f in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
        for r in jl(f):
            d = last.get(r.get("id"))
            if d == "particular":
                particular[r.get("sub")] += 1
            if d != "accept" or not r.get("element"):
                continue
            ev[r["sub"]][r["element"]].add(r.get("op"))
            if r.get("op") not in ("instantiate", "absent"):
                changes[(r["element"], r.get("op"))].add(r["sub"])
    def state(sub, el):
        ops = ev[sub].get(el, set())
        if ops & TAKE:
            return "taken up"
        if "contradict" in ops:
            return "contradicted"
        if "absent" in ops:
            return "absent"
        return "no line"
    branch_of = collections.defaultdict(list)
    for b in jl("branches.jsonl"):
        for m in b.get("members") or []:
            branch_of[m].append(b["id"])
    V = {}
    for v in jl("verdicts-D.jsonl"):
        if not v.get("stage"):
            rs = sorted({r.get("verdict") for r in v.get("readers") or []})
            V[v["sub"]] = rs[0] if len(rs) == 1 else "split"
    by_b, by_v = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    tot = collections.Counter()
    per_el = collections.defaultdict(collections.Counter)
    for e in jl("sealed/EXPECTATIONS.jsonl"):
        s = e["sub"]
        outs = []
        for el in e.get("expect_instantiate") or []:
            st = state(s, el)
            outs.append(("met" if st == "taken up" else "untested" if st == "no line" else "failed: absent where expected", el))
        for el in e.get("expect_absent") or []:
            st = state(s, el)
            outs.append(("failed: instantiated where absent was expected" if st == "taken up" else "untested" if st == "no line" else "met", el))
        for o, el in outs:
            tot[o] += 1
            per_el[el][o] += 1
            for b in branch_of.get(s) or ["no branch"]:
                by_b[b][o] += 1
            by_v[V.get(s, "none")][o] += 1
    def score(c):
        met = c["met"]
        failed = sum(v for k, v in c.items() if k.startswith("failed"))
        return round(met / (met + failed), 3) if met + failed else None
    R = {"expectations": {"total": dict(tot), "score": score(tot),
                          "by_branch": {k: {**dict(v), "score": score(v)} for k, v in sorted(by_b.items())},
                          "by_verdict": {k: {**dict(v), "score": score(v)} for k, v in sorted(by_v.items())},
                          "by_element": {k: {**dict(v), "score": score(v)} for k, v in sorted(per_el.items())}}}
    els = [x for x in jl("model/elements.jsonl") + jl("model/arrows.jsonl") if x.get("status") == "standing"]
    subs = sorted({e["sub"] for e in jl("sealed/EXPECTATIONS.jsonl")})
    def shares(el):
        c = collections.Counter(state(s, el) for s in subs)
        return {k: c[k] for k in ("taken up", "contradicted", "absent", "no line")}
    field = {f["id"]: shares(f["id"]) for f in jl("sealed/FIELD.jsonl")}
    others = collections.Counter()
    for x in els:
        if x["id"] not in field:
            others.update(shares(x["id"]))
    n_other = len([x for x in els if x["id"] not in field])
    R["field"] = {"entries": field, "other_standing_elements_and_arrows": n_other,
                  "their_mean": {k: round(v / n_other, 1) for k, v in others.items()} if n_other else None}
    R["onset"] = {a["id"]: a.get("early_late") for a in jl("model/arrows.jsonl")}
    rc = collections.defaultdict(list)
    for p in glob.glob(os.path.join(OUT, "rooms", "*", "verdict-D-recheck.jsonl")):
        for l in open(p, encoding="utf-8"):
            if l.strip():
                rc[os.path.basename(os.path.dirname(p))].append(json.loads(l).get("verdict"))
    rcv = {s: (sorted(set(v))[0] if len(set(v)) == 1 else "split") for s, v in rc.items()}
    ruled1, ruled2 = dict(V), dict(rcv)  # the analyst's D3 rulings settle the split rooms (recheck true: the re-check's)
    for v in jl("verdicts-D.jsonl"):
        if v.get("stage") == "D3" and v.get("verdict"):
            (ruled2 if v.get("recheck") else ruled1)[v["sub"]] = v["verdict"]
    R["verdicts"] = {"first_return_readers": dict(collections.Counter(V.values())),
                     "recheck_readers": dict(collections.Counter(rcv.values())),
                     "first_return_ruled": dict(collections.Counter(ruled1.values())),
                     "recheck_ruled": dict(collections.Counter(ruled2.values()))}
    shared = {k: len(v) for k, v in changes.items() if len(v) >= 2}
    R["particulars"] = {"lines": sum(particular.values()), "rooms": len(particular)}
    R["distinct_shared_changes"] = len(shared)
    R["changes_in_one_room_only"] = sum(1 for v in changes.values() if len(v) == 1)
    order = subs
    op = os.path.join(OUT, "_analysis", "a1_order-A1.txt")  # the first run looked for a .json that does not exist
    if os.path.exists(op):
        seq = []
        for line in open(op, encoding="utf-8"):
            if line.startswith("block ") and "rooms: " in line:
                seq += [x.strip() for x in line.split("rooms: ", 1)[1].split(",") if x.strip()]
        if len(seq) == len(subs):
            order = seq
    seen, curve, room_set = set(), [], collections.defaultdict(set)
    for i, s in enumerate(order, 1):
        for el, ops in ev[s].items():
            for o in ops:
                if o not in ("instantiate", "absent"):
                    room_set[(el, o)].add(s)
                    if len(room_set[(el, o)]) == 2:
                        seen.add((el, o))
        if i in (len(order) // 3, 2 * len(order) // 3, len(order)):
            curve.append((i, len(seen)))
    R["shared_change_curve_by_thirds"] = curve
    R["order_source"] = "a1_order.json" if order is not subs else "by name"
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-07):")[1].strip(), **R},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
