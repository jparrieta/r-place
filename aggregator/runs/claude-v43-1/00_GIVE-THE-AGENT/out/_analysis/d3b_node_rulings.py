#!/usr/bin/env python3
"""Print the propose lines lifted to one third-order node, with their last ruling (read-only).

Reads out/adaptations.jsonl (first return) and out/adaptations-recheck.jsonl,
keeps the lines whose JSON names the node, and prints each id, room, the
line's statement and the last ruling in out/adjudications.jsonl (decision,
kind and the head of the reason). Used to rule a re-check propose line as
the other rooms' lines at the same node were ruled.

usage: python3 out/_analysis/d3b_node_rulings.py --node T3-131 [--reason-chars 300]
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "out"


def load_last_rulings():
    last = {}
    with open(OUT / "adjudications.jsonl", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            aid = rec.get("adaptation")
            if aid:
                last[aid] = rec
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", required=True)
    ap.add_argument("--reason-chars", type=int, default=300)
    ap.add_argument("--all-ops", action="store_true",
                    help="print every op lifted to the node, not only propose")
    args = ap.parse_args()
    last = load_last_rulings()
    for name in ("adaptations.jsonl", "adaptations-recheck.jsonl"):
        path = OUT / name
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if args.node not in line:
                    continue
                rec = json.loads(line)
                if args.node not in (rec.get("lift") or []):
                    continue
                if not args.all_ops and rec.get("op") != "propose":
                    continue
                aid = rec.get("id")
                r = last.get(aid)
                stmt = rec.get("statement") or ""
                if r is None:
                    ruling = "UNRULED"
                else:
                    ruling = "%s/%s pair=%s | %s" % (
                        r.get("decision"), r.get("kind"), r.get("pair"),
                        (r.get("reason") or "")[: args.reason_chars])
                print("%s  %s  %s  [%s]" % (aid, rec.get("sub"), rec.get("op"), name))
                print("   statement: %s" % stmt)
                print("   ruling: %s" % ruling)
                print()


if __name__ == "__main__":
    main()
