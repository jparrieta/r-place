#!/usr/bin/env python3
"""E1 section 4, the reconstruction sample (E1c): thirty rooms by seed, stratified by branch and by verdict, drawn from
the ledgers alone, before any room is opened. Prints one JSON line per room ({"sub", "branch", "verdict"}).

    python3 out/audit-E1/reconstruction_draw.py > out/reconstruction-sample-E1.jsonl

The rule, declared before the run (E1c):
- A room's verdict: the first return's fixed-global verdict, ruled (both readers agreeing, else the analyst's D3 ruling
  on the split, the D3 line of verdicts-D.jsonl without `recheck`). Section 5 sets this verdict beside fidelity.
- A room's branch: the branch of branches.jsonl it is a member of with the fewest members (the most specific; ties by
  id), or "none".
- By verdict: does-not-compose takes every such room (1); cannot-tell 2; the other 27 go to composes and
  composes-with-residue in proportion to their counts, rounded.
- Within a verdict, the rooms are shuffled with random.Random(int(out/seed.txt, 16)), strata in the order
  does-not-compose, cannot-tell, composes, composes-with-residue. A first pass takes, in shuffled order, rooms whose
  branch no earlier pick holds, with "none" allowed until the sample holds round(30 x rooms in no branch / 705); a
  second pass fills any stratum still short, in the same order.
"""
import collections, json, os, random, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(l) for l in open(os.path.join(OUT, p), encoding="utf-8") if l.strip()]


def main():
    V = {}
    for v in jl("verdicts-D.jsonl"):
        if not v.get("stage"):
            rs = sorted({r.get("verdict") for r in v.get("readers") or []})
            V[v["sub"]] = rs[0] if len(rs) == 1 else None
    for v in jl("verdicts-D.jsonl"):
        if v.get("stage") == "D3" and not v.get("recheck") and v.get("verdict"):
            V[v["sub"]] = v["verdict"]
    B = jl("branches.jsonl")
    size = {b["id"]: len(b.get("members") or []) for b in B}
    branch = {}
    for b in sorted(B, key=lambda b: (size[b["id"]], b["id"])):
        for m in b.get("members") or []:
            branch.setdefault(m, b["id"])
    subs = sorted(V)
    for s in subs:
        branch.setdefault(s, "none")
    counts = collections.Counter(V[s] for s in subs)
    rest = 30 - counts["does-not-compose"] - 2
    n_c = round(rest * counts["composes"] / (counts["composes"] + counts["composes-with-residue"]))
    quota = {"does-not-compose": counts["does-not-compose"], "cannot-tell": 2, "composes": n_c,
             "composes-with-residue": rest - n_c}
    none_cap = round(30 * sum(1 for s in subs if branch[s] == "none") / len(subs))
    rnd = random.Random(int(open(os.path.join(OUT, "seed.txt")).read().split()[0], 16))
    pools = {}
    for v in ("does-not-compose", "cannot-tell", "composes", "composes-with-residue"):
        p = [s for s in subs if V[s] == v]
        rnd.shuffle(p)
        pools[v] = p
    picked, used, n_none = [], set(), 0
    for v, pool in pools.items():
        got = []
        for s in pool:
            if len(got) >= quota[v]:
                break
            b = branch[s]
            if b == "none":
                if n_none < none_cap:
                    got.append(s)
                    n_none += 1
            elif b not in used:
                got.append(s)
                used.add(b)
        for s in pool:
            if len(got) >= quota[v]:
                break
            if s not in got:
                got.append(s)
                n_none += branch[s] == "none"
        picked += [(s, v) for s in got]
    for s, v in picked:
        print(json.dumps({"sub": s, "branch": branch[s], "verdict": v}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
