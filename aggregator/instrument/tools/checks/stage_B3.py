"""checks/stage_B3.py: the close-check of stage B3, the assignment fleet, v38.

Written from stages/STAGE-B3-coding-fleet.md (Outputs, sections 1 to 3 and 3.6, Close),
FLEET.md, and the v37 check it descends from (_v37-source/tools/validate.py, stage04). It checks
the SHAPE of the stage's files: existence, parse, ids that resolve, counts that reconcile. It
cannot check whether a placement is right, and section 3.6 says the last two of its list (read,
families_opened, label-only) are screened by hand as well.

Stage B3 is a fleet stage; the check decides which leg it is closing:

  build leg   no DONE anywhere under out/_fleet_raw/B3/: RETURN-B3.md, batches-B3.jsonl and the
              packets exist; per replicate the batches place every second-order theme of the
              analysed set exactly once (assignment_items_expected, computed here from the store
              as it stands now, out/recut/ laid over it and WITHDRAWN.json honoured); each item's
              replicates sit on different readers and in different batches; the room-batch graph
              is one component; every packet has B2's shape in MANIFEST.json; notes-B3.md carries
              the declarations; the manifest entry is appended; gold_items.jsonl is nowhere a
              reader can reach.
  check leg   a DONE under out/_fleet_raw/B3/ or out/_fleet_raw/B3/batch-k/: everything the
              build leg owed, and assign_raw.jsonl, assign_pass2.jsonl, multiplacement_log.jsonl
              and the four reports, with section 3.6's list run on assign_raw.jsonl and the
              returns cross-checked against the batches.

The packet shape (J, 2026-10-12: stage B3's fleet uses B2's packet shape). Every batch packet is
self-contained: MANIFEST.json gives it its own "items" (at most 15) and "item_bytes" (at most
180,000), and no group, part or parts entry; a batch line over 15 items is refused as well. The
shared pages (index.md, G*.md) are not packets and keep the 50 KB file ceiling. A room may now be
spread over several batches, each carrying the room's sibling block.

The gates, restated for split rooms. The whole-room gates of v38 assumed a room sat in one batch
per replicate; with rooms spread over packets they are kept where they still say something about
an item, and dropped where they only said something about a room:
  - "a room split across batches": dropped; splitting a room is now the design. What it guarded,
    that no theme of a room is left out, is the coverage rule: per replicate every second-order
    theme of the analysed set is placed exactly once (the declared duplicate aside), a shortfall
    named item by item unless its room is in a batch marked coverage_short.
  - "no room meets a reader twice": dropped as a room rule. Two batches of one room on one reader
    show that reader different items under the same sibling block, which is what a whole-room
    batch did. Restated per item: an item's replicates sit on different readers and in different
    batches.
  - "each room's replicates sit on different readers" / "a room twice in one replicate": restated
    per item, as above and in the coverage rule.
  - "the room-batch graph is one component": kept, over the rooms the batches' corpus items come
    from, at the build leg (rooms against batches) and over the returns (rooms against readers).
  - "an item outside the batch's rooms": kept for corpus items (the batch's rooms are the sibling
    blocks it carries), dropped for gold copies.

Gold copies (the analyst's proposal, accepted 2026-10-12). A gold copy seeded into a live batch is
listed both in the batch's "items" (so n_items counts every position the reader answers) and in
its "gold_items"; a gold_items entry not among the items is an error. Gold copies are exempt from
the room rules, are left out of the coverage count of the analysed set, and are counted with every
other returned line against n_items at the check leg. A batch may hold an item both live and as a
gold copy: its "items" then list it twice and its "gold_items" once.

The line count of a return. A return is counted exactly as MANIFEST.json's count_key and
count_exclude say, with fleet.py's own rule (fleet.counted): a line counts when it carries
"position" and none of "primary", "revises", "predicted_confusion", and no pass other than 1. The
prediction line comes first; the pass-1 lines hold n_items; the pass-2 lines follow them in the
same return, each carrying "revises" (the position of the pass-1 line it revises), and are read
apart by that key. A multiplacement record rides on its item line as "multiplacement_log", a list
of records (or B2's object); the check leg assembles them into multiplacement_log.jsonl, and a
multi line whose extra themes are recorded on the line itself is not refused for want of a
multiplacement_log.jsonl line.

What tools/assemble.py writes (the handler's brief, 2026-10-12; J's rulings of 12 October via the orchestrator's
note of 19:00Z). The returns are in fleet ids; assemble.py reads them back into room ids and keeps the fleet's beside
them (fleet_sub, fleet_theme_id, fleet_support, fleet_also_present, and fleet_* on a multiplacement record), which this
check reads past. It tags every line with copy_kind, "corpus", "gold" or "duplicate" (the duplicate's second copy),
from batches-B3.jsonl; where a line carries copy_kind this check counts a corpus reading by it (a gold copy is never
one) and refuses a tag the batch does not bear out: "gold" on an item the batch does not seed as a gold copy, "corpus"
or "duplicate" on an item the batch does not hold live, "duplicate" on an item not its declared duplicate, more gold or
duplicate lines than the batch tags. Lines without copy_kind are read by batch membership, as before. assemble.py
drops the readers' t_start and t, which readers invent (every line of the 2026-10-12 run read 2026-05-09T00:00:00Z),
and carries the dispatch's measured time, packet_elapsed_s from the return's meta: a line carries both timestamps or
packet_elapsed_s, and one with neither is refused, so section 3.6's "both timestamps" is kept as "a measured time".
agent is the batch's agent (a0001), the dispatch's reader id (r6, reused across packets) kept as `reader`.

Files the stage file names without giving their fields, checked for existence and the licence
sentence only: fidelity-B3.md, position-B3.md, agent_report-B3.md, multiplacement_register-B3.md,
notes-B3.md (declarations by keyword), RETURN-B3.md (by keyword). assign_pass2.jsonl's fields
are not given beyond "names the pass-1 line it revises": a pass-2 line must key to a pass-1
(batch, agent, position).

The line count. Section 3.6 says items x R; section 1.4 puts one duplicate item in every batch
and section 1.6 seeds gold copies, so the raw file legitimately holds more lines than items x R.
The check reconciles two ways: every (batch, agent) return holds the batch's n_items (gold copies
and the duplicate included), and the distinct (item, replicate) pairs over the analysed set, gold
copies left out, number items x R, a shortfall named item by item unless the room is in a batch
marked coverage_short.

Not carried from v37:
  - R read off a batch line's "R" field or notes-B3.md by regex; v38 fixes R = 2 in section 1
    and the batch line carries replicate, so R is the largest replicate on the batches.
  - the v37 ids `case_theme` and `second_order`: now `theme_id` and `third_order`.
  - the community-agent graph over assign_raw.jsonl only: v38 runs the gate at the build leg
    over batches-B3.jsonl as well, since section 1.2 refuses to build a fleet in pieces.
"""
import collections, fnmatch, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
try:
    from fleet import counted      # one rule for what counts, the dispatch's and the check's
except ImportError:                # a copy of the tools without fleet.py: the same rule, word for word
    def counted(o, rule):
        key = rule.get("count_key")
        if not key:
            return True
        if key not in o or any(k in o for k in rule.get("count_exclude", [])):
            return False
        return o.get("pass", 1) in (1, "1", None)

CONF = ("clear", "arguable")
READ = ("whole", "theme-block")
BATCH_FIELDS = ("batch", "agent", "n_items", "replicate", "rooms", "exemplar_items", "gold_items",
                "duplicate_items", "warmup_items", "reissue", "original_agent", "seed", "items")
LINE_FIELDS = ("sub", "theme_id", "batch", "agent", "replicate", "position", "third_order", "multi", "why",
               "confidence", "read", "exemplar_read", "families_opened", "bag", "support")
TIME_FIELDS = ("t_start", "t")     # the readers' own; assemble.py drops them for the dispatch's packet_elapsed_s
COPY_KINDS = ("corpus", "gold", "duplicate")
MULTI_FIELDS = ("sub", "theme_id", "key", "batch", "agent", "replicate", "position", "primary", "additional",
                "why_not_one", "why_this_one", "support_primary", "support_additional", "dispensable")
KB50 = 50 * 1024                   # the shared pages' ceiling (index.md, G*.md)
MAX_ITEMS = 15                     # a B3 packet: B2's shape (J, 2026-10-12)
MAX_ITEM_BYTES = 180000
SHARED = ("index.md", "G*.md")
COUNT_DEFAULT = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}


# ---- helpers vlib does not have -----------------------------------------------------------------

def fleet_dirs(outdir, stage):
    base = os.path.join(outdir, "_fleet_raw", stage)
    if not os.path.isdir(base):
        return []
    out = []
    if os.path.exists(os.path.join(base, "DONE")):
        out.append(base)
    for d in sorted(glob.glob(os.path.join(base, "*"))):
        if os.path.isdir(d) and os.path.exists(os.path.join(d, "DONE")):
            out.append(d)
    return out


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def key_of(r):
    return "%s/%s" % (r.get("sub"), r.get("theme_id"))


def split_key(k):
    if isinstance(k, dict):
        return (k.get("sub"), k.get("theme_id"))
    if isinstance(k, str) and "/" in k:
        a, b = k.split("/", 1)
        return (a, b)
    return (None, None)


def packets_dir(outdir, stage):
    c = sorted(glob.glob(os.path.join(outdir, "_packets-%s*" % stage)))
    return c[-1] if c else None


def connected(edges):
    """edges: iterable of (room, reader). True when the bipartite graph is one component."""
    adj = collections.defaultdict(set)
    for a, b in edges:
        adj["c:" + str(a)].add("a:" + str(b))
        adj["a:" + str(b)].add("c:" + str(a))
    if not adj:
        return True, 0, 0
    seen, stack = set(), [next(iter(adj))]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj[n] - seen)
    return len(seen) == len(adj), len(seen), len(adj)


def expected_items(stage, what, outdir, ctx):
    """assignment_items_expected: every second-order theme that stands now over the analysed set: the store
    with out/recut/ laid over it as recut_overlay lays it, so once out/recut/WITHDRAWN.json exists the split's
    children are not expected and the parents are (J, 2026-10-12: the 56 children made it 7,900 against the
    store's 7,844). (analysed rooms, set of (sub, theme_id)) or None having said what was not checked."""
    sets = vlib.analysed_set(stage, what, outdir, ctx)
    if sets is None:
        return None
    analysed, _d = sets
    themes = vlib.current_themes(ctx)          # out/recut/ laid over the store, WITHDRAWN.json honoured
    items = {k for k in themes if k[0] in analysed}
    empty = sorted(r for r in analysed if not any(k[0] == r for k in items))
    if empty:
        warn("%d rooms of the analysed set have no second-order theme in package/store/themes.jsonl (%s); they "
             "hold no item and cannot be in a batch" % (len(empty), empty[:5]))
    return analysed, items


# ---- the build leg -------------------------------------------------------------------------------------

def check_return_spec(outdir, name):
    t = text(outdir, name)
    if not t:
        return
    low = t.lower()
    for word, what in (("rule 0", "rule 0 in the contract's words, first"),
                       ("predicted_confusion", "the prediction line each reader writes first"),
                       ("why_not_one", "the multiplacement record"),
                       ("multiplacement_log", "that a second placement owes a multiplacement_log.jsonl line"),
                       ("exemplar_read", "exemplar_read on the return line"),
                       ("confirm", "the line telling the reader to confirm it reached the end marker")):
        if word not in low:
            err("%s does not carry %s (no %r in it); section 1.5 gives the order" % (name, what, word))
    if not re.search(r"```[^\n]*\n.*?```", t, re.S):
        err("%s has no fenced block; fleet.py reads the end marker off the last line of the last fenced block" % name)


def live_items(b):
    """A batch's corpus items as a Counter: its "items" less its gold copies ("gold_items", each listed in
    "items" as well). An item seeded as a gold copy into a batch that also holds it live keeps its live count."""
    live = collections.Counter(split_key(x) for x in as_list(b.get("items")))
    live.subtract(collections.Counter(split_key(g) for g in as_list(b.get("gold_items"))))
    return collections.Counter({k: n for k, n in live.items() if n > 0})


def short_rooms(by_batch):
    return {r for b in by_batch.values() if b.get("coverage_short") for r in as_list(b.get("rooms"))}


def check_batches(outdir, ctx, gold_keys, items_expected):
    """batches-B3.jsonl: fields, ids, the packet cap, coverage per replicate, the per-item gates, the graph.
    Returns (rows, R, by_batch)."""
    rows = jsonl(os.path.join(outdir, "batches-B3.jsonl")) or []
    if not rows:
        err("batches-B3.jsonl is empty; the allocator writes one line per batch before any packet is built")
        return rows, 2, {}
    resolvable = vlib.store_themes(ctx)
    current = vlib.current_themes(ctx)
    analysed = items_expected[0] if items_expected else None
    by_batch, edges = {}, []
    placed = collections.defaultdict(collections.Counter)       # replicate -> item -> live placements
    item_seats = collections.defaultdict(list)                  # item -> [(agent, batch, replicate)]
    reps = []
    for i, b in enumerate(rows, 1):
        for k in BATCH_FIELDS:
            if k not in b:
                err("batches-B3.jsonl line %d lacks %r; the batch line of section 1.2 carries it" % (i, k),
                    shape="batches-B3.jsonl: a line without %s" % k, where="line %d" % i)
        bid, agent, rep = b.get("batch"), b.get("agent"), b.get("replicate")
        if bid in by_batch:
            err("batches-B3.jsonl line %d repeats batch %s" % (i, bid), shape="batches-B3.jsonl: a repeated batch id",
                where="line %d" % i)
        by_batch[bid] = b
        if isinstance(rep, int):
            reps.append(rep)
        items = [split_key(x) for x in as_list(b.get("items"))]
        rooms = set(as_list(b.get("rooms")))
        if isinstance(b.get("n_items"), int) and b["n_items"] != len(items):
            err("batches-B3.jsonl %s: n_items %d but items lists %d; the count is computed from the list, gold copies "
                "included" % (bid, b["n_items"], len(items)), shape="batches-B3.jsonl: n_items off its items", where=str(bid))
        if len(items) > MAX_ITEMS:
            err("batches-B3.jsonl %s holds %d items; a B3 packet holds %d at most (B2's packet shape, J 2026-10-12), "
                "redraw the batches" % (bid, len(items), MAX_ITEMS),
                shape="batches-B3.jsonl: a batch over fifteen items", where=str(bid))
        golds = collections.Counter(split_key(g) for g in as_list(b.get("gold_items")))
        have = collections.Counter(items)
        for g, n in golds.items():
            if g not in gold_keys:
                err("batches-B3.jsonl %s tags gold item %s/%s, which gold_items.jsonl does not hold" % (bid, g[0], g[1]),
                    shape="batches-B3.jsonl: a gold tag off the key", where=str(bid))
            if have[g] < n:
                err("batches-B3.jsonl %s tags gold copy %s/%s %d time(s) and lists it %d time(s) in items; a gold copy "
                    "is listed in both, so n_items counts every position the reader answers"
                    % (bid, g[0], g[1], n, have[g]), shape="batches-B3.jsonl: a gold copy not among its items",
                    where=str(bid))
        live = live_items(b)
        for k in items:
            if k not in resolvable:
                err("batches-B3.jsonl %s lists item %s/%s, not a second-order theme in package/store/themes.jsonl"
                    % (bid, k[0], k[1]), shape="batches-B3.jsonl: an item not in the store", where=str(bid))
            elif k in live and k not in current:
                err("batches-B3.jsonl %s lists item %s/%s, which is not a second-order theme as the store stands now: "
                    "out/recut/ has superseded it (the parent of a standing split) or withdrawn it (a child of a split "
                    "out/recut/WITHDRAWN.json withdraws from every view)" % (bid, k[0], k[1]),
                    shape="batches-B3.jsonl: an item the recut layer superseded or withdrew", where=str(bid))
        for k in live:                                      # gold copies are exempt from room membership
            if k[0] not in rooms:
                err("batches-B3.jsonl %s lists item %s/%s from a room not in its rooms; the batch's rooms are the "
                    "sibling blocks its packet carries" % (bid, k[0], k[1]),
                    shape="batches-B3.jsonl: an item outside the batch's rooms", where=str(bid))
            edges.append((k[0], bid))
        for r in rooms:
            if analysed is not None and r not in analysed:
                err("batches-B3.jsonl %s holds room %r, which is not in the analysed set (the frame minus "
                    "dropped.jsonl)" % (bid, r), shape="batches-B3.jsonl: a room outside the analysed set", where=str(bid))
        dups = {split_key(x) for x in as_list(b.get("duplicate_items"))}
        for dkey in dups:
            if dkey not in set(items):
                err("batches-B3.jsonl %s tags duplicate %s/%s, which is not among its items" % (bid, dkey[0], dkey[1]),
                    shape="batches-B3.jsonl: a duplicate tag off the batch", where=str(bid))
        for k, n in live.items():
            if n > (2 if k in dups else 1):
                err("batches-B3.jsonl %s lists %s/%s %d times beyond its gold copies; one reading per item, two for "
                    "the batch's declared duplicate" % (bid, k[0], k[1], n),
                    shape="batches-B3.jsonl: an item repeated in one batch", where=str(bid))
            placed[rep][k] += 1
            item_seats[k].append((agent, bid, rep))
        if isinstance(b.get("reissue"), int) and b["reissue"] > 2:
            err("batches-B3.jsonl %s: reissue %d; section 2 reissues at most twice, then the build leg rebuilds"
                % (bid, b["reissue"]), shape="batches-B3.jsonl: reissue beyond two", where=str(bid))
    R = max(reps) if reps else 2
    if R != 2:
        warn("batches-B3.jsonl: replicates run to %d; section 1 fixes R = 2, say in notes-B3.md what more bought" % R)
    # gate 1, per item: an item's replicates on different readers and in different batches
    for k, seats in item_seats.items():
        by_agent, by_bid = collections.defaultdict(set), collections.defaultdict(set)
        for a_, b_, r_ in seats:
            by_agent[a_].add(r_)
            by_bid[b_].add(r_)
        a2 = sorted(str(a_) for a_, rs in by_agent.items() if len(rs) > 1)
        b2 = sorted(str(b_) for b_, rs in by_bid.items() if len(rs) > 1)
        if a2:
            err("batches-B3.jsonl: item %s/%s meets reader %s in two replicates; an item's replicates sit on "
                "different readers, reject and redraw (gate 1)" % (k[0], k[1], a2[0]),
                shape="batches-B3.jsonl: an item meeting the same reader in two replicates", where="%s/%s" % k)
        if b2:
            err("batches-B3.jsonl: item %s/%s sits in batch %s for two replicates; its replicates sit in different "
                "batches" % (k[0], k[1], b2[0]),
                shape="batches-B3.jsonl: an item's replicates in one batch", where="%s/%s" % k)
    # gate 2: one component, rooms (of the corpus items) against batches
    ok, seen, total = connected(edges)
    if not ok:
        err("batches-B3.jsonl: the room-batch graph is in pieces (%d of %d nodes reachable from the first); "
            "section 1.2 refuses to build a fleet in pieces, redraw" % (seen, total))
    # coverage: per replicate, every item of the analysed set placed exactly once (gold copies left out)
    if items_expected:
        analysed, items = items_expected
        short = short_rooms(by_batch)
        if not placed:
            err("batches-B3.jsonl covers no room of the analysed set")
        for rep in sorted(set(placed) | set(range(1, R + 1)), key=str):
            got = placed.get(rep, collections.Counter())
            miss = sorted(k for k in items - set(got) if k[0] not in short)
            if miss:
                err("batches-B3.jsonl: replicate %s lacks %d of the %d items assignment_items_expected counts (%s, in "
                    "%d rooms); every second-order theme of the analysed set is placed once per replicate at R = 2, a "
                    "shortfall only in a batch marked coverage_short" % (rep, len(miss), len(items),
                                                                        ["%s/%s" % k for k in miss[:3]],
                                                                        len({k[0] for k in miss})),
                    shape="batches-B3.jsonl: a replicate short of the analysed set", where="replicate %s" % rep)
            twice = sorted(k for k in got if k in items and
                           len({b_ for _a, b_, r in item_seats[k] if r == rep}) > 1)
            if twice:
                err("batches-B3.jsonl: replicate %s places %d items in two batches (%s); each replicate places an item "
                    "once" % (rep, len(twice), ["%s/%s" % k for k in twice[:3]]),
                    shape="batches-B3.jsonl: an item twice in one replicate", where="replicate %s" % rep)
            stray = sorted(k for k in got if k not in items and k in current)
            if stray and items:
                err("batches-B3.jsonl: replicate %s places %d items outside the analysed set (%s)"
                    % (rep, len(stray), ["%s/%s" % k for k in stray[:3]]))
    print("  batches %d, R %d, rooms %d, items %d, graph %s" % (len(rows), R, len({e[0] for e in edges}),
                                                              len(item_seats), "one component" if ok else "IN PIECES"))
    return rows, R, by_batch


def check_notes(outdir):
    notes = text(outdir, "notes-B3.md")
    low = notes.lower()
    if not notes:
        return
    for word, what in (("seed", "the seed"), ("cap", "the item cap per batch"), ("gold", "the gold seeding rate and policy"),
                       ("exemplar", "the exemplar arm, served to every reader or to none"),
                       ("reissue", "the reissue policy"), ("batch", "the batch count and reader count")):
        if word not in low:
            err("notes-B3.md does not declare %s (no %r in it); section 1.2 says it is declared before any packet "
                "exists" % (what, word))
    if not re.search(r"\bR\b", notes):
        err("notes-B3.md does not declare the replication factor R; section 1.2 says why it is 2")
    for word in ("warm", "bag", "order"):
        if word not in low:
            warn("notes-B3.md says nothing of %r (the warm-up block, the bag flags, the order of batches)" % word)


def is_shared(name):
    return any(fnmatch.fnmatch(name, g) for g in SHARED)


def load_manifest(pd):
    if not pd:
        return {}
    try:
        m = json.load(open(os.path.join(pd, "MANIFEST.json"), encoding="utf-8"))
        return m if isinstance(m, dict) else {}
    except (OSError, ValueError):
        return {}


def check_packets(outdir, stage, by_batch=None):
    """The packets folder: the shared pages under 50 KB; every batch packet in B2's shape, read from
    MANIFEST.json (its own "items", at most 15; "item_bytes", at most 180,000; no group, part or parts)."""
    pd = packets_dir(outdir, stage)
    if pd is None:
        err("no _packets-%s/ in the output directory; the build leg writes the index page, the family pages and "
            "one file per batch with packets.py %s before it closes at packets-out" % (stage, stage))
        return None
    files = sorted(glob.glob(os.path.join(pd, "*.md")))
    if not files:
        err("%s holds no .md packet" % os.path.relpath(pd, outdir))
    rel = os.path.relpath(pd, outdir)
    man = load_manifest(pd)
    if files and not os.path.exists(os.path.join(pd, "MANIFEST.json")):
        err("%s has no MANIFEST.json; packets.py writes one with each packet's item count, which fleet.py and this "
            "check read" % rel, shape="_packets-%s: no MANIFEST.json" % stage)
    for p in files:
        base = os.path.basename(p)
        name = os.path.splitext(base)[0]
        if is_shared(base):
            n = os.path.getsize(p)
            if n > KB50:
                err("%s/%s is %d bytes, over FLEET.md's 50 KB ceiling for a shared page; split the family page"
                    % (rel, base, n), shape="_packets-%s: a shared page over 50 KB" % stage, where=base)
            continue
        if base.startswith("RETURN-"):
            continue
        e = man.get(name)
        if not isinstance(e, dict):
            if man:
                err("%s/%s has no MANIFEST.json entry; every packet carries its own item count there" % (rel, base),
                    shape="_packets-%s: a packet without its MANIFEST entry" % stage, where=base)
            continue
        parts = [k for k in ("group", "part", "parts") if k in e]
        if parts:
            err("%s: MANIFEST.json gives packet %s %s; a B3 packet is self-contained, never a part of a batch (J, "
                "2026-10-12), rebuild with packets.py B3" % (rel, name, ", ".join(parts)),
                shape="_packets-%s: a packet in parts" % stage, where=name)
        n = e.get("items")
        if not isinstance(n, int):
            err("%s: MANIFEST.json gives packet %s no \"items\"; every packet carries its own item count"
                % (rel, name), shape="_packets-%s: a packet without its item count" % stage, where=name)
        elif n > MAX_ITEMS:
            err("%s: packet %s holds %d items; a B3 packet holds %d at most (B2's packet shape, J 2026-10-12)"
                % (rel, name, n, MAX_ITEMS), shape="_packets-%s: a packet over fifteen items" % stage, where=name)
        ib = e.get("item_bytes")
        if not isinstance(ib, int):
            err("%s: MANIFEST.json gives packet %s no \"item_bytes\"; packets.py B3 records the bytes of item text"
                % (rel, name), shape="_packets-%s: a packet without item_bytes" % stage, where=name)
        elif ib > MAX_ITEM_BYTES:
            err("%s: packet %s carries %d bytes of item text; a B3 packet carries %d at most"
                % (rel, name, ib, MAX_ITEM_BYTES), shape="_packets-%s: a packet over 180,000 item bytes" % stage,
                where=name)
        b = (by_batch or {}).get(name)
        if b and isinstance(n, int) and isinstance(b.get("n_items"), int) and n != b["n_items"]:
            err("%s: packet %s holds %d items and batches-B3.jsonl gives it n_items %d; rebuild the packet"
                % (rel, name, n, b["n_items"]), shape="_packets-%s: a packet off its batch's count" % stage, where=name)
    return pd


def gold_leaked(outdir, dirs):
    for d in dirs:
        if not d or not os.path.isdir(d):
            continue
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            if os.path.isfile(p) and os.path.basename(p).lower().startswith("gold_items"):
                err("%s holds %s; the answer key stays outside the readers' directory (FLEET.md, section 1.6). "
                    "Move it out and rebuild" % (os.path.relpath(d, outdir), os.path.basename(p)))


# ---- the check leg -------------------------------------------------------------------------------------

B3_LINE_WAIVERS = ("support_overlap", "support_count", "no_multi")


def b3_waivers(outdir, report=True):
    """J's waivers by name for stage B3 (QB3-004, QB3-005, 2026-10-12), out/return_waivers.jsonl lines with stage "B3",
    a check, a reason and ruled_by, and either file "<batch>/<reader>.jsonl" (check no_prediction) or batch and
    position (checks support_overlap, support_count, no_multi; keyed so that a re-assembly that renumbers
    assign_raw.jsonl keeps them). Returns (by_file, by_position): sets of (file, check), (batch, position, check)."""
    by_file, by_pos = set(), set()
    for i, w in enumerate(jsonl(os.path.join(outdir, "return_waivers.jsonl")) or [], 1):
        if w.get("stage") != "B3":
            continue
        ck = w.get("check")
        ok = w.get("reason") and w.get("ruled_by") and ck
        if ok and ck == "no_prediction" and w.get("file"):
            by_file.add((w["file"], ck))
        elif ok and ck in B3_LINE_WAIVERS and w.get("batch") and isinstance(w.get("position"), int):
            by_pos.add((w["batch"], w["position"], ck))
        elif report:
            err("return_waivers.jsonl line %d (stage B3) lacks its check, reason, ruled_by, or the file (no_prediction) "
                "or batch and position (%s) it names" % (i, ", ".join(B3_LINE_WAIVERS)),
                shape="a B3 waiver without its ruling", where="return_waivers.jsonl line %d" % i)
    return by_file, by_pos


def check_returns(outdir, dirs, scheme, by_batch, manifest):
    """The returns as fleet.py left them: a prediction line first, then the batch's n_items pass-1 lines counted
    as MANIFEST.json says (fleet.counted), then the pass-2 lines, each carrying "revises". Returns (pass-1
    lines, pass-2 lines)."""
    total = total2 = 0
    waived, _ = b3_waivers(outdir)               # J, 2026-10-12 (QB3-004)
    n_waived = 0
    for d in dirs:
        rel = os.path.relpath(d, outdir)
        for p in sorted(glob.glob(os.path.join(d, "*", "*.jsonl"))):
            rows = jsonl(p) or []
            name = os.path.basename(os.path.dirname(p))
            reader = os.path.basename(p)[:-6]
            rule = dict(COUNT_DEFAULT)
            rule.update({k: v for k, v in (manifest.get(name) or {}).items() if k in ("count_key", "count_exclude")})
            preds = [r for r in rows if "predicted_confusion" in r]
            lines = [r for r in rows if counted(r, rule)]
            pass2 = [(i, r) for i, r in enumerate(rows) if "revises" in r]
            total += len(lines)
            total2 += len(pass2)
            if not preds and ("%s/%s.jsonl" % (name, reader), "no_prediction") in waived:
                n_waived += 1
            elif not preds:
                err("%s/%s/%s: no prediction line; each reader writes its predicted_confusion first in its return "
                    "(section 1.5), and agent_report-B3.md compiles them" % (rel, name, reader),
                    shape="_fleet_raw/04: a return without a prediction line", where="%s/%s" % (name, reader))
            elif rows and "predicted_confusion" not in rows[0]:
                warn("%s/%s/%s: the prediction line is not first" % (rel, name, reader))
            for pr in preds:
                for s in as_list(pr.get("predicted_confusion")):
                    if scheme and s not in scheme:
                        err("%s/%s/%s predicts confusion on %r, which scheme_final.jsonl does not define"
                            % (rel, name, reader, s), shape="_fleet_raw/04: a prediction on an id the scheme does not define",
                            where="%s/%s" % (name, reader))
            b = by_batch.get(name)
            if b and isinstance(b.get("n_items"), int) and len(lines) != b["n_items"]:
                err("%s/%s/%s returned %d lines for a batch of %d items (counted as MANIFEST.json says: %s, not %s); a "
                    "partial return is not a return, it is reissued or the batch is marked coverage_short"
                    % (rel, name, reader, len(lines), b["n_items"], rule.get("count_key"),
                       ", ".join(rule.get("count_exclude") or [])),
                    shape="_fleet_raw/04: a return short of its batch", where="%s/%s" % (name, reader))
            pos1 = {r.get("position") for r in lines}
            last1 = max((i for i, r in enumerate(rows) if counted(r, rule)), default=-1)
            for i, r in pass2:
                v = r.get("revises")
                v = v.get("position") if isinstance(v, dict) else v
                v = int(v) if isinstance(v, str) and v.isdigit() else v
                if v not in pos1:
                    err("%s/%s/%s line %d revises %r, which names no pass-1 line of this return (a position the reader "
                        "returned); every pass-2 line names the pass-1 line it revises" % (rel, name, reader, i + 1, v),
                        shape="_fleet_raw/04: a pass-2 line naming no pass-1 line", where="%s/%s" % (name, reader))
                if i < last1:
                    warn("%s/%s/%s line %d: a pass-2 line before the last pass-1 line; pass 2 follows pass 1 in the "
                         "return" % (rel, name, reader, i + 1))
    if n_waived:
        print("  returns without a prediction line waived by J by name: %d (return_waivers.jsonl)" % n_waived)
    return total, total2


def check_raw(outdir, ctx, scheme, by_batch, R, gold_keys, items_expected):
    raw = jsonl(os.path.join(outdir, "assign_raw.jsonl")) or []
    if not raw:
        err("assign_raw.jsonl is empty; the check leg assembles it from the returns, keyed on packet heading and "
            "cell number")
    vlib.store_codes(ctx)
    codes = ctx["codes"]
    ct = vlib.code_themes(vlib.recut_overlay("codes", jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or [], ctx.get("outdir")))
    spec_ap = "also_present" in text(outdir, "RETURN-B3.md")
    share_rule = vlib.BOUND_PHRASE in text(outdir, "RETURN-B3.md")
    if not codes:
        err("package/store/codes.jsonl holds no concept, so no support id could be resolved")
    _, waived_pos = b3_waivers(outdir, report=False)    # J, 2026-10-12 (QB3-005): by batch and position
    n_waived = collections.Counter()
    multi = jsonl(os.path.join(outdir, "multiplacement_log.jsonl")) or []
    mkeys = collections.defaultdict(set)
    for i, m in enumerate(multi, 1):
        for k in MULTI_FIELDS:
            if k not in m:
                err("multiplacement_log.jsonl line %d lacks %r; the record of section 1.5 carries it" % (i, k),
                    shape="multiplacement_log.jsonl: a record without %s" % k, where="line %d" % i)
        if m.get("key") and m.get("key") != key_of(m):
            err("multiplacement_log.jsonl line %d: key %r is not sub/theme_id of the line" % (i, m.get("key")),
                shape="multiplacement_log.jsonl: key off sub/theme_id", where="line %d" % i)
        why = " ".join(str(m.get("why_not_one") or "").split()).lower()
        if not why:
            err("multiplacement_log.jsonl line %d: why_not_one is empty; the line is reduced to its primary and the "
                "defect written to defects.jsonl" % i, shape="multiplacement_log.jsonl: an empty why_not_one",
                where="line %d" % i)
        elif re.search(r"both (gates|tests) (are|were) (satisfied|met)", why) and len(why) < 90:
            err("multiplacement_log.jsonl line %d: why_not_one only says both gates are satisfied; decide_when_both "
                "settles that case, name what the single placement would fail to carry" % i,
                shape="multiplacement_log.jsonl: why_not_one restates both gates", where="line %d" % i)
        if m.get("dispensable") in (None, ""):
            err("multiplacement_log.jsonl line %d: dispensable is null; it is compulsory" % i,
                shape="multiplacement_log.jsonl: dispensable null", where="line %d" % i)
        sp, sa = set(as_list(m.get("support_primary"))), set(as_list(m.get("support_additional")))
        if (not sa or sa & sp) and (m.get("batch"), m.get("position"), "support_overlap") in waived_pos:
            n_waived["support_overlap"] += 1
        elif not sa or sa & sp:
            err("multiplacement_log.jsonl line %d: the additional theme %s has no supporting concept of its own "
                "(same concept twice is the same reading twice)" % (i, m.get("additional")),
                shape="multiplacement_log.jsonl: no distinct support for the additional theme", where="line %d" % i)
        for c in sp | sa:
            if codes and (m.get("sub"), c) not in codes:
                err("multiplacement_log.jsonl line %d: support %r does not resolve in package/store/codes.jsonl for "
                    "%s" % (i, c, m.get("sub")), shape="multiplacement_log.jsonl: a support id that does not resolve",
                    where="line %d" % i)
        for s in (m.get("primary"), m.get("additional")):
            if scheme and s not in scheme:
                err("multiplacement_log.jsonl line %d names %r, which scheme_final.jsonl does not define" % (i, s),
                    shape="multiplacement_log.jsonl: an id the scheme does not define", where="line %d" % i)
        mkeys[(m.get("sub"), m.get("theme_id"), m.get("agent"))].add(m.get("additional"))

    lives = {}

    def live_of(bid):
        if bid not in lives:
            lives[bid] = live_items(by_batch.get(bid) or {})
        return lives[bid]
    per_item = collections.defaultdict(list)
    per_key_agent = collections.Counter()
    positions = collections.defaultdict(list)
    edges = []
    ex_seen = set()
    copies = collections.Counter()                  # (batch, agent, item, copy_kind) -> lines
    for i, r in enumerate(raw, 1):
        for k in LINE_FIELDS:
            if k == "multi" and k not in r and (r.get("batch"), r.get("position"), "no_multi") in waived_pos:
                n_waived["no_multi"] += 1
            elif k not in r:
                err("assign_raw.jsonl line %d carries no %s; the return line of section 1.5 carries it, and the v35 "
                    "analyst found a field missing on every row at the end of the run" % (i, k),
                    shape="assign_raw.jsonl: a line without %s" % k, where="line %d" % i)
        if not all(k in r for k in TIME_FIELDS) and not isinstance(r.get("packet_elapsed_s"), (int, float)):
            err("assign_raw.jsonl line %d carries neither both timestamps (t_start, t) nor packet_elapsed_s, the "
                "dispatch's measured time assemble.py carries from the return's meta; per-reader elapsed time is what a "
                "cost estimate is built from (section 1.5)" % i,
                shape="assign_raw.jsonl: a line with no measured time", where="line %d" % i)
        so = as_list(r.get("third_order"))
        if not so:
            err("assign_raw.jsonl line %d has no third_order" % i, shape="assign_raw.jsonl: a line with no placement",
                where="line %d" % i)
        for s in so:
            if scheme and s not in scheme:
                err("assign_raw.jsonl line %d places on %r, which scheme_final.jsonl does not define" % (i, s),
                    shape="assign_raw.jsonl: an id the frozen scheme does not define", where="line %d" % i)
        if len(so) > 3:
            err("assign_raw.jsonl line %d carries %d themes; three at most, beyond three place one and set bag true"
                % (i, len(so)), shape="assign_raw.jsonl: more than three themes on a line", where="line %d" % i)
        for pb in vlib.also_present_problems(r.get("also_present"), so, r.get("sub"), r.get("theme_id"), ct, scheme):
            err("assign_raw.jsonl line %d: %s" % (i, pb), shape="assign_raw.jsonl: also_present", where="line %d" % i)
        if share_rule:                              # J, 2026-10-12: twenty themes at most, three concepts each
            for pb in vlib.also_present_bound_problems(r.get("also_present")):
                err("assign_raw.jsonl line %d: %s" % (i, pb), shape="assign_raw.jsonl: also_present over its bound",
                    where="line %d" % i)
        if r.get("bag") and spec_ap and not r.get("also_present"):
            err("assign_raw.jsonl line %d is a bag and names no also_present; rule 0 keeps every theme beyond the one "
                "placed, each with its own concepts (J, 2026-10-11)" % i,
                shape="assign_raw.jsonl: a bag with no also_present", where="line %d" % i)
        sup = as_list(r.get("support"))
        for c in sup:
            if codes and (r.get("sub"), c) not in codes:
                err("assign_raw.jsonl line %d: support %r does not resolve in package/store/codes.jsonl for %s"
                    % (i, c, r.get("sub")), shape="assign_raw.jsonl: a support id that does not resolve",
                    where="line %d" % i)
        if r.get("multi"):
            extra = set(so[1:])
            have = set(mkeys.get((r.get("sub"), r.get("theme_id"), r.get("agent")), set()))
            ml = r.get("multiplacement_log")       # records riding on the line (a list, or B2's object)
            for rec in (ml if isinstance(ml, list) else [ml] if isinstance(ml, dict) else []):
                if isinstance(rec, dict):
                    have |= set(as_list(rec.get("additional")))
            if not extra:
                err("assign_raw.jsonl line %d: multi is true with one id" % i,
                    shape="assign_raw.jsonl: multi with a single id", where="line %d" % i)
            elif not extra <= have:
                err("assign_raw.jsonl line %d: multi-assigned with no record in multiplacement_log.jsonl for %s; "
                    "reduce the line to its primary and write the defect" % (i, sorted(extra - have)),
                    shape="assign_raw.jsonl: a multi line with no multiplacement record", where="line %d" % i)
            if len(set(sup)) < len(set(so)) and (r.get("batch"), r.get("position"), "support_count") in waived_pos:
                n_waived["support_count"] += 1
            elif len(set(sup)) < len(set(so)):
                err("assign_raw.jsonl line %d: %d themes on %d distinct support concepts; a multi-assigned line names "
                    "at least one distinct concept per theme" % (i, len(set(so)), len(set(sup))),
                    shape="assign_raw.jsonl: fewer support concepts than themes on a multi line", where="line %d" % i)
        elif len(so) > 1:
            err("assign_raw.jsonl line %d carries %d themes with multi false" % (i, len(so)),
                shape="assign_raw.jsonl: several themes with multi false", where="line %d" % i)
        if r.get("read") == "label-only":
            err("assign_raw.jsonl line %d carries read: \"label-only\"; a reader that read only the label placed the "
                "coder's grouping, not the material; write the defect and reissue" % i,
                shape="assign_raw.jsonl: read is label-only", where="line %d" % i)
        elif "read" in r and r.get("read") not in READ:
            err("assign_raw.jsonl line %d: read is %r, not whole|theme-block" % (i, r.get("read")),
                shape="assign_raw.jsonl: read outside whole|theme-block", where="line %d" % i)
        if "confidence" in r and r.get("confidence") not in CONF:
            err("assign_raw.jsonl line %d: confidence is %r, not clear|arguable" % (i, r.get("confidence")),
                shape="assign_raw.jsonl: confidence outside clear|arguable", where="line %d" % i)
        if "replicate" in r and r.get("replicate") not in range(1, R + 1):
            err("assign_raw.jsonl line %d: replicate %r is not in 1..%d" % (i, r.get("replicate"), R),
                shape="assign_raw.jsonl: replicate outside 1..R", where="line %d" % i)
        fo = as_list(r.get("families_opened"))
        for g in fo:
            if not vlib.FAMILY.match(str(g)):
                err("assign_raw.jsonl line %d: families_opened holds %r, not a family id GNN" % (i, g),
                    shape="assign_raw.jsonl: families_opened with a non-family id", where="line %d" % i)
        if "exemplar_read" in r:
            ex_seen.add(r.get("exemplar_read") is None)
        if r.get("batch") not in by_batch and by_batch:
            err("assign_raw.jsonl line %d names batch %r, which batches-B3.jsonl does not hold" % (i, r.get("batch")),
                shape="assign_raw.jsonl: a batch not in batches-B3.jsonl", where="line %d" % i)
        k = (r.get("sub"), r.get("theme_id"))
        bid = r.get("batch")
        if "copy_kind" in r:                        # assemble.py's tag, read from batches-B3.jsonl (2026-10-12)
            ck = r.get("copy_kind")
            b = by_batch.get(bid)
            if ck not in COPY_KINDS:
                err("assign_raw.jsonl line %d: copy_kind is %r, not one of %s" % (i, ck, ", ".join(COPY_KINDS)),
                    shape="assign_raw.jsonl: copy_kind outside corpus|gold|duplicate", where="line %d" % i)
            elif b is not None:
                if ck == "gold" and k not in {split_key(g) for g in as_list(b.get("gold_items"))}:
                    err("assign_raw.jsonl line %d: %s/%s is tagged gold and batch %s seeds no gold copy of it"
                        % (i, k[0], k[1], bid), shape="assign_raw.jsonl: a gold tag the batch does not bear out",
                        where="line %d" % i)
                if ck in ("corpus", "duplicate") and k not in live_of(bid):
                    err("assign_raw.jsonl line %d: %s/%s is tagged %s and batch %s does not hold it live (a gold copy "
                        "is never a corpus reading)" % (i, k[0], k[1], ck, bid),
                        shape="assign_raw.jsonl: a corpus tag on an item the batch does not hold live", where="line %d" % i)
                if ck == "duplicate" and k not in {split_key(x) for x in as_list(b.get("duplicate_items"))}:
                    err("assign_raw.jsonl line %d: %s/%s is tagged duplicate and is not batch %s's declared duplicate"
                        % (i, k[0], k[1], bid), shape="assign_raw.jsonl: a duplicate tag off the batch's duplicate",
                        where="line %d" % i)
            copies[(bid, r.get("agent"), k, ck)] += 1
            corpus = ck == "corpus"
        else:
            corpus = k in live_of(bid) or bid not in by_batch
        if corpus:
            per_item[k].append((r.get("agent"), r.get("replicate")))    # a gold copy is not a corpus reading
        per_key_agent[(k, r.get("agent"), r.get("batch"))] += 1
        positions[(r.get("batch"), r.get("agent"))].append(r.get("position"))
        edges.append((r.get("sub"), r.get("agent")))
    if len(ex_seen) > 1:
        err("assign_raw.jsonl mixes exemplar_read null with true|false; the arm is served to every reader or to "
            "none, and the field is null only when not served")
    # duplicates and gold copies: the same item to the same reader only as the batch's declared duplicate or as
    # a gold copy the batch lists in both items and gold_items
    for (k, agent, bid), n in per_key_agent.items():
        if n > 1:
            b = by_batch.get(bid) or {}
            dups = {split_key(x) for x in as_list(b.get("duplicate_items"))}
            allowed = (2 if k in dups else 1 if k in live_of(bid) else 0) + \
                sum(1 for g in as_list(b.get("gold_items")) if split_key(g) == k)
            if n > max(1, allowed):
                err("assign_raw.jsonl: %s/%s was read %d times by reader %s in %s and is not that batch's declared "
                    "duplicate item or gold copy" % (k[0], k[1], n, agent, bid),
                    shape="assign_raw.jsonl: one reader reading an item twice", where="%s/%s" % k)
    # copy_kind against the batch's tags: one corpus line and one duplicate line at most, gold lines as many as tagged
    for (bid, agent, k, ck), n in copies.items():
        b = by_batch.get(bid) or {}
        cap = sum(1 for g in as_list(b.get("gold_items")) if split_key(g) == k) if ck == "gold" else 1
        if ck in COPY_KINDS and n > cap:
            err("assign_raw.jsonl: %s/%s carries %d lines tagged %s by reader %s in %s, where the batch allows %d; no "
                "seeded copy counts as a corpus reading" % (k[0], k[1], n, ck, agent, bid, cap),
                shape="assign_raw.jsonl: more %s copies than the batch tags" % ck, where="%s/%s" % k)
    # no reader in two replicates of one item
    for k, ar in per_item.items():
        by_agent = collections.defaultdict(set)
        for a, rep in ar:
            by_agent[a].add(rep)
        for a, reps in by_agent.items():
            if len(reps) > 1:
                err("assign_raw.jsonl: reader %s appears in replicates %s of %s/%s; an item's replicates land on "
                    "different readers" % (a, sorted(reps), k[0], k[1]),
                    shape="assign_raw.jsonl: one reader in two replicates of the same item", where="%s/%s" % k)
    # positions a permutation of 1..n, and n the batch's count
    for (bid, a), pos in positions.items():
        ps = sorted(p for p in pos if isinstance(p, int))
        if ps != list(range(1, len(pos) + 1)):
            err("assign_raw.jsonl: batch %s reader %s: positions are not a permutation of 1..%d" % (bid, a, len(pos)),
                shape="assign_raw.jsonl: positions within a batch are not a permutation")
        b = by_batch.get(bid)
        if b and isinstance(b.get("n_items"), int) and len(pos) != b["n_items"]:
            err("assign_raw.jsonl: batch %s reader %s holds %d lines for a batch of %d items; a partial return is "
                "named in notes-B3.md and marked coverage_short, never absorbed" % (bid, a, len(pos), b["n_items"]),
                shape="assign_raw.jsonl: a batch short of its item count", where="%s/%s" % (bid, a))
    # the line count: distinct (item, replicate) over the analysed set against items x R
    if items_expected and raw:
        analysed, items = items_expected
        short = short_rooms(by_batch)
        got = {(k, rep) for k, ar in per_item.items() for _a, rep in ar}
        want = {(k, rep) for k in items for rep in range(1, R + 1)}
        missing = sorted((k, rep) for (k, rep) in want - got if k[0] not in short)
        if missing:
            err("assign_raw.jsonl lacks %d of the %d (item, replicate) readings items %d x R %d (first: %s/%s "
                "replicate %s); name the reader failure in notes-B3.md and mark the batch coverage_short rather "
                "than absorb it" % (len(missing), len(want), len(items), R, missing[0][0][0], missing[0][0][1], missing[0][1]))
        else:
            print("  readings %d cover items %d x R %d (%d lines with duplicates and gold copies)"
                  % (len(got & want), len(items), R, len(raw)))
        stray = sorted(k for k in set(per_item) | {x[0] for x in per_key_agent} if k not in items and k not in gold_keys)
        if stray:
            err("assign_raw.jsonl holds %d items outside the analysed set and the gold set (%s)"
                % (len(stray), ["%s/%s" % k for k in stray[:3]]))
        covered = {k[0] for k in per_item}
        miss_r = sorted({k[0] for k in items} - covered - short)
        if miss_r:
            err("%d rooms of the analysed set have no line in assign_raw.jsonl (%s); every room is in the fleet"
                % (len(miss_r), miss_r[:5]))
    ok, seen, total = connected(edges)
    if raw and not ok:
        err("the room-reader graph over what the fleet returned is in pieces (%d of %d nodes reachable from the "
            "first); re-run the gate after every reissue and redraw" % (seen, total))
    elif raw:
        print("  room-reader graph over the returns: one component over %d rooms and %d readers"
              % (len({a for a, _ in edges}), len({b for _, b in edges})))
    # pass 2, kept apart
    pass2 = jsonl(os.path.join(outdir, "assign_pass2.jsonl"))
    if pass2 is not None:
        keys1 = {(r.get("batch"), r.get("agent"), r.get("position")) for r in raw}
        for i, r in enumerate(pass2, 1):
            if (r.get("batch"), r.get("agent"), r.get("position")) not in keys1:
                err("assign_pass2.jsonl line %d names no pass-1 line (batch %r, agent %r, position %r is not in "
                    "assign_raw.jsonl); every pass-2 line names the pass-1 line it revises"
                    % (i, r.get("batch"), r.get("agent"), r.get("position")),
                    shape="assign_pass2.jsonl: a line naming no pass-1 line", where="line %d" % i)
        if pass2 and len(raw) > len(keys1):
            err("assign_raw.jsonl holds %d lines on %d (batch, agent, position) keys: the second pass was merged into "
                "the first; pass 2 goes to assign_pass2.jsonl and never back" % (len(raw), len(keys1)))
        if raw and any(r.get("pass") == 2 for r in raw):
            err("assign_raw.jsonl carries lines marked pass 2; the second pass never overwrites or joins the first")
    if n_waived:
        print("  lines waived by J by name (return_waivers.jsonl): %s" % ", ".join("%s %d" % kv for kv in sorted(n_waived.items())))
    return raw


# ---- the check ----------------------------------------------------------------------------------------

def check(root, outdir, ctx):
    stage = "B3"
    need(outdir, "RETURN-B3.md", "batches-B3.jsonl", "notes-B3.md")
    vlib.manifest_entry(outdir, stage, "the fleet")
    scheme = {r.get("id") for r in (jsonl(os.path.join(outdir, "scheme_final.jsonl")) or []) if r.get("id")}
    if not scheme:
        err("scheme_final.jsonl is absent or empty; stage B2 froze it and every third_order id resolves to it")
    gold = jsonl(os.path.join(outdir, "gold_items.jsonl")) or []
    gold_keys = {(g.get("sub"), g.get("theme_id")) for g in gold}
    if not gold_keys:
        err("gold_items.jsonl is absent or empty; the build leg seeds it at the rate notes-B2.md declares")
    items_expected = expected_items(stage, "coverage of the analysed set by the batches", outdir, ctx)
    check_return_spec(outdir, "RETURN-B3.md")
    check_notes(outdir)
    batches, R, by_batch = check_batches(outdir, ctx, gold_keys, items_expected)
    pd = check_packets(outdir, stage, by_batch)
    if pd and by_batch:
        have = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(pd, "*.md"))}
        for b in sorted(by_batch):
            if b not in have:
                err("batch %s has no packet %s.md; packets.py B3 writes one self-contained packet per batch line"
                    % (b, b), shape="04: batch without packet", where=b)
    gold_leaked(outdir, [pd, os.path.join(outdir, "_fleet_raw", stage)])

    dirs = fleet_dirs(outdir, stage)
    leg = "check" if dirs else "build"
    print("  leg: %s (%d dispatch folders with DONE)" % (leg, len(dirs)))
    if leg == "build":
        return
    need(outdir, "assign_raw.jsonl", "assign_pass2.jsonl", "multiplacement_log.jsonl",
         "multiplacement_register-B3.md", "fidelity-B3.md", "position-B3.md", "agent_report-B3.md")
    n_ret, n_ret2 = check_returns(outdir, dirs, scheme, by_batch, load_manifest(pd))
    raw = check_raw(outdir, ctx, scheme, by_batch, R, gold_keys, items_expected)
    if raw and n_ret and len(raw) != n_ret:
        warn("assign_raw.jsonl holds %d lines and the validated returns under _fleet_raw/B3 hold %d pass-1 lines; "
             "say in notes-B3.md which returns were set aside and why" % (len(raw), n_ret))
    p2 = jsonl(os.path.join(outdir, "assign_pass2.jsonl")) or []
    if n_ret2 and len(p2) != n_ret2:
        warn("assign_pass2.jsonl holds %d lines and the returns hold %d lines carrying \"revises\"; pass 2 is "
             "assembled from those lines" % (len(p2), n_ret2))
    vlib.licence_sentence(outdir, "fidelity-B3.md", "gold fidelity")
    vlib.licence_sentence(outdir, "multiplacement_register-B3.md", "the multiplacement rate")
    if "coverage_short" in text(outdir, "batches-B3.jsonl") and "coverage_short" not in text(outdir, "notes-B3.md"):
        err("batches-B3.jsonl marks a batch coverage_short and notes-B3.md does not name its rooms (section 3.1)")


# ---- the self-test ---------------------------------------------------------------------------------------

LINE = {"sub": "denmark", "theme_id": "t07", "batch": "B001", "agent": "a001", "replicate": 1, "position": 1,
        "third_order": ["T3-001"], "multi": False, "why": {"T3-001": "hands"}, "confidence": "clear",
        "read": "whole", "exemplar_read": None, "families_opened": ["G01"], "bag": False,
        "t_start": "t0", "t": "t1", "support": ["c0117"]}


def _line(**kw):
    d = dict(LINE)
    d.update(kw)
    return d


def _w(outdir, n, s):
    open(os.path.join(outdir, n), "w", encoding="utf-8").write(s)


def _wjl(outdir, n, rows):
    _w(outdir, n, "".join(json.dumps(x) + "\n" for x in rows))


def _batches(outdir):
    return jsonl(os.path.join(outdir, "batches-B3.jsonl"))


def _manifest(outdir, **upd):
    """MANIFEST.json of the fixture's packets, as packets.py B3 writes it; upd replaces whole entries."""
    rule = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}
    m = {b["batch"]: dict(rule, items=b["n_items"], item_bytes=400 * b["n_items"], bytes=900, sha256="x")
         for b in _batches(outdir)}
    m.update(upd)
    json.dump(m, open(os.path.join(outdir, "_packets-B3", "MANIFEST.json"), "w"), indent=1)


def _base(outdir, root):
    """Three batches at R = 2. Replicate 1 spreads the two rooms over two batches (B001 holds denmark and a gold
    copy of asoiaf/t02, listed in items and gold_items; B003 holds asoiaf); replicate 2 holds both in B002. A
    split of denmark/t07 into t08 and t09 sits in out/recut/ and is withdrawn, so its children are not expected."""
    os.makedirs(os.path.join(outdir, "_packets-B3"), exist_ok=True)
    w = lambda n, s: _w(outdir, n, s)
    w("dropped.jsonl", json.dumps({"sub": "sweden", "why": "fixture"}) + "\n")
    w("scheme_final.jsonl", "\n".join(json.dumps(x) for x in (
        {"id": "T3-001", "name": "recruiting", "gloss": "asking outsiders for hands"},
        {"id": "T3-002", "name": "holding", "gloss": "defending a border"})) + "\n")
    w("gold_items.jsonl", json.dumps({"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-002"],
                                      "confidence": "clear", "reason": "a border"}) + "\n")
    w("RETURN-B3.md", "# RETURN-B3\n\nRule 0. Single placement, exception on the record: a second placement owes "
      "why_not_one and a multiplacement_log.jsonl line.\n\n```json\n{\"agent\": \"a017\", \"predicted_confusion\": []}\n"
      "{\"sub\": \"...\", \"exemplar_read\": null}\nEND-OF-RETURN\n```\n\nConfirm that you reached the marker.\n")
    w("notes-B3.md", "Seed 20260827. Item cap 15 per batch. R = 2. Gold seeding rate 0.1, tagged in the batches. "
      "Exemplar arm: none. Reissue policy: twice. Batch count 3, reader count 3. Warm-up in reserve; bag flags none; "
      "order of batches seeded.\n")
    w("run_manifest.json", json.dumps([{"stage": "B3", "model": "cheap", "seeds": {"fleet": 20260827},
                                        "decoding": {"temperature": 0}, "n_agents": 2}]))
    rc = os.path.join(outdir, "recut")
    os.makedirs(rc, exist_ok=True)
    _wjl(rc, "themes.jsonl", [{"sub": "denmark", "theme_id": "t08", "parent": "t07", "code_ids": ["c0117"]},
                              {"sub": "denmark", "theme_id": "t09", "parent": "t07", "code_ids": ["c0118"]}])
    _wjl(rc, "codes.jsonl", [{"sub": "denmark", "code_id": "c0117", "theme_id": "t08", "parent": "t07"},
                             {"sub": "denmark", "code_id": "c0118", "theme_id": "t09", "parent": "t07"}])
    _w(rc, "WITHDRAWN.json", json.dumps({"ruled_by": "J 2026-10-12", "reason": "the coders' layer"}))
    bl = lambda bid, agent, rep, rooms, items, gold=(): {
        "batch": bid, "agent": agent, "n_items": len(items), "replicate": rep, "rooms": rooms, "exemplar_items": [],
        "gold_items": list(gold), "duplicate_items": [], "warmup_items": [], "reissue": 0, "original_agent": None,
        "seed": 20260827, "items": items}
    _wjl(outdir, "batches-B3.jsonl", [
        bl("B001", "a001", 1, ["denmark"], ["denmark/t07", "asoiaf/t02"], ["asoiaf/t02"]),
        bl("B003", "a003", 1, ["asoiaf"], ["asoiaf/t02"]),
        bl("B002", "a002", 2, ["denmark", "asoiaf"], ["asoiaf/t02", "denmark/t07"])])
    for bid in ("B001", "B002", "B003"):
        open(os.path.join(outdir, "_packets-B3", "%s.md" % bid), "w").write("# Batch %s\n" % bid)
    open(os.path.join(outdir, "_packets-B3", "index.md"), "w").write("# The scheme: index\n")
    open(os.path.join(outdir, "_packets-B3", "G01.md"), "w").write("# Family G01\n")
    _manifest(outdir)


def _rebatch(outdir, fn):
    rows = _batches(outdir)
    fn({b["batch"]: b for b in rows})
    _wjl(outdir, "batches-B3.jsonl", rows)


def _plant_item_reader_twice(outdir, root):
    _base(outdir, root)
    _rebatch(outdir, lambda B: B["B002"].update(agent="a001"))


def _plant_packet_16(outdir, root):
    _base(outdir, root)
    _manifest(outdir, B001={"items": 16, "item_bytes": 6400, "count_key": "position"})


def _plant_packet_in_parts(outdir, root):
    _base(outdir, root)
    _manifest(outdir, B001={"items": 2, "item_bytes": 800, "group": "B001", "part": 1, "parts": 2})


def _plant_withdrawn_child(outdir, root):
    _base(outdir, root)
    _rebatch(outdir, lambda B: B["B002"].update(items=B["B002"]["items"] + ["denmark/t08"], n_items=3))
    _manifest(outdir)


def _plant_split_standing(outdir, root):
    """The same split not withdrawn: its children stand, the parent is gone, and the batches owe t08 and t09."""
    _base(outdir, root)
    os.replace(os.path.join(outdir, "recut", "WITHDRAWN.json"), os.path.join(outdir, "recut", "WITHDRAWN.json.off"))


def _plant_gold_not_in_items(outdir, root):
    _base(outdir, root)
    _rebatch(outdir, lambda B: B["B001"].update(items=["denmark/t07"], n_items=1))
    _manifest(outdir)


def _returns(outdir, lines_by_batch):
    for bid, agent, lines in lines_by_batch:
        d = os.path.join(outdir, "_fleet_raw", "B3", bid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "r1.jsonl"), "w") as f:
            f.write(json.dumps({"agent": agent, "predicted_confusion": ["T3-001", "T3-002"], "why": "close"}) + "\n")
            for ln in lines:
                f.write(json.dumps(ln) + "\n")
    open(os.path.join(outdir, "_fleet_raw", "B3", "DONE"), "w").write("{}\n")


def _lines():
    l1 = [_line(), _line(sub="asoiaf", theme_id="t02", position=2, third_order=["T3-002"], support=["c0011"])]
    l3 = [_line(batch="B003", agent="a003", sub="asoiaf", theme_id="t02", position=1, third_order=["T3-002"],
                support=["c0011"])]
    l2 = [_line(batch="B002", agent="a002", replicate=2, sub="asoiaf", theme_id="t02", position=1,
                third_order=["T3-002"], support=["c0011"]),
          _line(batch="B002", agent="a002", replicate=2, position=2)]
    return l1, l2, l3


def _write_raw(outdir, l1, l2, l3, rev=None, short2=False):
    """The returns (B001's with a pass-2 line after its pass-1 lines, which counts toward no item) and the
    files the check leg assembles from them."""
    rev = rev if rev is not None else [_line(revises=1, third_order=["T3-002"], why={"T3-002": "on reflection"})]
    r2 = l2
    if short2:
        r2 = l2[:1] + [_line(batch="B002", agent="a002", replicate=2, revises=1, sub="asoiaf", theme_id="t02",
                             third_order=["T3-001"], support=["c0011"])]
    _returns(outdir, (("B001", "a001", l1 + rev), ("B002", "a002", r2), ("B003", "a003", l3)))
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2) + "\n")
    _w(outdir, "assign_pass2.jsonl", "".join(json.dumps(dict(x, pass_=2)) + "\n" for x in rev))


def _check_base(outdir, root):
    _base(outdir, root)
    l1, l2, l3 = _lines()
    _write_raw(outdir, l1, l2, l3)
    w = lambda n, s: _w(outdir, n, s)
    w("multiplacement_log.jsonl", "")
    lic = "The figure bounds whether the instrument decides, not whether it is right.\n"
    w("multiplacement_register-B3.md", "# register\n\nrate 0.\n" + lic)
    w("fidelity-B3.md", "# fidelity\n\nB001 a001: 1 of 1.\n" + lic)
    w("position-B3.md", "# position\n\nslope 0.\n")
    w("agent_report-B3.md", "# agents\n\na001 predicted T3-001 vs T3-002.\n")
    return l1, l2, l3


def _plant_multi_without_record(outdir, root):
    l1, l2, l3 = _check_base(outdir, root)
    l1[0] = _line(third_order=["T3-001", "T3-002"], multi=True, support=["c0117", "c0118"])
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2) + "\n")


def _plant_label_only(outdir, root):
    l1, l2, l3 = _check_base(outdir, root)
    l2[1] = _line(batch="B002", agent="a002", replicate=2, position=2, read="label-only")
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2) + "\n")


def _plant_missing_reading(outdir, root):
    l1, l2, l3 = _check_base(outdir, root)
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2[:1]) + "\n")


def _plant_revises_off_pass1(outdir, root):
    l1, l2, l3 = _check_base(outdir, root)
    _write_raw(outdir, l1, l2, l3, rev=[_line(revises=9, third_order=["T3-002"])])


def _plant_return_short_beside_pass2(outdir, root):
    """B002's reader returned one pass-1 line and one pass-2 line: two lines, but one counts."""
    l1, l2, l3 = _check_base(outdir, root)
    _write_raw(outdir, l1, l2, l3, short2=True)


def _assembled(l1, l2, l3):
    """The fixture's lines as tools/assemble.py writes them: copy_kind tagged, the readers' timestamps dropped for
    the dispatch's packet_elapsed_s."""
    for ls in (l1, l2, l3):
        for x in ls:
            x.pop("t_start", None)
            x.pop("t", None)
            x["packet_elapsed_s"] = 12.5
            x["copy_kind"] = "gold" if (x["batch"], x["sub"]) == ("B001", "asoiaf") else "corpus"


def _plant_gold_tagged_corpus(outdir, root):
    """A gold copy tagged corpus: it would count as a reading of the analysed set."""
    l1, l2, l3 = _check_base(outdir, root)
    _assembled(l1, l2, l3)
    l1[1]["copy_kind"] = "corpus"
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2) + "\n")


def _plant_no_measured_time(outdir, root):
    """The readers' timestamps dropped and no packet_elapsed_s carried in their place."""
    l1, l2, l3 = _check_base(outdir, root)
    _assembled(l1, l2, l3)
    del l2[0]["packet_elapsed_s"]
    _w(outdir, "assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l3 + l2) + "\n")


PLANTED = [
    ("a gold copy tagged corpus", _plant_gold_tagged_corpus, "does not hold it live"),
    ("a line with no measured time", _plant_no_measured_time, "neither both timestamps"),
    ("an item meeting one reader twice", _plant_item_reader_twice, "meets reader a001 in two replicates"),
    ("a 16-item packet", _plant_packet_16, "holds 16 items"),
    ("a packet in parts", _plant_packet_in_parts, "never a part of a batch"),
    ("a withdrawn child batched", _plant_withdrawn_child, "as the store stands now"),
    ("a standing split owes its kids", _plant_split_standing, "replicate 1 lacks"),
    ("a gold copy not among items", _plant_gold_not_in_items, "a gold copy is listed in both"),
    ("multi line without a record", _plant_multi_without_record, "no record in multiplacement_log.jsonl"),
    ("read label-only", _plant_label_only, "label-only"),
    ("a reading missing against items x R", _plant_missing_reading, "(item, replicate) readings"),
    ("pass 2 revising no pass-1 line", _plant_revises_off_pass1, "names no pass-1 line of this return"),
    ("pass 2 not counted as items", _plant_return_short_beside_pass2, "returned 1 lines for a batch of 2"),
]
