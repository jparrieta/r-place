#!/usr/bin/env python3
"""B4b: the blind sample's packets, as declared in notes-B4.md ("The blind sample, built at B4b"), built once for both
arms (DeepSeek V4.1 Flash on the fleet's route; OpenAI gpt-6-astra on J's computer).

tools/packets.py B4 writes room ids, which J's fleet-id ruling forbids (the QB3-003 fault), so this builder renders
the items with stage B2's renderer (b2_packets_fleet.py), as stages B2 and B3 were built:

  _packets-B4/index.md, G01.md ... G21.md   packets.py's scheme_pages on scheme_final.jsonl, no exemplars, each under
                                            50 KB (checked byte for byte against _packets-B3's pages)
  _packets-B4/S05-NN.md                     the items of out/sample-B4.jsonl in its serving order, cut consecutively;
                                            title, the brief with the packet's own item count, the items (heading with
                                            the room and the fleet theme id, label, note, each concept under its fleet
                                            id with the participants' words), the end line; no sibling block, no bag
                                            flag, no stratum, no ruling, no reader's line
  _packets-B4/MANIFEST.json                 per packet: items, bytes, item_bytes, sha256, count key and excludes,
                                            codes_by_item {fleet theme id: [fleet code ids]}

Caps: at most 15 items a packet and every packet file under 50 KB (51,200 bytes), the cut chosen so that the largest
packet is as small as the caps allow. The build stops on a room id in an id position (a heading or a concept line), a
canvas field, a broken cap, or a rule 0 in RETURN-B4.md that is not the contract's; it reports room-id-like strings
inside participants' words. Also writes out/_analysis/b4b_order.json (packet -> items), outside the packets folder.

    python3 out/_analysis/b4b_packets.py [--write]
"""
import argparse, hashlib, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)
pk, r2b = bpf.pk, bpf.r2b

MAX_ITEMS, CEILING = 15, 50 * 1024
ROOM_ID = re.compile(r"(?<![A-Za-z0-9])[ct]\d{2,4}(?![0-9])")
ID_POS = re.compile(r"^(### \d+\. r/\S+ [ct]\d|- [ct]\d{4}\s)")
BRIEF = ("Place each second-order theme below onto the scheme, one line per item in the form the return specification "
         "gives, the prediction line first and your second pass after your last item. Items are numbered by position. "
         "Each item is headed by its room and its id, and each concept by its id; copy ids exactly as written here. "
         "This packet is complete in itself: it holds %d items; return %d lines, then your second pass, then the end "
         "marker.")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def text_of(name, its, blocks):
    body = []
    for pos, b in enumerate(blocks, 1):
        body += [re.sub(r"^### \d+\. ", "### %d. " % pos, b[0])] + b[1:]
    txt = "\n".join(["# Items %s" % name, "", BRIEF % (len(its), len(its)), "", "## The items", ""] + body + ["", pk.END, ""])
    return txt, body


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    # rule 0 in RETURN-B4.md must be the contract's words
    ret = open(os.path.join(OUT, "RETURN-B4.md"), encoding="utf-8").read()
    if pk.rule0(ROOT) not in " ".join(ret.split()):
        sys.exit("RETURN-B4.md does not carry rule 0 in the contract's words")
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    translated = []
    for (s, t), th in store.themes.items():                # a coder's label or note naming a room id: fleet id served
        for f in ("second_order", "theme_note"):
            v = str(th.get(f) or "")
            nv = re.sub(r"\b(c\d{4}|t\d{2,3})\b", lambda m: cmap.get((s, m.group(1))) or tmap.get((s, m.group(1))) or m.group(1), v)
            if nv != v:
                th[f] = nv
                translated.append("%s/%s %s" % (s, t, f))
    sample = sorted(jl(os.path.join(OUT, "sample-B4.jsonl")), key=lambda r: r["order"])
    items = [(r["sub"], r["theme_id"]) for r in sample]
    if len(set(items)) != len(items) or len(items) != 500:
        sys.exit("sample-B4.jsonl is not 500 distinct items")
    blocks = [bpf.render(store, cmap, tmap, s, t, 1) for s, t in items]
    sizes = [len(("\n".join(b) + "\n").encode("utf-8")) for b in blocks]
    head_max = len(("# Items S05-99\n\n" + BRIEF % (15, 15) + "\n\n## The items\n\n").encode("utf-8")) + len(("\n" + pk.END + "\n").encode("utf-8")) + 64
    r2b.MAX_ITEMS, r2b.MAX_BYTES = MAX_ITEMS, CEILING - head_max
    big = [("%s/%s" % it, z) for it, z in zip(items, sizes) if z > r2b.MAX_BYTES]
    if big:
        sys.exit("an item alone is over the packet ceiling (the declared exception would apply): %s" % big)
    n0 = -(-len(items) // MAX_ITEMS)
    n = next(k for k in range(n0, len(items) + 1) if r2b.partition(sizes, k))
    groups = r2b.partition(sizes, n)
    files, bad, shaped = [], [], []
    for k, (i, j) in enumerate(groups, 1):
        name = "S05-%02d" % k
        its = items[i:j]
        txt, body = text_of(name, its, blocks[i:j])
        b = txt.encode("utf-8")
        ib = len("\n".join(body).encode("utf-8"))
        if len(its) > MAX_ITEMS or len(b) > CEILING:
            bad.append("%s: %d items, %d bytes" % (name, len(its), len(b)))
        if [ln for ln in body if ID_POS.match(ln)]:
            bad.append("%s serves a room id in an id position" % name)
        if pk.CANVAS.search(txt):
            bad.append("%s carries a canvas field" % name)
        leak = ROOM_ID.findall("\n".join(body))
        if leak:
            shaped.append("%s: %s" % (name, sorted(set(leak))))
        files.append((name, txt, its, ib))
    print("coder labels and notes with a room id served as its fleet id: %s" % ([x for x in translated if tuple(x.split(" ")[0].split("/")) in set(items)] or "none in the sample"))
    print("room-id-like strings inside participants' words (reported, not ids): %s" % (shaped or "none"))
    print("packets %d (the least the caps allow is %d); items per packet %d to %d; bytes per packet %d to %d; largest item %d bytes"
          % (len(files), n0, min(len(f[2]) for f in files), max(len(f[2]) for f in files),
             min(len(f[1].encode("utf-8")) for f in files), max(len(f[1].encode("utf-8")) for f in files), max(sizes)))
    for x in bad[:20]:
        print("  STOP: " + x)
    if bad:
        sys.exit("%d packets fail a check" % len(bad))
    if not a.write:
        return
    to = os.path.join(OUT, "_packets-B4")
    if os.path.exists(to) and os.listdir(to):
        sys.exit("%s exists and is not empty" % to)
    rows, sname = pk.load_scheme(OUT, ["scheme_final.jsonl"])
    pk.scheme_pages(ROOT, OUT, to, rows, pk.jl(os.path.join(OUT, "families.jsonl")), False)
    shared = sorted(f for f in os.listdir(to) if f.endswith(".md"))
    over = [f for f in shared if os.path.getsize(os.path.join(to, f)) > CEILING]
    if over:
        sys.exit("shared pages over 50 KB: %s" % over)
    same = [f for f in shared if os.path.exists(os.path.join(OUT, "_packets-B3", f)) and
            open(os.path.join(to, f), "rb").read() == open(os.path.join(OUT, "_packets-B3", f), "rb").read()]
    man, order = {}, {}
    for name, txt, its, ib in files:
        open(os.path.join(to, name + ".md"), "w", encoding="utf-8").write(txt)
        cbi = {}
        for s, t in its:
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        man[name] = {"items": len(its), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                     "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(), "count_key": "position",
                     "count_exclude": pk.COUNT_04["count_exclude"], "codes_by_item": cbi}
        order[name] = ["%s/%s" % x for x in its]
    json.dump(man, open(os.path.join(to, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    json.dump({"seed": 20261013, "sample": "out/sample-B4.jsonl", "fleet_ids": "out/fleet_ids.jsonl", "scheme": sname,
               "caps": {"items": MAX_ITEMS, "bytes": CEILING}, "packets": order},
              open(os.path.join(OUT, "_analysis", "b4b_order.json"), "w", encoding="utf-8"), indent=1)
    print("wrote %s: %d shared pages (%d identical to _packets-B3's), %d packets, MANIFEST.json (%d lines due)"
          % (to, len(shared), len(same), len(files), sum(v["items"] for v in man.values())))


if __name__ == "__main__":
    main()
