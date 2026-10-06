#!/usr/bin/env python3
"""transitions.py, v38: stage 00, the transitions ledger.

    python3 tools/transitions.py [--root .]

Reads package/forest.jsonl and package/store/codes.jsonl. Writes
package/store/transitions.jsonl: one line for every coded turn that answers a coded turn,
directly or through uncoded turns (bridge or removed nodes) that the forest kept:

    {"id", "sub", "thread_id", "from_item", "to_item", "from_coord", "to_coord",
     "from_codes", "to_codes", "from_case_themes", "to_case_themes",
     "from_author", "to_author", "same_author", "interval_s", "hops", "from_hour", "limit"}

`from_case_themes` and `to_case_themes` hold second-order theme ids (the coder's `theme_id`);
the key names are kept so mem.py's `after` and `pairs` read them unchanged. `id` is `<thread_id>:<from_coord>><to_coord>`, readable off the
forest (`trees/<sub>.md` prints the thread id and every coordinate), so a labeler at D2 cites a
transition in `evidence.transitions` without the store. `from` is the earlier
turn, `to` the answer. `hops` is 1 for a direct reply; a larger number counts the uncoded turns
between. `interval_s` is the time between the two posts.

The limit is on every line and it is the whole ledger's meaning: a reply is a reply. The ledger
shows that one coded turn was posted in answer to another and how long after; it does not show
that the first caused the second, and an interval is elapsed time, never the speed of a decision.
mem.py lifts these pairs to third-order themes and fourth-order themes at query time through the
analyst's own tier files; nothing here knows what a theme is.

Also writes package/store/_README-transitions.md, which build_store.py --readme-only folds into
README-store.md.
"""
import argparse, json, os, sys

LIMIT = "a reply is a reply: posted after, not caused by"


def jl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def walk(node, sub, tid, theme_of, out, ancestor=None, hops=0):
    coded = bool(node.get("code_ids"))
    if coded and ancestor is not None:
        out.append({
            "id": "%s:%s>%s" % (tid, ancestor["coord"], node["coord"]),
            "sub": sub, "thread_id": tid,
            "from_item": ancestor["item_id"], "to_item": node["item_id"],
            "from_coord": ancestor["coord"], "to_coord": node["coord"],
            "from_codes": ancestor["code_ids"], "to_codes": node["code_ids"],
            "from_case_themes": sorted({theme_of.get((sub, c)) for c in ancestor["code_ids"]} - {None}),
            "to_case_themes": sorted({theme_of.get((sub, c)) for c in node["code_ids"]} - {None}),
            "from_author": ancestor["author"], "to_author": node["author"],
            "same_author": ancestor["author"] == node["author"],
            "interval_s": round(node["dt_thread_sec"] - ancestor["dt_thread_sec"], 1),
            "hops": hops, "from_hour": ancestor.get("hour"),
            "limit": LIMIT})
    nxt, nhops = (node, 1) if coded else (ancestor, hops + 1 if ancestor is not None else 0)
    for ch in node.get("children", []):
        if ch.get("state") == "collapsed":
            continue
        walk(ch, sub, tid, theme_of, out, nxt, nhops)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    P = os.path.join(a.root, "package")
    S = os.path.join(P, "store")
    theme_of = {(c["sub"], c["code_id"]): c["theme_id"] for c in jl(os.path.join(S, "codes.jsonl"))}
    out, n_threads = [], 0
    with open(os.path.join(P, "forest.jsonl"), encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            n_threads += 1
            t0 = d.get("hours_since_open")
            root = d["tree"]

            def stamp(n, t0=t0):
                n["hour"] = None if t0 is None else round(t0 + n["dt_thread_sec"] / 3600.0, 2)
                for ch in n.get("children", []):
                    stamp(ch)
            stamp(root)
            walk(root, d.get("sub") or d["community"], d["thread_id"], theme_of, out)
    out.sort(key=lambda r: (r["sub"], r["thread_id"], r["to_coord"]))
    with open(os.path.join(S, "transitions.jsonl"), "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    direct = sum(1 for r in out if r["hops"] == 1)
    same = sum(1 for r in out if r["same_author"])
    rooms = len({r["sub"] for r in out})
    ivs = sorted(r["interval_s"] for r in out)
    med = ivs[len(ivs) // 2] if ivs else None
    txt = """## The transitions ledger (`transitions.jsonl`)

One line per coded turn that answers a coded turn: %d lines in %d threads of %d rooms;
%d are direct replies (`hops` = 1), the rest reach their nearest coded ancestor through uncoded
turns the forest kept; %d are the same author answering themselves. Median interval %s s.
`from_case_themes` and `to_case_themes` carry second-order theme ids. `mem.py after <sub>/<code_id>`
reads it per code; `mem.py pairs --level second|third|fourth|dimension` lifts it through your own tier files and
prints the limit with every table.

**The limit:** %s. An interval is elapsed time, never the speed of a decision.
""" % (len(out), n_threads, rooms, direct, same, med, LIMIT)
    with open(os.path.join(S, "_README-transitions.md"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("transitions %d (direct %d, same author %d) over %d threads, %d rooms"
          % (len(out), direct, same, n_threads, rooms))
    return 0


if __name__ == "__main__":
    sys.exit(main())
