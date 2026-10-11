#!/usr/bin/env python3
"""B2a-r1: draw the round-1 hard set and the gold set, each to fit one B2 packet (50 KB, packets.py).

Three sources per set (stage B2 section 1), sizes fixed here and declared in notes-B2.md:
  pair    one exposing second-order theme for each of the 19 confusion pairs (confusions.md's 17 and
          two sibling pairs added at B2a-r1). Round 1 takes the item confusions.md nominated when it
          renders at or under NOM_CAP bytes; otherwise a seeded pick from the pair's pool. Gold takes a
          seeded pick from the pool, never a round-1 item. The pool: second-order themes that hold both
          kinds in scheme_current.jsonl and render at or under CAP bytes.
  bag     rule 0 bags (multiplacement_log.jsonl lines with item_is_a_bag), rendering at or under CAP:
          BAGS per set, seeded. The ten biggest second-order themes of notes-B1.md cannot be served:
          two of them alone pass the ceiling, and all ten hold about 3,500 concepts.
  random  placed second-order themes rendering at or under RCAP bytes, RANDOM per set, seeded.
No second-order theme appears twice across both sets. Seeds are strings, recorded below.

Usage: python3 out/_analysis/b2_select.py [--write]   writes out/_analysis/b2_hardset_r1.tsv and b2_goldset.tsv
"""
import collections, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import packets  # noqa: E402

OUT = os.path.join(ROOT, "out")
NOM_CAP, CAP, RCAP = 2500, 1600, 1500
BAGS, RANDOM = 8, 13
SEED_R1, SEED_GOLD = "b2a-r1:hard", "b2a-r1:gold"
PAIRS = [  # (rank, a, b, nominated item)
    (1, "T3-005", "T3-021", "GreenCorner/t03"), (2, "T3-010", "T3-149", "anarcho_capitalism/t12"),
    (3, "T3-001", "T3-023", "AyyMD/t08"), (4, "T3-028", "T3-070", "england/t03"), (5, "T3-004", "T3-020", "nyu/t01"),
    (6, "T3-002", "T3-033", "dofus/t01"), (7, "T3-015", "T3-075", "trees/t13"), (8, "T3-004", "T3-070", "naruto/t01"),
    (9, "T3-009", "T3-073", "flashtv/t13"), (10, "T3-004", "T3-038", "signal/t01"), (11, "T3-010", "T3-151", "rocketbeans/t06"),
    (12, "T3-010", "T3-150", "AMD/t13"), (13, "T3-010", "T3-024", "4chan/t07"), (14, "T3-009", "T3-043", "stardustcrusaders/t19"),
    (15, "T3-001", "T3-095", "donaldglover/t04"), (16, "T3-188", "T3-087", "megaman/t11"), (17, "T3-044", "T3-082", "DevonUK/t02"),
    (18, "T3-014", "T3-152", "floridagators/t09"), (19, "T3-015", "T3-063", "quebec/t13"),
]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    store = packets.Store(ROOT)
    size = lambda k: len(("\n".join(store.item(k[0], k[1], 99)) + "\n").encode("utf-8"))
    fam = {r["id"]: r["family"] for r in jl(os.path.join(OUT, "scheme.jsonl"))}
    lab2id = {(t["sub"], t["second_order"]): t["theme_id"] for t in store.themes.values()}
    kinds = collections.defaultdict(set)
    for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl")):
        for m in r["members"]:
            kinds[(m["sub"], lab2id.get((m["sub"], m["second_order"]), m["second_order"]))].add(r["theme"])
    used = set()
    r1, gold = [], []
    for rank, a, b, nom in PAIRS:
        nk = tuple(nom.split("/"))
        pool = sorted(k for k, v in kinds.items() if a in v and b in v and size(k) <= CAP)
        pick_r1 = nk if size(nk) <= NOM_CAP else None
        how = "nominated"
        if pick_r1 is None:
            c = [k for k in pool if k not in used and k != nk]
            random.Random("%s:%s/%s" % (SEED_R1, a, b)).shuffle(c)
            pick_r1, how = (c[0], "pool, nominated %s too long" % nom) if c else (None, "none")
        used.add(pick_r1); used.add(nk)
        r1.append((pick_r1, "pair", "%d %s/%s (%s, %s) %s" % (rank, a, b, fam[a], fam[b], how)))
        c = [k for k in pool if k not in used]
        random.Random("%s:%s/%s" % (SEED_GOLD, a, b)).shuffle(c)
        if c:
            used.add(c[0])
            gold.append((c[0], "pair", "%d %s/%s (%s, %s) pool" % (rank, a, b, fam[a], fam[b])))
        else:
            print("NO GOLD ITEM for pair %d %s/%s (pool %d)" % (rank, a, b, len(pool)))
    bagkeys = sorted({(x["sub"], x["theme_id"]) for x in jl(os.path.join(OUT, "multiplacement_log.jsonl"))
                      if x.get("item_is_a_bag")})
    bagkeys = [k for k in bagkeys if size(k) <= CAP and k not in used]
    for seed, dst in ((SEED_R1, r1), (SEED_GOLD, gold)):
        c = [k for k in bagkeys if k not in used]
        random.Random(seed + ":bags").shuffle(c)
        for k in c[:BAGS]:
            used.add(k); dst.append((k, "bag", "rule 0 bag, keeps %s" % ",".join(sorted(kinds.get(k, [])))))
    placed = sorted(k for k in kinds if k in store.themes and size(k) <= RCAP)
    for seed, dst in ((SEED_R1, r1), (SEED_GOLD, gold)):
        c = [k for k in placed if k not in used]
        random.Random(seed + ":random").shuffle(c)
        for k in c[:RANDOM]:
            used.add(k); dst.append((k, "random", "seeded from %d placed themes at or under %d bytes" % (len(placed), RCAP)))
    for name, rows in (("b2_hardset_r1.tsv", r1), ("b2_goldset.tsv", gold)):
        tot = sum(size(k) for k, _, _ in rows if k)
        within = sum(1 for k, s, w in rows if s == "pair" and w.split("(")[1].split(",")[0] == w.split(", ")[1].split(")")[0])
        print("%s: %d items, %d bytes of items; by source %s; pairs inside one family %d" % (
            name, len(rows), tot, dict(collections.Counter(s for _, s, _ in rows)), within))
        if "--write" in sys.argv:
            with open(os.path.join(OUT, "_analysis", name), "w", encoding="utf-8") as f:
                f.write("item\tsource\tbytes\twhy\n")
                for k, s, w in rows:
                    f.write("%s/%s\t%s\t%d\t%s\n" % (k[0], k[1], s, size(k), w))
        else:
            for k, s, w in rows:
                print("  %s/%s\t%s\t%d\t%s" % (k[0], k[1], s, size(k), w))


if __name__ == "__main__":
    main()
