#!/usr/bin/env python3
"""E1 section 1, the unplaced (E1b-05): the 151 second-order themes with no placement, sorted into kinds by their
labels, so that the reading by hand starts from counts a script made. Reads unplaced.json (E1a); prints JSON.

    python3 out/audit-E1/unplaced_kinds.py > out/audit-E1/unplaced_kinds.json

The rule, declared before the run (E1b-05), by the label, in this order:
- "lost post": the label says the post's body or text is gone, deleted or removed, or that only a title, marker,
  mention or bare post is left (body, deleted, removed post, gone, only, bare, marker, unrecoverable, no surviving,
  unexplained, leaving only, little surviving);
- "the sub's own April Fools play": April, fool, prank, joke, goof, shitpost, meme;
- "a member's act the scheme names" (read by hand for whether it should have been placed): bot, building or
  repair words (build, almost complete, finish, plan, design, propos, call, recruit, welcom, mourn, defend, flag,
  sign, grid);
- "talk about the event": everything else (asking what an effort is, admiring, reacting, arguing about the canvas).
The themes in unplaced-B1.jsonl are marked; B1 listed them as holding no act.
"""
import collections, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KINDS = [("lost post", r"\bbody\b|deleted|removed post|\bgone\b|\bonly\b|\bbare\b|marker|unrecoverable|no surviving|unexplained|leaving only|little surviving"),
         ("the sub's own April Fools play", r"april|\bfool|prank|joke|goof|shitpost|meme"),
         ("a member's act the scheme names", r"\bbot\b|build|almost complete|finish|\bplan|design|propos|calling .* to|recruit|welcom|mourn|defend|\bflag\b|\bsign\b|\bgrid\b")]


def main():
    d = json.load(open(os.path.join(HERE, "unplaced.json"), encoding="utf-8"))
    out = collections.defaultdict(list)
    for x in d["unplaced_list"]:
        lab = x["label"].lower()
        k = next((name for name, pat in KINDS if re.search(pat, lab)), "talk about the event")
        out[k].append({"theme": x["theme"], "label": x["label"], "n_codes": x["n_codes"], "in_unplaced_B1": x["in_unplaced_B1"]})
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-05), by the label, in this order:")[1].strip(),
                      "counts": {k: len(v) for k, v in out.items()},
                      "concepts": {k: sum(x["n_codes"] for x in v) for k, v in out.items()},
                      "in_unplaced_B1": {k: sum(1 for x in v if x["in_unplaced_B1"]) for k, v in out.items()},
                      "kinds": out}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
