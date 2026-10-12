"""checks/stage_C1.py: the close-check of stage C1 (revision: scheme v2, the fourth-order themes), v38.

Written from stages/STAGE-C1-model-structuring.md (Outputs; sections 2, 3, 4, 6, 7, 8, 9; Close),
the contract's rules 0, 5, 10, 11, FLEET.md section 2, and the v37 check it descends from
(_v37-source/tools/validate.py, stage06). It checks the SHAPE of the stage's files: existence,
parse, ids that resolve against scheme_v2 and the store, counts that reconcile against the
analysed set and against assign_final.jsonl, every change to a tier logged. It cannot check
whether a recut is right.

What it holds to:
  scheme_v2.jsonl     mirrors scheme_final.jsonl field for field; T3 ids, unique; tier main|rare;
                      discriminators resolve; every id retired, created or moved to rare has its
                      stage-C1 line in tier_history.jsonl; scheme_v2.md carries every id (whole, not a diff).
  assignments_final   every second-order theme of the analysed set once, keys equal to
                      assign_final.jsonl's, nothing deleted; every placement a third-order id of
                      scheme_v2 and a (sub, theme_id) of the store; count.txt equals the line count;
                      every changed line in assign_revisions_only.jsonl and vice versa.
  fourth/fourth.jsonl T4 ids, unique; declared borrowed|adapted|coined; members third-order ids of
                      scheme_v2, no third-order id in two fourth-order themes (the stage file allows
                      none: a second-order theme lifts to two only through rule 0); prose; each cut
                      logged in tier_history with tier fourth and move merging|relating; the
                      unpicked third-order themes listed in fourth.md or notes-C1.md.
  form_pass-C1.md     FP- ids live there and in no JSONL, no count receipt and no gate; the sweep's
                      coverage is allowed there (2026-10-08).
  notes-C1.md         the revision rate; the empties at the top when above one in five; stage B4's
                      figures cited with the licence and never as reliability.

Fields the stage file does not give (existence and parse only): assign_revisions_only.jsonl
beyond its being a subset of assignments_final.jsonl; fourth/fourth.md's shape.

Not carried from v37: the fallback that parsed S.. ids out of the scheme's prose when no JSONL
was there (v38's vlib.load_scheme reads JSONL only, and the ids are T3-nnn); `second_order` as
the placement field (now third_order); `case_theme` (now theme_id); the F id prefix in the form
pass (now FP-, since F is stage D4's).
"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

EVENTS = ("created", "relabelled", "split", "merged", "retired", "members_changed", "rescoped", "moved_to_rare")
DECLARED = ("borrowed", "adapted", "coined")
FOURTH_MOVES = ("merging", "relating")
FP = re.compile(r"\bFP-\d{2,3}\b")


def _ids(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v else []
    return list(v) if isinstance(v, list) else None


def _placement(row):
    so = _ids(row.get("third_order"))
    return sorted(s for s in (so or []) if s and s != "unresolved")


def _reliability_word(outdir, name):
    t = text(outdir, name)
    for s in re.split(r"(?<=[.!?])\s+|\n+", t):
        if re.search(r"\breliability\b", s, re.I) and not re.search(r"\b(not|never|no)\b", s, re.I):
            err("%s calls a figure reliability: %r. Stage B4's figures are transmission after revision "
                "(FLEET.md section 2); never call any of them reliability (section 2)"
                % (name, " ".join(s.split())[:90]), shape="reliability:%s" % name, where=s[:60])


def _history_06(outdir):
    th = jsonl(os.path.join(outdir, "tier_history.jsonl"))
    if th is None:
        return None
    rows = [r for r in th if str(r.get("stage")) == "C1"]
    for i, r in enumerate(rows, 1):
        w = "stage-C1 line %d" % i
        tier = r.get("tier")
        if tier not in ("third", "fourth"):
            err("tier_history.jsonl %s: tier is %r; stage C1 changes the third-order and fourth-order tiers "
                "(third|fourth; a theme moved to rare is a third-tier event moved_to_rare)" % (w, tier),
                shape="tier_history.jsonl: tier outside third|fourth", where=w)
        if r.get("event") not in EVENTS:
            err("tier_history.jsonl %s: event is %r, not one of %s" % (w, r.get("event"), ", ".join(EVENTS)),
                shape="tier_history.jsonl: event outside the eight", where=w)
        if not r.get("move"):
            err("tier_history.jsonl %s carries no move; every recut names one of Grodal, Anteby and Holm's "
                "eight (rule 11)" % w, shape="tier_history.jsonl: no move", where=w)
        if tier == "fourth":
            if r.get("move") not in FOURTH_MOVES:
                err("tier_history.jsonl %s: a fourth-order cut's move is %r, not merging|relating (section 8)"
                    % (w, r.get("move")), shape="tier_history.jsonl: fourth-order move outside merging|relating", where=w)
            if not vlib.T4.match(str(r.get("id") or "")):
                err("tier_history.jsonl %s: a fourth-tier line's id is %r, not T4-nnn" % (w, r.get("id")),
                    shape="tier_history.jsonl: fourth-tier id not T4-nnn", where=w)
        elif tier == "third" and not vlib.T3.match(str(r.get("id") or "")):
            err("tier_history.jsonl %s: a third-tier line's id is %r, not T3-nnn" % (w, r.get("id")),
                shape="tier_history.jsonl: third-tier id not T3-nnn", where=w)
        if not str(r.get("why") or "").strip():
            warn("tier_history.jsonl %s carries no why; one clause of reason" % w,
                 shape="tier_history.jsonl: no why", where=w)
    return rows


def _touched(hist, tier, events=None):
    """Ids a stage-C1 tier_history line names, on its id or inside now[]."""
    out = set()
    for r in hist or []:
        if r.get("tier") != tier or (events and r.get("event") not in events):
            continue
        if r.get("id"):
            out.add(r["id"])
        for n in r.get("now") or []:
            if isinstance(n, dict) and n.get("id"):
                out.add(n["id"])
            elif isinstance(n, str):
                out.add(n)
    return out


def _check_scheme(outdir, hist):
    """scheme_v2.jsonl and scheme_v2.md (section 9). Returns the ids, or None."""
    v2 = jsonl(os.path.join(outdir, "scheme_v2.jsonl"))
    if v2 is None:
        return None
    if not v2:
        err("scheme_v2.jsonl is empty; it is the whole scheme after revision, every theme including the untouched")
        return None
    fz = jsonl(os.path.join(outdir, "scheme_final.jsonl")) or []
    ids, counts = set(), collections.Counter()
    fkeys = set()
    for r in fz:
        fkeys |= set(r.keys())
    for i, r in enumerate(v2, 1):
        w = "line %d" % i
        t = r.get("id")
        counts[t] += 1
        if not vlib.T3.match(str(t or "")):
            err("scheme_v2.jsonl line %d: id is %r, not T3-nnn" % (i, t),
                shape="scheme_v2.jsonl: id not T3-nnn", where=w)
            continue
        ids.add(t)
        if fkeys:
            lack = sorted(fkeys - set(r.keys()))
            if lack:
                err("scheme_v2.jsonl line %d (%s) lacks fields scheme_final.jsonl carries (%s); it mirrors the "
                    "frozen file field for field" % (i, t, lack),
                    shape="scheme_v2.jsonl: fields the frozen file carries are missing", where=w)
        if r.get("tier") not in ("main", "rare"):
            err("scheme_v2.jsonl line %d (%s): tier is %r, not main|rare" % (i, t, r.get("tier")),
                shape="scheme_v2.jsonl: tier outside main|rare", where=w)
        if r.get("family") is not None and not vlib.FAMILY.match(str(r.get("family"))):
            warn("scheme_v2.jsonl line %d (%s): family is %r, not Gnn" % (i, t, r.get("family")),
                 shape="scheme_v2.jsonl: family not Gnn", where=w)
    dup = [k for k, n in counts.items() if n > 1]
    if dup:
        err("scheme_v2.jsonl defines %s more than once; an id is never reused" % dup[:5])
    fids = {r.get("id") for r in fz if r.get("id")}
    ftier = {r.get("id"): r.get("tier") for r in fz}
    for i, r in enumerate(v2, 1):
        t = r.get("id")
        if t not in ids:
            continue
        for d in r.get("discriminators") or []:
            vs = d.get("vs") if isinstance(d, dict) else None
            if vs and vs not in ids:
                err("scheme_v2.jsonl line %d (%s): discriminator vs %r is not a theme of scheme_v2; a retired "
                    "or merged theme leaves its discriminators too" % (i, t, vs),
                    shape="scheme_v2.jsonl: discriminator against an id scheme_v2 lacks", where="line %d" % i)
        new = bool(fids) and t not in fids
        for f in ("must_show", "must_not_show"):
            if not str(r.get(f) or "").strip():
                (err if new else warn)(
                    "scheme_v2.jsonl line %d (%s) has an empty %s; a theme that arrives here declares its gate "
                    "here, in stage B1's form, before any count (rule 5)" % (i, t, f),
                    shape="scheme_v2.jsonl: an empty gate field (%s)" % ("new theme" if new else "carried theme"),
                    where="line %d" % i)
    if fids:
        gone = fids - ids
        logged = _touched(hist, "third", ("retired", "merged", "split", "members_changed"))
        miss = sorted(gone - logged)
        if miss:
            err("themes %s are in scheme_final.jsonl and not in scheme_v2.jsonl with no stage-C1 line in "
                "tier_history.jsonl; a retired or merged id is logged with its move, never dropped (rule 11)"
                % miss[:6])
        born = ids - fids
        logged = _touched(hist, "third", ("created", "split"))
        miss = sorted(born - logged)
        if miss:
            err("themes %s are in scheme_v2.jsonl and not in scheme_final.jsonl with no stage-C1 created or split "
                "line in tier_history.jsonl; a theme added or split here is logged with its move (rule 11)"
                % miss[:6])
        rare = {r.get("id") for r in v2 if r.get("tier") == "rare" and ftier.get(r.get("id")) == "main"}
        logged = _touched(hist, "third", ("moved_to_rare",))
        miss = sorted(rare - logged)
        if miss:
            err("themes %s moved from main to rare between scheme_final.jsonl and scheme_v2.jsonl with no "
                "moved_to_rare line in tier_history.jsonl (section 4)" % miss[:6])
    else:
        warn("scheme_final.jsonl is not in out/, so scheme_v2.jsonl could not be compared with the frozen file "
             "(fields, retired ids, new ids, moves to rare)")
    md = text(outdir, "scheme_v2.md")
    if md:
        absent = sorted(t for t in ids if t not in md)
        for t in absent:
            err("scheme_v2.md does not carry %s; it is the whole scheme, every theme including the untouched, "
                "not a diff (section 9)" % t, shape="scheme_v2.md: a theme of scheme_v2.jsonl missing", where=t)
        if fids and not re.search(r"\bchanged?\b|\bwhy\b", md, re.I):
            warn("scheme_v2.md declares no change (what changed, why, which placements it moves)")
    sc = os.path.join(outdir, "scheme", "scheme_current.jsonl")
    v2p = os.path.join(outdir, "scheme_v2.jsonl")
    if os.path.exists(sc) and os.path.exists(v2p) and os.path.getmtime(sc) > os.path.getmtime(v2p):
        cur = {r.get("id") or r.get("theme") for r in (jsonl(sc) or []) if r.get("id") or r.get("theme")}
        warn("scheme/scheme_current.jsonl was written after scheme_v2.jsonl (%d themes); after the freeze an edit "
             "there reaches nothing: the scheme is v2, and a recut is written into it (section 9)" % len(cur))
    print("  scheme_v2: %d themes (%d rare), frozen %d, retired %d, new %d"
          % (len(ids), sum(1 for r in v2 if r.get("tier") == "rare"), len(fids), len(fids - ids), len(ids - fids)))
    return ids


def _expected_items(outdir, ctx):
    sets = vlib.analysed_set("C1", "assignments_final.jsonl against the analysed set", outdir, ctx)
    if sets is None:
        return None, None
    analysed, _d = sets
    vlib.store_themes(ctx)
    return sum(ctx["themes_per_room"].get(s, 0) for s in analysed), analysed


def _check_assignments(outdir, ctx, ids):
    """assignments_final.jsonl, its count file, and the overlay (sections 4 and 9). Returns keyed rows."""
    fin = jsonl(os.path.join(outdir, "assignments_final.jsonl"))
    if fin is None:
        return {}
    vlib.store_themes(ctx)
    keyed, counts, empties = {}, collections.Counter(), 0
    for i, r in enumerate(fin, 1):
        w = "line %d" % i
        k = (r.get("sub"), r.get("theme_id"))
        counts[k] += 1
        keyed[k] = r
        if k not in ctx["themes"]:
            err("assignments_final.jsonl line %d: %s/%s is not a second-order theme of the store" % (i, k[0], k[1]),
                shape="assignments_final.jsonl: (sub, theme_id) not in the store", where=w)
        so = _ids(r.get("third_order"))
        if so is None:
            err("assignments_final.jsonl line %d: third_order is not a list" % i,
                shape="assignments_final.jsonl: third_order not a list", where=w)
            so = []
        so = [s for s in so if s != "unresolved"]
        if not so:
            empties += 1
        for s in so:
            if not vlib.T3.match(str(s)):
                err("assignments_final.jsonl line %d: %r is not a T3-nnn id" % (i, s),
                    shape="assignments_final.jsonl: id not T3-nnn", where=w)
            elif ids is not None and s not in ids:
                err("assignments_final.jsonl line %d: %s/%s is placed on %s, which scheme_v2.jsonl does not "
                    "define; every placement names a third-order theme of scheme v2 (section 9)" % (i, k[0], k[1], s),
                    shape="assignments_final.jsonl: an id scheme_v2 does not define", where=w)
        if len(so) > 3:
            err("assignments_final.jsonl line %d carries %d third-order ids; rule 0 allows three at most" % (i, len(so)),
                shape="assignments_final.jsonl: more than three placements", where=w)
        if r.get("confidence") not in ("clear", "arguable"):
            err("assignments_final.jsonl line %d: confidence is %r, not clear|arguable (the stage B3 schema)"
                % (i, r.get("confidence")), shape="assignments_final.jsonl: confidence outside clear|arguable", where=w)
        if r.get("read") not in ("whole", "theme-block"):
            err("assignments_final.jsonl line %d: read is %r, not whole|theme-block (the stage B3 schema)"
                % (i, r.get("read")), shape="assignments_final.jsonl: read outside whole|theme-block", where=w)
    dup = [k for k, n in counts.items() if n > 1]
    if dup:
        err("assignments_final.jsonl carries more than one line for %d items (%s ...); last write wins on "
            "(sub, theme_id) and the file is written whole, one line per second-order theme"
            % (len(dup), ["%s/%s" % k for k in dup[:3]]))
    cp = os.path.join(outdir, "assignments_final.count.txt")
    if os.path.exists(cp):
        raw = open(cp, encoding="utf-8").read().strip()
        m = re.search(r"\d+", raw)
        if not m:
            err("assignments_final.count.txt carries no number")
        elif int(m.group(0)) != len(fin):
            err("assignments_final.count.txt says %d and assignments_final.jsonl has %d lines; the count is "
                "computed from the file in the same act (rule 19)" % (int(m.group(0)), len(fin)))
    expected, analysed = _expected_items(outdir, ctx)
    if expected is not None:
        if len(keyed) != expected:
            err("assignments_final.jsonl covers %d items; the analysed set holds %d second-order themes "
                "(assignment_items_expected), one line each, not the readers' lines times R (section 9)"
                % (len(keyed), expected))
        else:
            print("  assignments_final %d lines = assignment_items_expected" % expected)
        outside = {k for k in keyed if k[0] not in analysed}
        if outside:
            err("assignments_final.jsonl places %d items in rooms outside the analysed set (%s ...)"
                % (len(outside), ["%s/%s" % k for k in sorted(outside)[:3]]))
    # against the settled line: nothing deleted, every moved item in the overlay
    prev = jsonl(os.path.join(outdir, "assign_final.jsonl"))
    rev = jsonl(os.path.join(outdir, "assign_revisions_only.jsonl"))
    if prev is None:
        warn("assign_final.jsonl is not in out/, so assignments_final.jsonl could not be compared with the "
             "settled line (keys, moved items)")
    else:
        pkeyed = {(r.get("sub"), r.get("theme_id")): r for r in prev}
        gone = sorted(set(pkeyed) - set(keyed))
        if gone:
            err("assignments_final.jsonl lacks %d items assign_final.jsonl settles (%s ...); nothing is deleted, "
                "unchanged lines are carried through verbatim (section 9)" % (len(gone), ["%s/%s" % k for k in gone[:3]]))
        if len(keyed) != len(pkeyed) and not gone:
            err("assignments_final.jsonl has %d distinct keys and assign_final.jsonl %d; the count equals the "
                "distinct (sub, theme_id) keys of assign_final.jsonl (section 9)" % (len(keyed), len(pkeyed)))
        moved = {k for k in keyed if k in pkeyed and _placement(keyed[k]) != _placement(pkeyed[k])}
        if rev is not None:
            rkeyed = {(r.get("sub"), r.get("theme_id")): r for r in rev}
            for k in sorted(moved - set(rkeyed)):
                err("assignments_final.jsonl moves %s/%s from %s to %s and assign_revisions_only.jsonl has no "
                    "line for it; the overlay holds every changed line (section 9)"
                    % (k[0], k[1], _placement(pkeyed[k]), _placement(keyed[k])),
                    shape="assign_revisions_only.jsonl: a moved item missing from the overlay", where="%s/%s" % k)
            for k, r in sorted(rkeyed.items()):
                if k not in keyed:
                    err("assign_revisions_only.jsonl revises %s/%s, which assignments_final.jsonl does not carry"
                        % k, shape="assign_revisions_only.jsonl: an item assignments_final lacks", where="%s/%s" % k)
                elif _placement(r) != _placement(keyed[k]):
                    err("assign_revisions_only.jsonl gives %s/%s %s and assignments_final.jsonl %s; the overlay's "
                        "line supersedes and the two agree" % (k[0], k[1], _placement(r), _placement(keyed[k])),
                        shape="assign_revisions_only.jsonl: overlay and final disagree", where="%s/%s" % k)
                for s in _placement(r):
                    if ids is not None and s not in ids:
                        err("assign_revisions_only.jsonl: %s/%s placed on %s, which scheme_v2.jsonl does not define"
                            % (k[0], k[1], s), shape="assign_revisions_only.jsonl: an id scheme_v2 does not define",
                            where="%s/%s" % k)
            print("  revised lines %d of %d (moved placements %d)" % (len(rev), len(fin), len(moved)))
    if fin:
        share = empties / float(len(fin))
        n6 = text(outdir, "notes-C1.md").lower()
        if share > 0.2 and n6 and "empt" not in n6:
            err("assignments_final.jsonl has %d empty placements of %d (%.0f%%), above one in five, and notes-C1.md "
                "does not mention the empties; that is a finding about the scheme and goes at the top (section 6)"
                % (empties, len(fin), 100 * share))
        print("  empties %d of %d" % (empties, len(fin)))
    return keyed


def _check_fourth(outdir, ids, hist, keyed):
    rows = jsonl(os.path.join(outdir, "fourth", "fourth.jsonl"))
    if rows is None:
        return
    if not rows:
        warn("fourth/fourth.jsonl is empty; no fourth-order theme has been cut yet (section 8)")
    counts, owner = collections.Counter(), collections.defaultdict(list)
    t4s = set()
    for i, r in enumerate(rows, 1):
        w = "line %d" % i
        t = r.get("id")
        counts[t] += 1
        if not vlib.T4.match(str(t or "")):
            err("fourth/fourth.jsonl line %d: id is %r, not T4-nnn" % (i, t),
                shape="fourth/fourth.jsonl: id not T4-nnn", where=w)
        else:
            t4s.add(t)
        for f in ("name", "gloss", "disconfirm") + (("source",) if r.get("declared") in ("borrowed", "adapted") else ()):
            if not str(r.get(f) or "").strip():
                err("fourth/fourth.jsonl line %d (%s) has no %s; a construct is declared with its source, its "
                    "gloss and what would disconfirm it (section 8, contract section 2)" % (i, t, f),
                    shape="fourth/fourth.jsonl: %s missing" % f, where=w)
        if r.get("declared") not in DECLARED:
            err("fourth/fourth.jsonl line %d (%s): declared is %r, not borrowed|adapted|coined" % (i, t, r.get("declared")),
                shape="fourth/fourth.jsonl: declared outside borrowed|adapted|coined", where=w)
        if not str(r.get("prose") or "").strip():
            err("fourth/fourth.jsonl line %d (%s) has no prose; a fourth-order theme with no prose is a heading: "
                "say what holds its members together without listing them, or recut it" % (i, t),
                shape="fourth/fourth.jsonl: no prose", where=w)
        mem = _ids(r.get("members"))
        if mem is None or not mem:
            err("fourth/fourth.jsonl line %d (%s) has no members; a fourth-order theme is a named group of "
                "third-order themes" % (i, t), shape="fourth/fourth.jsonl: no members", where=w)
            mem = []
        for m in mem:
            if not vlib.T3.match(str(m)):
                err("fourth/fourth.jsonl line %d (%s): member %r is not a third-order id (T3-nnn)" % (i, t, m),
                    shape="fourth/fourth.jsonl: a member that is not a third-order id", where=w)
            elif ids is not None and m not in ids:
                err("fourth/fourth.jsonl line %d (%s): member %s is not a theme of scheme_v2.jsonl" % (i, t, m),
                    shape="fourth/fourth.jsonl: a member scheme_v2 does not define", where=w)
            owner[m].append(t)
        if len(set(mem)) != len(mem):
            err("fourth/fourth.jsonl line %d (%s) lists a member twice" % (i, t),
                shape="fourth/fourth.jsonl: a member listed twice", where=w)
    dup = [k for k, n in counts.items() if n > 1]
    if dup:
        err("fourth/fourth.jsonl defines %s more than once; an id is never reused" % dup[:5])
    for m, ts in sorted(owner.items()):
        if len(ts) > 1:
            err("third-order theme %s sits in two fourth-order themes (%s); the stage file allows no overlap: a "
                "fourth-order theme is a partition of the third-order tier, and a second-order theme lifts to two "
                "only through rule 0. Cut it once." % (m, ", ".join(ts)),
                shape="fourth/fourth.jsonl: a third-order theme in two fourth-order themes", where=m)
    if hist is not None:
        logged = _touched(hist, "fourth")
        for t in sorted(t4s - logged):
            err("fourth/fourth.jsonl cuts %s with no stage-C1 line in tier_history.jsonl (tier fourth, move "
                "merging|relating); each cut is a tier_history line, logged and snapped when it is made (section 8)" % t,
                shape="tier_history.jsonl: a fourth-order cut not logged", where=t)
    if rows and ids:
        md = text(outdir, os.path.join("fourth", "fourth.md")) or text(outdir, "fourth.md")
        if not md:
            err("fourth/fourth.md was not written; the fourth-order themes are written there with their prose, and "
                "the third-order themes none picks up are listed at its foot")
        else:
            for t in sorted(t4s):
                if t not in md:
                    err("fourth/fourth.md does not carry %s" % t, shape="fourth/fourth.md: a fourth-order theme missing", where=t)
            notes = text(outdir, "notes-C1.md")
            unpicked = sorted(ids - set(owner))
            for t in unpicked:
                if t not in md and t not in notes:
                    err("%s is picked up by no fourth-order theme and is listed neither in fourth/fourth.md nor in "
                        "notes-C1.md; the unpicked are reported as a list, never gathered into a catch-all "
                        "(section 8)" % t, shape="fourth/fourth.md: an unpicked third-order theme not listed", where=t)
            print("  fourth-order themes %d over %d third-order themes, %d unpicked" % (len(t4s), len(owner), len(unpicked)))


def _check_form_pass(outdir):
    fp = text(outdir, "form_pass-C1.md")
    if not fp:
        return
    fids = sorted(set(FP.findall(fp)))
    if not fids:
        warn("form_pass-C1.md mints no FP- id; if the form pass found nothing, say so there, since stage C2 takes "
             "the FP ids from that file and nowhere else")
    low = fp.lower()
    # The sentence is owed (section 7), but a word is not the test: a finding enters the arithmetic only
    # through a count receipt or a gate, and those are checked below. The coverage of a sweep (how many
    # communities and lines a finding covers) is prose in this file and is allowed (2026-10-08).
    if not re.search(r"arithmetic|never counted|not counted|never clustered", low):
        warn("form_pass-C1.md does not say that a form-pass finding never enters the arithmetic (section 7)")
    receipts = sorted(n for n in os.listdir(outdir)
                      if n.endswith(".count.txt") or re.match(r"counts?[-_.]", n)) if os.path.isdir(outdir) else []
    for name in receipts:
        hit = sorted(set(FP.findall(text(outdir, name))))
        if hit:
            err("the count receipt %s names %s; a form-pass finding never enters a count (section 7)"
                % (name, hit[:4]), shape="an FP id in a count receipt", where=name)
    sp = os.path.join(outdir, "scheme_v2.jsonl")
    for row in [r for r in (jsonl(sp) or []) if isinstance(r, dict)]:
        for f in ("must_show", "must_not_show"):
            hit = sorted(set(FP.findall(json.dumps(row.get(f, "")))))
            if hit:
                err("the gate %s of %s names %s; do not invent a gate to make a form-pass finding look "
                    "promotable (section 7, rule 5)" % (f, row.get("id"), hit[:4]),
                    shape="an FP id in a gate", where="scheme_v2.jsonl")
    for word, sweep in (("form", "form (turn shape, position, length, timing)"), ("register", "register"),
                        ("not said", "what is not said")):
        if word not in low:
            warn("form_pass-C1.md does not name the %s sweep; the pass runs three times over" % sweep)
    if "cannot reach" not in low and "could not reach" not in low and "not reach" not in low:
        warn("form_pass-C1.md does not name what the pass could not reach (a register or a stance is invisible to "
             "string matching; section 7)")
    for name in ("assignments_final.jsonl", "assign_revisions_only.jsonl", "scheme_v2.jsonl",
                 os.path.join("fourth", "fourth.jsonl"), "tier_history.jsonl"):
        raw = text(outdir, name)
        hit = sorted(set(FP.findall(raw)))
        if hit:
            err("%s carries %s; a form-pass finding lives in form_pass-C1.md prose and nowhere else, no line in any "
                "JSONL (section 7)" % (name, hit[:4]), shape="an FP id in a JSONL", where=name)
    print("  form pass: %d FP ids" % len(fids))


def _check_notes(outdir):
    t = text(outdir, "notes-C1.md")
    if not t:
        return
    low = t.lower()
    if "revision rate" not in low:
        err("notes-C1.md does not report the revision rate (two hundred placements re-decided by seed; section 3)")
    if "seed" not in low:
        warn("notes-C1.md does not record the seed the two hundred placements were drawn by (section 3)")
    if "stopping" not in low:
        warn("notes-C1.md does not declare the stopping criterion, which comes before the first recut (section 4)")
    for word, what in (("arguable", "the pair test's arguable rates, joints and lumps (section 5)"),
                       ("empt", "the empties by kind (section 6)"),
                       ("prediction", "whether stage B1's prediction in confusions.md held (section 6)"),
                       ("reach", "what the form pass could not reach (section 7)")):
        if word not in low:
            warn("notes-C1.md does not give %s" % what)
    if re.search(r"transmission after revision|\balpha\b", low):
        vlib.licence_sentence(outdir, "notes-C1.md", "stage B4's transmission after revision")
    _reliability_word(outdir, "notes-C1.md")


def _check_rechecks(outdir, ctx, ids):
    """J, 2026-10-11: a gate amended at C1 owes the rechecks of the placements it could move; a move made with
    mem.py reassign names the concepts behind each theme; the gates of scheme v2 agree with one another."""
    ct = vlib.code_themes(vlib.recut_overlay("codes", jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or [], ctx.get("outdir")))
    vlib.recheck_errors(outdir, "C1", ct, ids)
    for i, r in enumerate(jsonl(os.path.join(outdir, "assignments_final.jsonl")) or [], 1):
        for m in r.get("moves") or []:
            if str(m.get("stage")) == "C1" and str(m.get("t") or "") >= vlib.RULE_DATE and not m.get("support"):
                err("assignments_final.jsonl line %d: a move at %s names no concepts; mem.py reassign takes --codes"
                    % (i, m.get("t")), shape="assignments_final.jsonl: a move without its concepts", where="line %d" % i)
    rows, name = vlib.gate_scheme(outdir)
    if rows and name.endswith("scheme_v2.jsonl"):
        vlib.gate_warnings(outdir, rows, name, edited={c.get("theme") for c in vlib.gate_changes(outdir, "C1")})


def check(root, outdir, ctx):
    # a pass may close early (section 1); the whole set is owed at the last pass, the one that writes the handback
    last = os.path.exists(os.path.join(outdir, "handback-C1.md")) or vlib.current_step(root) is None
    if not last:
        need(outdir, "notes-C1.md")
        if not vlib.diary_lines(outdir, "C1"):
            err("the diary holds no line for stage C1; every move is logged as you work (Moments to log)")
        hist = _history_06(outdir)
        ids = _check_scheme(outdir, hist) if os.path.exists(os.path.join(outdir, "scheme_v2.jsonl")) else None
        if os.path.exists(os.path.join(outdir, "assignments_final.jsonl")):
            _check_assignments(outdir, ctx, ids)
        _check_rechecks(outdir, ctx, ids)
        print("  a pass closed; the full set (scheme v2, assignments, the fourth-order themes, the form pass) is "
              "owed at the last pass, with the handback")
        return
    need(outdir, "scheme_v2.md", "scheme_v2.jsonl", "assignments_final.jsonl", "assignments_final.count.txt",
         "assign_revisions_only.jsonl", os.path.join("fourth", "fourth.jsonl"), "form_pass-C1.md", "notes-C1.md",
         "tier_history.jsonl")
    if not vlib.diary_lines(outdir, "C1"):
        err("the diary holds no line for stage C1; each source line read, the stopping criterion, each gate amended, "
            "each pair called, each sweep and each cut are logged as you work (Moments to log)")
    hist = _history_06(outdir)
    if hist is not None and not hist:
        warn("tier_history.jsonl has no stage-C1 line; if the revision changed no theme and cut no fourth-order "
             "theme, say so in notes-C1.md")
    ids = _check_scheme(outdir, hist)
    keyed = _check_assignments(outdir, ctx, ids)
    _check_rechecks(outdir, ctx, ids)
    _check_fourth(outdir, ids, hist, keyed)
    _check_form_pass(outdir)
    _check_notes(outdir)


# ---- the self-test ------------------------------------------------------------------------------

SCHEME = [
    {"id": "T3-014", "name": "recruiting outside", "gloss": "asking strangers for hands", "family": "G01",
     "tier": "main", "must_show": "a call for placers addressed beyond the room",
     "must_not_show": "a call to members already present", "decide_when_both": "the addressee decides",
     "discriminators": [{"vs": "T3-020", "question": "is the addressee outside the room"}],
     "varies": "", "is_not": "", "gate_parts": None, "exemplars": []},
    {"id": "T3-020", "name": "defending", "gloss": "holding a border under attack", "family": "G02",
     "tier": "main", "must_show": "a line held against another room",
     "must_not_show": "a call for hands", "decide_when_both": "the verb decides",
     "discriminators": [{"vs": "T3-014", "question": "is the act holding or asking"}],
     "varies": "", "is_not": "", "gate_parts": None, "exemplars": []},
]
FOURTH = [{"id": "T4-001", "name": "getting hands", "gloss": "calling for placers", "declared": "coined",
           "source": "this corpus", "disconfirm": "a room that recruits without addressing anyone",
           "members": ["T3-014"], "prose": "What holds these together is the act of asking beyond the room."},
          {"id": "T4-002", "name": "holding", "gloss": "keeping a border", "declared": "adapted",
           "source": "March 1991", "disconfirm": "a border held with no attacker",
           "members": ["T3-020"], "prose": "What holds these together is the act of keeping a line."}]
LICENCE = ("Stage B4's figure bounds whether the written descriptions decide, not whether they are right.\n")


def _w(outdir, name, content=""):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


def _fixture(outdir, root):
    _wj(outdir, "dropped.jsonl", [])
    _wj(outdir, "scheme_final.jsonl", SCHEME)
    _wj(outdir, "scheme_v2.jsonl", SCHEME)
    _w(outdir, "scheme_v2.md", "# Scheme v2\n\n## T3-014 recruiting outside\n\n## T3-020 defending\n\n"
       "No theme changed; why: no source line required it.\n")
    lines = [{"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"], "confidence": "clear", "read": "whole"},
             {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"}]
    _wj(outdir, "assign_final.jsonl", lines)
    _wj(outdir, "assignments_final.jsonl", lines)
    _w(outdir, "assignments_final.count.txt", "2\n")
    _wj(outdir, "assign_revisions_only.jsonl", [])
    _wj(outdir, os.path.join("fourth", "fourth.jsonl"), FOURTH)
    _w(outdir, os.path.join("fourth", "fourth.md"), "# Fourth-order themes\n\n## T4-001 getting hands\n\n"
       "## T4-002 holding\n\nUnpicked: none.\n")
    _wj(outdir, "tier_history.jsonl", [
        {"t": "x", "stage": "C1", "leg": "C1-1", "tier": "fourth", "id": "T4-001", "move": "relating",
         "event": "created", "why": "cut"},
        {"t": "x", "stage": "C1", "leg": "C1-1", "tier": "fourth", "id": "T4-002", "move": "relating",
         "event": "created", "why": "cut"}])
    _w(outdir, "form_pass-C1.md", "Sweep 1, form. Sweep 2, register. Sweep 3, what is not said.\n"
       "FP-01: the cheapest act is the one-word call; denmark, 2 lines.\n"
       "A form-pass finding never enters the arithmetic. What the pass could not reach: stance.\n")
    _w(outdir, "notes-C1.md", "Stopping criterion declared. Revision rate: 0 of 200 moved, seed 7. Arguable pairs: "
       "none above the corpus rate. Empties: none. Stage B1's prediction held. The pass could not reach stance.\n"
       "Transmission after revision as stage B4 read it, alpha 0.6. " + LICENCE)
    _wj(outdir, "diary/C1-1.jsonl", [{"t": "x", "stage": "C1", "leg": "C1-1", "kind": "note", "ids": [],
                                      "text": "read the sources"}])


def _plant_outside_v2(outdir, root):
    _fixture(outdir, root)
    _wj(outdir, "assignments_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-099"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"}])
    _wj(outdir, "assign_revisions_only.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-099"], "confidence": "clear", "read": "whole"}])


def _plant_two_fourths(outdir, root):
    _fixture(outdir, root)
    rows = [dict(r) for r in FOURTH]
    rows[1]["members"] = ["T3-020", "T3-014"]
    _wj(outdir, os.path.join("fourth", "fourth.jsonl"), rows)


def _plant_member_not_t3(outdir, root):
    _fixture(outdir, root)
    rows = [dict(r) for r in FOURTH]
    rows[0]["members"] = ["t07"]
    _wj(outdir, os.path.join("fourth", "fourth.jsonl"), rows)


def _plant_count(outdir, root):
    _fixture(outdir, root)
    _w(outdir, "assignments_final.count.txt", "4\n")


def _plant_unlogged_retire(outdir, root):
    _fixture(outdir, root)
    _wj(outdir, "scheme_v2.jsonl", SCHEME[:1])
    _wj(outdir, "assignments_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-014"], "confidence": "clear", "read": "whole"}])
    _wj(outdir, "assign_revisions_only.jsonl", [
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-014"], "confidence": "clear", "read": "whole"}])
    _wj(outdir, os.path.join("fourth", "fourth.jsonl"), FOURTH[:1])


def _plant_moved_not_in_overlay(outdir, root):
    _fixture(outdir, root)
    _wj(outdir, "assignments_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"}])


def _plant_fp_in_receipt(outdir, root):
    _fixture(outdir, root)
    _w(outdir, "assignments_final.count.txt", "2\nFP-01 1\n")


def _plant_fp_in_gate(outdir, root):
    _fixture(outdir, root)
    rows = [dict(r) for r in SCHEME]
    rows[0]["must_show"] = "a call for placers addressed beyond the room, as FP-01"
    _wj(outdir, "scheme_v2.jsonl", rows)


def _plant_no_sentence(outdir, root):
    # the word test is gone: a form pass that reports its sweep's coverage and omits the sentence is no error
    _fixture(outdir, root)
    _w(outdir, "form_pass-C1.md", "Sweep 1, form. Sweep 2, register. Sweep 3, what is not said.\n"
       "FP-01: the cheapest act is the one-word call; 2 communities, 14 lines.\n"
       "What the pass could not reach: stance.\n")


PLANTED = [
    ("placement outside scheme_v2", _plant_outside_v2, "which scheme_v2.jsonl does not define"),
    ("a T3 in two fourth-order themes", _plant_two_fourths, "sits in two fourth-order themes"),
    ("a member that is not a T3", _plant_member_not_t3, "is not a third-order id"),
    ("count.txt off", _plant_count, "assignments_final.count.txt says"),
    ("a retired id unlogged", _plant_unlogged_retire, "not in scheme_v2.jsonl with no stage-C1 line"),
    ("a moved item not in the overlay", _plant_moved_not_in_overlay, "has no line for it; the overlay"),
    ("an FP id in a count receipt", _plant_fp_in_receipt, "the count receipt assignments_final.count.txt names"),
    ("an FP id in a gate", _plant_fp_in_gate, "the gate must_show of T3-014 names"),
    ("sweep coverage, no sentence", _plant_no_sentence, None),   # passes: coverage is allowed, no word test
]
