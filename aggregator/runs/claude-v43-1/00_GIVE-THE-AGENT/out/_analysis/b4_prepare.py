#!/usr/bin/env python3
"""B4a-01: what stage B4 computes before any ruling. Reads only; writes out/_analysis/b4_prepare.json.

  gold drop    the seeded gold placements (copy_kind gold in assign_raw.jsonl, told apart by (item, agent,
               replicate) on batches-B3.jsonl's gold tags) and the duplicates' second copies: counted; neither
               enters assign_final.jsonl, which reads the corpus copies only (b3_classes.jsonl)
  transmission section 3's four rows over the 90 items with my answer on record (gold_items.jsonl 40,
               author_items.jsonl 50): readers = the two corpus replicates (b3_classes r1, r2); my answer = the
               latest recheck in rechecks-B2.jsonl ("now"), else the file's third_order; my confidence = the file's.
               agree = same set (Jaccard 1); row 1 readers agree and equal mine; row 2 readers split, I clear;
               row 3 readers split, I arguable; row 4 readers agree and differ from mine. Beside it, for the gold
               items, the seeded copies: the modal set and its share.
  inventory    the contested items (classes 3, 4, 5) by family of the first reader's primary, gloss-only
               (unopened_family) first; the packet plan at about five hundred; the sibling pairs in each packet
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
CAP = 500


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme_final.jsonl"))}
    cls = {"%s/%s" % (c["sub"], c["theme_id"]): c for c in jl(os.path.join(OUT, "b3_classes.jsonl"))}
    raw = jl(os.path.join(OUT, "assign_raw.jsonl"))
    kinds = collections.Counter(x["copy_kind"] for x in raw)
    batches = jl(os.path.join(OUT, "batches-B3.jsonl"))
    gkeys = {(it, b["agent"], b["replicate"]) for b in batches for it in b["gold_items"]}
    gl = [x for x in raw if x["copy_kind"] == "gold"]
    on_keys = sum(("%s/%s" % (x["sub"], x["theme_id"]), x["agent"], x["replicate"]) in gkeys for x in gl)
    R = {"gold_drop": {"gold_lines": len(gl), "on_batches_gold_keys": on_keys, "gold_keys": len(gkeys),
                       "duplicate_second_copies": kinds["duplicate"], "corpus_lines": kinds["corpus"],
                       "items": len(cls)}}
    # ---- transmission
    rech = {}
    for r in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        k = "%s/%s" % (r["sub"], r["theme_id"])
        if k not in rech or r["t"] >= rech[k]["t"]:
            rech[k] = r
    mine = {}
    for src in ("gold_items.jsonl", "author_items.jsonl"):
        for r in jl(os.path.join(OUT, src)):
            k = r["item"]
            now = rech[k]["now"] if k in rech and rech[k].get("now") else r["third_order"]
            mine[k] = {"set": now, "file_set": r["third_order"], "confidence": r["confidence"],
                       "set_from": "recheck" if k in rech and rech[k].get("now") else "file", "src": src}
    seeded = collections.defaultdict(list)
    for x in gl:
        seeded["%s/%s" % (x["sub"], x["theme_id"])].append(tuple(sorted(x["third_order"])))
    rows = []
    for k, m in sorted(mine.items()):
        c = cls[k]
        r1, r2 = c["r1"], c["r2"]
        agree = set(r1) == set(r2)
        if agree and set(r1) == set(m["set"]):
            row = 1
        elif agree:
            row = 4
        else:
            row = 2 if m["confidence"] == "clear" else 3
        sd = collections.Counter(seeded.get(k, []))
        mode = sd.most_common(1)[0] if sd else None
        rows.append({"item": k, "src": m["src"], "row": row, "mine": m["set"], "mine_file": m["file_set"],
                     "set_from": m["set_from"], "confidence": m["confidence"], "r1": r1, "r2": r2,
                     "family": fam.get(m["set"][0]) if m["set"] else None, "class": c["class"],
                     "seeded_n": sum(sd.values()), "seeded_mode": list(mode[0]) if mode else None,
                     "seeded_mode_share": mode[1] / sum(sd.values()) if mode else None})
    R["transmission"] = rows
    R["transmission_counts"] = {src: dict(collections.Counter(r["row"] for r in rows if r["src"] == src))
                                for src in ("gold_items.jsonl", "author_items.jsonl")}
    # ---- inventory and packets
    cont = [c for c in cls.values() if c["class"] in (3, 4, 5)]

    def famkey(c):
        p = (c["r1"] or c["r2"] or [None])[0]
        return fam.get(p, "G99")
    for c in cont:
        c["_fam"] = famkey(c)
        c["_pair"] = "|".join(sorted({(c["r1"] or [""])[0], (c["r2"] or [""])[0]} - {""}))
    order = sorted(cont, key=lambda c: (not c["flags"].get("unopened_family"), c["_fam"], c["_pair"], c["sub"].lower(), c["theme_id"]))
    byfam = collections.Counter(c["_fam"] for c in cont)
    R["inventory"] = {"contested": len(cont), "by_class": dict(collections.Counter(c["class"] for c in cont)),
                      "unopened_family": sum(bool(c["flags"].get("unopened_family")) for c in cont),
                      "by_family": dict(sorted(byfam.items()))}
    # packets of at most CAP items (section 7): gloss-only first, then whole families poured in order; a family that
    # does not fit closes the packet when the packet already holds CAP - 150 or more, else it is cut at CAP within
    # its pairs' order and runs on into the next packet
    packets = []
    gloss = [c for c in order if c["flags"].get("unopened_family")]
    rest = [c for c in order if not c["flags"].get("unopened_family")]
    cur = list(gloss)
    for f in sorted({c["_fam"] for c in rest}):
        items = [c for c in rest if c["_fam"] == f]
        while items:
            room = CAP - len(cur)
            if len(items) <= room:
                cur += items; items = []
            elif len(cur) >= CAP - 150:
                packets.append(cur); cur = []
            else:
                cur += items[:room]; items = items[room:]
                packets.append(cur); cur = []
    if cur:
        packets.append(cur)
    assert all(len(p) <= CAP for p in packets) and sum(len(p) for p in packets) == len(cont)
    R["packets"] = []
    for n, p in enumerate(packets, 1):
        pairs = collections.Counter(c["_pair"] for c in p if c["class"] == 3)
        R["packets"].append({"packet": n, "items": ["%s/%s" % (c["sub"], c["theme_id"]) for c in p],
                             "n": len(p), "families": dict(collections.Counter(c["_fam"] for c in p)),
                             "classes": dict(collections.Counter(c["class"] for c in p)),
                             "gloss_only": sum(bool(c["flags"].get("unopened_family")) for c in p),
                             "pairs_top": pairs.most_common(25)})
    json.dump(R, open(os.path.join(OUT, "_analysis", "b4_prepare.json"), "w", encoding="utf-8"), indent=1)
    print("gold drop: %s" % R["gold_drop"])
    print("transmission rows: %s" % R["transmission_counts"])
    print("rechecked answers used: %d of 90" % sum(r["set_from"] == "recheck" for r in rows))
    print("inventory: %s" % R["inventory"])
    for p in R["packets"]:
        print("packet %d: %d items, families %s, classes %s, gloss-only %d" % (p["packet"], p["n"], p["families"], p["classes"], p["gloss_only"]))
    print("packet 1 top pairs: %s" % R["packets"][0]["pairs_top"])


if __name__ == "__main__":
    main()
