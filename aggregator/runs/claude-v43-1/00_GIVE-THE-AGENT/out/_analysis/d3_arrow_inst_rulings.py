#!/usr/bin/env python3
"""Build an arrow's instantiate rulings from a spec file: one line per id, 'id|class|evidence'.

Classes (G33's readings for an arrow of kind order, FROM -> TO):
  O      the FROM act comes before the TO act (or the TO act names a FROM act already made): accept, specification
  J+     a joint opening (FROM and TO in one post) followed by a later TO act gathering around the mark: accept, specification
  J      a lone joint opening: reject
  BOUND  the TO act comes first, the arrow's bound: reject
  ONE    only one end is shown: reject
  OTHER  the evidence names its own reason in full: reject
Each ruling's reason is the evidence written for that id plus the class's clause, so every id carries its own reason.
The script refuses an id the packet does not hold, a repeated id, or a packet id the spec lacks.

  python3 out/_analysis/d3_arrow_inst_rulings.py --element A02 --spec out/_analysis/d3_rulings/A02-inst-spec.txt \
      --out out/_analysis/d3_rulings/A02-inst.jsonl --rule G33 --total 215
"""
import argparse
import json
import subprocess
import sys

CLAUSE = {
    "O": ("accept", "a start or proposal comes before the call, or the call names a start already made, so {el}'s order is shown; a specification"),
    "J+": ("accept", "a joint opening (the proposal and the call in one post) followed by a later call that gathers around the mark, so {el}'s mechanism is shown across turns; the census counts the joint opening apart; a specification"),
    "J": ("reject", "a joint opening, the proposal and the call in one post, with no later call gathering around the mark; {el}'s order cannot be shown, and the census counts the joint opening apart"),
    "BOUND": ("reject", "the first call names no mark and comes before the proposal, the bound's pattern ('the proposal answers the call instead'); {el}'s order is not shown"),
    "ONE": ("reject", "no call for hands is shown, only a start or proposal and joins; {el}'s order is not shown"),
    "OTHER": ("reject", "{el}'s order is not shown"),
}


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
    ap.add_argument("--out", required=True)
    ap.add_argument("--rule", required=True)
    ap.add_argument("--total", type=int, required=True)
    a = ap.parse_args()
    ids = packet_ids(a.element, a.total)
    if len(ids) != a.total:
        sys.exit(f"packet holds {len(ids)} ids, expected {a.total}")
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
            sys.exit(f"spec line {n}: {aid} is not in the packet")
        if aid in seen:
            sys.exit(f"spec line {n}: {aid} repeated")
        if cls not in CLAUSE:
            sys.exit(f"spec line {n}: class {cls!r}")
        seen.add(aid)
        dec, clause = CLAUSE[cls]
        reason = f"{a.rule}: {ev}; {clause.format(el=a.element)}"
        row = {"adaptation": aid, "decision": dec, "reason": reason}
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
