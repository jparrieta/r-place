#!/usr/bin/env python3
"""D4: declare the cross-links (stage D4 section 2, cut rule R5): every room that is a member of two branches that do
not nest (neither is an ancestor of the other) gets one out/crosslinks.jsonl line per such pair: sub, branches (the
two ids), reason (the key each branch holds the room on, and that the branches do not nest). A line already in the
file is not written again. With --write it also appends one stage-D4 tier_history.jsonl line per branch pair newly
cross-linked (tier crosslink, move relating, the rooms). Creates crosslinks.jsonl when absent, empty if no room
qualifies. Without --write it prints the pairs and writes nothing.

    python3 out/_analysis/d4_crosslinks.py --leg D4a-01 [--write]
"""
import argparse, collections, datetime, itertools, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--leg", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


B = {b["id"]: b for b in jl(os.path.join(OUT, "branches.jsonl"))}


def ancestors(x):
    out = set()
    while B.get(x, {}).get("parent") in B and B[x]["parent"] not in out:
        x = B[x]["parent"]
        out.add(x)
    return out


CP = os.path.join(OUT, "crosslinks.jsonl")
have = {(r["sub"], frozenset(r["branches"])) for r in jl(CP)}
new, pairs = [], collections.defaultdict(list)
for x, y in itertools.combinations(sorted(B), 2):
    if x in ancestors(y) or y in ancestors(x):
        continue
    for s in sorted(set(B[x]["members"]) & set(B[y]["members"]), key=str.lower):
        if (s, frozenset([x, y])) in have:
            continue
        new.append({"sub": s, "branches": [x, y],
                    "reason": "%s is a member of %s on %s and of %s on %s; the two branches do not nest, so the room's "
                              "adaptations meet both groups (declared, not forced)" % (
                                  s, x, ", ".join(B[x]["keys"]), y, ", ".join(B[y]["keys"])),
                    "leg": a.leg})
        pairs[(x, y)].append(s)
for (x, y), ss in sorted(pairs.items()):
    print("%s and %s: %d rooms: %s" % (x, y, len(ss), ", ".join(ss)))
print("new cross-link lines: %d over %d branch pairs" % (len(new), len(pairs)))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
with open(CP, "a", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
with open(os.path.join(OUT, "tier_history.jsonl"), "a", encoding="utf-8") as f:
    for (x, y), ss in sorted(pairs.items()):
        f.write(json.dumps({"t": t, "stage": "D4", "leg": a.leg, "tier": "crosslink", "id": "%s+%s" % (x, y),
                            "move": "relating", "event": "cross-link declared",
                            "why": "rooms in two branches that do not nest (cut rule R5)", "ground": "keys",
                            "rooms": ss}, ensure_ascii=False) + "\n")
print("crosslinks.jsonl now %d lines" % len(jl(CP)))
