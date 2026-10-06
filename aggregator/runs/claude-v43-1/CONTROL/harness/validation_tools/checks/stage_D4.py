"""checks/stage_D4.py: the close-check of stage D4, the taxonomy from adaptations, v38.

Written from stages/STAGE-D4-forming-the-tree.md (its Outputs block, sections 1 to 6, its Close
section), from SCHEMA-adaptations.md sections 7 and 8, from the docstring of tools/distance.py,
and from the v37 check it descends from (_v37-source/tools/validate.py, stage11 and
_dendrogram_common). What it checks is the SHAPE of the stage's files: existence, parse, ids that
resolve, keys that the matrices carry, members in the analysed set, counts that reconcile. It
cannot check whether a cut is right.

What is checked, in order:
  1. distance.py's outputs in _views/: the sixteen key matrices, distance.tsv and the three per-kind
     distances, tree-likeness.json; the weights and grades in tree-likeness.json are prior.md
     section 7's; distance.tsv is square, symmetric, in [0, 1], zero on the diagonal, and holds
     every room of the analysed set; no matrix column is a canvas field or a verdict (rule 7).
  2. branches.jsonl: id, parent, level, kind, keys, members, name, what_it_changes, since; every
     key is op:target:node with the op in OPS, the target an element (or a dimension for link) and
     the node resolving at the branch's level; every member is in the analysed set and holds
     every key in the matrix of that level; a subform's members are a subset of its parent's and
     its keys a superset; a room in two branches that do not nest is declared in crosslinks.jsonl;
     a branch is not named after a member; not every room gets its own label (contract section 1).
  3. forms/<id>.md per branch, naming every member and every key.
  4. crosslinks.jsonl: parse; any branch id and any room it names resolve. The stage file gives
     no fields for it, so nothing more is checked.
  5. tier_history.jsonl: one stage-D4 line per move at least (a branch named, a subform or a
     cross-link declared), each with a move from the eight and the leg it was made in; a leg may
     carry several moves.
  6. The accounting of section 4: every room of the analysed set is a branch member, or is named
     in tree-D4.md (the unadapted group, adapted but in no branch, unreturned at D2); an
     unreturned room is in no branch; tree-D4.md reports the delta score.
  7. The comparison (section 5) and the projections (section 6): chunk-share-D4.py reads neither
     the ledger, the branches, the verdicts nor the canvas; chunk-share-D4.md carries the
     percentile, the adjusted Rand index, the silhouette and the two seeds; chunk-share-D4.jsonl
     carries per cluster a two-letter code, members in the analysed set and in one cluster only,
     n, n_low_information, a profile over fourth-order themes and nothing from the canvas or the
     verdicts; projections-D4.jsonl carries one line per branch and per cluster with the verdict
     counts, a canvas block and a percentile; notes-D4.md declares the method. At a leg that made
     a move (the current leg has a stage-D4 tier_history line) their absence is a warning, because
     they are built after the last cut; at any other leg it is an error.

The snaps that prove each cut preceded the projection are not read here (rule: only stage E1
reads _snap/); stage E1 checks them.

Not carried from v37 stage11 / _dendrogram_common:
  - objections.jsonl and the answer to the operator's objections in notes-D4.md (no such file in
    v38; D3 adjudication replaces it).
  - profiles-D4.csv, distance-D4.csv, dendrogram-D4.json, clusters-D4.jsonl,
    clusters_members-D4.jsonl, tier_robustness-D4.md, cluster_report-D4.md, cluster-D4.py (the
    dendrogram as the stage's result; v38 reads the taxonomy off the ledger and keeps the tree
    only as the comparison in chunk-share-D4.*).
  - the crossing columns (division, allocation, reward, information, exception, goal,
    is_problem, beyond_four) as forbidden coordinates: the crossing is gone.
  - _snap/D4-cut.sha256 against cluster_report-D4.md: snaps are harness-owned per cut and are
    read at E1 only.
"""
import collections, json, os, re, sys
from adaptation_ledger import effective_lines
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

BRANCH = re.compile(r"^[FG]\d{2,3}$")          # the stage file writes F03; vlib.FAMILY is G
T3 = re.compile(r"^T3-\d{3}$")
T4 = re.compile(r"^T4-\d{2,3}$")               # the fixture and the contract write T4-03, stage D5 T4-005
DIM = re.compile(r"^D\d{1,2}$")
CLUSTER = re.compile(r"^[A-Z]{2}$")
LEVELS = {"third": "3", "fourth": "4", "dimension": "dim", "target": "target",
          "3": "3", "4": "4", "dim": "dim"}
KINDS = ("correction", "elaboration", "specification")
MOVE_STEMS = ("asking", "puzzle", "dropping", "merging", "splitting", "relating", "contrasting",
              "sequencing", "hypothes")
CANVAS_WORDS = ("canvas", "area_px", "artwork", "composes", "verdict", "cannot-tell", "residue")
FORBIDDEN_IN_SCRIPT = ("branches.jsonl", "adaptations.jsonl", "adjudications.jsonl",
                       "verdicts-D", "canvas", "crosslinks.jsonl", "projections-D4")
W_DEFAULT = {"3": 4.0, "4": 2.0, "dim": 1.0, "target": 0.5}
G_DEFAULT = {"same_op": 1.0, "same_kind": 0.5, "diff_kind": 0.0, "opposite": -1.0}


# ---- helpers vlib lacks ------------------------------------------------------------------------

def read_prior_weights(outdir):
    """prior.md section 7 as distance.py reads it; None when prior.md is absent."""
    p = os.path.join(outdir, "prior.md")
    if not os.path.exists(p):
        return None, None
    import distance
    try:
        return distance.read_prior(p)
    except ValueError as exc:
        err("Invalid prior distance controls: %s" % exc)
        return None,None


def min_group_size(outdir):
    """A default of five; the analyst's number in tree-D4.md (with its reason) wins over prior.md's."""
    for f in ("tree-D4.md", "prior.md"):
        m = re.search(r"minimum group size[^\d]{0,60}(\d+)", text(outdir, f), re.I)
        if m:
            return int(m.group(1))
    return 5


def read_tsv(p):
    rows = [ln.rstrip("\n").split("\t") for ln in open(p, encoding="utf-8") if ln.strip()]
    return (rows[0], rows[1:]) if rows else ([], [])


def is_move(m):
    m = re.sub(r"[\s_]+", "-", str(m or "").strip().lower())
    return bool(m) and any(s in m for s in MOVE_STEMS)


def current_leg(root):
    p = os.path.join(root, ".leg")
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None


def elements(outdir):
    """(element ids, arrow ids) from out/model/, or (None, None) when elements.jsonl is absent."""
    el = jsonl(os.path.join(outdir, "model", "elements.jsonl"))
    if el is None:
        return None, None
    ar = jsonl(os.path.join(outdir, "model", "arrows.jsonl")) or []
    return {r.get("id") for r in el if r.get("id")}, {r.get("id") for r in ar if r.get("id")}


def fourth_ids(outdir):
    rows = jsonl(os.path.join(outdir, "fourth", "fourth.jsonl"))
    return {r.get("id") for r in rows if r.get("id")} if rows else None


def dimension_ids(outdir):
    rows = jsonl(os.path.join(outdir, "dimensions.jsonl"))
    return {r.get("id") for r in rows if r.get("id")} if rows else None


def unreturned_rooms(root, outdir):
    """DROPS/D/UNRETURNED.tsv (first column the room), from the folder root or out/."""
    for base in (root, outdir):
        p = os.path.join(base, "DROPS", "D", "UNRETURNED.tsv")
        if os.path.exists(p):
            out = set()
            for ln in open(p, encoding="utf-8"):
                s = ln.strip().split("\t")[0]
                if s and s.lower() not in ("sub", "room"):
                    out.add(s)
            return out
    return set()


def unadapted_rooms(outdir):
    """Rooms whose every ledger line is op none."""
    led = effective_lines(outdir, include_particular=True, include_pending=True, include_rejected=True)
    ops = collections.defaultdict(set)
    for l in led:
        if l.get("sub"):
            ops[l["sub"]].add(l.get("op"))
    return {s for s, o in ops.items() if o == {"none"}}


def branches(outdir):
    return jsonl(os.path.join(outdir, "branches.jsonl")) or []


def node_ok(node, level, scheme, fourth, dims):
    """Does the key's node resolve at the branch's level? None where the file to resolve it
    against is absent (then only the pattern is checked)."""
    if level == "3":
        if not T3.match(node):
            return False
        return None if scheme is None else node in scheme
    if level == "4":
        if not T4.match(node):
            return False
        return None if fourth is None else node in fourth
    if level == "dim":
        if not DIM.match(node):
            return False
        return None if dims is None else node in dims
    return node == "*"


def four_counts(outdir, root, ctx, stage="D4"):
    """Section 4's four groups over the analysed set: members of a declared branch, the unadapted
    group, adapted but in no branch, unreturned at D2. Returns None when the analysed set is
    not computable, else (analysed, in_branch, unadapted, no_branch, unreturned)."""
    got = vlib.analysed_set(stage, "the accounting of stage D4 section 4", outdir, ctx)
    if got is None:
        return None
    analysed, _d = got
    in_branch = set()
    for b in branches(outdir):
        in_branch |= set(b.get("members") or [])
    in_branch &= analysed
    unret = unreturned_rooms(root, outdir) & analysed - in_branch
    unad = unadapted_rooms(outdir) & analysed - in_branch - unret
    rest = analysed - in_branch - unret - unad
    return analysed, in_branch, unad, rest, unret


# ---- the check ---------------------------------------------------------------------------------

def check_sealed_prior(outdir):
    """prior.md as done.sh recorded it at D1's close; a later change is a departure (stage D1, rule 10)."""
    rec = os.path.join(outdir, "_closes", "prior-D1.sha256")
    p = os.path.join(outdir, "prior.md")
    if not (os.path.exists(rec) and os.path.exists(p)):
        return
    import hashlib
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != open(rec).read().strip():
        deps = " ".join(json.dumps(r) for r in (jsonl(os.path.join(outdir, "departures.jsonl")) or []))
        if "prior" not in deps:
            err("prior.md changed after D1 sealed it, and departures.jsonl names no departure for it; the weights "
                "and thresholds are the ones set before any room answered (rule 10)", shape="prior:unsealed")


def check_views(outdir, ctx):
    check_sealed_prior(outdir)
    vlib.model_moved(outdir, "D3", "D4")
    vd = os.path.join(outdir, "_views")
    for level in ("3", "4", "dim", "target"):
        for kind in ("all",) + KINDS:
            need(outdir, os.path.join("_views", "rooms-x-adaptations.%s.%s.tsv" % (level, kind)))
    for kind in KINDS:
        need(outdir, os.path.join("_views", "distance.%s.tsv" % kind))
    need(outdir, os.path.join("_views", "distance.tsv"), os.path.join("_views", "tree-likeness.json"))
    # tree-likeness.json: the weights and grades are prior.md's (section 1)
    tp = os.path.join(vd, "tree-likeness.json")
    if os.path.exists(tp):
        try:
            tl = json.load(open(tp, encoding="utf-8"))
        except Exception as e:
            err("_views/tree-likeness.json will not parse (%s); rerun distance.py" % e)
            tl = None
        if isinstance(tl, dict):
            if "delta_score" not in tl:
                err("_views/tree-likeness.json carries no delta_score; distance.py writes it on the "
                    "combined matrix (stage D4 section 1)")
            w, g = read_prior_weights(outdir)
            if w is None:
                err("prior.md is not in the output directory; the distance weights and grades are "
                    "declared there before stage D4 opens (SCHEMA section 7) and tree-likeness.json "
                    "must be confirmed against it")
            else:
                tw, tg = tl.get("weights") or {}, tl.get("grades") or {}
                if {k: float(v) for k, v in tw.items()} != w:
                    err("_views/tree-likeness.json weights %s are not prior.md section 7's %s; rerun "
                        "distance.py with the sealed prior, never edit either" % (tw, w))
                if {k: float(v) for k, v in tg.items()} != g:
                    err("_views/tree-likeness.json grades %s are not prior.md section 7's %s; rerun "
                        "distance.py with the sealed prior, never edit either" % (tg, g))
    # distance.tsv: square, symmetric, bounded, complete over the analysed set
    dp = os.path.join(vd, "distance.tsv")
    if os.path.exists(dp):
        hdr, rows = read_tsv(dp)
        cols = hdr[1:]
        names = [r[0] for r in rows]
        if cols != names:
            err("_views/distance.tsv is not square: its columns and rows name different rooms; "
                "rerun distance.py")
        else:
            n = len(names)
            D = {}
            for r in rows:
                if len(r) != n + 1:
                    err("_views/distance.tsv row %s has %d cells for %d rooms; rerun distance.py"
                        % (r[0], len(r) - 1, n), shape="distance.tsv: ragged row", where=r[0])
                    continue
                for j, v in enumerate(r[1:]):
                    try:
                        D[(r[0], names[j])] = float(v)
                    except ValueError:
                        err("_views/distance.tsv %s x %s is %r, not a number" % (r[0], names[j], v),
                            shape="distance.tsv: not a number", where="%s x %s" % (r[0], names[j]))
            for (a, b), v in D.items():
                if not (0.0 <= v <= 1.0):
                    err("_views/distance.tsv %s x %s = %s lies outside [0, 1]; d = (1 - S) / 2 with S "
                        "in [-1, 1] (SCHEMA section 7)" % (a, b, v), shape="distance.tsv: out of range",
                        where="%s x %s" % (a, b))
                if a == b and abs(v) > 1e-9:
                    err("_views/distance.tsv %s x %s = %s; a room is at distance 0 from itself" % (a, b, v),
                        shape="distance.tsv: nonzero diagonal", where=a)
                if (b, a) in D and abs(D[(b, a)] - v) > 1e-6:
                    err("_views/distance.tsv is not symmetric at %s x %s" % (a, b),
                        shape="distance.tsv: asymmetric", where="%s x %s" % (a, b))
            got = vlib.analysed_set("D4", "distance.tsv against the analysed set", outdir, ctx)
            if got is not None:
                expected = got[0] - unreturned_rooms(ctx.get("root", os.path.dirname(outdir)), outdir)
                missing = sorted(expected - set(names))
                extra = sorted(set(names) - expected)
                if extra:
                    err("distance.tsv includes dropped, unreturned or unknown rooms: %s" % extra)
                if missing:
                    err("_views/distance.tsv has no row for %d rooms of the analysed set (%s); every "
                        "room is in the distance, declared unreturned rooms are excluded"
                        % (len(missing), missing[:6]))
    # rule 7: nothing from the canvas or the verdicts is a coordinate
    for level in ("3", "4", "dim", "target"):
        for kind in ("all",) + KINDS:
            p = os.path.join(vd, "rooms-x-adaptations.%s.%s.tsv" % (level, kind))
            if not os.path.exists(p):
                continue
            hdr = open(p, encoding="utf-8").readline().lower()
            for bad in CANVAS_WORDS:
                if bad in hdr:
                    err("_views/%s carries a column naming %r: nothing from the canvas or the "
                        "verdicts may be a coordinate (rule 7); rerun distance.py from the ledger"
                        % (os.path.basename(p), bad))


def check_branches(outdir, root, ctx):
    rows = branches(outdir)
    if not rows:
        try:
            status=json.load(open(os.path.join(outdir,"taxonomy-status.json")))
            got=vlib.analysed_set("D4","negative taxonomy outcome",outdir,ctx)
            expected=got[0]-unreturned_rooms(root,outdir) if got else set()
            if status.get("status")!="no-supported-forms" or not str(status.get("reason","")).strip() or set(status.get("reviewed_rooms",[]))!=expected:
                raise ValueError("record must explain the negative result and account for every returned case")
        except (OSError,ValueError,TypeError) as exc:
            err("Empty branches require taxonomy-status.json with no-supported-forms, reason and reviewed_rooms: %s" % exc)
    got = vlib.analysed_set("D4", "branch members against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    el, _ar = elements(outdir)
    if el is None:
        err("model/elements.jsonl is not in the output directory; every branch key names an element "
            "and cannot be resolved without it")
    scheme, _sname = vlib.load_scheme(outdir)
    fourth, dims = fourth_ids(outdir), dimension_ids(outdir)
    unret = unreturned_rooms(root, outdir)
    # cuts whose tier_history line declares the members' material as a ground beside the keys (section 2)
    material_grounded = {str(r.get("id")) for r in (jsonl(os.path.join(outdir, "tier_history.jsonl")) or [])
                         if str(r.get("stage")) == "D4" and "material" in str(r.get("ground") or "")}
    matrices = {}
    ids, by_id = [], {}
    for i, b in enumerate(rows, 1):
        where = "line %d" % i
        bid = b.get("id")
        if not bid or not BRANCH.match(str(bid)):
            err("branches.jsonl %s: id %r is not a branch id (F03)" % (where, bid),
                shape="branches.jsonl: bad id", where=where)
            continue
        if bid in by_id:
            err("branches.jsonl: id %s appears twice; a cut supersedes a branch under a new id, "
                "never reuses one" % bid)
        by_id[bid] = b
        ids.append(bid)
        for k in ("id", "parent", "level", "kind", "keys", "members", "name", "what_it_changes", "since"):
            if k not in b:
                err("branches.jsonl %s (%s): field %r missing; the line carries id, parent, level, kind, "
                    "keys, members, name, what_it_changes, since" % (where, bid, k),
                    shape="branches.jsonl: field missing", where="%s %s" % (bid, k))
        level = LEVELS.get(str(b.get("level")))
        if level is None:
            err("branches.jsonl %s: level %r is not third, fourth, dimension or target; a branch is "
                "declared at the level where its members meet" % (bid, b.get("level")),
                shape="branches.jsonl: level outside the ladder", where=bid)
        if b.get("kind") not in KINDS:
            err("branches.jsonl %s: kind %r is not correction, elaboration or specification"
                % (bid, b.get("kind")), shape="branches.jsonl: kind outside the three", where=bid)
        if not str(b.get("name") or "").strip():
            err("branches.jsonl %s: name is empty; name the branch by what its keys change in the "
                "global model" % bid, shape="branches.jsonl: no name", where=bid)
        if not str(b.get("what_it_changes") or "").strip():
            err("branches.jsonl %s: what_it_changes is empty" % bid,
                shape="branches.jsonl: no what_it_changes", where=bid)
        if not str(b.get("since") or "").strip():
            err("branches.jsonl %s: since names no cut leg" % bid, shape="branches.jsonl: no since", where=bid)
        members = b.get("members") or []
        if not isinstance(members, list) or not members:
            err("branches.jsonl %s: members is empty; a branch with no member is not a branch" % bid,
                shape="branches.jsonl: no members", where=bid)
            members = []
        name_l = str(b.get("name") or "").lower()
        for m in members:
            if m and str(m).lower() in name_l:
                err("branches.jsonl %s: the name %r contains the member %s; a branch is named by what "
                    "its keys change, never by a member's name (stage D4 section 2)"
                    % (bid, b.get("name"), m), shape="branches.jsonl: named after a member", where=bid)
            if analysed is not None and m not in analysed:
                err("branches.jsonl %s: member %r is not in the analysed set (dropped at A1, or not in "
                    "the frame)" % (bid, m), shape="branches.jsonl: member outside the analysed set",
                    where="%s %s" % (bid, m))
            if m in unret:
                err("branches.jsonl %s: member %r was unreturned at D2 and has no ledger; it is out "
                    "by name, never a member" % (bid, m), shape="branches.jsonl: unreturned member",
                    where="%s %s" % (bid, m))
        if members and len(members) < min_group_size(outdir):
            warn("branches.jsonl %s has %d members, below the minimum group size %d (tree-D4.md, prior.md "
                 "or the default); below it a shared meeting is variation, not a subform (stage D4 section 2)"
                 % (bid, len(members), min_group_size(outdir)))
        keys = b.get("keys") or []
        unadapted = b.get("type") == "unadapted"
        if unadapted and (keys or not set(members) <= unadapted_rooms(outdir) or b.get("parent")):
            err("Unadapted branch must have no keys or parent and contain only explicit none returns: %s" % bid)
        if not isinstance(keys, list) or (not keys and not unadapted):
            err("branches.jsonl %s: keys is empty; a branch is grounded on keys, and on its members' material "
                "only beside them as a declared ground" % bid,
                shape="branches.jsonl: no keys", where=bid)
            keys = []
        # the matrix at the branch's level: every member holds every key
        mat = None
        if level:
            mp = os.path.join(outdir, "_views", "rooms-x-adaptations.%s.all.tsv" % level)
            if mp not in matrices and os.path.exists(mp):
                hdr, mrows = read_tsv(mp)
                matrices[mp] = (hdr, {r[0]: dict(zip(hdr[1:], r[1:])) for r in mrows})
            mat = matrices.get(mp)
        for k in keys:
            parts = str(k).split(":")
            if len(parts) != 3:
                err("branches.jsonl %s: key %r is not op:target:node" % (bid, k),
                    shape="branches.jsonl: malformed key", where="%s %s" % (bid, k))
                continue
            op, target, node = parts
            if op not in vlib.OPS or op in ("propose", "none"):
                err("branches.jsonl %s: key %r names op %r, not one of the seven operations"
                    % (bid, k, op), shape="branches.jsonl: key op outside the seven", where="%s %s" % (bid, k))
            tgt_ok = (el is None or target in el) or (op == "link" and DIM.match(target) and
                                                       (dims is None or target in dims))
            if not tgt_ok:
                err("branches.jsonl %s: key %r targets %r, which model/elements.jsonl does not hold"
                    % (bid, k, target), shape="branches.jsonl: key target unresolved", where="%s %s" % (bid, k))
            if level:
                ok = node_ok(node, level, scheme, fourth, dims)
                if ok is False:
                    err("branches.jsonl %s: key %r ends in %r, which is not a node at the %s level "
                        "(T3- at third, T4- at fourth, D at dimension, * at the bare target) or does "
                        "not resolve" % (bid, k, node, b.get("level")),
                        shape="branches.jsonl: key node unresolved at the level", where="%s %s" % (bid, k))
            if mat is not None:
                hdr, cells = mat
                if k not in hdr:
                    err("branches.jsonl %s: key %r is not a column of _views/rooms-x-adaptations.%s.all.tsv; "
                        "a key is one the ledger's accepted lines carry at that level"
                        % (bid, k, level), shape="branches.jsonl: key not in the matrix", where="%s %s" % (bid, k))
                else:
                    for m in members:
                        if str(cells.get(m, {}).get(k, "0")) != "1":
                            if bid in material_grounded:
                                warn("branches.jsonl %s: member %s does not hold key %r; the cut declares the "
                                     "members' material as a ground, so tree-D4.md says what in %s's material "
                                     "puts it here" % (bid, m, k, m))
                                continue
                            err("branches.jsonl %s: member %s does not hold key %r in the %s-level matrix; "
                                "a branch is grounded on keys its members share, or on their material where the "
                                "cut's tier_history line declares it" % (bid, m, k, level),
                                shape="branches.jsonl: member without the key", where="%s %s %s" % (bid, m, k))
            elif level:
                err("_views/rooms-x-adaptations.%s.all.tsv is absent, so %s's keys were NOT checked "
                    "against the ledger" % (level, bid), shape="branches.jsonl: matrix absent", where=level)
    # nesting and cross-links
    for bid, b in by_id.items():
        par = b.get("parent")
        if par in (None, "", "null"):
            continue
        if par not in by_id:
            err("branches.jsonl %s: parent %r is not a declared branch" % (bid, par))
            continue
        pm, cm = set(by_id[par].get("members") or []), set(b.get("members") or [])
        if not cm <= pm:
            err("branches.jsonl %s: members %s are not in its parent %s; a subform nests inside its "
                "parent" % (bid, sorted(cm - pm)[:5], par))
        pk, ck = set(by_id[par].get("keys") or []), set(b.get("keys") or [])
        t4map={m:r['id'] for r in (jsonl(os.path.join(outdir,'fourth','fourth.jsonl')) or []) for m in r.get('members',[])}
        dimmap={m:r['id'] for r in (jsonl(os.path.join(outdir,'dimensions.jsonl')) or []) for m in r.get('members',[])}
        def inherited(parent_key, child_key):
            if len(parent_key.split(':'))!=3 or len(child_key.split(':'))!=3:return False
            po,pt,pn=parent_key.split(':');co,ct,cn=child_key.split(':')
            nodes={cn,'*'};four=t4map.get(cn)
            if four:nodes.add(four)
            dim=dimmap.get(four or cn)
            if dim:nodes.add(dim)
            return po==co and pt==ct and pn in nodes
        missing_keys={p for p in pk if not any(inherited(p,c) for c in ck)}
        if missing_keys:
            err("branches.jsonl %s: it lacks its parent %s's keys %s; a subform nests by adding keys"
                % (bid, par, sorted(missing_keys)[:5]))

    def ancestors(x):
        out = set()
        while x in by_id and by_id[x].get("parent") in by_id and by_id[x]["parent"] not in out:
            x = by_id[x]["parent"]
            out.add(x)
        return out
    for bid in by_id:
        if bid in ancestors(bid): err("Branch parent cycle detected at %s" % bid)
    cross = jsonl(os.path.join(outdir, "crosslinks.jsonl")) or []
    cross_pairs={(r.get('sub'),frozenset([a,b])) for r in cross for a in r.get('branches',[]) for b in r.get('branches',[]) if a!=b}
    seen_pairs = set()
    for a in ids:
        for c in ids:
            if a >= c or c in ancestors(a) or a in ancestors(c):
                continue
            both = set(by_id[a].get("members") or []) & set(by_id[c].get("members") or [])
            for m in sorted(both):
                if (m, a, c) in seen_pairs:
                    continue
                seen_pairs.add((m, a, c))
                if (m,frozenset([a,c])) not in cross_pairs:
                    err("room %s is a member of %s and of %s, which do not nest, and crosslinks.jsonl "
                        "does not declare it; a room whose adaptations meet different groups is a "
                        "cross-link, declared and never forced" % (m, a, c),
                        shape="branches.jsonl: room in two branches without a cross-link", where=m)
    if analysed and ids and len(ids) >= len(analysed):
        err("branches.jsonl declares %d branches over an analysed set of %d rooms; never give every "
            "room its own label (contract section 1)" % (len(ids), len(analysed)))
    # forms/<id>.md per branch
    for bid, b in by_id.items():
        fp = os.path.join(outdir, "forms", "%s.md" % bid)
        if not os.path.exists(fp):
            err("forms/%s.md was not written; it is generated from branches.jsonl and the ledger at "
                "every cut (stage D4 section 3)" % bid, shape="forms: file missing", where=bid)
            continue
        ft = open(fp, encoding="utf-8").read()
        for m in b.get("members") or []:
            if str(m) not in ft:
                err("forms/%s.md does not name member %s; regenerate it from branches.jsonl" % (bid, m),
                    shape="forms: member not named", where="%s %s" % (bid, m))
        for k in b.get("keys") or []:
            if str(k) not in ft:
                err("forms/%s.md does not carry key %s with its how sentences; regenerate it" % (bid, k),
                    shape="forms: key not carried", where="%s %s" % (bid, k))
    return by_id


def check_crosslinks(outdir, ctx, by_id):
    rows = jsonl(os.path.join(outdir, "crosslinks.jsonl")) or []
    for i,r in enumerate(rows,1):
        sub=r.get('sub'); links=r.get('branches')
        if not isinstance(links,list) or len(links)<2 or len(set(links))!=len(links) or not str(r.get('reason','')).strip():
            err("crosslinks.jsonl line %d requires sub, at least two distinct branches and reason" % i);continue
        for bid in links:
            if bid not in by_id or sub not in by_id[bid].get('members',[]):
                err("crosslinks.jsonl line %d endpoint %s does not contain room %s" % (i,bid,sub))


def check_tier_history(outdir, by_id):
    rows = jsonl(os.path.join(outdir, "tier_history.jsonl"))
    if rows is None:
        err("tier_history.jsonl is not in the output directory; every move writes a line with its name")
        return []
    mine = [r for r in rows if str(r.get("stage")) == "D4"]
    for i, r in enumerate(mine, 1):
        if not is_move(r.get("move")):
            err("tier_history.jsonl stage-D4 line %d: move %r is not one of Grodal, Anteby and Holm's "
                "eight (asking questions, focusing on puzzles, dropping, merging, splitting, relating "
                "or contrasting, sequencing, developing or dropping working hypotheses)" % (i, r.get("move")),
                shape="tier_history.jsonl: move outside the eight", where="line %d" % i)
        if not r.get("leg"):
            err("tier_history.jsonl stage-D4 line %d names no leg; every move names its leg (a leg may carry "
                "several moves)" % i,
                shape="tier_history.jsonl: no leg", where="line %d" % i)
    if by_id and len(mine) < len(by_id):
        err("tier_history.jsonl holds %d stage-D4 lines for %d branches; every move is a line in "
            "tier_history.jsonl, logged and snapped when it is made" % (len(mine), len(by_id)))
    return mine


def check_accounting(outdir, root, ctx):
    tree = text(outdir, "tree-D4.md")
    if tree and not re.search(r"delta|tree-like", tree, re.I):
        err("tree-D4.md does not report the tree-likeness statistic (the delta score); it is read and "
            "logged before any cut (stage D4 section 1)")
    fc = four_counts(outdir, root, ctx)
    if fc is None:
        return
    analysed, in_branch, unad, rest, unret = fc
    print("  section 4: %d in a branch + %d unadapted + %d adapted in no branch + %d unreturned = %d, "
          "analysed %d" % (len(in_branch), len(unad), len(rest), len(unret),
                           len(in_branch | unad | rest | unret), len(analysed)))
    if not tree:
        err("tree-D4.md was not written; the accounting of section 4 lives there")
        return
    for m in sorted(unad | rest | unret):
        if not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(m), tree):
            err("tree-D4.md does not name %s, a room of the analysed set in no branch; every such room is "
                "named with why (the unadapted group, adapted but in no branch, or unreturned at D2)"
                % m, shape="tree-D4.md: room in no branch not named", where=m)
    if not re.search(r"n_analysed|analysed set", tree, re.I):
        err("tree-D4.md does not state the four counts against n_analysed (stage D4 section 4)")


def check_comparison(outdir, root, ctx, by_id, hist):
    names = ("chunk-share-D4.md", "chunk-share-D4.jsonl", "chunk-share-D4.py", "projections-D4.jsonl")
    present = [n for n in names if os.path.exists(os.path.join(outdir, n))]
    leg = current_leg(root)
    at_cut = bool(leg) and any(r.get("leg") == leg for r in hist)
    if not present:
        if at_cut:
            warn("the comparison (chunk-share-D4.*) and projections-D4.jsonl are not built yet; they "
                 "are built by script after the last cut, and the stage does not close without them")
            return
        need(outdir, *names)
        return
    need(outdir, *names)
    got = vlib.analysed_set("D4", "the comparison's clusters against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    # the script reads the store and the placements, never the ledger, the branches, the verdicts or the canvas
    src = text(outdir, "chunk-share-D4.py")
    for bad in FORBIDDEN_IN_SCRIPT:
        if bad in src:
            err("chunk-share-D4.py mentions %r; the comparison reads the store and the placements, never "
                "the ledger, branches.jsonl, the verdicts or the canvas (stage D4 section 5)" % bad)
    n11 = text(outdir, "notes-D4.md").lower()
    if "chunk-share" not in n11 and "chunk share" not in n11:
        err("notes-D4.md does not declare the comparison's method before chunk-share-D4.py runs "
            "(stage D4 section 5)")
    rep = text(outdir, "chunk-share-D4.md")
    if rep:
        for word, why in (("percentile", "the tier and volume verdicts are reported with the number"),
                          ("adjusted rand", "the index among the three distances and across tiers"),
                          ("silhouette", "the two numbers for every k from 2 to 12"),
                          ("seed", "the whole table twice under two declared seeds")):
            if word not in rep.lower():
                err("chunk-share-D4.md does not report %s; %s" % (word, why))
    try:
        import subprocess
        engine=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'chunk_compare.py')
        env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        replay=subprocess.run([sys.executable,'-I','-B',engine,'--verify','--out',outdir,'--store',os.path.join(ctx['package'],'store')], env=env, capture_output=True,text=True,timeout=600)
        if replay.returncode:
            err("chunk-share computation failed trusted numeric replay: "+(replay.stderr or replay.stdout)[-2000:])
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        err("chunk-share computation cannot be verified: %s" % exc)
    # the clusters
    cl = jsonl(os.path.join(outdir, "chunk-share-D4.jsonl")) or []
    fourth = fourth_ids(outdir)
    codes, allm = set(), []
    for i, c in enumerate(cl, 1):
        code = str(c.get("code") or "")
        if not CLUSTER.match(code):
            err("chunk-share-D4.jsonl line %d: code %r is not a two-letter hash code" % (i, code),
                shape="chunk-share-D4.jsonl: bad code", where="line %d" % i)
        codes.add(code)
        members = c.get("members") or []
        allm += members
        if analysed is not None:
            off = sorted(set(members) - analysed)
            if off:
                err("chunk-share-D4.jsonl %s names rooms outside the analysed set: %s" % (code, off[:5]),
                    shape="chunk-share-D4.jsonl: member outside the analysed set", where=code)
        if c.get("n") != len(members):
            err("chunk-share-D4.jsonl %s: n = %r but members holds %d" % (code, c.get("n"), len(members)),
                shape="chunk-share-D4.jsonl: n disagrees with members", where=code)
        nl = c.get("n_low_information")
        if not isinstance(nl, int) or nl < 0 or nl > len(members):
            err("chunk-share-D4.jsonl %s: n_low_information %r is not a count within n" % (code, nl),
                shape="chunk-share-D4.jsonl: n_low_information", where=code)
        prof = c.get("profile")
        if not isinstance(prof, dict) or not prof:
            err("chunk-share-D4.jsonl %s carries no profile over fourth-order themes" % code,
                shape="chunk-share-D4.jsonl: no profile", where=code)
        else:
            for k in prof:
                if any(w in str(k).lower() for w in CANVAS_WORDS):
                    err("chunk-share-D4.jsonl %s: profile key %r is a canvas field or a verdict; nothing "
                        "from either enters the feature space (rule 7)" % (code, k),
                        shape="chunk-share-D4.jsonl: canvas or verdict in the profile", where=code)
                elif not T4.match(str(k)) or (fourth is not None and k not in fourth):
                    err("chunk-share-D4.jsonl %s: profile key %r is not a fourth-order theme of the model"
                        % (code, k), shape="chunk-share-D4.jsonl: profile key unresolved", where="%s %s" % (code, k))
        for fld in ("over", "under"):
            for k in c.get(fld) or []:
                if not T4.match(str(k)) or (fourth is not None and k not in fourth):
                    err("chunk-share-D4.jsonl %s: %s names %r, not a fourth-order theme" % (code, fld, k),
                        shape="chunk-share-D4.jsonl: over/under unresolved", where="%s %s" % (code, k))
        bb = c.get("best_branch", c.get("branch"))
        if bb and bb not in by_id:
            err("chunk-share-D4.jsonl %s: best-matching branch %r is not in branches.jsonl" % (code, bb),
                shape="chunk-share-D4.jsonl: branch unresolved", where=code)
        jac = c.get("jaccard")
        if jac is not None and not (isinstance(jac, (int, float)) and 0 <= jac <= 1):
            err("chunk-share-D4.jsonl %s: jaccard %r is not in [0, 1]" % (code, jac),
                shape="chunk-share-D4.jsonl: jaccard", where=code)
    dup = [m for m, n in collections.Counter(allm).items() if n > 1]
    if dup:
        err("chunk-share-D4.jsonl puts rooms in more than one cluster: %s" % dup[:8])
    for c in cl:
        nb = c.get("nearest")
        if nb and nb not in codes:
            err("chunk-share-D4.jsonl %s: nearest cluster %r is not a cluster in the file" % (c.get("code"), nb),
                shape="chunk-share-D4.jsonl: nearest unresolved", where=str(c.get("code")))
    # the projections
    pr = jsonl(os.path.join(outdir, "projections-D4.jsonl")) or []
    seen_b, seen_c = set(), set()
    for i, p in enumerate(pr, 1):
        b, c = p.get("branch"), p.get("cluster")
        if bool(b) == bool(c):
            err("projections-D4.jsonl line %d names %s; one line per branch or per cluster"
                % (i, "both a branch and a cluster" if b else "neither a branch nor a cluster"),
                shape="projections-D4.jsonl: not one of branch or cluster", where="line %d" % i)
            continue
        key = b or c
        if b and b not in by_id:
            err("projections-D4.jsonl line %d: branch %r is not in branches.jsonl" % (i, b),
                shape="projections-D4.jsonl: branch unresolved", where=str(b))
        if c and c not in codes:
            err("projections-D4.jsonl line %d: cluster %r is not in chunk-share-D4.jsonl" % (i, c),
                shape="projections-D4.jsonl: cluster unresolved", where=str(c))
        (seen_b if b else seen_c).add(key)
        v = p.get("verdicts")
        if not isinstance(v, dict) or set(v) - set(vlib.VERDICTS):
            err("projections-D4.jsonl %s: verdicts block missing or carries a key outside the four "
                "verdicts" % key, shape="projections-D4.jsonl: verdicts block", where=key)
        cv = p.get("canvas")
        if not isinstance(cv, dict) or not cv:
            err("projections-D4.jsonl %s carries no canvas block; the six fields are summarised per "
                "branch and per cluster after the cuts, with contract section 5's sentence beside them"
                % key, shape="projections-D4.jsonl: canvas block", where=key)
        elif not any(isinstance(x, str) and len(x.split()) >= 4 for x in cv.values()):
            err("projections-D4.jsonl %s: the canvas block carries no sentence on what the canvas "
                "measures (contract section 5)" % key, shape="projections-D4.jsonl: canvas sentence", where=key)
        pct = [x for k, x in p.items() if "percentile" in str(k).lower()]
        if not pct and isinstance(v, dict) and "percentile" in v:
            pct = [v["percentile"]]
        if not pct or not all(isinstance(x, (int, float)) for x in pct):
            err("projections-D4.jsonl %s reports no percentile against the permutation null; the number, "
                "not only the word" % key, shape="projections-D4.jsonl: no percentile", where=key)
    for bid in by_id:
        if bid not in seen_b:
            err("projections-D4.jsonl has no line for branch %s" % bid,
                shape="projections-D4.jsonl: branch without a line", where=bid)
    for code in codes:
        if code not in seen_c:
            err("projections-D4.jsonl has no line for cluster %s" % code,
                shape="projections-D4.jsonl: cluster without a line", where=code)


def check(root, outdir, ctx):
    template = os.path.join(root, "handoff", "RETURN-D.md")
    if os.path.exists(template) and "local_status:" in open(template, encoding="utf-8").read():
        need(outdir, "_views/adaptation-tree.json", "_views/adaptation-tree.svg", "_views/adaptation-tree.html")
    need(outdir, "branches.jsonl", "crosslinks.jsonl", "tier_history.jsonl", "tree-D4.md", "notes-D4.md")
    if not os.path.isdir(os.path.join(outdir, "forms")):
        err("stage output 'forms/' was not written; forms/<id>.md is generated per branch")
    check_views(outdir, ctx)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import ingest                      # the ledger re-lifted to the model D3 froze (stage D3 §6)
    stale = ingest.relift_problems(os.path.dirname(ctx["package"]), outdir)
    if stale:
        err("%d ledger line(s) carry a lift the placements no longer give (%s ...); the distances are measured on the "
            "re-lifted ledger: python3 tools/ingest.py D --relift" % (len(stale), stale[:4]), shape="ledger:relift")
    by_id = check_branches(outdir, root, ctx)
    check_crosslinks(outdir, ctx, by_id)
    hist = check_tier_history(outdir, by_id)
    check_accounting(outdir, root, ctx)
    check_comparison(outdir, root, ctx, by_id, hist)
    # the diary's lines for the stage are checked by validate.py's common checks (rule 20)


# ---- the planted fixture ----------------------------------------------------------------------

def _w(outdir, name, content=""):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


LEDGER = [
    {"id": "denmark-001", "sub": "denmark", "op": "add-condition", "element": "P07", "source": "denmark:t07",
     "lift": ["denmark:t07", "T3-014", "T4-003", "D2"], "condition": "under attack from two sides",
     "statement": None, "how": "explains why the room recruited outside on night two.",
     "evidence": {"codes": ["denmark:c0117"]}, "relation": None, "portable": True, "kind": "elaboration",
     "origin": "labeler", "model_version": "sha256:x", "labeler_run": "r"},
    {"id": "asoiaf-001", "sub": "asoiaf", "op": "add-condition", "element": "P07", "source": "asoiaf:t02",
     "lift": ["asoiaf:t02", "T3-014", "T4-003", "D2"], "condition": "under attack from two sides",
     "statement": None, "how": "explains why the room called for outside hands.",
     "evidence": {"codes": ["asoiaf:c0011"]}, "relation": None, "portable": True, "kind": "elaboration",
     "origin": "labeler", "model_version": "sha256:x", "labeler_run": "r"},
    {"id": "sweden-001", "sub": "sweden", "op": "none", "how": "the global model explains this room as stated.",
     "evidence": {"codes": []}, "model_version": "sha256:x"},
]
ADJ = [{"adaptation": "denmark-001", "decision": "accept", "kind": "elaboration", "reason": "met twice",
        "pair": "asoiaf-001", "leg": "D3-P07"},
       {"adaptation": "asoiaf-001", "decision": "accept", "kind": "elaboration", "reason": "met twice",
        "pair": "denmark-001", "leg": "D3-P07"}]
BRANCH_F01 = {"id": "F01", "parent": None, "level": "third", "kind": "elaboration",
              "keys": ["add-condition:P07:T3-014"], "members": ["denmark", "asoiaf"],
              "name": "recruiting conditioned on a two-sided attack",
              "what_it_changes": "P07 runs only under a condition the model leaves open", "since": "D4a-01"}
PROJ_F01 = {"branch": "F01", "verdicts": {"composes": 1, "does-not-compose": 1}, "verdicts_percentile": 40.0,
            "canvas": {"median_area_px": 1200, "rooms_with_artwork": 2,
                       "read": "the atlas records what survived the last hour; it is not a measure of skill"},
            "canvas_percentile": 55.0}
PROJ_QX = {"cluster": "QX", "verdicts": {"composes": 1, "does-not-compose": 1}, "verdicts_percentile": 40.0,
           "canvas": {"median_area_px": 1200, "rooms_with_artwork": 2,
                      "read": "the atlas records what survived the last hour; it is not a measure of skill"},
           "canvas_percentile": 55.0}
CLUSTER_QX = {"code": "QX", "members": ["denmark", "asoiaf"], "n": 2, "n_low_information": 2,
              "profile": {"T4-003": 1.0}, "over": ["T4-003"], "under": [], "nearest": None, "merge_height": None,
              "volume": {"items_in_window": 40, "concepts": 3, "themes": 1}, "best_branch": "F01", "jaccard": 1.0}
CHUNK_MD = ("# chunk-share-D4\n\nsilhouette and stability for every k from 2 to 12 under seed 0 and seed 1; "
            "the tier check's adjusted Rand index against its null: 0.9, 99th percentile; the volume check: "
            "percentile 40. sweden has no placed second-order theme and is out of the comparison by name.\n")
CHUNK_PY = '"""chunk-share-D4.py: the comparison. Reads package/store/themes.jsonl and out/assignments_final.jsonl.\n' \
           'Dirichlet-multinomial shrinkage, CLR + Ward; Jaccard and Hellinger beside it."""\nprint("stub")\n'
TREE_MD = ("# tree-D4\n\nThe delta score is null (three rooms; fewer than four leaves), so no tree was drawn.\n"
           "Accounting against n_analysed = 3: 2 in a branch (F01); 1 unadapted (sweden, returned none); "
           "0 adapted in no branch; 0 unreturned.\n")


def base(outdir, root):
    """A minimal fixture that passes stage D4's check: two adapted rooms meeting on one key at the
    third-order level, one unadapted room, one branch, the comparison and the projections."""
    _w(outdir, "dropped.jsonl", "")
    _w(outdir, "prior.md", "## 7\nw = 4, 2, 1, 0.5 for a meeting at third-order, fourth-order, dimension, bare "
                           "target; g = 1, 0.5, 0, -1 for same op, same kind, different kind, the two opposite "
                           "pairs.\nminimum group size: 2\n")
    _wj(outdir, "model/elements.jsonl", [
        {"id": "P07", "kind": "process", "statement": "recruiting from outside", "tier": "T4-003",
         "dimension": "D2", "status": "standing", "since": "C2-pass-2", "evidence": {"codes": ["denmark:c0117"]}},
        {"id": "P02", "kind": "process", "statement": "holding the border", "tier": "T4-001",
         "dimension": "D1", "status": "standing"}])
    _wj(outdir, "model/arrows.jsonl", [{"id": "A01", "from": "P02", "to": "P07", "kind": "order",
                                        "subs": ["denmark", "asoiaf"], "in_model": True, "status": "standing"}])
    _wj(outdir, "scheme_final.jsonl", [{"id": "T3-014", "label": "calling outside"}, {"id": "T3-020", "label": "defending"}])
    _wj(outdir, "fourth/fourth.jsonl", [{"id": "T4-003", "members": ["T3-014", "T3-020"]}, {"id": "T4-001", "members": []}])
    _wj(outdir, "dimensions.jsonl", [{"id": "D1", "label": "defence", "members": ["T4-001"]},
                                     {"id": "D2", "label": "growth", "members": ["T4-003"]}])
    _wj(outdir, "assignments_final.jsonl", [{"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"]},
                                            {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-014"]}])
    _wj(outdir, "adaptations.jsonl", LEDGER)
    _wj(outdir, "adjudications.jsonl", ADJ)
    tools = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    import subprocess
    subprocess.run([sys.executable, os.path.join(tools, "distance.py"), "--out", outdir, "--quartets", "50"],
                   check=True, stdout=subprocess.DEVNULL, cwd=root)
    _wj(outdir, "branches.jsonl", [BRANCH_F01])
    _w(outdir, "crosslinks.jsonl", "")
    _wj(outdir, "tier_history.jsonl", [{"t": "2026-01-01T00:00:00Z", "stage": "D4", "leg": "D4a-01", "tier": "branch",
                                        "id": "F01", "move": "relating", "event": "created", "why": "shared key"}])
    _w(outdir, "forms/F01.md", "# F01\n\nmembers: denmark, asoiaf\n\nkeys: add-condition:P07:T3-014\n")
    _w(outdir, "tree-D4.md", TREE_MD)
    _w(outdir, "notes-D4.md", "# notes-D4\n\nThe chunk-share comparison's method, declared before the script ran.\n")
    _w(outdir, "chunk-share-D4.py", CHUNK_PY)
    _w(outdir, "chunk-share-D4.md", CHUNK_MD)
    _wj(outdir, "chunk-share-D4.jsonl", [CLUSTER_QX])
    _wj(outdir, "projections-D4.jsonl", [PROJ_F01])
    subprocess.run([sys.executable, '-I', '-B', os.path.join(tools, 'chunk_compare.py'), '--out', outdir, '--store', os.path.join(root,'package','store')], check=True, stdout=subprocess.DEVNULL)


def _plant_member_off_set(outdir, root):
    base(outdir, root)
    _wj(outdir, "branches.jsonl", [dict(BRANCH_F01, members=["denmark", "asoiaf", "narnia"])])


def _plant_key_not_held(outdir, root):
    base(outdir, root)
    _wj(outdir, "branches.jsonl", [dict(BRANCH_F01, members=["denmark", "asoiaf", "sweden"])])
    _w(outdir, "tree-D4.md", TREE_MD)


def _plant_weights_moved(outdir, root):
    base(outdir, root)
    _w(outdir, "prior.md", "## 7\nw = 3, 2, 1, 0.5 ...; g = 1, 0.5, 0, -1 ...\nminimum group size: 2\n")


def _plant_room_unaccounted(outdir, root):
    base(outdir, root)
    _w(outdir, "tree-D4.md", "# tree-D4\n\ndelta score null. Accounting against n_analysed: 2 in a branch.\n")


def _plant_script_reads_ledger(outdir, root):
    base(outdir, root)
    _w(outdir, "chunk-share-D4.py", CHUNK_PY + "open('out/adaptations.jsonl')\n")


def _plant_no_comparison(outdir, root):
    base(outdir, root)
    for n in ("chunk-share-D4.md", "chunk-share-D4.jsonl", "chunk-share-D4.py", "projections-D4.jsonl"):
        os.remove(os.path.join(outdir, n))


def _plant_named_after_member(outdir, root):
    base(outdir, root)
    _wj(outdir, "branches.jsonl", [dict(BRANCH_F01, name="the denmark form")])


def _plant_two_branches_no_crosslink(outdir, root):
    base(outdir, root)
    _wj(outdir, "branches.jsonl", [BRANCH_F01, dict(BRANCH_F01, id="F02", members=["asoiaf"],
                                                    name="recruiting under attack, twice")])
    _w(outdir, "forms/F02.md", "# F02\n\nasoiaf\n\nadd-condition:P07:T3-014\n")
    _wj(outdir, "projections-D4.jsonl", [PROJ_F01, dict(PROJ_F01, branch="F02"), PROJ_QX])
    _wj(outdir, "tier_history.jsonl", [{"stage": "D4", "leg": "D4a-01", "move": "relating", "id": "F01"},
                                       {"stage": "D4", "leg": "D4a-02", "move": "splitting", "id": "F02"}])


def _plant_not_relifted(outdir, root):
    base(outdir, root)
    _wj(outdir, "assignments_final.jsonl", [{"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"]},
                                            {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-020"]}])


def _plant_prior_moved(outdir, root):
    base(outdir, root)
    _w(outdir, "_closes/prior-D1.sha256", "0" * 64 + "\n")


PLANTED = [
    ("prior.md changed after D1's seal", _plant_prior_moved, "changed after D1 sealed it"),
    ("a ledger not re-lifted after D3", _plant_not_relifted, "the re-lifted ledger"),
    ("member outside analysed set", _plant_member_off_set, "not in the analysed set"),
    ("member without the key", _plant_key_not_held, "does not hold key"),
    ("weights not prior.md's", _plant_weights_moved, "not prior.md section 7's"),
    ("room in no branch unnamed", _plant_room_unaccounted, "does not name sweden"),
    ("script reads the ledger", _plant_script_reads_ledger, "chunk-share-D4.py mentions"),
    ("comparison not built", _plant_no_comparison, "'chunk-share-D4.jsonl' was not written"),
    ("branch named after member", _plant_named_after_member, "never by a member's name"),
    ("cross-link undeclared", _plant_two_branches_no_crosslink, "crosslinks.jsonl does not declare"),
]
