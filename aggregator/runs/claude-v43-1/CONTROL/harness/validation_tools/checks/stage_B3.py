"""checks/stage_B3.py: the close-check of stage B3, the assignment fleet, v38.

Written from stages/STAGE-B3-coding-fleet.md (Outputs, sections 1 to 3 and 3.6, Close),
FLEET.md, and the v37 check it descends from (_v37-source/tools/validate.py, stage04). It checks
the SHAPE of the stage's files: existence, parse, ids that resolve, counts that reconcile. It
cannot check whether a placement is right, and section 3.6 says the last two of its list (read,
families_opened, label-only) are screened by hand as well.

Stage B3 is a fleet stage; the check decides which leg it is closing:

  build leg   no DONE anywhere under out/_fleet_raw/B3/: RETURN-B3.md, batches-B3.jsonl and the
              packets exist; the batches cover the analysed set and every second-order theme of
              it (assignment_items_expected, computed here from the store since counts.py's
              number is the same sum); no room meets a reader twice, each room's replicates sit
              on different readers, the room-batch graph is one component; notes-B3.md carries
              the declarations; the manifest entry is appended; gold_items.jsonl is nowhere a
              reader can reach.
  check leg   a DONE under out/_fleet_raw/B3/ or out/_fleet_raw/B3/batch-k/: everything the
              build leg owed, and assign_raw.jsonl, assign_pass2.jsonl, multiplacement_log.jsonl
              and the four reports, with section 3.6's list run on assign_raw.jsonl and the
              returns cross-checked against the batches.

Files the stage file names without giving their fields, checked for existence and the licence
sentence only: fidelity-B3.md, position-B3.md, agent_report-B3.md, multiplacement_register-B3.md,
notes-B3.md (declarations by keyword), RETURN-B3.md (by keyword). assign_pass2.jsonl's fields
are not given beyond "names the pass-1 line it revises": a pass-2 line must key to a pass-1
(batch, agent, position).

The line count. Section 3.6 says items x R; section 1.4 puts one duplicate item in every batch
and section 1.6 seeds gold copies, so the raw file legitimately holds more lines than items x R.
The check reconciles two ways: every (batch, agent) return holds the batch's n_items, and the
distinct (item, replicate) pairs over the analysed set number items x R, a shortfall named item
by item unless the batch is marked coverage_short.

Not carried from v37:
  - R read off a batch line's "R" field or notes-B3.md by regex; v38 fixes R = 2 in section 1
    and the batch line carries replicate, so R is the largest replicate on the batches.
  - the v37 ids `case_theme` and `second_order`: now `theme_id` and `third_order`.
  - the community-agent graph over assign_raw.jsonl only: v38 runs the gate at the build leg
    over batches-B3.jsonl as well, since section 1.2 refuses to build a fleet in pieces.
"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

CONF = ("clear", "arguable")
READ = ("whole", "theme-block")
BATCH_FIELDS = ("batch", "agent", "n_items", "replicate", "rooms", "exemplar_items", "gold_items",
                "duplicate_items", "warmup_items", "reissue", "original_agent", "seed", "items")
LINE_FIELDS = ("sub", "theme_id", "batch", "agent", "replicate", "position", "third_order", "multi", "why",
               "confidence", "read", "exemplar_read", "families_opened", "bag", "t_start", "t", "support")
MULTI_FIELDS = ("sub", "theme_id", "key", "batch", "agent", "replicate", "position", "primary", "additional",
                "why_not_one", "why_this_one", "support_primary", "support_additional", "dispensable")
KB50 = 50 * 1024


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
    """assignment_items_expected: every second-order theme of the store over the analysed set.
    (analysed rooms, set of (sub, theme_id)) or None having said what was not checked."""
    sets = vlib.analysed_set(stage, what, outdir, ctx)
    if sets is None:
        return None
    analysed, _d = sets
    themes = vlib.store_themes(ctx)
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


def check_batches(outdir, ctx, gold_keys, items_expected):
    """batches-B3.jsonl: fields, ids, coverage, the two gates. Returns (rows, R, by_batch)."""
    rows = jsonl(os.path.join(outdir, "batches-B3.jsonl")) or []
    if not rows:
        err("batches-B3.jsonl is empty; the allocator writes one line per batch before any packet is built")
        return rows, 2, {}
    themes = vlib.store_themes(ctx)
    analysed = items_expected[0] if items_expected else None
    by_batch, room_agents, edges = {}, collections.defaultdict(list), []
    items_by_rep = collections.defaultdict(set)
    rooms_by_rep = collections.defaultdict(set)
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
            err("batches-B3.jsonl %s: n_items %d but items lists %d; the count is computed from the list"
                % (bid, b["n_items"], len(items)), shape="batches-B3.jsonl: n_items off its items", where=str(bid))
        for k in items:
            if k not in themes:
                err("batches-B3.jsonl %s lists item %s/%s, not a second-order theme in package/store/themes.jsonl"
                    % (bid, k[0], k[1]), shape="batches-B3.jsonl: an item not in the store", where=str(bid))
            if k[0] not in rooms:
                err("batches-B3.jsonl %s lists item %s/%s from a room not in its rooms; a batch holds whole rooms"
                    % (bid, k[0], k[1]), shape="batches-B3.jsonl: an item outside the batch's rooms", where=str(bid))
        for r in rooms:
            if analysed is not None and r not in analysed:
                err("batches-B3.jsonl %s holds room %r, which is not in the analysed set (the frame minus "
                    "dropped.jsonl)" % (bid, r), shape="batches-B3.jsonl: a room outside the analysed set", where=str(bid))
            have = {k[1] for k in items if k[0] == r}
            want = {k[1] for k in themes if k[0] == r}
            if want - have and not b.get("coverage_short"):
                err("batches-B3.jsonl %s holds room %s without %d of its second-order themes (%s); no room is ever "
                    "split" % (bid, r, len(want - have), sorted(want - have)[:3]),
                    shape="batches-B3.jsonl: a room split across batches", where=str(bid))
            room_agents[r].append((agent, rep))
            edges.append((r, bid))
            if not b.get("coverage_short"):
                rooms_by_rep[rep].add(r)
        for k in items:
            items_by_rep[rep].add(k)
        for g in as_list(b.get("gold_items")):
            if split_key(g) not in gold_keys:
                err("batches-B3.jsonl %s tags gold item %r, which gold_items.jsonl does not hold" % (bid, g),
                    shape="batches-B3.jsonl: a gold tag off the key", where=str(bid))
        for dkey in as_list(b.get("duplicate_items")):
            if split_key(dkey) not in set(items):
                err("batches-B3.jsonl %s tags duplicate %r, which is not among its items" % (bid, dkey),
                    shape="batches-B3.jsonl: a duplicate tag off the batch", where=str(bid))
        if isinstance(b.get("reissue"), int) and b["reissue"] > 2:
            err("batches-B3.jsonl %s: reissue %d; section 2 reissues at most twice, then the build leg rebuilds"
                % (bid, b["reissue"]), shape="batches-B3.jsonl: reissue beyond two", where=str(bid))
    R = max(reps) if reps else 2
    if R != 2:
        warn("batches-B3.jsonl: replicates run to %d; section 1 fixes R = 2, say in notes-B3.md what more bought" % R)
    # gate 1: no room meets the same reader twice; replicates on different readers
    for r, ar in room_agents.items():
        agents = [a for a, _ in ar]
        if len(agents) != len(set(agents)):
            err("batches-B3.jsonl: room %s meets reader %s twice; reject and redraw (gate 1)"
                % (r, next(a for a in agents if agents.count(a) > 1)),
                shape="batches-B3.jsonl: a room meeting the same reader twice", where=str(r))
        rs = [p for _, p in ar]
        if len(rs) != len(set(rs)):
            err("batches-B3.jsonl: room %s sits in two batches of the same replicate; each replicate covers a room "
                "once" % r, shape="batches-B3.jsonl: a room twice in one replicate", where=str(r))
    # gate 2: one component
    ok, seen, total = connected(edges)
    if not ok:
        err("batches-B3.jsonl: the room-reader graph is in pieces (%d of %d nodes reachable from the first); "
            "section 1.2 refuses to build a fleet in pieces, redraw" % (seen, total))
    # coverage: every replicate covers the analysed set and every item
    if items_expected:
        analysed, items = items_expected
        rooms_with_items = {k[0] for k in items}
        for rep in sorted(rooms_by_rep):
            miss_r = sorted(rooms_with_items - rooms_by_rep[rep])
            if miss_r:
                err("batches-B3.jsonl: replicate %s holds no batch for %d rooms of the analysed set (%s); every room "
                    "is in the fleet at R = 2" % (rep, len(miss_r), miss_r[:5]))
            miss_i = sorted(items - items_by_rep[rep])
            if miss_i and not miss_r:
                err("batches-B3.jsonl: replicate %s lacks %d of the %d items assignment_items_expected counts (%s)"
                    % (rep, len(miss_i), len(items), ["%s/%s" % k for k in miss_i[:3]]))
        if not rooms_by_rep:
            err("batches-B3.jsonl covers no room of the analysed set")
    print("  batches %d, R %d, rooms %d, graph %s" % (len(rows), R, len(room_agents), "one component" if ok else "IN PIECES"))
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


def check_packets(outdir, stage):
    pd = packets_dir(outdir, stage)
    if pd is None:
        err("no _packets-%s/ in the output directory; the build leg writes the index page, the family pages and "
            "one file per batch with packets.py %s before it closes at packets-out" % (stage, stage))
        return None
    files = sorted(glob.glob(os.path.join(pd, "*.md")))
    if not files:
        err("%s holds no .md packet" % os.path.relpath(pd, outdir))
    for p in files:
        n = os.path.getsize(p)
        if n > KB50:
            err("%s/%s is %d bytes, over FLEET.md's 50 KB ceiling; lower the cap or split the family page"
                % (os.path.relpath(pd, outdir), os.path.basename(p), n),
                shape="_packets-%s: a packet over 50 KB" % stage, where=os.path.basename(p))
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

def check_returns(outdir, dirs, scheme, by_batch):
    """The returns as fleet.py left them: a prediction line first, then the batch's item count."""
    total = 0
    for d in dirs:
        rel = os.path.relpath(d, outdir)
        for p in sorted(glob.glob(os.path.join(d, "*", "*.jsonl"))):
            rows = jsonl(p) or []
            name = os.path.basename(os.path.dirname(p))
            reader = os.path.basename(p)[:-6]
            preds = [r for r in rows if "predicted_confusion" in r]
            lines = [r for r in rows if "predicted_confusion" not in r]
            total += len(lines)
            if not preds:
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
                err("%s/%s/%s returned %d lines for a batch of %d items; a partial return is not a return, it is "
                    "reissued or the batch is marked coverage_short" % (rel, name, reader, len(lines), b["n_items"]),
                    shape="_fleet_raw/04: a return short of its batch", where="%s/%s" % (name, reader))
    return total


def check_raw(outdir, ctx, scheme, by_batch, R, gold_keys, items_expected):
    raw = jsonl(os.path.join(outdir, "assign_raw.jsonl")) or []
    if not raw:
        err("assign_raw.jsonl is empty; the check leg assembles it from the returns, keyed on packet heading and "
            "cell number")
    vlib.store_codes(ctx)
    codes = ctx["codes"]
    if not codes:
        err("package/store/codes.jsonl holds no concept, so no support id could be resolved")
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
        if not sa or sa & sp:
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

    per_item = collections.defaultdict(list)
    per_key_agent = collections.Counter()
    positions = collections.defaultdict(list)
    edges = []
    ex_seen = set()
    for i, r in enumerate(raw, 1):
        for k in LINE_FIELDS:
            if k not in r:
                err("assign_raw.jsonl line %d carries no %s; the return line of section 1.5 carries it, and the v35 "
                    "analyst found a field missing on every row at the end of the run" % (i, k),
                    shape="assign_raw.jsonl: a line without %s" % k, where="line %d" % i)
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
        sup = as_list(r.get("support"))
        for c in sup:
            if codes and (r.get("sub"), c) not in codes:
                err("assign_raw.jsonl line %d: support %r does not resolve in package/store/codes.jsonl for %s"
                    % (i, c, r.get("sub")), shape="assign_raw.jsonl: a support id that does not resolve",
                    where="line %d" % i)
        if r.get("multi"):
            extra = set(so[1:])
            have = mkeys.get((r.get("sub"), r.get("theme_id"), r.get("agent")), set())
            if not extra:
                err("assign_raw.jsonl line %d: multi is true with one id" % i,
                    shape="assign_raw.jsonl: multi with a single id", where="line %d" % i)
            elif not extra <= have:
                err("assign_raw.jsonl line %d: multi-assigned with no record in multiplacement_log.jsonl for %s; "
                    "reduce the line to its primary and write the defect" % (i, sorted(extra - have)),
                    shape="assign_raw.jsonl: a multi line with no multiplacement record", where="line %d" % i)
            if len(set(sup)) < len(set(so)):
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
        per_item[k].append((r.get("agent"), r.get("replicate")))
        per_key_agent[(k, r.get("agent"), r.get("batch"))] += 1
        positions[(r.get("batch"), r.get("agent"))].append(r.get("position"))
        edges.append((r.get("sub"), r.get("agent")))
    if len(ex_seen) > 1:
        err("assign_raw.jsonl mixes exemplar_read null with true|false; the arm is served to every reader or to "
            "none, and the field is null only when not served")
    # duplicates and gold copies: the same item to the same reader only as the batch's declared duplicate
    for (k, agent, bid), n in per_key_agent.items():
        if n > 1:
            b = by_batch.get(bid) or {}
            dups = {split_key(x) for x in as_list(b.get("duplicate_items"))}
            if k not in dups:
                err("assign_raw.jsonl: %s/%s was read %d times by reader %s in %s and is not that batch's declared "
                    "duplicate item" % (k[0], k[1], n, agent, bid),
                    shape="assign_raw.jsonl: one reader reading an item twice", where="%s/%s" % k)
    # no reader in two replicates of one item
    for k, ar in per_item.items():
        by_agent = collections.defaultdict(set)
        for a, rep in ar:
            by_agent[a].add(rep)
        for a, reps in by_agent.items():
            if len(reps) > 1:
                err("assign_raw.jsonl: reader %s appears in replicates %s of %s/%s; each room's replicates land on "
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
        short = {r for b in by_batch.values() if b.get("coverage_short") for r in as_list(b.get("rooms"))}
        got = {(k, rep) for k, ar in per_item.items() for _a, rep in ar}
        want = {(k, rep) for k in items for rep in range(1, R + 1)}
        missing = sorted((k, rep) for (k, rep) in want - got if k[0] not in short)
        if missing:
            err("assign_raw.jsonl lacks %d of the %d (item, replicate) readings items %d x R %d (first: %s/%s "
                "replicate %s); name the reader failure in notes-B3.md and mark the batch coverage_short rather "
                "than absorb it" % (len(missing), len(want), len(items), R, missing[0][0][0], missing[0][0][1], missing[0][1]))
        else:
            print("  readings %d cover items %d x R %d (%d lines with duplicates and gold copies)"
                  % (len(got), len(items), R, len(raw)))
        stray = sorted(k for k in per_item if k not in items and k not in gold_keys)
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
    pd = check_packets(outdir, stage)
    if pd and by_batch:
        have = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(pd, "*.md"))}
        for b in sorted(by_batch):
            if b not in have and not any(h.startswith(b + "-p") for h in have):
                err("batch %s has no packet (%s.md, or parts %s-p1.md ... for a batch over the ceiling)" % (b, b, b),
                    shape="04: batch without packet", where=b)
    gold_leaked(outdir, [pd, os.path.join(outdir, "_fleet_raw", stage)])

    dirs = fleet_dirs(outdir, stage)
    leg = "check" if dirs else "build"
    print("  leg: %s (%d dispatch folders with DONE)" % (leg, len(dirs)))
    if leg == "build":
        return
    need(outdir, "assign_raw.jsonl", "assign_pass2.jsonl", "multiplacement_log.jsonl",
         "multiplacement_register-B3.md", "fidelity-B3.md", "position-B3.md", "agent_report-B3.md")
    n_ret = check_returns(outdir, dirs, scheme, by_batch)
    raw = check_raw(outdir, ctx, scheme, by_batch, R, gold_keys, items_expected)
    if raw and n_ret and len(raw) != n_ret:
        warn("assign_raw.jsonl holds %d lines and the validated returns under _fleet_raw/B3 hold %d; say in "
             "notes-B3.md which returns were set aside and why" % (len(raw), n_ret))
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


def _base(outdir, root):
    os.makedirs(os.path.join(outdir, "_packets-B3"), exist_ok=True)
    w = lambda n, s: open(os.path.join(outdir, n), "w", encoding="utf-8").write(s)
    w("dropped.jsonl", json.dumps({"sub": "sweden", "why": "fixture"}) + "\n")
    w("scheme_final.jsonl", "\n".join(json.dumps(x) for x in (
        {"id": "T3-001", "name": "recruiting", "gloss": "asking outsiders for hands"},
        {"id": "T3-002", "name": "holding", "gloss": "defending a border"})) + "\n")
    w("gold_items.jsonl", json.dumps({"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-002"],
                                      "confidence": "clear", "reason": "a border"}) + "\n")
    w("RETURN-B3.md", "# RETURN-B3\n\nRule 0. Single placement, exception on the record: a second placement owes "
      "why_not_one and a multiplacement_log.jsonl line.\n\n```json\n{\"agent\": \"a017\", \"predicted_confusion\": []}\n"
      "{\"sub\": \"...\", \"exemplar_read\": null}\nEND-OF-RETURN\n```\n\nConfirm that you reached the marker.\n")
    w("notes-B3.md", "Seed 20260827. Item cap 40 per batch. R = 2. Gold seeding rate 0.1, tagged in the batches. "
      "Exemplar arm: none. Reissue policy: twice. Batch count 2, reader count 2. Warm-up in reserve; bag flags none; "
      "order of batches seeded.\n")
    w("run_manifest.json", json.dumps([{"stage": "B3", "model": "cheap", "seeds": {"fleet": 20260827},
                                        "decoding": {"temperature": 0}, "n_agents": 2}]))
    batches = []
    for rep, bid, agent in ((1, "B001", "a001"), (2, "B002", "a002")):
        batches.append({"batch": bid, "agent": agent, "n_items": 2, "replicate": rep, "rooms": ["denmark", "asoiaf"],
                        "exemplar_items": [], "gold_items": [], "duplicate_items": [], "warmup_items": [],
                        "reissue": 0, "original_agent": None, "seed": 20260827,
                        "items": ["denmark/t07", "asoiaf/t02"]})
    w("batches-B3.jsonl", "\n".join(json.dumps(b) for b in batches) + "\n")
    for bid in ("B001", "B002"):
        open(os.path.join(outdir, "_packets-B3", "%s.md" % bid), "w").write("# Batch %s\n" % bid)


def _plant_room_twice(outdir, root):
    _base(outdir, root)
    rows = jsonl(os.path.join(outdir, "batches-B3.jsonl"))
    rows[1]["agent"] = "a001"
    open(os.path.join(outdir, "batches-B3.jsonl"), "w").write("\n".join(json.dumps(b) for b in rows) + "\n")


def _returns(outdir, lines_by_batch):
    for bid, agent, lines in lines_by_batch:
        d = os.path.join(outdir, "_fleet_raw", "B3", bid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "r1.jsonl"), "w") as f:
            f.write(json.dumps({"agent": agent, "predicted_confusion": ["T3-001", "T3-002"], "why": "close"}) + "\n")
            for ln in lines:
                f.write(json.dumps(ln) + "\n")
    open(os.path.join(outdir, "_fleet_raw", "B3", "DONE"), "w").write("{}\n")


def _check_base(outdir, root):
    _base(outdir, root)
    l1 = [_line(), _line(sub="asoiaf", theme_id="t02", position=2, third_order=["T3-002"], support=["c0011"])]
    l2 = [_line(batch="B002", agent="a002", replicate=2, sub="asoiaf", theme_id="t02", position=1,
                third_order=["T3-002"], support=["c0011"]),
          _line(batch="B002", agent="a002", replicate=2, position=2)]
    _returns(outdir, (("B001", "a001", l1), ("B002", "a002", l2)))
    w = lambda n, s: open(os.path.join(outdir, n), "w", encoding="utf-8").write(s)
    w("assign_raw.jsonl", "\n".join(json.dumps(x) for x in l1 + l2) + "\n")
    w("assign_pass2.jsonl", json.dumps(dict(l1[0], pass_=2)) + "\n")
    w("multiplacement_log.jsonl", "")
    lic = "The figure bounds whether the instrument decides, not whether it is right.\n"
    w("multiplacement_register-B3.md", "# register\n\nrate 0.\n" + lic)
    w("fidelity-B3.md", "# fidelity\n\nB001 a001: 1 of 1.\n" + lic)
    w("position-B3.md", "# position\n\nslope 0.\n")
    w("agent_report-B3.md", "# agents\n\na001 predicted T3-001 vs T3-002.\n")
    return l1, l2


def _plant_multi_without_record(outdir, root):
    l1, l2 = _check_base(outdir, root)
    l1[0] = _line(third_order=["T3-001", "T3-002"], multi=True, support=["c0117", "c0118"])
    open(os.path.join(outdir, "assign_raw.jsonl"), "w").write("\n".join(json.dumps(x) for x in l1 + l2) + "\n")


def _plant_label_only(outdir, root):
    l1, l2 = _check_base(outdir, root)
    l2[1] = _line(batch="B002", agent="a002", replicate=2, position=2, read="label-only")
    open(os.path.join(outdir, "assign_raw.jsonl"), "w").write("\n".join(json.dumps(x) for x in l1 + l2) + "\n")


def _plant_missing_reading(outdir, root):
    l1, l2 = _check_base(outdir, root)
    open(os.path.join(outdir, "assign_raw.jsonl"), "w").write("\n".join(json.dumps(x) for x in l1 + l2[:1]) + "\n")


PLANTED = [
    ("a room meeting one reader twice", _plant_room_twice, "meets reader a001 twice"),
    ("multi line without a record", _plant_multi_without_record, "no record in multiplacement_log.jsonl"),
    ("read label-only", _plant_label_only, "label-only"),
    ("a reading missing against items x R", _plant_missing_reading, "(item, replicate) readings"),
]
