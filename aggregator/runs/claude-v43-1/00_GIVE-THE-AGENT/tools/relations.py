#!/usr/bin/env python3
"""relations.py, v38: stage 00, the mention graph, from the pointers the coders wrote.

    python3 tools/relations.py [--root .] [--adjacency FILE]

Reads package/store/pointers.jsonl (every pointer a coder wrote, as written) and
package/store/rooms.jsonl (the frame). Writes package/store/relations.jsonl, one line per
(room, other) pair the room's coder recorded, and package/store/_README-relations.md, which
build_store.py --readme-only folds into README-store.md.

    {"sub", "other", "other_in_frame", "direction", "label", "labels", "n", "pointer_ids",
     "code_ids", "moved", "reciprocal", "adjacent"}

`other` is the pointer's `normalised` form with the `r/` prefix removed, matched to the frame
case-insensitively; `other_in_frame` says whether the other is a room of this study. `direction`
is `names` (this room's coder recorded the other); `reciprocal` is true when the other room's
coder recorded this room too. `label` is the coder's relation (`attacked`, `allied`,
`negotiated`, `mentioned-only`, ...) that the pair carries most often, ties broken toward the
stronger tie in the order below; `labels` counts every one. `moved` counts the coder's `moved`
values. Off-platform pointers (Discord, IRC and the like) are not relations between rooms; they
are counted per room in `off_platform` lines with `other` null.

`adjacent` is canvas adjacency. It is null unless --adjacency names a file of
{"sub", "other", "adjacent": true|false} lines built from the canvas outside the analyst's
reach; adjacency is a relation between rooms only.

**The limit.** A pointer is a mention the coder read and recorded. It is not the whole of a
room's dealings with another: a room that coordinated off the record, or whose coder read other
threads, has relations this file does not hold.
"""
import argparse, collections, json, os, sys

ORDER = ("attacked", "attacked-by", "destroyed-carelessly", "allied", "gave-help-to", "asked-help-from",
         "negotiated", "mentioned-only")


def jl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def norm(x):
    x = (x or "").strip()
    for pre in ("/r/", "r/", "R/"):
        if x.startswith(pre):
            x = x[len(pre):]
    return x.strip("/ ").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--adjacency", default=None)
    a = ap.parse_args()
    S = os.path.join(a.root, "package", "store")
    rooms = [r["sub"] for r in jl(os.path.join(S, "rooms.jsonl"))]
    if not rooms:
        sys.exit("no rooms in %s; build the store first" % S)
    by_lower = {r.lower(): r for r in rooms}
    pairs = collections.defaultdict(lambda: {"labels": collections.Counter(), "moved": collections.Counter(),
                                             "pointer_ids": [], "code_ids": []})
    off = collections.defaultdict(lambda: {"n": 0, "pointer_ids": [], "names": collections.Counter()})
    for p in jl(os.path.join(S, "pointers.jsonl")):
        sub = p.get("sub")
        if p.get("kind") == "off_platform":
            o = off[sub]
            o["n"] += 1
            o["pointer_ids"].append(p.get("pointer_id"))
            o["names"][(p.get("normalised") or p.get("raw") or "").lower()] += 1
            continue
        if p.get("kind") != "subreddit":
            continue
        other_l = norm(p.get("normalised") or p.get("raw"))
        if not other_l or other_l == sub.lower():
            continue
        other = by_lower.get(other_l, other_l)
        d = pairs[(sub, other)]
        d["labels"][p.get("relation") or "unlabelled"] += 1
        d["moved"][p.get("moved") or "unknown"] += 1
        d["pointer_ids"].append(p.get("pointer_id"))
        d["code_ids"] += [c for c in p.get("code_ids") or [] if c not in d["code_ids"]]
    adj = {}
    if a.adjacency:
        for r in jl(a.adjacency):
            adj[(r["sub"], r["other"])] = bool(r.get("adjacent"))
    rank = {k: i for i, k in enumerate(ORDER)}
    out = []
    for (sub, other), d in sorted(pairs.items()):
        top = max(d["labels"].items(), key=lambda kv: (kv[1], -rank.get(kv[0], 99)))[0]
        out.append({"sub": sub, "other": other, "other_in_frame": other.lower() in by_lower,
                    "direction": "names", "label": top, "labels": dict(d["labels"]),
                    "n": sum(d["labels"].values()), "pointer_ids": d["pointer_ids"], "code_ids": d["code_ids"],
                    "moved": dict(d["moved"]), "reciprocal": (other, sub) in pairs,
                    "adjacent": adj.get((sub, other)) if a.adjacency else None})
    for sub, o in sorted(off.items()):
        out.append({"sub": sub, "other": None, "other_in_frame": False, "direction": "off_platform",
                    "label": "off_platform", "labels": dict(o["names"]), "n": o["n"],
                    "pointer_ids": o["pointer_ids"], "code_ids": [], "moved": {}, "reciprocal": False,
                    "adjacent": None})
    with open(os.path.join(S, "relations.jsonl"), "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    inter = [r for r in out if r["direction"] == "names"]
    in_frame = sum(1 for r in inter if r["other_in_frame"])
    recip = sum(1 for r in inter if r["reciprocal"])
    labels = collections.Counter(r["label"] for r in inter)
    txt = """## The mention graph (`relations.jsonl`)

One line per (room, other) pair a room's coder recorded: %d pairs from %d rooms, %d naming a room
of this study, %d reciprocated (the other room's coder recorded this room too). Labels, the pair's
most frequent: %s. Off-platform pointers are %d lines with `other` null. `adjacent` (canvas
adjacency) is %s.

**The limit:** a pointer is a mention the coder read and recorded, not the whole of a room's
dealings with another.
""" % (len(inter), len({r["sub"] for r in inter}), in_frame, recip,
       ", ".join("%s %d" % kv for kv in labels.most_common()), len(out) - len(inter),
       "joined from %s" % os.path.basename(a.adjacency) if a.adjacency else "null: no adjacency file was given")
    with open(os.path.join(S, "_README-relations.md"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("relations %d pairs (%d in the frame, %d reciprocal), %d off-platform lines"
          % (len(inter), in_frame, recip, len(out) - len(inter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
