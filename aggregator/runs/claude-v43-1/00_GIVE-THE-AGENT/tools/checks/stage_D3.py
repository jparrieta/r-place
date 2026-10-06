"""checks/stage_D3.py: the close-check of stage D3, adjudication by element, v38.

Written from stages/STAGE-D3-adaptation-adjudication.md (its Outputs block, §1 by element, §2
corrections met twice, §3 the unattached lines, §4 the verdicts and the uncomposed rooms, §5
the re-check, §6 the close), SCHEMA-adaptations.md §1, §6, §7 and §10, contract rules 12, 14
and 16, and from the v37 check it descends from (_v37-source/tools/validate.py, stage10: one
verdict per room of the analysed set, every does-not-compose read by name in uncomposed-D.md
with a kind from the three, the findings warning, and the §7 counts computed here and last).
What it checks is the SHAPE of the adjudication: every ledger line has a decision from the
five and none is left pending, a modify carries a portable revised text, every pair and change
resolves, a correction met twice has its history line, the model's ids and statuses hold, the
model is frozen as one version whose hash is in RUN.json, the re-check handoff exists when the
model was rewritten, and the verdict counts are computed last. It cannot check whether a ruling
is right.

    def check(root, outdir, ctx): ...

Definitions this module fixes where the stage file gives none:
- The model hash is vlib.model_hash (the elements, the arrows, the fourth-order themes, the
  dimensions, scheme_v2 and assignments_final); RUN.json must carry it, bare or sha256:-prefixed,
  anywhere in its text.
- A model rewrite at D3 is any history.jsonl line whose leg or stage starts with D3 (a field entry's
  ruling out of tentative aside), any
  adjudication with decision modify, or any element with since D3; when one exists, the
  re-check handoff (handoff-D/recheck/ with VERSION, VOCABULARY.json, MODEL.md and at least
  one task) and adaptations-recheck.jsonl are required, and the re-check rooms are named in
  notes-D3.md. Every ledger line is re-lifted (ingest.py D --relift) before this close, and the
  close and stage D4 both check it.
- The last decision written for an adaptation is its decision (mem.py adjudicate appends).
- The kind of a does-not-compose room is read from the ruling line's `kind` when it carries
  one, else from the block of uncomposed-D.md that names the room.

Not carried from v37's stage10: author_compositions.jsonl, composition_brief.md,
composition_raw.jsonl, composition.jsonl's read_by (verdicts-D.jsonl carries ruled_by on the
rulings only), transmission-D.md's licence sentence (no fidelity figure appears at D3),
operator_draw-D.json.

The common checks in validate.py already require the diary lines and the head.
"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
from checks import stage_D1 as s10a
from checks import stage_D2 as s10b

KINDS = ("outside-the-model", "out-of-scope", "too-thin")
ADJ_KINDS = ("specification", "elaboration", "correction", "proposal", "particular", "none")
STATUSES = ("standing", "bounded", "withdrawn", "candidate", "tentative")   # tentative until D3c (check_field)
MOVE_WORDS = ("asking", "question", "puzzle", "focus", "dropping", "drop", "merging", "merge", "splitting",
              "split", "relating", "relate", "contrasting", "contrast", "sequencing", "sequence", "hypothes",
              "developing")


def last_decisions(rows):
    """adaptation id -> its last adjudication line."""
    out = {}
    for r in rows:
        if r.get("adaptation"):
            out[r["adaptation"]] = r
    return out


def is_10c(r):
    return any(str(r.get(k) or "").startswith("D3") for k in ("leg", "stage", "since"))


def room_block(txt, sub):
    """The text between the heading naming the room and the next heading."""
    parts = re.split(r"^(?=#+ )", txt, flags=re.M)
    for p in parts:
        head = p.split("\n", 1)[0]
        if re.search(r"\b%s\b" % re.escape(sub), head):
            return p
    return ""


def check_adjudications(root, outdir, ctx, ledger, history_ids):
    rows = jsonl(os.path.join(outdir, "adjudications.jsonl"))
    if rows is None:
        return {}
    N = "adjudications.jsonl"
    frame = vlib.frame("D3", "the revised text's portability", ctx) or set()
    lex = {}
    by_id = {l["id"]: l for l in ledger if l.get("id")}
    for n, r in enumerate(rows, 1):
        a = r.get("adaptation")
        w = a or "line %d" % n
        if a not in by_id:
            err("%s %s: adaptation %r is not an id in adaptations.jsonl; a ruling names a ledger line" % (N, w, a),
                shape="adj:unresolved", where=w)
            continue
        line = by_id[a]
        d = r.get("decision")
        if d not in vlib.DECISIONS:
            err("%s %s: decision %r is not one of %s" % (N, w, d, vlib.DECISIONS), shape="adj:decision", where=w)
        if not (r.get("reason") or "").strip():
            err("%s %s: no reason; one reason from the line's evidence and the room's material (§1)" % (N, w),
                shape="adj:reason", where=w)
        if r.get("kind") not in (None, "") and r.get("kind") not in ADJ_KINDS:
            err("%s %s: kind %r is not specification, elaboration, correction or proposal" % (N, w, r.get("kind")),
                shape="adj:kind", where=w)
        sub = line.get("sub")
        if d == "modify":
            revised = r.get("revised")
            if isinstance(revised, dict):
                if set(revised) - {"condition", "statement", "how", "kind"}:
                    err("adjudication revised object contains unsupported fields", shape="adj:revised-fields", where=w)
                rev = " ".join(str(value) for value in revised.values() if value is not None)
            else:
                rev = revised
            if not isinstance(rev, str) or not rev.strip():
                err("%s %s: modify without revised; the rewritten condition or statement goes in revised and the "
                    "original stays in the ledger (SCHEMA §6)" % (N, w), shape="adj:revised", where=w)
            else:
                if sub not in lex:
                    lex[sub] = s10b.lexicon_names(root, sub)
                hits = s10b.name_hits(rev, sub, frame, lex[sub])
                if hits:
                    err("%s %s: revised names %s; it passes the same portability check as the labeler's line" % (N, w, hits[:3]),
                        shape="adj:revised-portable", where=w)
        elif r.get("revised"):
            err("%s %s: revised on a decision that is not modify" % (N, w), shape="adj:revised-stray", where=w)
        if d == "accept" and line.get("portable") is False:
            err("%s %s: accept on a line ingest marked portable false; it is a particular by construction (rule 5, "
                "contract rule 12), or a modify with a portable revised" % (N, w), shape="adj:accept-nonportable", where=w)
        p = r.get("pair")
        if p not in (None, ""):
            if p not in by_id:
                err("%s %s: pair %r is not a ledger id" % (N, w, p), shape="adj:pair", where=w)
            elif by_id[p].get("sub") == sub:
                err("%s %s: pair %s is a line of the same room; the pair is the second room's line (SCHEMA §6)" % (N, w, p),
                    shape="adj:pair-same-room", where=w)
        c = r.get("change")
        if c not in (None, "") and history_ids is not None and c not in history_ids:
            err("%s %s: change %r is not an id in model/history.jsonl" % (N, w, c), shape="adj:change", where=w)
    return last_decisions(rows)


def check_model(outdir):
    md = os.path.join(outdir, "model")
    els = jsonl(os.path.join(md, "elements.jsonl")) or []
    seen = collections.Counter(e.get("id") for e in els)
    dup = [i for i, c in seen.items() if c > 1]
    if dup:
        err("model/elements.jsonl carries id(s) %s more than once; ids are never reused, a change is a history line" % dup[:5])
    for e in els:
        i = e.get("id") or "?"
        if e.get("status") not in STATUSES:
            err("model/elements.jsonl %s: status %r is not standing, bounded, withdrawn or candidate" % (i, e.get("status")),
                shape="model:status", where=i)
        if e.get("status") == "bounded":
            conds = e.get("bounded_by") or e.get("conditions") or e.get("bounds")
            if not conds:
                err("model/elements.jsonl %s is bounded and carries no condition ids (bounded_by); a restrict met twice "
                    "bounds the element with the condition ids (§2)" % i, shape="model:bounded", where=i)
        if e.get("status") == "candidate" and not str(e.get("since") or "").startswith("D3"):
            err("model/elements.jsonl %s is a candidate without since D3; a candidate is a proposal accepted here (§3)" % i,
                shape="model:candidate", where=i)
    hist = jsonl(os.path.join(md, "history.jsonl"))
    ids = set()
    if hist is not None:
        for n, h in enumerate(hist, 1):
            if h.get("id"):
                ids.add(h["id"])
            mv = str(h.get("move") or "").lower()
            if not mv:
                err("model/history.jsonl line %d has no move; every change names one of Grodal, Anteby and Holm's eight"
                    % n, shape="history:move", where="line %d" % n)
            elif not any(w in mv for w in MOVE_WORDS):
                warn("model/history.jsonl line %d: move %r is not one of the eight by name" % (n, h.get("move")),
                     shape="history:move-name", where="line %d" % n)
    return els, hist, ids


def check_verdicts(outdir, ctx, analysed):
    rows = jsonl(os.path.join(outdir, "verdicts-D.jsonl")) or []
    themes = vlib.store_themes(ctx) if vlib.rooms(ctx) else None
    readers = collections.defaultdict(list)
    ruled = {}
    N = "verdicts-D.jsonl"
    for r in rows:
        sub = r.get("sub")
        if not sub:
            continue
        if r.get("ruled_by") == "analyst":
            if "changed_from" not in r:
                err("%s: the ruling on r/%s carries no changed_from (the readers' verdicts)" % (N, sub),
                    shape="ruling:changed_from", where=sub)
            if not (r.get("reason") or "").strip():
                err("%s: the ruling on r/%s has no reason (§4)" % (N, sub), shape="ruling:reason", where=sub)
            s10b.verdict_line(r, N, "ruling %s" % sub, themes, sub)
            if r.get("verdict") == "does-not-compose" and r.get("kind") not in (None, "") and r.get("kind") not in KINDS:
                err("%s: the ruling on r/%s names kind %r, not one of %s" % (N, sub, r.get("kind"), KINDS),
                    shape="ruling:kind", where=sub)
            ruled[sub] = r
        elif r.get("ruled_by"):
            err("%s: r/%s ruled_by %r; the readers are not judges, and a ruling is the analyst's (rule 13)" % (N, sub, r.get("ruled_by")),
                shape="ruling:by", where=sub)
        else:
            for e in (r.get("readers") if isinstance(r.get("readers"), list) else [r]):
                if isinstance(e, dict):
                    readers[sub].append(e)
    final, split = {}, []
    for sub in set(readers) | set(ruled):
        vs = {e.get("verdict") for e in readers.get(sub, [])}
        if sub in ruled:
            final[sub] = ruled[sub]
        elif len(vs) == 1:
            final[sub] = readers[sub][0]
        else:
            split.append(sub)
    if split:
        err("%s: %d room(s) whose readers differ have no ruling with ruled_by analyst: %s; the split verdicts are ruled "
            "with the criterion in front of you (§4)" % (N, len(split), sorted(split)[:6]))
    if analysed is not None:
        miss = sorted(analysed - set(final) - set(split))
        if miss:
            err("%s: no verdict for %d rooms of the analysed set: %s" % (N, len(miss), miss[:6]))
        stray = sorted(set(final) - analysed)
        if stray:
            err("%s names rooms outside the analysed set: %s" % (N, stray[:6]))
    return final


def check_recheck(outdir, ledger, decisions, els, hist):
    field = {r.get("id") for r in (jsonl(os.path.join(outdir, "sealed", "FIELD.jsonl")) or [])}
    # a field entry ruled out of tentative is not a rewrite of the model; everything else at D3 is
    rewritten = any(is_10c(h) and h.get("changed", True) and (h.get("id") or h.get("element")) not in field for h in (hist or [])) \
        or any(e.get("status") == "candidate" for e in els)
    # a modify ruling rewords a labeler's line, not the model; only a rewritten element sends rooms back (§5)
    R = os.path.join(outdir, "handoff-D", "recheck")
    if not rewritten:
        if os.path.isdir(R):
            warn("handoff-D/recheck/ exists while no history line, modify or candidate shows a rewrite")
        return
    for f in ("VERSION", "VOCABULARY.json", "MODEL.md"):
        if not os.path.exists(os.path.join(R, f)):
            err("the model was rewritten at D3 and handoff-D/recheck/%s is missing; handoff.py D --recheck builds the "
                "re-check handoff with the revised vocabulary, VERSION and model (§5)" % f, shape="recheck:%s" % f)
    tasks = {os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(R, "tasks", "*", "TASK.md"))}
    root = os.path.dirname(os.path.abspath(outdir))
    template = os.path.join(root, "handoff", "RETURN-D.md")
    revised = os.path.exists(template) and "local_status:" in open(template, encoding="utf-8").read()
    if revised:
        scope_path = os.path.join(outdir, "recheck-scope.json")
        try:
            scope = json.load(open(scope_path, encoding="utf-8"))
        except (OSError, ValueError):
            scope = {}
            err("recheck-scope.json is required: enumerate affected rooms and give reasons for every unaffected room")
        universe = {r.get("sub") for r in (jsonl(os.path.join(root, "package", "store", "rooms.jsonl")) or [])}
        universe -= {r.get("sub") for r in (jsonl(os.path.join(outdir, "dropped.jsonl")) or [])}
        affected = set(scope.get("affected_rooms") or [])
        unaffected = scope.get("unaffected_rooms") or {}
        if not isinstance(unaffected, dict):
            unaffected = {}
            err("recheck-scope.json unaffected_rooms must map each room to its reason")
        if affected & set(unaffected) or affected | set(unaffected) != universe:
            err("recheck-scope.json must account for every analysed room exactly once")
        if any(not str(v).strip() for v in unaffected.values()) or not scope.get("reason"):
            err("recheck-scope.json requires a reason for scope and for every unaffected room")
        if not affected <= tasks:
            err("recheck tasks omit affected rooms: %s; a pilot does not validate all affected cases" % sorted(affected - tasks)[:8])
        for sub in tasks:
            p = os.path.join(outdir, "rooms", sub, "model-D-recheck.md")
            if not os.path.isfile(p) or not re.search(r"local_status:\s*(validated|unresolved|insufficient-evidence)\b", open(p, encoding="utf-8").read()):
                err("r/%s has no checked local account for the revised model" % sub)
    if not tasks:
        err("handoff-D/recheck/tasks/ holds no task; affected rooms must return through their case leads (§5)")
    rv = s10a.read_version(outdir, "recheck")
    mh = s10a.model_hash(outdir)
    if rv and mh and rv != mh:          # acting on what the re-check found moves the model again; say so
        (err if revised else warn)("the model moved after the re-check was built (recheck/VERSION %s..., now %s...); say in notes-D3.md what "
             "moved and why" % (rv[:12], mh[:12]))
    ar = jsonl(os.path.join(outdir, "adaptations-recheck.jsonl"))
    if ar is None:
        err("adaptations-recheck.jsonl was not written; ingest compiles it from DROPS/D/recheck/ (§5)")
    else:
        from adaptation_ledger import effective_rooms
        selected_ids = {item for record in effective_rooms(outdir).values() if record.get("phase") == "recheck"
                        for item in record.get("ids", [])}
        ar = [row for row in ar if row.get("id") in selected_ids]
        for r in ar:
            w = r.get("id") or "?"
            if r.get("sub") not in tasks:
                err("adaptations-recheck.jsonl %s: r/%s is not a re-check task" % (w, r.get("sub")), shape="recheck:room", where=w)
            if rv and s10a.bare_hash(str(r.get("model_version") or "")) != rv:
                err("adaptations-recheck.jsonl %s: model_version is not recheck/VERSION" % w, shape="recheck:version", where=w)
    vr = jsonl(os.path.join(outdir, "verdicts-recheck-D.jsonl"))
    if vr is None:
        warn("verdicts-recheck-D.jsonl was not written: the verdict fleet's re-check (_fleet_raw/D3v/) has not "
             "returned or was not compiled; both verdict lines stand, with the version on each (§5)")
    else:
        got = {r.get("sub") for r in vr}
        for t in sorted(set(tasks) - got):
            warn("verdicts-recheck-D.jsonl has no line for re-check room r/%s; say why in notes-D3.md" % t)
        for r in vr:
            for e in r.get("readers") or []:
                if rv and s10a.bare_hash(str(e.get("model_version") or "")) != rv:
                    err("verdicts-recheck-D.jsonl r/%s reader %s: model_version is not recheck/VERSION"
                        % (r.get("sub"), e.get("reader")), shape="recheck:verdict-version", where=str(r.get("sub")))
    s10a.scan_canvas(outdir, (os.path.join("handoff-D", "recheck"),), "D3")
    notes = text(outdir, "notes-D3.md")
    unnamed = sorted(t for t in tasks if not re.search(r"\b%s\b" % re.escape(t), notes))
    if unnamed:
        err("notes-D3.md does not name re-check room(s) %s, with why, and whether the rewrite fixed what the evidence "
            "pointed at (§5)" % unnamed[:5])


def check_field(outdir):
    """The field's entries (§4, J 2026-09-29): every id in out/sealed/FIELD.jsonl is ruled out of tentative by the
    freeze and reported apart in notes-D3.md under `The field's entries`."""
    field = jsonl(os.path.join(outdir, "sealed", "FIELD.jsonl")) or []
    ids = [r.get("id") for r in field if r.get("id")]
    if not ids:
        return
    notes = text(outdir, "notes-D3.md")
    m = re.search(r"^#+\s*The field's entries\s*$(.*?)(?=^#|\Z)", notes, re.M | re.S | re.I)
    if not m:
        err("notes-D3.md has no heading `The field's entries`; the %d tentative entries from stage C4 are reported "
            "apart (§4)" % len(ids), shape="field:section")
    else:
        missing = [i for i in ids if not re.search(r"\b%s\b" % re.escape(i), m.group(1))]
        if missing:
            err("notes-D3.md, The field's entries, does not report %s" % ", ".join(missing[:5]), shape="field:unreported")
    still = [r.get("id") for f in ("model/elements.jsonl", "model/arrows.jsonl")
             for r in (jsonl(os.path.join(outdir, f)) or []) if r.get("status") == "tentative"]
    if still:
        err("%s still tentative at the close; each field entry becomes standing, bounded or withdrawn (§4)"
            % ", ".join(still[:5]), shape="field:tentative")


def check(root, outdir, ctx):
    stage = "D3"
    step = vlib.current_step(root)
    if step in ("D3a", "D3b"):   # an element group, or the re-check: what is ruled so far is well formed;
        need(outdir, "adjudications.jsonl", "adaptations.jsonl", "verdicts-D.jsonl", "notes-D3.md",
             "model/elements.jsonl", "model/history.jsonl")        # the close's demands wait for D3c (§6)
        ledger = (jsonl(os.path.join(outdir, "adaptations.jsonl")) or []) + (jsonl(os.path.join(outdir, "adaptations-recheck.jsonl")) or [])
        els, hist, hids = check_model(outdir)
        decisions = check_adjudications(root, outdir, ctx, ledger, hids if hist is not None else None)
        if step == "D3b":
            check_recheck(outdir, ledger, decisions, els, hist)
        print("  %s: %d of %d ledger lines ruled; the close's checks run at D3c" % (step, len(decisions), len(ledger)))
        return
    need(outdir, "adjudications.jsonl", "adaptations.jsonl", "verdicts-D.jsonl", "uncomposed-D.md",
         "exception-report-D.md", "notes-D3.md", "handback-D3.md", "model/elements.jsonl", "model/history.jsonl")
    check_field(outdir)
    got = vlib.analysed_set(stage, "the verdicts against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    ledger = (jsonl(os.path.join(outdir, "adaptations.jsonl")) or []) + (jsonl(os.path.join(outdir, "adaptations-recheck.jsonl")) or [])
    els, hist, hids = check_model(outdir)
    decisions = check_adjudications(root, outdir, ctx, ledger, hids if hist is not None else None)
    by_id = {l["id"]: l for l in ledger if l.get("id")}
    # every line ruled, none pending at the close
    from adaptation_ledger import effective_rooms
    selected_ids = {item for record in effective_rooms(outdir).values() for item in record.get("ids", [])}
    unruled = sorted(i for i in by_id if i in selected_ids and i not in decisions)
    if unruled:
        err("%d ledger line(s) have no adjudication: %s. Every line is accepted, modified, rejected or a particular "
            "before the close (§6)" % (len(unruled), unruled[:6]))
    pending = sorted(i for i, d in decisions.items() if i in selected_ids and d.get("decision") == "pending")
    if pending:
        from adaptation_ledger import effective_rooms
        returns = effective_rooms(outdir)
        inconsistent = [i for i in pending if returns.get(by_id.get(i, {}).get("sub"), {}).get("local_status") == "validated"]
        if inconsistent:
            err("pending adaptations conflict with a validated local account: %s" % inconsistent[:6], shape="pending:local-status")
        warn("%d pending adaptations remain unresolved, excluded from asserted local or shared support" % len(pending))
    # corrections met twice have their history line (rule 12, §2)
    final_kind = {}
    for i, d in decisions.items():
        l = by_id.get(i)
        if not l:
            continue
        final_kind[i] = d.get("kind") or l.get("kind")
    met = collections.defaultdict(set)
    for i, d in decisions.items():
        l = by_id.get(i)
        if not l or d.get("decision") not in ("accept", "modify") or final_kind.get(i) != "correction":
            continue
        lift = l.get("lift") or [None] * 4
        for lvl in (1, 2):
            if len(lift) > lvl and lift[lvl]:
                met[(l.get("element"), lift[lvl])].add(i)
    hist_blob = json.dumps(hist or [])
    for (el, node), ids in met.items():
        if len({by_id[i]["sub"] for i in ids}) < 2:
            continue
        if not any(i in hist_blob for i in ids):
            err("corrections met twice on %s at %s (%s) with no model/history.jsonl line citing them; two rooms are the "
                "trigger and your written reason is the warrant, in the same leg (rule 12, §2)" % (el, node, sorted(ids)[:4]),
                shape="met-twice", where="%s %s" % (el, node))
    # accepted proposals became candidate elements
    acc_prop = [i for i, d in decisions.items() if d.get("decision") == "accept" and by_id.get(i, {}).get("op") == "propose"]
    if acc_prop and not any(e.get("status") == "candidate" for e in els):
        err("%d propose line(s) accepted (%s) and model/elements.jsonl holds no candidate element; an accepted proposal "
            "becomes an element with status candidate, since D3 (§3)" % (len(acc_prop), acc_prop[:4]))
    # the verdicts, the uncomposed rooms
    final = check_verdicts(outdir, ctx, analysed)
    unc = text(outdir, "uncomposed-D.md")
    dnc = sorted(s for s, r in final.items() if r.get("verdict") == "does-not-compose")
    kinds = collections.Counter()
    for s in dnc:
        blk = room_block(unc, s)
        if not blk and s not in unc:
            err("uncomposed-D.md does not read r/%s, a does-not-compose room, by name: what it did, what the model would "
                "need, whether it should have it, and the condition (§4)" % s, shape="uncomposed:missing", where=s)
            continue
        k = final[s].get("kind") if final[s].get("kind") in KINDS else next((k for k in KINDS if k in (blk or unc)), None)
        if k is None:
            err("uncomposed-D.md names r/%s without its kind from the three (outside-the-model, out-of-scope, too-thin)" % s,
                shape="uncomposed:kind", where=s)
        kinds[k] += 1
    find = jsonl(os.path.join(outdir, "findings.jsonl"))
    if find is not None and dnc and not any(is_10c(f) for f in find):
        warn("findings.jsonl carries no D3 line while %d rooms do not compose; a room that does not compose requires re-examining the "
             "finding it touches, and is written beside it (§4, rule 16)" % len(dnc))
    jsonl(os.path.join(outdir, "tier_history.jsonl"))  # named by the stage file without fields: parse only
    # the exception report, and its sentence
    rep = text(outdir, "exception-report-D.md")
    dec_of = {i: d.get("decision") for i, d in decisions.items()}
    per_room = collections.defaultdict(list)
    for i, l in by_id.items():
        if l.get("op") != "none":
            per_room[l["sub"]].append(dec_of.get(i))
    all_part = sorted(s for s, ds in per_room.items() if ds and all(d == "particular" for d in ds))
    for s in all_part:
        if not re.search(r"\b%s\b" % re.escape(s), rep):
            err("exception-report-D.md does not name r/%s, whose adaptations are all particulars (SCHEMA §7)" % s,
                shape="report:room", where=s)
    n_lines = sum(len(v) for v in per_room.values())
    n_part = sum(1 for v in per_room.values() for d in v if d == "particular")
    if n_lines and n_part == n_lines and "has not composed" not in rep:
        err("every adaptation is a particular and exception-report-D.md does not say, in the contract's words, that a "
            "model whose adaptations are all particulars has not composed (rule 12, §6)")
    for w in ("particular", "prior"):
        if rep and w not in rep.lower():
            err("exception-report-D.md does not report the %s share against prior.md's numbers (§6)"
                % ("particulars" if w == "particular" else "composition criteria"), shape="report:%s" % w)
    # the model frozen as one version
    mh = s10a.model_hash(outdir)
    rp = os.path.join(root, "RUN.json")
    if not os.path.exists(rp):
        err("RUN.json is not in the folder root; the model's hash at the close goes into it (§6)")
    elif mh and mh not in open(rp, encoding="utf-8", errors="replace").read():
        err("RUN.json does not carry the hash of model/ as it stands (%s...); the model at the close is frozen as one "
            "version and hashed, and every ledger line is re-lifted to it before stage D4 (§6)" % mh[:12])
    check_recheck(outdir, ledger, decisions, els, hist)
    # the ledger re-lifted to the model as it stands (§6), before stage D4 measures anything
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import ingest
    stale = ingest.relift_problems(os.path.dirname(ctx["package"]), outdir)
    if stale:
        err("%d ledger line(s) carry a lift the placements no longer give (%s ...); re-lift before the close: "
            "python3 tools/ingest.py D --relift (§6)" % (len(stale), stale[:4]), shape="ledger:relift")
    # the counts, last (§6; v37 §7 ported)
    dist = collections.Counter(r.get("verdict") for r in final.values())
    under = collections.Counter(r.get("cannot_tell_under") for r in final.values() if r.get("verdict") == "cannot-tell")
    dcount = collections.Counter(dec_of.values())
    print("  D3 decisions over %d lines: %s" % (len(by_id), dict(dcount)))
    print("  D3 verdicts over %d rooms: %s" % (len(final), dict(dist)))
    print("  D3 does-not-compose by kind: %s" % dict(kinds))
    print("  D3 cannot-tell under: %s" % dict(under))
    stories = s10a.last_story(outdir)
    verdict = {s: r.get("verdict") for s, r in final.items()}
    if stories:
        last = jsonl(stories[-1]) or []
        read_any = set()
        for s in stories:
            read_any |= {r.get("sub") for r in (jsonl(s) or [])}
        miss = [r.get("sub") for r in last if r.get("verdict") == "not-told"]
        told = [r.get("sub") for r in last if r.get("verdict") == "told"]
        print("  D3 the last story's %d not-told rooms now: %s" % (len(miss), dict(collections.Counter(verdict.get(s) for s in miss))))
        print("  D3 the last story's %d told rooms now: %s (a told room that does not compose is the measure of how "
              "well the loop prepared)" % (len(told), dict(collections.Counter(verdict.get(s) for s in told))))
        composed = lambda v: v in ("composes", "composes-with-residue")
        ra = [s for s in verdict if s in read_any]
        nr = [s for s in verdict if s not in read_any]
        rate = lambda xs: (round(sum(1 for s in xs if composed(verdict[s])) / len(xs), 3) if xs else None)
        print("  D3 composition rate, rooms read against a story at C2: %s over %d; never read: %s over %d"
              % (rate(ra), len(ra), rate(nr), len(nr)))
    else:
        warn("no story_rooms-pN.jsonl in the output directory, so the story figures of §6 were not computed")


# ---- the self-test ------------------------------------------------------------------------------

_w, _wj = s10a._w, s10a._wj


def plant_base(out, root):
    s10b.plant_base(out, root)
    _wj(os.path.join(out, "diary", "D3-1.jsonl"), [{"stage": "D3", "text": "ruled"}])
    _wj(os.path.join(out, "adjudications.jsonl"), [
        {"adaptation": "denmark-001", "decision": "accept", "kind": "elaboration", "reason": "stated without the room", "pair": None, "change": None, "leg": "D3-P07"},
        {"adaptation": "denmark-002", "decision": "accept", "kind": None, "reason": "absent is ordinary", "pair": None, "change": None, "leg": "D3-K04"},
        {"adaptation": "asoiaf-001", "decision": "particular", "kind": None, "reason": "one room", "pair": None, "change": None, "leg": "D3-K04"}])
    _w(os.path.join(out, "uncomposed-D.md"), "# uncomposed\n\nnone.\n")
    _w(os.path.join(out, "exception-report-D.md"), "# exceptions\n\nasoiaf: 1 particular against 0 shared lines.\n"
                                                    "particulars 1 of 3 against prior.md's share.\n")
    _w(os.path.join(out, "notes-D3.md"), "counts read.\n")
    _w(os.path.join(out, "handback-D3.md"), "nothing\n")
    ver = s10a.model_hash(out)
    _w(os.path.join(root, "RUN.json"), json.dumps({"stage_D2": {"accepted": 2, "reissued": 0, "unreturned": 0},
                                                    "model_10c": "sha256:" + ver}))


def _plant_bad_adaptation(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adjudications.jsonl"))
    rows[0]["adaptation"] = "denmark-099"
    _wj(os.path.join(out, "adjudications.jsonl"), rows)


def _plant_modify_no_revised(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adjudications.jsonl"))
    rows[0]["decision"] = "modify"
    _wj(os.path.join(out, "adjudications.jsonl"), rows)


def _plant_pending(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adjudications.jsonl"))
    rows[2]["decision"] = "pending"
    ledger = jsonl(os.path.join(out, "adaptations.jsonl")) or []
    sub = next(r["sub"] for r in ledger if r["id"] == rows[2]["adaptation"])
    _wj(os.path.join(out, "adaptation-returns.jsonl"), [{"sub": sub, "phase": "initial", "status": "accepted",
        "model_version": vlib.model_hash(out), "ids": [r["id"] for r in ledger if r["sub"] == sub],
        "local_status": "validated", "local_grade": "composes"}])
    _wj(os.path.join(out, "adjudications.jsonl"), rows)


def _plant_unfrozen(out, root):
    plant_base(out, root)
    _w(os.path.join(root, "RUN.json"), json.dumps({"stage_D2": {"accepted": 2, "reissued": 0, "unreturned": 0}}))


def _plant_split_unruled(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "verdicts-D.jsonl"))
    for r in rows:
        if r["sub"] == "asoiaf" and r["reader"] == "r2":
            r["verdict"] = "does-not-compose"
    _wj(os.path.join(out, "verdicts-D.jsonl"), rows)


def _plant_recheck_missing(out, root):
    plant_base(out, root)
    hist = jsonl(os.path.join(out, "model", "history.jsonl")) or []
    hist.append({"id": "P01", "leg": "D3a-01", "move": "rewritten: the call names both borders", "why": "two rooms"})
    _wj(os.path.join(out, "model", "history.jsonl"), hist)


def _plant_field_unreported(out, root):
    plant_base(out, root)
    _wj(os.path.join(out, "sealed", "FIELD.jsonl"), [{"id": "A09", "kind": "order", "origin": "from-field"}])


PLANTED = [
    ("a field entry not reported apart", _plant_field_unreported, "The field's entries"),
    ("an adaptation id that does not resolve", _plant_bad_adaptation, "is not an id in adaptations.jsonl"),
    ("a modify without revised", _plant_modify_no_revised, "modify without revised"),
    ("pending line contradicts validated local status", _plant_pending, "pending adaptations conflict with a validated local account"),
    ("the model not frozen in RUN.json", _plant_unfrozen, "does not carry the hash of model/"),
    ("a split verdict without a ruling", _plant_split_unruled, "have no ruling with ruled_by analyst"),
    ("a rewritten element with no re-check handoff", _plant_recheck_missing, "handoff-D/recheck/VERSION is missing"),
]
