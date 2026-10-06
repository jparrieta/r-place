"""checks/stage_C5.py: the close-check of stage C5, the account, v38.

Written from stages/STAGE-C5-model-account.md (its Outputs block, sections 1 to 13, its
Close section), FLEET.md (the three legs, the 50 KB ceiling, the licence sentence) and the v37
check it descends from (_v37-source/tools/validate.py, stage09). It checks the SHAPE of the
stage's files: existence, parse, ids that resolve, counts that reconcile. It cannot check
whether the account is true or the readers independent.

The stage runs build legs (one per pass), a dispatch leg that is not the analyst's, and check
legs (one per pass). The leg is read from the files: a build leg until RETURN-C5.md exists
(then the packets, author_claims.jsonl, propositions.jsonl and the run_manifest entry are due);
a check leg when _fleet_raw/C5/DONE exists (then readers-C5/ holds the three validated returns,
notes-C5.md scores fidelity both ways with the licence sentence, and data_structure-C5.md,
figure-C5.md and implications-C5.md are due).

Ported from v37 under the v38 names: account_passes.jsonl (increasing passes, criterion_says in
prefer|reject|no change, the four fields, tier_events resolving to tier_history.jsonl or
model/history.jsonl); author_claims.jsonl five to nine; reader_round.jsonl -> readers-C5/ and
_fleet_raw/C5/ (three readers, each saying what it was served, the fourth reader's three rooms
folded into every reader's line); the run_manifest entry and its account digest where the entry
records one; propositions.md `### Pn` -> propositions.jsonl ids, every id the figure tags
defined, every defined id the figure carries warned about; an in-model arrow drawn with no
instance; every fourth-order theme in data_structure-C5.md; a stage-C5 recut carrying its move.

Not carried: reader_round.md; the second reader round; chunks_log.jsonl and
dimensions_log.jsonl; gioia_table.md (merged into data_structure-C5.md); the `P|Proposition n`
warning on account.md (propositions are numbered in their own file now); the edges.v2 fallback.

Fields the stage file does not give, checked loosely: the run_manifest entry's account digest
(read from account_sha256 or a pass block, as v37 did, when present); the reader files' names
under readers-C5/ (any *.jsonl); the data-structure table's metadata (a code id or a footnote
key is looked for in each row and warned about); sketches.md's three arrangements (headings
counted, warned about).
"""
import collections, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
try:
    from checks import stage_C2 as s7
except ImportError:
    import stage_C2 as s7

CRITERION = ("prefer", "reject", "no change")
PASS_FIELDS = ("what_changed", "tier_events", "sketches_tried", "elements_cut")
RETURN_KEYS = ("reader", "served", "claims", "relations", "could_not_follow", "unsupported", "rooms")
PROP_ID = vlib.PROPOSITION
CARRIED = ("words", "pattern", "both")   # what carries a proposition (section 6; contract section 1)
PACKET_CEILING = 50 * 1024
FLEET_DONE = os.path.join("_fleet_raw", "C5", "DONE")
HEDGES = ("tends to", "in some communities", "in some rooms")


def check_passes(outdir):
    passes = jsonl(os.path.join(outdir, "account_passes.jsonl")) or []
    if not passes:
        err("account_passes.jsonl is empty; one line per pass is how the criterion is shown to have been "
            "applied rather than asserted (stage C5 section 7)")
    nums = [p.get("pass") for p in passes]
    if nums != sorted(n for n in nums if isinstance(n, int)) or len(set(nums)) != len(nums):
        err("account_passes.jsonl pass numbers are not strictly increasing integers: %r" % (nums,))
    for p in passes:
        head = str(p.get("criterion_says") or "").split(" - ")[0].strip().lower()
        v = next((x for x in sorted(CRITERION, key=len, reverse=True) if head.startswith(x)), head)
        if v not in CRITERION:
            err("account_passes.jsonl pass %r: criterion_says starts %r, not one of prefer|reject|no change"
                % (p.get("pass"), v), shape="passes:criterion", where=str(p.get("pass")))
        for k in PASS_FIELDS:
            if k not in p:
                err("account_passes.jsonl pass %r has no %r" % (p.get("pass"), k),
                    shape="passes:field:%s" % k, where=str(p.get("pass")))
        if not p.get("leg"):
            err("account_passes.jsonl pass %r carries no leg (C5-build-2, C5-check-1)" % p.get("pass"),
                shape="passes:leg", where=str(p.get("pass")))
    claimed = [t for p in passes for t in (p.get("tier_events") or [])]
    if claimed:
        have = set()
        for name in ("tier_history.jsonl", os.path.join("model", "history.jsonl")):
            for r in jsonl(os.path.join(outdir, name)) or []:
                if r.get("id"):
                    have.add(str(r["id"]))
                if r.get("event"):
                    have.add(str(r["event"]))
        if not have:
            warn("account_passes.jsonl claims tier events and neither tier_history.jsonl nor "
                 "model/history.jsonl carries an id or event field to resolve them against")
        else:
            for t in claimed:
                if str(t) not in have:
                    err("account_passes.jsonl claims tier event %r, which neither tier_history.jsonl nor "
                        "model/history.jsonl carries" % t, shape="passes:tier-event", where=str(t))
    return passes


def check_propositions(outdir, arrows, arows, findings):
    rows = jsonl(os.path.join(outdir, "propositions.jsonl"))
    if rows is None:
        return None
    grounding = {r.get("id"): str(r.get("grounding") or "") for r in arows}
    ids = collections.Counter()
    for r in rows:
        pid = str(r.get("id") or "")
        ids[pid] += 1
        if not PROP_ID.match(pid):
            err("propositions.jsonl id %r is not of the form N12" % pid, shape="props:id", where=pid)
            continue
        if not r.get("statement"):
            err("propositions.jsonl %s has no statement" % pid, shape="props:statement", where=pid)
        ro = r.get("rests_on") or []
        if not ro:
            err("propositions.jsonl %s rests on no arrow; the figure tags its arrows with the proposition "
                "that carries them" % pid, shape="props:rests_on", where=pid)
        for a in ro:
            if a not in arrows:
                err("propositions.jsonl %s rests on %r, which model/arrows.jsonl does not carry" % (pid, a),
                    shape="props:arrow-unresolved", where=pid)
        if "theorised" not in r or not isinstance(r.get("theorised"), bool):
            err("propositions.jsonl %s does not say whether the arrows beneath it are observed or theorised "
                "(theorised true|false)" % pid, shape="props:theorised", where=pid)
        else:
            known = [a for a in ro if a in grounding]
            if known and all(grounding[a] == "reading-alone" for a in known) and r["theorised"] is False:
                err("propositions.jsonl %s rests wholly on reading-alone arrows (%s) and is marked observed; a "
                    "proposition resting wholly on theorised arrows is a conjecture and is marked so"
                    % (pid, ", ".join(known)), shape="props:theorised-wrong", where=pid)
        f = r.get("finding")
        if f and f not in findings:
            err("propositions.jsonl %s names finding %r, which findings.jsonl does not carry" % (pid, f),
                shape="props:finding", where=pid)
        if r.get("carried_by") not in CARRIED:
            err("propositions.jsonl %s does not say what carries it (carried_by words|pattern|both; section 6, "
                "contract section 1)" % pid, shape="props:carried_by", where=pid)
        if not str(r.get("rival") or "").strip():
            err("propositions.jsonl %s names no rival; the strongest other reading of the same evidence, in one "
                "clause (section 6)" % pid, shape="props:rival", where=pid)
    for pid, n in ids.items():
        if n > 1:
            err("propositions.jsonl carries id %s %d times" % (pid, n))
    return rows


def check_figure(outdir, arrows, arows, props):
    fig = text(outdir, "figure-C5.md")
    if not fig.strip():
        err("figure-C5.md is empty; the figure as text, precisely enough that someone else could draw it")
        return
    defined = {str(r.get("id")) for r in (props or []) if r.get("id")}
    tagged = set(re.findall(r"\bN\d{2,3}\b", fig))
    for u in sorted(tagged - defined):
        err("figure-C5.md tags an arrow with %s, which propositions.jsonl does not define" % u,
            shape="figure:prop-unresolved", where=u)
    unused = sorted(defined - tagged)
    if unused:
        warn("propositions.jsonl defines %s, which the figure carries no arrow for; a proposition the figure "
             "cannot draw is not wrong, but say so in notes-C5.md" % ", ".join(unused))
    drawn = set(re.findall(r"\bA\d{2}\b", fig))
    by_id = {r.get("id"): r for r in arows}
    for a in sorted(drawn):
        if a not in arrows:
            err("figure-C5.md draws %s, which model/arrows.jsonl does not carry" % a,
                shape="figure:arrow-unresolved", where=a)
            continue
        r = by_id[a]
        sup = [s for s in (r.get("support") or []) if isinstance(s, dict) and s.get("quote")]
        tr = [s for s in (r.get("support_transition") or []) if isinstance(s, dict) and s.get("items")]
        if not sup and not tr:
            err("figure-C5.md draws %s, which carries no support or support_transition; an arrow with no "
                "instance is not drawn (contract section 2)" % a, shape="figure:no-instance", where=a)
        if not r.get("in_model"):
            err("figure-C5.md draws %s, which is not in the model (in_model false)" % a,
                shape="figure:not-in-model", where=a)
    if not drawn:
        err("figure-C5.md names no arrow by id; every box and every arrow is named")
    if "theoris" not in fig.lower():
        warn("figure-C5.md does not say which drawing is with the theorised arrows and which without")
    if not re.search(r"leaves out|left out", fig, re.I):
        warn("figure-C5.md has no paragraph on what the figure leaves out (stage C5 section 10)")


def table_rows(md):
    """The rows of the first markdown table with six or more cells, minus header and rule."""
    rows = []
    for ln in md.split("\n"):
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 6:
            continue
        if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else rows


def check_data_structure(outdir, root, ctx, t3, t4, dims):
    ds = text(outdir, "data_structure-C5.md")
    if not ds.strip():
        err("data_structure-C5.md is empty; the six-column table over all five tiers is re-emitted in the last "
            "check leg from the tiers as they finally stand")
        return
    rows = table_rows(ds)
    if not rows:
        err("data_structure-C5.md carries no six-column table (representative quote, first-order concept, "
            "second-order theme, third-order theme, fourth-order theme, aggregate dimension)")
        return
    labels = {(" ".join(str(r.get("second_order") or "").split())).lower()
              for r in (jsonl(os.path.join(ctx["package"], "store", "themes.jsonl")) or [])}
    quotes = []
    for cells in rows:
        # the quoted words, when the cell quotes them; else the cell minus a trailing
        # parenthetical (the metadata) and a footnote key
        m = re.search(r"[\"“](.+?)[\"”]", cells[0])
        q = m.group(1) if m else re.sub(r"\s*\([^)]*\)\s*$", "", cells[0])
        q = re.sub(r"\s*\[\^?\w+\]\s*$", "", q)
        q = re.sub(r"^[\"'*_“]+|[\"'*_”]+$", "", q).strip()
        if not q:
            continue
        low = " ".join(q.split()).lower()
        if "label" in low or low in labels:
            continue  # the cell says it carries the coder's second-order theme label
        quotes.append(q)
        row = " ".join(cells)
        if not re.search(r"\bc\d{3,5}\b|\[\^?\w+\]", row):
            warn("data_structure-C5.md row %r carries no concept id or footnote key; every row's quote "
                 "carries its metadata" % q[:50], shape="data_structure:metadata", where=q[:40])
    vlib.cites_resolve(outdir, root, quotes, "data_structure-C5.md")
    for tid in sorted((t3 or set()) | t4 | dims):
        if tid not in ds:
            err("data_structure-C5.md does not display %s; every third-order theme, fourth-order theme and "
                "dimension appears" % tid, shape="data_structure:missing-id", where=tid)
    print("  data_structure-C5.md: %d rows, %d quotes checked" % (len(rows), len(quotes)))


def check_readers(outdir, rooms, sha_ok):
    """The three returns: validated in _fleet_raw/C5/, copied into readers-C5/."""
    raw = [p for p in glob.glob(os.path.join(outdir, "_fleet_raw", "C5", "*", "r*.jsonl"))]
    raw_sha = {vlib.sha(p) for p in raw}
    copies = sorted(glob.glob(os.path.join(outdir, "readers-C5", "*.jsonl")))
    if len(copies) < 3:
        err("readers-C5/ holds %d return(s); the three validated returns are copied there in the check leg"
            % len(copies))
    served = {}
    for p in copies:
        rel = os.path.relpath(p, outdir)
        if raw_sha and vlib.sha(p) not in raw_sha:
            err("%s does not match any validated return under _fleet_raw/C5/; the copy is byte for byte" % rel,
                shape="readers:copy", where=rel)
        for r in jsonl(p) or []:
            for k in RETURN_KEYS:
                if k not in r:
                    err("%s: the return line has no %r" % (rel, k), shape="readers:key:%s" % k, where=rel)
            s = str(r.get("served") or "")
            served[rel] = s
            if s and sha_ok and s not in sha_ok:
                err("%s: served %s... is not the account.md digest run_manifest.json records; the readers "
                    "were served a file the manifest does not name" % (rel, s[:12]), shape="readers:served", where=rel)
            cl = r.get("claims") or []
            if not (5 <= len(cl) <= 9):
                warn("%s returns %d claims; the return line asks for five to nine" % (rel, len(cl)),
                     shape="readers:claims", where=rel)
            rms = r.get("rooms") or []
            if len(rms) != 3:
                err("%s names %d rooms, not the three it was given" % (rel, len(rms)), shape="readers:rooms", where=rel)
            for x in rms:
                if not isinstance(x, dict):
                    continue
                if rooms is not None and x.get("sub") not in rooms:
                    err("%s: room %r is not in the analysed set" % (rel, x.get("sub")), shape="readers:room", where=rel)
                if not isinstance(x.get("fits"), bool):
                    err("%s: room %r carries no fits true|false" % (rel, x.get("sub")), shape="readers:fits", where=rel)
    if len({s for s in served.values() if s}) > 1:
        err("the readers in readers-C5/ report different served digests (%s); the three were served one "
            "account" % ", ".join(sorted({s[:12] for s in served.values() if s})))
    return copies


def check(root, outdir, ctx):
    stage = "C5"
    need(outdir, "account.md", "sketches.md", "account_passes.jsonl", "prose-test-C5.md", "notes-C5.md",
         "model/elements.jsonl", "model/arrows.jsonl", "model/history.jsonl", "fourth/fourth.jsonl",
         "dimensions.jsonl", "findings.jsonl")
    rooms = s7.frame_or_analysed(stage, "the rooms the readers and arrows name", outdir, ctx)
    t3, _ = vlib.load_scheme(outdir)
    if t3 is None:
        err("no scheme file is in the output directory (scheme_v2.jsonl); third-order ids were NOT resolved")
    findings = s7.check_findings(outdir, stage)
    t4, t4rows = s7.check_fourth(outdir, t3, stage)
    dims, _d = s7.check_dimensions(outdir, t4rows, stage)
    s7.check_tier_history(outdir, stage, t3, t4, dims)
    fps = s7.form_pass_ids(outdir)
    elements, erows = s7.check_elements(outdir, ctx, t3 or set(), t4, dims, findings, fps, stage)
    arrows, arows = s7.check_arrows(outdir, root, ctx, elements, rooms, stage)
    s7.check_loops(outdir, ctx)
    history = s7.check_history(outdir, stage, elements, arrows, require_all=False)
    for r in erows:
        if str(r.get("since") or "").startswith("C5"):
            err("model/elements.jsonl %s entered at %s; no new element at stage C5 (the model is fixed at its "
                "close except through D3)" % (r.get("id"), r.get("since")), shape="elements:new-at-C5", where=r.get("id"))
    status = {r.get("id"): r.get("status") for r in erows}
    passes = check_passes(outdir)
    for p in passes:
        for e in p.get("elements_cut") or []:
            if e not in elements:
                err("account_passes.jsonl pass %r cut %r, which model/elements.jsonl does not carry; a cut element "
                    "keeps its id with its status changed" % (p.get("pass"), e), shape="passes:cut-unresolved", where=str(e))
            elif status.get(e) == "standing":
                err("account_passes.jsonl pass %r cut %s and it still stands in model/elements.jsonl; a cut "
                    "element keeps its id with its status changed and a history line" % (p.get("pass"), e),
                    shape="passes:cut-standing", where=e)

    acc = text(outdir, "account.md")
    if not acc.strip():
        err("account.md is empty")
    else:
        used = set(re.findall(r"\b[PKCR]\d{2}\b", acc))
        if not used:
            err("account.md names no element by id; every claim goes through an element id and a quote or a "
                "transition (stage C5 section 1)")
        for e in sorted(used - elements):
            err("account.md names %s, which model/elements.jsonl does not carry" % e,
                shape="account:element-unresolved", where=e)
        for a in sorted(set(re.findall(r"\bA\d{2}\b", acc)) - arrows):
            err("account.md names arrow %s, which model/arrows.jsonl does not carry" % a,
                shape="account:arrow-unresolved", where=a)
        low = acc.lower()
        for h in HEDGES:
            if h in low:
                warn("account.md says %r; a claim you can only state with a hedge is two claims or none: name "
                     "the condition or take the first horn (rule 16)" % h)
    pt = text(outdir, "prose-test-C5.md")
    if pt.strip():
        for tid in sorted(t4 | dims):
            if tid not in pt:
                err("prose-test-C5.md has no sentence for %s; one per construct, in which the name does "
                    "theoretical work" % tid, shape="prose-test:missing", where=tid)
    else:
        err("prose-test-C5.md is empty")
    sk = text(outdir, "sketches.md")
    if sk and len(re.findall(r"^#{1,3}\s", sk, re.M)) < 3:
        warn("sketches.md has fewer than three headed arrangements; at least three, each with what it showed "
             "and what it hid")
    n9 = text(outdir, "notes-C5.md").lower()
    if n9 and "criterion" not in n9:
        err("notes-C5.md carries no criterion; it is written before pass 1 (stage C5 section 5)")

    props = check_propositions(outdir, arrows, arows, findings)
    build_done = os.path.exists(os.path.join(outdir, "RETURN-C5.md"))
    check_leg = os.path.exists(os.path.join(outdir, FLEET_DONE))
    sha_ok = set()
    if build_done or check_leg:
        if props is None:
            err("propositions.jsonl is not written; section 6 is written before the packets go out")
        rt = text(outdir, "RETURN-C5.md")
        for k in RETURN_KEYS:
            if k not in rt:
                err("RETURN-C5.md does not name %r on the return line" % k, shape="return:key", where=k)
        if "confirm" not in rt.lower():
            err("RETURN-C5.md carries no line telling the reader to confirm it reached the end marker (FLEET.md)")
        claims = jsonl(os.path.join(outdir, "author_claims.jsonl"))
        if claims is None:
            err("author_claims.jsonl is not written; five to nine claims, first, before the packets")
        else:
            if not (5 <= len(claims) <= 9):
                err("author_claims.jsonl has %d claims; stage C5 section 8 says five to nine" % len(claims))
            for c in claims:
                if not (c.get("id") and c.get("claim") and c.get("where")):
                    err("author_claims.jsonl line %r lacks id, claim or where" % c.get("id"),
                        shape="author_claims:fields", where=str(c.get("id")))
        ents = vlib.manifest_entry(outdir, stage, "the readers")
        if ents:
            e = ents[-1]
            rec = None
            for k in ("final", "pass5", "pass4", "pass3", "pass2", "pass1"):
                rec = (e.get(k) or {}).get("account_sha256") if isinstance(e.get(k), dict) else None
                if rec:
                    break
            rec = rec or e.get("account_sha256") or e.get("served")
            if rec:
                sha_ok.add(str(rec))
                ap = os.path.join(outdir, "account.md")
                if os.path.exists(ap) and not check_leg and vlib.sha(ap) != rec:
                    err("account.md on disk (%s...) is not the file run_manifest.json records for stage C5 "
                        "(%s...); the account was edited after the manifest was written, or the manifest names "
                        "an earlier pass" % (vlib.sha(ap)[:12], str(rec)[:12]))
            if not (e.get("model") or e.get("reader_model")):
                warn("run_manifest.json's stage-C5 entry names no model for the readers")
        pk = glob.glob(os.path.join(outdir, "_packets-C5", "*.md"))
        if len(pk) < 3:
            err("_packets-C5/ holds %d packet(s); three, one per reader, by hand and logged, under 50 KB" % len(pk))
        for p in pk:
            b = os.path.basename(p)
            if os.path.getsize(p) > PACKET_CEILING:
                err("_packets-C5/%s is %d bytes; the ceiling is 50 KB" % (b, os.path.getsize(p)))
            pt = open(p, encoding="utf-8", errors="replace").read().lower()
            if "as a stranger" not in pt:
                err("_packets-C5/%s does not carry the instruction verbatim (*Read the account as a stranger ...*)" % b,
                    shape="packets:instruction", where=b)
            if "notes-C5" in pt or "notes-C2" in pt:
                err("_packets-C5/%s names the analyst's notes; nothing of yours but the account, the figure, the "
                    "propositions and the three rooms goes to a reader" % b, shape="packets:notes", where=b)
    if check_leg:
        check_readers(outdir, rooms, sha_ok)
        if n9:
            if "fidelity" not in n9:
                err("notes-C5.md does not score fidelity both ways (the claims each reader recovered, and the "
                    "claims they recovered that you did not write)")
            vlib.licence_sentence(outdir, "notes-C5.md", "the readers' fidelity")
    step = vlib.current_step(root)
    if check_leg and step in (None, "C5d"):     # C5d's own outputs, demanded at C5d (or in the self-test)
        need(outdir, "data_structure-C5.md", "figure-C5.md", "implications-C5.md")
        check_data_structure(outdir, root, ctx, t3, t4, dims)
        check_figure(outdir, arrows, arows, props)
        imp = text(outdir, "implications-C5.md").lower()
        if imp and "work_remained" not in imp and "organizing_end_hour" not in imp:
            err("implications-C5.md says nothing on which forms keep the work alive from the record "
                "(organizing_end_hour, work_remained); contract §1 answers that clause from the record, silence "
                "included, never from the canvas (section 12)", shape="implications:work")
        if imp and "expect" not in imp:
            warn("implications-C5.md writes no expectation for stage D (which elements should instantiate in which "
                 "kinds of room, which should be absent); stage D1 writes EXPECTATIONS.jsonl from it")
    else:
        # the figure and the data structure are re-emitted in the last check leg; before it they are
        # checked when present
        if os.path.exists(os.path.join(outdir, "figure-C5.md")):
            check_figure(outdir, arrows, arows, props)
        if os.path.exists(os.path.join(outdir, "data_structure-C5.md")):
            check_data_structure(outdir, root, ctx, t3, t4, dims)
    print("  leg: %s; passes %d, propositions %d, elements %d, arrows %d, history lines %d"
          % ("check" if check_leg else ("build, packets out" if build_done else "build"),
             len(passes), len(props or []), len(elements), len(arrows), len(history)))


# ---- the self-test fixture --------------------------------------------------------------------

def base(outdir, root):
    s7.base(outdir, root)
    s7._w(outdir, "account.md", "# account\n\nWhen the border was contested (K01), the room called for hands "
          "(P01) [A01], and the call went out before the first attack.\n")
    s7._w(outdir, "sketches.md", "# sketches\n\n## by time\n\nshowed order.\n\n## by tier\n\nhid the loop.\n\n"
          "## by trajectory\n\ndenmark then asoiaf.\n")
    s7._wj(outdir, "account_passes.jsonl", [{"pass": 1, "t": "2026-09-24T00:00:00Z", "leg": "C5-build-1",
                                             "what_changed": "first draft", "tier_events": [], "sketches_tried": 3,
                                             "elements_cut": [], "criterion_says": "no change"}])
    s7._w(outdir, "prose-test-C5.md", "# prose test\n\nT4-001: because the room had border work, a call could go "
          "out. T4-002: because the room counted, it knew. D01: because the border asked, the room answered.\n")
    s7._w(outdir, "notes-C5.md", "# notes\n\nThe criterion: prefer the account that tells sweden.\n")
    s7._wj(outdir, "propositions.jsonl", [{"id": "N01", "statement": "where K01 holds, P01 starts before the first attack",
                                           "rests_on": ["A01"], "theorised": False, "finding": "F-001",
                                           "carried_by": "words", "rival": "the call came after the attack"}])


def check_base(outdir, root):
    """The check leg: RETURN-C5.md, the packets, the claims, the manifest, DONE, three returns copied,
    the figure, the data structure, the implications, fidelity scored with its licence."""
    base(outdir, root)
    s7._w(outdir, "RETURN-C5.md", "# RETURN-C5\n\n```\n{\"reader\": \"r1\", \"served\": \"<sha256 of account.md>\", "
          "\"claims\": [], \"relations\": [], \"could_not_follow\": [], \"unsupported\": \"\", \"rooms\": []}\n"
          "END-OF-RETURN\n```\n\nConfirm you reached the end marker.\n")
    for k in (1, 2, 3):
        s7._w(outdir, os.path.join("_packets-C5", "p%d.md" % k), "Read the account as a stranger. ...\n")
    s7._wj(outdir, "author_claims.jsonl", [{"id": "c%d" % i, "claim": "claim %d" % i, "where": "paragraph 1"}
                                           for i in range(1, 6)])
    acc_sha = vlib.sha(os.path.join(outdir, "account.md"))
    s7._w(outdir, "run_manifest.json", '[{"stage": "C5", "model": "opus", "seed": 1, "decoding": "t0", '
          '"readers": 3, "account_sha256": "%s"}]' % acc_sha)
    s7._w(outdir, os.path.join("_fleet_raw", "C5", "DONE"), "3 packets\n")
    line = {"reader": "r1", "served": acc_sha, "claims": ["a", "b", "c", "d", "e"], "relations": ["A01 acts on K01"],
            "could_not_follow": [], "unsupported": "",
            "rooms": [{"sub": "denmark", "fits": True, "instead": ""}, {"sub": "asoiaf", "fits": True, "instead": ""},
                      {"sub": "sweden", "fits": False, "instead": "no call went out"}]}
    for k in (1, 2, 3):
        row = dict(line); row["reader"] = "r%d" % k
        s7._wj(outdir, os.path.join("_fleet_raw", "C5", "p%d" % k, "r%d.jsonl" % k), [row])
        s7._wj(outdir, os.path.join("readers-C5", "r%d.jsonl" % k), [row])
    s7._w(outdir, "notes-C5.md", "# notes\n\nThe criterion: prefer the account that tells sweden.\n\n## fidelity\n\n"
          "Each reader recovered 4 of 5 claims. The figure bounds whether the account carries what was meant, "
          "not whether it is right.\n")
    s7._w(outdir, "figure-C5.md", "# figure\n\nK01 -> P01 [A01] N01, grounded in codes-read, instance: "
          "\"we need more people at the border\" (denmark:c0117), 1 community. Drawn once with the theorised arrows "
          "and once without. What the figure leaves out: T4-002.\n")
    s7._w(outdir, "data_structure-C5.md", "# data structure\n\n"
          "| representative quote | first-order concept | second-order theme | third-order theme | fourth-order theme | aggregate dimension |\n"
          "|---|---|---|---|---|---|\n"
          "| \"we need more people at the border\" (denmark, c0117, h10) | calling for hands | t07 | T3-001 | T4-001 | D01 |\n"
          "| \"hold the line\" (asoiaf, c0011, h20) | defending | t02 | T3-002 | T4-002 | D01 |\n")
    s7._w(outdir, "implications-C5.md", "# implications\n\nStage D should expect P01 in every border room.\n\n"
          "Keeping the work alive: rooms with a late organizing_end_hour hold P01; work_remained is silent elsewhere.\n")


def _plant_prop_arrow(outdir, root):
    base(outdir, root)
    s7._wj(outdir, "propositions.jsonl", [{"id": "N01", "statement": "where K01 holds, P01 starts first",
                                           "rests_on": ["A09"], "theorised": False, "finding": "F-001",
                                           "carried_by": "words", "rival": "the call came after the attack"}])


def _plant_prop_uncarried(outdir, root):
    base(outdir, root)
    s7._wj(outdir, "propositions.jsonl", [{"id": "N01", "statement": "where K01 holds, P01 starts first",
                                           "rests_on": ["A01"], "theorised": False, "finding": "F-001",
                                           "rival": "the call came after the attack"}])


def _plant_table_quote(outdir, root):
    check_base(outdir, root)
    s7._w(outdir, "data_structure-C5.md", "# data structure\n\n"
          "| representative quote | first-order concept | second-order theme | third-order theme | fourth-order theme | aggregate dimension |\n"
          "|---|---|---|---|---|---|\n"
          "| \"we need more people at the border\" (denmark, c0117, h10) | calling for hands | t07 | T3-001 | T4-001 | D01 |\n"
          "| \"nobody ever said this\" (asoiaf, c0011, h20) | defending | t02 | T3-002 | T4-002 | D01 |\n")


def _plant_reader_served(outdir, root):
    check_base(outdir, root)
    row = jsonl(os.path.join(outdir, "readers-C5", "r2.jsonl"))[0]
    row["served"] = "f" * 64
    s7._wj(outdir, os.path.join("readers-C5", "r2.jsonl"), [row])
    s7._wj(outdir, os.path.join("_fleet_raw", "C5", "p2", "r2.jsonl"), [row])


def _plant_new_element(outdir, root):
    base(outdir, root)
    rows = jsonl(os.path.join(outdir, "model", "elements.jsonl"))
    rows.append({"id": "R01", "kind": "role", "statement": "the template keeper", "tier": "T4-001", "dimension": "D01",
                 "range": "one to many", "evidence": {"findings": [], "codes": []}, "since": "C5-build-1", "status": "standing"})
    s7._wj(outdir, "model/elements.jsonl", rows)


def _plant_work_from_canvas(outdir, root):
    check_base(outdir, root)
    s7._w(outdir, "implications-C5.md", "# implications\n\nStage D should expect P01 in every border room. The rooms "
          "whose artwork survived on the canvas kept their work alive.\n")


PLANTED = [
    ("keeping the work alive read off the canvas", _plant_work_from_canvas, "says nothing on which forms keep the work alive"),
    ("proposition rests on unknown arrow", _plant_prop_arrow, "which model/arrows.jsonl does not carry"),
    ("proposition says not what carries it", _plant_prop_uncarried, "does not say what carries it"),
    ("table quote nobody said", _plant_table_quote, "does not resolve to a participant's words"),
    ("reader served another account", _plant_reader_served, "is not the account.md digest"),
    ("new element at C5", _plant_new_element, "no new element at stage C5"),
]
