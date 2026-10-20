#!/usr/bin/env python3
"""Build an arrow's restrict rulings from a spec file ('id|class|evidence[|pair]') and a clause file.

Version 3 of d3_arrow_restrict_rulings.py (D3a-34). As version 2, except that a class whose kind is "elaboration"
also needs a pair (the fourth field), as G4a's last clause rules a paired elaboration; version 2 wrote a pair only for
a correction. A pair must name another room's id among the packets. Each ruling's reason is
'<rule>: <evidence>; <clause>'. The script refuses an id the packets do not hold, a repeat, an unknown class, a
pair on a class that takes none, or a packet id the spec lacks.

  python3 out/_analysis/d3_arrow_restrict_rulings_v3.py --element A07 --spec out/_analysis/d3_rulings/A07-restrict-spec-105.txt \
      --clauses out/_analysis/d3_rulings/A07-restrict-clauses.json --out out/_analysis/d3_rulings/A07-restrict.jsonl \
      --rule "G39 and G9" --total 105
"""
import argparse
import json
import subprocess
import sys

PAIRED = ("correction", "elaboration")


def packet_ids(element, op, total):
    ids = []
    for off in range(0, total, 100):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element, "--op", op,
                              "--offset", str(off), "--limit", str(min(100, total - off))],
                             capture_output=True, text=True).stdout
        ids += [blk.split("\n", 1)[0].split()[0] for blk in out.split("\n== ")[1:]]
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--clauses", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rule", required=True)
    ap.add_argument("--total", type=int, required=True)
    ap.add_argument("--op", default="restrict")
    a = ap.parse_args()
    clauses = json.load(open(a.clauses))
    for c, (dec, kind, _) in clauses.items():
        if dec not in ("accept", "particular", "reject"):
            sys.exit(f"clause {c}: decision {dec!r}")
    ids = packet_ids(a.element, a.op, a.total)
    if len(ids) != a.total:
        sys.exit(f"packets hold {len(ids)} ids, expected {a.total}")
    rows, seen, counts = [], set(), {}
    for n, ln in enumerate(open(a.spec), 1):
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) not in (3, 4):
            sys.exit(f"spec line {n}: expected id|class|evidence[|pair]")
        aid, cls, ev = parts[0], parts[1], parts[2].replace('\\"', '"')
        if aid not in ids or aid in seen or cls not in clauses:
            sys.exit(f"spec line {n}: bad id, repeat or class ({aid}, {cls})")
        seen.add(aid)
        dec, kind, clause = clauses[cls]
        row = {"adaptation": aid, "decision": dec}
        if kind:
            row["kind"] = kind
        if kind in PAIRED:
            if len(parts) != 4:
                sys.exit(f"spec line {n}: a {kind} needs a pair")
            pair = parts[3]
            if pair not in ids or pair.rsplit("-", 1)[0] == aid.rsplit("-", 1)[0]:
                sys.exit(f"spec line {n}: pair {pair!r} is not another room's line in the packets")
            row["pair"] = pair
        elif len(parts) == 4:
            sys.exit(f"spec line {n}: class {cls} takes no pair")
        row["reason"] = f"{a.rule}: {ev}; {clause.format(el=a.element)}"
        rows.append(row)
        counts[cls] = counts.get(cls, 0) + 1
    missing = [i for i in ids if i not in seen]
    if missing:
        sys.exit(f"spec lacks {len(missing)} ids: {missing[:10]}")
    order = {i: k for k, i in enumerate(ids)}
    rows.sort(key=lambda r: order[r["adaptation"]])
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rulings to {a.out}; by class {counts}")


if __name__ == "__main__":
    main()
