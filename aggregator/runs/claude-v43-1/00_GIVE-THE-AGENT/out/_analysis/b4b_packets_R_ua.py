#!/usr/bin/env python3
"""B4b-p4: packets for the 18 unresolved items of U and A, read again as R's own items (notes-B4.md, "Stratum R, the 18
from U and A read again in R packets"), built into out/_packets-B4/ beside the 46 packets, which stay as built. Both
arms read them.

The same section 10 rules and the same renderer, brief, end line and checks as b4b_packets.py (imported from it):
fleet ids only, at most 15 items, every file under 50 KB, no sibling block, bag flag, stratum or ruling, the cut chosen
so that the largest packet is as small as the caps allow. Names run on from S05-47. The items are the lines of
out/sample-B4-R.jsonl with order 668 or later, in that order.

Before writing: MANIFEST.json holds exactly S05-01 to S05-46 and each file matches its sha256; no S05-47 or later exists;
each item is one of the 500 in the stratum its also_in names, and none is in S05-35 to S05-46. On --write: MANIFEST.json
is kept first as out/_analysis/packets-B4_MANIFEST_before_R_ua.json (refused if that copy exists); the new packets are
written; MANIFEST.json gains their entries and nothing else; out/_analysis/b4b_order_R_ua.json records each new
packet's items.

    python3 out/_analysis/b4b_packets_R_ua.py [--write]
"""
import argparse, hashlib, importlib.util, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
TO = os.path.join(OUT, "_packets-B4")
spec = importlib.util.spec_from_file_location("b4b", os.path.join(OUT, "_analysis", "b4b_packets.py"))
b4b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b4b)
bpf, pk, r2b = b4b.bpf, b4b.pk, b4b.r2b
FIRST = 47


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    man = json.load(open(os.path.join(TO, "MANIFEST.json"), encoding="utf-8"))
    if sorted(man) != ["S05-%02d" % k for k in range(1, FIRST)]:
        sys.exit("MANIFEST.json does not hold exactly S05-01 to S05-46: %s" % sorted(man)[-3:])
    for name, e in man.items():
        if hashlib.sha256(open(os.path.join(TO, name + ".md"), "rb").read()).hexdigest() != e["sha256"]:
            sys.exit("%s no longer matches its MANIFEST entry" % name)
    if any(re.match(r"^S05-(\d{2})\.md$", f) and int(f[4:6]) >= FIRST for f in os.listdir(TO)):
        sys.exit("a packet numbered %d or later already exists" % FIRST)
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    for (s, t), th in store.themes.items():
        for f in ("second_order", "theme_note"):
            v = str(th.get(f) or "")
            nv = re.sub(r"\b(c\d{4}|t\d{2,3})\b", lambda m: cmap.get((s, m.group(1))) or tmap.get((s, m.group(1))) or m.group(1), v)
            if nv != v:
                th[f] = nv
    rr = b4b.jl(os.path.join(OUT, "sample-B4-R.jsonl"))
    rows = sorted((x for x in rr if x["read_in"] == "R" and x["order"] >= 668), key=lambda x: x["order"])
    items = [(x["sub"], x["theme_id"]) for x in rows]
    if len(items) != 18 or len(set(items)) != 18 or [x["order"] for x in rows] != list(range(668, 686)):
        sys.exit("the R record does not hold the 18 from U and A in orders 668 to 685")
    st0 = {(x["sub"], x["theme_id"]): x["stratum"] for x in b4b.jl(os.path.join(OUT, "sample-B4.jsonl"))}
    if any(st0.get((x["sub"], x["theme_id"])) != x["also_in"] for x in rows):
        sys.exit("an item is not among the 500 in the stratum its also_in names")
    inr = set()
    for f in ("b4b_order_R.json", "b4b_order_R_all.json"):
        o = json.load(open(os.path.join(OUT, "_analysis", f), encoding="utf-8"))["packets"]
        inr |= {tuple(i.split("/")) for its in o.values() for i in its}
    if inr & set(items):
        sys.exit("an item is already served in an R packet: %s" % sorted(inr & set(items))[:5])
    blocks = [bpf.render(store, cmap, tmap, s, t, 1) for s, t in items]
    sizes = [len(("\n".join(b) + "\n").encode("utf-8")) for b in blocks]
    head_max = len(("# Items S05-99\n\n" + b4b.BRIEF % (15, 15) + "\n\n## The items\n\n").encode("utf-8")) + len(("\n" + pk.END + "\n").encode("utf-8")) + 64
    r2b.MAX_ITEMS, r2b.MAX_BYTES = b4b.MAX_ITEMS, b4b.CEILING - head_max
    big = [("%s/%s" % it, z) for it, z in zip(items, sizes) if z > r2b.MAX_BYTES]
    if big:
        sys.exit("an item alone is over the packet ceiling (the declared exception would apply): %s" % big)
    n0 = -(-len(items) // b4b.MAX_ITEMS)
    n = next(k for k in range(n0, len(items) + 1) if r2b.partition(sizes, k))
    files, bad, shaped = [], [], []
    for k, (i, j) in enumerate(r2b.partition(sizes, n), FIRST):
        name = "S05-%02d" % k
        its = items[i:j]
        txt, body = b4b.text_of(name, its, blocks[i:j])
        ib = len("\n".join(body).encode("utf-8"))
        if len(its) > b4b.MAX_ITEMS or len(txt.encode("utf-8")) > b4b.CEILING:
            bad.append("%s: %d items, %d bytes" % (name, len(its), len(txt.encode("utf-8"))))
        if [ln for ln in body if b4b.ID_POS.match(ln)]:
            bad.append("%s serves a room id in an id position" % name)
        if pk.CANVAS.search(txt):
            bad.append("%s carries a canvas field" % name)
        leak = b4b.ROOM_ID.findall("\n".join(body))
        if leak:
            shaped.append("%s: %s" % (name, sorted(set(leak))))
        files.append((name, txt, its, ib))
    print("room-id-like strings inside participants' words (reported, not ids): %s" % (shaped or "none"))
    print("packets %d (the least the caps allow is %d); largest item %d bytes" % (len(files), n0, max(sizes)))
    for name, txt, its, ib in files:
        print("%s: %2d items, %6d bytes" % (name, len(its), len(txt.encode("utf-8"))))
    for x in bad:
        print("  STOP: " + x)
    if bad:
        sys.exit("%d packets fail a check" % len(bad))
    if not a.write:
        return
    keep = os.path.join(OUT, "_analysis", "packets-B4_MANIFEST_before_R_ua.json")
    if os.path.exists(keep):
        sys.exit("%s exists" % keep)
    shutil.copyfile(os.path.join(TO, "MANIFEST.json"), keep)
    order = {}
    for name, txt, its, ib in files:
        open(os.path.join(TO, name + ".md"), "w", encoding="utf-8").write(txt)
        cbi = {}
        for s, t in its:
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        man[name] = {"items": len(its), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(), "count_key": "position",
                     "count_exclude": pk.COUNT_04["count_exclude"], "codes_by_item": cbi}
        order[name] = ["%s/%s" % x for x in its]
    json.dump(man, open(os.path.join(TO, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    json.dump({"order_stream": "20261013:R-ua-order", "sample": "out/sample-B4-R.jsonl (orders 668-685)",
               "caps": {"items": b4b.MAX_ITEMS, "bytes": b4b.CEILING}, "packets": order},
              open(os.path.join(OUT, "_analysis", "b4b_order_R_ua.json"), "w", encoding="utf-8"), indent=1)
    print("wrote %d packets into %s; MANIFEST.json now %d entries (%d lines due); the old manifest kept as %s"
          % (len(files), TO, len(man), sum(v["items"] for v in man.values()), os.path.relpath(keep, ROOT)))


if __name__ == "__main__":
    main()
