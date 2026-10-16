#!/usr/bin/env python3
"""Revise one element's field in out/model/elements.jsonl and append its history line.

The spec is a JSON file: {"id", "field", "now", "move", "event", "why", "adaptations"}.
Without --write it prints the field before and after and writes nothing. With --write it
replaces only that element's line (every other line is kept byte for byte) and appends to
out/model/history.jsonl a line in the form move 172 used: t, stage, leg, id, event, move, why,
field, now, was (the whole element as it stood), adaptations.

  python3 out/_analysis/d3_revise_element.py --spec out/_analysis/d3_revision_P05.json --leg D3a-04
"""
import argparse
import copy
import datetime
import json
import sys

ELEMENTS = "out/model/elements.jsonl"
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
    for key in ("id", "field", "now", "move", "event", "why", "adaptations"):
        if key not in spec:
            sys.exit(f"spec lacks {key}")
    if spec["move"] not in MOVES:
        sys.exit(f"move {spec['move']!r} is not one of Grodal, Anteby and Holm's")
    lines = open(ELEMENTS).read().splitlines()
    hits = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("id") == spec["id"]]
    if len(hits) != 1:
        sys.exit(f"{spec['id']}: {len(hits)} lines in {ELEMENTS}")
    i = hits[0]
    was = json.loads(lines[i])
    if spec["field"] not in was:
        sys.exit(f"{spec['id']} has no field {spec['field']}")
    new = copy.deepcopy(was)
    new[spec["field"]] = spec["now"]
    print(f"{spec['id']}.{spec['field']} was: {was[spec['field']]}")
    print(f"{spec['id']}.{spec['field']} now: {new[spec['field']]}")
    hist = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "stage": a.stage, "leg": a.leg, "id": spec["id"], "event": spec["event"],
            "move": spec["move"], "why": spec["why"], "field": spec["field"], "now": spec["now"],
            "was": was, "adaptations": spec["adaptations"]}
    if not a.write:
        print("dry run: nothing written")
        return
    lines[i] = json.dumps(new, ensure_ascii=False)
    with open(ELEMENTS, "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(HISTORY, "a") as f:
        f.write(json.dumps(hist, ensure_ascii=False) + "\n")
    print(f"rewrote {spec['id']} in {ELEMENTS}; appended one line to {HISTORY}")


if __name__ == "__main__":
    main()
