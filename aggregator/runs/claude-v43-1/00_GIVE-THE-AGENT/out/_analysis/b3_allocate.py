#!/usr/bin/env python3
"""B3a: the allocation (stage B3 section 1.2), written to out/batches-B3.jsonl with --write.

Whole rooms, crossed with readers, at R = 2. For each replicate the analysed rooms are shuffled under the seed and
packed in that order (next fit) into batches of at most CAP items and BUDGET bytes of rendered text (the items in
fleet ids as b2_packets_fleet.py renders them, and the rooms' sibling blocks), so that a batch is one file under
FLEET.md's 50 KB ceiling; a room larger than either is a batch by itself, served in parts to one reader (QB3-001).
Each batch is one reader, so a room meets two readers, one per replicate, and never the same one.

Into each batch: one duplicate item (an item of its own, twice, the copies at least a quarter of the batch
apart); gold copies at one per 20 items (expected; at most two per batch; never a gold item whose room is in the
batch; never twice in a batch), drawn round-robin from a seeded order of gold_items.jsonl's 40 so each is seeded
about as often as the others, and placed so that no two readers hold the same gold item at the same position.
Positions are a seeded shuffle of everything the reader answers, interleaved across rooms. The batch's `items` is
that order (gold copies and the duplicate's second copy included), so n_items counts every position (QB3-001).
`gold_items` and `duplicate_items` tag them; `bag_flags` names the batch's items among notes-B1.md's ten biggest
bags (the instruction unchanged: place from the concepts, not from the coder's grouping).

The gates run before anything is written: no room meets the same reader twice; the room-batch graph is one
component (redrawn under a new seed suffix on failure, the redraws counted). The coverage assertion is computed
from the batches: each replicate's rooms are the analysed set and its items (copies aside) are the store's
second-order themes of that set. Dispatch order: a seeded shuffle of the batch ids, in two groups (the first
GROUP1 batches, then the rest); written to out/_analysis/b3_dispatch_order.json.

    python3 out/_analysis/b3_allocate.py --seed N [--write]
"""
import argparse, collections, importlib.util, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)

CAP, BUDGET, CEILING, HEAD, PART_BYTES, BIG_GAP = 40, 44000, 50 * 1024, 2600, 160000, 6000
R, GOLD_RATE, GOLD_MAX, GROUP1 = 2, 1 / 20, 2, 60
BAGS = ["2007scape/t04", "theblackvoid/t12", "ainbowroad/t04", "ainbowroad/t03", "ainbowroad/t07", "sweden/t01",
        "leagueoflegends/t02", "theblackvoid/t09", "ainbowroad/t11", "dota2/t05"]


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()] if os.path.exists(p) else []


def connected(edges):
    adj = collections.defaultdict(set)
    for a, b in edges:
        adj["r:" + a].add("b:" + b); adj["b:" + b].add("r:" + a)
    seen, stack = set(), [next(iter(adj))]
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n); stack.extend(adj[n] - seen)
    return len(seen) == len(adj)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    cmap, tmap = bpf.load_ids()
    store = bpf.pk.Store(ROOT, OUT)
    dropped = {r.get("sub") for r in jl(os.path.join(OUT, "dropped.jsonl"))}
    rooms = sorted(s for s in store.by_sub if s not in dropped)
    size, sib = {}, {}
    for s in rooms:
        sib[s] = sum(len(("- %s %s\n" % (tmap[(s, t["theme_id"])], t.get("second_order") or "")).encode("utf-8")) for t in store.by_sub[s]) + 120
        for t in store.by_sub[s]:
            size[(s, t["theme_id"])] = len("\n".join(bpf.render(store, cmap, tmap, s, t["theme_id"], 1)).encode("utf-8")) + 60
    room_items = {s: sorted(t["theme_id"] for t in store.by_sub[s]) for s in rooms}
    room_bytes = {s: sum(size[(s, t)] for t in room_items[s]) + sib[s] for s in rooms}
    expected = {(s, t) for s in rooms for t in room_items[s]}
    gold = [g["item"] for g in jl(os.path.join(OUT, "gold_items.jsonl"))]
    gsize = {g: size[tuple(g.split("/"))] for g in gold}

    redraws = 0
    while True:
        suffix = "" if redraws == 0 else ":redraw%d" % redraws
        rng = random.Random("%d%s" % (a.seed, suffix))
        batches = []
        for rep in range(1, R + 1):
            order = rooms[:]
            random.Random("%d%s:rep%d" % (a.seed, suffix, rep)).shuffle(order)
            # a room over the budget opens a batch served in parts; it first takes one ordinary room, so that it is
            # not an island in the room-batch graph (gate 2), then more rooms up to PART_ITEMS and PART_BYTES (or
            # the large room's own size and 12 KB more); a room over the item cap takes at most 3 items beside it
            # first fit over the open batches, in the shuffled room order; a room that leaves less than BIG_GAP
            # bytes or 4 items of room under the budget or the cap is large: it opens a batch served in parts
            small, parts = [], []           # [rooms, n, bytes, item limit, byte limit, rooms taken beside]
            for s in order:
                n, z = len(room_items[s]), room_bytes[s]
                if n > CAP - 4 or z > BUDGET - BIG_GAP:
                    parts.append([[s], n, z, max(CAP, n + 3), max(PART_BYTES, z + 12000), 0])
                    continue
                lonely = [p for p in parts if p[5] == 0 and p[1] + n <= p[3] and p[2] + z <= p[4]]
                fit = lonely or [p for p in small if p[1] + n <= p[3] and p[2] + z <= p[4]]
                if fit:
                    p = fit[0]
                    p[0].append(s); p[1] += n; p[2] += z; p[5] += 1
                else:
                    small.append([[s], n, z, CAP, BUDGET, 0])
            batches += [(rep, p[0], False) for p in small] + [(rep, p[0], True) for p in parts]
        edges = [(s, "%d:%d" % (i, rep)) for i, (rep, rs, _) in enumerate(batches) for s in rs]
        if connected(edges):
            break
        redraws += 1
        if redraws > 20:
            adj = collections.defaultdict(set)
            for x, y in edges:
                adj["r:" + x].add("b:" + y); adj["b:" + y].add("r:" + x)
            comps, seen = [], set()
            for n0 in adj:
                if n0 in seen:
                    continue
                c, st = set(), [n0]
                while st:
                    n = st.pop()
                    if n not in c:
                        c.add(n); st.extend(adj[n] - c)
                seen |= c; comps.append(c)
            comps.sort(key=len)
            print("components %d; the smallest: %s" % (len(comps), [sorted(c)[:6] for c in comps[:4]]))
            print("rooms in no batch: %s" % sorted(set(rooms) - {x for x, _ in edges})[:10])
            sys.exit("the room-batch graph stayed in pieces over 20 redraws")

    gold_order = gold[:]
    random.Random("%d%s:gold" % (a.seed, suffix)).shuffle(gold_order)
    gi = 0
    gold_pos = collections.defaultdict(set)
    rows, total_pos, gold_copies, split_batches = [], 0, 0, 0
    for k, (rep, rs, alone) in enumerate(batches, 1):
        own = [(s, t) for s in rs for t in room_items[s]]
        room_b = sum(room_bytes[s] for s in rs)
        free = CEILING - HEAD - room_b
        # gold copies
        e = len(own) * GOLD_RATE
        n_gold = min(GOLD_MAX, int(e) + (1 if rng.random() < e - int(e) else 0))
        picks = []
        tries = 0
        while len(picks) < n_gold and tries < len(gold_order) * 2:
            g = gold_order[gi % len(gold_order)]; gi += 1; tries += 1
            if g.split("/")[0] in rs or g in picks:
                continue
            if not alone and gsize[g] > free:
                continue
            picks.append(g); free -= gsize[g]
        # the duplicate: an item of the batch's own, small enough to keep a one-file batch under the ceiling
        cand = [it for it in own if alone or size[it] <= free]
        dup = rng.choice(cand) if cand else rng.choice(own)
        entries = ["%s/%s" % it for it in own] + picks + ["%s/%s" % dup]
        n = len(entries)
        for attempt in range(500):
            rng.shuffle(entries)
            dpos = [i for i, x in enumerate(entries) if x == "%s/%s" % dup]
            if len(dpos) == 2 and dpos[1] - dpos[0] < max(3, n // 4):
                continue
            # a gold copy: not at a position another reader holds it at; the corpus copy of a gold item in its own
            # room's batch is not a seeded copy and is not checked here
            gpos = [(x, i + 1) for i, x in enumerate(entries) if x in picks]
            if any(p in gold_pos[x] for x, p in gpos):
                continue
            break
        else:
            sys.exit("batch %d: no order met the duplicate spacing and the gold positions in 500 shuffles" % k)
        for x, p in gpos:
            gold_pos[x].add(p)
        total_pos += n; gold_copies += len(picks); split_batches += alone
        rows.append({"batch": "B%03d" % k, "agent": "a%03d" % k, "n_items": n, "replicate": rep, "rooms": rs,
                     "exemplar_items": [], "gold_items": picks, "duplicate_items": ["%s/%s" % dup], "warmup_items": [],
                     "reissue": 0, "original_agent": None, "seed": a.seed,
                     "bag_flags": [x for x in BAGS if x.split("/")[0] in rs],
                     "served_in_parts": bool(alone), "items": entries})
    # coverage, from the batches
    for rep in range(1, R + 1):
        rr = [b for b in rows if b["replicate"] == rep]
        got_rooms = {s for b in rr for s in b["rooms"]}
        got_items = {tuple(x.split("/")) for b in rr for x in b["items"] if x.split("/")[0] in b["rooms"]}
        if got_rooms != set(rooms) or got_items != expected:
            sys.exit("replicate %d does not cover the analysed set (%d of %d rooms, %d of %d items)"
                     % (rep, len(got_rooms), len(rooms), len(got_items), len(expected)))
        if sum(len(b["rooms"]) for b in rr) != len(rooms):
            sys.exit("replicate %d holds a room twice" % rep)
    order = [b["batch"] for b in rows]
    random.Random("%d%s:order" % (a.seed, suffix)).shuffle(order)
    sizes = [b["n_items"] for b in rows]
    print("seed %d%s; redraws %d; rooms %d; items %d; R %d" % (a.seed, suffix, redraws, len(rooms), len(expected), R))
    print("batches %d (replicate 1: %d, replicate 2: %d); readers %d; served in parts: %d" % (
        len(rows), sum(1 for b in rows if b["replicate"] == 1), sum(1 for b in rows if b["replicate"] == 2),
        len(rows), split_batches))
    print("positions %d (items x R %d, duplicates %d, gold copies %d); items per batch min %d median %d max %d" % (
        total_pos, len(expected) * R, len(rows), gold_copies, min(sizes), sorted(sizes)[len(sizes) // 2], max(sizes)))
    print("gold copies per gold item: %s" % sorted(collections.Counter(g for b in rows for g in b["gold_items"]).values()))
    print("graph: one component; coverage: each replicate holds the %d rooms and the %d items" % (len(rooms), len(expected)))
    if not a.write:
        return
    with open(os.path.join(OUT, "batches-B3.jsonl"), "w", encoding="utf-8") as f:
        for b in rows:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    json.dump({"seed": a.seed, "suffix": suffix, "redraws": redraws, "order": order,
               "groups": {"1": order[:GROUP1], "2": order[GROUP1:]}},
              open(os.path.join(OUT, "_analysis", "b3_dispatch_order.json"), "w"), indent=1)
    print("wrote out/batches-B3.jsonl (%d lines) and out/_analysis/b3_dispatch_order.json" % len(rows))


if __name__ == "__main__":
    main()
