"""checks/stage_C2.py: the close-check of stage C2, the loop, v38.

Written from stages/STAGE-C2-model-the-loop.md (its Outputs block, sections 1 to 6, its Close
section), SCHEMA-adaptations.md section 1 (the element and arrow lines), FLEET.md (the fleet
legs) and the v37 check it descends from (_v37-source/tools/validate.py, stage07 and
_edges_common). It checks the SHAPE of the stage's files: existence, parse, ids that resolve,
counts that reconcile. It cannot check whether a judgement is right.

The stage runs one leg per pass, so this check is run at the close of every pass. The pass count
is the number of lines in saturation.jsonl; the stopping rule (a guide: two quiet passes, a
declared stop from the third pass on) is a rule on stopping, not on the pass at hand, so a run
with fewer than three passes is reported and not failed. The reviewer's files (RETURN-C2.md, the packet, the run_manifest entry) are
checked when RETURN-C2.md is present, the build leg; review-C2.md and the reader's return are
checked when _fleet_raw/C2/DONE is present, the check leg.

Ported from v37 under the v38 names: chunks.jsonl -> fourth/fourth.jsonl (T4- ids, the C1 fields
plus changed, mistaken_for, in_model, pass); dimensions.jsonl one line per dimension with members
(the v38 target won over v37's one line per theme); edges.jsonl -> model/arrows.jsonl (A ids,
from/to are P/K/C/R ids, in_model needs mechanism_fails_if, sampled_against and an instance,
negative_check never silent); story-pN.md -> model/story-pN.md naming arrows as [A03]; the
rooms per story (fifteen a guide, warned below it); the three verdicts; the criterion paragraph; the reviewer's instruction
in review-C2.md; the run_manifest entry for the reviewer.

Not carried: data_structure.md (the generated _views/data-structure, rule 15); chunks_log.jsonl
and dimensions_log.jsonl (tier_history.jsonl carries the old line as `was`); edges_dimension.jsonl
(the dimension projection is prose in model.md's apparatus); the [S03->S07] arrow form (arrows
have ids now); the chunk-count print against the scheme size; the fork_comparison file.

Fields the stage file does not give, checked for existence and parse only: saturation.jsonl (the
line carries the story's number, the rooms and the three counts, under no fixed keys; the three
count names are looked for in the line's text); story_rooms-pN.jsonl beyond sub and verdict (the
residue clause and the drawing rule are looked for under loose keys and warned about);
concept.md (its three quotes are not marked in a form this can find); the reviewer's return
line (its error kinds are checked only where a list under `errors` carries `kind`).
"""
import collections, glob, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

KINDS = {"P": "process", "K": "condition", "C": "claim", "R": "role"}
ELEMENT_STATUS = ("standing", "bounded", "withdrawn", "candidate", "tentative")
ARROW_KINDS = ("order", "transition", "co-occurrence")
STRENGTHS = ("strong", "fair", "thin")
NEGATIVE = ("tested-absent", "counterexample", "not-addressed")
FOUND = ("holds", "fails", "not testable")
CONSTRUCT = ("borrowed", "adapted", "coined")
STORY_VERDICTS = ("told", "told-with-residue", "not-told")
WARRANTS = ("entailed", "read", "inferred")
FINDING_STATUS = ("standing", "bounded", "withdrawn")
# Grodal, Anteby and Holm's eight moves (METHOD.md): a move name is accepted when it carries one
# of these stems, so `merging`, `merge`, `relating or contrasting`, `dropping a hypothesis` pass.
MOVE_STEMS = ("question", "puzzle", "drop", "merg", "split", "relat", "contrast", "sequenc", "hypothes")
ERROR_KINDS = ("quote", "contradiction", "count", "loop", "order")
PACKET_CEILING = 50 * 1024
FLEET_DONE = os.path.join("_fleet_raw", "C2", "DONE")


# ---- helpers shared with stages C3 and C5 (they import these) --------------------------------

def move_ok(m):
    m = str(m or "").lower()
    return any(s in m for s in MOVE_STEMS)


def latest_pass_file(outdir, base, npass):
    """The newest version of a per-pass file: base-pN.md for the highest N present (N <= npass
    when npass is known), else base.md. Returns (name or None)."""
    top = npass if npass else 99
    for p in range(top, 1, -1):
        n = "%s-p%d.md" % (base, p)
        if os.path.exists(os.path.join(outdir, n)):
            return n
    return "%s.md" % base if os.path.exists(os.path.join(outdir, "%s.md" % base)) else None


def frame_or_analysed(stage, what, outdir, ctx):
    """The analysed set when stage A1's dropped.jsonl is there, else the frame; None having said
    so when the store holds no rooms."""
    fr = vlib.frame(stage, what, ctx)
    if fr is None:
        return None
    dropped = jsonl(os.path.join(outdir, "dropped.jsonl"))
    if dropped is None:
        warn("stage %s: dropped.jsonl is not in the output directory; %s was checked against the "
             "frame and not the analysed set" % (stage, what))
        return fr
    return fr - {x["sub"] for x in dropped if x.get("sub")}


def fourth_ids(outdir):
    rows = jsonl(os.path.join(outdir, "fourth", "fourth.jsonl")) or []
    return {r.get("id") for r in rows if r.get("id")}, rows


def dimension_ids(outdir):
    rows = jsonl(os.path.join(outdir, "dimensions.jsonl")) or []
    return {r.get("id") for r in rows if r.get("id")}, rows


def finding_ids(outdir):
    rows = jsonl(os.path.join(outdir, "findings.jsonl")) or []
    return {r.get("id") for r in rows if r.get("id")}, rows


def check_findings(outdir, stage):
    """findings.jsonl (rule 14): ids, warrant, status, why when the status changed, supersedes
    resolving to an earlier id."""
    ids, rows = finding_ids(outdir)
    name = "findings.jsonl"
    for r in rows:
        fid = r.get("id")
        if not fid or not vlib.FINDING.match(str(fid)):
            err("%s: id %r is not of the form F-031 (rule 14); give every finding an id"
                % (name, fid), shape="findings:id", where=str(fid))
            continue
        if r.get("warrant") not in WARRANTS:
            err("%s %s: warrant %r is not entailed|read|inferred" % (name, fid, r.get("warrant")),
                shape="findings:warrant", where=fid)
        if r.get("status") not in FINDING_STATUS:
            err("%s %s: status %r is not standing|bounded|withdrawn" % (name, fid, r.get("status")),
                shape="findings:status", where=fid)
        if not r.get("statement"):
            err("%s %s has no statement" % (name, fid), shape="findings:statement", where=fid)
        if r.get("status") in ("bounded", "withdrawn") and not r.get("why"):
            err("%s %s is %s and says nothing under why; why is required whenever the status changes "
                "(rule 14)" % (name, fid, r.get("status")), shape="findings:why", where=fid)
        sup = r.get("supersedes")
        if sup:
            sid = str(sup).split("@")[0]
            if sid not in ids:
                err("%s %s supersedes %r, an id the file does not carry" % (name, fid, sup),
                    shape="findings:supersedes", where=fid)
    return ids


def check_tier_history(outdir, stage, t3, t4, dims):
    """tier_history.jsonl lines for this stage: a move, a tier, an id that resolves, and for a
    recut of the fourth or dimension tier the old line as `was` (stage C2 section 2)."""
    rows = jsonl(os.path.join(outdir, "tier_history.jsonl")) or []
    mine = [r for r in rows if str(r.get("stage")) == stage or str(r.get("leg", "")).startswith(stage)]
    for r in mine:
        where = str(r.get("id") or r.get("theme") or r.get("t") or "")
        if not move_ok(r.get("move")):
            err("tier_history.jsonl (stage %s) line %r: move %r is not one of Grodal, Anteby and Holm's "
                "eight (rule 11)" % (stage, where, r.get("move")), shape="tier_history:move", where=where)
        if r.get("event") in ("split", "merged", "retired", "rescoped", "moved_to_rare") and not str(r.get("prompted_by") or "").strip():
            err("tier_history.jsonl (stage %s) line %r: a %s carries no `prompted_by`; a consequential move is "
                "recorded as what prompted it, the move, what changed and why (stage B1 section 6)"
                % (stage, where, r.get("event")), shape="tier_history:prompted_by", where=where)
        tier = str(r.get("tier") or "").lower()
        if tier in ("fourth", "dimension") and "was" not in r:
            warn("tier_history.jsonl (stage %s) recut %r at the %s tier carries no `was`; the superseded "
                 "line travels there since the tier file is edited in place" % (stage, where, tier),
                 shape="tier_history:was", where=where)
    return mine


def check_history(outdir, stage, elements, arrows, require_all=True):
    """model/history.jsonl: every line carries a move and a leg and names an element or arrow that
    exists; every element and arrow has at least one line, since entering the model is a change.
    Returns the lines."""
    p = os.path.join(outdir, "model", "history.jsonl")
    rows = jsonl(p)
    if rows is None:
        err("model/history.jsonl was not written; every change to an element or arrow is a line "
            "there with its move and the harness's stamp")
        return []
    touched = set()
    for i, r in enumerate(rows, 1):
        tid = r.get("id") or r.get("element") or r.get("arrow") or r.get("target")
        if not tid:
            err("model/history.jsonl line %d names no element or arrow (id, element or arrow)" % i,
                shape="history:target", where="line %d" % i)
        elif tid not in elements and tid not in arrows:
            err("model/history.jsonl line %d names %r, which neither elements.jsonl nor arrows.jsonl "
                "carries; ids are never reused and a withdrawn id stays in the file" % (i, tid),
                shape="history:unresolved", where=str(tid))
        else:
            touched.add(tid)
        if not move_ok(r.get("move")):
            err("model/history.jsonl line %d: move %r is not one of Grodal, Anteby and Holm's eight"
                % (i, r.get("move")), shape="history:move", where="line %d" % i)
        if not (r.get("leg") or r.get("stage")):
            err("model/history.jsonl line %d carries no leg; the harness's stamp names the leg"
                % i, shape="history:leg", where="line %d" % i)
    if require_all:
        for x in sorted((set(elements) | set(arrows)) - touched):
            err("model/history.jsonl has no line for %s; entering the model is a change, and every "
                "change is a line with its move" % x, shape="history:missing", where=x)
    return rows


def check_elements(outdir, ctx, t3, t4, dims, findings, form_ids, stage):
    """model/elements.jsonl (SCHEMA-adaptations section 1, stage C2 section 4). Returns the ids."""
    p = os.path.join(outdir, "model", "elements.jsonl")
    rows = jsonl(p)
    if rows is None:
        err("model/elements.jsonl was not written; the model is elements and arrows with ids")
        return set(), []
    codes = vlib.store_codes(ctx)
    ids, out = collections.Counter(), set()
    for r in rows:
        eid = str(r.get("id") or "")
        ids[eid] += 1
        if not vlib.ELEMENT.match(eid):
            err("elements.jsonl id %r is not of the form P07, K04, C02 or R01" % eid,
                shape="elements:id", where=eid)
            continue
        out.add(eid)
        if r.get("kind") != KINDS[eid[0]]:
            err("elements.jsonl %s: kind %r does not match its prefix (%s)" % (eid, r.get("kind"), KINDS[eid[0]]),
                shape="elements:kind", where=eid)
        if not r.get("statement"):
            err("elements.jsonl %s has no statement" % eid, shape="elements:statement", where=eid)
        if r.get("status") not in ELEMENT_STATUS:
            err("elements.jsonl %s: status %r is not standing|bounded|withdrawn|candidate|tentative"
                % (eid, r.get("status")), shape="elements:status", where=eid)
        if (r.get("status") == "tentative") != (r.get("origin") == "from-field"):
            err("elements.jsonl %s: tentative is the status of an entry from the field, and only of one (origin "
                "from-field, stage C4)" % eid, shape="elements:tentative", where=eid)
        if not r.get("since"):
            err("elements.jsonl %s carries no since (the leg it entered)" % eid, shape="elements:since", where=eid)
        tier = r.get("tier")
        tiers = tier if isinstance(tier, list) else [tier]
        for t in tiers:
            if t is None or t == "":
                err("elements.jsonl %s carries no tier; every element names the third-order theme, "
                    "fourth-order theme, dimension or FP- finding it belongs to" % eid,
                    shape="elements:tier", where=eid)
            elif not (t in t3 or t in t4 or t in dims or t in form_ids):
                err("elements.jsonl %s: tier %r resolves to no third-order theme in the scheme, no "
                    "fourth-order theme in fourth/fourth.jsonl, no dimension in dimensions.jsonl and "
                    "no FP- id in form_pass-C1.md" % (eid, t), shape="elements:tier-unresolved", where=eid)
        d = r.get("dimension")
        for dd in (d if isinstance(d, list) else ([d] if d else [])):
            if dd not in dims:
                err("elements.jsonl %s: dimension %r is not in dimensions.jsonl" % (eid, dd),
                    shape="elements:dimension", where=eid)
        ev = r.get("evidence") or {}
        if not isinstance(ev, dict):
            err("elements.jsonl %s: evidence is not an object with findings and codes" % eid,
                shape="elements:evidence", where=eid)
            ev = {}
        for f in ev.get("findings") or []:
            if f not in findings:
                err("elements.jsonl %s cites finding %r, which findings.jsonl does not carry" % (eid, f),
                    shape="elements:finding", where=eid)
        for c in ev.get("codes") or []:
            parts = str(c).split(":", 1)
            if len(parts) != 2 or (parts[0], parts[1]) not in codes:
                err("elements.jsonl %s cites code %r, which does not resolve to the store (sub:code_id "
                    "of a code in store/codes.jsonl)" % (eid, c), shape="elements:code", where=eid)
        if "range" not in r:
            warn("elements.jsonl %s carries no range; every element has one (stage C2 section 4)" % eid,
                 shape="elements:range", where=eid)
        if r.get("status") == "bounded" and not (r.get("bound") or r.get("bounded_by")):
            warn("elements.jsonl %s is bounded and names no condition that bounds it" % eid,
                 shape="elements:bound", where=eid)
    for eid, n in ids.items():
        if n > 1:
            err("elements.jsonl carries id %s %d times; ids are never reused" % (eid, n))
    return out, rows


def check_arrows(outdir, root, ctx, elements, rooms, stage, name="model/arrows.jsonl"):
    """model/arrows.jsonl (stage C2 section 4): the v37 _edges_common checks under the v38 names,
    plus the ends, the sampled rooms, the support quotes and the onset contrast. Returns
    (ids, rows)."""
    p = os.path.join(outdir, name)
    rows = jsonl(p)
    if rows is None:
        err("%s was not written; the model is elements and arrows with ids" % name)
        return set(), []
    codes = vlib.store_codes(ctx)
    ids, out, quotes = collections.Counter(), set(), []
    for r in rows:
        aid = str(r.get("id") or "")
        ids[aid] += 1
        if not vlib.ARROW.match(aid):
            err("%s id %r is not of the form A03" % (name, aid), shape="arrows:id", where=aid)
            continue
        out.add(aid)
        for end in ("from", "to"):
            e = r.get(end)
            if e not in elements:
                err("%s %s: %s %r is not an element id in model/elements.jsonl" % (name, aid, end, e),
                    shape="arrows:end", where=aid)
        if r.get("kind") not in ARROW_KINDS:
            err("%s %s: kind %r is not order|transition|co-occurrence" % (name, aid, r.get("kind")),
                shape="arrows:kind", where=aid)
        if not r.get("grounding"):
            err("%s %s carries no grounding (coder-dated, coder-stated, codes-read, ledger, "
                "reading-alone, or yours named)" % (name, aid), shape="arrows:grounding", where=aid)
        if r.get("negative_check") not in NEGATIVE:
            err("%s %s: negative_check must be one of tested-absent|counterexample|not-addressed, "
                "never silent" % (name, aid), shape="arrows:negative_check", where=aid)
        if not r.get("status"):
            err("%s %s carries no status" % (name, aid), shape="arrows:status", where=aid)
        if not r.get("since"):
            err("%s %s carries no since" % (name, aid), shape="arrows:since", where=aid)
        sa = r.get("sampled_against") or []
        for s in sa:
            if not isinstance(s, dict):
                continue
            if s.get("found") not in FOUND:
                err("%s %s: sampled_against %r found %r is not holds|fails|not testable"
                    % (name, aid, s.get("sub"), s.get("found")), shape="arrows:sampled-found", where=aid)
            if rooms is not None and s.get("sub") not in rooms:
                err("%s %s: sampled_against room %r is not in the analysed set" % (name, aid, s.get("sub")),
                    shape="arrows:sampled-room", where=aid)
        fails = [s.get("sub") for s in sa if isinstance(s, dict) and s.get("found") == "fails"]
        if fails and not r.get("bound") and r.get("status") != "withdrawn" and not r.get("counterexample_response"):
            err("%s %s fails in %s and carries no bound or counterexample_response; rule 16 requires "
                "a reasoned response: local adaptation, refinement, scope condition, uncertainty or withdrawal"
                % (name, aid, ", ".join(map(str, fails))), shape="arrows:fails-unbound", where=aid)
        for s in r.get("subs") or []:
            if rooms is not None and s not in rooms:
                err("%s %s: subs names %r, not in the analysed set" % (name, aid, s),
                    shape="arrows:subs", where=aid)
        sup = [s for s in (r.get("support") or []) if isinstance(s, dict) and s.get("quote")]
        tr = [s for s in (r.get("support_transition") or []) if isinstance(s, dict) and s.get("items")]
        for s in sup:
            quotes.append(s["quote"])
            if s.get("sub") and s.get("code") and (s["sub"], s["code"]) not in codes:
                err("%s %s: support cites %s:%s, which is not a code in the store" % (name, aid, s["sub"], s["code"]),
                    shape="arrows:support-code", where=aid)
        for s in tr:
            if rooms is not None and s.get("sub") not in rooms:
                err("%s %s: support_transition room %r is not in the analysed set" % (name, aid, s.get("sub")),
                    shape="arrows:transition-room", where=aid)
            if len(s.get("items") or []) < 2:
                err("%s %s: support_transition names fewer than two items; a transition is two coded "
                    "turns in one thread, in order" % (name, aid), shape="arrows:transition-items", where=aid)
        if r.get("in_model"):
            if not r.get("mechanism"):
                err("%s %s is in the model with no mechanism; an arrow with a count and no mechanism "
                    "is a correlation, in_model false" % (name, aid), shape="arrows:mechanism", where=aid)
            if not r.get("mechanism_fails_if"):
                err("%s %s is in the model with no mechanism_fails_if; an arrow without it is not an "
                    "arrow" % (name, aid), shape="arrows:mechanism_fails_if", where=aid)
            tentative = r.get("status") == "tentative" and r.get("origin") == "from-field"
            if not sa and not tentative:     # a field entry is tested by every room at stage D, not before
                err("%s %s is in the model and was sampled against no room" % (name, aid),
                    shape="arrows:sampled-against-nothing", where=aid)
            if not sup and not tr and not tentative:
                err("%s %s is in the model with neither support (a quote through cite.py) nor "
                    "support_transition (two coded turns in one thread); an arrow with neither is "
                    "in_model false whatever its count (stage C2 section 4)" % (name, aid),
                    shape="arrows:no-instance", where=aid)
            if r.get("strength") not in STRENGTHS:
                err("%s %s: strength %r is not strong|fair|thin" % (name, aid, r.get("strength")),
                    shape="arrows:strength", where=aid)
            if r.get("strength") == "strong":
                el = r.get("early_late")
                if not (isinstance(el, dict) and "early" in el and "late" in el):
                    err("%s %s is strong and carries no early_late {early, late}; the onset contrast "
                        "is carried to every strong arrow" % (name, aid), shape="arrows:early_late", where=aid)
            mfp = r.get("mechanism_failure_present")
            if mfp not in (True, False, "true", "false", "not-addressed"):
                err("%s %s: mechanism_failure_present %r is not true|false|not-addressed"
                    % (name, aid, mfp), shape="arrows:mechanism_failure_present", where=aid)
    for aid, n in ids.items():
        if n > 1:
            err("%s carries id %s %d times; ids are never reused" % (name, aid, n))
    if quotes:
        vlib.cites_resolve(outdir, root, quotes, "%s support" % name)
    return out, rows


def check_fourth(outdir, t3, stage, need_07_fields=True):
    """fourth/fourth.jsonl: T4- ids, stage C1's fields, stage C2's gains, members resolving to the
    scheme. Returns (ids, rows)."""
    p = os.path.join(outdir, "fourth", "fourth.jsonl")
    rows = jsonl(p)
    if rows is None:
        err("fourth/fourth.jsonl was not written; the fourth-order tier cut at C1 is recut here in place")
        return set(), []
    ids, out, members = collections.Counter(), set(), []
    for r in rows:
        tid = str(r.get("id") or "")
        ids[tid] += 1
        if not vlib.T4.match(tid):
            err("fourth/fourth.jsonl id %r is not of the form T4-003" % tid, shape="fourth:id", where=tid)
            continue
        out.add(tid)
        if r.get("declared") not in CONSTRUCT:
            err("fourth/fourth.jsonl %s: declared %r is not borrowed|adapted|coined; a fourth-order theme "
                "is a construct from the moment it is cut" % (tid, r.get("declared")), shape="fourth:declared", where=tid)
        for k in ("name", "gloss", "disconfirm", "prose"):
            if not r.get(k):
                err("fourth/fourth.jsonl %s: %s is empty (a fourth-order theme with no prose is a heading)"
                    % (tid, k), shape="fourth:%s" % k, where=tid)
        if r.get("declared") in ("borrowed", "adapted") and not r.get("source"):
            err("fourth/fourth.jsonl %s is %s and names no source" % (tid, r.get("declared")),
                shape="fourth:source", where=tid)
        if need_07_fields:
            for k in ("changed", "mistaken_for", "in_model", "pass"):
                if k not in r:
                    err("fourth/fourth.jsonl %s gains %s at stage C2 and does not carry it" % (tid, k),
                        shape="fourth:07-field:%s" % k, where=tid)
        ms = r.get("members") or []
        if not ms:
            err("fourth/fourth.jsonl %s has no members" % tid, shape="fourth:members", where=tid)
        for m in ms:
            members.append(m)
            if t3 is not None and m not in t3:
                err("fourth/fourth.jsonl %s names member %r, which the scheme does not define" % (tid, m),
                    shape="fourth:member-unresolved", where=tid)
    for tid, n in ids.items():
        if n > 1:
            err("fourth/fourth.jsonl carries id %s %d times" % (tid, n))
    dup = sorted(m for m, n in collections.Counter(members).items() if n > 1)
    if dup:
        err("fourth/fourth.jsonl places third-order themes in more than one fourth-order theme: %s; the fourth-order "
            "themes partition the third-order tier (stage C1 section 8)" % ", ".join(dup), shape="fourth:overlap")
    return out, rows


def check_dimensions(outdir, t4rows, stage):
    """dimensions.jsonl: one line per dimension, members resolving to fourth/fourth.jsonl, the
    construct block; every fourth-order theme gathered or carrying "dimension": []. Returns
    (ids, rows)."""
    p = os.path.join(outdir, "dimensions.jsonl")
    rows = jsonl(p)
    if rows is None:
        err("dimensions.jsonl was not written; where none was built, the file says so with the "
            "partitions tried (contract section 2)")
        return set(), []
    t4 = {r.get("id") for r in t4rows}
    ids, out, gathered = collections.Counter(), set(), collections.defaultdict(list)
    for r in rows:
        did = str(r.get("id") or "")
        ids[did] += 1
        if not vlib.DIM.match(did):
            err("dimensions.jsonl id %r is not of the form D01" % did, shape="dimensions:id", where=did)
            continue
        out.add(did)
        if not r.get("label"):
            err("dimensions.jsonl %s has no label" % did, shape="dimensions:label", where=did)
        ms = r.get("members") or []
        if len(ms) < 2:
            err("dimensions.jsonl %s gathers %d fourth-order theme(s); a dimension gathers two or more"
                % (did, len(ms)), shape="dimensions:members", where=did)
        for m in ms:
            gathered[m].append(did)
            if m not in t4:
                err("dimensions.jsonl %s names member %r, which fourth/fourth.jsonl does not carry" % (did, m),
                    shape="dimensions:member-unresolved", where=did)
        cb = r.get("construct") or {}
        if cb.get("status") not in CONSTRUCT:
            err("dimensions.jsonl %s carries no construct block with a status in borrowed|adapted|coined"
                % did, shape="dimensions:construct", where=did)
        for k in ("mistaken_for", "disconfirm_elsewhere", "gloss"):
            if not cb.get(k):
                err("dimensions.jsonl %s: construct.%s is empty" % (did, k), shape="dimensions:construct-%s" % k, where=did)
        if cb.get("status") in ("borrowed", "adapted") and not cb.get("source"):
            err("dimensions.jsonl %s is %s and names no source" % (did, cb.get("status")),
                shape="dimensions:source", where=did)
        if cb.get("status") == "adapted" and not cb.get("changed"):
            err("dimensions.jsonl %s is adapted and says nothing under construct.changed" % did,
                shape="dimensions:changed", where=did)
        if not r.get("question"):
            err("dimensions.jsonl %s carries no question (what it answers that no member answers alone)"
                % did, shape="dimensions:question", where=did)
        if r.get("confidence") not in ("clear", "arguable"):
            err("dimensions.jsonl %s: confidence %r is not clear|arguable" % (did, r.get("confidence")),
                shape="dimensions:confidence", where=did)
    for did, n in ids.items():
        if n > 1:
            err("dimensions.jsonl carries id %s %d times" % (did, n))
    for r in t4rows:
        tid = r.get("id")
        if not tid:
            continue
        own = r.get("dimension")
        if tid in gathered:
            if own is not None and own != [] and set(own if isinstance(own, list) else [own]) != set(gathered[tid]):
                err("fourth/fourth.jsonl %s says dimension %r but dimensions.jsonl gathers it under %s"
                    % (tid, own, ", ".join(gathered[tid])), shape="fourth:dimension-mismatch", where=tid)
        elif own not in ([], None) and own != "":
            err("fourth/fourth.jsonl %s says dimension %r but no dimension in dimensions.jsonl gathers it"
                % (tid, own), shape="fourth:dimension-mismatch", where=tid)
        elif "dimension" not in r:
            err("fourth/fourth.jsonl %s sits in no dimension's members and does not carry \"dimension\": [] "
                "with its clause; no catch-all, but the file says so" % tid, shape="fourth:ungathered", where=tid)
    return out, rows


def check_loops(outdir, ctx):
    """A process loop is a typed, dated cycle, never a cycle inferred from code similarity."""
    rows = jsonl(os.path.join(outdir, "model", "loops.jsonl"))
    if rows is None:
        err("model/loops.jsonl is required; an empty file records no grounded process loop", shape="loops:missing")
        return
    arrows = {r.get("id"): r for r in (jsonl(os.path.join(outdir, "model", "arrows.jsonl")) or [])}
    codes = vlib.store_codes(ctx)
    seen = set()
    for row in rows:
        lid = row.get("id")
        if not re.fullmatch(r"L\d{2,}", str(lid or "")) or lid in seen:
            err("process loop needs a unique LNN id", shape="loops:id", where=str(lid))
        seen.add(lid)
        level = row.get("level")
        if level not in ("within-room", "inter-room"):
            err("process loop level must be within-room or inter-room", shape="loops:level", where=lid)
        path = row.get("arrows") or []
        if len(path) < 2 or any(a not in arrows or not arrows[a].get("in_model") for a in path):
            err("process loop must name at least two in-model arrows", shape="loops:arrows", where=lid)
        elif any(arrows[path[i]].get("to") != arrows[path[(i + 1) % len(path)]].get("from") for i in range(len(path))):
            err("process loop arrows do not form an ordered closed path", shape="loops:path", where=lid)
        events = row.get("events")
        if not isinstance(events, list) or len(events) != len(path) or any(not isinstance(e, dict) for e in events):
            err("process loop needs one dated provenance event per arrow", shape="loops:events", where=lid)
            continue
        hours, subs = [], set()
        for arrow, event in zip(path, events):
            sub, code, hour = event.get("sub"), event.get("code"), event.get("hour")
            subs.add(sub)
            if event.get("arrow") != arrow or (sub, code) not in codes or not event.get("item") or event.get("clock") != "forest-hours-since-open":
                err("process loop event must cite its arrow, room code, exact item and forest clock", shape="loops:provenance", where=lid)
            if not isinstance(hour, (int, float)) or isinstance(hour, bool) or not math.isfinite(hour) or hour < 0:
                err("process loop event requires a finite nonnegative hour", shape="loops:time", where=lid)
            else:
                hours.append(hour)
        if hours != sorted(hours):
            err("process loop dates run backwards", shape="loops:order", where=lid)
        if (level == "within-room" and len(subs) != 1) or (level == "inter-room" and len(subs) < 2):
            err("process loop provenance does not match its stated level", shape="loops:scope", where=lid)
        for field in ("mechanism", "alternative", "why_not_alternative"):
            if not str(row.get(field) or "").strip():
                err("process loop lacks %s" % field, shape="loops:warrant", where=lid)


def json_blocks(txt):
    """Objects in fenced ```json blocks of a markdown file (structure.md's exemplar lines)."""
    out = []
    for block in re.findall(r"```json\s*\n(.*?)```", txt, re.S):
        block = block.strip()
        try:
            out.append(json.loads(block))
            continue
        except ValueError:
            pass
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith("{"):
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    return out


def form_pass_ids(outdir):
    return set(re.findall(r"\bFP-\d{2,3}\b", text(outdir, "form_pass-C1.md")))


def counts_from(row, key):
    """The first value under `key` anywhere in a nested line (saturation.jsonl's three counts)."""
    if isinstance(row, dict):
        for k, v in row.items():
            if k == key and isinstance(v, (int, float)):
                return v
            got = counts_from(v, key)
            if got is not None:
                return got
    elif isinstance(row, list):
        for v in row:
            got = counts_from(v, key)
            if got is not None:
                return got
    return None


# ---- the check -------------------------------------------------------------------------------

def check(root, outdir, ctx):
    stage = "C2"
    need(outdir, "model/elements.jsonl", "model/arrows.jsonl", "model/history.jsonl",
         "fourth/fourth.jsonl", "dimensions.jsonl", "structure.md", "concept.md", "model.md",
         "within_case.md", "saturation.jsonl", "findings.jsonl", "notes-C2.md",
         "model/story-p*.md", "story_rooms-p*.jsonl")
    rooms = frame_or_analysed(stage, "the rooms arrows and stories name", outdir, ctx)
    t3, scheme_name = vlib.load_scheme(outdir)
    if t3 is None:
        err("no scheme file is in the output directory (scheme_v2.jsonl); third-order ids were NOT "
            "resolved. Stage C1 writes scheme_v2.jsonl.")
    findings = check_findings(outdir, stage)
    t4, t4rows = check_fourth(outdir, t3, stage)
    dims, dimrows = check_dimensions(outdir, t4rows, stage)
    check_tier_history(outdir, stage, t3, t4, dims)
    fps = form_pass_ids(outdir)
    elements, erows = check_elements(outdir, ctx, t3 or set(), t4, dims, findings, fps, stage)
    arrows, arows = check_arrows(outdir, root, ctx, elements, rooms, stage)
    check_loops(outdir, ctx)
    check_history(outdir, stage, elements, arrows)

    # every third-order theme placed in assignments_final sits in a fourth-order theme or in the
    # unpicked list at the foot of fourth.md
    placed, _pn = vlib.placements(outdir)
    fourth_md = text(outdir, "fourth/fourth.md") or text(outdir, "fourth.md")
    members = {m for r in t4rows for m in (r.get("members") or [])}
    if placed:
        used = {t for v in placed.values() for t in v}
        for t in sorted(used - members):
            if t not in fourth_md:
                err("third-order theme %s is placed in assignments_final.jsonl, sits in no fourth-order "
                    "theme's members and is not listed at the foot of fourth.md; every unpicked theme "
                    "is listed there with one clause" % t, shape="fourth:unpicked-unlisted", where=t)

    # the passes: saturation.jsonl, one line per pass; each pass its story and its rooms
    sat = jsonl(os.path.join(outdir, "saturation.jsonl")) or []
    if not sat:
        err("saturation.jsonl is empty; one line per pass of the loop with the story's number, the "
            "rooms and the three counts (stage C2 section 5)")
    npass = len(sat)
    prev = None
    for i, s in enumerate(sat, 1):
        dumped = json.dumps(s)
        if not all(k in dumped for k in ("told", "not-told", "told-with-residue")):
            err("saturation.jsonl line %d does not carry the three counts (told, told-with-residue, "
                "not-told) by name" % i, shape="saturation:counts", where="line %d" % i)
        twr = counts_from(s, "told-with-residue")
        if prev is not None and twr is not None and twr > prev:
            warn("saturation.jsonl: told-with-residue rose from %s to %s at pass %d; a rise is a stopping "
                 "failure and the residues are the next pass's material" % (prev, twr, i))
        prev = twr if twr is not None else prev
    if 0 < npass < 3:
        print("  %d pass(es) so far; a declared stop comes from the third pass on (stage C2 section 1)" % npass)
    floor = min(15, len(rooms)) if rooms is not None else 15
    for p in range(1, npass + 1):
        sp = os.path.join(outdir, "model", "story-p%d.md" % p)
        if not os.path.exists(sp):
            err("model/story-p%d.md is not written; every pass tells the story (stage C2 section 5)" % p,
                shape="story:missing", where="pass %d" % p)
        else:
            st = open(sp, encoding="utf-8").read()
            named = set(re.findall(r"\[(A\d{2})\]", st))
            if not named:
                err("model/story-p%d.md names no arrow in brackets ([A03]); the story names every arrow "
                    "it uses so that no change is checked against arrows.jsonl and not the prose" % p,
                    shape="story:no-arrow", where="pass %d" % p)
            for a in sorted(named - arrows):
                err("model/story-p%d.md names arrow [%s], which model/arrows.jsonl does not carry" % (p, a),
                    shape="story:arrow-unresolved", where=a)
        rp = os.path.join(outdir, "story_rooms-p%d.jsonl" % p)
        rows = jsonl(rp)
        if rows is None:
            err("story_rooms-p%d.jsonl is not written; the rooms read against the story are named there "
                "before any is opened" % p, shape="story_rooms:missing", where="pass %d" % p)
            continue
        subs = [r.get("sub") for r in rows if r.get("sub")]
        if not subs:
            err("story_rooms-p%d.jsonl names no room; every pass reads whole rooms against the story"
                % p, shape="story_rooms:empty", where="pass %d" % p)
        elif len(set(subs)) < floor:
            warn("story_rooms-p%d.jsonl names %d rooms; fifteen per pass is a guide, not a floor: say in "
                 "notes-C2.md why fewer served the story" % (p, len(set(subs))))
        if not any(r.get("rule") or r.get("drawn_by") or r.get("draw_rule") for r in rows):
            warn("story_rooms-p%d.jsonl carries no line saying the rule the rooms were drawn by (a `rule` "
                 "field); the rule is written there before any room is opened" % p)
        for r in rows:
            if not r.get("sub"):
                continue
            if rooms is not None and r["sub"] not in rooms:
                err("story_rooms-p%d.jsonl names %r, not in the analysed set" % (p, r["sub"]),
                    shape="story_rooms:room", where=r["sub"])
            v = r.get("verdict")
            if v not in STORY_VERDICTS:
                err("story_rooms-p%d.jsonl %s: verdict %r is not told|told-with-residue|not-told"
                    % (p, r["sub"], v), shape="story_rooms:verdict", where=r["sub"])
            elif v != "told" and not any(r.get(k) for k in ("residue", "reason", "clause", "why", "needs")):
                warn("story_rooms-p%d.jsonl %s is %s with no residue or reason clause" % (p, r["sub"], v),
                     shape="story_rooms:clause", where=r["sub"])
    for r in t4rows + dimrows:
        ps = r.get("pass")
        if isinstance(ps, int) and npass and ps > npass:
            warn("%s says pass %d but saturation.jsonl has %d pass(es)" % (r.get("id"), ps, npass),
                 shape="pass-ahead", where=str(r.get("id")))

    # structure.md (the newest pass's version): every tier id appears; exemplar lines resolve
    sname = latest_pass_file(outdir, "structure", npass)
    if sname:
        st = text(outdir, sname)
        for tid in sorted((t3 or set()) | t4 | dims):
            if tid not in st:
                err("%s does not describe %s; per third-order theme, fourth-order theme and dimension "
                    "(stage C2 section 2)" % (sname, tid), shape="structure:missing-id", where=tid)
        quotes, codes = [], vlib.store_codes(ctx)
        for ob in json_blocks(st):
            if not isinstance(ob, dict) or not ob.get("quote"):
                continue
            quotes.append(ob["quote"])
            if ob.get("sub") and ob.get("code_id") and (ob["sub"], ob["code_id"]) not in codes:
                err("%s exemplar cites %s:%s, which is not a code in the store" % (sname, ob["sub"], ob["code_id"]),
                    shape="structure:exemplar-code", where=ob["code_id"])
            if ob.get("fourth") and ob["fourth"] not in t4:
                err("%s exemplar names fourth %r, not in fourth/fourth.jsonl" % (sname, ob["fourth"]),
                    shape="structure:exemplar-fourth", where=ob["fourth"])
            if ob.get("third") and t3 and ob["third"] not in t3:
                err("%s exemplar names third %r, not in the scheme" % (sname, ob["third"]),
                    shape="structure:exemplar-third", where=ob["third"])
        if quotes:
            vlib.cites_resolve(outdir, root, quotes, "%s exemplars" % sname)

    # model.md (the newest pass's version)
    mname = latest_pass_file(outdir, "model", npass)
    if mname:
        mt = text(outdir, mname)
        low = mt.lower()
        if "ungrounded relationship" not in low:
            err("%s has no section under *ungrounded relationships*; every arrow with a count and no "
                "mechanism is listed there, and stage C5 marks what rests on them" % mname)
        if not re.search(r"looked[ -]for[ -]and[ -]not[ -]found", low):
            err("%s has no *looked-for-and-not-found* section; what was looked for and not grounded goes "
                "there, in the results (rule 8)" % mname)
        for r in arows:
            if r.get("in_model") and r.get("id") and r["id"] not in mt:
                err("%s does not show arrow %s, which is in the model" % (mname, r["id"]),
                    shape="model.md:arrow-missing", where=r["id"])
        for r in erows:
            if r.get("id") and r.get("status") == "standing" and r["id"] not in mt:
                err("%s does not show element %s, which stands in the model" % (mname, r["id"]),
                    shape="model.md:element-missing", where=r["id"])
        for a in set(re.findall(r"\bA\d{2}\b", mt)) - arrows:
            err("%s names arrow %s, which model/arrows.jsonl does not carry" % (mname, a),
                shape="model.md:arrow-unresolved", where=a)

    # within_case.md: three rooms, no theme above the second tier
    wc = text(outdir, "within_case.md")
    if wc:
        if rooms is not None:
            named = [s for s in rooms if re.search(r"\b%s\b" % re.escape(s), wc)]
            if len(named) < min(3, len(rooms)):
                err("within_case.md names %d room(s) of the analysed set; three rooms are written there "
                    "(one ordinary, one the scheme could not predict, one that stopped early)" % len(named))
        above = sorted(set(re.findall(r"\b(?:T3-\d{3}|T4-\d{3}|D\d{1,2})\b", wc)))
        if above:
            err("within_case.md uses %s; the three rooms are written from the room's concepts, forest and "
                "timeline using no theme above the second tier" % ", ".join(above[:6]))
    else:
        err("within_case.md is empty")
    if not text(outdir, "concept.md").strip():
        err("concept.md is empty; name the concept, or say the study produced a description")
    n7 = text(outdir, "notes-C2.md").lower()
    if n7 and "criterion" not in n7:
        err("notes-C2.md carries no criterion paragraph; it is written before pass 1")
    for q in glob.glob(os.path.join(outdir, "_questions", "*.md")):
        w = len(open(q, encoding="utf-8", errors="replace").read().split())
        if w > 600:
            err("_questions/%s is %d words; the ceiling is 600" % (os.path.basename(q), w),
                shape="questions:ceiling", where=os.path.basename(q))

    # the reviewer: build leg (RETURN-C2.md present) and check leg (_fleet_raw/C2/DONE present)
    if os.path.exists(os.path.join(outdir, "RETURN-C2.md")):
        rt = text(outdir, "RETURN-C2.md")
        if "confirm" not in rt.lower():
            err("RETURN-C2.md carries no line telling the reader to confirm it reached the end marker (FLEET.md)")
        if "sha256" not in rt.lower():
            err("RETURN-C2.md does not ask for the sha256 of model.md served on the return line")
        vlib.manifest_entry(outdir, stage, "the reviewer")
        pk = glob.glob(os.path.join(outdir, "_packets-C2", "*.md"))
        if not pk:
            err("RETURN-C2.md is written and _packets-C2/ holds no packet; build one, by hand and logged, "
                "under the 50 KB ceiling")
        for p in pk:
            if os.path.getsize(p) > PACKET_CEILING:
                err("_packets-C2/%s is %d bytes; the ceiling is 50 KB" % (os.path.basename(p), os.path.getsize(p)))
            pt = open(p, encoding="utf-8", errors="replace").read().lower()
            if "find errors" not in pt:
                err("_packets-C2/%s does not carry the reviewer's instruction verbatim (*Find errors: ...*)"
                    % os.path.basename(p))
    if os.path.exists(os.path.join(outdir, FLEET_DONE)):
        rv = text(outdir, "review-C2.md")
        if not rv:
            err("the reader left its file in _fleet_raw/C2/ and review-C2.md is not written; copy the "
                "validated return there under the instruction (check leg)")
        else:
            if "find errors" not in rv.lower():
                err("review-C2.md does not carry the reviewer's instruction above its return; stage C2 "
                    "section 6 serves it verbatim and copies it there")
            if not re.search(r"partition", rv, re.I):
                warn("review-C2.md names no rival partition; the reviewer is asked for one")
        if n7 and "review" not in n7:
            err("notes-C2.md does not answer the reviewer's items; every item is answered there under rule 13")
        served_ok = set()
        for base in ("model.md",) + tuple("model-p%d.md" % p for p in range(2, max(npass, 1) + 1)):
            q = os.path.join(outdir, base)
            if os.path.exists(q):
                served_ok.add(vlib.sha(q))
        rets = [p for p in glob.glob(os.path.join(outdir, "_fleet_raw", "C2", "*", "r*.jsonl"))
                if not p.endswith(".failed.txt")]
        if not rets:
            err("_fleet_raw/C2/DONE is present and no validated return (r*.jsonl) is under _fleet_raw/C2/; "
                "the dispatch exhausted its reissues, so rebuild the packet")
        for p in rets:
            rel = os.path.relpath(p, outdir)
            for r in jsonl(p) or []:
                s = str(r.get("served") or "")
                if not s:
                    err("%s: the return line carries no served (the sha256 of model.md served)" % rel,
                        shape="return:served", where=rel)
                elif served_ok and s not in served_ok:
                    err("%s: served %s... matches no model.md or model-pN.md in the output directory; the "
                        "reader was served a file no pass wrote, or the file was edited without a new pass name"
                        % (rel, s[:12]), shape="return:served-mismatch", where=rel)
                for e in r.get("errors") or []:
                    if isinstance(e, dict) and e.get("kind") not in ERROR_KINDS:
                        err("%s: error kind %r is not quote|contradiction|count|loop|order" % (rel, e.get("kind")),
                            shape="return:error-kind", where=rel)
    print("  elements %d, arrows %d (%d in the model), fourth-order themes %d, dimensions %d, passes %d, "
          "findings %d" % (len(elements), len(arrows), sum(1 for a in arows if a.get("in_model")),
                           len(t4), len(dims), npass, len(findings)))


# ---- the self-test fixture --------------------------------------------------------------------

def _w(outdir, name, content):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


ELEMENT_ROW = {"id": "P01", "kind": "process", "statement": "calling for hands at the border",
               "tier": "T3-001", "dimension": "D01", "range": "one call to a standing rota",
               "evidence": {"findings": ["F-001"], "codes": ["denmark:c0117"]},
               "since": "C2-pass-1", "status": "standing"}
ARROW_ROW = {"id": "A01", "from": "P01", "to": "K01", "kind": "order", "grounding": "codes-read",
             "grounding_note": "the call precedes the defence in the forest", "in_model": True,
             "sampled_against": [{"sub": "asoiaf", "why_chosen": "a border room", "found": "holds"}],
             "strength": "fair", "subs": ["denmark"], "mechanism": "a call brings placers to the border",
             "mechanism_fails_if": "the border holds with no call", "mechanism_failure_present": "false",
             "negative_check": "tested-absent", "base_rate_beaten": None, "bound": None,
             "support": [{"sub": "denmark", "code": "c0117", "quote": "we need more people at the border"}],
             "support_transition": [], "gloss": "call then hold", "since": "C2-pass-1", "status": "standing"}


def base(outdir, root):
    """A minimal stage C2 run that passes: two third-order themes, one fourth-order theme, one
    dimension, two elements, one arrow, one pass with its story and rooms."""
    _wj(outdir, "scheme_v2.jsonl", [{"id": "T3-001", "label": "calling for hands"},
                                    {"id": "T3-002", "label": "holding the border"}])
    _wj(outdir, "dropped.jsonl", [])
    _wj(outdir, "assignments_final.jsonl", [{"sub": "denmark", "theme_id": "t07", "third_order": ["T3-001"]},
                                            {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-002"]}])
    _wj(outdir, "findings.jsonl", [{"id": "F-001", "stage": "C2", "leg": "C2-pass-1", "statement": "calls precede holds",
                                    "tier": "T3-001", "warrant": "read", "evidence": ["denmark:c0117"],
                                    "bound": None, "refuted_by": "a hold with no call", "status": "standing"}])
    _wj(outdir, "fourth/fourth.jsonl", [{"id": "T4-001", "name": "border work", "gloss": "calling and holding",
                                         "declared": "coined", "source": None, "disconfirm": "a room with no border",
                                         "members": ["T3-001"], "prose": "what a border makes a room do",
                                         "changed": None, "mistaken_for": "defence", "in_model": True, "pass": 1,
                                         "dimension": ["D01"]},
                                        {"id": "T4-002", "name": "counting", "gloss": "counting placers",
                                         "declared": "coined", "source": None, "disconfirm": "no counts",
                                         "members": ["T3-002"], "prose": "rooms count what they have",
                                         "changed": None, "mistaken_for": "audit", "in_model": False, "pass": 1,
                                         "dimension": ["D01"]}])
    _wj(outdir, "dimensions.jsonl", [{"id": "D01", "label": "the border", "members": ["T4-001", "T4-002"],
                                      "construct": {"status": "coined", "source": None, "changed": None,
                                                    "mistaken_for": "territory", "disconfirm_elsewhere": "no borders",
                                                    "gloss": "what a border asks of a room"},
                                      "question": "why rooms call for hands", "confidence": "clear", "pass": 1}])
    _wj(outdir, "model/elements.jsonl", [dict(ELEMENT_ROW),
                                         {"id": "K01", "kind": "condition", "statement": "the border is contested",
                                          "tier": "T4-001", "dimension": "D01", "range": "quiet to attacked",
                                          "evidence": {"findings": [], "codes": ["asoiaf:c0011"]},
                                          "since": "C2-pass-1", "status": "standing"}])
    _wj(outdir, "model/arrows.jsonl", [dict(ARROW_ROW)])
    _wj(outdir, "model/loops.jsonl", [])
    _wj(outdir, "model/history.jsonl", [{"id": "P01", "move": "asking questions", "leg": "C2-pass-1", "why": "entered"},
                                        {"id": "K01", "move": "asking questions", "leg": "C2-pass-1", "why": "entered"},
                                        {"id": "A01", "move": "sequencing", "leg": "C2-pass-1", "why": "entered"}])
    _wj(outdir, "saturation.jsonl", [{"pass": 1, "story": "story-p1", "rooms": 3,
                                      "counts": {"told": 2, "told-with-residue": 1, "not-told": 0}}])
    _w(outdir, "model/story-p1.md", "The rooms called for hands and then held the line [A01].\n")
    _wj(outdir, "story_rooms-p1.jsonl", [{"rule": "the three within-case rooms, every time"},
                                         {"sub": "denmark", "verdict": "told"},
                                         {"sub": "asoiaf", "verdict": "told"},
                                         {"sub": "sweden", "verdict": "told-with-residue", "residue": "no call"}])
    _w(outdir, "structure.md", "# structure\n\nT3-001 calling for hands. T3-002 holding the border. T4-001 border work. "
       "T4-002 counting. D01 the border.\n\n```json\n"
       + json.dumps({"fourth": "T4-001", "third": "T3-001", "sub": "denmark", "code_id": "c0117",
                     "quote": "we need more people at the border", "position": "core"}) + "\n```\n")
    _w(outdir, "concept.md", "# concept\n\nThe open call: not yet.\n")
    _w(outdir, "model.md", "# model\n\nP01 calls; K01 the border; A01 runs from P01 to K01.\n\n"
       "## ungrounded relationships\n\nnone yet.\n\n## looked-for-and-not-found\n\nreward talk.\n")
    _w(outdir, "within_case.md", "# within case\n\n## denmark\n\nordinary.\n\n## asoiaf\n\nunpredicted.\n\n## sweden\n\nstopped early.\n")
    _w(outdir, "notes-C2.md", "# notes\n\nThe criterion: a later pass is preferred when it tells sweden.\n")


def _plant_arrow_end(outdir, root):
    base(outdir, root)
    a = dict(ARROW_ROW); a["to"] = "K09"
    _wj(outdir, "model/arrows.jsonl", [a])


def _plant_element_code(outdir, root):
    base(outdir, root)
    e = dict(ELEMENT_ROW); e["evidence"] = {"findings": ["F-001"], "codes": ["denmark:c9999"]}
    _wj(outdir, "model/elements.jsonl", [e, {"id": "K01", "kind": "condition", "statement": "the border is contested",
                                             "tier": "T4-001", "dimension": "D01", "range": "quiet to attacked",
                                             "evidence": {"findings": [], "codes": []}, "since": "C2-pass-1",
                                             "status": "standing"}])


def _plant_story_arrow(outdir, root):
    base(outdir, root)
    _w(outdir, "model/story-p1.md", "The rooms called for hands and then held the line [A07].\n")


def _plant_no_instance(outdir, root):
    base(outdir, root)
    a = dict(ARROW_ROW); a["support"] = []
    _wj(outdir, "model/arrows.jsonl", [a])


def _plant_tentative_unmarked(outdir, root):
    base(outdir, root)
    a = dict(ARROW_ROW); a["support"] = []; a["status"] = "tentative"
    _wj(outdir, "model/arrows.jsonl", [a])


def _plant_reviewer(outdir, root):
    base(outdir, root)
    _w(outdir, os.path.join("_fleet_raw", "C2", "DONE"), "1 packet\n")
    _wj(outdir, os.path.join("_fleet_raw", "C2", "p1", "r1.jsonl"),
        [{"served": "0" * 64, "errors": [{"kind": "quote", "where": "A01", "what": "does not show order"}],
          "partition": [{"label": "border", "members": ["T3-001", "T3-002"], "holds": "the border"}]}])
    _w(outdir, "review-C2.md", "Find errors: ... propose one partition ...\n\n(the return)\n")
    _w(outdir, "notes-C2.md", "# notes\n\nThe criterion: a later pass is preferred when it tells sweden.\n\n"
       "## review\n\nquote error fixed.\n")


PLANTED = [
    ("arrow end unresolved", _plant_arrow_end, "is not an element id"),
    ("element code unresolved", _plant_element_code, "does not resolve to the store"),
    ("story names unknown arrow", _plant_story_arrow, "which model/arrows.jsonl does not carry"),
    ("in-model arrow no instance", _plant_no_instance, "in_model false whatever its count"),
    ("reviewer served mismatch", _plant_reviewer, "matches no model.md"),
    ("a tentative arrow not from the field", _plant_tentative_unmarked, "in_model false whatever its count"),
]
