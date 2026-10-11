"""checks/stage_B2.py: the close-check of stage B2, the assignment pilot, v38.

Written from stages/STAGE-B2-coding-pilot.md (Outputs, sections 1 to 6, Close), FLEET.md,
and the v37 check it descends from (_v37-source/tools/validate.py, stage03). It checks the
SHAPE of the stage's files: existence, parse, ids that resolve, counts that reconcile. It cannot
check whether a placement or an edit is right.

Stage B2 is a fleet stage with rounds. Every leg closes through this check, so the check first
decides which leg it is closing:

  build leg   no DONE anywhere under out/_fleet_raw/B2/: the packets and RETURN-B2.md exist,
              author_items.jsonl and gold_items.jsonl were placed first, notes-B2.md carries
              the declarations, the round's manifest entry is there.
  check leg   a DONE under out/_fleet_raw/B2/round-k/ (or _fleet_raw/B2/ itself): everything a
              build leg owes, and one scored line per dispatched round in pilot_rounds.jsonl,
              every edit in scheme_edits.jsonl with its caused_by and its tier_history line,
              every return line in _fleet_raw resolving to an item and a scheme id.
  the freeze  once a dispatch that is not a numbered round has returned (the gold round and the
              stability check, FLEET.md), or once stability-B2.md exists: scheme_final.md and
              .jsonl with families.jsonl beside them, stability-B2.md, pilot_report.md,
              exemplar_candidates.jsonl, and the licence sentence wherever a figure appears.

A later build leg owes everything the earlier check leg owed, so the check-leg checks stay on
once any DONE exists.

Files the stage file names without giving their fields, checked for existence and parse only:
scheme_final.md, pilot_report.md, stability-B2.md, notes-B2.md (declarations by keyword),
RETURN-B2.md (by keyword), tier_history.jsonl (stage B1 gives its fields; here only the count).

Not carried from v37:
  - the error that pilot_rounds.jsonl holds a line with "gold": true. v38's line schema in
    section 3 has no gold flag; the gold round is recognised by its dispatch folder, and a line
    flagged "gold": true is still accepted as that round's line. Its absence is a warning.
  - the v37 ids `case_theme` and `second_order` on every line: now `theme_id` and `third_order`
    (CHANGELOG-v37-to-v38.md).
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

CONF = ("clear", "arguable")
READ = ("whole", "theme-block")
KINDS = ("scheme-ambiguous", "item-is-a-bag", "reader-error", "author-error", "genuine-joint", "gate-check")
ROUND_FIELDS = ("round", "n_items", "agents", "exemplars", "fidelity_vs_author", "agreement_pairwise",
                "alpha", "items_with_disagreement", "seed")
EDIT_FIELDS = ("round", "theme", "field", "caused_by", "was", "now", "why")
RETURN_FIELDS = ("sub", "theme_id", "batch", "agent", "replicate", "position", "third_order", "multi",
                 "why", "confidence", "read", "exemplar_read", "families_opened", "t_start", "t", "support")
KB50 = 50 * 1024


# ---- helpers vlib does not have -----------------------------------------------------------------

def fleet_dirs(outdir, stage):
    """Every folder under out/_fleet_raw/NN (and NN itself) holding a DONE, sorted."""
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


def returns_in(d):
    """(reader_path, rows) for every validated return fleet.py left under a raw folder."""
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*", "*.jsonl"))):
        if p.endswith(".failed.txt"):
            continue
        out.append((p, jsonl(p) or []))
    return out


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def key_of(r):
    return "%s/%s" % (r.get("sub"), r.get("theme_id"))


def packets_dir(outdir, stage):
    c = sorted(glob.glob(os.path.join(outdir, "_packets-%s*" % stage)))
    return c[-1] if c else None


def gold_leaked(outdir, stage, where_dirs):
    for d in where_dirs:
        if not d or not os.path.isdir(d):
            continue
        for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            b = os.path.basename(p).lower()
            if os.path.isfile(p) and b.startswith("gold_items"):
                err("%s holds %s; the answer key stays outside the readers' directory (FLEET.md). Move it "
                    "out and rebuild the packets" % (os.path.relpath(d, outdir), os.path.basename(p)))


def check_placement_file(name, rows, themes, scheme, need_reason):
    keys = set()
    for i, r in enumerate(rows, 1):
        k = (r.get("sub"), r.get("theme_id"))
        if k not in themes:
            err("%s line %d places %s, which is not a second-order theme in package/store/themes.jsonl; "
                "every item is a store theme" % (name, i, key_of(r)),
                shape="%s: an item not in the store" % name, where="line %d" % i)
        if k in keys:
            err("%s line %d repeats %s; one line per item" % (name, i, key_of(r)),
                shape="%s: a repeated item" % name, where="line %d" % i)
        keys.add(k)
        so = as_list(r.get("third_order"))
        if not so:
            err("%s line %d has no third_order; place every item yourself before any packet exists" % (name, i),
                shape="%s: a line with no placement" % name, where="line %d" % i)
        for s in so:
            if scheme is not None and s not in scheme:
                err("%s line %d places %s on %r, which the scheme file does not define; place on an id the "
                    "scheme holds" % (name, i, key_of(r), s),
                    shape="%s: a placement on an id the scheme does not define" % name, where="line %d" % i)
        if r.get("confidence") not in CONF:
            err("%s line %d: confidence is %r, not clear|arguable; stage B4 splits its transmission rows "
                "on it" % (name, i, r.get("confidence")),
                shape="%s: confidence outside clear|arguable" % name, where="line %d" % i)
        if r.get("corrected") or r.get("corrected_round"):
            err("%s line %d carries a correction. That file is the record of what you placed BEFORE the "
                "rounds, which is the whole of its value; log the change in scheme_edits.jsonl instead"
                % (name, i), shape="%s: a line carries a correction" % name, where="line %d" % i)
        if need_reason and not (r.get("reason") or r.get("reasons") or r.get("why")):
            err("%s line %d has no reason for its placement (section 1: placements, confidence and "
                "reasons)" % (name, i), shape="%s: a line with no reason" % name, where="line %d" % i)
    return keys


def check_return_spec(outdir, name):
    t = text(outdir, name)
    if not t:
        return
    low = t.lower()
    if "rule 0" not in low:
        err("%s does not state rule 0; the return specification opens with rule 0 in the contract's words" % name)
    if "multiplacement_log" not in low:
        err("%s does not tell a reader that a second placement owes its line in multiplacement_log.jsonl" % name)
    if not re.search(r"```[^\n]*\n.*?```", t, re.S):
        err("%s has no fenced block; fleet.py reads the end marker off the last line of the last fenced "
            "block, so the return line and the end marker go in one" % name)
    if "confirm" not in low:
        err("%s has no line telling the reader to confirm it reached the end marker (FLEET.md)" % name)


def spec_in_force(outdir, name, d):
    """Was the dispatch in d sent under the current return specification (fleet.py's arm.json keeps the
    sha256 of the specification it sent)? None when the dispatch kept no arm.json."""
    try:
        arm = json.load(open(os.path.join(d, "arm.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return None
    t = text(outdir, name)
    import hashlib
    return bool(t) and arm.get("return_spec_sha256") == hashlib.sha256(t.encode("utf-8")).hexdigest()


def check_also_present(rel, r, ct, scheme, required, where):
    """Rule 0 as amended (J, 2026-10-11): a bag places one theme and names the others under also_present,
    each with its own concepts. Checked where present; required on a bag line when the specification the
    round was sent under asks for it."""
    so = as_list(r.get("third_order"))
    bag = bool(r.get("item_is_a_bag") or r.get("bag"))
    for p in vlib.also_present_problems(r.get("also_present"), so, r.get("sub"), r.get("theme_id"), ct, scheme):
        err("%s: a return on %s: %s" % (rel, key_of(r), p), shape="%s: also_present" % rel, where=where)
    if bag and required and not r.get("also_present"):
        err("%s: a return on %s is a bag and names no also_present; rule 0 keeps every theme beyond the one placed, "
            "each with its own concepts" % (rel, key_of(r)), shape="%s: a bag with no also_present" % rel, where=where)


def check_packets(outdir, stage, exemplars_allowed):
    pd = packets_dir(outdir, stage)
    if pd is None:
        err("no _packets-%s/ in the output directory; the build leg writes one packet per reader with "
            "packets.py %s before it closes at packets-out" % (stage, stage))
        return None
    files = sorted(glob.glob(os.path.join(pd, "*.md")))
    if not files:
        err("%s holds no .md packet; packets.py %s writes the index page, the family pages and the items"
            % (os.path.relpath(pd, outdir), stage))
    for p in files:
        n = os.path.getsize(p)
        if n > KB50:
            err("%s/%s is %d bytes, over FLEET.md's 50 KB ceiling; split the batch or the family page"
                % (os.path.relpath(pd, outdir), os.path.basename(p), n),
                shape="_packets-%s: a packet over 50 KB" % stage, where=os.path.basename(p))
        if not exemplars_allowed:
            with open(p, encoding="utf-8", errors="replace") as f:
                for i, ln in enumerate(f, 1):
                    if ln.lower().startswith("exemplar ("):
                        err("%s/%s line %d serves an exemplar; stage B2 measures the description alone, "
                            "rebuild the packets without --exemplars"
                            % (os.path.relpath(pd, outdir), os.path.basename(p), i),
                            shape="_packets-%s: an exemplar served" % stage, where=os.path.basename(p))
                        break
    return pd


# ---- the check -------------------------------------------------------------------------------------

def check(root, outdir, ctx):
    stage = "B2"
    need(outdir, "author_items.jsonl", "gold_items.jsonl", "RETURN-B2.md", "notes-B2.md")
    vlib.manifest_entry(outdir, stage, "the pilot's readers")
    themes = vlib.store_themes(ctx)
    if not themes:
        err("package/store/themes.jsonl holds no second-order themes, so no item could be resolved; give "
            "validate.py the folder root holding package/")
    vlib.store_codes(ctx)
    codes = ctx["codes"]
    scheme, scheme_name = vlib.load_scheme(outdir)
    if scheme is None:
        err("no scheme file in the output directory (scheme.jsonl from stage B1, or scheme_final.jsonl); "
            "no third_order id can be resolved without one")
    else:
        bad = sorted(s for s in scheme if not vlib.T3.match(s))
        if bad:
            err("%s defines ids that are not third-order ids of the form T3-NNN: %s" % (scheme_name, bad[:5]))

    auth = jsonl(os.path.join(outdir, "author_items.jsonl")) or []
    gold = jsonl(os.path.join(outdir, "gold_items.jsonl")) or []
    if not auth:
        err("author_items.jsonl is empty; place every item of the hard set yourself before any packet exists")
    elif not (40 <= len(auth) <= 60):
        warn("author_items.jsonl has %d items; section 1 says forty to sixty" % len(auth))
    if not gold:
        err("gold_items.jsonl is empty; the gold set is drawn by section 1's rule, placed by you and shown "
            "to no pilot reader")
    ak = check_placement_file("author_items.jsonl", auth, themes, scheme, False)
    gk = check_placement_file("gold_items.jsonl", gold, themes, scheme, True)
    both = ak & gk
    if both:
        err("%d items are in both author_items.jsonl and gold_items.jsonl (%s); the gold set is drawn from "
            "what is left" % (len(both), sorted("%s/%s" % k for k in both)[:3]))
    item_keys = {"%s/%s" % k for k in ak | gk}

    # the declarations, by keyword; the words are the stage file's
    notes = text(outdir, "notes-B2.md").lower()
    for word, what in (("threshold", "the stopping threshold"),
                       ("agreement", "the agreement definition stages B3 and B4 reuse"),
                       ("gold", "the gold policy: count, seeding rate, that they are seeded"),
                       ("seed", "the seed of the random sample"),
                       ("cap", "the batch cap stage B3 runs under")):
        if notes and word not in notes:
            err("notes-B2.md does not declare %s (no %r in it); section 1 says it is declared before round 1"
                % (what, word))

    check_return_spec(outdir, "RETURN-B2.md")
    pd = check_packets(outdir, stage, exemplars_allowed=False)
    gold_leaked(outdir, stage, [pd, os.path.join(outdir, "_fleet_raw", stage)])

    # ---- the check leg: what the dispatch returned -------------------------------------------------
    dirs = fleet_dirs(outdir, stage)
    leg = "check" if dirs else "build"
    print("  leg: %s (%d dispatch folders with DONE)" % (leg, len(dirs)))
    round_dirs, other_dirs = {}, []
    for d in dirs:
        m = re.search(r"round-?(\d+)$", os.path.basename(d))
        if m:
            round_dirs[int(m.group(1))] = d
        elif d != os.path.join(outdir, "_fleet_raw", stage):
            other_dirs.append(d)
        else:
            round_dirs.setdefault(1, d)

    rounds = jsonl(os.path.join(outdir, "pilot_rounds.jsonl"))
    edits = jsonl(os.path.join(outdir, "scheme_edits.jsonl"))
    if leg == "build":
        if rounds is None and edits is None:
            print("  author items %d, gold items %d, scheme ids %d" % (len(auth), len(gold), len(scheme or ())))
            return
    rounds = rounds or []
    edits = edits or []

    if dirs and not rounds:
        err("pilot_rounds.jsonl is empty or absent while _fleet_raw/B2 holds a finished dispatch; the check "
            "leg scores every round, one line each")
    # the returns themselves
    ct = vlib.code_themes(jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or [])
    spec_ap = "also_present" in text(outdir, "RETURN-B2.md")
    for d in dirs:
        rel = os.path.relpath(d, outdir)
        n_lines, n_readers = 0, 0
        required = bool(spec_ap and spec_in_force(outdir, "RETURN-B2.md", d))
        for p, rows in returns_in(d):
            n_readers += 1
            for i, r in enumerate(rows, 1):
                if "predicted_confusion" in r:
                    continue
                n_lines += 1
                for k in RETURN_FIELDS:
                    if k not in r:
                        err("%s: a return line lacks %r; the return line of section 1 carries it. A return "
                            "that fails the specification is reissued, not scored" % (rel, k),
                            shape="%s: a return line without %s" % (rel, k), where="%s line %d" % (os.path.basename(p), i))
                if key_of(r) not in item_keys:
                    err("%s: a return places %s, which is in neither author_items.jsonl nor gold_items.jsonl; a "
                        "reader placed an item you never placed yourself" % (rel, key_of(r)),
                        shape="%s: a return on an item you did not place" % rel, where=key_of(r))
                so = as_list(r.get("third_order"))
                for s in so:
                    if scheme is not None and s not in scheme:
                        err("%s: a return places %s on %r, which %s does not define" % (rel, key_of(r), s, scheme_name),
                            shape="%s: a return on an id the scheme does not define" % rel, where=key_of(r))
                if r.get("multi") and len(so) < 2:
                    err("%s: a return on %s says multi with one id" % (rel, key_of(r)),
                        shape="%s: multi with a single id" % rel, where=key_of(r))
                if len(so) > 3:
                    err("%s: a return on %s carries %d themes; three at most (rule 0)" % (rel, key_of(r), len(so)),
                        shape="%s: more than three themes on a line" % rel, where=key_of(r))
                if r.get("read") == "label-only":
                    err("%s: a return on %s reads label-only; a reader that read only the label placed the "
                        "coder's grouping, not the material; reissue it" % (rel, key_of(r)),
                        shape="%s: read is label-only" % rel, where=key_of(r))
                elif "read" in r and r.get("read") not in READ:
                    err("%s: a return on %s has read %r, not whole|theme-block" % (rel, key_of(r), r.get("read")),
                        shape="%s: read outside whole|theme-block" % rel, where=key_of(r))
                if "confidence" in r and r.get("confidence") not in CONF:
                    err("%s: a return on %s has confidence %r, not clear|arguable" % (rel, key_of(r), r.get("confidence")),
                        shape="%s: confidence outside clear|arguable" % rel, where=key_of(r))
                if r.get("exemplar_read") is not None:
                    err("%s: a return on %s has exemplar_read %r; no exemplar is served at stage B2, the field is "
                        "null" % (rel, key_of(r), r.get("exemplar_read")),
                        shape="%s: exemplar_read not null" % rel, where=key_of(r))
                for c in as_list(r.get("support")):
                    if codes and (r.get("sub"), c) not in codes:
                        err("%s: a return on %s cites support %r, which does not resolve in package/store/codes.jsonl "
                            "for that room" % (rel, key_of(r), c),
                            shape="%s: a support id that does not resolve" % rel, where=key_of(r))
                check_also_present(rel, r, ct, scheme, required, "%s line %d" % (os.path.basename(p), i))
        print("  %s: %d readers, %d return lines" % (rel, n_readers, n_lines))

    # one scored line per dispatched round
    by_round = {}
    for i, r in enumerate(rounds, 1):
        for k in ROUND_FIELDS:
            if k not in r:
                err("pilot_rounds.jsonl line %d lacks %r; the line of section 3 carries it" % (i, k),
                    shape="pilot_rounds.jsonl: a line without %s" % k, where="line %d" % i)
        if r.get("exemplars") is True:
            err("pilot_rounds.jsonl line %d says exemplars true; this stage measures the description alone, "
                "no exemplar is served" % i, shape="pilot_rounds.jsonl: exemplars true", where="line %d" % i)
        for k in ("fidelity_vs_author", "agreement_pairwise", "alpha"):
            v = r.get(k)
            if k in r and not (isinstance(v, (int, float)) and not isinstance(v, bool)):
                err("pilot_rounds.jsonl line %d: %s is %r, not a number" % (i, k, v),
                    shape="pilot_rounds.jsonl: %s not a number" % k, where="line %d" % i)
            elif k != "alpha" and isinstance(v, (int, float)) and not (0 <= v <= 1):
                err("pilot_rounds.jsonl line %d: %s is %r, outside 0..1" % (i, k, v),
                    shape="pilot_rounds.jsonl: %s outside 0..1" % k, where="line %d" % i)
        n = r.get("n_items")
        if isinstance(n, int) and auth and n not in (len(auth), len(gold)):
            err("pilot_rounds.jsonl line %d: n_items %d is neither the hard set (%d) nor the gold set (%d); "
                "a round runs the whole set" % (i, n, len(auth), len(gold)),
                shape="pilot_rounds.jsonl: n_items off the set", where="line %d" % i)
        if isinstance(r.get("agents"), int) and r["agents"] != 3:
            warn("pilot_rounds.jsonl line %d: agents %d; section 2 sends each packet to three fresh readers"
                 % (i, r["agents"]))
        for it in as_list(r.get("items_with_disagreement")):
            if it not in item_keys:
                err("pilot_rounds.jsonl line %d: items_with_disagreement names %r, not an item of the hard set or "
                    "the gold set (sub/theme_id)" % (i, it),
                    shape="pilot_rounds.jsonl: a disagreement on an item you did not place", where="line %d" % i)
        if r.get("gold") is True:
            by_round.setdefault("gold", r)
        elif isinstance(r.get("round"), int):
            by_round.setdefault(r["round"], r)
    for k, d in sorted(round_dirs.items()):
        if k not in by_round:
            err("%s holds a finished dispatch and pilot_rounds.jsonl has no line for round %d; the check leg "
                "scores it (fidelity, pairwise agreement, alpha) before it closes" % (os.path.relpath(d, outdir), k))
    if other_dirs and "gold" not in by_round:
        warn("%s returned but no pilot_rounds.jsonl line is flagged \"gold\": true; the gold figure is reported "
             "beside the last round's" % ", ".join(os.path.relpath(d, outdir) for d in other_dirs))

    # the edits
    if dirs and edits is None:
        err("scheme_edits.jsonl was not written; every edit is logged there, and a round with no edit leaves "
            "it empty rather than absent")
    for i, e in enumerate(edits, 1):
        for k in EDIT_FIELDS:
            if k not in e:
                err("scheme_edits.jsonl line %d lacks %r" % (i, k),
                    shape="scheme_edits.jsonl: a line without %s" % k, where="line %d" % i)
        cb = as_list(e.get("caused_by"))
        if not cb:
            err("scheme_edits.jsonl line %d: the edit on %s (%s, round %s) has no caused_by; an edit with no "
                "caused_by is not allowed, name the items that divided the readers"
                % (i, e.get("theme"), e.get("field"), e.get("round")),
                shape="scheme_edits.jsonl: an edit with no caused_by", where="line %d" % i)
        gate_check = e.get("kind") == "gate-check"      # J, 2026-10-11 (QB2-003): a repair the gate check found
        for it in cb:
            if str(it).startswith("gates:"):
                continue
            if it not in item_keys:
                err("scheme_edits.jsonl line %d: caused_by names %r, not an item of the hard set (sub/theme_id)"
                    % (i, it), shape="scheme_edits.jsonl: caused_by on an item you did not place", where="line %d" % i)
        if scheme is not None and e.get("theme") and e["theme"] not in scheme:
            err("scheme_edits.jsonl line %d edits %r, which %s does not define" % (i, e.get("theme"), scheme_name),
                shape="scheme_edits.jsonl: an edit on an id the scheme does not define", where="line %d" % i)
        if e.get("kind") and e.get("kind") not in KINDS:
            err("scheme_edits.jsonl line %d: kind %r is not one of the five (%s)" % (i, e.get("kind"), ", ".join(KINDS)),
                shape="scheme_edits.jsonl: a kind outside the five", where="line %d" % i)
    if edits and not any(e.get("kind") == "author-error" for e in edits):
        warn("no scheme edit is recorded as author-error; a pilot that never returns one measures obedience "
             "(say so in pilot_report.md if it is so)")
    if edits:                       # J, 2026-10-11: every edit owes the rechecks of your placements it could move
        vlib.recheck_errors(outdir, stage, ct, scheme)
    if edits:
        th = [r for r in (jsonl(os.path.join(outdir, "tier_history.jsonl")) or []) if str(r.get("stage")) == stage]
        moves = [e for e in edits if e.get("kind") != "gate-check"]
        if len(th) < len(moves):
            err("tier_history.jsonl has %d stage-B2 lines for %d scheme edits; every edit is a tier_history line "
                "with its move (relabelled or rescoped); gate-check mirrors excepted" % (len(th), len(moves)))

    # ---- the gate check (J, 2026-10-11): warnings while the rounds run, errors on the frozen scheme --------
    frozen = os.path.exists(os.path.join(outdir, "scheme_final.jsonl"))
    grows, gname = vlib.gate_scheme(outdir)
    if grows:
        vlib.gate_warnings(outdir, grows, gname, as_errors=frozen and gname.endswith("scheme_final.jsonl"),
                           edited={e.get("theme") for e in edits if e.get("theme")})

    # ---- the freeze ------------------------------------------------------------------------------------
    finished = bool(other_dirs) or os.path.exists(os.path.join(outdir, "stability-B2.md")) or "gold" in by_round
    if finished or frozen:
        need(outdir, "scheme_final.md", "scheme_final.jsonl", "families.jsonl")
    if frozen:
        fin = jsonl(os.path.join(outdir, "scheme_final.jsonl")) or []
        fids = {r.get("id") for r in fin}
        for r in fin:
            if r.get("tier") not in (None, "rare", "common", "core"):
                err("scheme_final.jsonl: theme %s has tier %r; the rare tier is marked \"tier\": \"rare\"" % (r.get("id"), r.get("tier")),
                    shape="scheme_final.jsonl: a tier outside rare", where=str(r.get("id")))
        for name, rows in (("author_items.jsonl", auth), ("gold_items.jsonl", gold)):
            for r in rows:
                for s in as_list(r.get("third_order")):
                    if s not in fids:
                        err("%s places %s on %r, which the frozen scheme_final.jsonl does not define; a merge or "
                            "retirement at the freeze must be recorded on the item" % (name, key_of(r), s),
                            shape="%s: a placement the frozen scheme does not define" % name, where=key_of(r))
    if finished:
        need(outdir, "stability-B2.md", "pilot_report.md", "exemplar_candidates.jsonl")
        ex = jsonl(os.path.join(outdir, "exemplar_candidates.jsonl")) or []
        for i, r in enumerate(ex, 1):
            k = r.get("key") or key_of(r)
            if k not in item_keys:
                err("exemplar_candidates.jsonl line %d names %r, not an item of the hard set or the gold set; the "
                    "candidates are the items that divided readers" % (i, k),
                    shape="exemplar_candidates.jsonl: an item you did not place", where="line %d" % i)
        vlib.licence_sentence(outdir, "stability-B2.md", "the stability figure")
        vlib.licence_sentence(outdir, "pilot_report.md", "fidelity")
    elif os.path.exists(os.path.join(outdir, "pilot_report.md")):
        vlib.licence_sentence(outdir, "pilot_report.md", "fidelity")

    print("  author items %d, gold items %d, rounds scored %d, edits %d (author-error %d), scheme ids %d (%s)%s"
          % (len(auth), len(gold), len(rounds), len(edits), sum(1 for e in edits if e.get("kind") == "author-error"),
             len(scheme or ()), scheme_name, ", frozen" if frozen else ""))


# ---- the self-test ---------------------------------------------------------------------------------

def _base(outdir, root):
    os.makedirs(os.path.join(outdir, "_packets-B2"), exist_ok=True)
    w = lambda n, s: open(os.path.join(outdir, n), "w", encoding="utf-8").write(s)
    w("dropped.jsonl", json.dumps({"sub": "sweden", "why": "fixture"}) + "\n")
    w("scheme.jsonl", "\n".join(json.dumps(x) for x in (
        {"id": "T3-001", "name": "recruiting", "gloss": "asking outsiders for hands"},
        {"id": "T3-002", "name": "holding", "gloss": "defending a border"})) + "\n")
    w("families.jsonl", json.dumps({"family": "G01", "name": "labour", "themes": ["T3-001", "T3-002"]}) + "\n")
    w("author_items.jsonl", "\n".join(json.dumps(x) for x in (
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-001"], "confidence": "clear"},)) + "\n")
    w("gold_items.jsonl", json.dumps({"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-002"],
                                      "confidence": "clear", "reason": "the gate names a border"}) + "\n")
    w("RETURN-B2.md", "# RETURN-B2\n\nRule 0. Single placement, exception on the record; a second placement "
      "owes its line in multiplacement_log.jsonl.\n\n```json\n{\"sub\": \"...\"}\nEND-OF-RETURN\n```\n\n"
      "Confirm on the last line that you reached the marker.\n")
    w("notes-B2.md", "Stopping threshold 0.8 pairwise agreement (Jaccard on sets). Gold: 1 item, seeded at 0.1. "
      "Random sample seed 7. Batch cap 40.\n")
    w("run_manifest.json", json.dumps([{"stage": "B2", "model": "cheap", "seeds": {"round1": 7},
                                        "decoding": {"temperature": 0}, "n_agents": 3}]))
    open(os.path.join(outdir, "_packets-B2", "P01.md"), "w").write("# packet\n")


def _plant_scheme_id(outdir, root):
    _base(outdir, root)
    with open(os.path.join(outdir, "author_items.jsonl"), "w") as f:
        f.write(json.dumps({"sub": "denmark", "theme_id": "t07", "third_order": ["T3-099"], "confidence": "clear"}) + "\n")


def _plant_unscored_round(outdir, root):
    _base(outdir, root)
    d = os.path.join(outdir, "_fleet_raw", "B2", "round-1", "P01")
    os.makedirs(d)
    open(os.path.join(outdir, "_fleet_raw", "B2", "round-1", "DONE"), "w").write("{}\n")
    open(os.path.join(d, "r1.jsonl"), "w").write(json.dumps(
        {"sub": "denmark", "theme_id": "t07", "batch": "P01", "agent": "r1", "replicate": 1, "position": 1,
         "third_order": ["T3-001"], "multi": False, "why": {"T3-001": "hands"}, "confidence": "clear",
         "read": "whole", "exemplar_read": None, "families_opened": ["G01"], "t_start": "t0", "t": "t1",
         "support": ["c0117"]}) + "\n")
    open(os.path.join(outdir, "scheme_edits.jsonl"), "w").write("")
    open(os.path.join(outdir, "pilot_rounds.jsonl"), "w").write("")


def _plant_edit_without_cause(outdir, root):
    _plant_unscored_round(outdir, root)
    open(os.path.join(outdir, "pilot_rounds.jsonl"), "w").write(json.dumps(
        {"round": 1, "n_items": 1, "agents": 3, "exemplars": False, "fidelity_vs_author": 1.0,
         "agreement_pairwise": 1.0, "alpha": 1.0, "items_with_disagreement": [], "seed": 7}) + "\n")
    open(os.path.join(outdir, "scheme_edits.jsonl"), "w").write(json.dumps(
        {"round": 1, "theme": "T3-001", "field": "must_not_show", "caused_by": [], "was": "a", "now": "b",
         "why": "readers split", "kind": "scheme-ambiguous"}) + "\n")
    open(os.path.join(outdir, "tier_history.jsonl"), "w").write(json.dumps(
        {"stage": "B2", "id": "T3-001", "event": "rescoped", "move": "asking questions"}) + "\n")


def _plant_edit_without_recheck(outdir, root):
    """J, 2026-10-11: an edit on T3-001 with author_items' denmark/t07 on it, and no recheck."""
    _plant_edit_without_cause(outdir, root)
    open(os.path.join(outdir, "scheme_edits.jsonl"), "w").write(json.dumps(
        {"round": 1, "theme": "T3-001", "field": "must_not_show", "caused_by": ["denmark/t07"], "was": "a", "now": "b",
         "why": "readers split", "kind": "scheme-ambiguous"}) + "\n")


def _plant_bag_without_also_present(outdir, root):
    """J, 2026-10-11: the round went out under a specification that asks for also_present, and a bag names none."""
    import hashlib
    _plant_unscored_round(outdir, root)
    spec = ("# RETURN-B2\n\nRule 0. Single placement; a second placement owes its line in multiplacement_log.jsonl; "
            "beyond three place one and name the rest under also_present.\n\n```json\n{\"sub\": \"...\", "
            "\"also_present\": {}}\nEND-OF-RETURN\n```\n\nConfirm on the last line that you reached the marker.\n")
    open(os.path.join(outdir, "RETURN-B2.md"), "w").write(spec)
    json.dump({"return_spec_sha256": hashlib.sha256(spec.encode("utf-8")).hexdigest()},
              open(os.path.join(outdir, "_fleet_raw", "B2", "round-1", "arm.json"), "w"))
    open(os.path.join(outdir, "_fleet_raw", "B2", "round-1", "P01", "r1.jsonl"), "w").write(json.dumps(
        {"sub": "denmark", "theme_id": "t07", "batch": "P01", "agent": "r1", "replicate": 1, "position": 1,
         "third_order": ["T3-001"], "multi": False, "why": {"T3-001": "hands"}, "confidence": "clear",
         "read": "whole", "exemplar_read": None, "families_opened": ["G01"], "t_start": "t0", "t": "t1",
         "support": ["c0117"], "item_is_a_bag": True}) + "\n")


def _plant_one_way_at_freeze(outdir, root):
    """J, 2026-10-11: the frozen scheme carries a discriminator that runs one way."""
    _plant_unscored_round(outdir, root)
    open(os.path.join(outdir, "pilot_rounds.jsonl"), "w").write(json.dumps(
        {"round": 1, "n_items": 1, "agents": 3, "exemplars": False, "fidelity_vs_author": 1.0,
         "agreement_pairwise": 1.0, "alpha": 1.0, "items_with_disagreement": [], "seed": 7}) + "\n")
    open(os.path.join(outdir, "scheme_final.jsonl"), "w").write("\n".join(json.dumps(x) for x in (
        {"id": "T3-001", "name": "recruiting", "gloss": "asking outsiders for hands", "tier": "core",
         "discriminators": [{"vs": "T3-002", "question": "outsiders asked, or a border held?"}]},
        {"id": "T3-002", "name": "holding", "gloss": "defending a border", "tier": "core", "discriminators": []})) + "\n")


PLANTED = [
    ("author placement off the scheme", _plant_scheme_id, "which the scheme file does not define"),
    ("dispatched round not scored", _plant_unscored_round, "has no line for round 1"),
    ("edit without caused_by", _plant_edit_without_cause, "has no caused_by"),
    ("edit without its rechecks", _plant_edit_without_recheck, "owes rechecks"),
    ("bag without also_present", _plant_bag_without_also_present, "names no also_present"),
    ("one-way discriminator frozen", _plant_one_way_at_freeze, "discriminators run both ways"),
]
