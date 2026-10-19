#!/usr/bin/env python3
"""Revise one arrow's fields in out/model/arrows.jsonl and append one history line per field.

The spec is a JSON file: {"id", "move", "adaptations", "changes": [{"field", "now", "event", "why"}, ...]}.
Without --write it prints each field before and after and writes nothing. With --write it replaces only
that arrow's line (every other line is kept byte for byte) and appends to out/model/history.jsonl, per
change, a line in the form d3_revise_element.py writes: t, stage, leg, id, event, move, why, field, now,
was (the whole arrow as it stood before that change), adaptations. A field the arrow lacks is added only
when the change says "new": true.

  python3 out/_analysis/d3_revise_arrow.py --spec out/_analysis/d3_revision_A21.json --leg D3a-27 [--write]
"""
import argparse
import copy
import datetime
import json
import sys

ARROWS = "out/model/arrows.jsonl"
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
    for key in ("id", "move", "adaptations", "changes"):
        if key not in spec:
            sys.exit(f"spec lacks {key}")
    if spec["move"] not in MOVES:
        sys.exit(f"move {spec['move']!r} is not one of Grodal, Anteby and Holm's")
    lines = open(ARROWS).read().splitlines()
    hits = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("id") == spec["id"]]
    if len(hits) != 1:
        sys.exit(f"{spec['id']}: {len(hits)} lines in {ARROWS}")
    i = hits[0]
    cur = json.loads(lines[i])
    hist = []
    for ch in spec["changes"]:
        for key in ("field", "now", "event", "why"):
            if key not in ch:
                sys.exit(f"a change lacks {key}")
        if ch["field"] not in cur and not ch.get("new"):
            sys.exit(f"{spec['id']} has no field {ch['field']} (mark the change new to add it)")
        was = copy.deepcopy(cur)
        print(f"{spec['id']}.{ch['field']} was: {cur.get(ch['field'])}")
        print(f"{spec['id']}.{ch['field']} now: {ch['now']}")
        cur = copy.deepcopy(cur)
        cur[ch["field"]] = ch["now"]
        hist.append({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "stage": a.stage, "leg": a.leg, "id": spec["id"], "event": ch["event"],
                     "move": spec["move"], "why": ch["why"], "field": ch["field"], "now": ch["now"],
                     "was": was, "adaptations": spec["adaptations"]})
    if not a.write:
        print(f"dry run: {len(hist)} changes, nothing written")
        return
    lines[i] = json.dumps(cur, ensure_ascii=False)
    with open(ARROWS, "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(HISTORY, "a") as f:
        for h in hist:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    print(f"rewrote {spec['id']} in {ARROWS}; appended {len(hist)} lines to {HISTORY}")


if __name__ == "__main__":
    main()
