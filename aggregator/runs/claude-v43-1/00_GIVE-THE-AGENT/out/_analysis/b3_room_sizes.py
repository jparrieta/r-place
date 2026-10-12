#!/usr/bin/env python3
"""B3a: how large each room of the analysed set renders as fleet items (b2_packets_fleet.py's render: fleet ids,
label, note, every concept with the participants' words) and as a sibling block (labels only). Writes
out/_analysis/b3_room_sizes.tsv (sub, themes, item bytes, largest item bytes, sibling bytes) and prints the
distribution. Reads only otherwise."""
import importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)

cmap, tmap = bpf.load_ids()
store = bpf.pk.Store(ROOT, OUT)
rows = []
for sub, ts in store.by_sub.items():
    sizes = [len("\n".join(bpf.render(store, cmap, tmap, sub, t["theme_id"], 1)).encode("utf-8")) for t in ts]
    sib = sum(len(("- %s %s\n" % (tmap[(sub, t["theme_id"])], t.get("second_order") or "")).encode("utf-8")) for t in ts)
    rows.append((sub, len(ts), sum(sizes), max(sizes), sib))
rows.sort(key=lambda r: -r[2])
with open(os.path.join(OUT, "_analysis", "b3_room_sizes.tsv"), "w", encoding="utf-8") as f:
    f.write("sub\tthemes\titem_bytes\tlargest_item\tsibling_bytes\n")
    for r in rows:
        f.write("%s\t%d\t%d\t%d\t%d\n" % r)
tot = sum(r[2] for r in rows)
print("rooms %d, items %d, item bytes %d (%.1f MB)" % (len(rows), sum(r[1] for r in rows), tot, tot / 1e6))
for lim in (50000, 100000, 180000, 300000):
    print("rooms over %d bytes: %d" % (lim, sum(1 for r in rows if r[2] > lim)))
print("items over 50,000 bytes: %d; over 180,000: %d" % (
    sum(1 for t in store.themes.values() if False), 0))
big = sorted(((len("\n".join(bpf.render(store, cmap, tmap, s, t, 1)).encode("utf-8")), s, t) for (s, t) in store.themes), reverse=True)
print("largest items:", ", ".join("%s/%s %d" % (s, t, z) for z, s, t in big[:8]))
print("items over 50,000 bytes: %d; over 100,000: %d" % (sum(1 for z, _, _ in big if z > 50000), sum(1 for z, _, _ in big if z > 100000)))
print("largest rooms:", ", ".join("%s %d themes %d bytes" % (r[0], r[1], r[2]) for r in rows[:10]))
print("themes per room: max %d; rooms with more than 40: %d" % (max(r[1] for r in rows), sum(1 for r in rows if r[1] > 40)))
