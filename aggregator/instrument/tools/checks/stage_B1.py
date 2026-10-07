"""checks/stage_B1.py: the close-check of stage B1, the scheme (third-order themes), v38.

Written from stages/STAGE-B1-coding-third-order-scheme.md (its Outputs block, sections 1 to 7, its Close
section) and from the v37 check it descends from (_v37-source/tools/validate.py, stage02). What it
checks is the SHAPE of the stage's files: existence, parse, ids that resolve, counts that
reconcile. It cannot check whether a judgement is right.

Stage B1 runs in legs, one per room block. Required at every close: `prior.md`,
`scheme/scheme_current.jsonl` (the grouping on disk), `theme_discovery.jsonl`, `notes-B1.md`, and
the diary. The shipped files (`scheme.md`, `scheme.jsonl`, `families.jsonl`, `confusions.md`,
`tier_history.jsonl`, `findings.jsonl`) are required once the pass has ended, which the check
reads from `handback-B1.md` or `scheme.jsonl` existing; until then it prints the pass's progress.
Stage B2's open-check catches a stage B1 that never wrote them.

Files the stage names without giving fields, checked for existence and content only:
`scheme.md` (every T3 id in it resolves, every scheme id appears in it), `confusions.md` (every T3
id in it resolves), `notes-B1.md`, `handback-B1.md`.

Exemplars: rule 3 and section 3 say the close-check resolves every exemplar through `cite.py
--resolve` and rejects one that resolves to a coder's note or a label. This module does what
`cite.py --resolve` does, in process: the quote must be a substring of a code's `text`; a quote
that is found only in a `first_order`, `second_order` or `note` field is rejected by name.

Not carried from v37's stage02:
- `_groups-B1.jsonl` (renamed: v38's grouping on disk is `scheme/scheme_current.jsonl`).
- the `gate` field (v38 gates are `must_show`, `must_not_show`, `decide_when_both`).
- S07 ids (v38: T3-007).
- the departures.jsonl line saying saturation is not a reported figure (v38 records saturation in
  `theme_discovery.jsonl`, section 6, and reports new kinds per hundred from it).
- the warning at fewer than eight themes for stage D4's feature space (v38 sets no floor or
  ceiling on the count; section 2).
"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need, T3, FAMILY, PROBLEMS

T3_ANY = re.compile(r"\bT3-\d{3}\b")
EVENTS = ("created", "relabelled", "split", "merged", "retired", "members_changed", "rescoped", "moved_to_rare")
CONSEQUENTIAL = ("split", "merged", "retired", "rescoped", "moved_to_rare")   # a move that needs prompted_by (section 6)
WARRANTS = ("entailed", "read", "inferred")
STATUS = ("standing", "bounded", "withdrawn")
SCHEME_KEYS = ("id", "name", "gloss", "family", "tier", "must_show", "must_not_show", "decide_when_both",
               "discriminators", "varies", "is_not", "gate_parts", "exemplars")   # rivals sits in each exemplar (line below)
DISCOVERY_KEYS = ("theme", "label", "t", "sub", "trigger", "rooms_read", "themes_read", "codes_read")


def _current_path(outdir):
    for p in (os.path.join(outdir, "scheme", "scheme_current.jsonl"), os.path.join(outdir, "scheme_current.jsonl")):
        if os.path.exists(p):
            return p
    return None


def _is_last_leg(outdir):
    return any(os.path.exists(os.path.join(outdir, n)) for n in ("handback-B1.md", "scheme.jsonl"))


def _store(ctx):
    """The store as this check needs it: themes by room (ids and labels), codes by room, and the
    code rows for the exemplar resolution."""
    if "s02" in ctx:
        return ctx["s02"]
    trows = jsonl(os.path.join(ctx["package"], "store", "themes.jsonl")) or []
    crows = jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or []
    theme_ids = {(r.get("sub"), r.get("theme_id")) for r in trows}
    theme_labels = {(r.get("sub"), " ".join(str(r.get("second_order") or "").split())) for r in trows}
    codes = {(r.get("sub"), r.get("code_id")): r for r in crows}
    ctx["s02"] = {"theme_ids": theme_ids, "theme_labels": theme_labels, "codes": codes,
                  "n_themes": len(trows), "has_store": bool(trows or crows)}
    return ctx["s02"]


def _resolve_quote(q, st, sub=None, code_id=None):
    """'text' when the words are a participant's words; 'label' or 'note' when they are found only
    there; None when nothing holds them."""
    w = " ".join(str(q).split())
    if not w:
        return None
    rows = list(st["codes"].values())
    if sub and code_id and (sub, code_id) in st["codes"]:
        r = st["codes"][(sub, code_id)]
        if w in " ".join(str(r.get("text") or "").split()):
            return "text"
    if any(w in " ".join(str(r.get("text") or "").split()) for r in rows):
        return "elsewhere" if sub and code_id and (sub, code_id) in st["codes"] else "text"
    for r in rows:
        if w in " ".join(str(r.get("note") or "").split()):
            return "note"
        if (w in " ".join(str(r.get("first_order") or "").split())
                or w in " ".join(str(r.get("second_order") or "").split())):
            return "label"
    return None


def _check_name(kind, ident, name, where):
    words = [x for x in re.split(r"[\s/,]+", str(name or "").strip()) if x]
    if not words:
        return
    low = [w.lower().strip(".:;()") for w in words]
    hit = [w for w in low if w in PROBLEMS]
    if hit:
        err("%s %s is named %r: a name is never one of the four problems (%s); this tier stays descriptive, "
            "near the material" % (kind, ident, name, ", ".join(hit)), shape="%s:problem-name" % kind, where=where)
    if kind == "theme" and not 2 <= len(words) <= 5:
        warn("theme %s: the name %r is %d words; section 3 asks for 2 to 5, gerund-led where the material "
             "allows" % (ident, name, len(words)), shape="theme:name-length", where=where)


def _check_current(outdir, ctx, analysed):
    """scheme/scheme_current.jsonl: the grouping on disk. Returns {T3 id: set of rooms}."""
    p = _current_path(outdir)
    if p is None:
        err("scheme/scheme_current.jsonl was not written; it is the grouping on disk, rewritten at every "
            "room boundary, and a theme the file does not hold does not exist (section 2)")
        return None
    if os.path.dirname(p) == outdir:
        warn("scheme_current.jsonl is at out/ root; the stage file and the standing instructions place it "
             "under out/scheme/")
    rows = jsonl(p) or []
    if not rows:
        err("scheme/scheme_current.jsonl is empty; the grouping in your head and on disk are one, and the "
            "file is rewritten at every room boundary")
        return {}
    st = _store(ctx)
    rooms_of, seen, placed = {}, set(), collections.defaultdict(set)
    for r in rows:
        tid = r.get("theme")
        where = str(tid)
        if not T3.match(str(tid or "")):
            err("scheme_current.jsonl: theme id %r is not of the form T3-007" % tid, shape="current:id", where=where)
            continue
        if tid in seen:
            err("scheme_current.jsonl holds %s twice; one line per theme as it stands" % tid, shape="current:dup", where=where)
        seen.add(tid)
        if not (r.get("label") or "").strip():
            err("scheme_current.jsonl %s has no label" % tid, shape="current:nolabel", where=where)
        members = r.get("members")
        if not isinstance(members, list):
            err("scheme_current.jsonl %s: members is not a list of {sub, second_order, codes}" % tid,
                shape="current:members", where=where)
            continue
        rooms_of[tid] = set()
        for m in members:
            sub, so = m.get("sub"), m.get("second_order")
            mw = "%s %s:%s" % (tid, sub, so)
            if not sub or so is None:
                err("scheme_current.jsonl %s: a member lacks sub or second_order" % tid, shape="current:member-keys", where=mw)
                continue
            rooms_of[tid].add(sub)
            placed[(sub, str(so))].add(tid)
            if analysed is not None and sub not in analysed:
                err("scheme_current.jsonl %s places a theme of r/%s, which is not in the analysed set" % (tid, sub),
                    shape="current:notanalysed", where=mw)
            if st["has_store"] and (sub, so) not in st["theme_ids"] \
                    and (sub, " ".join(str(so).split())) not in st["theme_labels"]:
                err("scheme_current.jsonl %s: member %s/%s is not a second-order theme of the store (themes.jsonl "
                    "theme_id or its second_order label)" % (tid, sub, so), shape="current:member-unresolved", where=mw)
            for c in m.get("codes") or []:
                if st["has_store"] and (sub, c) not in st["codes"]:
                    err("scheme_current.jsonl %s: member %s/%s cites concept %s, which the store does not hold for "
                        "r/%s" % (tid, sub, so, c, sub), shape="current:code-unresolved", where="%s %s" % (mw, c))
    multi = {k: v for k, v in placed.items() if len(v) > 1}
    for k, v in sorted(multi.items())[:200]:
        warn("scheme_current.jsonl: second-order theme %s/%s is under %d third-order themes (%s); rule 0 is single "
             "placement, a second one on the record with its why_not_one" % (k[0], k[1], len(v), ", ".join(sorted(v))),
             shape="current:multiplaced", where="%s/%s" % k)
    n_members = sum(len(v) for v in placed.values())
    if placed:
        big = [(t, sum(1 for k, v in placed.items() if t in v)) for t in rooms_of]
        for t, n in big:
            if n > 0.1 * len(placed) and len(placed) >= 20:
                warn("scheme_current.jsonl %s holds %d of %d second-order themes, more than one in ten; section 2 "
                     "says such a theme is read again for the kinds inside it, and either split or has its "
                     "variation written out" % (t, n, len(placed)), shape="current:bag", where=t)
    print("  scheme_current: %d themes over %d placed second-order themes (%d members)"
          % (len(rooms_of), len(placed), n_members))
    return rooms_of


def _check_discovery(outdir, ctx, analysed, current_ids, diary):
    rows = jsonl(os.path.join(outdir, "theme_discovery.jsonl"))
    if rows is None:
        return None
    st = _store(ctx)
    ids, seen = set(), collections.Counter()
    logged = {i for d in diary for i in (d.get("ids") or [])}
    for r in rows:
        tid = r.get("theme")
        where = str(tid)
        lacking = [k for k in DISCOVERY_KEYS if k not in r]
        if lacking:
            err("theme_discovery.jsonl %s lacks %s; the line is written by `mem.py mint` and never by hand "
                "(section 6)" % (tid, lacking), shape="discovery:keys", where=where)
        if not T3.match(str(tid or "")):
            err("theme_discovery.jsonl: theme id %r is not of the form T3-007" % tid, shape="discovery:id", where=where)
            continue
        seen[tid] += 1
        ids.add(tid)
        trig = str(r.get("trigger") or "")
        if ":" not in trig:
            err("theme_discovery.jsonl %s: trigger %r is not <sub>:<theme_id>" % (tid, trig),
                shape="discovery:trigger", where=where)
        else:
            sub, th = trig.split(":", 1)
            if analysed is not None and sub not in analysed:
                err("theme_discovery.jsonl %s: trigger names r/%s, not in the analysed set" % (tid, sub),
                    shape="discovery:trigger-room", where=where)
            elif st["has_store"] and (sub, th) not in st["theme_ids"]:
                err("theme_discovery.jsonl %s: trigger %s is not a second-order theme of the store" % (tid, trig),
                    shape="discovery:trigger-unresolved", where=where)
        if tid not in logged:
            err("theme_discovery.jsonl %s has no diary line naming it; a theme is minted through `mem.py mint`, "
                "which logs, and a discovery line written by hand is not a mint" % tid,
                shape="discovery:unlogged", where=where)
    for tid, n in seen.items():
        if n > 1:
            err("theme_discovery.jsonl holds %s %d times; a line is written once, the first time a theme exists, "
                "and an id is never reused" % (tid, n), shape="discovery:dup", where=tid)
    if current_ids is not None:
        for tid in sorted(set(current_ids) - ids):
            err("scheme_current.jsonl holds %s but theme_discovery.jsonl has no line for it; every theme is minted "
                "through `mem.py mint` the first time it exists" % tid, shape="discovery:unminted", where=tid)
    print("  theme_discovery: %d themes minted" % len(ids))
    return ids


def _check_walk(outdir, ctx, analysed, last):
    """The walk under the stopping rule (tools/saturation.py): no room read out of the rule's turn; at the last
    leg the walk has reached the list's end or stopped by the PI's decision after marker 3, with its report."""
    import saturation
    for i, r in enumerate(jsonl(os.path.join(outdir, "unplaced-B1.jsonl")) or [], 1):
        if not str(r.get("why") or "").strip() or not r.get("sub") or not r.get("second_order"):
            err("unplaced-B1.jsonl line %d needs sub, second_order and why" % i, shape="walk:unplaced", where=str(i))
    # the kinds ledger: every placement on disk was met through mem.py, so the rule's past is the one read
    cur = _current_path(outdir)
    members = set()
    for r in (jsonl(cur) or []) if cur else []:
        for m in r.get("members") or []:
            if isinstance(m, dict) and m.get("sub"):
                members.add((str(m["sub"]).lower(), r.get("theme")))
    led_p = os.path.join(outdir, "kinds-B1.jsonl")
    if members and not os.path.exists(led_p):
        err("kinds-B1.jsonl is absent while scheme_current.jsonl places %d second-order theme(s): the stopping rule "
            "counts kinds as met, and only mem.py mint and place record them; a grouping written by hand has no "
            "past" % len(members), shape="kinds:ledger")
    elif members:
        logged = {(str(r.get("sub") or "").lower(), r.get("kind")) for r in jsonl(led_p) or []}
        missing = sorted(m for m in members if m not in logged)
        if missing:
            err("%d placement(s) in scheme_current.jsonl are not in kinds-B1.jsonl (%s): placed without mem.py mint "
                "or place, so the stopping rule never met them" % (len(missing), ", ".join("%s:%s" % m for m in missing[:4])),
                shape="kinds:unlogged", where="%s:%s" % missing[0])
    root = os.path.dirname(ctx["package"])
    R = saturation.replay(root, outdir, "B1")
    print("  " + saturation.status_lines(R)[0])
    if R["out_of_turn"]:
        err("%d room(s) are placed whole but were not yet the rule's turn (%s): a room was skipped, or read out of "
            "order; `mem.py next --stage B1` names the room the rule asks for" % (len(R["out_of_turn"]),
            ", ".join(R["out_of_turn"][:6])), shape="walk:gap", where=R["out_of_turn"][0])
    if R["state"] in ("report", "check-in") and not os.path.exists(os.path.join(outdir, "stopping-B1.md")):
        err("the walk waits for the PI (%s) but stopping-B1.md is not written: python3 tools/saturation.py report "
            "--stage B1, then done.sh B1 --pause" % R["state"], shape="walk:report")
    if last and not os.path.exists(os.path.join(outdir, "stopping-B1.md")):
        err("stopping-B1.md is not written at the walk's end; the report says where the rule stood, even when the "
            "order ran out before marker 3: python3 tools/saturation.py report --stage B1", shape="walk:report")
    rep = text(outdir, "stopping-B1.md")
    if rep:
        m = re.search(r"\| rooms read \| (\d+) of", rep)
        if m and int(m.group(1)) != R["now"]["rooms_read"]:
            err("stopping-B1.md reports %s rooms read, the record now %d: the report is stale; run python3 "
                "tools/saturation.py report --stage B1 again" % (m.group(1), R["now"]["rooms_read"]),
                shape="walk:stale-report")
    if last and R["state"] not in ("end", "stopped"):
        err("the walk has neither reached the list's end nor stopped by the PI's decision (state: %s; next: %s); the "
            "scheme stands only when the walk has ended" % (R["state"], R["next"]), shape="walk:unfinished")


def _check_prior(outdir):
    p = text(outdir, "prior.md")
    if not p.strip():
        err("prior.md is empty; it is written first, from PRIOR-template.md, sections 1 to 6 filled and dated, "
            "before the first second-order theme is opened (section 1)")
        return
    # sections 1 to 6 are written at B1; 7 (distance weights) and 8 (the cannot-tell thresholds) at D1
    for n in range(1, 7):
        if not re.search(r"^##\s*%d\b" % n, p, re.M):
            err("prior.md has no section %d; sections 1 to 6 of PRIOR-template.md are filled at B1" % n,
                shape="prior:section", where=str(n))
    m7 = re.search(r"^##\s*7\b", p, re.M)
    head = p[:m7.start()] if m7 else p
    for ph in ("(number)", "(share)", "(how you will choose"):
        if ph in head:
            err("prior.md sections 1 to 6 still carry the template placeholder %r; fill them before the first "
                "theme is opened" % ph, shape="prior:placeholder", where=ph)
    if not re.search(r"^\s*exemplar rule:\s*\S", head, re.M | re.I):
        err("prior.md has no `exemplar rule:` line; the rule for choosing among quotes that all pass a gate is "
            "written before the first theme is opened (section 3)", shape="prior:exemplar-rule")


def _check_episodes(outdir, analysed, ids):
    """episodes-B1.jsonl: one episode seen twice. Returns {T3 id: [set of rooms], ...}, the rooms each
    episode joins for that theme (an episode with no themes joins its rooms for every theme)."""
    p = os.path.join(outdir, "episodes-B1.jsonl")
    rows = jsonl(p)
    if rows is None:
        err("episodes-B1.jsonl is absent; section 2 records every episode two rooms tell there, and the file is "
            "empty when there was none")
        return {}
    joins, seen = collections.defaultdict(list), set()
    for i, r in enumerate(rows, 1):
        w = "episodes-B1.jsonl line %d" % i
        eid = r.get("episode")
        if not eid or eid in seen:
            err("%s: episode id %r is missing or repeated" % (w, eid), shape="episodes:id", where=w)
        seen.add(eid)
        rooms = [x for x in (r.get("rooms") or []) if x]
        if len(set(rooms)) < 2:
            err("%s: an episode seen twice names two rooms or more" % w, shape="episodes:rooms", where=w)
        for x in rooms:
            if analysed is not None and x not in analysed:
                err("%s: r/%s is not in the analysed set" % (w, x), shape="episodes:room", where=w)
        if r.get("same") not in ("thread", "artwork"):
            err("%s: same %r is not thread or artwork; the test is the record, not the likeness of the accounts"
                % (w, r.get("same")), shape="episodes:same", where=w)
        for k in ("evidence", "why"):
            if not str(r.get(k) or "").strip():
                err("%s: no %s" % (w, k), shape="episodes:" + k, where=w)
        ths = r.get("themes") or []
        for t in ths:
            if ids is not None and t not in ids:
                err("%s: theme %r is not a theme of scheme.jsonl" % (w, t), shape="episodes:theme", where=w)
        for t in (ths or ["*"]):
            joins[t].append(set(rooms))
    print("  episodes seen twice: %d" % len(rows))
    return joins


def _floor_holds(rooms, joined):
    """Two rooms, rooms that tell one episode counted as one (episodes-B1.jsonl)."""
    units = [{s} for s in rooms]
    for g in joined:
        hit = [u for u in units if u & g]
        if len(hit) > 1:
            merged = set().union(*hit)
            units = [u for u in units if u not in hit] + [merged]
    return len(units) >= 2


FLOOR_AXES = ("size", "side", "form")


def _check_floor_pair(r, tid, rooms, joined, ctx, where):
    """A main theme names the two rooms its floor rests on and how they are unlike (section 2): `floor`:
    {"rooms": [a, b], "unlike": "size" | "side" | "form", "why": "..."}. Size is checked against the store
    (items in the window, one at least twice the other); side and form are read from the why."""
    f = r.get("floor")
    if not isinstance(f, dict):
        err("scheme.jsonl %s is tier main and names no floor: {rooms: [two rooms], unlike: size|side|form, why}; "
            "the floor is two rooms unlike each other (section 2)" % tid, shape="scheme:floor-pair", where=where)
        return
    _c = lambda x: vlib.canon(x).lower()   # case-blind, as the frame is (audit 2026-09-29b, F19)
    pr = [_c(x) for x in (f.get("rooms") or [])]
    if len(pr) != 2 or pr[0] == pr[1]:
        err("scheme.jsonl %s: floor.rooms is not two different rooms" % tid, shape="scheme:floor-pair", where=where)
        return
    low = {_c(x) for x in rooms}
    for x in pr:
        if x not in low:
            err("scheme.jsonl %s: floor room r/%s holds no member of the theme" % (tid, x), shape="scheme:floor-pair", where=where)
    if any(set(pr) <= {_c(y) for y in g} for g in joined):
        err("scheme.jsonl %s: the floor's two rooms tell one episode (episodes-B1.jsonl), so they are one room here"
            % tid, shape="scheme:floor-pair", where=where)
    if f.get("unlike") not in FLOOR_AXES:
        err("scheme.jsonl %s: floor.unlike is %r, not size, side or form" % (tid, f.get("unlike")),
            shape="scheme:floor-axis", where=where)
    elif not str(f.get("why") or "").strip():
        err("scheme.jsonl %s: floor names no why" % tid, shape="scheme:floor-axis", where=where)
    elif f.get("unlike") == "size":
        size = {_c(x.get("sub")): x.get("items_in_window") for x in (vlib.rooms(ctx) or [])}
        a, b = size.get(pr[0]), size.get(pr[1])
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and min(a, b) > 0 and max(a, b) < 2 * min(a, b):
            err("scheme.jsonl %s: floor unlike in size, but r/%s and r/%s hold %d and %d items in the window, less than "
                "twice apart" % (tid, pr[0], pr[1], a, b), shape="scheme:floor-axis", where=where)


def _check_scheme(outdir, ctx, analysed, rooms_of, joins=None):
    rows = jsonl(os.path.join(outdir, "scheme.jsonl")) or []
    fams = jsonl(os.path.join(outdir, "families.jsonl")) or []
    fam_ids = {f.get("family") for f in fams}
    st = _store(ctx)
    ids, seen = set(), collections.Counter()
    for r in rows:
        tid = r.get("id")
        where = str(tid)
        if not T3.match(str(tid or "")):
            err("scheme.jsonl id %r is not of the form T3-007" % tid, shape="scheme:id", where=where)
            continue
        seen[tid] += 1
        ids.add(tid)
        lacking = [k for k in SCHEME_KEYS if k not in r]
        if lacking:
            err("scheme.jsonl %s lacks the field(s) %s; section 4 gives every field, gate_parts null where the "
                "gate names no two-part move" % (tid, lacking), shape="scheme:keys", where=where)
        for k in ("name", "gloss", "must_show", "must_not_show", "decide_when_both", "varies", "is_not"):
            if k in r and not str(r.get(k) or "").strip():
                err("scheme.jsonl %s: %s is empty; every field is a test the stranger runs" % (tid, k),
                    shape="scheme:empty-field", where="%s %s" % (tid, k))
        _check_name("theme", tid, r.get("name"), where)
        if r.get("tier") not in ("main", "rare"):
            err("scheme.jsonl %s: tier is %r, not main|rare (the rare tier is a field, not a file)" % (tid, r.get("tier")),
                shape="scheme:tier", where=where)
        if r.get("family") not in fam_ids:
            err("scheme.jsonl %s names family %r, which families.jsonl does not define" % (tid, r.get("family")),
                shape="scheme:family-unresolved", where=where)
        for d in r.get("discriminators") or []:
            vs = d.get("vs") if isinstance(d, dict) else None
            if not (isinstance(d, dict) and str(d.get("question") or "").strip()):
                err("scheme.jsonl %s: a discriminator carries no question" % tid, shape="scheme:discriminator", where=where)
            if vs is not None and vs not in {x.get("id") for x in rows}:
                err("scheme.jsonl %s: discriminator vs %r is not a theme of the scheme" % (tid, vs),
                    shape="scheme:discriminator-unresolved", where="%s %s" % (tid, vs))
        ex = r.get("exemplars") or []
        if len(ex) < 3:
            warn("scheme.jsonl %s carries %d exemplar(s); section 3 asks for three, each through `cite.py --room "
                 "<sub> --code <id>`" % (tid, len(ex)), shape="scheme:exemplars-few", where=where)
        for e in ex:
            sub, cid, q = e.get("sub"), e.get("code_id"), e.get("quote")
            ew = "%s %s/%s" % (tid, sub, cid)
            if st["has_store"] and (sub, cid) not in st["codes"]:
                err("scheme.jsonl %s: exemplar cites %s/%s, which the store does not hold" % (tid, sub, cid),
                    shape="scheme:exemplar-code", where=ew)
            if analysed is not None and sub not in analysed:
                err("scheme.jsonl %s: exemplar from r/%s, not in the analysed set" % (tid, sub),
                    shape="scheme:exemplar-room", where=ew)
            if not st["has_store"]:
                continue
            how = _resolve_quote(q, st, sub, cid)
            for rv in e.get("rivals") or []:
                if st["has_store"] and (sub, str(rv).split(":")[-1]) not in st["codes"]:
                    err("scheme.jsonl %s: exemplar rival %s is not a concept of r/%s in the store" % (tid, rv, sub),
                        shape="scheme:exemplar-rival", where=ew)
            if how == "text":
                continue
            if how == "elsewhere":
                err("scheme.jsonl %s: exemplar %r is a participant's words, but not those of %s/%s, the concept it names"
                    % (tid, str(q)[:60], sub, cid), shape="scheme:exemplar-elsewhere", where=ew)
                continue
            if how in ("label", "note"):
                err("scheme.jsonl %s: exemplar %r resolves to a %s, not a participant's words; rule 3 rejects it, "
                    "quote through `cite.py --room %s --code %s`" % (tid, str(q)[:60], "coder's note" if how == "note" else "label", sub, cid),
                    shape="scheme:exemplar-label", where=ew)
            else:
                err("scheme.jsonl %s: exemplar %r does not resolve to a participant's words in the store (`cite.py "
                    "--resolve`)" % (tid, str(q)[:60]), shape="scheme:exemplar-unresolved", where=ew)
        # the floor (section 2): a main theme rests on two rooms unlike each other
        if rooms_of is not None:
            if tid not in rooms_of:
                err("scheme.jsonl ships %s, which scheme_current.jsonl does not hold; a theme the grouping on disk "
                    "does not hold does not exist" % tid, shape="scheme:not-in-current", where=where)
            else:
                n = len(rooms_of[tid])
                if r.get("tier") == "main" and n < 2:
                    err("scheme.jsonl %s is tier main on %d room(s); the floor is two rooms unlike each other, and a "
                        "kind seen in one room goes to the rare tier" % (tid, n), shape="scheme:floor", where=where)
                elif r.get("tier") == "main":
                    joined = (joins or {}).get(tid, []) + (joins or {}).get("*", [])
                    _check_floor_pair(r, tid, rooms_of[tid], joined, ctx, where)
                    if not _floor_holds(rooms_of[tid], joined):
                        err("scheme.jsonl %s is tier main, but its rooms are one once rooms that tell one episode count "
                            "as one (episodes-B1.jsonl); the floor is two rooms unlike each other, and short of it the "
                            "theme is rare" % tid, shape="scheme:floor-episode", where=where)
                if r.get("tier") == "rare" and n >= 2:
                    warn("scheme.jsonl %s is tier rare yet holds members from %d rooms; say why it is not main"
                         % (tid, n), shape="scheme:rare-wide", where=where)
    for tid, n in seen.items():
        if n > 1:
            err("scheme.jsonl holds %s %d times" % (tid, n), shape="scheme:dup", where=tid)
    if rooms_of is not None:
        for tid in sorted(set(rooms_of) - ids):
            err("scheme_current.jsonl holds %s but scheme.jsonl does not ship it; at the close every theme of the "
                "grouping ships, rare ones with \"tier\": \"rare\"" % tid, shape="scheme:missing-from-shipped", where=tid)
    # families.jsonl (section 4): an index and nothing else
    for f in fams:
        fid = f.get("family")
        if not FAMILY.match(str(fid or "")):
            err("families.jsonl family %r is not of the form G03" % fid, shape="families:id", where=str(fid))
        if not str(f.get("name") or "").strip():
            err("families.jsonl %s has no name" % fid, shape="families:noname", where=str(fid))
        _check_name("family", fid, f.get("name"), str(fid))
        for t in f.get("themes") or []:
            if t not in ids:
                err("families.jsonl %s lists %r, which scheme.jsonl does not define" % (fid, t),
                    shape="families:theme-unresolved", where="%s %s" % (fid, t))
    grouped = collections.Counter(t for f in fams for t in (f.get("themes") or []))
    orphan = sorted(ids - set(grouped))
    if orphan:
        err("themes in no family: %s; the fleet opens one family's tests at a time and a theme outside every "
            "family is never opened" % orphan[:8])
    dup = sorted(t for t, n in grouped.items() if n > 1)
    if dup:
        err("themes in more than one family: %s; every theme belongs to one family" % dup[:8])
    for f in fams:
        fid = f.get("family")
        for t in f.get("themes") or []:
            own = next((r.get("family") for r in rows if r.get("id") == t), None)
            if own is not None and own != fid:
                err("families.jsonl %s lists %s, whose scheme.jsonl line says family %s" % (fid, t, own),
                    shape="families:disagree", where=t)
    if not ids:
        err("scheme.jsonl defines no theme; the scheme must be addressable by T3 id or nothing downstream can "
            "place on it")
    else:
        rare = sum(1 for r in rows if r.get("tier") == "rare")
        print("  scheme ships %d themes in %d families (%d rare)" % (len(ids), len(fam_ids), rare))
    return ids


def _check_prose(outdir, ids):
    for name in ("scheme.md", "confusions.md"):
        t = text(outdir, name)
        if not t.strip():
            err("%s is empty" % name)
            continue
        cited = set(T3_ANY.findall(t))
        for tid in sorted(cited - ids):
            err("%s names %s, which scheme.jsonl does not define" % (name, tid), shape="%s:unresolved" % name, where=tid)
        if name == "scheme.md":
            for tid in sorted(ids - cited):
                err("scheme.md does not carry %s; the prose file stays authoritative for a human and holds every "
                    "theme by id" % tid, shape="scheme.md:missing", where=tid)


def _check_tier_history(outdir, ids):
    rows = jsonl(os.path.join(outdir, "tier_history.jsonl"))
    if rows is None:
        return
    for r in rows:
        where = "%s %s" % (r.get("id"), r.get("event"))
        for k in ("t", "stage", "tier", "id", "move", "event", "why"):
            if k not in r:
                err("tier_history.jsonl line for %r lacks `%s`; section 6 gives the line's form" % (r.get("id"), k),
                    shape="history:keys", where=where)
        if r.get("event") not in EVENTS:
            err("tier_history.jsonl %r: event %r is not one of %s" % (r.get("id"), r.get("event"), ", ".join(EVENTS)),
                shape="history:event", where=where)
        if not str(r.get("move") or "").strip():
            err("tier_history.jsonl %r: move is empty; it is one of Grodal, Anteby and Holm's eight" % r.get("id"),
                shape="history:move", where=where)
        if r.get("event") in CONSEQUENTIAL and not str(r.get("prompted_by") or "").strip():
            err("tier_history.jsonl %r: a %s carries no `prompted_by`; a consequential move is recorded as what "
                "prompted it, the move, what changed and why (section 6)" % (r.get("id"), r.get("event")),
                shape="history:prompted_by", where=where)
        if r.get("tier") == "third" and not T3.match(str(r.get("id") or "")):
            err("tier_history.jsonl: id %r on tier third is not of the form T3-007" % r.get("id"),
                shape="history:id", where=where)
    print("  tier_history: %d lines" % len(rows))


def _check_findings(outdir):
    rows = jsonl(os.path.join(outdir, "findings.jsonl"))
    if rows is None:
        return
    mine = [r for r in rows if str(r.get("stage")) == "B1"]
    if not mine:
        err("findings.jsonl carries no stage-B1 line; the stage opens it with the scheme's claim in rule 14's form")
    for r in rows:
        where = str(r.get("id"))
        for k in ("id", "stage", "statement", "warrant", "status"):
            if not str(r.get(k) or "").strip():
                err("findings.jsonl %r lacks `%s` (rule 14)" % (r.get("id"), k), shape="findings:keys", where=where)
        if r.get("warrant") not in WARRANTS:
            err("findings.jsonl %r: warrant %r is not entailed|read|inferred" % (r.get("id"), r.get("warrant")),
                shape="findings:warrant", where=where)
        if r.get("status") not in STATUS:
            err("findings.jsonl %r: status %r is not standing|bounded|withdrawn" % (r.get("id"), r.get("status")),
                shape="findings:status", where=where)


def check(root, outdir, ctx):
    step = vlib.current_step(root)
    if step == "B1a":            # B1a writes prior.md and notes; the first mint, in B1b, writes the rest
        need(outdir, "prior.md", "notes-B1.md")
        _check_prior(outdir)
        print("  B1a: prior.md and notes-B1.md; the grouping starts with the first mint in B1b")
        return
    need(outdir, "prior.md", "theme_discovery.jsonl", "notes-B1.md")
    last = _is_last_leg(outdir)
    sets = vlib.analysed_set("B1", "every member, trigger and exemplar room against the analysed set", outdir, ctx)
    analysed = sets[0] if sets else None
    _check_prior(outdir)
    if not text(outdir, "notes-B1.md").strip():
        err("notes-B1.md is empty; the reading order and why go there before the first theme is opened")
    diary = vlib.diary_lines(outdir, "B1")
    rooms_of = _check_current(outdir, ctx, analysed)
    current_ids = set(rooms_of) if rooms_of is not None else None
    _check_discovery(outdir, ctx, analysed, current_ids, diary)
    _check_walk(outdir, ctx, analysed, last)
    if not last:
        print("  the pass has not ended (no scheme.jsonl or handback-B1.md); the shipped files are checked at the "
              "last leg")
        return
    need(outdir, "scheme.md", "scheme.jsonl", "families.jsonl", "confusions.md", "tier_history.jsonl",
         "findings.jsonl", "handback-B1.md", "saturation-B1.md")
    sat = text(outdir, "saturation-B1.md").lower()
    if not sat.strip():
        err("saturation-B1.md is empty; it holds the saturation test and the second pass (section 2)")
    elif not ("two stretches" in sat or "added no new" in sat or "still climbing" in sat):
        err("saturation-B1.md does not say how the second pass stopped: thirty rooms in a row that added no new "
            "third-order theme, or the count still climbing (section 2, B1d)")
    ids0 = {r.get("id") for r in (jsonl(os.path.join(outdir, "scheme.jsonl")) or [])}
    joins = _check_episodes(outdir, analysed, ids0)
    ids = _check_scheme(outdir, ctx, analysed, rooms_of, joins)
    _check_prose(outdir, ids)
    _check_tier_history(outdir, ids)
    _check_findings(outdir)


# ---- the self-test ------------------------------------------------------------------------------

def _w(outdir, name, content=""):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


def _theme(tid, name, fam, tier, exemplars, floor=None):
    r = {"id": tid, "name": name, "gloss": "a gloss", "family": fam, "tier": tier,
         "must_show": "a call", "must_not_show": "a recount", "decide_when_both": "the later one",
         "discriminators": [], "varies": "from a plea to an order", "is_not": "a joke about hands",
         "gate_parts": None, "exemplars": exemplars}
    if tier == "main":
        r["floor"] = floor or {"rooms": ["denmark", "asoiaf"], "unlike": "form",
                               "why": "a national flag against a fandom's sigil"}
    return r


def _base(outdir, root):
    _wj(outdir, "dropped.jsonl", [{"sub": "sweden", "why": "wrote nothing about the event"}])
    _w(outdir, "prior.md", "".join("## %d. x\nfilled 2026-09-24\n" % n for n in range(1, 7))
       + "exemplar rule: the line that meets the gate most directly\n")
    _w(outdir, "episodes-B1.jsonl", "")
    _w(outdir, "notes-B1.md", "# notes\norder: stage A1's.\n")
    _wj(outdir, "scheme/scheme_current.jsonl", [
        {"theme": "T3-001", "label": "calling for hands", "members": [
            {"sub": "denmark", "second_order": "t07", "codes": ["c0117"]},
            {"sub": "asoiaf", "second_order": "t02", "codes": ["c0011"]}]}])
    _wj(outdir, "kinds-B1.jsonl", [
        {"t": "2026-09-24T10:00:00Z", "leg": "B1b-01", "at": "denmark", "sub": "denmark", "kind": "T3-001", "event": "minted"},
        {"t": "2026-09-24T10:05:00Z", "leg": "B1b-01", "at": "asoiaf", "sub": "asoiaf", "kind": "T3-001", "event": "placed"}])
    _wj(outdir, "theme_discovery.jsonl", [
        {"theme": "T3-001", "label": "calling for hands", "t": "2026-09-24T10:00:00Z", "stage": "B1", "leg": "B1-block-1",
         "sub": "denmark", "trigger": "denmark:t07", "rooms_read": 1, "themes_read": 1, "codes_read": 2, "tokens_read": 100}])
    _wj(outdir, "diary/B1-1.jsonl", [
        {"t": "2026-09-24T10:00:00Z", "stage": "B1", "leg": "B1-block-1", "kind": "split", "ids": ["T3-001"],
         "text": "minted T3-001 calling for hands (trigger denmark:t07)"}])
    ex = [{"sub": "denmark", "quote": "we need more people at the border", "code_id": "c0117"},
          {"sub": "denmark", "quote": "posting on r/place for help", "code_id": "c0118"},
          {"sub": "asoiaf", "quote": "hold the line", "code_id": "c0011"}]
    _wj(outdir, "scheme.jsonl", [_theme("T3-001", "calling for hands", "G01", "main", ex)])
    _wj(outdir, "families.jsonl", [{"family": "G01", "name": "getting hands", "themes": ["T3-001"]}])
    _w(outdir, "scheme.md", "# scheme\n## G01 getting hands\n### T3-001 calling for hands\n")
    _w(outdir, "confusions.md", "# confusions\nT3-001 against nothing yet.\n")
    _w(outdir, "tier_history.jsonl", "")
    _wj(outdir, "findings.jsonl", [{"id": "F-001", "stage": "B1", "leg": "B1-block-1", "statement": "rooms called for hands",
                                    "tier": "third", "warrant": "read", "evidence": ["T3-001"], "bound": "",
                                    "refuted_by": "a room that never called", "status": "standing"}])
    _w(outdir, "handback-B1.md", "# handback\n")
    _w(outdir, "saturation-B1.md", "# saturation\n\nThe second pass stopped after two stretches in a row added no new theme.\n")
    _w(outdir, "stopping-B1.md", "# When to stop, stage B1\n")


def _plant_split_unprompted(outdir, root):
    _base(outdir, root)
    _w(outdir, "tier_history.jsonl", json.dumps(
        {"t": "x", "stage": "B1", "leg": "B1-block-1", "tier": "third", "id": "T3-001", "move": "splitting",
         "event": "split", "was": {"label": "calling for hands", "members": []}, "now": [], "why": "two kinds"}) + "\n")


def _plant_exemplar_label(outdir, root):
    _base(outdir, root)
    ex = [{"sub": "denmark", "quote": "calling for hands", "code_id": "c0117"}]
    _wj(outdir, "scheme.jsonl", [_theme("T3-001", "calling for hands", "G01", "main", ex)])


def _plant_exemplar_unresolved(outdir, root):
    _base(outdir, root)
    ex = [{"sub": "denmark", "quote": "words nobody in the store said", "code_id": "c0117"}]
    _wj(outdir, "scheme.jsonl", [_theme("T3-001", "calling for hands", "G01", "main", ex)])


def _plant_family(outdir, root):
    _base(outdir, root)
    _wj(outdir, "families.jsonl", [{"family": "G02", "name": "getting hands", "themes": ["T3-001"]}])


def _plant_unminted(outdir, root):
    _base(outdir, root)
    _w(outdir, "theme_discovery.jsonl", "")


def _plant_floor(outdir, root):
    _base(outdir, root)
    _wj(outdir, "scheme/scheme_current.jsonl", [
        {"theme": "T3-001", "label": "calling for hands", "members": [
            {"sub": "denmark", "second_order": "t07", "codes": ["c0117"]}]}])


def _plant_member(outdir, root):
    _base(outdir, root)
    _wj(outdir, "scheme/scheme_current.jsonl", [
        {"theme": "T3-001", "label": "calling for hands", "members": [
            {"sub": "denmark", "second_order": "t99", "codes": ["c0117"]},
            {"sub": "asoiaf", "second_order": "t02", "codes": ["c0011"]}]}])


def _plant_problem_name(outdir, root):
    _base(outdir, root)
    ex = [{"sub": "asoiaf", "quote": "hold the line", "code_id": "c0011"}]
    _wj(outdir, "scheme.jsonl", [_theme("T3-001", "the allocation problem", "G01", "main", ex)])


def _plant_findings(outdir, root):
    _base(outdir, root)
    _wj(outdir, "findings.jsonl", [{"id": "F-001", "stage": "B1", "statement": "x", "warrant": "guessed", "status": "standing"}])


def _plant_saturation_missing(outdir, root):
    _base(outdir, root)
    os.remove(os.path.join(outdir, "saturation-B1.md"))


def _plant_one_episode(outdir, root):
    _base(outdir, root)
    _wj(outdir, "episodes-B1.jsonl", [{"episode": "E001", "rooms": ["denmark", "asoiaf"], "same": "thread",
                                       "evidence": "t3_abc", "themes": ["T3-001"], "why": "one call told twice"}])


def _plant_episode_bad(outdir, root):
    _base(outdir, root)
    _wj(outdir, "episodes-B1.jsonl", [{"episode": "E001", "rooms": ["denmark", "asoiaf"], "same": "alike",
                                       "evidence": "t3_abc", "why": "x"}])


def _plant_walk_gap(outdir, root):
    import saturation
    _base(outdir, root)
    os.remove(os.path.join(outdir, "scheme.jsonl")); os.remove(os.path.join(outdir, "handback-B1.md"))
    second = saturation.shuffled(["asoiaf", "denmark"], saturation.seed(root), "B1")[1]
    member = {"denmark": {"sub": "denmark", "second_order": "t07", "codes": ["c0117"]},
              "asoiaf": {"sub": "asoiaf", "second_order": "t02", "codes": ["c0011"]}}[second]
    _wj(outdir, "scheme/scheme_current.jsonl", [{"theme": "T3-001", "label": "calling for hands", "members": [member]}])


def _plant_walk_left(outdir, root):
    _base(outdir, root)
    _wj(outdir, "scheme/scheme_current.jsonl", [
        {"theme": "T3-001", "label": "calling for hands", "members": [
            {"sub": "denmark", "second_order": "t07", "codes": ["c0117"]}]}])


def _plant_kinds_unlogged(outdir, root):
    _base(outdir, root)
    _wj(outdir, "kinds-B1.jsonl", [
        {"t": "2026-09-24T10:00:00Z", "leg": "B1b-01", "at": "denmark", "sub": "denmark", "kind": "T3-001", "event": "minted"}])


def _plant_floor_axis(outdir, root):
    _base(outdir, root)
    ex = [{"sub": "denmark", "quote": "we need more people at the border", "code_id": "c0117"},
          {"sub": "asoiaf", "quote": "hold the line", "code_id": "c0011"}]
    _wj(outdir, "scheme.jsonl", [_theme("T3-001", "calling for hands", "G01", "main", ex,
                                        {"rooms": ["denmark", "asoiaf"], "unlike": "colour", "why": "red and grey"})])


def _plant_no_exemplar_rule(outdir, root):
    _base(outdir, root)
    _w(outdir, "prior.md", "".join("## %d. x\nfilled 2026-09-24\n" % n for n in range(1, 7)))


PLANTED = [
    ("an exemplar that is a label", _plant_exemplar_label, "resolves to a label"),
    ("an exemplar nobody said", _plant_exemplar_unresolved, "does not resolve to a participant's words"),
    ("a family the index lacks", _plant_family, "which families.jsonl does not define"),
    ("a theme never minted", _plant_unminted, "theme_discovery.jsonl has no line for it"),
    ("a main theme on one room", _plant_floor, "the floor is two rooms"),
    ("a member the store lacks", _plant_member, "is not a second-order theme of the store"),
    ("a theme named for a problem", _plant_problem_name, "never one of the four problems"),
    ("a finding with a bad warrant", _plant_findings, "is not entailed|read|inferred"),
    ("a split that says not what prompted it", _plant_split_unprompted, "carries no `prompted_by`"),
    ("no saturation record", _plant_saturation_missing, "saturation-B1.md"),
    ("a main theme on one episode seen twice", _plant_one_episode, "its rooms are one once rooms that tell one episode"),
    ("an episode judged by likeness", _plant_episode_bad, "is not thread or artwork"),
    ("no exemplar rule in prior.md", _plant_no_exemplar_rule, "no `exemplar rule:` line"),
    ("a room skipped in the seeded order", _plant_walk_gap, "a room was skipped, or read out of order"),
    ("a floor unlike in no named way", _plant_floor_axis, "not size, side or form"),
    ("a placement the kinds ledger never met", _plant_kinds_unlogged, "are not in kinds-B1.jsonl"),
    ("the walk unfinished at the end", _plant_walk_left, "has neither reached the list's end"),
]
