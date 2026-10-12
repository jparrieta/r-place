#!/usr/bin/env python3
"""vlib.py, v38: what every close-check shares. validate.py and tools/checks/stage_*.py import it.

Errors and warnings are collected here (E, W) and folded by shape at the end, so a per-line check
over thousands of lines prints one line per shape with a count and the first instance.
"""
import collections, glob, hashlib, json, os, re

E, W = [], []


def err(m, shape=None, where=None):
    E.append((m, shape, where))


def warn(m, shape=None, where=None):
    W.append((m, shape, where))


def fold(items):
    out, seen = [], {}
    for m, shape, where in items:
        if shape is None:
            out.append(m)
            continue
        if shape not in seen:
            seen[shape] = [1, m, where]
            out.append(shape)
        else:
            seen[shape][0] += 1
    final = []
    for row in out:
        if isinstance(row, str) and row in seen:
            n, m, where = seen.pop(row)
            final.append(m if n == 1 else "%s  [%d lines with this shape; first: %s]" % (m, n, where))
        elif row not in seen:
            final.append(row)
    return final


def resolve_root(arg):
    arg = arg or "."
    pkg = os.path.join(arg, "package")
    if os.path.isdir(pkg):
        return arg, pkg
    return (os.path.dirname(os.path.abspath(arg)) or "."), arg


def jsonl(p):
    """Rows, or None when the file is absent. A line that is not JSON is an error."""
    if not os.path.exists(p):
        return None
    out = []
    for i, line in enumerate(open(p, encoding="utf-8"), 1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except ValueError as ex:
            err("%s line %d is not JSON: %s" % (os.path.basename(p), i, ex),
                shape="notjson:%s" % os.path.basename(p), where="line %d" % i)
    return out


def text(outdir, name):
    p = os.path.join(outdir, name)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""


def need(outdir, *names):
    """Every named output exists. A name with a glob is satisfied by one match."""
    for n in names:
        p = os.path.join(outdir, n)
        if any(ch in n for ch in "*?[") and glob.glob(p):
            continue
        if not os.path.exists(p):
            err("stage output %r was not written" % n)


def current_step(root):
    """The step of the open leg, from .leg (`A1b-03` -> `A1b`, `C5c` -> `C5c`), or None when no leg is open
    (the self-test). A check that is step-aware demands a step's outputs only at that step."""
    import re as _re
    p = os.path.join(root or ".", ".leg")
    if not os.path.exists(p):
        return None
    m = _re.match(r"^([A-E]\d[a-z])", open(p, encoding="utf-8").read().strip())
    return m.group(1) if m else None


MODEL_FILES = ("model/elements.jsonl", "model/arrows.jsonl", "model/loops.jsonl", "fourth/fourth.jsonl", "dimensions.jsonl",
               "scheme_v2.jsonl", "assignments_final.jsonl")


def model_hash(outdir):
    """The model's version: sha256 over the model and its tiers (MODEL_FILES present), each file's bytes
    preceded by its relative name and a newline. None when model/elements.jsonl is absent. done.sh records it
    at the close of C5, D3 and D6 in out/_closes/model-<stage>.sha256; handoff.py writes it as VERSION."""
    if not os.path.exists(os.path.join(outdir, "model", "elements.jsonl")):
        return None
    h = hashlib.sha256()
    for name in MODEL_FILES:
        p = os.path.join(outdir, name)
        if os.path.exists(p):
            h.update((name + "\n").encode("utf-8"))
            h.update(open(p, "rb").read())
    return h.hexdigest()


def frozen_hash(outdir, stage):
    p = os.path.join(outdir, "_closes", "model-%s.sha256" % stage)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None


def tree_hash(outdir):
    """Hash D4's substantive branch structure; D5 account files are separate outputs."""
    if not os.path.isfile(os.path.join(outdir, "branches.jsonl")):
        return None
    digest = hashlib.sha256()
    for name in ("branches.jsonl", "subforms.jsonl", "crosslinks.jsonl"):
        path = os.path.join(outdir, name)
        digest.update((name + "\n").encode())
        digest.update(open(path, "rb").read() if os.path.isfile(path) else b"<missing>")
    return digest.hexdigest()


def tree_moved(outdir):
    path = os.path.join(outdir, "_closes", "tree-D4.sha256")
    frozen = open(path, encoding="utf-8").read().strip() if os.path.isfile(path) else None
    current = tree_hash(outdir)
    if not frozen or not current or frozen != current:
        err("D4 tree has no matching trusted closure hash; branches, subforms and crosslinks must remain unchanged",
            shape="tree:moved")


def model_moved(outdir, frozen_at, here, allowed=None):
    """An error when the model and its tiers are not the version done.sh froze at `frozen_at`'s close, unless
    `allowed` (a callable) says the move is an amendment the stage permits (rule 11)."""
    fz, mh = frozen_hash(outdir, frozen_at), model_hash(outdir)
    if fz and mh and fz != mh and not (allowed and allowed()):
        err("model/ and its tiers moved after %s froze them (%s..., now %s...); at %s nothing below the model moves "
            "except as a recorded amendment (rule 11)" % (frozen_at, fz[:12], mh[:12], here), shape="model:moved")


def local_return_states(outdir):
    """Versioned adapted-local status, distinct from any fixed-global reader verdict.

    An old return may carry forward only through D3's explicit unaffected-case decision.
    Missing legacy status and stale versions remain unresolved, never implicit successes.
    """
    from adaptation_ledger import effective_rooms, effective_lines
    from dreturn import LOCAL_STATUSES
    current = model_hash(outdir)
    scope_path = os.path.join(outdir, "recheck-scope.json")
    try:
        scope = json.load(open(scope_path, encoding="utf-8"))
    except (OSError, ValueError):
        scope = {}
    unaffected = scope.get("unaffected_rooms") or {}
    out = {}
    pending_rooms = {row.get("sub") for row in effective_lines(outdir, include_pending=True, include_particular=True, include_rejected=True)
                     if row.get("decision") in ("pending", "reject") and row.get("op") != "none"}
    for sub, record in effective_rooms(outdir).items():
        state = dict(record)
        original = str(record.get("model_version") or "").removeprefix("sha256:")
        carried = bool(current and frozen_hash(outdir, "D3") == current
                       and isinstance(unaffected, dict) and str(unaffected.get(sub) or "").strip())
        matches = bool(current and original == current)
        state["current_model_version"] = current
        state["version_status"] = "current" if matches else "unaffected-carry-forward" if carried else "stale-or-unknown"
        status = record.get("local_status")
        state["local_status"] = status if status in LOCAL_STATUSES and (matches or carried) else "unresolved"
        if sub in pending_rooms:
            state["local_status"] = "unresolved"
            state["pending_evidence"] = True
        if record.get("account_sha256"):
            account = os.path.join(outdir, "rooms", sub, "model-D-recheck.md" if record.get("phase") == "recheck" else "model-D.md")
            if not os.path.isfile(account) or sha(account) != record["account_sha256"]:
                state["local_status"] = "unresolved"
                state["account_status"] = "changed-or-missing"
        out[sub] = state
    return out


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---- the store, the frame, the analysed set -------------------------------------------------

def rooms(ctx):
    """package/store/rooms.jsonl: the frame. None, having said so, when the store is not there."""
    if "rooms" not in ctx:
        p = os.path.join(ctx["package"], "store", "rooms.jsonl")
        ctx["rooms"] = jsonl(p)
        ctx["rooms_path"] = p
    return ctx["rooms"]


def frame(stage, what, ctx):
    r = rooms(ctx)
    if not r:
        err("stage %s: %s holds no rooms, so %s was NOT checked. Give validate.py the folder root "
            "(the one holding package/) as its second argument." % (stage, ctx.get("rooms_path"), what))
        return None
    return {x["sub"] for x in r}


def analysed_set(stage, what, outdir, ctx):
    """The frame minus what stage A1 dropped (dropped.jsonl, written under its §4, empty or not).
    Returns (analysed, dropped) or None having said what was not checked."""
    fr = frame(stage, what, ctx)
    if fr is None:
        return None
    dropped = jsonl(os.path.join(outdir, "dropped.jsonl"))
    if dropped is None:
        err("stage %s: dropped.jsonl is not in the output directory, so there is no analysed set and "
            "%s was NOT checked. Stage A1 writes it under §4, empty or not." % (stage, what))
        return None
    d = {x["sub"] for x in dropped if x.get("sub")}
    return fr - d, d


def store_themes(ctx):
    """(sub, theme_id) of every second-order theme in the store, and the count per room."""
    if "themes" not in ctx:
        rows = jsonl(os.path.join(ctx["package"], "store", "themes.jsonl")) or []
        # a split child is a second-order theme too, and its parent stays one for the records made before
        # the split (J, 2026-10-12, QB2-011)
        rows = rows + (jsonl(os.path.join(ctx.get("outdir") or "", "recut", "themes.jsonl")) or [])
        ctx["themes"] = {(r["sub"], r["theme_id"]) for r in rows}
        ctx["themes_per_room"] = collections.Counter(r["sub"] for r in rows)
    return ctx["themes"]


def store_codes(ctx):
    """(sub, code_id) of every first-order concept in the store (retracted ones are not there)."""
    if "codes" not in ctx:
        rows = jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or []
        ctx["codes"] = {(r["sub"], r["code_id"]) for r in rows}
        ctx["code_text"] = {(r["sub"], r["code_id"]): r.get("text") or "" for r in rows}
    return ctx["codes"]


# ---- the analyst's tiers ----------------------------------------------------------------------

T3 = re.compile(r"^T3-\d{3}$")
T4 = re.compile(r"^T4-\d{3}$")
DIM = re.compile(r"^D\d{1,2}$")
FAMILY = re.compile(r"^G\d{2,3}$")
ELEMENT = re.compile(r"^[PKCR]\d{2}$")
ARROW = re.compile(r"^A\d{2}$")
FINDING = re.compile(r"^F-\d{3}$")   # findings F-001 (rule 14), the lines of findings.jsonl
FORM_PASS = re.compile(r"^FP-\d{2,3}$")   # form-pass findings FP-01: prose in form_pass-C1.md, never a JSONL line
PROPOSITION = re.compile(r"^N\d{2,3}$")            # propositions N01 (stage C5); branches are F01 (stage D4)
VERDICTS = ("composes", "composes-with-residue", "does-not-compose", "cannot-tell")
LABELER_GRADES = ("composes", "composes-with-residue", "does-not-compose")
OPS = ("instantiate", "absent", "add-condition", "add-step", "link", "restrict", "contradict", "propose", "none")
DECISIONS = ("accept", "modify", "reject", "particular", "pending")
PROBLEMS = ("division", "allocation", "reward", "information")
CANVAS = ("canvas_entries", "canvas_area_px", "canvas_centre", "canvas_ring", "canvas_artwork", "canvas_source")


def load_scheme(outdir):
    """Ids of the third-order themes the current scheme defines: the newest scheme file present
    (scheme_v2, scheme_final, scheme_current, scheme), else None."""
    for name in ("scheme_v2.jsonl", "scheme_final.jsonl", "scheme_current.jsonl", "scheme.jsonl"):
        for d in ("", "scheme"):
            rows = jsonl(os.path.join(outdir, d, name))
            if rows:
                return {r.get("id") or r.get("theme") for r in rows if r.get("id") or r.get("theme")}, os.path.join(d, name)
    return None, None


def placements(outdir):
    """assignments_final.jsonl, else assign_final.jsonl: (sub, theme_id) -> [third-order ids]."""
    for name in ("assignments_final.jsonl", "assign_final.jsonl"):
        rows = jsonl(os.path.join(outdir, name))
        if rows:
            out = {}
            for r in rows:
                so = r.get("third_order") or []
                if isinstance(so, str):
                    so = [so]
                out[(r["sub"], r.get("theme_id"))] = so
            return out, name
    return None, None


def manifest_entry(outdir, stage, what):
    mp = os.path.join(outdir, "run_manifest.json")
    if not os.path.exists(mp):
        err("run_manifest.json is not in the output directory; stage %s appends its entry (%s) before "
            "the first reader is served" % (stage, what))
        return None
    try:
        man = json.load(open(mp, encoding="utf-8"))
    except Exception as e:
        err("run_manifest.json will not parse: %s" % e)
        return None
    ents = [e for e in (man if isinstance(man, list) else [man])
            if isinstance(e, dict) and str(e.get("stage")) == stage]
    if not ents:
        err("run_manifest.json has no stage-%s entry; %s is served under an entry appended before the "
            "first reader, with model, seed, decoding settings and the reader count" % (stage, what))
        return None
    return ents


def check_digest(outdir, name, sidecar):
    pm, ps = os.path.join(outdir, name), os.path.join(outdir, sidecar)
    if os.path.exists(pm) and os.path.exists(ps):
        raw = open(ps, encoding="utf-8").read().strip()
        if not re.fullmatch(r"[0-9a-f]{64}", raw):
            err("%s is not a bare 64-character hex digest on one line" % sidecar)
        elif sha(pm) != raw:
            err("%s is not the digest of %s as it stands: edited after hashing, or never rehashed" % (sidecar, name))


def check_manifest_digests(outdir, sidecar, names):
    ps = os.path.join(outdir, sidecar)
    if not os.path.exists(ps):
        err("%s was not written; the stage closes its files with it" % sidecar)
        return
    got = {}
    for line in open(ps, encoding="utf-8"):
        parts = line.split()
        if len(parts) != 2:
            continue
        a, b = parts
        if re.fullmatch(r"[0-9a-f]{64}", a):
            got[b] = a
        else:
            got[a] = b
    for n in names:
        if n not in got:
            err("%s does not list %s" % (sidecar, n))
            continue
        q = os.path.join(outdir, n)
        if not os.path.exists(q):
            err("%s lists %s, which does not exist" % (sidecar, n))
        elif sha(q) != got[n]:
            err("%s: %s was edited after it was hashed" % (sidecar, n))


def licence_sentence(outdir, name, what):
    """Wherever a fidelity or transmission figure appears, the sentence saying it bounds whether
    the instrument decides, not whether it is right (rule 17)."""
    t = text(outdir, name).lower()
    if not t:
        return
    if "bound" not in t or "not whether" not in t:
        err("%s reports %s without the sentence saying what it licenses (it bounds whether the "
            "instrument decides, not whether it is right)" % (name, what))


def snap_matches(outdir, snap_name, file_name, stage, what):
    sp = os.path.join(outdir, "_snap", snap_name)
    if not os.path.exists(sp):
        err("stage %s: _snap/%s was not written; %s is proved by that snap and by nothing else" % (stage, snap_name, what))
        return False
    fp = os.path.join(outdir, file_name)
    if not os.path.exists(fp):
        err("stage %s: %s is not in the output directory" % (stage, file_name))
        return False
    got = sha(fp)
    listed = None
    for line in open(sp, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.rstrip("\n").split("  ", 3)
        if len(parts) == 4 and parts[3] == file_name:
            listed = parts[0]
    if listed is None:
        err("stage %s: _snap/%s does not list %s; the file was written after the snap" % (stage, snap_name, file_name))
        return False
    if listed != got:
        err("stage %s: %s changed after _snap/%s was taken; %s rests on that file not moving" % (stage, file_name, snap_name, what))
        return False
    return True


def diary_lines(outdir, stage):
    """The running diary's lines for a stage (out/diary/*.jsonl, harness-stamped by mem.py log)."""
    rows = []
    for p in sorted(glob.glob(os.path.join(outdir, "diary", "*.jsonl")), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", os.path.basename(p))]):   # A1-10 after A1-9 (2026-10-07)
        for r in jsonl(p) or []:
            if str(r.get("stage")) == stage:
                rows.append(r)
    return rows


def cites_resolve(outdir, root, quotes, where):
    """Every quote resolves through the store's participant words (rule 3): the words must be a
    substring of some code's text. Returns the misses."""
    ctx = {"package": os.path.join(root, "package")}
    store_codes(ctx)
    texts = list(ctx["code_text"].values())
    misses = []
    for q in quotes:
        w = " ".join(str(q).split())
        if not w:
            continue
        if not any(w in " ".join(t.split()) for t in texts):
            misses.append(q)
    for q in misses:
        err("%s: quote does not resolve to a participant's words in the store: %r" % (where, str(q)[:80]),
            shape="quote:%s" % where, where=str(q)[:60])
    return misses


def canon(name, frame=None):
    """A room name as the frame spells it: `r/` stripped, case folded to the frame's spelling. A
    name the frame does not hold comes back stripped and unchanged in case."""
    n = str(name or "").strip()
    n = n[2:] if n.lower().startswith("r/") else n
    if frame:
        low = {s.lower(): s for s in frame}
        return low.get(n.lower(), n)
    return n


def b1_progress(outdir, themes, analysed=None, order=None):
    """Stage B1's walk in its seeded order. A room is done when every one of its second-order themes
    is placed in scheme/scheme_current.jsonl (by id or by its label) or listed in unplaced-B1.jsonl.
    Returns (order, done, left) where left maps a room to its themes not yet placed; order is None
    when the analysed set is empty. The order is B1's seeded random order (tools/saturation.py)."""
    import json as _j
    def rows(p):
        try:
            return [_j.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
        except (OSError, ValueError):
            return []
    if order is None:                    # the seeded random order of tools/saturation.py
        import saturation
        root = os.path.dirname(os.path.abspath(outdir))
        an = analysed if analysed is not None else set(saturation.analysed(root, outdir))
        order = saturation.shuffled(sorted(an), saturation.seed(root), "B1")
    if not order:
        return None, set(), {}
    with_themes = {canon(t.get("sub")) for t in themes}
    order = [canon(s) for s in order if (analysed is None or canon(s) in analysed) and canon(s) in with_themes]
    placed = set()                       # a room with no second-order theme has nothing to place: not in the walk
    cur = os.path.join(outdir, "scheme", "scheme_current.jsonl")
    if not os.path.exists(cur):
        cur = os.path.join(outdir, "scheme_current.jsonl")
    for r in rows(cur):
        for m in r.get("members") or []:
            placed.add((canon(m.get("sub")).lower(), " ".join(str(m.get("second_order") or "").split())))
    for r in rows(os.path.join(outdir, "unplaced-B1.jsonl")):
        placed.add((canon(r.get("sub")).lower(), " ".join(str(r.get("second_order") or "").split())))
    left = {}
    for t in themes:
        s = canon(t.get("sub"))
        if s not in order:
            continue
        keys = {str(t.get("theme_id") or ""), " ".join(str(t.get("second_order") or "").split())}
        if not any((s.lower(), k) in placed for k in keys if k):
            left.setdefault(s, []).append(t.get("theme_id"))
    done = {s for s in order if s not in left}
    return order, done, left


# ---- gates, rechecks and the concepts behind a placement (J, 2026-10-11) -------------------------
# The B1e interview asked for a check that the gates agree with one another, for a recheck of the
# placements a gate change could move, and for every placement to name the concepts that carry each
# third-order theme it places. mem.py (gates, gate, recheck, rechecks) and the stage checks share
# what follows.

GATE_TEXT_FIELDS = ("must_show", "must_not_show", "decide_when_both", "is_not")
GATE_FIELDS = GATE_TEXT_FIELDS + ("discriminators",)
T3_REF = re.compile(r"\bT3-\d{3}\b")
FAM_REF = re.compile(r"\bG\d{2,3}\b")
RECHECK_ALL = 30           # a change owes every placement it could move, up to this many ...
RECHECK_ESCALATE = 0.10    # ... else a seeded sample of this many, and all of them once more than this share of the sample moved
RULE_DATE = "2026-10-11T17:00:00"   # lines stamped before it were written under the earlier rules


def gate_scheme(outdir):
    """The scheme whose gates are in force: scheme_v2, else scheme_final, else scheme.jsonl (the
    working grouping in scheme_current holds no gates). ({id: row}, file name), or ({}, None)."""
    for name in ("scheme_v2.jsonl", "scheme_final.jsonl", "scheme.jsonl"):
        for d in ("", "scheme"):
            p = os.path.join(outdir, d, name)
            if os.path.exists(p):
                rows = {}
                for r in jsonl(p) or []:
                    i = r.get("id") or r.get("theme")
                    if i:
                        rows[i] = r
                if rows:
                    return rows, os.path.join(d, name)
    return {}, None


def family_ids(outdir):
    return {r.get("family") for r in (jsonl(os.path.join(outdir, "families.jsonl")) or []) if r.get("family")}


def _flat(v):
    if v is None:
        return ""
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def discriminators(row):
    """[(vs, question)] of one theme, from a list of {vs, question} (or a {vs: question} object)."""
    d = row.get("discriminators") or []
    if isinstance(d, dict):
        d = [{"vs": k, "question": v} for k, v in d.items()]
    out = []
    for x in d if isinstance(d, list) else []:
        if isinstance(x, dict):
            vs = x.get("vs")
            for v in (vs if isinstance(vs, list) else [vs]):
                if v:
                    out.append((str(v), _flat(x.get("question") or x.get("text") or x.get("test"))))
        elif isinstance(x, str):
            for v in T3_REF.findall(x):
                out.append((v, x))
    return out


def gate_refs(row):
    """{field: the ids it names}, for the four gate sentences, and the discriminators by their `vs`."""
    me = row.get("id") or row.get("theme")
    refs = {f: (set(T3_REF.findall(_flat(row.get(f)))) | set(FAM_REF.findall(_flat(row.get(f))))) - {me}
            for f in GATE_TEXT_FIELDS}
    refs["discriminators"] = {v for v, _ in discriminators(row)} - {me}
    return refs


def gate_report(rows, families=()):
    """The mechanical half of the gate check, over {id: row}:
    unresolved [(A, field, id)]  an id a gate names that the scheme (or families.jsonl) lacks;
    one_way [(A, B)]             A has a discriminator against B and B none against A;
    mns_no_disc [(A, B)]         A's must_not_show sends material to B with no discriminator against B;
    pairs {frozenset}            every pair of themes whose gates name each other."""
    ids, fams = set(rows), set(families or ())
    R = {i: gate_refs(r) for i, r in rows.items()}
    out = {"unresolved": [], "one_way": [], "mns_no_disc": [], "pairs": set()}
    for a, refs in sorted(R.items()):
        for f in GATE_FIELDS:
            for x in sorted(refs[f]):
                if T3_REF.fullmatch(x):
                    if x in ids:
                        out["pairs"].add(frozenset((a, x)))
                    else:
                        out["unresolved"].append((a, f, x))
                elif FAM_REF.fullmatch(x):
                    if fams and x not in fams:
                        out["unresolved"].append((a, f, x))
                else:
                    out["unresolved"].append((a, f, x))
        for b in sorted(refs["discriminators"]):
            if b in ids and a not in R[b]["discriminators"]:
                out["one_way"].append((a, b))
        for b in sorted(refs["must_not_show"]):
            if b in ids and b not in refs["discriminators"]:
                out["mns_no_disc"].append((a, b))
    return out


def gate_hash(rows, a, b):
    """A fingerprint of both themes' gates, so a confirmation goes stale when either changes."""
    h = hashlib.sha256()
    for i in sorted((a, b)):
        r = rows.get(i) or {}
        h.update(json.dumps({f: r.get(f) for f in GATE_FIELDS}, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return h.hexdigest()[:16]


def _clauses(text, ref):
    parts = re.split(r";\s+|(?<=[.!?])\s+", _flat(text))
    return [p.strip() for p in parts if ref in p]


def pair_lines(rows, a, b):
    """The two themes' sentences about each other, side by side, for a reader to judge."""
    L = []
    for x, y in ((a, b), (b, a)):
        r = rows.get(x) or {}
        L.append("%s  %s" % (x, r.get("name") or r.get("label") or ""))
        L.append("  must_show: %s" % _flat(r.get("must_show")))
        for f in ("must_not_show", "decide_when_both", "is_not"):
            for c in _clauses(r.get(f), y):
                L.append("  %s naming %s: %s" % (f, y, c))
        d = [q for v, q in discriminators(r) if v == y]
        L.append("  discriminator against %s: %s" % (y, d[0] if d else "NONE"))
        L.append("")
    return L


def gate_confirmations(outdir, rows):
    """{frozenset(A, B): ("confirmed" | "stale", line)} from out/gate_checks.jsonl, the latest line per pair."""
    out = {}
    for r in jsonl(os.path.join(outdir, "gate_checks.jsonl")) or []:
        p = r.get("pair") or []
        if len(p) == 2:
            k = frozenset(p)
            out[k] = ("confirmed" if r.get("hash") == gate_hash(rows, p[0], p[1]) else "stale", r)
    return out


class Owner(str):
    """A concept's second-order theme, remembering the themes it was split from (J, 2026-10-12, QB2-011): a
    record made before a split names the parent, one made after names the child, and both are right."""
    lineage = ()


def owns(th, tid):
    """Whether the concept whose theme is th belongs to tid: its own theme, or one it was split from."""
    return th == tid or tid in getattr(th, "lineage", ())


def code_themes(rows):
    """(sub, code_id) -> the second-order theme id it belongs to, from the store's codes rows (read through
    recut_overlay, a split concept's theme carries its parents in .lineage)."""
    out = {}
    for c in rows:
        o = Owner(c.get("theme_id") or c.get("case_theme_id") or "")
        o.lineage = tuple(c.get("split_lineage") or ())
        out[(c.get("sub"), c.get("code_id"))] = o if str(o) else None
    return out


def support_problems(mapping, placed, sub, tid, ct):
    """What is wrong with `support_by_theme`, {third-order id: [concept ids]}, for one placement `placed`
    (primary first) of the second-order theme sub/tid; ct is code_themes() of the store."""
    if not isinstance(mapping, dict):
        return ["support_by_theme is not an object {third-order id: [concept ids]}"]
    P = []
    for t in placed:
        if not mapping.get(t):
            P.append("%s names no concept in support_by_theme" % t)
    for t, cs in mapping.items():
        if t not in placed:
            P.append("support_by_theme names %s, which the placement does not hold" % t)
        for c in (cs if isinstance(cs, list) else [cs]):
            th = ct.get((sub, c))
            if th is None:
                P.append("%s is not a concept of r/%s" % (c, sub))
            elif tid and not owns(th, tid):
                P.append("%s is a concept of %s/%s, not of %s" % (c, sub, th, tid))
    prim = set(mapping.get(placed[0]) or []) if placed else set()
    for t in placed[1:]:
        if mapping.get(t) and not set(mapping.get(t)) - prim:
            P.append("%s has no concept of its own (rule 0's distinct support)" % t)
    return P


def also_present_problems(ap, placed, sub, tid, ct, scheme_ids=None):
    """What is wrong with `also_present`, {third-order id: [concept ids]}: the themes beyond the one a
    bag places (rule 0, J 2026-10-11), each with its own concepts."""
    if ap in (None, {}):
        return []
    if not isinstance(ap, dict):
        return ["also_present is not an object {third-order id: [concept ids]}"]
    P = []
    for t, cs in ap.items():
        if scheme_ids and t not in scheme_ids:
            P.append("also_present names %s, which the scheme does not define" % t)
        if t in (placed or []):
            P.append("also_present names %s, which the line places" % t)
        cs = cs if isinstance(cs, list) else [cs]
        if not cs:
            P.append("also_present names %s with no concept" % t)
        for c in cs:
            th = ct.get((sub, c))
            if th is None:
                P.append("%s is not a concept of r/%s" % (c, sub))
            elif tid and not owns(th, tid):
                P.append("%s is a concept of %s/%s, not of %s" % (c, sub, th, tid))
    return P


def parse_support(text, themes):
    """--codes for a placement: "T3-a=c1,c2;T3-b=c3", or "c1,c2" when one theme is placed."""
    text = str(text or "").strip()
    if not text:
        return None
    if "=" not in text:
        return {themes[0]: [c.strip() for c in text.split(",") if c.strip()]} if len(themes) == 1 else None
    out = {}
    for part in re.split(r"[;\s]+(?=T3-)", text):
        k, _, v = part.partition("=")
        if k.strip():
            out[k.strip()] = [c.strip() for c in v.replace(";", ",").split(",") if c.strip()]
    return out


# ---- the rechecks a gate change owes -----------------------------------------------------------

def gate_changes(outdir, stage):
    """A stage's gate changes, each with its ref: at B2 the lines of scheme_edits.jsonl (edit:<n>);
    elsewhere that stage's lines of gate_history.jsonl (gate:<n>, n counting every line of the file)."""
    stage = str(stage).upper()
    if stage == "B2":           # a gate-check mirror copies a question already in force and owes no recheck (QB2-003)
        return [dict(r, ref="edit:%d" % i) for i, r in enumerate(jsonl(os.path.join(outdir, "scheme_edits.jsonl")) or [], 1)
                if r.get("kind") != "gate-check"]
    return [dict(r, ref="gate:%d" % i) for i, r in enumerate(jsonl(os.path.join(outdir, "gate_history.jsonl")) or [], 1)
            if str(r.get("stage") or "").upper() == stage]


def touched(change):
    """The third-order themes a change names: the edited one, and every id its old or new sentence names."""
    t = {change.get("theme")} if change.get("theme") else set()
    for f in ("was", "now"):
        t |= set(T3_REF.findall(_flat(change.get(f))))
    return {x for x in t if x}


def placed_items(outdir, stage):
    """(sub, theme_id) -> {"source", "third_order"}: the placements a gate change at this stage can
    move. B1: the working grouping (scheme_current members); B2: your own placements
    (author_items.jsonl and gold_items.jsonl); C1 on: assignments_final.jsonl."""
    out, stage = {}, str(stage).upper()
    if stage == "B1":
        p = os.path.join(outdir, "scheme", "scheme_current.jsonl")
        if not os.path.exists(p):
            p = os.path.join(outdir, "scheme_current.jsonl")
        for r in jsonl(p) or []:
            for m in r.get("members") or []:
                if isinstance(m, dict) and m.get("sub") and m.get("theme_id"):
                    e = out.setdefault((m["sub"], m["theme_id"]), {"source": "scheme_current.jsonl", "third_order": []})
                    e["third_order"].append(r.get("theme") or r.get("id"))
        return out
    names = ("author_items.jsonl", "gold_items.jsonl") if stage == "B2" else ("assignments_final.jsonl",)
    for name in names:
        for r in jsonl(os.path.join(outdir, name)) or []:
            so = r.get("third_order") or []
            out[(r.get("sub"), r.get("theme_id"))] = {"source": name, "third_order": list(so) if isinstance(so, list) else [so]}
    return out


def recheck_lines(outdir, stage):
    return jsonl(os.path.join(outdir, "rechecks-%s.jsonl" % str(stage).upper())) or []


def draw_owed(cands, stage, ref):
    """Every candidate up to RECHECK_ALL, else a seeded sample of RECHECK_ALL (the seed is the change)."""
    import random
    cands = sorted(cands)
    if len(cands) <= RECHECK_ALL:
        return cands, False
    return sorted(random.Random("%s|%s" % (stage, ref)).sample(cands, RECHECK_ALL)), True


def owed_rechecks(outdir, stage):
    """For every gate change of the stage: the placements it could move, those it owes, those done and
    those missing. At B2 the candidates are your placements as they stood before the change (the
    earlier changes' rechecks applied, in order); after B1 `mem.py gate` stores them on its line."""
    stage = str(stage).upper()
    done = collections.defaultdict(dict)
    for r in recheck_lines(outdir, stage):
        done[r.get("change")][(r.get("sub"), r.get("theme_id"))] = r
    items = placed_items(outdir, stage)
    out = []
    for ch in gate_changes(outdir, stage):
        ref, th = ch["ref"], touched(ch)
        if ch.get("candidates_list") is not None:
            cands = [tuple(x) for x in ch["candidates_list"]]
        else:
            cands = [k for k, v in items.items() if set(v["third_order"]) & th]
        if ch.get("owed") is not None:
            owed, sampled = [tuple(x) for x in ch["owed"]], len(ch["owed"]) < len(cands)
        else:
            owed, sampled = draw_owed(cands, stage, ref)
        d = done.get(ref, {})
        moved = sum(1 for k in owed if k in d and d[k].get("changed"))
        checked = sum(1 for k in owed if k in d)
        escalated = bool(sampled and checked and moved / float(checked) > RECHECK_ESCALATE)
        if escalated:
            owed = sorted(cands)
        out.append({"ref": ref, "theme": ch.get("theme"), "field": ch.get("field"), "touched": sorted(th),
                    "candidates": sorted(cands), "owed": owed, "done": d, "sampled": sampled,
                    "before": {k: list((items.get(k) or {}).get("third_order") or []) for k in cands},
                    "source": {k: (items.get(k) or {}).get("source") for k in cands},
                    "escalated": escalated, "moved": sum(1 for r in d.values() if r.get("changed")),
                    "missing": [k for k in owed if k not in d]})
        if stage == "B2":                      # the next change starts from the placements as rechecked
            for k, r in d.items():
                if k in items and r.get("now"):
                    items[k] = dict(items[k], third_order=list(r["now"]))
    return out


def recheck_errors(outdir, stage, ct=None, scheme_ids=None):
    """The checks' half: every owed recheck done, and every recheck line well formed."""
    stage = str(stage).upper()
    name = "scheme_edits.jsonl" if stage == "B2" else "gate_history.jsonl"
    n = 0
    for o in owed_rechecks(outdir, stage):
        if o["missing"]:
            n += 1
            err("%s %s (%s, %s) owes rechecks of %d placement(s) it could move and %d are not done (%s%s); "
                "mem.py rechecks --owed lists them, mem.py recheck records each (J, 2026-10-11)"
                % (name, o["ref"], o["theme"], o["field"], len(o["owed"]), len(o["missing"]),
                   ", ".join("%s/%s" % k for k in o["missing"][:4]), " ..." if len(o["missing"]) > 4 else ""),
                shape="%s: a gate change with rechecks owed" % name, where=o["ref"])
    refs = {c["ref"] for c in gate_changes(outdir, stage)}
    for i, r in enumerate(recheck_lines(outdir, stage), 1):
        w = "line %d" % i
        if r.get("change") not in refs:
            err("rechecks-%s.jsonl line %d names change %r, which %s does not hold" % (stage, i, r.get("change"), name),
                shape="rechecks-%s.jsonl: a recheck of no change" % stage, where=w)
        now = r.get("now") or []
        if not isinstance(now, list) or not now or len(now) > 3:
            err("rechecks-%s.jsonl line %d: now is %r; one to three third-order ids, primary first (rule 0)" % (stage, i, now),
                shape="rechecks-%s.jsonl: now not one to three ids" % stage, where=w)
            continue
        for s in now:
            if scheme_ids and s not in scheme_ids:
                err("rechecks-%s.jsonl line %d places on %s, which the scheme does not define" % (stage, i, s),
                    shape="rechecks-%s.jsonl: an id the scheme does not define" % stage, where=w)
        if ct is not None:
            for p in support_problems(r.get("support_by_theme"), now, r.get("sub"), r.get("theme_id"), ct):
                err("rechecks-%s.jsonl line %d (%s/%s): %s" % (stage, i, r.get("sub"), r.get("theme_id"), p),
                    shape="rechecks-%s.jsonl: support" % stage, where=w)
        if not r.get("why"):
            err("rechecks-%s.jsonl line %d has no why" % (stage, i), shape="rechecks-%s.jsonl: no why" % stage, where=w)
    return n


def gate_warnings(outdir, rows, name, as_errors=False, edited=None):
    """The gate check as the stage checks report it: one-way discriminators, must_not_show lines with
    no discriminator, unresolved ids (errors when as_errors, at a freeze), and the pairs of the
    edited themes that were not confirmed against their current sentences."""
    rep = gate_report(rows, family_ids(outdir))
    say = err if as_errors else warn
    for a, f, x in rep["unresolved"]:
        say("%s: %s's %s names %s, which the scheme does not define" % (name, a, f, x),
            shape="%s: a gate names an id the scheme lacks" % name, where="%s %s" % (a, f))
    for a, b in rep["one_way"]:
        say("%s: %s has a discriminator against %s and %s none against %s; discriminators run both ways "
            "(mem.py gates %s %s)" % (name, a, b, b, a, a, b),
            shape="%s: a discriminator that runs one way" % name, where="%s|%s" % (a, b))
    for a, b in rep["mns_no_disc"]:
        say("%s: %s's must_not_show sends material to %s and %s has no discriminator against %s (mem.py gates %s %s)"
            % (name, a, b, a, b, a, b), shape="%s: must_not_show with no discriminator" % name, where="%s|%s" % (a, b))
    if edited:
        conf = gate_confirmations(outdir, rows)
        for p in sorted(rep["pairs"], key=sorted):
            if p & set(edited) and (conf.get(p, ("none",))[0] != "confirmed"):
                a, b = sorted(p)
                warn("%s: the pair %s|%s touches an edited theme and is not confirmed against its current sentences "
                     "(mem.py gates %s %s --confirm --reason ...)" % (name, a, b, a, b),
                     shape="%s: an edited pair not confirmed" % name, where="%s|%s" % (a, b))
    return rep


# ---- the split layer and the fleet ids (J, 2026-10-12, QB2-010 and QB2-009) -------------------------------
# A second-order theme too coarse for one, two or three third-order themes is split by the analyst into
# children (mem.py split). The store stays read-only; the children live in out/recut/: themes.jsonl (one line
# per child, with its parent) and codes.jsonl (each moved concept's new theme). Every reader of the store's
# codes and themes reads them through recut_overlay, so a superseded parent is gone and its children stand
# in its place. A child split again is itself superseded the same way.

def recut_overlay(name, rows, outdir):
    """The store's rows of `name` ("themes" or "codes") with out/recut/ laid over them; other names unchanged."""
    if name not in ("themes", "codes") or not outdir:
        return rows
    d = os.path.join(outdir, "recut")
    tp = os.path.join(d, "themes.jsonl")
    if not os.path.exists(tp):
        return rows
    kids = jsonl(tp) or []
    if os.path.exists(os.path.join(d, "WITHDRAWN.json")):
        # J, 2026-10-12: the split is withdrawn (second-order themes are the coders' to cut, not the aggregator's).
        # The parents stand again; a concept keeps its children in .lineage only, so a record made while the
        # split stood still resolves, and nothing written under out/recut/ is deleted
        if name == "themes":
            return rows
        kid_of = {}
        for c in jsonl(os.path.join(d, "codes.jsonl")) or []:
            kid_of.setdefault((c.get("sub"), c.get("code_id")), []).append(c.get("theme_id"))
        out = []
        for r in rows:
            k = kid_of.get((r.get("sub"), r.get("code_id")))
            if k:
                r = dict(r)
                r["split_lineage"] = k
            out.append(r)
        return out
    gone = {(k.get("sub"), k.get("parent")) for k in kids}
    if name == "themes":
        keep = [r for r in rows if (r.get("sub"), r.get("theme_id")) not in gone]
        keep += [k for k in kids if (k.get("sub"), k.get("theme_id")) not in gone]
        return keep
    moved, lineage = {}, {}
    for c in jsonl(os.path.join(d, "codes.jsonl")) or []:
        k = (c.get("sub"), c.get("code_id"))
        moved[k] = c                                          # the latest line wins: a child split again
        lineage.setdefault(k, []).append(c.get("parent"))
    if not moved:
        return rows
    out = []
    for r in rows:
        m = moved.get((r.get("sub"), r.get("code_id")))
        if m:
            r = dict(r)
            r["theme_id"] = m.get("theme_id")
            r["second_order"] = m.get("second_order", r.get("second_order"))
            r["split_from"] = m.get("parent")
            r["split_lineage"] = lineage.get((r.get("sub"), r.get("code_id")), [])
        out.append(r)
    return out


def fleet_table(outdir):
    """(by fleet id, by (kind, sub, room id)) from out/fleet_ids.jsonl, or (None, None) when there is none."""
    p = os.path.join(outdir, "fleet_ids.jsonl")
    if not os.path.exists(p):
        return None, None
    rows = jsonl(p) or []
    return ({r["fleet"]: r for r in rows}, {(r["kind"], r["sub"], r["id"]): r["fleet"] for r in rows})


def fleet_translate(r, by_fleet):
    """A return line written in fleet ids, read back into room ids (a copy). Lines already in room ids, and
    ids the table does not hold, are left as written, so the checks still see an invented id as invented."""
    if not by_fleet or not isinstance(r, dict):
        return r
    r = dict(r)
    t = by_fleet.get(r.get("theme_id"))
    if t and t.get("kind") == "t":
        r["theme_id"] = t["id"]
        r["sub"] = t["sub"]
    def c(x):
        # a code of another room keeps its room in the id, so it can never resolve inside this one
        e = by_fleet.get(x) if isinstance(x, str) else None
        if not e or e.get("kind") != "c":
            return x
        return e["id"] if e["sub"] == r.get("sub") else "%s:%s" % (e["sub"], e["id"])
    if isinstance(r.get("support"), list):
        r["support"] = [c(x) for x in r["support"]]
    if isinstance(r.get("also_present"), dict):
        r["also_present"] = {k: [c(x) for x in (v or [])] for k, v in r["also_present"].items()}
    ml = r.get("multiplacement_log")
    if isinstance(ml, dict):
        r["multiplacement_log"] = {k: ([c(x) for x in v] if isinstance(v, list) else v) for k, v in ml.items()}
    return r
