#!/usr/bin/env python3
"""B2a-r2: build pilot round 2 in parts for one reader (QB2-001), with tools/packets.py's own renderers.

packets.py B2 writes one packet and exits when it is over the 50 KB ceiling. Round 2's hard set (50
items, the ten biggest bags among them) renders far over it, and leagueoflegends t02 alone is over it,
so this helper cuts the rendered packet into parts P03-r2-p1 ... P03-r2-pN, each under the ceiling with
its end line. An item may run on into the next part under a "(continued)" heading; positions run on
across parts. The reader reads every part in one conversation and answers once per item after the last
part: parts 1 to N-1 ask for the end marker alone. MANIFEST.json (QB2-004, assumption pending the
answer): each part carries count_key position, group P03-r2, part k, parts N; items 0 on every part but
the last, which carries all items.

    python3 out/_analysis/b2_parts_r2.py --seed N [--scheme scheme.jsonl] [--items author_items.jsonl] [--write]

The shared pages (index.md and the family pages) come from packets.scheme_pages on the scheme given
(default scheme.jsonl, the edited scheme), and the items are shuffled exactly as packets.py v03 does.
Dry run unless --write.
"""
import argparse, importlib.util, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("packets", os.path.join(ROOT, "tools", "packets.py"))
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

NAME = "P03-r2"
INTRO = ("Place each second-order theme below onto the scheme, one line per item in the form the return "
         "specification gives. Items are numbered by position.")


def head(k, n, total):
    return ["# Pilot round 2, part %d of %d" % (k, n), "",
            "Packet %s is served in %d parts. You read every part in this one conversation; the parts are one "
            "packet of %d items. %s An item may run on from one part into the next: its concepts continue under "
            "the same heading, marked (continued). Answer once per item, after the last part." % (NAME, n, total, INTRO),
            "", "## The items, part %d of %d" % (k, n), ""]


def foot(k, n, total):
    if k < n:
        last = ("This is the end of part %d of %d. Do not place anything yet. Reply with the end marker the return "
                "specification names, alone; part %d follows. END OF PACKET" % (k, n, k + 1))
    else:
        last = ("This is the last part. Now return one line per item of the whole packet, positions 1 to %d, in "
                "packet order, then the end marker. %s" % (total, pk.END))
    return ["", last, ""]


def size(lines):
    return len("\n".join(lines).encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--scheme", default="scheme.jsonl")
    ap.add_argument("--families", default="families.jsonl")
    ap.add_argument("--items", default="author_items.jsonl")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    store = pk.Store(ROOT)
    items = [pk.key_of(x) for x in pk.jl(pk.path_in(OUT, a.items))]
    items = list(dict.fromkeys(items))
    random.Random(a.seed).shuffle(items)
    total = len(items)
    # blocks: (position, item, rendered lines without the heading)
    blocks = []
    for pos, (s, t) in enumerate(items, 1):
        L = store.item(s, t, pos)
        blocks.append((pos, "%s/%s" % (s, t), L[0], L[1:]))
    # greedy packing of lines; the budget leaves room for the longest header and footer
    budget = pk.CEILING - size(head(99, 99, total)) - size(foot(98, 99, total)) - size(foot(99, 99, total)) - 512
    def chunk_at(body, i):
        # a concept line travels with its quote line
        return body[i:i + 2] if body[i].startswith("- c") else body[i:i + 1]

    parts, cur, cur_items = [], [], []
    for pos, it, h, body in blocks:
        i, first = 0, True
        while i < len(body):
            hd = h if first else "%s (continued)" % h
            if cur and size(cur + [hd, ""] + chunk_at(body, i)) > budget:
                parts.append((cur, cur_items)); cur, cur_items = [], []
            cur += [hd, ""]
            cur_items.append(pos)
            placed = 0
            while i < len(body):
                c = chunk_at(body, i)
                if placed and size(cur + c) > budget:
                    break
                cur += c; i += len(c); placed += 1
            first = False
            if i < len(body):
                parts.append((cur, cur_items)); cur, cur_items = [], []
    if cur:
        parts.append((cur, cur_items))
    n = len(parts)
    texts = []
    for k, (L, its) in enumerate(parts, 1):
        txt = "\n".join(head(k, n, total) + L + foot(k, n, total))
        if size([txt]) > pk.CEILING:
            sys.exit("part %d is %d bytes, over the ceiling" % (k, size([txt])))
        texts.append((k, txt, sorted(set(its))))
    for k, txt, its in texts:
        print("%s-p%d  %6d bytes  positions %d-%d" % (NAME, k, size([txt]), its[0], its[-1]))
    print("%d items, %d parts, %d bytes in all; seed %d; scheme %s" % (total, n, sum(size([t]) for _, t, _ in texts), a.seed, a.scheme))
    # every concept of every item is served exactly once
    served = "\n".join(t for _, t, _ in texts)
    missing = []
    for s, t in items:
        for cid in store.themes[(s, t)].get("code_ids") or []:
            if (s, cid) in store.codes and "- %s  " % cid not in served:
                missing.append("%s/%s %s" % (s, t, cid))
    if missing:
        sys.exit("concepts not served: %d, e.g. %s" % (len(missing), missing[:3]))
    if not a.write:
        return
    rows, sname = pk.load_scheme(OUT, [a.scheme])
    fams = pk.jl(pk.path_in(OUT, a.families))
    to = os.path.join(OUT, "_packets-B2", "round-2")
    pk.scheme_pages(ROOT, OUT, to, rows, fams, False)
    man = {}
    for k, txt, its in texts:
        pname = "%s-p%d" % (NAME, k)
        rule = dict(pk.COUNT_04, group=NAME, part=k, parts=n, positions=[its[0], its[-1]], seed=a.seed)
        pk.write(os.path.join(to, "%s.md" % pname), txt, man, pname, total if k == n else 0, rule)
    pk.save_manifest(to, man)
    # the order record stays out of the readers' folder
    with open(os.path.join(OUT, "_analysis", "b2_order_r2.json"), "w", encoding="utf-8") as f:
        json.dump({"seed": a.seed, "scheme": sname, "parts": {"%s-p%d" % (NAME, k): its for k, _, its in texts},
                   "items": ["%s/%s" % x for x in items]}, f, indent=1)
    print("wrote %s: index.md, %d family pages, %d parts, MANIFEST.json; order in out/_analysis/b2_order_r2.json"
          % (to, len(fams), n))


if __name__ == "__main__":
    main()
