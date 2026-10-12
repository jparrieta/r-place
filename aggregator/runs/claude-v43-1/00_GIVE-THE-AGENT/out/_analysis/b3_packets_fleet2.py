#!/usr/bin/env python3
"""B3a: the stage B3 packets in B2's packet shape (J, QB3-001, 16:37 Berlin) and in fleet ids (J, 2026-10-12), from
out/batches-B3.jsonl. It supersedes b3_packets_fleet.py's parts (out/_analysis/packets-B3_parts_superseded/).
packets.py B3 now writes this shape but with room ids, so this builder renders it with b2_packets_fleet.py's item
renderer:

  _packets-B3/index.md, G01.md ... G21.md   packets.py's scheme_pages on scheme_final.jsonl, no exemplars
  _packets-B3/B0017.md                      one self-contained packet per batch: title (batch and replicate), the
                                            brief with its own item count, the sibling block of every room in the
                                            batch's `rooms` (labels only, fleet ids), the items in position order,
                                            the end line
A flagged bag carries one line under its heading. A coder's label or note that names a room id (one in the store,
nyjets t11) is served with the fleet id in its place, the words unchanged; participants' words are never touched.
MANIFEST.json, per packet: items (its own count), bytes, item_bytes, sha256, count key and excludes, and
codes_by_item {fleet theme id: [fleet code ids]}; no group, part or parts. The build stops if a packet holds more
than 15 items or 180,000 bytes of item text, if an actual room id of a room in it stands anywhere in it, or if a
canvas field appears; it reports strings shaped like a room id that are no id of its rooms.

    python3 out/_analysis/b3_packets_fleet2.py [--write]
"""
import argparse, hashlib, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
pk = bpf.pk

MAX_ITEMS, MAX_BYTES, SHARED_CEILING = 15, 180000, 50 * 1024
ROOM_ID = re.compile(r"\b(?:c\d{4}|t\d{2,3})\b")
BRIEF = ("Each room is introduced once by the labels of all its second-order themes (the sibling block). Then the "
         "items, interleaved across rooms, numbered by position. Place each item and return one line per item in the "
         "form the return specification gives, the prediction line first and your second pass after your last item. "
         "Copy ids exactly as written here. This packet is complete in itself.")
BAGLINE = "flagged as a bag: place from the concepts, not from the coder's grouping."


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    translated = []
    for (s, t), th in store.themes.items():
        for f in ("second_order", "theme_note"):
            v = str(th.get(f) or "")
            nv = re.sub(r"\b(c\d{4}|t\d{2,3})\b",
                        lambda m: cmap.get((s, m.group(1))) or tmap.get((s, m.group(1))) or m.group(1), v)
            if nv != v:
                th[f] = nv
                translated.append("%s/%s %s" % (s, t, f))
    real = {}
    for (r, x) in list(cmap) + list(tmap):
        real.setdefault(r, set()).add(x)
    batches = jl(os.path.join(OUT, "batches-B3.jsonl"))
    files, bad, shaped = [], [], []
    for b in batches:
        name, rep, items = b["batch"], b["replicate"], b["items"]
        bags = set(b.get("bag_flags") or [])
        sib = []
        for r in sorted(b["rooms"]):
            ts = sorted(store.by_sub[r], key=lambda t: tmap[(r, t["theme_id"])])
            sib += (["## r/%s" % r, "", "sibling block, the labels of all %d second-order themes of this room (labels only):"
                     % len(ts)] + ["- %s %s" % (tmap[(r, t["theme_id"])], t.get("second_order") or "") for t in ts] + [""])
        body = []
        for p, k in enumerate(items, 1):
            s, t = k.split("/")
            bl = bpf.render(store, cmap, tmap, s, t, p)
            if k in bags:
                bl = bl[:2] + [BAGLINE, ""] + bl[2:]
            body += bl
        ib = len("\n".join(body).encode("utf-8"))
        txt = "\n".join(["# Batch %s, replicate %d" % (name, rep), "",
                         BRIEF + " It holds %d items; return %d lines, then your second pass, then the end marker."
                         % (len(items), len(items)), ""] + sib + ["## The items", ""] + body + ["", pk.END, ""])
        if len(items) > MAX_ITEMS or ib > MAX_BYTES:
            bad.append("%s: %d items, %d bytes of item text" % (name, len(items), ib))
        ids_here = set().union(*(real.get(r, set()) for r in b["rooms"]))
        m = set(ROOM_ID.findall(txt))
        if m & ids_here:
            bad.append("%s carries room ids of its rooms %s" % (name, sorted(m & ids_here)[:5]))
        elif m:
            shaped.append("%s: %s" % (name, sorted(m)))
        if pk.CANVAS.search(txt):
            bad.append("%s carries a canvas field" % name)
        files.append((name, txt, items, ib))
    print("coder labels and notes with a room id served as its fleet id: %s" % (translated or "none"))
    print("packets with strings shaped like a room id, no id of their rooms (participants' words): %s" % (shaped or "none"))
    print("packets %d; largest item text %d bytes; most items %d" % (
        len(files), max(f[3] for f in files), max(len(f[2]) for f in files)))
    for x in bad[:20]:
        print("  STOP: " + x)
    if bad:
        sys.exit("%d packets fail a check" % len(bad))
    if not a.write:
        return
    to = os.path.join(OUT, "_packets-B3")
    if os.path.exists(to) and os.listdir(to):
        sys.exit("%s exists and is not empty" % to)
    rows, sname = pk.load_scheme(OUT, ["scheme_final.jsonl"])
    pk.scheme_pages(ROOT, OUT, to, rows, pk.jl(os.path.join(OUT, "families.jsonl")), False)
    over = [f for f in os.listdir(to) if os.path.getsize(os.path.join(to, f)) > SHARED_CEILING]
    if over:
        sys.exit("shared pages over 50 KB: %s" % over)
    man = {}
    for name, txt, items, ib in files:
        open(os.path.join(to, name + ".md"), "w", encoding="utf-8").write(txt)
        cbi = {}
        for k in items:
            s, t = k.split("/")
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        man[name] = {"items": len(items), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(), "count_key": "position",
                     "count_exclude": pk.COUNT_04["count_exclude"], "codes_by_item": cbi}
    json.dump(man, open(os.path.join(to, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    print("wrote %s: 22 shared pages, %d packets, MANIFEST.json (%d lines due)" % (to, len(files), sum(v["items"] for v in man.values())))


if __name__ == "__main__":
    main()
