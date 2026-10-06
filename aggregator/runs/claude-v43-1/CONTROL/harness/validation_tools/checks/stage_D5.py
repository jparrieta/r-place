"""checks/stage_D5.py: the close-check of stage D5, the branch accounts, v38.

Written from stages/STAGE-D5-forming-branch-accounts.md (its Outputs block, sections 1 to 5, its Close
section), from SCHEMA-adaptations.md sections 7 and 8, and from the v37 check it descends from
(_v37-source/tools/validate.py, stage12). What it checks is the SHAPE of the accounts: files that
exist, ids that resolve, rooms in the analysed set, counts that reconcile with verdicts-D.jsonl
and with the arrows' own datings. It cannot check whether an account is right.

The stage runs one leg per branch, then one leg for the waterfall and survival. So: at every leg,
every line of branches-D5.jsonl names a branch stage D4 cut and has its account file, and every
account file has its line; once waterfall-D5.md or survival-D5.md exists (the last leg), every
branch of branches.jsonl must be accounted and both files must exist; before that the remainder
is a warning.

What is checked:
  1. branches-D5.jsonl per line: branch resolves to branches.jsonl; n equals the branch's member
     count; verdicts keys are the four and sum to n, and agree with verdicts-D.jsonl (analyst
     ruling, else the readers where they agree); uncomposed_members are the members with verdict
     does-not-compose; binds and leaves_free are organizing problems, disjoint, binds non-empty for
     a form; over and under resolve to fourth-order themes; arrows_present, arrows_absent and
     arrows_not_testable name arrows of model/arrows.jsonl, each once, with expected equal to the
     arrow's corpus-wide subs count over the analysed set times n (rule 6); an absent arrow with
     expected below one is an error, since nothing may be written from it; propositions_* resolve
     to propositions.jsonl, each once; a failed proposition rests on at least one arrow with
     expected at or above one; survival carries median_organizing_end_hour, aftermath_share in
     [0, 1] and work_remained counts (kept, lost, silent) summing to n (reconciled to
     organizing_end-A1.jsonl where present, as a warning); canvas carries
     median_area_px, rooms_with_artwork and a read sentence; form_or_grouping is form or grouping;
     unmodelled and confidence are non-empty.
  2. forms/<id>-account.md per branch: the thirteen sections in order (by heading words); every
     unresolved member named; at least two members named (the representative members); every
     element, arrow, third- and fourth-order id and every r/<room> resolves; every citation
     [sub/code] resolves to the store; at least one citation (participants' words through cite.py).
  3. waterfall-D5.md: states its rule, names a branch and a room of the analysed set, and reads
     the walk against prior.md. survival-D5.md: names every accounted branch, reports
     organizing_end_hour and the aftermath share, and carries the contract's sentence on what
     the canvas measures.
  4. findings.jsonl and defects.jsonl exist; a stage-D5 line in neither is a warning (a branch
     may bound nothing).

Not carried from v37 stage12:
  - cluster_names-D5.md and _snap/D5-names.sha256 (names before the model): v38 names branches at
    stage D4; snaps are harness-owned per leg and read at E1 only.
  - operator_draw-D5.json: no external audit inside the v38 instrument.
  - name_defensible_from_members: superseded by the name read against the members in the account
    (item 3) and a renaming proposal in notes-D5.md, which is prose and not checked.
  - composition and canvas blocks on clusters-D5.jsonl: verdicts and canvas blocks on
    branches-D5.jsonl take their place.
"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
from checks import stage_D4 as s11

SECTIONS = [
    ("narrative", r"narrative|how these rooms organized"),
    ("what the branch does", r"what the branch does"),
    ("what it does differently", r"does differently"),
    ("the concepts it employs", r"concepts it employs"),
    ("composition here", r"composition here"),
    ("how the model runs here", r"how the model runs"),
    ("the one relationship that runs differently", r"relationship that runs differently|one relationship"),
    ("fourth-order themes over- and under-represented", r"over-? ?and under-?represented|over-represented"),
    ("arrows present, absent or not-testable-here", r"arrows present|not-testable-here"),
    ("how representative members do the work", r"representative members"),
    ("the nearest branch", r"nearest branch"),
    ("the form test", r"form test"),
    ("what would make you doubt", r"doubt"),
]
ID_PAT = re.compile(r"\b(T3-\d{3}|T4-\d{2,3}|[PKCR]\d{2}|A\d{2})\b")
ROOM_PAT = re.compile(r"\br/([A-Za-z0-9_]+)")
CITE_PAT = re.compile(r"\[([A-Za-z0-9_]+)/(c\d{3,5})\]")
TOL_ABS, TOL_REL = 0.06, 0.05


def room_verdicts(outdir):
    """verdicts-D.jsonl read per room: the analyst's ruling (ruled_by: analyst) wins, else the
    readers' verdict where they agree, else None (a split D3 has not ruled)."""
    rows = jsonl(os.path.join(outdir, "verdicts-D.jsonl"))
    if rows is None:
        return None
    by = collections.defaultdict(list)
    for r in rows:
        if r.get("sub"):
            by[r["sub"]].append(r)
    out = {}
    for sub, rs in by.items():
        ruled = [r for r in rs if str(r.get("ruled_by") or "").lower() == "analyst" or r.get("reader") == "analyst"]
        if ruled:
            out[sub] = ruled[-1].get("verdict")
            continue
        vs = set()
        for r in rs:                   # a room line with its readers (ingest.py), or one line per reader
            for e in (r.get("readers") if isinstance(r.get("readers"), list) else [r]):
                if isinstance(e, dict) and e.get("verdict"):
                    vs.add(e["verdict"])
        out[sub] = vs.pop() if len(vs) == 1 else None
    return out


def arrow_subs(outdir):
    rows = jsonl(os.path.join(outdir, "model", "arrows.jsonl"))
    if rows is None:
        return None
    return {r["id"]: set(r.get("subs") or []) for r in rows if r.get("id")}


def propositions(outdir):
    rows = jsonl(os.path.join(outdir, "propositions.jsonl"))
    if rows is None:
        return None
    return {r["id"]: r for r in rows if r.get("id")}


def last_leg(outdir):
    return os.path.exists(os.path.join(outdir, "waterfall-D5.md")) or \
        os.path.exists(os.path.join(outdir, "survival-D5.md"))


def check_line(r, i, outdir, ctx, by_id, analysed, verdicts, arrows, props, fourth):
    bid = r.get("branch")
    where = "line %d" % i
    if bid not in by_id:
        err("branches-D5.jsonl %s names branch %r that stage D4 did not cut" % (where, bid),
            shape="branches-D5.jsonl: branch unresolved", where=where)
        return None
    members = list(by_id[bid].get("members") or [])
    if analysed is not None:
        members = [m for m in members if m in analysed]
    n = r.get("n")
    if n != len(members):
        err("branches-D5.jsonl %s: n = %r but the branch has %d members in the analysed set" % (bid, n, len(members)),
            shape="branches-D5.jsonl: n disagrees with the branch", where=bid)
    if not str(r.get("name") or "").strip():
        err("branches-D5.jsonl %s: name is empty" % bid, shape="branches-D5.jsonl: no name", where=bid)
    v = r.get("verdicts")
    if not isinstance(v, dict) or set(v) - set(vlib.VERDICTS) or not all(isinstance(x, int) for x in v.values()):
        err("branches-D5.jsonl %s: verdicts is not a block of integer counts over the four verdicts" % bid,
            shape="branches-D5.jsonl: verdicts block", where=bid)
        v = {}
    elif sum(v.values()) != len(members):
        err("branches-D5.jsonl %s: the verdict counts sum to %d for %d members; every member has one verdict "
            "in verdicts-D.jsonl" % (bid, sum(v.values()), len(members)),
            shape="branches-D5.jsonl: verdicts do not sum to n", where=bid)
    unc = r.get("unresolved_members")
    if not isinstance(unc, list):
        err("branches-D5.jsonl %s: unresolved_members missing; name every unresolved adapted-local account" % bid,
            shape="branches-D5.jsonl: unresolved_members missing", where=bid)
        unc = []
    for m in unc:
        if m not in members:
            err("branches-D5.jsonl %s lists unresolved member %r that is not in the branch" % (bid, m),
                shape="branches-D5.jsonl: unresolved member outside the branch", where="%s %s" % (bid, m))
    if verdicts is not None and members:
        known = {m: verdicts.get(m) for m in members}
        unruled = sorted(m for m, x in known.items() if x is None)
        if unruled:
            warn("branches-D5.jsonl %s: verdicts-D.jsonl gives no single verdict for %s (readers split, "
                 "no analyst ruling); the counts were reconciled without them" % (bid, unruled[:5]))
        got = collections.Counter(x for x in known.values() if x)
        if v and not unruled and {k: n_ for k, n_ in v.items() if n_} != dict(got):
            err("branches-D5.jsonl %s: verdicts %s do not match verdicts-D.jsonl over the members (%s); "
                "recompute from the file" % (bid, {k: n_ for k, n_ in v.items() if n_}, dict(got)),
                shape="branches-D5.jsonl: verdicts disagree with verdicts-D.jsonl", where=bid)
    # These are historical fixed-global verdicts, not the adapted-local result.
    hand_version = text(outdir, "handoff-D/VERSION").strip().removeprefix("sha256:")
    if not hand_version or r.get("global_model_version") != hand_version:
        err("branches-D5.jsonl %s: global_model_version must identify the original handoff" % bid,
            shape="branches-D5.jsonl: global version", where=bid)
    current = vlib.model_hash(outdir)
    if not current or r.get("local_model_version") != current:
        err("branches-D5.jsonl %s: local_model_version must equal the current model hash" % bid,
            shape="branches-D5.jsonl: local version", where=bid)
    local = vlib.local_return_states(outdir)
    wanted = {sub: local.get(sub, {}).get("local_status", "unresolved") for sub in members}
    if r.get("local_statuses") != wanted:
        err("branches-D5.jsonl %s: local_statuses disagree with versioned adapted-local returns" % bid,
            shape="branches-D5.jsonl: local statuses", where=bid)
    unresolved = sorted(sub for sub, status in wanted.items() if status != "validated")
    if sorted(unc) != unresolved:
        err("branches-D5.jsonl %s: unresolved_members disagree with adapted-local returns: %s" % (bid, unresolved),
            shape="branches-D5.jsonl: unresolved members", where=bid)
    if r.get("shared_status") not in ("supported", "unsupported", "unresolved") or not str(r.get("shared_warrant") or "").strip():
        err("branches-D5.jsonl %s: shared_status and its separate shared_warrant are required" % bid,
            shape="branches-D5.jsonl: shared status", where=bid)
    # Empirical bindings and the optional four-problem mapping are separate.
    binds, free = r.get("binds"), r.get("leaves_free")
    for fld, val in (("binds", binds), ("leaves_free", free)):
        if not isinstance(val, list) or set(val) - set(vlib.PROBLEMS):
            err("branches-D5.jsonl %s: %s is not a list of organizing problems from %s" % (bid, fld, vlib.PROBLEMS),
                shape="branches-D5.jsonl: %s" % fld, where=bid)
    if isinstance(binds, list) and isinstance(free, list) and set(binds) & set(free):
        err("branches-D5.jsonl %s: %s both bound and left free" % (bid, sorted(set(binds) & set(free))),
            shape="branches-D5.jsonl: problem bound and free", where=bid)
    fog = r.get("form_or_grouping")
    if fog not in ("form", "grouping"):
        err("branches-D5.jsonl %s: form_or_grouping %r is not form or grouping" % (bid, fog),
            shape="branches-D5.jsonl: form_or_grouping", where=bid)
    construct_ids = set(fourth or []) | set(s11.elements(outdir)[0] or [])
    construct_ids |= set(vlib.load_scheme(outdir)[0] or []) | set(s11.dimension_ids(outdir) or [])
    bindings = r.get("construct_bindings")
    if not isinstance(bindings, list) or any(x not in construct_ids for x in bindings):
        err("branches-D5.jsonl %s: construct_bindings must resolve to the empirical model's constructs" % bid,
            shape="branches-D5.jsonl: construct bindings", where=bid)
    if fog == "form" and (not bindings or not str(r.get("binding_account") or "").strip()):
        err("branches-D5.jsonl %s: a form needs empirical construct bindings and their relational account" % bid,
            shape="branches-D5.jsonl: form binding nothing", where=bid)
    for fld in ("over", "under"):
        val = r.get(fld)
        if not isinstance(val, list):
            err("branches-D5.jsonl %s: %s missing (a list of fourth-order themes)" % (bid, fld),
                shape="branches-D5.jsonl: %s missing" % fld, where=bid)
            continue
        for k in val:
            if not s11.T4.match(str(k)) or (fourth is not None and k not in fourth):
                err("branches-D5.jsonl %s: %s names %r, not a fourth-order theme of the model" % (bid, fld, k),
                    shape="branches-D5.jsonl: %s unresolved" % fld, where="%s %s" % (bid, k))
    # arrows and their expectations (rule 6)
    n_an = len(analysed) if analysed else None
    expected = {}
    seen_arrows = collections.Counter()
    for fld in ("arrows_present", "arrows_absent", "arrows_not_testable"):
        val = r.get(fld)
        if not isinstance(val, list):
            err("branches-D5.jsonl %s: %s missing" % (bid, fld), shape="branches-D5.jsonl: %s missing" % fld, where=bid)
            continue
        for a in val:
            aid = a.get("arrow") if isinstance(a, dict) else a
            seen_arrows[aid] += 1
            if arrows is not None and aid not in arrows:
                err("branches-D5.jsonl %s: %s names arrow %r, not in model/arrows.jsonl" % (bid, fld, aid),
                    shape="branches-D5.jsonl: arrow unresolved", where="%s %s" % (bid, aid))
                continue
            ex = a.get("expected") if isinstance(a, dict) else None
            if not isinstance(ex, (int, float)):
                err("branches-D5.jsonl %s: %s %s carries no expected count; rule 6 requires the expectation "
                    "on every arrow compared across branches" % (bid, fld, aid),
                    shape="branches-D5.jsonl: arrow without expected", where="%s %s" % (bid, aid))
                continue
            expected[aid] = ex
            if arrows is not None and n_an:
                want = len(arrows[aid] & analysed) / float(n_an) * len(members)
                if abs(want - ex) > max(TOL_ABS, TOL_REL * want):
                    err("branches-D5.jsonl %s: %s expected %.2f but the arrow's subs over the analysed set "
                        "(%d of %d) times n (%d) gives %.2f" % (bid, aid, ex, len(arrows[aid] & analysed), n_an,
                                                                len(members), want),
                        shape="branches-D5.jsonl: expected does not recompute", where="%s %s" % (bid, aid))
            if fld == "arrows_absent" and ex < 1:
                err("branches-D5.jsonl %s: arrow %s is reported absent with expected %.2f, below one; it is "
                    "not-testable-here and no boundary condition may be written from it (rule 6)" % (bid, aid, ex),
                    shape="branches-D5.jsonl: absent below expectation one", where="%s %s" % (bid, aid))
            if fld == "arrows_not_testable" and ex >= 1:
                warn("branches-D5.jsonl %s: arrow %s is not-testable-here with expected %.2f, at or above one; "
                     "say in the account why" % (bid, aid, ex))
    for aid, k in seen_arrows.items():
        if k > 1:
            err("branches-D5.jsonl %s: arrow %s appears in more than one of present, absent, not_testable" % (bid, aid),
                shape="branches-D5.jsonl: arrow in two lists", where="%s %s" % (bid, aid))
    seen_props = collections.Counter()
    for fld in ("propositions_hold", "propositions_fail", "propositions_not_testable"):
        val = r.get(fld)
        if not isinstance(val, list):
            err("branches-D5.jsonl %s: %s missing" % (bid, fld), shape="branches-D5.jsonl: %s missing" % fld, where=bid)
            continue
        for pid in val:
            seen_props[pid] += 1
            if props is not None and pid not in props:
                err("branches-D5.jsonl %s: %s names %r, not in propositions.jsonl" % (bid, fld, pid),
                    shape="branches-D5.jsonl: proposition unresolved", where="%s %s" % (bid, pid))
                continue
            if fld == "propositions_fail" and props is not None and arrows is not None and n_an:
                rests = props[pid].get("rests_on") or []
                exps = [expected.get(a, len(arrows.get(a, set()) & analysed) / float(n_an) * len(members))
                        for a in rests]
                if rests and not any(e >= 1 for e in exps):
                    err("branches-D5.jsonl %s: %s fails here, but every arrow it rests on (%s) has expected "
                        "below one; no propositions_fail may be written from a not-testable arrow (rule 6)"
                        % (bid, pid, rests), shape="branches-D5.jsonl: proposition failed on no expectation",
                        where="%s %s" % (bid, pid))
    for pid, k in seen_props.items():
        if k > 1:
            err("branches-D5.jsonl %s: proposition %s appears in more than one of hold, fail, not_testable" % (bid, pid),
                shape="branches-D5.jsonl: proposition in two lists", where="%s %s" % (bid, pid))
    # survival and the canvas
    sv = r.get("survival")
    if not isinstance(sv, dict) or not isinstance(sv.get("median_organizing_end_hour"), (int, float)) \
            or not isinstance(sv.get("aftermath_share"), (int, float)) or not 0 <= sv.get("aftermath_share", -1) <= 1:
        err("branches-D5.jsonl %s: survival needs median_organizing_end_hour (a number) and aftermath_share in "
            "[0, 1], from the record and never from the canvas" % bid, shape="branches-D5.jsonl: survival block", where=bid)
    else:
        oe = jsonl(os.path.join(outdir, "organizing_end-A1.jsonl"))
        if oe:
            hrs = sorted(x.get("organizing_end_hour") for x in oe
                         if x.get("sub") in members and isinstance(x.get("organizing_end_hour"), (int, float)))
            if hrs:
                med = hrs[len(hrs) // 2] if len(hrs) % 2 else (hrs[len(hrs) // 2 - 1] + hrs[len(hrs) // 2]) / 2.0
                if abs(med - sv["median_organizing_end_hour"]) > 1.0:
                    warn("branches-D5.jsonl %s: median_organizing_end_hour %s against %.1f from organizing_end-A1.jsonl "
                         "over the members; the harness's recomputed figure is the one reported" % (bid, sv["median_organizing_end_hour"], med))
        wr = sv.get("work_remained")
        if not isinstance(wr, dict) or sorted(wr) != ["kept", "lost", "silent"] or \
                not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in wr.values()):
            err("branches-D5.jsonl %s: survival needs work_remained {kept, lost, silent} as counts of members, from "
                "organizing_end-A1.jsonl; silence is a value (contract §1)" % bid, shape="branches-D5.jsonl: work_remained", where=bid)
        elif isinstance(r.get("n"), int) and sum(wr.values()) != r["n"]:
            err("branches-D5.jsonl %s: work_remained counts %d rooms, the branch holds %d" % (bid, sum(wr.values()), r["n"]),
                shape="branches-D5.jsonl: work_remained", where=bid)
    cv = r.get("canvas")
    if not isinstance(cv, dict) or "median_area_px" not in cv or "rooms_with_artwork" not in cv \
            or not str(cv.get("read") or "").strip():
        err("branches-D5.jsonl %s: canvas needs median_area_px, rooms_with_artwork and a read clause, projected "
            "on after the record" % bid, shape="branches-D5.jsonl: canvas block", where=bid)
    for fld in ("unmodelled", "confidence"):
        if not str(r.get(fld) or "").strip():
            err("branches-D5.jsonl %s: %s is empty" % (bid, fld), shape="branches-D5.jsonl: %s empty" % fld, where=bid)
    return bid, members, unc


def check_account(outdir, ctx, bid, members, unc, analysed, el, ar, scheme, fourth):
    name = os.path.join("forms", "%s-account.md" % bid)
    p = os.path.join(outdir, name)
    if not os.path.exists(p):
        err("%s was not written; every accounted branch has its account file" % name,
            shape="account file missing", where=bid)
        return
    t = open(p, encoding="utf-8").read()
    # the sections are found on heading lines (or bold lead-ins), so a word in prose does not count
    heads = [(i, ln.lower()) for i, ln in enumerate(t.split("\n"))
             if ln.lstrip().startswith("#") or ln.lstrip().startswith("**")]
    pos = -1
    for label, pat in SECTIONS:
        hit = next((i for i, ln in heads if re.search(pat, ln)), None)
        if hit is None:
            err("%s has no heading for %r; the thirteen sections of stage D5 section 2, in order, each under "
                "its heading" % (name, label), shape="%s: section missing" % name, where=label)
            continue
        if hit < pos:
            err("%s: section %r comes before the one the stage file puts ahead of it; the sections are in "
                "order" % (name, label), shape="%s: section out of order" % name, where=label)
        pos = max(pos, hit)
    for m in unc:
        if not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(str(m)), t):
            err("%s does not name %s, a member whose adapted-local account remains unresolved; name the evidence limit D3 "
                "named" % (name, m), shape="%s: unresolved member not named" % name, where=str(m))
    named = [m for m in members if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(str(m)), t)]
    if len(named) < min(2, len(members)):
        err("%s names %d of the branch's members; the representative members are two or three rooms told in "
            "the branch's terms" % (name, len(named)))
    for x in sorted(set(ID_PAT.findall(t))):
        pool = None
        if x.startswith("T3-"):
            pool = scheme
        elif x.startswith("T4-"):
            pool = fourth
        elif x.startswith("A"):
            pool = ar
        else:
            pool = el
        if pool is not None and x not in pool:
            err("%s names %s, which resolves to nothing in the model (elements, arrows, the scheme, the "
                "fourth-order themes)" % (name, x), shape="%s: id unresolved" % name, where=x)
    if analysed is not None:
        for x in sorted(set(ROOM_PAT.findall(t))):
            if x not in analysed and x != "place":
                err("%s names r/%s, which is not in the analysed set" % (name, x),
                    shape="%s: room unresolved" % name, where=x)
    cites = CITE_PAT.findall(t)
    if not cites:
        err("%s carries no citation [sub/code_id]; the narrative and the concepts carry participants' words "
            "through cite.py, each with its citation" % name)
    codes = vlib.store_codes(ctx)
    for sub, cid in sorted(set(cites)):
        if (sub, cid) not in codes:
            err("%s cites [%s/%s], which is not a concept in the store" % (name, sub, cid),
                shape="%s: citation unresolved" % name, where="%s/%s" % (sub, cid))


def check_waterfall_survival(outdir, ctx, accounted, analysed):
    wf = text(outdir, "waterfall-D5.md")
    if wf:
        if not re.search(r"\brule\b", wf, re.I):
            err("waterfall-D5.md does not state the rule by which the branch and the room were chosen before "
                "the walk (stage D5 section 3)")
        if not re.search(r"prior\.md", wf):
            err("waterfall-D5.md does not read the walk against prior.md's expectation of what the lower "
                "levels describe")
        if accounted and not any(re.search(r"\b%s\b" % re.escape(b), wf) for b in accounted):
            err("waterfall-D5.md names no accounted branch; the walk goes through one branch")
        if analysed and not any(re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(m), wf) for m in analysed):
            err("waterfall-D5.md names no room of the analysed set; the walk goes down to one room's model")
    sv = text(outdir, "survival-D5.md")
    if sv:
        for b in sorted(accounted):
            if not re.search(r"\b%s\b" % re.escape(b), sv):
                err("survival-D5.md does not report branch %s; organizing_end_hour and the aftermath share per "
                    "branch, from the record" % b, shape="survival-D5.md: branch missing", where=b)
        if "organizing_end_hour" not in sv or "aftermath" not in sv.lower() or "work_remained" not in sv:
            err("survival-D5.md does not report organizing_end_hour, the aftermath share and work_remained")
        low = sv.lower()
        if "canvas" not in low or not re.search(r"survived|left behind|not a measure|not a score", low):
            err("survival-D5.md does not carry the contract's section 5 sentence on what the canvas measures "
                "(what the drawing left behind; not a measure of skill, not a score) beside the record")


def check(root, outdir, ctx):
    need(outdir, "branches-D5.jsonl", "notes-D5.md", "findings.jsonl", "defects.jsonl")
    vlib.model_moved(outdir, "D3", "D5")
    by_id = {b["id"]: b for b in s11.branches(outdir) if b.get("id")}
    if not by_id and not str(text(outdir, "notes-D5.md")).strip():
        err("No shared branch: notes-D5.md must explain the negative result and remaining local accounts")
    got = vlib.analysed_set("D5", "branch members against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    verdicts = room_verdicts(outdir)
    if verdicts is None:
        err("verdicts-D.jsonl is not in the output directory; composition per branch is counted from it")
    arrows = arrow_subs(outdir)
    if arrows is None:
        err("model/arrows.jsonl is not in the output directory; every arrow compared across branches carries "
            "its expectation from its subs")
    props = propositions(outdir)
    if props is None:
        warn("propositions.jsonl is absent; propositions_hold, _fail and _not_testable were NOT resolved")
    el, ar = s11.elements(outdir)
    scheme, _ = vlib.load_scheme(outdir)
    fourth = s11.fourth_ids(outdir)
    rows = jsonl(os.path.join(outdir, "branches-D5.jsonl")) or []
    accounted = set()
    for i, r in enumerate(rows, 1):
        res = check_line(r, i, outdir, ctx, by_id, analysed, verdicts, arrows, props, fourth)
        if res is None:
            continue
        bid, members, unc = res
        if bid in accounted:
            err("branches-D5.jsonl has two lines for %s; a closed branch's account is superseded, not rewritten "
                "(rule 18)" % bid)
        accounted.add(bid)
        check_account(outdir, ctx, bid, members, unc, analysed, el, ar, scheme, fourth)
    for f in sorted(os.listdir(os.path.join(outdir, "forms"))) if os.path.isdir(os.path.join(outdir, "forms")) else []:
        m = re.match(r"^(.+)-account\.md$", f)
        if m and m.group(1) not in accounted:
            err("forms/%s exists with no branches-D5.jsonl line for %s; the line and the account are one leg"
                % (f, m.group(1)), shape="account without a line", where=f)
    missing = sorted(set(by_id) - accounted)
    if last_leg(outdir):
        need(outdir, "waterfall-D5.md", "survival-D5.md")
        for b in missing:
            err("branch %s has no account and no branches-D5.jsonl line, and the waterfall leg has begun; every "
                "branch is accounted, the unadapted group with an account of its own" % b,
                shape="branch unaccounted at the last leg", where=b)
    elif missing:
        warn("%d of %d branches accounted so far (%s remain); the waterfall and survival leg closes the stage"
             % (len(accounted), len(by_id), missing[:6]))
    elif not rows and by_id:
        err("branches-D5.jsonl holds no line; a branch leg writes the account and its line")
    check_waterfall_survival(outdir, ctx, accounted, analysed)
    for f in ("findings.jsonl", "defects.jsonl"):
        rows_f = jsonl(os.path.join(outdir, f)) or []
        if not any(str(x.get("stage")) == "D5" for x in rows_f):
            warn("%s has no stage-D5 line yet; a claim a branch bounds is a findings line (rule 14), a theme that "
                 "lumps two things a defects line" % f)
    print("  branches accounted %d of %d" % (len(accounted), len(by_id)))
    # the diary's lines for the stage are checked by validate.py's common checks (rule 20)


# ---- the planted fixture ----------------------------------------------------------------------

VERDICTS_10 = [
    {"sub": "denmark", "reader": "r1", "verdict": "composes", "themes": ["t07"], "residue": None, "cannot_tell_under": None},
    {"sub": "denmark", "reader": "r2", "verdict": "composes", "themes": ["t07"], "residue": None, "cannot_tell_under": None},
    {"sub": "asoiaf", "reader": "r1", "verdict": "does-not-compose", "themes": ["t02"], "residue": None, "cannot_tell_under": None},
    {"sub": "asoiaf", "reader": "r2", "verdict": "does-not-compose", "themes": ["t02"], "residue": None, "cannot_tell_under": None},
    {"sub": "sweden", "reader": "r1", "verdict": "composes", "themes": [], "residue": None, "cannot_tell_under": None},
    {"sub": "sweden", "reader": "r2", "verdict": "composes", "themes": [], "residue": None, "cannot_tell_under": None},
]
LINE_F01 = {"branch": "F01", "name": "recruiting conditioned on a two-sided attack", "n": 2,
            "verdicts": {"composes": 1, "composes-with-residue": 0, "does-not-compose": 1, "cannot-tell": 0},
            "uncomposed_members": ["asoiaf"], "binds": ["division"], "leaves_free": ["reward"],
            "over": ["T4-003"], "under": [],
            "arrows_present": [{"arrow": "A01", "expected": 1.33}], "arrows_absent": [], "arrows_not_testable": [],
            "propositions_hold": ["N12"], "propositions_fail": [], "propositions_not_testable": [],
            "survival": {"median_organizing_end_hour": 70, "aftermath_share": 0.1,
                         "work_remained": {"kept": 1, "lost": 0, "silent": 1}},
            "canvas": {"median_area_px": 1200, "rooms_with_artwork": 2, "read": "both kept an artwork"},
            "unmodelled": "the template keeper", "form_or_grouping": "form", "confidence": "fair"}
ACCOUNT = """# F01, the account

## 1. How these rooms organized, as a narrative
r/denmark called for hands: "we need more people at the border" [denmark/c0117]. r/asoiaf held: "hold the line" [asoiaf/c0011].

## 2. What the branch does
P02 unchanged.

## 3. What it does differently
add-condition on P07 (T3-014), in denmark and asoiaf.

## 4. The concepts it employs
[denmark/c0118].

## 5. Composition here
One composes (denmark), one does not (asoiaf), under the condition D3 named.

## 6. How the model runs here
P07 does the work; P02 sits idle in asoiaf.

## 7. The one relationship that runs differently here
A01, both sides quoted.

## 8. Fourth-order themes over- and under-represented
T4-003 over.

## 9. Arrows present, absent or not-testable-here
A01 present, expected 1.33.

## 10. How representative members do the work
denmark read at length; asoiaf fits worst.

## 11. The nearest branch and what separates them
None; no cross-link.

## 12. The form test
Binds division; leaves reward free.

## 13. What would make you doubt this is a form at all
A third room meeting the key without the condition.
"""
SURVIVAL = ("# survival-D5\n\nF01: median organizing_end_hour 70, aftermath share 0.1, work_remained kept 1, "
            "lost 0, silent 1, from the record.\n\n"
            "The canvas, projected on afterwards: the atlas records what survived the last hour; it is not a "
            "measure of skill and not a score.\n")
WATERFALL = ("# waterfall-D5\n\nThe rule: the largest branch and its worst-fitting member. F01, then asoiaf's "
             "model, its adaptations, the quotes, and back up; read against prior.md's expectation.\n")


def base(outdir, root):
    s11.base(outdir, root)
    _w, _wj = s11._w, s11._wj
    version = vlib.model_hash(outdir)
    _w(outdir, "handoff-D/VERSION", version + "\n")
    _wj(outdir, "verdicts-D.jsonl", [dict(row, model_version=version) for row in VERDICTS_10])
    manifest = [{"sub": sub, "phase": "initial", "status": "accepted", "model_version": version,
                 "ids": [x["id"] for x in (jsonl(os.path.join(outdir, "adaptations.jsonl")) or []) if x.get("sub") == sub],
                 "local_status": "validated" if sub == "denmark" else "unresolved",
                 "local_grade": "composes" if sub == "denmark" else "composes-with-residue"}
                for sub in ["denmark", "asoiaf"]]
    _wj(outdir, "adaptation-returns.jsonl", manifest)
    LINE_F01.update(global_model_version=version, local_model_version=version,
                    local_statuses={"denmark": "validated", "asoiaf": "unresolved"},
                    unresolved_members=["asoiaf"], construct_bindings=["P07"],
                    binding_account="Recruiting depends on a documented attack condition.",
                    shared_status="supported", shared_warrant="Both cases document the same condition and mechanism.")
    _wj(outdir, "propositions.jsonl", [{"id": "N12", "statement": "recruiting follows holding", "rests_on": ["A01"],
                                        "theorised": False, "finding": "F-031", "carried_by": "pattern",
                                        "rival": "holding follows recruiting"}])
    _wj(outdir, "branches-D5.jsonl", [LINE_F01])
    _w(outdir, "forms/F01-account.md", ACCOUNT)
    _w(outdir, "waterfall-D5.md", WATERFALL)
    _w(outdir, "survival-D5.md", SURVIVAL)
    _w(outdir, "notes-D5.md", "# notes-D5\n")
    _wj(outdir, "findings.jsonl", [{"id": "F-003", "stage": "D5", "leg": "D5a-01", "statement": "x", "warrant": "read",
                                    "status": "bounded", "why": "F01 bounds it"}])
    _wj(outdir, "defects.jsonl", [{"stage": "D5", "leg": "D5a-01", "where": "T4-003", "what": "lumps two things", "sure": True}])


def _plant_uncomposed_unnamed(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "branches-D5.jsonl", [dict(LINE_F01, unresolved_members=[])])


def _plant_absent_below_one(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "model/arrows.jsonl", [{"id": "A01", "from": "P02", "to": "P07", "subs": ["denmark"], "in_model": True}])
    s11._wj(outdir, "branches-D5.jsonl", [dict(LINE_F01, arrows_present=[], arrows_absent=[{"arrow": "A01", "expected": 0.67}])])


def _plant_element_unresolved(outdir, root):
    base(outdir, root)
    s11._w(outdir, "forms/F01-account.md", ACCOUNT.replace("P02 unchanged.", "P02 and P99 unchanged."))


def _plant_section_missing(outdir, root):
    base(outdir, root)
    s11._w(outdir, "forms/F01-account.md", ACCOUNT.replace("## 12. The form test\n", "## 12. The constructs\n"))


def _plant_verdicts_disagree(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "branches-D5.jsonl", [dict(LINE_F01, verdicts={"composes": 2, "does-not-compose": 0}, uncomposed_members=[])])


def _plant_branch_unaccounted(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "branches.jsonl", [s11.BRANCH_F01, dict(s11.BRANCH_F01, id="F02", parent="F01", members=["denmark"],
                                                            keys=["add-condition:P07:T3-014"], name="the same, in one room")])


def _plant_room_unresolved(outdir, root):
    base(outdir, root)
    s11._w(outdir, "forms/F01-account.md", ACCOUNT.replace("r/asoiaf held", "r/narnia held"))


def _plant_silence_dropped(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "branches-D5.jsonl", [dict(LINE_F01, survival={"median_organizing_end_hour": 70, "aftermath_share": 0.1,
                                                                    "work_remained": {"kept": 1, "lost": 0}})])


PLANTED = [
    ("silence left out of work_remained", _plant_silence_dropped, "survival needs work_remained"),
    ("unresolved member unnamed", _plant_uncomposed_unnamed, "unresolved_members disagree with adapted-local returns"),
    ("absent below expectation one", _plant_absent_below_one, "not-testable-here and no boundary"),
    ("element id unresolved", _plant_element_unresolved, "names P99, which resolves to nothing"),
    ("account section missing", _plant_section_missing, "has no heading for 'the form test'"),
    ("verdicts disagree with D", _plant_verdicts_disagree, "do not match verdicts-D.jsonl"),
    ("branch unaccounted at last leg", _plant_branch_unaccounted, "has no account and no branches-D5.jsonl line"),
    ("room outside analysed set", _plant_room_unresolved, "names r/narnia, which is not in the analysed set"),
]
