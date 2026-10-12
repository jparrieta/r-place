#!/usr/bin/env python3
"""B3a: the allocation in B2's packet shape (J, QB3-001, 16:37 Berlin), written to out/batches-B3.jsonl with --write.
It supersedes b3_allocate.py's whole-room batches in parts (out/_analysis/batches-B3_parts_superseded.jsonl).

Every batch is one self-contained packet of at most CAP positions (corpus items, its gold copies and its
duplicate's second copy) and at most BYTES bytes of item text (the items in fleet ids as b2_packets_fleet.py
renders them). For each replicate the analysed rooms are shuffled under the seed and their items poured in that
order, a room's items kept together and running on into the next batch when a batch is full, so that a room is
spread over as few batches as the caps allow. A batch's `rooms` are the rooms whose sibling blocks its packet
carries: the rooms of its corpus items, and the rooms of its gold copies, so a gold copy looks like any other item.

Per batch: one duplicate (an item of its own corpus items, twice, the copies at least a third of the batch
apart); gold copies at one per 20 corpus items (expected; at most two; never an item the batch already holds;
never twice), drawn round-robin from a seeded order of gold_items.jsonl's 40, at a position no other reader holds
that gold item at. Positions are a seeded shuffle of the batch's entries, interleaved across rooms. `items` is
that order, so n_items counts every position the reader answers.

Gates before anything is written: an item's two replicates sit in different batches and on different readers
(one reader a batch, two replicates drawn apart, so by construction, and checked); the room-batch graph over the
corpus items is one component (redrawn under a seed suffix on failure). Coverage from the batches: each replicate
places every second-order theme of the analysed set exactly once (the duplicate aside, gold copies left out).
Dispatch order: a seeded shuffle of the batch ids, in two groups (GROUP1, then the rest).

    python3 out/_analysis/b3_allocate2.py --seed N [--write]
"""
import argparse, collections, importlib.util, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(OUT, "_analysis", "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)

CAP, BYTES, R, GOLD_RATE, GOLD_MAX, GROUP1 = 15, 180000, 2, 1 / 20, 2, 100
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
    size = {}
    for s in rooms:
        for t in store.by_sub[s]:
            size["%s/%s" % (s, t["theme_id"])] = len("\n".join(bpf.render(store, cmap, tmap, s, t["theme_id"], 1)).encode("utf-8"))
    big = [k for k, z in size.items() if z > BYTES]
    if big:
        sys.exit("items over %d bytes alone; stop and ask J: %s" % (BYTES, big))
    room_items = {s: sorted("%s/%s" % (s, t["theme_id"]) for t in store.by_sub[s]) for s in rooms}
    expected = {k for s in rooms for k in room_items[s]}
    gold = [g["item"] for g in jl(os.path.join(OUT, "gold_items.jsonl"))]
    gsize = {g: size[g] for g in gold}

    redraws = 0
    while True:
        suffix = "" if redraws == 0 else ":redraw%d" % redraws
        rng = random.Random("%d%s" % (a.seed, suffix))
        drafts = []                      # (rep, [corpus items])
        for rep in range(1, R + 1):
            order = rooms[:]
            random.Random("%d%s:rep%d" % (a.seed, suffix, rep)).shuffle(order)
            cur, cur_b = [], 0
            # room for the duplicate's second copy and one expected gold copy in every batch
            slots = CAP - 2
            for s in order:
                for k in room_items[s]:
                    if cur and (len(cur) >= slots or cur_b + size[k] > BYTES - 40000):
                        drafts.append((rep, cur)); cur, cur_b = [], 0
                    cur.append(k); cur_b += size[k]
            if cur:
                drafts.append((rep, cur))
        edges = [(k.split("/")[0], "%d" % i) for i, (rep, its) in enumerate(drafts) for k in its]
        if connected(edges):
            break
        redraws += 1
        if redraws > 20:
            sys.exit("the room-batch graph stayed in pieces over 20 redraws")

    gold_order = gold[:]
    random.Random("%d%s:gold" % (a.seed, suffix)).shuffle(gold_order)
    # each gold item is seeded more often than a batch has positions, so "no two readers at the same position"
    # cannot hold for every copy; a copy takes a position its gold item has been seeded at least often so far
    gi, gold_pos = 0, collections.defaultdict(collections.Counter)
    rows = []
    for k, (rep, own) in enumerate(drafts, 1):
        room_cap = CAP - 1 - len(own)                      # positions left after the duplicate's second copy
        e = len(own) * GOLD_RATE
        n_gold = min(GOLD_MAX, room_cap, int(e) + (1 if rng.random() < e - int(e) else 0))
        used = sum(size[x] for x in own)
        picks, tries = [], 0
        while len(picks) < n_gold and tries < 2 * len(gold_order):
            g = gold_order[gi % len(gold_order)]; gi += 1; tries += 1
            if g in own or g in picks or used + gsize[g] > BYTES - 25000:
                continue
            picks.append(g); used += gsize[g]
        cand = [x for x in own if used + size[x] <= BYTES]
        dup = rng.choice(cand) if cand else min(own, key=lambda x: size[x])
        entries = own + picks + [dup]
        n = len(entries)
        for attempt in range(2000):
            rng.shuffle(entries)
            dpos = [i for i, x in enumerate(entries) if x == dup]
            if dpos[1] - dpos[0] < min(max(2, n // 3), n - 1):
                continue
            gp = [(x, i + 1) for i, x in enumerate(entries) if x in picks]
            if attempt < 1500 and any(gold_pos[x][p] > min(gold_pos[x][q] for q in range(1, n + 1)) for x, p in gp):
                continue
            break
        else:
            sys.exit("batch %d: no order met the duplicate spacing" % k)
        for x, p in gp:
            gold_pos[x][p] += 1
        live_rooms = list(dict.fromkeys(x.split("/")[0] for x in own))
        rows.append({"batch": "B%04d" % k, "agent": "a%04d" % k, "n_items": n, "replicate": rep,
                     "rooms": live_rooms + [g.split("/")[0] for g in picks if g.split("/")[0] not in live_rooms],
                     "exemplar_items": [], "gold_items": picks, "duplicate_items": [dup], "warmup_items": [],
                     "reissue": 0, "original_agent": None, "seed": a.seed,
                     "bag_flags": [x for x in BAGS if x in own], "item_bytes": sum(size[x] for x in entries),
                     "items": entries})
    # checks from the batches
    for rep in range(1, R + 1):
        got = collections.Counter(x for b in rows if b["replicate"] == rep for x in b["items"][:]
                                  if x not in b["gold_items"])
        for b in rows:
            if b["replicate"] == rep:
                got[b["duplicate_items"][0]] -= 1
        live = collections.Counter()
        for b in rows:
            if b["replicate"] != rep:
                continue
            c = collections.Counter(b["items"])
            for g in b["gold_items"]:
                c[g] -= 1
            c[b["duplicate_items"][0]] -= 1
            live.update({x: m for x, m in c.items() if m > 0})
        if set(live) != expected or any(m != 1 for m in live.values()):
            sys.exit("replicate %d does not place every item exactly once (%d of %d)" % (rep, len(live), len(expected)))
    seats = collections.defaultdict(set)
    for b in rows:
        for x in set(b["items"]) - set(b["gold_items"]):
            seats[x].add((b["agent"], b["replicate"]))
    if any(len({ag for ag, _ in s}) < len(s) for s in seats.values()):
        sys.exit("an item meets one reader in two replicates")
    if max(b["n_items"] for b in rows) > CAP or max(b["item_bytes"] for b in rows) > BYTES:
        sys.exit("a batch breaks a cap")
    order = [b["batch"] for b in rows]
    random.Random("%d%s:order" % (a.seed, suffix)).shuffle(order)
    sizes = sorted(b["n_items"] for b in rows)
    spread = collections.Counter()
    for b in rows:
        for r in set(x.split("/")[0] for x in b["items"]) - set(b["gold_items"]):
            spread[(r, b["replicate"])] += 1
    print("seed %d%s; redraws %d; rooms %d; items %d; R %d" % (a.seed, suffix, redraws, len(rooms), len(expected), R))
    print("batches %d (replicate 1: %d, replicate 2: %d); readers %d" % (
        len(rows), sum(1 for b in rows if b["replicate"] == 1), sum(1 for b in rows if b["replicate"] == 2), len(rows)))
    print("positions %d (items x R %d, duplicates %d, gold copies %d); positions per batch min %d median %d max %d; "
          "item bytes per batch max %d" % (sum(sizes), len(expected) * R, len(rows), sum(len(b["gold_items"]) for b in rows),
                                           sizes[0], sizes[len(sizes) // 2], sizes[-1], max(b["item_bytes"] for b in rows)))
    print("gold copies per gold item: min %d max %d" % (
        min(collections.Counter(g for b in rows for g in b["gold_items"]).values()),
        max(collections.Counter(g for b in rows for g in b["gold_items"]).values())))
    print("rooms spread over more than one batch in a replicate: %d of %d room-replicates; most batches for one room: %d" % (
        sum(1 for v in spread.values() if v > 1), len(spread), max(spread.values())))
    print("graph: one component; coverage: each replicate places the %d items once" % len(expected))
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
