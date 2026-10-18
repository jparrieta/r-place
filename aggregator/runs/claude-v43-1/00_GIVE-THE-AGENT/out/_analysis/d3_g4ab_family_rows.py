#!/usr/bin/env python3
"""D3a-11: write G4a backward re-rulings for one elaboration family, chosen by a regex over the latest reason.
Each row keeps the line's own evidence (the reason's text after 'read whole, G..: ' and before its last '; ')
and adds the tail that names where the model states the link or step. Refuses to overwrite a file, and prints
the ids chosen so that they can be checked before the batch writer runs.

  python3 out/_analysis/d3_g4ab_family_rows.py --element P03 --op link \
      --regex 'after a loss( or a move)? the room builds again' --tail "..." --out out/_analysis/d3_rulings/F.jsonl
"""
import argparse
import json
import os
import re
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--element", required=True)
    ap.add_argument("--op", required=True)
    ap.add_argument("--regex", required=True)
    ap.add_argument("--tail", required=True, help="the clause naming the model's statement, after the evidence")
    ap.add_argument("--lead", default="G4a applied backwards to links (QD3-004)")
    ap.add_argument("--exclude", default="", help="comma-separated ids to leave out")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"{a.out} exists; choose a new name")
    out = subprocess.run([sys.executable, "out/_analysis/d3_group_rulings.py", "--element", a.element, "--op", a.op],
                         capture_output=True, text=True).stdout
    skip = {x for x in a.exclude.split(",") if x}
    rows = []
    for ln in out.splitlines():
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < 6 or parts[2] != "accept" or parts[3] != "elaboration":
            continue
        i, pair, reason = parts[0], parts[4].replace("pair ", "").strip(), "|".join(parts[5:])
        if i in skip or not re.search(a.regex, reason):
            continue
        body = re.sub(r"^(re-ruled[^:]*: |read whole(, G\d+[a-z]?( and G\d+[a-z]?)*)?: )", "", reason)
        evidence = body.rsplit("; ", 1)[0]
        rows.append({"adaptation": i, "decision": "accept", "kind": "specification",
                     "reason": f"{a.lead}: re-ruled from elaboration (pair {pair}). {evidence}; {a.tail}"})
    with open(a.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows to {a.out}: {' '.join(r['adaptation'] for r in rows)}")


if __name__ == "__main__":
    main()
