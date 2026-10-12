#!/usr/bin/env python3
"""B3b: bring the handler's split of the two exhausted packets into the fleet's record (J, 2026-10-12 21:39; the
PI's leg message, ruling 2). Never deletes.

  out/batches-B3.jsonl          kept as out/batches-B3.superseded-<utc>.jsonl; rewritten with B0192 and B0927
                                replaced in place by their halves (out/batches-B3-split.jsonl), the B0019 spares
                                left out (B0019 passed on retry)
  out/_packets-B3/              B0192.md and B0927.md moved to out/_analysis/packets-B3_exhausted_superseded/;
                                the four half packets copied in from out/_packets-B3-split/; MANIFEST.json kept as
                                out/_analysis/packets-B3_MANIFEST_before_split.json and rewritten with the halves'
                                entries in place of the two
Checks first: each pair of halves holds the original's items (as a multiset), agent ids new, replicate kept; each
half packet's sha256 equals its MANIFEST entry and the sha256 its accepted return was served. The halves were
built by tools/packets.py in room ids with no codes_by_item; they are brought in as served, and the script says so.
Dry run unless --write.
"""
import collections, datetime, hashlib, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
PK, SP, RAW = os.path.join(OUT, "_packets-B3"), os.path.join(OUT, "_packets-B3-split"), os.path.join(OUT, "_fleet_raw", "B3")
REPLACED = ("B0192", "B0927")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    write = "--write" in sys.argv
    rows = jl(os.path.join(OUT, "batches-B3.jsonl"))
    split = {b["batch"]: b for b in jl(os.path.join(OUT, "batches-B3-split.jsonl"))}
    man = json.load(open(os.path.join(PK, "MANIFEST.json"), encoding="utf-8"))
    sman = json.load(open(os.path.join(SP, "MANIFEST.json"), encoding="utf-8"))
    agents = {b["agent"] for b in rows}
    bad, new = [], []
    for b in rows:
        if b["batch"] not in REPLACED:
            new.append(b); continue
        halves = [split[b["batch"] + s] for s in "ab"]
        if collections.Counter(b["items"]) != collections.Counter(halves[0]["items"] + halves[1]["items"]):
            bad.append("%s: halves do not hold its items" % b["batch"])
        for h in halves:
            if h["agent"] in agents or h["replicate"] != b["replicate"] or h["original_agent"] != b["agent"]:
                bad.append("%s: agent or replicate wrong" % h["batch"])
            txt = open(os.path.join(SP, h["batch"] + ".md"), "rb").read()
            sha = hashlib.sha256(txt).hexdigest()
            e = sman[h["batch"]]
            if sha != e["sha256"] or e["items"] != h["n_items"]:
                bad.append("%s: packet and MANIFEST entry disagree" % h["batch"])
            if "codes_by_item" not in e or "T2-" not in txt.decode("utf-8"):
                print("note: %s was built by tools/packets.py in room ids, with no codes_by_item; served so" % h["batch"])
            d = os.path.join(RAW, h["batch"])
            acc = [f for f in os.listdir(d) if f.endswith(".jsonl")]
            meta = json.load(open(os.path.join(d, acc[0][:-6] + ".meta.json"), encoding="utf-8")) if len(acc) == 1 else {}
            if len(acc) != 1 or meta.get("packet_sha256") != sha or not meta.get("valid"):
                bad.append("%s: accepted return missing or served another packet" % h["batch"])
            new.append(h)
            print("%s -> %s: %d items, agent %s, replicate %d, gold %s, duplicate %s" % (
                b["batch"], h["batch"], h["n_items"], h["agent"], h["replicate"], h["gold_items"], h["duplicate_items"]))
    if bad:
        sys.exit("\n".join(bad))
    nman = {}
    for k, v in man.items():
        if k in REPLACED:
            for s in "ab":
                nman[k + s] = sman[k + s]
        else:
            nman[k] = v
    print("batches %d -> %d; positions %d -> %d; MANIFEST %d -> %d entries, lines due %d -> %d" % (
        len(rows), len(new), sum(b["n_items"] for b in rows), sum(b["n_items"] for b in new), len(man), len(nman),
        sum(v["items"] for v in man.values()), sum(v["items"] for v in nman.values())))
    if not write:
        return
    utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    an = os.path.join(OUT, "_analysis")
    old = os.path.join(OUT, "batches-B3.superseded-%s.jsonl" % utc)
    os.rename(os.path.join(OUT, "batches-B3.jsonl"), old)
    with open(os.path.join(OUT, "batches-B3.jsonl"), "w", encoding="utf-8") as fh:
        for b in new:
            fh.write(json.dumps(b, ensure_ascii=False) + "\n")
    ex = os.path.join(an, "packets-B3_exhausted_superseded")
    os.makedirs(ex, exist_ok=True)
    for k in REPLACED:
        os.rename(os.path.join(PK, k + ".md"), os.path.join(ex, k + ".md"))
        for s in "ab":
            shutil.copyfile(os.path.join(SP, k + s + ".md"), os.path.join(PK, k + s + ".md"))
    os.rename(os.path.join(PK, "MANIFEST.json"), os.path.join(an, "packets-B3_MANIFEST_before_split.json"))
    json.dump(nman, open(os.path.join(PK, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    print("wrote batches-B3.jsonl (old kept as %s), _packets-B3/ with the halves, the two exhausted packets in %s"
          % (os.path.basename(old), ex))


if __name__ == "__main__":
    main()
