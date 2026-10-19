#!/usr/bin/env python3
"""Build an arrow's instantiate rulings from a spec file ('id|class|evidence') and a clause file.

Version 2 of d3_arrow_inst_rulings.py (D3a-29): the classes and their clauses come from a JSON file,
{"CLASS": ["accept" or "reject", "clause with {el} for the arrow's id"], ...}, so each arrow's rule (G33, G34, ...)
words its own classes. An accepted class is a specification. Each ruling's reason is '<rule>: <evidence>; <clause>'.
The script refuses an id the packets do not hold, a repeated id, an unknown class, or a packet id the spec lacks.

  python3 out/_analysis/d3_arrow_inst_rulings_v2.py --element A01 --spec out/_analysis/d3_rulings/A01-inst-spec.txt \
      --clauses out/_analysis/d3_rulings/A01-inst-clauses.json --out out/_analysis/d3_rulings/A01-inst.jsonl \
      --rule G34 --total 276
"""
import argparse
import json
import subprocess
import sys


def packet_ids(element, total):
    ids = []
    for off in range(0, total, 100):
        out = subprocess.run([sys.executable, "out/_analysis/d3_packet.py", "--element", element, "--op", "instantiate",
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
    a = ap.parse_args()
    clauses = json.load(open(a.clauses))
    for c, (dec, _) in clauses.items():
        if dec not in ("accept", "reject"):
            sys.exit(f"clause {c}: decision {dec!r}")
    ids = packet_ids(a.element, a.total)
    if len(ids) != a.total:
        sys.exit(f"packets hold {len(ids)} ids, expected {a.total}")
    rows, seen, counts = [], set(), {}
    for n, ln in enumerate(open(a.spec), 1):
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        parts = ln.split("|", 2)
        if len(parts) != 3:
            sys.exit(f"spec line {n}: expected id|class|evidence")
        aid, cls, ev = (p.strip() for p in parts)
        ev = ev.replace('\\"', '"')
        if aid not in ids:
            sys.exit(f"spec line {n}: {aid} is not in the packets")
        if aid in seen:
            sys.exit(f"spec line {n}: {aid} repeated")
        if cls not in clauses:
            sys.exit(f"spec line {n}: class {cls!r}")
        seen.add(aid)
        dec, clause = clauses[cls]
        row = {"adaptation": aid, "decision": dec, "reason": f"{a.rule}: {ev}; {clause.format(el=a.element)}"}
        if dec == "accept":
            row["kind"] = "specification"
        rows.append(row)
        counts[cls] = counts.get(cls, 0) + 1
    missing = [i for i in ids if i not in seen]
    if missing:
        sys.exit(f"spec lacks {len(missing)} packet ids: {missing[:10]}")
    order = {i: k for k, i in enumerate(ids)}
    rows.sort(key=lambda r: order[r["adaptation"]])
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rulings to {a.out}; by class {counts}")


if __name__ == "__main__":
    main()
