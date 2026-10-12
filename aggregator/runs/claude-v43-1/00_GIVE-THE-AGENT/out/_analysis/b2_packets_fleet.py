#!/usr/bin/env python3
"""B2 from round 3 (and the model for B3): self-contained pilot packets that carry only fleet ids
(J, 2026-10-12 09:14 Berlin).

Every code and second-order theme is served under its fleet id from out/fleet_ids.jsonl (codes `C` and seven
digits, themes `T2-` and five digits); the room's name stays. No room id (c0006, t01) reaches a packet, and
the build fails if one would. Returns are translated back with out/_analysis/b2_translate_fleet.py before
scoring; my own files keep the room ids.

Caps as J ruled for round 2 (2026-10-12): at most 15 items and 180,000 bytes of item text a packet; no item
split; each packet carries its own item count; MANIFEST.json without group or part, and with
"codes_by_item" ({fleet theme id: [fleet code ids served under it]}), which fleet.py reads to reject and
reissue a line citing a code its item does not hold (J, QB2-009). The items are
author_items.jsonl's, shuffled under --seed, cut into consecutive packets so that the largest is smallest
(--n packets, else the least the caps allow). The shared pages (index.md, the family pages) come from
tools/packets.py's scheme_pages on scheme.jsonl; they hold third-order ids only, which stay as they are.

    python3 out/_analysis/b2_packets_fleet.py --round 3 --seed N [--n K] [--write]
Dry run unless --write. Writes out/_packets-B2/round-K/ and out/_analysis/b2_order_rK.json.
"""
import argparse, hashlib, importlib.util, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
spec = importlib.util.spec_from_file_location("packets", os.path.join(ROOT, "tools", "packets.py"))
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)
spec2 = importlib.util.spec_from_file_location("r2b", os.path.join(OUT, "_analysis", "b2_packets_r2b.py"))
r2b = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(r2b)

MAX_ITEMS, MAX_BYTES = 15, 180000
ROOM_ID = re.compile(r"(?<![A-Za-z0-9])[ct]\d{2,4}(?![0-9])")
INTRO = ("Place each second-order theme below onto the scheme, one line per item in the form the return "
         "specification gives. Items are numbered by position. Each item is headed by its room and its id, and "
         "each concept by its id; copy ids exactly as written here. This packet is complete in itself: it holds "
         "%d items, and you return %d lines, then the end marker.")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def load_ids():
    c, t = {}, {}
    for r in jl(os.path.join(OUT, "fleet_ids.jsonl")):
        (c if r["kind"] == "c" else t)[(r["sub"], r["id"])] = r["fleet"]
    return c, t


def render(store, cmap, tmap, sub, tid, pos):
    t = store.themes[(sub, tid)]
    L = ["### %d. r/%s %s" % (pos, sub, tmap[(sub, tid)]), "",
         "label: %s" % (t.get("second_order") or ""), "",
         "note: %s" % " ".join(str(t.get("theme_note") or "").split()), ""]
    for cid in t.get("code_ids") or []:
        c = store.codes.get((sub, cid))
        if not c:
            continue
        L.append("- %s  %s" % (cmap[(sub, cid)], c.get("first_order") or ""))
        L.append("    \"%s\"" % " ".join(str(c.get("text") or "").split()))
    L.append("")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True); ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cmap, tmap = load_ids()
    store = pk.Store(ROOT)
    items = list(dict.fromkeys(pk.key_of(x) for x in jl(os.path.join(OUT, "author_items.jsonl"))))
    random.Random(a.seed).shuffle(items)
    blocks = [render(store, cmap, tmap, s, t, 1) for s, t in items]
    sizes = [len("\n".join(b).encode("utf-8")) + 2 for b in blocks]
    big = [("%s/%s" % it, z) for it, z in zip(items, sizes) if z > MAX_BYTES]
    if big:
        sys.exit("an item alone is over %d bytes; ask J before building: %s" % (MAX_BYTES, big))
    r2b.MAX_ITEMS, r2b.MAX_BYTES = MAX_ITEMS, MAX_BYTES
    n0 = -(-len(items) // MAX_ITEMS)
    n = a.n or next(k for k in range(n0, len(items) + 1) if r2b.partition(sizes, k))
    groups = r2b.partition(sizes, n)
    if not groups:
        sys.exit("no cut into %d packets meets the caps" % n)
    texts = []
    for k, (i, j) in enumerate(groups, 1):
        name = "P03-r%s-%d" % (a.round, k)
        its = items[i:j]
        body = []
        for pos, (s, t) in enumerate(its, 1):
            body += render(store, cmap, tmap, s, t, pos)
        txt = "\n".join(["# Pilot round %s, packet %s" % (a.round, name), "", INTRO % (len(its), len(its)), "",
                         "## The items", ""] + body + ["", pk.END, ""])
        # a room-id-like string may sit inside participants' own words: counted and reported; an id in an
        # id position (the heading or a concept line) stops the build
        leak = ROOM_ID.findall("\n".join(body))
        bad = [ln for ln in body if re.match(r"^(### \d+\. r/\S+ [ct]\d|- [ct]\d{4}\s)", ln)]
        if bad:
            sys.exit("%s would serve a room id in an id position: %s" % (name, bad[:3]))
        ib = len("\n".join(body).encode("utf-8"))
        if len(its) > MAX_ITEMS or ib > MAX_BYTES or pk.CANVAS.search(txt):
            sys.exit("%s breaks a cap or carries a canvas field" % name)
        texts.append((name, txt, ["%s/%s" % x for x in its], ib, len(leak)))
    for name, txt, its, ib, nl in texts:
        print("%-10s %2d items  %7d bytes of item text  room-id-like strings in quotes: %d" % (name, len(its), ib, nl))
    if not a.write:
        return
    to = os.path.join(OUT, "_packets-B2", "round-%s" % a.round)
    if os.path.exists(to) and os.listdir(to):
        sys.exit("%s exists and is not empty; supersede it under a new name first" % to)
    rows, sname = pk.load_scheme(OUT, ["scheme.jsonl"])
    pk.scheme_pages(ROOT, OUT, to, rows, pk.jl(os.path.join(OUT, "families.jsonl")), False)
    man = {}
    for name, txt, its, ib, _ in texts:
        open(os.path.join(to, name + ".md"), "w", encoding="utf-8").write(txt)
        # fleet.py rejects a line citing a code its item does not hold (J, QB2-009): it reads, per packet,
        # {the item's fleet theme id, as the line writes theme_id: [the fleet code ids served under it]}
        cbi = {}
        for it in its:
            s, t = it.split("/")
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        man[name] = {"items": len(its), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
                     "count_key": "position", "count_exclude": pk.COUNT_04["count_exclude"],
                     "codes_by_item": cbi}
    json.dump(man, open(os.path.join(to, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    json.dump({"seed": a.seed, "scheme": sname, "fleet_ids": "out/fleet_ids.jsonl",
               "packets": {name: its for name, _, its, _, _ in texts}},
              open(os.path.join(OUT, "_analysis", "b2_order_r%s.json" % a.round), "w", encoding="utf-8"), indent=1)
    print("wrote %s: shared pages, %d packets, MANIFEST.json" % (to, len(texts)))


if __name__ == "__main__":
    main()
