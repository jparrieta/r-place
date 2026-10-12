#!/usr/bin/env python3
"""B2c: the gold round and the two stability rounds on the frozen scheme (stage B2 section 5), in fleet ids, as
round 3 was built (b2_packets_fleet.py: J's caps, at most 15 items and 180,000 bytes of item text a packet, no
item split, self-contained packets, MANIFEST.json with codes_by_item and without group or part).

Differences from b2_packets_fleet.py: the items come from --items (gold_items.jsonl); the shared pages come from
scheme_final.jsonl; the brief, the packet's opening paragraph, is BRIEF below unless --brief names a file (the
stability rounds, out/brief-stab-1.md and -2.md, reworded and changing no test); the item count follows the brief
as its own sentence, the same in every round. The three rounds use the same seed, so the same items fall in the
same packets in the same order, and only the brief differs. Packets are named P03-r<round>-<k>.

    python3 out/_analysis/b2_packets_fleet2.py --round gold|stab-1|stab-2 --seed N [--brief out/brief-stab-1.md] [--write]
Dry run unless --write. Writes out/_packets-B2/round-<round>/ and out/_analysis/b2_order_r<round>.json.
"""
import argparse, hashlib, importlib.util, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
pk, r2b = bpf.pk, bpf.r2b

BRIEF = ("Place each second-order theme below onto the scheme, one line per item in the form the return "
         "specification gives. Items are numbered by position. Each item is headed by its room and its id, and each "
         "concept by its id; copy ids exactly as written here. This packet is complete in itself.")
COUNT = "It holds %d items; return %d lines, then the end marker."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True, choices=["gold", "stab-1", "stab-2"])
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--brief")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.round.startswith("stab") and not a.brief:
        sys.exit("a stability round needs --brief")
    brief = " ".join(open(a.brief, encoding="utf-8").read().split()) if a.brief else BRIEF
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    items = list(dict.fromkeys(pk.key_of(x) for x in bpf.jl(os.path.join(OUT, "gold_items.jsonl"))))
    random.Random(a.seed).shuffle(items)
    blocks = [bpf.render(store, cmap, tmap, s, t, 1) for s, t in items]
    sizes = [len("\n".join(b).encode("utf-8")) + 2 for b in blocks]
    big = [("%s/%s" % it, z) for it, z in zip(items, sizes) if z > bpf.MAX_BYTES]
    if big:
        sys.exit("an item alone is over the cap; ask J: %s" % big)
    r2b.MAX_ITEMS, r2b.MAX_BYTES = bpf.MAX_ITEMS, bpf.MAX_BYTES
    n = next(k for k in range(-(-len(items) // bpf.MAX_ITEMS), len(items) + 1) if r2b.partition(sizes, k))
    groups = r2b.partition(sizes, n)
    texts = []
    for k, (i, j) in enumerate(groups, 1):
        name = "P03-r%s-%d" % (a.round, k)
        its = items[i:j]
        body = []
        for pos, (s, t) in enumerate(its, 1):
            body += bpf.render(store, cmap, tmap, s, t, pos)
        txt = "\n".join(["# Pilot round %s, packet %s" % (a.round, name), "", brief + " " + COUNT % (len(its), len(its)),
                         "", "## The items", ""] + body + ["", pk.END, ""])
        if bpf.ROOM_ID.search("\n".join(["# Pilot round", brief] + [ln for ln in body if ln.startswith(("### ", "- "))])):
            sys.exit("%s would serve a room id in a heading or an id position" % name)
        ib = len("\n".join(body).encode("utf-8"))
        if len(its) > bpf.MAX_ITEMS or ib > bpf.MAX_BYTES or pk.CANVAS.search(txt):
            sys.exit("%s breaks a cap or carries a canvas field" % name)
        texts.append((name, txt, ["%s/%s" % x for x in its], ib))
    for name, txt, its, ib in texts:
        print("%-16s %2d items  %7d bytes of item text" % (name, len(its), ib))
    if not a.write:
        return
    to = os.path.join(OUT, "_packets-B2", "round-%s" % a.round)
    if os.path.exists(to) and os.listdir(to):
        sys.exit("%s exists and is not empty" % to)
    rows, sname = pk.load_scheme(OUT, ["scheme_final.jsonl"])
    if sname != "scheme_final.jsonl":
        sys.exit("the shared pages must come from scheme_final.jsonl, not %s" % sname)
    pk.scheme_pages(ROOT, OUT, to, rows, pk.jl(os.path.join(OUT, "families.jsonl")), False)
    man = {}
    for name, txt, its, ib in texts:
        open(os.path.join(to, name + ".md"), "w", encoding="utf-8").write(txt)
        cbi = {}
        for it in its:
            s, t = it.split("/")
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        man[name] = {"items": len(its), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
                     "count_key": "position", "count_exclude": pk.COUNT_04["count_exclude"], "codes_by_item": cbi}
    json.dump(man, open(os.path.join(to, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    json.dump({"seed": a.seed, "scheme": sname, "brief": a.brief or "BRIEF in b2_packets_fleet2.py",
               "fleet_ids": "out/fleet_ids.jsonl", "packets": {name: its for name, _, its, _ in texts}},
              open(os.path.join(OUT, "_analysis", "b2_order_r%s.json" % a.round), "w", encoding="utf-8"), indent=1)
    print("wrote %s: shared pages from %s, %d packets, MANIFEST.json" % (to, sname, len(texts)))


if __name__ == "__main__":
    main()
