#!/usr/bin/env python3
"""B4b, read-only: the rendered size of every second-order theme of the analysed set as a B4 packet would serve it
(fleet ids, b2_packets_fleet.py's renderer: heading, label, note, each concept with the participants' words).
A property of the population, measured before the sample is declared and drawn, to choose a packet shape that
can serve any item the draw may take.

    python3 out/_analysis/b4b_item_sizes.py
"""
import importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def main():
    cmap, tmap = bpf.load_ids()
    store = bpf.pk.Store(ROOT, OUT)
    keys = [(x["sub"], x["theme_id"]) for x in (json.loads(l) for l in open(os.path.join(OUT, "assign_final.jsonl"), encoding="utf-8") if l.strip())]
    sizes = []
    for s, t in keys:
        b = bpf.render(store, cmap, tmap, s, t, 1)
        sizes.append((len(("\n".join(b) + "\n").encode("utf-8")), "%s/%s" % (s, t)))
    sizes.sort()
    n = len(sizes)
    q = lambda f: sizes[min(n - 1, int(f * n))][0]
    print("items %d; median %d bytes; p90 %d; p99 %d; max %d (%s)" % (n, q(0.5), q(0.9), q(0.99), sizes[-1][0], sizes[-1][1]))
    for cap in (20000, 30000, 40000, 45000, 50 * 1024, 100000, 180000):
        print("  over %6d bytes: %d" % (cap, sum(1 for z, _ in sizes if z > cap)))
    print("largest ten: %s" % ", ".join("%s %d" % (k, z) for z, k in sizes[-10:]))


if __name__ == "__main__":
    main()
