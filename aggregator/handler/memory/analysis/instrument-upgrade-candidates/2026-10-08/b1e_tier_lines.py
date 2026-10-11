#!/usr/bin/env python3
"""B1e: tier_history.jsonl lines for the scheme standing.

One `relabelled` line per theme whose shipped name (out/scheme.jsonl) differs from its working
label (scheme/scheme_current.jsonl), move "asking questions": the gates at section 3 are that move,
and each name was set against its gate and its family's discriminators. One `moved_to_rare` line
per theme shipped on the rare tier, move "relating or contrasting": the floor sets a theme's rooms
against each other, and a theme short of two rooms unlike each other goes to the rare tier.

Dry run by default; --write appends to out/tier_history.jsonl.
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
HEAD_LISTED = {"T3-010", "T3-056", "T3-121", "T3-023", "T3-048", "T3-030", "T3-192", "T3-065", "T3-115", "T3-063",
               "T3-088", "T3-132", "T3-117", "T3-188", "T3-041", "T3-087", "T3-120"}
EPISODE = {"T3-128": "its three rooms (PurplePixels, destiny, ice_poseidon) tell one episode, E1132 in episodes-B1.jsonl, so they count as one room"}


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def main():
    write = "--write" in sys.argv
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    cur = {r["theme"]: r for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl"))}
    lines = []
    for r in jl(os.path.join(OUT, "scheme.jsonl")):
        tid, old = r["id"], cur[r["id"]]["label"]
        if r["name"] != old:
            pb = "B1e gate writing for family %s: the name set against the theme's gate and its discriminators" % r["family"]
            if tid in HEAD_LISTED:
                pb += "; the change was listed in the head's names to change, from the second pass"
            lines.append({"t": t, "stage": "B1", "leg": "B1e", "tier": "third", "id": tid, "move": "asking questions",
                          "event": "relabelled", "was": {"label": old}, "now": [{"id": tid, "label": r["name"]}],
                          "prompted_by": pb,
                          "why": "the name now says in 2 to 5 words what the gate admits, near the material, and the gloss carries the rest"})
        if r["tier"] == "rare":
            rooms = sorted({m["sub"] for m in cur[tid]["members"]})
            why = EPISODE.get(tid, "seen in one room only (%s)" % ", ".join(rooms))
            lines.append({"t": t, "stage": "B1", "leg": "B1e", "tier": "third", "id": tid, "move": "relating or contrasting",
                          "event": "moved_to_rare", "was": {"label": old, "tier": None},
                          "now": [{"id": tid, "tier": "rare", "members": len(cur[tid]["members"])}],
                          "prompted_by": "the floor read at B1e (out/_analysis/b1e_floor.py against episodes-B1.jsonl and the store's rooms)",
                          "why": why + "; it ships on the rare tier with every field, so the fleet can place onto it and its count is measured; folding it into a neighbour was set aside"})
    print("relabelled %d, moved_to_rare %d; %s" % (sum(x["event"] == "relabelled" for x in lines),
                                                   sum(x["event"] == "moved_to_rare" for x in lines), "written" if write else "dry run"))
    if write:
        with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
            for x in lines:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
