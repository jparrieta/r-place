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
