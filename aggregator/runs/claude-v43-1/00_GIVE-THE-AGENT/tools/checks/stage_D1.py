"""checks/stage_D1.py: the close-check of stage D1, the return's build, v38.

Written from stages/STAGE-D1-adaptation-return-build.md (its Outputs block, §1 the handoff folder, §2 the
verdict packets, §3 the payload, §4 what you check), SCHEMA-adaptations.md §1 and §9, FLEET.md
§1 and §3, contract rules 6, 7 and 19, and from the v37 check it descends from
(_v37-source/tools/validate.py, stage10). What it checks is the SHAPE of the handoff: every
served file exists, the vocabulary is the projection of model/ at one version, VERSION is that
version, every id a task names resolves, every room of the analysed set has a task, an index row
and a verdict packet, the expectations are written and sealed away from the served folders, and
nothing served carries a canvas field. It cannot check whether the model is right.

    def check(root, outdir, ctx): ...

Definitions this module fixes, because handoff.py writes the folder and no other file states
them (TOOLS-STATUS.md). handoff.py adopts them; a change to either is made in both:

- model_hash(outdir): vlib.model_hash, sha256 over the model and its tiers (vlib.MODEL_FILES), each file's
  bytes preceded by its relative name and a newline; VERSION is that digest, bare or with a `sha256:`
  prefix. It covers the elements, the arrows, the fourth-order themes, the dimensions, scheme_v2 and
  assignments_final; history.jsonl is not in it, so a history line that changes nothing else does not
  move it.
- folder_hash(handoff-D): sha256 over "<relative path>  <file sha256>\\n" for every file under
  the folder in sorted order, `recheck/` excluded. notes-D1.md and RUN.json carry it.
- A verdict packet is `verdict-D/<sub>.md`, written by handoff.py beside RETURN-D2v.md and its schema;
  fleet.py names the raw return folder after the packet's stem, so the stem is the room.
- VOCABULARY.json: {"elements": [...], "arrows": [...], "third": [...], "fourth": [...],
  "dimensions": [...]} with an optional "version"; arrows may instead sit inside "elements"
  with kind "arrow", which is how ingest.py resolves them.

Not carried from v37's stage10 (the composition fleet's check): author_compositions.jsonl and
its floor of thirty (the analyst no longer composes rooms; labelers and a fleet do), the
composition_brief.md digest, composition_raw.jsonl and composition.jsonl (the verdicts are
D2's, verdicts-D.jsonl), transmission-D.md and its licence sentence (no fidelity figure is
computed at D1), operator_draw-D.json, the §7 counts (D3 computes them last).

The common checks in validate.py already require the diary lines and the head; they are not
repeated here.
"""
import collections, glob, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

HAND = "handoff-D"
VERD = "verdict-D"
PACKET_CEILING = 50 * 1024
ELEMENT_KINDS = ("process", "condition", "claim", "role", "arrow")
VOCAB_KEYS = ("elements", "arrows", "third", "fourth", "dimensions")
VOCAB_EXTRA_OK = ("version", "model_version")
ELEMENT_FIELDS = ("id", "kind", "statement", "tier", "dimension")
ARROW_FIELDS = ("id", "kind", "from", "to", "mechanism")
ARROW_KINDS = ("order", "transition", "co-occurrence")
CANVAS_RE = re.compile(r"\bcanvas_[a-z_]+\b")
HEX64 = re.compile(r"\b[0-9a-f]{64}\b")
ANY_ID = re.compile(r"\b(T3-\d{3}|T4-\d{3}|D\d{1,2}|[PKCRA]\d{2})\b")
EXPECT_FIELDS = ("sub", "expect_instantiate", "expect_absent", "from", "why")
EXPECT_OPTIONAL = ("not_testable_here",)
TASK_REQUIRED = ("TASK.md", "case.md", "codes.jsonl", "themes.jsonl", "placements.jsonl")
TASK_USUAL = ("brief.md", "forest.md")


# ---- helpers other 10x modules import ------------------------------------------------------

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def model_hash(outdir):
    """The version of model/ as this module defines it (see the docstring). None when
    elements.jsonl is absent."""
    return vlib.model_hash(outdir)


def bare_hash(s):
    s = (s or "").strip()
    return s[7:] if s.startswith("sha256:") else s


def folder_hash(folder, exclude=("recheck",)):
    rows = []
    for d, dirs, files in os.walk(folder):
        dirs[:] = sorted(x for x in dirs if x not in exclude)
        for f in sorted(files):
            p = os.path.join(d, f)
            rows.append("%s  %s\n" % (os.path.relpath(p, folder), vlib.sha(p)))
    return sha_bytes("".join(rows).encode("utf-8"))


def read_version(outdir, sub=""):
    p = os.path.join(outdir, HAND, sub, "VERSION") if sub else os.path.join(outdir, HAND, "VERSION")
    if not os.path.exists(p):
        return None
    return bare_hash(open(p, encoding="utf-8").read())


def load_vocab(outdir, sub=""):
    """VOCABULARY.json as a dict of id sets: elements (elements and arrows), third, fourth,
    dimensions, plus the element rows by id; None when absent or unparsable (having said so)."""
    p = os.path.join(outdir, HAND, sub, "VOCABULARY.json") if sub else os.path.join(outdir, HAND, "VOCABULARY.json")
    if not os.path.exists(p):
        return None
    try:
        v = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        err("%s will not parse as JSON: %s" % (os.path.relpath(p, outdir), e))
        return None
    if not isinstance(v, dict):
        err("%s is not a JSON object with elements, arrows, third, fourth and dimensions" % os.path.relpath(p, outdir))
        return None
    rows = list(v.get("elements") or []) + list(v.get("arrows") or [])
    out = {"raw": v, "path": p,
           "elements": {r.get("id"): r for r in rows if isinstance(r, dict)},
           "third": {r.get("id") for r in (v.get("third") or []) if isinstance(r, dict)},
           "fourth": {r.get("id") for r in (v.get("fourth") or []) if isinstance(r, dict)},
           "dimensions": {r.get("id") for r in (v.get("dimensions") or []) if isinstance(r, dict)}}
    return out


def model_rows(outdir):
    """(elements by id, arrows by id) from model/, rows as written; {} when absent."""
    md = os.path.join(outdir, "model")
    els = {r.get("id"): r for r in (jsonl(os.path.join(md, "elements.jsonl")) or []) if r.get("id")}
    ars = {r.get("id"): r for r in (jsonl(os.path.join(md, "arrows.jsonl")) or []) if r.get("id")}
    return els, ars


def canvas_hits(path):
    """The canvas field names a served file carries (rule 7): vlib.CANVAS and any canvas_* name."""
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    hits = {m for m in CANVAS_RE.findall(t)} | {c for c in vlib.CANVAS if c in t}
    return sorted(hits)


def scan_canvas(outdir, folders, stage):
    for folder in folders:
        base = os.path.join(outdir, folder)
        for d, _dirs, files in os.walk(base):
            for f in files:
                p = os.path.join(d, f)
                hits = canvas_hits(p)
                if hits:
                    rel = os.path.relpath(p, outdir)
                    err("stage %s: %s is served and carries a canvas field (%s); the fleets and labelers are "
                        "never served the canvas (rule 7). Rebuild the file without it." % (stage, rel, ", ".join(hits)),
                        shape="canvas:%s" % folder, where=rel)


def ids_in(txt):
    return set(ANY_ID.findall(txt or ""))


def id_resolves(i, vocab):
    if vlib.T3.match(i):
        return i in vocab["third"]
    if vlib.T4.match(i):
        return i in vocab["fourth"]
    if vlib.DIM.match(i):
        return i in vocab["dimensions"]
    return i in vocab["elements"]


def packet_path(outdir, sub):
    p = os.path.join(outdir, VERD, "%s.md" % sub)
    if os.path.exists(p):
        return p
    c = glob.glob(os.path.join(outdir, VERD, "**", "%s.md" % sub), recursive=True)
    return c[0] if c else None


def last_story(outdir):
    stories = sorted(glob.glob(os.path.join(outdir, "story_rooms-p*.jsonl")),
                     key=lambda p: int(re.search(r"p(\d+)", os.path.basename(p)).group(1)))
    return stories


# ---- the check --------------------------------------------------------------------------------

def check_vocabulary(outdir, vocab, els, ars):
    raw, rel = vocab["raw"], os.path.relpath(vocab["path"], outdir)
    extra = [k for k in raw if k not in VOCAB_KEYS and k not in VOCAB_EXTRA_OK]
    if extra:
        err("%s carries keys beyond elements, arrows, third, fourth and dimensions: %s. The vocabulary is "
            "the projection and nothing else (SCHEMA §1); rebuild it." % (rel, extra))
    for k in ("elements", "third", "fourth", "dimensions"):
        if not raw.get(k):
            err("%s has no %r list; the labelers cannot name what it does not hold" % (rel, k))
    for r in list(raw.get("elements") or []) + list(raw.get("arrows") or []):
        if not isinstance(r, dict):
            err("%s: an element entry is not an object" % rel, shape="vocab:notobj"); continue
        i = r.get("id") or "?"
        if not (vlib.ELEMENT.match(i) or vlib.ARROW.match(i)):
            err("%s: element id %r is not P/K/C/R/A plus two digits" % (rel, i), shape="vocab:badid", where=i)
        is_arrow = bool(vlib.ARROW.match(i))
        fields = ARROW_FIELDS if is_arrow else ELEMENT_FIELDS
        miss = [f for f in fields if f not in r]
        if miss:
            err("%s: %s lacks %s; every %s carries %s" % (rel, i, miss, "arrow" if is_arrow else "element",
                ", ".join(fields)), shape="vocab:fields", where=i)
        more = [f for f in r if f not in fields and f != "status" and not (is_arrow and f == "statement")]
        if more:
            err("%s: %s carries %s beyond %s (SCHEMA §1: nothing else)" % (rel, i, more, ", ".join(fields)),
                shape="vocab:extra", where=i)
        if "status" in r and r["status"] != "tentative":
            err("%s: %s carries status %r; the only status a labeler sees is tentative (stage C4)" % (rel, i, r["status"]),
                shape="vocab:status", where=i)
        if r.get("kind") not in (ARROW_KINDS if is_arrow else ELEMENT_KINDS):
            err("%s: %s has kind %r, not one of %s" % (rel, i, r.get("kind"), ARROW_KINDS if is_arrow else ELEMENT_KINDS),
                shape="vocab:kind", where=i)
        for t in (r.get("tier") if isinstance(r.get("tier"), list) else [r.get("tier")]):   # as stage C2 allows
            if t not in (None, "") and not (vlib.T4.match(str(t)) or vlib.T3.match(str(t)) or vlib.DIM.match(str(t))
                                            or vlib.FORM_PASS.match(str(t))):
                err("%s: %s tier %r is not a third- or fourth-order theme, a dimension or an FP- finding"
                    % (rel, i, t), shape="vocab:tier", where=i)
        if r.get("dimension") not in (None, "") and not vlib.DIM.match(str(r["dimension"])):
            err("%s: %s dimension %r is not a dimension id" % (rel, i, r["dimension"]), shape="vocab:dim", where=i)
        elif r.get("dimension") and r["dimension"] not in vocab["dimensions"]:
            err("%s: %s names dimension %s, which the vocabulary's dimensions list does not hold"
                % (rel, i, r["dimension"]), shape="vocab:dimres", where=i)
        if r.get("status") == "withdrawn":
            err("%s: %s is withdrawn and still in the vocabulary; a labeler must not adapt it" % (rel, i),
                shape="vocab:withdrawn", where=i)
        # the projection of model/ at this version
        src = els.get(i) if i in els else ars.get(i)
        if src is None:
            err("%s: %s is not in model/elements.jsonl or model/arrows.jsonl; the vocabulary is projected from "
                "them and from nothing else" % (rel, i), shape="vocab:notinmodel", where=i)
        elif (src.get("statement") or "") != (r.get("statement") or ""):
            err("%s: %s's statement differs from model/; regenerate the vocabulary from the frozen model"
                % (rel, i), shape="vocab:statement", where=i)
    live = {i for i, r in els.items() if r.get("status") != "withdrawn"}
    live |= {i for i, r in ars.items() if r.get("status") != "withdrawn" and r.get("in_model", True)}
    missing = sorted(live - set(vocab["elements"]))
    if missing:
        err("%s lacks %d standing element(s) or arrow(s) of model/: %s. Every element and arrow at the frozen "
            "version is in the vocabulary." % (rel, len(missing), missing[:8]))
    for k, pat, what in (("third", vlib.T3, "third-order theme"), ("fourth", vlib.T4, "fourth-order theme"),
                         ("dimensions", vlib.DIM, "dimension")):
        for r in raw.get(k) or []:
            if not isinstance(r, dict) or not r.get("id"):
                err("%s: a %s entry has no id" % (rel, what), shape="vocab:%s:noid" % k); continue
            if not pat.match(str(r["id"])):
                err("%s: %s id %r has the wrong form" % (rel, what, r["id"]), shape="vocab:%s:form" % k, where=r["id"])
            if k != "dimensions" and not (r.get("name") or r.get("label")):
                err("%s: %s %s has no name" % (rel, what, r["id"]), shape="vocab:%s:name" % k, where=r["id"])
    scheme, sname = vlib.load_scheme(outdir)
    if scheme is None:
        err("no scheme file in the output directory, so the vocabulary's third-order ids were NOT checked")
    else:
        bad = sorted(vocab["third"] - scheme)
        if bad:
            err("%s names third-order themes not in %s: %s" % (rel, sname, bad[:8]))
    fourth = jsonl(os.path.join(outdir, "fourth", "fourth.jsonl"))
    if fourth is None:
        err("fourth/fourth.jsonl is not in the output directory, so the vocabulary's fourth-order ids were NOT checked")
    else:
        f4 = {r.get("id") for r in fourth}
        bad = sorted(vocab["fourth"] - f4)
        if bad:
            err("%s names fourth-order themes not in fourth/fourth.jsonl: %s" % (rel, bad[:8]))
    dims = jsonl(os.path.join(outdir, "dimensions.jsonl"))
    if dims is None:
        err("dimensions.jsonl is not in the output directory, so the vocabulary's dimension ids were NOT checked")
    else:
        dd = {r.get("id") for r in dims}
        bad = sorted(vocab["dimensions"] - dd)
        if bad:
            err("%s names dimensions not in dimensions.jsonl: %s" % (rel, bad[:8]))


def check_task(outdir, sub, vocab, ctx, themes):
    tdir = os.path.join(outdir, HAND, "tasks", sub)
    rel = os.path.relpath(tdir, outdir)
    for f in TASK_REQUIRED:
        if not os.path.exists(os.path.join(tdir, f)):
            err("%s/%s is missing; the task holds TASK.md and the room's documents (§1)" % (rel, f),
                shape="task:missing:%s" % f, where=sub)
    for f in TASK_USUAL:
        if not os.path.exists(os.path.join(tdir, f)):
            warn("%s/%s is not served; if the room has none, say so in handback-D1.md" % (rel, f),
                 shape="task:usual:%s" % f, where=sub)
    # the return specification, verbatim in every task; MODEL.md per task starts with the global one
    top = text(outdir, os.path.join(HAND, "RETURN-D.md"))
    mine = os.path.join(tdir, "RETURN-D.md")
    if os.path.exists(mine) and top and open(mine, encoding="utf-8").read() != top:
        err("%s/RETURN-D.md differs from handoff-D/RETURN-D.md; the specification is verbatim in every task"
            % rel, shape="task:return-differs", where=sub)
    gm = text(outdir, os.path.join(HAND, "MODEL.md"))
    mm = os.path.join(tdir, "MODEL.md")
    if os.path.exists(mm) and gm and not open(mm, encoding="utf-8").read().startswith(gm.rstrip()[:2000]):
        err("%s/MODEL.md does not begin with handoff-D/MODEL.md; the wiki pages are appended to the global "
            "model, which is not rewritten per task" % rel, shape="task:model-differs", where=sub)
    # only this room's material in the room's documents
    for f in ("codes.jsonl", "themes.jsonl", "placements.jsonl"):
        p = os.path.join(tdir, f)
        if not os.path.exists(p):
            continue
        rows = jsonl(p) or []
        others = sorted({r.get("sub") for r in rows if r.get("sub") and r.get("sub") != sub})
        if others:
            err("%s/%s carries lines of another room (%s); a task holds one room and no other (rule 7, §1)"
                % (rel, f, others[:3]), shape="task:otherroom", where=sub)
        if f == "placements.jsonl":
            for r in rows:
                tid = r.get("theme_id")
                if themes is not None and (sub, tid) not in themes:
                    err("%s/placements.jsonl names theme %r, not a second-order theme of r/%s in the store"
                        % (rel, tid, sub), shape="task:placement-theme", where="%s %s" % (sub, tid))
                for k in ("third_order", "fourth_order", "dimension"):
                    v = r.get(k)
                    vs = v if isinstance(v, list) else [v]
                    for x in vs:
                        if x not in (None, "", "none") and not id_resolves(str(x), vocab):
                            err("%s/placements.jsonl: %s %r does not resolve in VOCABULARY.json" % (rel, k, x),
                                shape="task:placement-id", where="%s %s" % (sub, x))
    # every id the instruction names resolves against the vocabulary
    for f in ("TASK.md",):
        p = os.path.join(tdir, f)
        if os.path.exists(p):
            bad = sorted(i for i in ids_in(open(p, encoding="utf-8", errors="replace").read()) if not id_resolves(i, vocab))
            if bad:
                err("%s/%s names ids not in VOCABULARY.json: %s; a labeler cannot resolve them" % (rel, f, bad[:6]),
                    shape="task:unresolved", where=sub)


def check_index(outdir, analysed):
    p = os.path.join(outdir, HAND, "tasks", "index.tsv")
    if not os.path.exists(p):
        return
    lines = [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]
    if not lines:
        err("handoff-D/tasks/index.tsv is empty; one row per room with items_in_window and the payload in bytes")
        return
    cols = lines[0].split("\t")
    lc = [c.strip().lower() for c in cols]
    if "sub" not in lc and "room" not in lc:
        err("handoff-D/tasks/index.tsv has no sub (or room) column")
        return
    si = lc.index("sub") if "sub" in lc else lc.index("room")
    if "items_in_window" not in lc:
        err("handoff-D/tasks/index.tsv has no items_in_window column; the handler dispatches by it")
    bi = [i for i, c in enumerate(lc) if "bytes" in c or "payload" in c]
    if not bi:
        err("handoff-D/tasks/index.tsv has no payload-in-bytes column (from mem.py room --size)")
    seen = collections.Counter()
    for n, l in enumerate(lines[1:], 2):
        cells = l.split("\t")
        if len(cells) != len(cols):
            err("handoff-D/tasks/index.tsv line %d has %d cells, header %d" % (n, len(cells), len(cols)),
                shape="index:cells", where="line %d" % n)
            continue
        sub = cells[si].strip()
        seen[sub] += 1
        if "items_in_window" in lc and not re.fullmatch(r"\d+", cells[lc.index("items_in_window")].strip()):
            err("handoff-D/tasks/index.tsv %s: items_in_window %r is not an integer" % (sub, cells[lc.index("items_in_window")]),
                shape="index:iiw", where=sub)
        for i in bi[:1]:
            if not re.fullmatch(r"\d+", cells[i].strip()):
                err("handoff-D/tasks/index.tsv %s: payload %r is not an integer of bytes" % (sub, cells[i]),
                    shape="index:bytes", where=sub)
    dup = [s for s, n in seen.items() if n > 1]
    if dup:
        err("handoff-D/tasks/index.tsv lists a room twice: %s" % dup[:5])
    if analysed is not None:
        miss = sorted(analysed - set(seen) - unbuilt_rooms(outdir))
        stray = sorted(set(seen) - analysed)
        if miss:
            err("handoff-D/tasks/index.tsv has no row for %d rooms of the analysed set: %s" % (len(miss), miss[:6]))
        if stray:
            err("handoff-D/tasks/index.tsv names rooms outside the analysed set: %s" % stray[:6])
    return seen


def unbuilt_rooms(outdir):
    """Rooms handoff.py could not build (UNBUILT.tsv) and the handback names (stage D1 section 4)."""
    p = os.path.join(outdir, HAND, "UNBUILT.tsv")
    if not os.path.exists(p):
        return set()
    hb = text(outdir, "handback-D1.md")
    rows = {l.split("\t")[0].strip() for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("sub\t")}
    for s in sorted(rows):
        if not re.search(r"\b%s\b" % re.escape(s), hb):
            err("handoff-D/UNBUILT.tsv lists r/%s and handback-D1.md does not name it with why (section 4)" % s,
                shape="unbuilt:unnamed", where=s)
    return rows


def check_expectations(outdir, vocab, analysed):
    p = os.path.join(outdir, "sealed", "EXPECTATIONS.jsonl")
    rows = jsonl(p)
    if rows is None:
        return
    seen = collections.Counter()
    for n, r in enumerate(rows, 1):
        sub = r.get("sub")
        seen[sub] += 1
        miss = [f for f in EXPECT_FIELDS if f not in r]
        if miss:
            err("EXPECTATIONS.jsonl line %d (%s) lacks %s; the line is sub, expect_instantiate, expect_absent, "
                "from, why" % (n, sub, miss), shape="expect:fields", where="line %d" % n)
        more = [f for f in r if f not in EXPECT_FIELDS and f not in EXPECT_OPTIONAL]
        if more:
            err("EXPECTATIONS.jsonl line %d (%s) carries %s beyond the five fields and not_testable_here"
                % (n, sub, more), shape="expect:extra", where="line %d" % n)
        for k in ("expect_instantiate", "expect_absent", "not_testable_here"):
            v = r.get(k)
            if k in r and not isinstance(v, list):
                err("EXPECTATIONS.jsonl %s: %s is not a list" % (sub, k), shape="expect:list", where=sub)
                continue
            for x in v or []:
                if not (vlib.ELEMENT.match(str(x)) or vlib.ARROW.match(str(x))) or str(x) not in vocab["elements"]:
                    err("EXPECTATIONS.jsonl %s: %s names %r, not an element or arrow of VOCABULARY.json"
                        % (sub, k, x), shape="expect:id", where="%s %s" % (sub, x))
        both = set(r.get("expect_instantiate") or []) & set(r.get("expect_absent") or [])
        if both:
            err("EXPECTATIONS.jsonl %s expects %s both to instantiate and to be absent" % (sub, sorted(both)),
                shape="expect:both", where=sub)
        if not isinstance(r.get("from"), list) or not r.get("from"):
            err("EXPECTATIONS.jsonl %s: from is not a non-empty list of sources (implications-C5, placements, ...)"
                % sub, shape="expect:from", where=sub)
        if not (r.get("why") or "").strip():
            err("EXPECTATIONS.jsonl %s: why is empty; one clause per element, in the model's terms" % sub,
                shape="expect:why", where=sub)
    dup = [s for s, n in seen.items() if n > 1]
    if dup:
        err("EXPECTATIONS.jsonl carries more than one line for %s; one line per room" % dup[:5])
    if analysed is not None:
        miss = sorted(analysed - set(seen))
        if miss:
            err("EXPECTATIONS.jsonl has no line for %d rooms of the analysed set: %s. The prediction is written "
                "before any return exists." % (len(miss), miss[:6]))
        stray = sorted(set(seen) - analysed)
        if stray:
            err("EXPECTATIONS.jsonl names rooms outside the analysed set: %s" % stray[:6])
    # sealed: outside both served folders
    for folder in (HAND, VERD):
        hits = glob.glob(os.path.join(outdir, folder, "**", "EXPECTATIONS*"), recursive=True)
        if hits:
            err("EXPECTATIONS.jsonl (or a copy) sits inside the served folder %s; it is kept outside the readers' "
                "and the labelers' directories and scored at E1" % folder)


def check_packets(outdir, analysed, ctx):
    spec = text(outdir, os.path.join(VERD, "RETURN-D2v.md"))
    if spec:
        for v in vlib.VERDICTS:
            if v not in spec:
                err("verdict-D/RETURN-D2v.md does not name the verdict value %r; the return line's four values "
                    "are written in it" % v, shape="rv:value", where=v)
        for f in ("cannot_tell_under", "residue", "themes", "sentence", "served"):
            if f not in spec:
                err("verdict-D/RETURN-D2v.md does not name the field %r of the return line" % f,
                    shape="rv:field", where=f)
        if "```" not in spec:
            err("verdict-D/RETURN-D2v.md has no fenced return example; fleet.py takes the end marker from its "
                "last fenced block")
    rooms = {r["sub"]: r for r in (vlib.rooms(ctx) or [])}
    if analysed is None:
        return
    for sub in sorted(analysed):
        p = packet_path(outdir, sub)
        if p is None:
            err("no verdict packet for r/%s (verdict-D/%s.md); every room of the analysed set has one (§4)" % (sub, sub),
                shape="packet:missing", where=sub)
            continue
        size = os.path.getsize(p)
        if size > PACKET_CEILING:
            err("verdict-D/%s is %d bytes, over the 50 KB ceiling (FLEET §1); cut the packet" % (os.path.basename(p), size),
                shape="packet:ceiling", where=sub)
        t = open(p, encoding="utf-8", errors="replace").read()
        tail = [l for l in t.strip().splitlines() if l.strip()]
        if not tail or "end" not in tail[-1].lower():
            err("verdict-D/%s does not end with an end marker (a last line naming the end, with the line telling "
                "the reader to confirm it reached it)" % os.path.basename(p), shape="packet:end", where=sub)
        low = t.lower()
        if "criterion" not in low and "composes" not in low:
            err("verdict-D/%s does not carry the verdict criterion (FLEET §3, verbatim)" % os.path.basename(p),
                shape="packet:criterion", where=sub)
        if "case.md" in low or "brief.md" in low:
            warn("verdict-D/%s mentions a coder document by name; the packet holds none of the coder's prose"
                 % os.path.basename(p), shape="packet:coder", where=sub)
        n = (rooms.get(sub) or {}).get("codes")
        if n is not None and not re.search(r"\b%d\b" % int(n), t):
            err("verdict-D/%s does not state the room's concept count (%d in rooms.jsonl) beside the floor; the "
                "reader must not estimate what the store holds (§2)" % (os.path.basename(p), n),
                shape="packet:count", where=sub)


def check_prior_10a(outdir):
    """prior.md sections 7 and 8 (the distance weights; the cannot-tell thresholds) are written at D1,
    before any adaptation is seen (PRIOR-template.md)."""
    p = text(outdir, "prior.md")
    if not p.strip():
        err("prior.md is not in the output directory; sections 7 and 8 are written into it at D1")
        return
    for n in (7, 8):
        m = re.search(r"^##\s*%d\b" % n, p, re.M)
        if not m:
            err("prior.md has no section %d; the distance weights (7) and the cannot-tell thresholds (8) are "
                "written at D1, before any adaptation is seen" % n, shape="prior:section-D1", where=str(n))
            continue
        nxt = re.search(r"^##\s", p[m.end():], re.M)
        body = p[m.end():m.end() + nxt.start()] if nxt else p[m.end():]
        if "(number)" in body:
            err("prior.md section %d still carries the template placeholder (number); write the figures at D1"
                % n, shape="prior:placeholder-D1", where=str(n))
        elif n == 7:                   # the form distance.py reads; anything else falls back to its defaults
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import distance
            for rx, what in ((distance.W_LINE, "w = <third>, <fourth>, <dimension>, <target>"),
                             (distance.G_LINE, "g = <same op>, <same kind>, <different kind>, <opposite>")):
                if not rx.search(body):
                    err("prior.md section 7 has no line `%s`; distance.py reads that form and nothing else" % what,
                        shape="prior:weights-form", where="7")


def check(root, outdir, ctx):
    stage = "D1"
    H = HAND
    need(outdir, "%s/RETURN-D.md" % H, "%s/VOCABULARY.json" % H, "%s/VERSION" % H, "%s/MODEL.md" % H,
         "%s/LADDER.md" % H, "sealed/EXPECTATIONS.jsonl", "%s/tasks/index.tsv" % H, "%s/HANDLER.md" % H,
         "%s/tasks/*/TASK.md" % H, "%s/RETURN-D2v.md" % VERD, "notes-D1.md", "handback-D1.md",
         "model/elements.jsonl", "model/arrows.jsonl")
    check_prior_10a(outdir)
    got = vlib.analysed_set(stage, "the tasks, index rows, packets and expectations against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    els, ars = model_rows(outdir)
    vocab = load_vocab(outdir)
    if vocab is None:
        err("handoff-D/VOCABULARY.json is absent or will not parse, so no id in the handoff was checked")
    else:
        check_vocabulary(outdir, vocab, els, ars)
    # VERSION is the model's hash
    mh = model_hash(outdir)
    ver = read_version(outdir)
    if ver is not None:
        if not re.fullmatch(r"[0-9a-f]{64}", ver):
            err("handoff-D/VERSION is not a sha256 digest (bare or sha256:-prefixed) on one line")
        elif mh and ver != mh:
            err("handoff-D/VERSION (%s...) is not the hash of model/ as it stands (%s...); the model moved after "
                "the handoff was built, or VERSION was written from something else. Rebuild the handoff from the "
                "frozen model; ingest.py rejects every return against any other version." % (ver[:12], mh[:12]))
    fz = vlib.frozen_hash(outdir, "C5")
    if fz and mh and fz != mh:
        err("model/ and its tiers are not the version stage C5 froze (%s... at C5d, now %s...); after C5 nothing below "
            "the model moves except as a recorded amendment at D3 or D6 (rule 11)" % (fz[:12], mh[:12]),
            shape="model:unfrozen")
    if vocab is not None and vocab["raw"].get("version") and bare_hash(str(vocab["raw"]["version"])) != ver:
        err("handoff-D/VOCABULARY.json carries a version that is not VERSION's")
    # MODEL.md and LADDER.md
    gm = text(outdir, os.path.join(H, "MODEL.md"))
    if gm and vocab is not None:
        absent = sorted(i for i in vocab["elements"] if i not in gm)
        if absent:
            err("handoff-D/MODEL.md never names %d element(s) or arrow(s) of the vocabulary: %s. A labeler cannot "
                "adapt an element it has not read; the prose carries every id." % (len(absent), absent[:8]))
        for w in ("room note", "branch", "my notes"):
            if w in gm.lower():
                warn("handoff-D/MODEL.md mentions %r; nothing in it refers to a room note, a branch or your notes" % w)
    lad = text(outdir, os.path.join(H, "LADDER.md"))
    if lad and vocab is not None:
        missing_dims = sorted(d for d in vocab["dimensions"] if d not in lad)
        if missing_dims:
            err("handoff-D/LADDER.md has no row for dimension(s) %s; the ladder is projected for every dimension "
                "in MODEL.md" % missing_dims[:6])
    # the ceiling declared in notes-D1.md, and MODEL.md against it
    notes = text(outdir, "notes-D1.md")
    m = re.search(r"ceiling[^\n]*?(\d[\d,]*)\s*(words|tokens|kb|bytes)", notes, re.I)
    if not m:
        err("notes-D1.md does not declare the MODEL.md ceiling as a number of words, tokens, KB or bytes (§3)")
    elif gm:
        n, unit = int(m.group(1).replace(",", "")), m.group(2).lower()
        size = {"words": len(gm.split()), "tokens": len(gm) // 4, "kb": len(gm.encode("utf-8")) // 1024,
                "bytes": len(gm.encode("utf-8"))}[unit]
        if size > n:
            err("handoff-D/MODEL.md is %d %s; notes-D1.md declares a ceiling of %d %s (§4: MODEL.md fits the "
                "declared ceiling)" % (size, unit, n, unit))
    # story-miss rooms listed before the build
    stories = last_story(outdir)
    if stories:
        last = jsonl(stories[-1]) or []
        miss = [r.get("sub") for r in last if r.get("verdict") == "not-told"]
        absent = [s for s in miss if s and s not in notes]
        if absent:
            err("notes-D1.md does not list %d of the %d rooms the last story (%s) could not tell: %s. They are "
                "listed before anything is built, so D3 can count how they fared." % (len(absent), len(miss),
                                                                                       os.path.basename(stories[-1]), absent[:6]))
    else:
        warn("no story_rooms-pN.jsonl in the output directory; the story-miss rooms were not checked")
    # tasks
    tasks = {os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(outdir, H, "tasks", "*", "TASK.md"))}
    themes = vlib.store_themes(ctx) if vlib.rooms(ctx) else None
    if analysed is not None:
        miss = sorted(analysed - tasks - unbuilt_rooms(outdir))
        if miss:
            err("no task for %d rooms of the analysed set (handoff-D/tasks/<sub>/TASK.md): %s. A room whose task "
                "could not be built goes to handback-D1.md with why." % (len(miss), miss[:6]))
        stray = sorted(tasks - analysed)
        if stray:
            err("handoff-D/tasks/ holds rooms outside the analysed set: %s" % stray[:6])
    if vocab is not None:
        for sub in sorted(tasks):
            check_task(outdir, sub, vocab, ctx, themes)
    check_index(outdir, analysed)
    if vocab is not None:
        check_expectations(outdir, vocab, analysed)
    check_packets(outdir, analysed, ctx)
    # nothing served carries a canvas field (rule 7)
    scan_canvas(outdir, (H, VERD), stage)
    # HANDLER.md says what it must
    hb = text(outdir, os.path.join(H, "HANDLER.md")).lower()
    if hb:
        for w, what in (("ascending", "dispatch by size ascending"), ("unreturned", "the UNRETURNED.tsv rule"),
                        ("done", "DROPS/D/DONE with the counts"), ("ingest.py", "the per-room check ingest.py --check"),
                        ("drops/d/", "the return path DROPS/D/<sub>/")):
            if w not in hb:
                err("handoff-D/HANDLER.md does not state %s (§1)" % what, shape="handler:%s" % w)
    # the folder hash in notes-D1.md and RUN.json; VERSION in both
    fh = folder_hash(os.path.join(outdir, H))
    digests = set(HEX64.findall(notes))
    if ver and ver not in digests:
        err("notes-D1.md does not carry VERSION (%s...); the final message and the notes name the folder's hash "
            "and VERSION (§4)" % (ver or "")[:12])
    if not (digests - {ver}):
        err("notes-D1.md carries no folder hash; the folder is hashed and the hash is in notes-D1.md and RUN.json (§4)")
    elif fh not in digests:
        warn("notes-D1.md carries no digest equal to this check's hash of handoff-D/ (%s...); if the harness hashes "
             "the folder another way, say which in the notes" % fh[:12])
    rp = os.path.join(root, "RUN.json")
    if not os.path.exists(rp):
        err("RUN.json is not in the folder root; the folder hash and VERSION go into it at the close")
    else:
        rt = open(rp, encoding="utf-8", errors="replace").read()
        if ver and ver not in rt:
            err("RUN.json does not carry VERSION (%s...); the model version the return runs against is recorded there" % ver[:12])
        if fh not in rt and not (digests - {ver}) & set(HEX64.findall(rt)):
            warn("RUN.json carries no hash of handoff-D/")
    print("  D1: %d tasks, %d rooms analysed, %d elements and arrows in the vocabulary, VERSION %s"
          % (len(tasks), len(analysed or ()), len(vocab["elements"]) if vocab else 0, (ver or "absent")[:12]))


# ---- the self-test ------------------------------------------------------------------------------

def _w(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)


def _wj(path, rows):
    _w(path, "".join(json.dumps(r) + "\n" for r in rows))


ELS = [{"id": "P07", "kind": "process", "statement": "recruiting placers from outside", "tier": "T4-003",
        "dimension": "D2", "evidence": {"findings": [], "codes": ["denmark:c0117"]}, "since": "C2-pass-1", "status": "standing"},
       {"id": "K04", "kind": "condition", "statement": "the artwork borders a hostile neighbour", "tier": "T4-003",
        "dimension": "D2", "evidence": {"findings": [], "codes": ["asoiaf:c0011"]}, "since": "C2-pass-1", "status": "standing"}]
ARS = [{"id": "A01", "kind": "order", "statement": "K04 precedes P07", "from": "K04", "to": "P07",
        "mechanism": "a hostile border makes the call urgent", "in_model": True, "status": "standing"}]


def plant_base(out, root):
    """A minimal passing D1 fixture over the store's rooms denmark and asoiaf (sweden dropped)."""
    _wj(os.path.join(out, "dropped.jsonl"), [{"sub": "sweden", "why": "no coded thread"}])
    _wj(os.path.join(out, "model", "elements.jsonl"), ELS)
    _wj(os.path.join(out, "model", "arrows.jsonl"), ARS)
    _wj(os.path.join(out, "model", "history.jsonl"), [{"id": "h-0001", "move": "merging", "element": "P07", "leg": "C2-1"}])
    _wj(os.path.join(out, "scheme_final.jsonl"), [{"id": "T3-014", "name": "recruiting"}])
    _wj(os.path.join(out, "fourth", "fourth.jsonl"), [{"id": "T4-003", "name": "getting hands", "members": ["T3-014"]}])
    _wj(os.path.join(out, "dimensions.jsonl"), [{"id": "D2", "label": "mobilising", "members": ["T4-003"]}])
    _wj(os.path.join(out, "assignments_final.jsonl"), [{"sub": "denmark", "theme_id": "t07", "third_order": ["T3-014"]},
                                                       {"sub": "asoiaf", "theme_id": "t02", "third_order": ["T3-014"]}])
    _wj(os.path.join(out, "story_rooms-p1.jsonl"), [{"sub": "denmark", "verdict": "told"}, {"sub": "asoiaf", "verdict": "not-told"}])
    _wj(os.path.join(out, "diary", "D1-1.jsonl"), [{"stage": "D1", "text": "built"}])
    _w(os.path.join(out, "_head.md"), "# head\n")
    _w(os.path.join(out, "prior.md"), "## 7. weights\nw = 4, 2, 1, 0.5; g = 1, 0.5, 0, -1\n"
                                      "## 8. thresholds\n- Concept floor: 3\n- Off-platform pointers: 5\n")
    H = os.path.join(out, HAND)
    ver = model_hash(out)
    vocab = {"elements": [{k: e.get(k) for k in ELEMENT_FIELDS} for e in ELS],
             "arrows": [dict({k: a.get(k) for k in ARROW_FIELDS}, statement=a["statement"]) for a in ARS],
             "third": [{"id": "T3-014", "name": "recruiting"}], "fourth": [{"id": "T4-003", "name": "getting hands"}],
             "dimensions": [{"id": "D2", "label": "mobilising"}]}
    _w(os.path.join(H, "VOCABULARY.json"), json.dumps(vocab))
    _w(os.path.join(H, "VERSION"), "sha256:%s\n" % ver)
    ret = ("# RETURN-D\n\n```json\n{\"end\": true, \"lines\": 1}\n```\n")
    _w(os.path.join(H, "RETURN-D.md"), ret)
    _w(os.path.join(H, "MODEL.md"), "# The model\n\nD2 mobilising. When K04 holds, P07 follows (A01), because hands are short. [T4-003]\n")
    _w(os.path.join(H, "LADDER.md"), "| quote | first | second | third | fourth | dimension |\n|---|---|---|---|---|---|\n"
                                     "| we need more people | calling | t07 | T3-014 | T4-003 | D2 |\n")
    _wj(os.path.join(out, "sealed", "EXPECTATIONS.jsonl"), [
        {"sub": "denmark", "expect_instantiate": ["P07"], "expect_absent": [], "from": ["placements"], "why": "P07: t07 is placed under it"},
        {"sub": "asoiaf", "expect_instantiate": ["K04"], "expect_absent": ["P07"], "from": ["implications-C5 §2"], "why": "K04: t02 defends; P07: no recruiting theme"}])
    _w(os.path.join(H, "HANDLER.md"), "dispatch by size ascending; ingest.py --check; returns to DROPS/D/<sub>/; "
                                      "UNRETURNED.tsv only when you cannot; DONE with the counts\n")
    _w(os.path.join(H, "tasks", "index.tsv"), "sub\titems_in_window\tpayload_bytes\tdocuments\ndenmark\t120\t5000\tcase.md\nasoiaf\t300\t9000\tcase.md\n")
    for sub, tid, cid in (("denmark", "t07", "c0117"), ("asoiaf", "t02", "c0011")):
        T = os.path.join(H, "tasks", sub)
        _w(os.path.join(T, "TASK.md"), "# Task: r/%s\nRead RETURN-D.md, MODEL.md (P07, K04, A01), LADDER.md, then case.md.\n" % sub)
        _w(os.path.join(T, "case.md"), "the room organised\n")
        _wj(os.path.join(T, "codes.jsonl"), [{"sub": sub, "code_id": cid, "theme_id": tid}])
        _wj(os.path.join(T, "themes.jsonl"), [{"sub": sub, "theme_id": tid}])
        _wj(os.path.join(T, "placements.jsonl"), [{"sub": sub, "theme_id": tid, "third_order": "T3-014", "fourth_order": "T4-003", "dimension": "D2"}])
        for f in TASK_USUAL:
            _w(os.path.join(T, f), "-\n")
        _w(os.path.join(out, VERD, "%s.md" % sub), "# r/%s\n\nthe model: P07, K04, A01.\n\nthe criterion: composes | composes-with-residue | "
                                                   "does-not-compose | cannot-tell.\n\nconcept count 3.\n\n<!-- end: confirm you reached this line -->\n" % sub)
    _w(os.path.join(out, VERD, "RETURN-D2v.md"), "verdict: composes|composes-with-residue|does-not-compose|cannot-tell; themes, residue, "
                                                 "cannot_tell_under, sentence, served\n\n```json\n{\"sub\": \"x\"}\n<!-- end -->\n```\n")
    fh = folder_hash(H)
    _w(os.path.join(out, "notes-D1.md"), "story-miss rooms: asoiaf\n\nceiling declared for MODEL.md: 4000 words\n\nfolder hash %s\nVERSION %s\n" % (fh, ver))
    _w(os.path.join(out, "handback-D1.md"), "nothing\n")
    _w(os.path.join(root, "RUN.json"), json.dumps({"handoff_D": {"folder": fh, "version": ver}}))


def _plant_version(out, root):
    plant_base(out, root)
    _w(os.path.join(out, HAND, "VERSION"), "sha256:" + "0" * 64 + "\n")


def _plant_canvas(out, root):
    plant_base(out, root)
    _w(os.path.join(out, HAND, "tasks", "denmark", "case.md"), "the room organised; canvas_area_px 4200\n")


def _plant_task_missing(out, root):
    plant_base(out, root)
    os.rename(os.path.join(out, HAND, "tasks", "asoiaf"), os.path.join(out, HAND, "tasks", "asoiaf_old"))
    os.rename(os.path.join(out, HAND, "tasks", "asoiaf_old", "TASK.md"), os.path.join(out, HAND, "tasks", "asoiaf_old", "TASK.txt"))


def _plant_vocab_stale(out, root):
    plant_base(out, root)
    v = json.load(open(os.path.join(out, HAND, "VOCABULARY.json")))
    v["elements"][0]["statement"] = "something the model does not say"
    _w(os.path.join(out, HAND, "VOCABULARY.json"), json.dumps(v))


def _plant_prior_unwritten(out, root):
    plant_base(out, root)
    _w(os.path.join(out, "prior.md"), "## 7. weights\nw = 4, 2, 1, 0.5\n## 8. thresholds\n- Concept floor: (number)\n")


PLANTED = [
    ("prior.md section 8 not written at D1", _plant_prior_unwritten, "still carries the template placeholder"),
    ("VERSION is not the model hash", _plant_version, "is not the hash of model/"),
    ("canvas field in a task", _plant_canvas, "carries a canvas field"),
    ("room without a task", _plant_task_missing, "no task for"),
    ("vocabulary not the projection", _plant_vocab_stale, "statement differs from model/"),
]
