#!/usr/bin/env python3
"""B2b-r2: rebuild pilot round 2 as self-contained packets (J's ruling, 2026-10-12 05:52 Berlin).

The 11-part packet of B2a-r2 overran the provider's window (HTTP 400 at part 6). Each packet here is
read on its own, with the shared pages (index.md, G01 to G21) and RETURN-B2.md:
- at most 15 items and at most 180,000 bytes of item text per packet;
- no item split across packets (an item alone over the cap stops the build: ask J);
- no MANIFEST group, part or parts; each packet carries its own item count, positions 1..k;
- the same 50 items in round 2's seeded order (out/_analysis/b2_order_r2.json, seed 20261012), cut into
  consecutive packets; the number of packets is the least the caps allow (or --n), and the cut points
  minimise the largest packet.
The items are rendered by tools/packets.py's own Store.item. The superseded 11-part files and the old
MANIFEST.json move to out/_analysis/b2_packets_round2_parts/ (never deleted). Dry run unless --write.
"""
import argparse, hashlib, importlib.util, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("packets", os.path.join(ROOT, "tools", "packets.py"))
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

MAX_ITEMS, MAX_BYTES = 15, 180000
TO = os.path.join(OUT, "_packets-B2", "round-2")
OLD = os.path.join(OUT, "_analysis", "b2_packets_round2_parts")
INTRO = ("Place each second-order theme below onto the scheme, one line per item in the form the return "
         "specification gives. Items are numbered by position. This packet is complete in itself: it holds "
         "%d items, and you return %d lines, then the end marker.")


def b(s):
    return len(s.encode("utf-8"))


def partition(sizes, n):
    """Cut sizes (in order) into n consecutive groups within the caps, minimising the largest group's
    bytes; returns the cut lists or None."""
    m = len(sizes)
    pre = [0]
    for s in sizes:
        pre.append(pre[-1] + s)
    INF = float("inf")
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    cut = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for k in range(1, n + 1):
        for j in range(1, m + 1):
            for i in range(max(0, j - MAX_ITEMS), j):
                w = pre[j] - pre[i]
                if w > MAX_BYTES or best[k - 1][i] == INF:
                    continue
                v = max(best[k - 1][i], w)
                if v < best[k][j]:
                    best[k][j], cut[k][j] = v, i
    if best[n][m] == INF:
        return None
    groups, j = [], m
    for k in range(n, 0, -1):
        i = cut[k][j]
        groups.append((i, j))
        j = i
    return groups[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2.json"), encoding="utf-8"))
    items = [tuple(x.split("/", 1)) for x in order["items"]]
    hard = {pk.key_of(x) for x in pk.jl(os.path.join(OUT, "author_items.jsonl"))}
    if set(items) != hard or len(items) != len(hard):
        sys.exit("round 2's order does not hold exactly the hard set")
    store = pk.Store(ROOT)
    blocks = ["\n".join(store.item(s, t, 0)) for s, t in items]      # size with a one-digit position
    sizes = [b(x) + 2 for x in blocks]
    big = [("%s/%s" % it, z) for it, z in zip(items, sizes) if z > MAX_BYTES]
    if big:
        sys.exit("an item alone is over %d bytes, ask J before building: %s" % (MAX_BYTES, big))
    n0 = -(-len(items) // MAX_ITEMS)
    for n in range(n0, n0 + 4):
        g = partition(sizes, n)
        if g:
            print("n=%d: items %s, item bytes %s" % (n, [j - i for i, j in g], [sum(sizes[i:j]) for i, j in g]))
    n = a.n
    if n is None:
        n = next(k for k in range(n0, len(items) + 1) if partition(sizes, k))
    groups = partition(sizes, n)
    if not groups:
        sys.exit("no cut into %d packets meets the caps" % n)
    texts = []
    for k, (i, j) in enumerate(groups, 1):
        name = "P03-r2-%d" % k
        its = items[i:j]
        L = ["# Pilot round 2, packet %s" % name, "", INTRO % (len(its), len(its)), "", "## The items", ""]
        body = []
        for pos, (s, t) in enumerate(its, 1):
            body += store.item(s, t, pos)
        L += body + ["", pk.END, ""]
        txt = "\n".join(L)
        item_bytes = b("\n".join(body))
        if len(its) > MAX_ITEMS or item_bytes > MAX_BYTES or pk.CANVAS.search(txt):
            sys.exit("%s breaks a cap or carries a canvas field" % name)
        texts.append((name, txt, ["%s/%s" % x for x in its], item_bytes))
    for name, txt, its, ib in texts:
        print("%-10s %2d items  %7d bytes of item text  %7d bytes in all  first %s" % (name, len(its), ib, b(txt), its[0]))
    if not a.write:
        return
    # supersede the 11-part build: move, never delete
    os.makedirs(OLD, exist_ok=True)
    moved = []
    for f in sorted(os.listdir(TO)):
        if f.startswith("P03-r2-p") and f.endswith(".md"):
            os.replace(os.path.join(TO, f), os.path.join(OLD, f)); moved.append(f)
    mp = os.path.join(TO, "MANIFEST.json")
    if os.path.exists(mp) and not os.path.exists(os.path.join(OLD, "MANIFEST.json")):
        shutil.copy2(mp, os.path.join(OLD, "MANIFEST.json"))
    man = {}
    for name, txt, its, ib in texts:
        open(os.path.join(TO, name + ".md"), "w", encoding="utf-8").write(txt)
        man[name] = {"items": len(its), "bytes": b(txt), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
                     "count_key": "position", "count_exclude": pk.COUNT_04["count_exclude"]}
    json.dump(man, open(mp, "w", encoding="utf-8"), indent=1)       # the new manifest replaces the old, kept in OLD
    with open(os.path.join(OUT, "_analysis", "b2_order_r2b.json"), "w", encoding="utf-8") as f:
        json.dump({"seed": order["seed"], "from": "out/_analysis/b2_order_r2.json",
                   "packets": {name: its for name, _, its, _ in texts}}, f, indent=1)
    print("moved %d superseded parts and the old MANIFEST.json to %s; wrote %d packets and MANIFEST.json in %s"
          % (len(moved), OLD, len(texts), TO))


if __name__ == "__main__":
    main()
