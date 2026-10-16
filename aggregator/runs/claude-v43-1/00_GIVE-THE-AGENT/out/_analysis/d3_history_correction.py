#!/usr/bin/env python3
"""Append one correction line to out/model/history.jsonl, changing no element.

Used when a history line already written carries a slip (a move misnamed): the earlier lines
stay, and this line records the correction with its date, leg and reason. The spec is a JSON
file: {"id", "event", "move", "why", "field", "now", "was", "corrects_lines"}. Without --write it
prints the line and writes nothing.

  python3 out/_analysis/d3_history_correction.py --spec out/_analysis/d3_history_fix_174.json --leg D3a-06 --write
"""
import argparse
import datetime
import json
import sys

HISTORY = "out/model/history.jsonl"
MOVES = {"asking questions", "focusing on puzzles", "dropping", "merging", "splitting",
         "relating", "developing working hypotheses", "dropping working hypotheses"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--leg", required=True)
    ap.add_argument("--stage", default="D3")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    for key in ("id", "event", "move", "why", "field", "now", "was", "corrects_lines"):
        if key not in spec:
            sys.exit(f"spec lacks {key}")
    if spec["move"] not in MOVES:
        sys.exit(f"move {spec['move']!r} is not one of Grodal, Anteby and Holm's eight")
    lines = open(HISTORY).read().splitlines()
    for n in spec["corrects_lines"]:
        if not (1 <= n <= len(lines)) or json.loads(lines[n - 1]).get("id") != spec["id"]:
            sys.exit(f"history line {n} is not a line for {spec['id']}")
    row = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "stage": a.stage, "leg": a.leg, "id": spec["id"], "event": spec["event"], "move": spec["move"],
           "why": spec["why"], "field": spec["field"], "now": spec["now"], "was": spec["was"],
           "corrects_lines": spec["corrects_lines"], "adaptations": []}
    print(json.dumps(row, ensure_ascii=False))
    if a.write:
        with open(HISTORY, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"appended one line to {HISTORY}")
    else:
        print("dry run: nothing written")


if __name__ == "__main__":
    main()
