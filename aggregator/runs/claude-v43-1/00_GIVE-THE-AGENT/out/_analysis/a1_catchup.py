"""Stage A1 catch-up pass (J's rulings of 7 October 2026, ruling 1): which rooms were not served case.md or
brief.md whole in A1, in what order to read them, and in what blocks.

python3 out/_analysis/a1_catchup.py [--write]
Reads only out/ files (the read log _mem_reads-A1.jsonl, the diary, order-A1.txt, the reconciliation table)
and the byte size of package/<sub>/case.md and brief.md (os.stat; no content is read; each size is printed
with its path). Prints the four tiers and the blocks. With --write, appends the blocks to out/order-A1.txt
as comment lines `#<block><TAB><sub>` (the checker and mem.py skip lines that open with '#', so the A1 order
keeps every room once), and writes out/_analysis/catchup-A1.tsv (block, tier, sub, case bytes, brief bytes).

Tiers, hardest-cut first:
  1 concepts partly served: before the room's first `noted` diary line, the codes calls for the room served
    fewer lines than the room's concept total (union of the served ranges);
  2 more than 170 concepts;
  3 the note's `ended:` concept differs from the rule's by more than an hour (verdict `differs`);
  4 the rest.
Within a tier, the declared A1 order. Blocks: about 25 rooms or 700 KB of case.md and brief.md, whichever
comes first.
"""
import collections, glob, json, os, sys

OUT = "out"
mem = [json.loads(l) for l in open(os.path.join(OUT, "_mem_reads-A1.jsonl"), encoding="utf-8")]
order = [l.rstrip("\n").split("\t")[1] for l in open(os.path.join(OUT, "order-A1.txt"), encoding="utf-8")
         if "\t" in l and not l.startswith("#")]
oset = set(order)


def room_of(r):
    for x in list(r.get("args") or []) + [(r.get("opts") or {}).get("sub")]:
        if isinstance(x, str) and x in oset:
            return x
    return None


def covered(calls):
    """lines served, as the union of [offset, offset+lines) ranges, and the file's total"""
    seen, total = set(), 0
    for r in calls:
        if r.get("refused"):
            continue
        o, n = r.get("offset") or 0, r.get("lines") or 0
        seen.update(range(o, o + n))
        total = max(total, r.get("total") or 0)
    return len(seen), total


noted_at = {}
for f in glob.glob(os.path.join(OUT, "diary", "A1-*.jsonl")):
    for l in open(f, encoding="utf-8"):
        d = json.loads(l)
        if d.get("kind") == "note" and d.get("text", "").strip().endswith("noted"):
            for s in d.get("ids") or []:
                if s not in noted_at or d["t"] < noted_at[s]:
                    noted_at[s] = d["t"]

by = collections.defaultdict(list)
for r in mem:
    s = room_of(r)
    if s and r.get("verb") in ("case", "brief", "codes"):
        by[(r["verb"], s)].append(r)

whole = {}
for s in order:
    c = covered(by[("case", s)])
    b = covered(by[("brief", s)])
    whole[s] = (c[1] > 0 and c[0] >= c[1]) and (b[1] > 0 and b[0] >= b[1])

partly, nconc = set(), {}
for s in order:
    calls = [r for r in by[("codes", s)] if s in noted_at and r["t"] <= noted_at[s]]
    n, t = covered(calls)
    nconc[s] = t
    if t and n < t:
        partly.add(s)
# a room's concept total from the whole-store dump at A1b-19 when the early calls carry none
for s in order:
    if not nconc[s]:
        nconc[s] = covered(by[("codes", s)])[1]

differs = set()
for l in open(os.path.join(OUT, "_analysis", "organizing_end-reconcile-A1.tsv"), encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) == 6 and p[5] == "differs":
        differs.add(p[0])

todo = [s for s in order if not whole[s]]
tier = {}
for s in todo:
    tier[s] = 1 if s in partly else 2 if nconc[s] > 170 else 3 if s in differs else 4
ranked = sorted(todo, key=lambda s: (tier[s], order.index(s)))


def size(s, name):
    p = os.path.join("package", s, name)
    return os.path.getsize(p) if os.path.exists(p) else 0


blocks, cur, cb, b = [], [], 0, 20
for s in ranked:
    sz = size(s, "case.md") + size(s, "brief.md")
    if cur and (len(cur) >= 25 or cb + sz > 700_000):
        blocks.append(cur)
        cur, cb = [], 0
    cur.append(s)
    cb += sz
if cur:
    blocks.append(cur)

print("rooms served case.md and brief.md whole in A1: %d; to read: %d" % (sum(whole.values()), len(todo)))
print("tiers:", dict(collections.Counter(tier.values())), "(1 concepts partly served, 2 over 170 concepts,"
      " 3 ended differs, 4 rest)")
print("concepts partly served, all rooms: %d; among rooms to read: %d" % (len(partly), len(partly & set(todo))))
for i, bl in enumerate(blocks):
    kb = sum(size(s, "case.md") + size(s, "brief.md") for s in bl) / 1000
    print("block %d: %d rooms, %.0f KB, tiers %s" % (20 + i, len(bl), kb, sorted({tier[s] for s in bl})))
if "--write" in sys.argv:
    with open(os.path.join(OUT, "order-A1.txt"), "a", encoding="utf-8") as f:
        f.write("# Catch-up pass (J's ruling 1, 7 October 2026): case.md and brief.md read whole for every room\n"
                "# not served them whole in A1. Blocks 20 onward, one comment line per room, `#<block><TAB><sub>`.\n"
                "# The lines open with '#' so that the A1 order above keeps every room once.\n")
        for i, bl in enumerate(blocks):
            for s in bl:
                f.write("#%d\t%s\n" % (20 + i, s))
    with open(os.path.join(OUT, "_analysis", "catchup-A1.tsv"), "w", encoding="utf-8") as f:
        f.write("block\ttier\tsub\tcase_bytes\tbrief_bytes\tcase_path\tbrief_path\n")
        for i, bl in enumerate(blocks):
            for s in bl:
                f.write("%d\t%d\t%s\t%d\t%d\tpackage/%s/case.md\tpackage/%s/brief.md\n"
                        % (20 + i, tier[s], s, size(s, "case.md"), size(s, "brief.md"), s, s))
    print("written")
