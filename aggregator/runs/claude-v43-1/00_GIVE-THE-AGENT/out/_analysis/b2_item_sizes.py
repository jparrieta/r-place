#!/usr/bin/env python3
"""B2: how many bytes each second-order theme takes in a B2 packet, rendered by packets.py's own Store.item.

Usage: python3 out/_analysis/b2_item_sizes.py [sub/tNN ...]
With no items: the distribution over all second-order themes of the store.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import packets  # noqa: E402

store = packets.Store(ROOT)


def size(s, t):
    return len(("\n".join(store.item(s, t, 99)) + "\n").encode("utf-8"))


if len(sys.argv) > 1:
    tot = 0
    for x in sys.argv[1:]:
        s, t = x.split("/")
        n = size(s, t)
        tot += n
        print("%s/%s\t%d bytes\t%d concepts" % (s, t, n, len(store.themes[(s, t)].get("code_ids") or [])))
    print("total %d bytes" % tot)
else:
    v = sorted(size(s, t) for (s, t) in store.themes)
    q = lambda f: v[int(f * (len(v) - 1))]
    print("themes %d; bytes min %d, p10 %d, p25 %d, median %d, p75 %d, p90 %d, max %d; mean %.0f" % (
        len(v), v[0], q(.1), q(.25), q(.5), q(.75), q(.9), v[-1], sum(v) / len(v)))
