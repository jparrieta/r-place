#!/usr/bin/env python3
"""Build an arrow's restrict rulings from a spec file ('id|class|evidence[|pair]') and a clause file.

Version 2 of d3_arrow_restrict_rulings.py (D3a-29): the classes and clauses come from a JSON file,
{"CLASS": ["accept" or "particular" or "reject", kind or null, "clause with {el}"], ...}, so each arrow's rule
words its own classes. A class whose kind is "correction" needs a pair (the fourth field). Each ruling's reason is
'<rule>: <evidence>; <clause>'. The script refuses an id the packets do not hold, a repeat, an unknown class, or a
packet id the spec lacks.

  python3 out/_analysis/d3_arrow_restrict_rulings_v2.py --element A01 --spec out/_analysis/d3_rulings/A01-restrict-spec.txt \
      --clauses out/_analysis/d3_rulings/A01-restrict-clauses.json --out out/_analysis/d3_rulings/A01-restrict.jsonl \
      --rule "G34 and G9" --total 115
"""
import argparse
import json
import subprocess
import sys


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
        if kind == "correction":
            if len(parts) != 4:
                sys.exit(f"spec line {n}: a correction needs a pair")
            row["pair"] = parts[3]
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
