#!/usr/bin/env python3
"""B3b: J's ruling at QB3-003 (b), 22:30 Berlin. The four halves of the exhausted packets B0192 and B0927, which the
handler built with tools/packets.py in room ids and with no codes_by_item, are rebuilt in fleet ids with the main
build's renderer (b3_packets_fleet2.py: same brief, sibling blocks, item renderer, checks; codes_by_item in the
MANIFEST so fleet.py checks concepts), under new batch names so no folder holds two accepted returns:

  B0192a -> B0192c   B0192b -> B0192d   B0927a -> B0927c   B0927b -> B0927d

Each new batch keeps its half's items in the same order, rooms, gold copy, duplicate and replicate; it gets a new
agent (the next free ids) and `supersedes` naming the room-id half. Never deletes; with --write:
  out/batches-B3.jsonl         kept as out/batches-B3.superseded-<utc>.jsonl, rewritten with the four in place
  out/_packets-B3/B0192a.md ...  moved to out/_analysis/packets-B3_roomid_halves_superseded/
  out/_packets-B3/MANIFEST.json  kept as out/_analysis/packets-B3_MANIFEST_before_fleet_halves.json, rewritten
  out/_fleet_raw/B3/B0192a ...   moved to out/_analysis/fleet_raw-B3_roomid_halves_superseded/
"""
import datetime, hashlib, importlib.util, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
spec = importlib.util.spec_from_file_location("f2", os.path.join(AN, "b3_packets_fleet2.py"))
f2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f2)
bpf, pk = f2.bpf, f2.pk
NEW = {"B0192a": "B0192c", "B0192b": "B0192d", "B0927a": "B0927c", "B0927b": "B0927d"}


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def render(store, cmap, tmap, b):
    """b3_packets_fleet2.main's packet text for one batch line, word for word in its parts."""
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
            bl = bl[:2] + [f2.BAGLINE, ""] + bl[2:]
        body += bl
    ib = len("\n".join(body).encode("utf-8"))
    txt = "\n".join(["# Batch %s, replicate %d" % (name, rep), "",
                     f2.BRIEF + " It holds %d items; return %d lines, then your second pass, then the end marker."
                     % (len(items), len(items)), ""] + sib + ["## The items", ""] + body + ["", pk.END, ""])
    return txt, ib


def main():
    write = "--write" in sys.argv
    cmap, tmap = bpf.load_ids()
    store = pk.Store(ROOT, OUT)
    for (s, t), th in store.themes.items():
        for f in ("second_order", "theme_note"):
            v = str(th.get(f) or "")
            th[f] = re.sub(r"\b(c\d{4}|t\d{2,3})\b",
                           lambda m: cmap.get((s, m.group(1))) or tmap.get((s, m.group(1))) or m.group(1), v)
    real = {}
    for (r, x) in list(cmap) + list(tmap):
        real.setdefault(r, set()).add(x)
    rows = jl(os.path.join(OUT, "batches-B3.jsonl"))
    if any(b["batch"] in NEW.values() for b in rows):
        sys.exit("batches-B3.jsonl already holds the rebuilt halves")
    nxt = max(int(b["agent"][1:]) for b in rows) + 1
    out_rows, built, bad = [], {}, []
    for b in rows:
        if b["batch"] not in NEW:
            out_rows.append(b); continue
        nb = dict(b, batch=NEW[b["batch"]], agent="a%04d" % nxt, reissue=0,
                  supersedes="%s (built by tools/packets.py in room ids with no codes_by_item; rebuilt in fleet ids, J at QB3-003)" % b["batch"])
        nxt += 1
        txt, ib = render(store, cmap, tmap, nb)
        nb["item_bytes"] = ib
        if len(nb["items"]) > f2.MAX_ITEMS or ib > f2.MAX_BYTES:
            bad.append("%s: %d items, %d item bytes" % (nb["batch"], len(nb["items"]), ib))
        ids_here = set().union(*(real.get(r, set()) for r in nb["rooms"]))
        m = set(f2.ROOM_ID.findall(txt))
        if m & ids_here:
            bad.append("%s carries room ids of its rooms %s" % (nb["batch"], sorted(m & ids_here)[:8]))
        if pk.CANVAS.search(txt):
            bad.append("%s carries a canvas field" % nb["batch"])
        if "T2-" not in txt:
            bad.append("%s has no fleet theme id" % nb["batch"])
        cbi = {}
        for k in nb["items"]:
            s, t = k.split("/")
            cbi[tmap[(s, t)]] = [cmap[(s, c)] for c in store.themes[(s, t)].get("code_ids") or [] if (s, c) in store.codes]
        built[nb["batch"]] = (b["batch"], txt, {"items": len(nb["items"]), "bytes": len(txt.encode("utf-8")), "item_bytes": ib,
                                                "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest(),
                                                "count_key": "position", "count_exclude": pk.COUNT_04["count_exclude"],
                                                "codes_by_item": cbi})
        out_rows.append(nb)
        print("%s -> %s: agent %s, replicate %d, %d items, %d item bytes, gold %s, duplicate %s, shaped strings %s" % (
            b["batch"], nb["batch"], nb["agent"], nb["replicate"], len(nb["items"]), ib, nb["gold_items"],
            nb["duplicate_items"], sorted(m) or "none"))
    for x in bad:
        print("STOP: " + x)
    if bad:
        sys.exit(1)
    print("batches %d, positions %d" % (len(out_rows), sum(b["n_items"] for b in out_rows)))
    if not write:
        return
    utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    os.rename(os.path.join(OUT, "batches-B3.jsonl"), os.path.join(OUT, "batches-B3.superseded-%s.jsonl" % utc))
    with open(os.path.join(OUT, "batches-B3.jsonl"), "w", encoding="utf-8") as fh:
        for b in out_rows:
            fh.write(json.dumps(b, ensure_ascii=False) + "\n")
    pdir = os.path.join(OUT, "_packets-B3")
    sp = os.path.join(AN, "packets-B3_roomid_halves_superseded")
    rw = os.path.join(AN, "fleet_raw-B3_roomid_halves_superseded")
    os.makedirs(sp, exist_ok=True); os.makedirs(rw, exist_ok=True)
    man = json.load(open(os.path.join(pdir, "MANIFEST.json"), encoding="utf-8"))
    shutil.copyfile(os.path.join(pdir, "MANIFEST.json"), os.path.join(AN, "packets-B3_MANIFEST_before_fleet_halves.json"))
    nman = {}
    inv = {v: k for k, v in NEW.items()}
    for k, v in man.items():
        if k in NEW:
            nman[NEW[k]] = built[NEW[k]][2]
        else:
            nman[k] = v
    for new, (old, txt, _) in built.items():
        os.rename(os.path.join(pdir, old + ".md"), os.path.join(sp, old + ".md"))
        open(os.path.join(pdir, new + ".md"), "w", encoding="utf-8").write(txt)
        os.rename(os.path.join(OUT, "_fleet_raw", "B3", old), os.path.join(rw, old))
    json.dump(nman, open(os.path.join(pdir, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    print("wrote batches-B3.jsonl (old kept as batches-B3.superseded-%s.jsonl); packets %s; MANIFEST %d entries, %d lines due; "
          "room-id packets in %s; their raw folders in %s" % (utc, sorted(built), len(nman), sum(v["items"] for v in nman.values()), sp, rw))


if __name__ == "__main__":
    main()
