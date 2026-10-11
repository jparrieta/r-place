"""checks/stage_B4.py: the close-check of stage B4 (adjudication, transmission, the blind sample), v38.

Written from stages/STAGE-B4-coding-adjudication-and-freeze.md (Outputs; sections 2, 3, 5, 7, 9, 10, 12;
Close), FLEET.md, and the v37 check it descends from (_v37-source/tools/validate.py, stage05).
It checks the SHAPE of the stage's files: existence, parse, ids that resolve, counts that
reconcile, the rulings against the settled line. It cannot check whether a ruling is right.

Three legs, told apart from out/:
  check leg        out/_fleet_raw/B4/DONE exists (fleet.py wrote it): everything below, plus
                   reassign.jsonl and transmission-after-revision-B4.md against the settled line.
  build leg        no DONE, but RETURN-B4.md, a stage-B4 manifest entry or out/_packets-B4/
                   exists: the adjudication files whole, adjudication_report.md, RETURN-B4.md,
                   the manifest entry, the sample's seed in notes-B4.md, the packets clean.
  adjudication leg neither: disagreements.jsonl, assign_final.jsonl, coder_conflicts.jsonl,
                   transmission-B4.md, notes-B4.md; the build leg's files are warned, not required.
A build leg closed without RETURN-B4.md therefore reads as an adjudication leg; the warning says so.

Fields the stage file does not give (checked for existence and parse only, with any (sub,
theme_id) they carry resolved): coder_conflicts.jsonl (section 4); reassign.jsonl beyond the two
strata of section 10 and the four outcomes of section 12, whose field names are v37's (stratum,
outcome).

Not carried from v37: `verdict` or `kind` as alternative names of the ruling's taxonomy (v38 fixes
`taxonomy` in section 7); `reliability-B4.md` (renamed transmission-after-revision-B4.md, and
"reliability" is now a banned word in it); `case_theme` (now theme_id).
"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

TAXONOMY = ("scheme-ambiguous", "item-is-a-bag", "reader-error", "author-error", "genuine-joint",
            "author-disagrees")
FIELDS = ("must_show", "must_not_show", "decide_when_both", "discriminators")
STRATA = ("uniform", "adjudicated")
OUTCOMES = ("agrees", "disagrees-contested", "disagrees-unanimous", "disagrees-unresolved")
FORBIDDEN_IN_PACKETS = ("assign_final.jsonl", "disagreements.jsonl", "gold_items.jsonl", "_head.md",
                        "findings.jsonl", "author_items.jsonl", "adjudication_report.md")
GATE_TEXT_FIELDS = ("must_show", "must_not_show", "decide_when_both", "varies", "is_not", "gloss", "name")


def _ids(v):
    """A placement field as a list of ids: a list, a bare string, or nothing."""
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v else []
    return list(v) if isinstance(v, list) else None


def _settled_ids(row):
    """The standing placement of an assign_final line; [] where it is unresolved."""
    if row.get("unresolved") is True:
        return []
    so = _ids(row.get("third_order"))
    if so is None:
        return []
    return [s for s in so if s and s != "unresolved"]


def _frozen_scheme(outdir):
    """Stage B4 rules against the frozen scheme, scheme_final.jsonl; scheme_v2 does not exist
    yet. Returns (ids, name, rows) or (None, None, []) having said so."""
    rows = jsonl(os.path.join(outdir, "scheme_final.jsonl"))
    if rows:
        return {r.get("id") for r in rows if r.get("id")}, "scheme_final.jsonl", rows
    ids, name = vlib.load_scheme(outdir)
    if ids:
        warn("scheme_final.jsonl is not in out/; ids were resolved against %s instead. Stage B4 rules "
             "against the frozen scheme; say in notes-B4.md which file the readers held." % name)
        return ids, name, jsonl(os.path.join(outdir, name)) or []
    err("no scheme file is in out/ (scheme_final.jsonl), so no third-order id in disagreements.jsonl "
        "or assign_final.jsonl could be resolved. Stage B2 freezes it; do not rule against a scheme "
        "that is not on disk.")
    return None, None, []


def _scheme_text(rows):
    """theme id -> the joined text of its gate fields, whitespace-normalised."""
    out = {}
    for r in rows:
        parts = []
        for f in GATE_TEXT_FIELDS:
            v = r.get(f)
            if isinstance(v, str):
                parts.append(v)
        for d in r.get("discriminators") or []:
            if isinstance(d, dict):
                parts.append(str(d.get("question") or ""))
        out[r.get("id")] = " ".join(" ".join(parts).split())
    return out


def _reliability_word(outdir, name):
    """FLEET.md section 2 and stage B4 section 12: the figure is transmission after revision and is
    never called reliability. A sentence that uses the word must be the one denying it."""
    t = text(outdir, name)
    for s in re.split(r"(?<=[.!?])\s+|\n+", t):
        if re.search(r"\breliability\b", s, re.I) and not re.search(r"\b(not|never|no)\b", s, re.I):
            err("%s calls a figure reliability: %r. It is transmission after revision (FLEET.md "
                "section 2), and the word appears only in the sentence saying it is not that."
                % (name, " ".join(s.split())[:90]), shape="reliability:%s" % name, where=s[:60])


def _expected_items(outdir, ctx):
    sets = vlib.analysed_set("B4", "assign_final.jsonl's line count", outdir, ctx)
    if sets is None:
        return None, None
    analysed, _d = sets
    vlib.store_themes(ctx)
    return sum(ctx["themes_per_room"].get(s, 0) for s in analysed), analysed


def _leg(outdir):
    if os.path.exists(os.path.join(outdir, "_fleet_raw", "B4", "DONE")):
        return "check"
    if os.path.exists(os.path.join(outdir, "RETURN-B4.md")) or glob.glob(os.path.join(outdir, "_packets-B4*")):
        return "build"
    mp = os.path.join(outdir, "run_manifest.json")
    if os.path.exists(mp):
        try:
            man = json.load(open(mp, encoding="utf-8"))
            if any(isinstance(e, dict) and str(e.get("stage")) == "B4" for e in (man if isinstance(man, list) else [man])):
                return "build"
        except Exception:
            pass
    return "adjudication"


# ---- the adjudication files -------------------------------------------------------------------

def _check_assign_final(outdir, ctx, ids):
    """assign_final.jsonl: every item of the analysed set with its standing placement (section 7),
    the gold placements dropped (section 2). Returns the file's keyed rows."""
    fin = jsonl(os.path.join(outdir, "assign_final.jsonl"))
    if fin is None:
        return {}
    vlib.store_themes(ctx)
    keyed, counts = {}, collections.Counter()
    for i, r in enumerate(fin, 1):
        k = (r.get("sub"), r.get("theme_id"))
        counts[k] += 1
        keyed[k] = r
        if k not in ctx["themes"]:
            err("assign_final.jsonl line %d: %s/%s is not a second-order theme of the store" % (i, k[0], k[1]),
                shape="assign_final.jsonl: (sub, theme_id) not in the store", where="line %d" % i)
        so = _ids(r.get("third_order"))
        if so is None:
            err("assign_final.jsonl line %d: third_order is not a list" % i,
                shape="assign_final.jsonl: third_order not a list", where="line %d" % i)
            so = []
        for s in so:
            if s == "unresolved":
                continue
            if not vlib.T3.match(str(s)):
                err("assign_final.jsonl line %d: %r is not a T3-nnn id" % (i, s),
                    shape="assign_final.jsonl: id not of the form T3-nnn", where="line %d" % i)
            elif ids and s not in ids:
                err("assign_final.jsonl line %d: %s/%s is placed on %s, outside the frozen scheme; the "
                    "standing placement names a theme scheme_final.jsonl defines" % (i, k[0], k[1], s),
                    shape="assign_final.jsonl: an id outside the frozen scheme", where="line %d" % i)
        if len(so) > 3:
            err("assign_final.jsonl line %d carries %d third-order ids; rule 0 allows three at most" % (i, len(so)),
                shape="assign_final.jsonl: more than three placements", where="line %d" % i)
        if r.get("confidence") not in ("clear", "arguable"):
            err("assign_final.jsonl line %d: confidence is %r, not clear|arguable (the stage B3 line)"
                % (i, r.get("confidence")), shape="assign_final.jsonl: confidence outside clear|arguable",
                where="line %d" % i)
        if "read" in r and r.get("read") not in ("whole", "theme-block"):
            err("assign_final.jsonl line %d: read is %r, not whole|theme-block; a label-only reading "
                "placed the coder's grouping, not the material" % (i, r.get("read")),
                shape="assign_final.jsonl: read outside whole|theme-block", where="line %d" % i)
    dup = [k for k, n in counts.items() if n > 1]
    if dup:
        err("assign_final.jsonl carries more than one line for %d items (%s ...); one settled line per "
            "(sub, theme_id), the standing placement" % (len(dup), ["%s/%s" % k for k in dup[:3]]))
    expected, analysed = _expected_items(outdir, ctx)
    if expected is not None:
        if len(keyed) != expected:
            err("assign_final.jsonl settles %d items; the analysed set holds %d second-order themes "
                "(assignment_items_expected). Section 2: the drop removes gold placements by (item, agent, "
                "replicate), never themes; a theme that carried gold still owes its line." % (len(keyed), expected))
        else:
            print("  settled items %d = assignment_items_expected" % expected)
        outside = {k for k in keyed if k[0] not in analysed}
        if outside:
            err("assign_final.jsonl settles %d items in rooms outside the analysed set (%s ...)"
                % (len(outside), ["%s/%s" % k for k in sorted(outside)[:3]]))
    # section 2: no seeded gold placement survives, told apart by (item, agent, replicate)
    batches = jsonl(os.path.join(outdir, "batches-B3.jsonl"))
    if batches is None:
        warn("batches-B3.jsonl is not in out/, so the gold drop (section 2) was NOT checked against stage "
             "B3's keys; the check reads the gold tags from that file")
    else:
        gold = set()
        for b in batches:
            for it in b.get("gold_items") or []:
                gold.add((it, b.get("agent"), b.get("replicate")))
        if gold:
            for i, r in enumerate(fin, 1):
                key = ("%s/%s" % (r.get("sub"), r.get("theme_id")), r.get("agent"), r.get("replicate"))
                if key in gold:
                    err("assign_final.jsonl line %d: %s by %s replicate %s is a seeded gold placement that "
                        "survived the drop; drop by (item, agent, replicate) on stage B3's keys before "
                        "anything else (section 2)" % (i, key[0], key[1], key[2]),
                        shape="assign_final.jsonl: a gold placement survived the drop", where="line %d" % i)
    return keyed


def _ct(ctx):
    if "code_themes" not in ctx:
        ctx["code_themes"] = vlib.code_themes(jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or [])
    return ctx["code_themes"]


def _check_disagreements(outdir, root, ctx, ids, srows, keyed):
    """disagreements.jsonl, section 7's line. Returns {key: last ruling row}."""
    dis = jsonl(os.path.join(outdir, "disagreements.jsonl"))
    if dis is None:
        return {}
    vlib.store_themes(ctx)
    stext = _scheme_text(srows)
    last, store_quotes, tax = {}, [], collections.Counter()
    unresolved_n = 0
    for i, d in enumerate(dis, 1):
        w = "line %d" % i
        k = (d.get("sub"), d.get("theme_id"))
        last[k] = d
        if k not in ctx["themes"]:
            err("disagreements.jsonl line %d: %s/%s is not a second-order theme of the store" % (i, k[0], k[1]),
                shape="disagreements.jsonl: (sub, theme_id) not in the store", where=w)
        if keyed and k not in keyed:
            err("disagreements.jsonl line %d: %s/%s has no line in assign_final.jsonl; every ruled item is "
                "an item of the analysed set with a standing placement" % (i, k[0], k[1]),
                shape="disagreements.jsonl: an item assign_final.jsonl does not settle", where=w)
        t = d.get("taxonomy")
        if t not in TAXONOMY:
            err("disagreements.jsonl line %d: taxonomy is %r, not one of %s (section 7)" % (i, t, ", ".join(TAXONOMY)),
                shape="disagreements.jsonl: a ruling outside the taxonomy", where=w)
        tax[t] += 1
        readers = d.get("readers")
        if not isinstance(readers, list) or not all(isinstance(x, list) for x in readers):
            err("disagreements.jsonl line %d: readers is not a list of placement lists (one per reader)" % i,
                shape="disagreements.jsonl: readers not a list of lists", where=w)
            readers = []
        for rr in readers:
            for s in rr:
                if ids and s not in ids:
                    err("disagreements.jsonl line %d: a reader's placement %r is outside the frozen scheme" % (i, s),
                        shape="disagreements.jsonl: a reader id outside the frozen scheme", where=w)
        ruling = _ids(d.get("ruling"))
        if ruling is None:
            err("disagreements.jsonl line %d: ruling is not a list" % i,
                shape="disagreements.jsonl: ruling not a list", where=w)
            ruling = []
        for s in ruling:
            if ids and s not in ids:
                err("disagreements.jsonl line %d: the ruling names %r, outside the frozen scheme; no edit to "
                    "the scheme here (section 8)" % (i, s),
                    shape="disagreements.jsonl: a ruling outside the frozen scheme", where=w)
        if ruling:                     # J, 2026-10-11: your ruling names the concepts behind each theme it places
            if not d.get("support_by_theme"):
                err("disagreements.jsonl line %d: the ruling %s names no support_by_theme; every placement you make "
                    "names the concepts behind each theme (rule 0)" % (i, ruling),
                    shape="disagreements.jsonl: a ruling without support_by_theme", where=w)
            else:
                for pb in vlib.support_problems(d.get("support_by_theme"), ruling, k[0], k[1], _ct(ctx)):
                    err("disagreements.jsonl line %d: %s" % (i, pb), shape="disagreements.jsonl: support_by_theme", where=w)
        for pb in vlib.also_present_problems(d.get("also_present"), ruling, k[0], k[1], _ct(ctx), ids):
            err("disagreements.jsonl line %d: %s" % (i, pb), shape="disagreements.jsonl: also_present", where=w)
        unresolved = d.get("unresolved")
        if not isinstance(unresolved, bool):
            err("disagreements.jsonl line %d: unresolved is %r, not true|false" % (i, unresolved),
                shape="disagreements.jsonl: unresolved not a boolean", where=w)
        elif unresolved and ruling:
            err("disagreements.jsonl line %d: unresolved is true and the ruling is %s; where the scheme does "
                "not decide, ruling is empty" % (i, ruling),
                shape="disagreements.jsonl: unresolved with a ruling", where=w)
        elif not unresolved and not ruling:
            err("disagreements.jsonl line %d: the ruling is empty and unresolved is false; an empty ruling "
                "is recorded as unresolved and carried" % i,
                shape="disagreements.jsonl: empty ruling not marked unresolved", where=w)
        if unresolved is True:
            unresolved_n += 1
        union = {s for rr in readers for s in rr}
        nn = d.get("named_neither")
        if not isinstance(nn, bool):
            err("disagreements.jsonl line %d: named_neither is %r, not true|false" % (i, nn),
                shape="disagreements.jsonl: named_neither not a boolean", where=w)
        elif ruling and readers:
            outside = [s for s in ruling if s not in union]
            if outside and not nn:
                err("disagreements.jsonl line %d: the ruling names %s, which no reader chose, and "
                    "named_neither is false; record named_neither every time (section 6)" % (i, outside),
                    shape="disagreements.jsonl: named_neither false on a placement no reader chose", where=w)
            if nn and not outside:
                err("disagreements.jsonl line %d: named_neither is true but every ruled id was a reader's "
                    "choice" % i, shape="disagreements.jsonl: named_neither true on a reader's choice", where=w)
        if d.get("confidence") not in ("clear", "arguable"):
            err("disagreements.jsonl line %d: confidence is %r, not clear|arguable" % (i, d.get("confidence")),
                shape="disagreements.jsonl: confidence outside clear|arguable", where=w)
        if not str(d.get("why") or "").strip():
            err("disagreements.jsonl line %d carries no why; one clause from the item's material" % i,
                shape="disagreements.jsonl: no why", where=w)
        if not d.get("leg"):
            warn("disagreements.jsonl line %d carries no leg" % i, shape="disagreements.jsonl: no leg", where=w)
        theme = d.get("theme")
        if theme is not None and ids and theme not in ids:
            err("disagreements.jsonl line %d: theme %r is not in the frozen scheme" % (i, theme),
                shape="disagreements.jsonl: theme outside the frozen scheme", where=w)
        br = d.get("boundary_ruling")
        if br is not None:
            m = re.fullmatch(r"(T3-\d{3})\|(T3-\d{3})", str(br))
            if not m:
                err("disagreements.jsonl line %d: boundary_ruling is %r, not \"T3-nnn|T3-mmm\" or null" % (i, br),
                    shape="disagreements.jsonl: boundary_ruling malformed", where=w)
            elif ids and not {m.group(1), m.group(2)} <= ids:
                err("disagreements.jsonl line %d: boundary_ruling %s names an id outside the frozen scheme" % (i, br),
                    shape="disagreements.jsonl: boundary_ruling outside the frozen scheme", where=w)
        if t == "reader-error" and len(readers) >= 2 and all(sorted(rr) == sorted(readers[0]) for rr in readers):
            err("disagreements.jsonl line %d: reader-error on an item where every reader made the same "
                "placement; two independent readers making the same miss is a scheme defect (section 7)" % i,
                shape="disagreements.jsonl: reader-error on an agreed placement", where=w)
        # the quote: for scheme-ambiguous the sentence of the scheme that failed to decide (section 7),
        # else the deciding sentence of the item's material, a participant's words through cite.py
        q = " ".join(str(d.get("quote") or "").split())
        if t == "scheme-ambiguous":
            f = d.get("field")
            if f not in FIELDS:
                err("disagreements.jsonl line %d: scheme-ambiguous names field %r; name one of %s" % (i, f, ", ".join(FIELDS)),
                    shape="disagreements.jsonl: scheme-ambiguous without a named field", where=w)
            if not q:
                err("disagreements.jsonl line %d: scheme-ambiguous with no quote; quote the sentence that "
                    "failed to decide" % i, shape="disagreements.jsonl: scheme-ambiguous without a quote", where=w)
            elif stext:
                own = stext.get(theme, "")
                if q in own:
                    pass
                elif any(q in v for v in stext.values()):
                    warn("disagreements.jsonl line %d: the quoted sentence is in the scheme but not under theme "
                         "%s; name the theme whose field failed" % (i, theme),
                         shape="disagreements.jsonl: quote under another theme", where=w)
                else:
                    store_quotes.append(q)
        elif not q:
            if unresolved is True:
                warn("disagreements.jsonl line %d: unresolved with no quote; the sentence that did not decide "
                     "is still worth quoting" % i, shape="disagreements.jsonl: unresolved without a quote", where=w)
            else:
                err("disagreements.jsonl line %d carries no quote; the deciding sentence is quoted through "
                    "cite.py and never from a room note" % i, shape="disagreements.jsonl: no quote", where=w)
        else:
            store_quotes.append(q)
        # the standing line agrees with the ruling
        if keyed and k in keyed and isinstance(unresolved, bool):
            standing = _settled_ids(keyed[k])
            if unresolved and standing:
                err("disagreements.jsonl line %d: %s/%s is unresolved, but assign_final.jsonl gives it %s; an "
                    "unresolved item carries no placement" % (i, k[0], k[1], standing),
                    shape="assign_final.jsonl: a placement on an unresolved item", where=w)
            elif not unresolved and ruling and sorted(standing) != sorted(ruling):
                err("assign_final.jsonl gives %s/%s %s, and disagreements.jsonl rules %s; the standing "
                    "placement is the ruling" % (k[0], k[1], standing, ruling),
                    shape="assign_final.jsonl: standing placement differs from the ruling", where=w)
    if store_quotes:
        vlib.cites_resolve(outdir, root, store_quotes, "disagreements.jsonl")
    if dis:
        if unresolved_n == 0:
            warn("disagreements.jsonl has no unresolved ruling among %d; an adjudication that resolves everything "
                 "has resolved some things by preference (section 8). If that count is honest, say so in "
                 "notes-B4.md." % len(dis))
        if tax.get("author-error", 0) == 0:
            warn("disagreements.jsonl has no author-error among %d rulings; an adjudication that never returns "
                 "one is measuring obedience (section 7). Say in adjudication_report.md why none arose." % len(dis))
    print("  rulings %d: %s" % (len(dis), dict(tax)))
    return last


def _check_coder_conflicts(outdir, ctx):
    # section 4 gives no schema for coder_conflicts.jsonl: existence and parse only, plus any
    # (sub, theme_id) it carries resolved to the store.
    rows = jsonl(os.path.join(outdir, "coder_conflicts.jsonl"))
    if rows is None:
        return
    vlib.store_themes(ctx)
    frame = {x.get("sub") for x in (ctx.get("rooms") or [])}
    for i, r in enumerate(rows, 1):
        if r.get("sub") and r.get("theme_id") and (r["sub"], r["theme_id"]) not in ctx["themes"]:
            err("coder_conflicts.jsonl line %d: %s/%s is not a second-order theme of the store" % (i, r["sub"], r["theme_id"]),
                shape="coder_conflicts.jsonl: (sub, theme_id) not in the store", where="line %d" % i)
        for s in r.get("subs") or r.get("rooms") or []:
            if frame and s not in frame:
                err("coder_conflicts.jsonl line %d: room %r is not in the frame" % (i, s),
                    shape="coder_conflicts.jsonl: a room outside the frame", where="line %d" % i)
    print("  coder conflicts %d" % len(rows))


def _check_transmission(outdir):
    t = text(outdir, "transmission-B4.md").lower()
    if not t:
        return
    for phrase, row in (("fails to transmit", "the second"), ("does not decide", "the third"),
                        ("unintended", "the fourth")):
        if phrase not in t:
            err("transmission-B4.md does not give %s row (%r) by name; section 3's four rows with their items, "
                "by family" % (row, phrase))
    if not re.search(r"\bG\d{2,3}\b", t, re.I):
        warn("transmission-B4.md names no family (G..); section 3 gives the rows by family")
    if "gold" not in t or "pilot" not in t:
        warn("transmission-B4.md does not say the rows are over the gold and pilot items and that the split rate "
             "outside them cannot be decomposed (section 3)")
    vlib.licence_sentence(outdir, "transmission-B4.md", "transmission")


def _check_report(outdir, last):
    t = text(outdir, "adjudication_report.md")
    if not t:
        return
    low = t.lower()
    for word in ("named_neither", "unresolved", "author-error", "author-disagrees"):
        if word not in low:
            err("adjudication_report.md does not name the %s count; section 9 lists it" % word)
    for word in ("scheme-ambiguous", "item-is-a-bag", "reader-error", "genuine-joint"):
        if word not in low:
            warn("adjudication_report.md does not name %s in the taxonomy split" % word)
    for word in ("must_show", "must_not_show", "decide_when_both", "discriminator"):
        if word not in low:
            warn("adjudication_report.md: fields by ambiguity does not name %s (four numbers)" % word)
    if "predict" not in low:
        warn("adjudication_report.md does not say whether stage B2's predictions held")
    if "before" not in low or "after" not in low:
        warn("adjudication_report.md does not report agreement before and after")
    if "reliab" in low and not re.search(r"\bnot\b[^.]{0,80}reliab", low):
        warn("adjudication_report.md mentions reliability; the figure after adjudication is not a reliability "
             "figure and the report says so in those words")
    pairs = {d.get("boundary_ruling") for d in last.values() if d.get("boundary_ruling")}
    for p in sorted(pairs):
        a, b = str(p).split("|", 1) if "|" in str(p) else (p, "")
        if p not in t and not (a and b and ("%s|%s" % (b, a)) in t) and not (a in t and b in t):
            err("adjudication_report.md has no paragraph for the boundary %s that disagreements.jsonl rules once; "
                "each boundary is one paragraph in the report with its item list (section 7)" % p,
                shape="adjudication_report.md: a boundary ruling with no paragraph", where=str(p))


def _check_notes(outdir, leg):
    t = text(outdir, "notes-B4.md").lower()
    if not t:
        return
    if "gold" not in t:
        err("notes-B4.md does not say how many placements the gold drop removed (section 2)")
    for word, what in (("packet", "how many items and packets (section 5)"),
                       ("confidence", "what a reader's confidence counts for (section 5)"),
                       ("neither", "whether a ruling may name a theme neither reader chose (section 5)"),
                       ("unresolved", "what you do when the scheme does not decide (section 5)")):
        if word not in t:
            warn("notes-B4.md does not declare %s" % what)
    if leg in ("build", "check"):
        if "seed" not in t:
            err("notes-B4.md does not record the blind sample's seed; the draw is declared there before it is "
                "made (section 10)")
        for word in ("uniform", "adjudicated", "jaccard"):
            if word not in t:
                warn("notes-B4.md does not declare the %s part of the blind sample's design (section 10: the two "
                     "strata, the agreement definition from notes-B2.md)" % word)


# ---- the build leg ------------------------------------------------------------------------------

def _check_build(outdir):
    rt = text(outdir, "RETURN-B4.md")
    if rt:
        if not re.search(r"```[^\n]*\n(.*?)```", rt, re.S):
            err("RETURN-B4.md has no fenced return example, so fleet.py can find no end marker; the "
                "specification carries the return line, rule 0, the end marker and the confirm line")
        if "confirm" not in rt.lower():
            warn("RETURN-B4.md has no confirm line (one line telling the reader to confirm it reached the end)")
        if "rule 0" not in rt.lower() and "single placement" not in rt.lower():
            warn("RETURN-B4.md does not give rule 0 in the contract's words")
    ents = vlib.manifest_entry(outdir, "B4", "the blind sample's readers")
    if ents:
        e = ents[-1]
        for f in ("model", "decoding"):
            if not e.get(f):
                err("run_manifest.json's stage-B4 entry carries no %s; the readers' model, seed, decoding and "
                    "reader count are appended before the first packet leaves (section 10)" % f)
        if not (e.get("seeds") or e.get("seed")):
            err("run_manifest.json's stage-B4 entry carries no seed (seeds or seed); the blind sample is drawn "
                "by a recorded seed (section 10)")
        if not e.get("n_agents"):
            err("run_manifest.json's stage-B4 entry carries no n_agents; two fresh readers per item (section 10)")
    for pdir in glob.glob(os.path.join(outdir, "_packets-B4*")):
        for p in glob.glob(os.path.join(pdir, "**", "*"), recursive=True):
            if not os.path.isfile(p):
                continue
            b = os.path.basename(p)
            if b in FORBIDDEN_IN_PACKETS:
                err("%s holds %s; section 10: the packets carry the frozen scheme and the sampled themes and "
                    "nothing else, never a ruling, a key, the head or your notes" % (os.path.relpath(pdir, outdir), b))
            if b.endswith((".md", ".txt", ".jsonl")) and os.path.getsize(p) > 50 * 1024:
                err("%s is %d bytes, above the 50 KB packet ceiling (FLEET.md)"
                    % (os.path.relpath(p, outdir), os.path.getsize(p)),
                    shape="_packets-05: a packet above 50 KB", where=b)
            try:
                raw = open(p, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if re.search(r"\b(ruling|adjudicat\w*|gold_items|unresolved)\b", raw, re.I):
                warn("%s mentions a ruling, an adjudication or the gold key; no hint that these items were "
                     "decided before reaches a blind reader (section 10). Read the packet." % os.path.relpath(p, outdir),
                     shape="_packets-05: a packet that hints at a ruling", where=b)


# ---- the check leg ------------------------------------------------------------------------------

def _check_reassign(outdir, ctx, ids, keyed, last):
    if not os.path.exists(os.path.join(outdir, "_fleet_raw", "B4", "arm.json")):
        warn("_fleet_raw/B4/arm.json is absent; the serving arm is declared on both sides of the comparison "
             "(FLEET.md), and fleet.py writes it")
    re_ = jsonl(os.path.join(outdir, "reassign.jsonl"))
    if re_ is None:
        return
    if not re_:
        err("reassign.jsonl is empty; section 12's comparison is one line per reading, two hundred for a "
            "hundred items by two fresh readers")
        return
    vlib.store_themes(ctx)
    strata = collections.Counter()
    per_item = collections.Counter()
    items_by_stratum = collections.defaultdict(set)
    unanimous = []
    for i, r in enumerate(re_, 1):
        w = "line %d" % i
        k = (r.get("sub"), r.get("theme_id"))
        per_item[k] += 1
        if k not in ctx["themes"]:
            err("reassign.jsonl line %d: %s/%s is not a second-order theme of the store" % (i, k[0], k[1]),
                shape="reassign.jsonl: (sub, theme_id) not in the store", where=w)
        if keyed and k not in keyed:
            err("reassign.jsonl line %d: %s/%s is an item assign_final.jsonl does not settle; every fresh "
                "reading is compared with the settled line" % (i, k[0], k[1]),
                shape="reassign.jsonl: an item assign_final.jsonl does not settle", where=w)
        s = r.get("stratum")
        strata[s] += 1
        items_by_stratum[s].add(k)
        if s not in STRATA:
            err("reassign.jsonl line %d: stratum is %r, not uniform|adjudicated; the two strata are reported "
                "apart and never pooled (section 10)" % (i, s),
                shape="reassign.jsonl: stratum outside uniform|adjudicated", where=w)
        o = r.get("outcome")
        if o not in OUTCOMES:
            err("reassign.jsonl line %d: outcome is %r, not one of %s (section 12's four comparisons)"
                % (i, o, ", ".join(OUTCOMES)), shape="reassign.jsonl: outcome outside the four comparisons", where=w)
        so = _ids(r.get("third_order"))
        for t in so or []:
            if ids and t not in ids and t != "unresolved":
                err("reassign.jsonl line %d: the fresh placement %r is outside the frozen scheme the readers held" % (i, t),
                    shape="reassign.jsonl: a fresh placement outside the frozen scheme", where=w)
        # the outcome against the record
        settled = _settled_ids(keyed[k]) if keyed and k in keyed else None
        contested = k in last
        if o == "disagrees-unresolved" and settled:
            err("reassign.jsonl line %d: outcome disagrees-unresolved on %s/%s, whose settled placement is %s, "
                "not unresolved" % (i, k[0], k[1], settled),
                shape="reassign.jsonl: disagrees-unresolved on a resolved item", where=w)
        if o in ("disagrees-contested", "disagrees-unanimous") and settled is not None and not settled:
            err("reassign.jsonl line %d: outcome %s on %s/%s, whose settled placement is unresolved; that reading "
                "is disagrees-unresolved and leaves the denominator" % (i, o, k[0], k[1]),
                shape="reassign.jsonl: a disagreement counted on an unresolved item", where=w)
        if o == "disagrees-contested" and last and not contested:
            err("reassign.jsonl line %d: outcome disagrees-contested on %s/%s, which disagreements.jsonl never "
                "ruled; that item was unanimous in the fleet" % (i, k[0], k[1]),
                shape="reassign.jsonl: disagrees-contested on an item never adjudicated", where=w)
        if o == "disagrees-unanimous" and contested:
            err("reassign.jsonl line %d: outcome disagrees-unanimous on %s/%s, which disagreements.jsonl rules; "
                "that item was contested, not unanimous" % (i, k[0], k[1]),
                shape="reassign.jsonl: disagrees-unanimous on an adjudicated item", where=w)
        if o == "disagrees-unanimous":
            unanimous.append(k)
    if last:
        for k in sorted(items_by_stratum.get("adjudicated", set())):
            if k not in last:
                err("reassign.jsonl: %s/%s is in the adjudicated stratum and disagreements.jsonl never ruled it; "
                    "that stratum is drawn from the adjudicated items" % k,
                    shape="reassign.jsonl: an adjudicated-stratum item never adjudicated", where="%s/%s" % k)
    if len(re_) != 200:
        warn("reassign.jsonl has %d readings; a hundred items by two readers is two hundred, unless notes-B4.md "
             "says why not" % len(re_))
    for s in STRATA:
        n = len(items_by_stratum.get(s, ()))
        if n and n != 50:
            warn("reassign.jsonl: the %s stratum holds %d items, not fifty (section 10)" % (s, n))
    odd = [k for k, n in per_item.items() if n != 2]
    if odd:
        warn("reassign.jsonl: %d items do not have exactly two readings (%s ...); two fresh readers per item"
             % (len(odd), ["%s/%s" % k for k in odd[:3]]))
    # the figures file, against the readings
    tr = text(outdir, "transmission-after-revision-B4.md")
    low = tr.lower()
    if tr:
        for word in STRATA:
            if word not in low:
                err("transmission-after-revision-B4.md does not report the %s stratum by name; the strata are "
                    "never pooled" % word)
        if "alpha" not in low:
            err("transmission-after-revision-B4.md gives no alpha on the hundred (section 12)")
        for word, what in (("stability", "the stability floor from stability-B2.md beside alpha"),
                           ("definition", "the agreement definition stated once above the figures"),
                           ("unanimous", "the unanimous-but-disagreed items, listed, or that there were none"),
                           ("gold", "the gap between the uniform stratum and stage B2's gold figure")):
            if word not in low:
                warn("transmission-after-revision-B4.md does not give %s" % what)
        if not re.search(r"\bG\d{2,3}\b", tr):
            warn("transmission-after-revision-B4.md names no family; the figures are per family, not per theme")
        for k in unanimous:
            if ("%s/%s" % k) not in tr and not (k[0] in tr and str(k[1]) in tr):
                err("transmission-after-revision-B4.md does not name %s/%s, a unanimous item a fresh reader placed "
                    "elsewhere; each is named individually with a paragraph (section 12)" % k,
                    shape="transmission-after-revision-B4.md: a unanimous-but-disagreed item not named", where="%s/%s" % k)
        vlib.licence_sentence(outdir, "transmission-after-revision-B4.md", "transmission after revision")
        _reliability_word(outdir, "transmission-after-revision-B4.md")
    print("  blind readings %d (%s), unanimous-but-disagreed %d" % (len(re_), dict(strata), len(unanimous)))


# ---- the check ---------------------------------------------------------------------------------

def check(root, outdir, ctx):
    leg = _leg(outdir)
    print("  leg: %s" % leg)
    need(outdir, "disagreements.jsonl", "assign_final.jsonl", "coder_conflicts.jsonl", "transmission-B4.md",
         "notes-B4.md")
    if leg == "adjudication":
        for n in ("adjudication_report.md", "RETURN-B4.md"):
            if not os.path.exists(os.path.join(outdir, n)):
                warn("%s is not yet written; the build leg owes it, and this leg was read as an adjudication "
                     "leg because neither RETURN-B4.md, a stage-B4 manifest entry nor _packets-B4/ exists" % n)
    else:
        need(outdir, "adjudication_report.md", "RETURN-B4.md")
    if leg == "check":
        need(outdir, "reassign.jsonl", "transmission-after-revision-B4.md")
    if not vlib.diary_lines(outdir, "B4"):
        err("the diary holds no line for stage B4; the gold drop, the transmission rows, the conflicts pass, each "
            "declaration and each packet ruled are logged as you work (Moments to log)")
    ids, sname, srows = _frozen_scheme(outdir)
    keyed = _check_assign_final(outdir, ctx, ids)
    last = _check_disagreements(outdir, root, ctx, ids, srows, keyed)
    _check_coder_conflicts(outdir, ctx)
    _check_transmission(outdir)
    _check_report(outdir, last)
    _check_notes(outdir, leg)
    if leg in ("build", "check"):
        _check_build(outdir)
    if leg == "check":
        _check_reassign(outdir, ctx, ids, keyed, last)
    elif os.path.exists(os.path.join(outdir, "reassign.jsonl")):
        warn("reassign.jsonl exists but _fleet_raw/B4/DONE does not; the comparison is made in the check leg, "
             "after the dispatch, and this leg was not read as one")


# ---- the self-test ------------------------------------------------------------------------------

LICENCE = ("Readers share an architecture with the analyst, so the figure bounds whether the written "
           "instrument decides, not whether it is right.\n")
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


def _w(outdir, name, content=""):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


def _fixture(outdir, root, leg="build"):
    _wj(outdir, "dropped.jsonl", [])
    _wj(outdir, "scheme_final.jsonl", SCHEME)
    _wj(outdir, "batches-B3.jsonl", [{"batch": "B001", "agent": "a001", "replicate": 1, "gold_items": ["asoiaf/t02"],
                                      "items": ["denmark/t07", "asoiaf/t02"]}])
    _wj(outdir, "assign_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"], "confidence": "clear", "read": "whole",
         "agent": "a002", "replicate": 2},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole",
         "agent": "a003", "replicate": 2}])
    _wj(outdir, "disagreements.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "readers": [["T3-014"], ["T3-020"]], "ruling": ["T3-014"], "support_by_theme": {"T3-014": ["c0117"]},
         "unresolved": False, "taxonomy": "item-is-a-bag", "field": None, "theme": "T3-014",
         "quote": "we need more people at the border", "boundary_ruling": None, "named_neither": False,
         "confidence": "clear", "why": "the call is addressed outside", "leg": "B4-adj-1"}])
    _wj(outdir, "coder_conflicts.jsonl", [])
    _w(outdir, "transmission-B4.md", "# Transmission\n\nRows over the gold and pilot items, by family G01.\n"
       "Row 2, fails to transmit: none. Row 3, the instrument does not decide: none. Row 4, teaches something "
       "unintended: none.\n" + LICENCE)
    _w(outdir, "adjudication_report.md", "Items adjudicated: 1. Taxonomy: item-is-a-bag 1, scheme-ambiguous 0, "
       "reader-error 0, author-error 0, genuine-joint 0, author-disagrees 0. Fields: must_show 0, must_not_show 0, "
       "decide_when_both 0, discriminators 0. named_neither rate 0. unresolved 0. Agreement before 0.5 and after "
       "1.0, not a reliability figure. Stage B2's predictions held.\n")
    _w(outdir, "notes-B4.md", "The gold drop removed 1 placement. One packet of 1 item. A clear reading against an "
       "arguable one is nothing. A ruling may name a theme neither reader chose. Unresolved is an outcome.\n"
       "Blind sample: seed 20260901, fifty uniform and fifty adjudicated, Jaccard on sets.\n")
    _w(outdir, "RETURN-B4.md", "Return one line per item, rule 0 in the contract's words.\n\n```\n"
       "{\"batch\": \"P001\", \"position\": 1, \"third_order\": [\"T3-014\"]}\nEND-OF-RETURN\n```\n"
       "Confirm you reached the end marker.\n")
    _w(outdir, "run_manifest.json", json.dumps([
        {"stage": "A1", "model": "m"},
        {"stage": "B4", "model": "cheap", "seeds": {"blind": 20260901}, "decoding": {"temperature": 0.0}, "n_agents": 2}]))
    _wj(outdir, "diary/B4-1.jsonl", [{"t": "x", "stage": "B4", "leg": "B4-1", "kind": "note", "ids": [],
                                      "text": "gold drop removed 1"}])
    if leg == "check":
        _w(outdir, "_fleet_raw/B4/DONE", "{}\n")
        _w(outdir, "_fleet_raw/B4/arm.json", "{}\n")
        _wj(outdir, "reassign.jsonl", [
            {"sub": "denmark", "theme_id": "t07", "stratum": "adjudicated", "reader": "r1", "third_order": ["T3-014"],
             "outcome": "agrees"},
            {"sub": "denmark", "theme_id": "t07", "stratum": "adjudicated", "reader": "r2", "third_order": ["T3-020"],
             "outcome": "disagrees-contested"},
            {"sub": "asoiaf", "theme_id": "t02", "stratum": "uniform", "reader": "r3", "third_order": ["T3-020"],
             "outcome": "agrees"},
            {"sub": "asoiaf", "theme_id": "t02", "stratum": "uniform", "reader": "r4", "third_order": ["T3-020"],
             "outcome": "agrees"}])
        _w(outdir, "transmission-after-revision-B4.md", "Definition: Jaccard on sets. Uniform stratum 1.0, "
           "adjudicated stratum 0.5, by family G01 and G02; alpha 0.6 against the stability floor 0.7. "
           "Unanimous items placed elsewhere: none. The gold figure was lower.\n" + LICENCE +
           "This is transmission after revision, not reliability.\n")


def _plant_outside_scheme(outdir, root):
    _fixture(outdir, root, "build")
    _wj(outdir, "assign_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-099"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"}])
    _wj(outdir, "disagreements.jsonl", [])


def _plant_gold_survived(outdir, root):
    _fixture(outdir, root, "build")
    _wj(outdir, "assign_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole",
         "agent": "a001", "replicate": 1}])


def _plant_ruling_differs(outdir, root):
    _fixture(outdir, root, "build")
    _wj(outdir, "assign_final.jsonl", [
        {"sub": "denmark", "theme_id": "t07", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"},
        {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"], "confidence": "clear", "read": "whole"}])


def _plant_ruling_without_support(outdir, root):
    """J, 2026-10-11: a ruling that names no concepts."""
    _fixture(outdir, root, "build")
    rows = [json.loads(l) for l in open(os.path.join(outdir, "disagreements.jsonl"))]
    for r in rows:
        r.pop("support_by_theme", None)
    _wj(outdir, "disagreements.jsonl", rows)


def _plant_outcome(outdir, root):
    _fixture(outdir, root, "check")
    rows = jsonl(os.path.join(outdir, "reassign.jsonl"))
    rows[1]["outcome"] = "split"
    _wj(outdir, "reassign.jsonl", rows)


def _plant_unanimous_on_adjudicated(outdir, root):
    _fixture(outdir, root, "check")
    rows = jsonl(os.path.join(outdir, "reassign.jsonl"))
    rows[1]["outcome"] = "disagrees-unanimous"
    _wj(outdir, "reassign.jsonl", rows)


PLANTED = [
    ("build: ruling without concepts", _plant_ruling_without_support, "names no support_by_theme"),
    ("build: id outside the frozen scheme", _plant_outside_scheme, "outside the frozen scheme"),
    ("build: gold placement survived", _plant_gold_survived, "seeded gold placement that survived the drop"),
    ("build: standing line vs ruling", _plant_ruling_differs, "standing placement is the ruling"),
    ("check: outcome outside the four", _plant_outcome, "not one of agrees, disagrees-contested"),
    ("check: unanimous on a ruled item", _plant_unanimous_on_adjudicated, "that item was contested, not unanimous"),
]
