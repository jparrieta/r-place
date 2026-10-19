#!/usr/bin/env python3
"""Build an arrow's restrict rulings from a spec file: one line per id, 'id|class|evidence[|pair]'.

Classes, by G9 read for an arrow and G33's amendment (D3a-28):
  S-O      the concepts show the order: accept, specification (the condition is held)
  S-J+     a joint opening with a later call around the mark: accept, specification
  S-BOUND  the bound's pattern: accept, specification (held by the bound)
  EL       only a joint opening, or the order cannot be read: accept, kind none (an evidence limit)
  C        a condition the arrow and its bound lack, with the order failing without it: accept, correction, pair required
  P-LOCAL  a correction with no second room meeting it: particular
  P-G6     the line fails portability: particular (G6)
Every id carries its own evidence; the script refuses an id the packets do not hold, a repeat, or a packet id the spec lacks.

  python3 out/_analysis/d3_arrow_restrict_rulings.py --element A02 --spec ... --out ... --rule "G33 and G9" --total 134
"""
import argparse
import json
import subprocess
import sys

CLAUSE = {
    "S-O": ("accept", "specification", "the concepts show the order, so the condition does not make {el} fail here and the connection holds it; a specification"),
    "S-J+": ("accept", "specification", "a joint opening followed by a later call around the mark: the condition, that the start and the first call can be one post, is held by the connection and does not make {el} fail (G33's amendment); a specification"),
    "S-BOUND": ("accept", "specification", "the first call comes before any proposal, the bound's pattern, so the condition is held by {el}'s bound; a specification"),
    "EL": ("accept", "none", "the concepts show only a joint opening, or no order can be read; the condition is held by the connection, a joint opening neither meets the order nor {el}'s mechanism_fails_if (G33's amendment), so this is an evidence limit"),
    "C": ("accept", "correction", "a condition {el} and its bound lack, with the order failing without it; a correction"),
    "P-LOCAL": ("particular", None, "a correction that no second room's line meets, kept as this room's particular (G4 and G5)"),
    "P-G6": ("particular", None, "the line fails portability, a particular (G6)"),
}


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
    ap.add_argument("--out", required=True)
    ap.add_argument("--rule", required=True)
    ap.add_argument("--total", type=int, required=True)
    ap.add_argument("--op", default="restrict")
    a = ap.parse_args()
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
        if aid not in ids or aid in seen or cls not in CLAUSE:
            sys.exit(f"spec line {n}: bad id, repeat or class ({aid}, {cls})")
        seen.add(aid)
        dec, kind, clause = CLAUSE[cls]
        row = {"adaptation": aid, "decision": dec}
        if kind:
            row["kind"] = kind
        if cls == "C":
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
