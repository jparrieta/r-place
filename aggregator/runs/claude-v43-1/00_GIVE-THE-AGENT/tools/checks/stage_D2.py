"""checks/stage_D2.py: the close-check of stage D2, the labelers' returns and the verdict fleet, v38.

Written from stages/STAGE-D2-adaptation-labelers-and-verdicts.md (its Outputs block, §1 what
ingest did, §2 the verdicts, §3 the sample), SCHEMA-adaptations.md §2 to §5, FLEET.md §1 to §3,
tools/ingest.py's six rules, and from the v37 check it descends from (_v37-source/tools/
validate.py, stage10: the verdict line's shape and the one-verdict-per-room rule, ported to the
readers' lines of verdicts-D.jsonl). What it checks is the SHAPE of the return: the drops are
complete or the room is marked unreturned, the ledger ingest.py compiled carries the fields,
ops, lifts and ids SCHEMA §3 names and every id resolves, every room model carries its marker,
grade and the elements its ledger adapts, the readers' verdicts are R = 2 per room with the
four values and their conditional fields, and the counts D2 writes reconcile. It cannot check
whether a labeler or a reader was right.

    def check(root, outdir, ctx): ...

Where this module reads: DROPS/D/ in the folder root (ingest.py's --drops default);
_fleet_raw/D2v/ under out/ (fleet.py's --raw), only the validated `<packet>/<reader>.jsonl`
returns, never the raw replies; RUN.json in the folder root (done.sh writes it there).

Shapes this module fixes where the stage file gives none:
- verdicts-D.jsonl: a line is either a reader's return line (RETURN-D2v: sub, reader, verdict,
  themes, residue, cannot_tell_under, sentence, served) or a room line with `readers`, a list
  of such lines; either shape may carry `grade`, the labeler's grade from model-D.md, which
  must sit beside the verdict on some line of the room. Lines with `ruled_by: analyst` are
  D3's rulings and are not counted as readers here.
- RUN.json: the D2 counts are any object holding the keys accepted, reissued and unreturned
  (the search is recursive); accepted must equal the rooms in the ledger, unreturned the rows
  of DROPS/D/UNRETURNED.tsv.
- rooms/<sub>/verdict-10: a file or folder whose name starts with verdict-D.

Not carried from v37's stage10: author_compositions.jsonl, composition_brief.md,
composition.jsonl's read_by and changed_from (the analyst's rulings are D3's),
uncomposed-D.md, transmission-D.md and the §7 counts (all D3's, in stage_D3.py).

The common checks in validate.py already require the diary lines and the head.
"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
from checks import stage_D1 as s10a
import dreturn                      # the one rule set ingest.py applies (audit 2026-09-29, H11)

R_READERS = 2
LEDGER_REQUIRED = ("id", "sub", "op", "element", "source", "lift", "condition", "statement", "how",
                   "evidence", "relation", "portable", "kind", "origin", "model_version")
LEDGER_OPTIONAL = ("observation", "nonportable_hits", "decision", "link_kind", "labeler_run", "why")
OP_NEEDS = dreturn.LEDGER_NEEDS
KIND_OF = dreturn.KIND
THRESHOLDS = ("coded-share", "off-platform", "both")
BRACKET = re.compile(r"\[(absent\s+)?([PKCRA]\d{2})\]")
CITE = re.compile(r"\[(c\d{4})\]")
QUOTE = re.compile(r"[\"“]([^\"”\n]{20,}?)[\"”]")


def one_sentence(s):
    s = " ".join((s or "").split())
    if not s or len(s.split()) > 40:
        return False
    body = s.rstrip(".!?")
    return not re.search(r"[.!?]\s", body)


def lexicon_names(root, sub):
    """Proper names from the analyst's own lexicon (out/lexicon-A1.md: term, room, item id of
    first use, one per line), the lines for this room."""
    p = os.path.join(root, "out", "lexicon-A1.md")
    words = set()
    if os.path.exists(p):
        for line in open(p, encoding="utf-8", errors="replace"):
            parts = [x for x in re.split(r"\t|\s{2,}", line.strip()) if x]
            if len(parts) < 3 or parts[-2].lower() != sub.lower():
                continue
            m = re.match(r"^\s*[-*]?\s*([A-Za-z][\w'-]{2,})", parts[0])
            if m and m.group(1)[0].isupper():
                words.add(m.group(1).lower())
    return words


def name_hits(txt, sub, frame, lex):
    """The room names and lexicon names a text carries (ingest rule 5)."""
    t = (txt or "").lower()
    hits = [n for n in frame if len(n) >= 3 and re.search(r"\b%s\b" % re.escape(n.lower()), t)]
    hits += [w for w in lex if re.search(r"\b%s\b" % re.escape(w), t)]
    return sorted(set(hits))


def find_counts(obj):
    """The first object, at any depth, holding accepted, reissued and unreturned."""
    if isinstance(obj, dict):
        if all(k in obj for k in ("accepted", "reissued", "unreturned")):
            return obj
        for v in obj.values():
            r = find_counts(v)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_counts(v)
            if r is not None:
                return r
    return None


def unreturned_rows(root):
    p = os.path.join(root, "DROPS", "D", "UNRETURNED.tsv")
    if not os.path.exists(p):
        return None
    rows = []
    for l in open(p, encoding="utf-8"):
        if not l.strip() or l.startswith("#"):
            continue
        cells = l.rstrip("\n").split("\t")
        if cells[0].strip().lower() in ("sub", "room"):
            continue
        rows.append(cells[0].strip())
    return rows


def verdict_line(r, name, where, themes, sub, codes=None):
    """RETURN-D2v's line (dreturn.verdict_problems, the rule set fleet.py's schema carries)."""
    room_t = {t for (s_, t) in themes if s_ == sub} if themes is not None else None
    room_c = {c for (s_, c) in codes if s_ == sub} if codes is not None else None
    for p in dreturn.verdict_problems(r, sub, room_t, room_c):
        err("%s %s: %s" % (name, where, p), shape="%s: %s" % (name, p.split(" ")[0]), where=where)
    if "served" in r and not re.fullmatch(r"[0-9a-f]{64}", str(r.get("served") or "")):
        warn("%s %s: served is not the packet's sha256" % (name, where), shape="%s: served" % name, where=where)


def check_drops(root, analysed, ledger_subs):
    D = os.path.join(root, "DROPS", "D")
    if not os.path.exists(os.path.join(D, "DONE")):
        err("DROPS/D/DONE is not in the folder root; the handler writes it with the counts when every room "
            "is returned or marked unreturned, and D2 is launched only after it")
    else:
        done = open(os.path.join(D, "DONE"), encoding="utf-8", errors="replace").read()
        if not re.search(r"\d", done):
            err("DROPS/D/DONE carries no count; it holds the rooms returned and unreturned")
    unret = unreturned_rows(root)
    unret_set = set(unret or [])
    have = {}
    if os.path.isdir(D):
        for sub in sorted(os.listdir(D)):
            d = os.path.join(D, sub)
            if not os.path.isdir(d) or sub == "recheck":
                continue
            have[sub] = {f for f in ("model-D.md", "adaptations.jsonl", "run.json") if os.path.exists(os.path.join(d, f))}
    if analysed is not None:
        for sub in sorted(analysed):
            if sub in unret_set:
                continue
            got = have.get(sub)
            if got is None:
                err("r/%s has no drop in DROPS/D/%s/ and is not in UNRETURNED.tsv; silence is a missing return, not "
                    "a verdict (SCHEMA §3). The handler returns it or marks it unreturned with the reason." % (sub, sub),
                    shape="drop:missing", where=sub)
            else:
                miss = sorted({"model-D.md", "adaptations.jsonl", "run.json"} - got)
                if miss:
                    err("DROPS/D/%s/ lacks %s; a return is model-D.md, adaptations.jsonl and run.json" % (sub, miss),
                        shape="drop:incomplete", where=sub)
        stray = sorted(set(have) - analysed)
        if stray:
            err("DROPS/D/ holds rooms outside the analysed set: %s" % stray[:6])
        both = sorted(unret_set & ledger_subs)
        if both:
            err("UNRETURNED.tsv lists %s, which the ledger holds; a room is one or the other" % both[:6])
    return have, unret


def check_drop_files(root, outdir, sub, ledger_lines, vocab, codes, elements_model):
    """ingest rule 6 on the drop, and the room model (SCHEMA §5) as copied into rooms/<sub>/."""
    D = os.path.join(root, "DROPS", "D", sub)
    lp = os.path.join(D, "adaptations.jsonl")
    if os.path.exists(lp):
        raw = [l for l in open(lp, encoding="utf-8").read().split("\n") if l.strip()]
        try:
            objs = [json.loads(l) for l in raw]
        except ValueError as e:
            err("DROPS/D/%s/adaptations.jsonl is not JSON per line (%s); ingest rule 1" % (sub, e), shape="drop:json", where=sub)
            objs = []
        if objs and objs[-1].get("end"):
            n = len(objs) - 1
            if objs[-1].get("lines") != n:
                err("DROPS/D/%s/adaptations.jsonl: end marker says %s lines, the file holds %d (rule 6)"
                    % (sub, objs[-1].get("lines"), n), shape="drop:endcount", where=sub)
            if len(ledger_lines) != n:
                err("adaptations.jsonl holds %d lines for r/%s, the drop %d; the ledger carries every line of an "
                    "accepted room, so re-run ingest.py D" % (len(ledger_lines), sub, n), shape="ledger:count", where=sub)
        elif objs:
            err("DROPS/D/%s/adaptations.jsonl has no end marker {\"end\": true, \"lines\": N} (rule 6)" % sub,
                shape="drop:end", where=sub)
    # the room model, from the copy under rooms/
    mp = os.path.join(outdir, "rooms", sub, "model-D.md")
    if not os.path.exists(mp):
        err("rooms/%s/model-D.md was not copied from the drop" % sub, shape="rooms:model", where=sub)
        return
    model = open(mp, encoding="utf-8", errors="replace").read()
    adapted = {l.get("element") for l in ledger_lines if l.get("element") and l.get("op") != "none"}
    vocab_ids = (set(vocab["elements"]) | set(vocab["dimensions"])) if vocab is not None else None
    room_codes = {c for (s_, c) in codes if s_ == sub} if codes is not None else None
    spec = os.path.join(outdir, 'handoff-D', 'RETURN-D.md')
    local = os.path.exists(spec) and 'local_status:' in open(spec, encoding='utf-8').read()
    for p in dreturn.model_problems(model, sub, vocab_ids, room_codes, adapted, require_local=local):   # the rules ingest applied
        err("rooms/%s/model-D.md: %s" % (sub, p), shape="rooms:%s" % p.split(":")[0].replace(" ", "-"), where=sub)
    grade = dreturn.grade_of(model)
    ids = {m.group(2) for m in BRACKET.finditer(model)}
    if elements_model:
        wd = sorted(i for i in ids if elements_model.get(i, {}).get("status") == "withdrawn")
        if wd:
            err("rooms/%s/model-D.md cites withdrawn element(s) %s" % (sub, wd[:4]), shape="rooms:withdrawn", where=sub)
    return grade


def check_ledger(root, outdir, ctx, vocab, version, analysed):
    rows = jsonl(os.path.join(outdir, "adaptations.jsonl"))
    if rows is None:
        return {}
    frame = vlib.frame("D2", "portability against the census names", ctx) or set()
    themes = vlib.store_themes(ctx)
    codes = vlib.store_codes(ctx)
    trans = {(r.get("sub"), r.get("id")) for r in (jsonl(os.path.join(ctx["package"], "store", "transitions.jsonl")) or [])}
    placed, pname = vlib.placements(outdir)
    fourth_of, dim_of = {}, {}
    for r in jsonl(os.path.join(outdir, "fourth", "fourth.jsonl")) or []:
        for m in r.get("members") or []:
            fourth_of[m] = r.get("id")
    for r in jsonl(os.path.join(outdir, "dimensions.jsonl")) or []:
        for m in r.get("members") or []:
            dim_of[m] = r.get("id")
    els, ars = s10a.model_rows(outdir)
    lex = {}
    by_sub = collections.defaultdict(list)
    seen_ids = collections.Counter()
    N = "adaptations.jsonl"
    for n, r in enumerate(rows, 1):
        w = r.get("id") or "line %d" % n
        sub, op = r.get("sub"), r.get("op")
        by_sub[sub].append(r)
        seen_ids[r.get("id")] += 1
        miss = [f for f in LEDGER_REQUIRED if f not in r]
        if miss:
            err("%s %s lacks field(s) %s; ingest.py writes every field of SCHEMA §3 on every line" % (N, w, miss),
                shape="ledger:fields", where=w)
        extra = [f for f in r if f not in LEDGER_REQUIRED and f not in LEDGER_OPTIONAL]
        if extra:
            warn("%s %s carries fields beyond the schema: %s" % (N, w, extra), shape="ledger:extra", where=w)
        if not re.fullmatch(r"%s-\d{3,}" % re.escape(str(sub)), str(r.get("id") or "")):
            err("%s %s: id is not <sub>-NNN" % (N, w), shape="ledger:id", where=w)
        if analysed is not None and sub not in analysed:
            err("%s %s: room %r is not in the analysed set" % (N, w, sub), shape="ledger:room", where=w)
        if op not in vlib.OPS:
            err("%s %s: op %r is not one of %s (rule 1)" % (N, w, op, vlib.OPS), shape="ledger:op", where=w)
            continue
        need_f = [f for f in OP_NEEDS[op] if not r.get(f)]
        for problem in dreturn.absence_problems(r):
            err("%s %s: %s" % (N, w, problem), shape="ledger:observation", where=w)
        if op == "link" and not r.get("link_kind"):
            need_f.append("link_kind")
        if need_f:
            err("%s %s: %s lacks %s (rule 1)" % (N, w, op, need_f), shape="ledger:%s:needs" % op, where=w)
        if r.get("kind") != KIND_OF[op]:
            err("%s %s: kind %r, but %s is a %s (SCHEMA §2)" % (N, w, r.get("kind"), op, KIND_OF[op]),
                shape="ledger:kind", where=w)
        if r.get("origin") not in ("labeler", "recheck"):
            err("%s %s: origin %r; ingest stamps labeler" % (N, w, r.get("origin")), shape="ledger:origin", where=w)
        if version and s10a.bare_hash(str(r.get("model_version") or "")) != version:
            err("%s %s: model_version is not handoff-D/VERSION; a return against another version is rejected whole "
                "(rule 2)" % (N, w), shape="ledger:version", where=w)
        # rule 2: the element
        el = r.get("element")
        if el:
            # a dimension may stand as the element of link, and (J, 2026-10-16, QD2-001, option 1) of restrict,
            # add-condition and add-step; D3 rules on those lines as they stand
            ok = vocab is not None and (el in vocab["elements"] or (op in ("link", "restrict", "add-condition", "add-step")
                                                                   and el in vocab["dimensions"]))
            if vocab is not None and not ok:
                err("%s %s: element %r does not resolve in VOCABULARY.json (rule 2)" % (N, w, el), shape="ledger:element", where=w)
            src_row = els.get(el) or ars.get(el)
            if src_row is not None and src_row.get("status") == "withdrawn":
                err("%s %s: element %s is withdrawn (rule 2)" % (N, w, el), shape="ledger:withdrawn", where=w)
        elif op not in ("propose", "none"):
            err("%s %s: %s with no element" % (N, w, op), shape="ledger:noelement", where=w)
        # rule 3: codes, transitions, the source
        ev = r.get("evidence") or {}
        if not isinstance(ev, dict):
            err("%s %s: evidence is not an object with codes" % (N, w), shape="ledger:evidence", where=w)
            ev = {}
        cl = ev.get("codes") or []
        if not cl and op not in ("none", "absent"):      # absent may rest on silence (RETURN-D)
            err("%s %s: no code id in evidence.codes (rule 1)" % (N, w), shape="ledger:nocodes", where=w)
        elif not cl:
            warn("%s %s: none line without evidence for the fit" % (N, w), shape="ledger:none-nocodes", where=w)
        for c in cl:
            cid = str(c).split(":")[-1]
            if (sub, cid) not in codes:
                err("%s %s: concept %s is not in r/%s's codes in the store, or is retracted (rule 3)" % (N, w, c, sub),
                    shape="ledger:code", where=w)
        for t in ev.get("transitions") or []:
            tid = str(t).split(":")[-1] if str(t).startswith("%s:" % sub) else t
            if (sub, tid) not in trans and (sub, t) not in trans:
                err("%s %s: transition %s is not in r/%s's forest (rule 3)" % (N, w, t, sub), shape="ledger:transition", where=w)
        src = r.get("source")
        node = None
        if src:
            node = str(src).split(":", 1)[1] if ":" in str(src) else str(src)
            is_theme, is_code = (sub, node) in themes, (sub, node) in codes
            if not (is_theme or is_code):
                err("%s %s: source %r is not a theme or concept of r/%s (rule 3)" % (N, w, src, sub), shape="ledger:source", where=w)
            elif is_code and op not in ("contradict", "instantiate", "absent", "none"):
                warn("%s %s: source is a code where a theme is expected for %s (SCHEMA §3)" % (N, w, op),
                     shape="ledger:source-code", where=w)
            if is_code and not is_theme:
                node = ctx.get("code_theme", {}).get((sub, node)) or node
        elif op not in dreturn.SOURCE_OPTIONAL:
            err("%s %s: %s with no source theme (SCHEMA §3: required for every op except absent and contradict)" % (N, w, op),
                shape="ledger:nosource", where=w)
        # rule 4
        if op != "none" and not one_sentence(r.get("how")):
            err("%s %s: how is not one sentence under forty words (rule 4)" % (N, w), shape="ledger:how", where=w)
        # rule 5
        if sub not in lex:
            lex[sub] = lexicon_names(root, sub)
        hits = name_hits(" ".join(str(r.get(k) or "") for k in ("condition", "statement", "how")), sub, frame, lex[sub])
        if not isinstance(r.get("portable"), bool):
            err("%s %s: portable is not a boolean" % (N, w), shape="ledger:portable-type", where=w)
        elif r["portable"] and hits:
            err("%s %s: portable is true while condition, statement or how names %s (rule 5); ingest keeps such a "
                "line with portable false" % (N, w, hits[:3]), shape="ledger:portable", where=w)
        # the lift
        lift = r.get("lift")
        if src:
            if not (isinstance(lift, list) and len(lift) == 4):
                err("%s %s: lift is not the four-entry path [theme, T3, T4, D] (SCHEMA §2)" % (N, w), shape="ledger:lift", where=w)
            else:
                l0, l3, l4, ld = lift
                if l0 != "%s:%s" % (sub, str(l0).split(":")[-1]):
                    err("%s %s: lift[0] %r is not <sub>:<theme>" % (N, w, l0), shape="ledger:lift0", where=w)
                if l3 is not None and not vlib.T3.match(str(l3)):
                    err("%s %s: lift[1] %r is not a third-order id" % (N, w, l3), shape="ledger:lift1", where=w)
                if l4 is not None and not vlib.T4.match(str(l4)):
                    err("%s %s: lift[2] %r is not a fourth-order id" % (N, w, l4), shape="ledger:lift2", where=w)
                if ld is not None and not vlib.DIM.match(str(ld)):
                    err("%s %s: lift[3] %r is not a dimension id" % (N, w, ld), shape="ledger:lift3", where=w)
                if (l4 and not l3) or (ld and not l4):
                    err("%s %s: lift has a level above a null; the path is contiguous from the theme up" % (N, w),
                        shape="ledger:lift-gap", where=w)
                if placed is not None:
                    key = (sub, str(l0).split(":")[-1])
                    exp = (placed.get(key) or [None])[0]
                    if exp != l3:
                        err("%s %s: lift[1] %r, but %s places %s under %r; ingest lifts through the placements at the "
                            "model version" % (N, w, l3, pname, key[1], exp), shape="ledger:lift-placement", where=w)
                if l3 and fourth_of and fourth_of.get(l3) != l4:
                    err("%s %s: lift[2] %r, but fourth/fourth.jsonl holds %s under %r" % (N, w, l4, l3, fourth_of.get(l3)),
                        shape="ledger:lift-fourth", where=w)
                if l4 and dim_of and dim_of.get(l4) != ld:
                    err("%s %s: lift[3] %r, but dimensions.jsonl holds %s under %r" % (N, w, ld, l4, dim_of.get(l4)),
                        shape="ledger:lift-dim", where=w)
        elif lift not in (None, []):
            err("%s %s: a lift on a line with no source" % (N, w), shape="ledger:lift-nosource", where=w)
    dup = [i for i, c in seen_ids.items() if c > 1]
    if dup:
        err("adaptations.jsonl repeats id(s) %s; ids are never reused" % dup[:5])
    for sub, ls in by_sub.items():
        if len(ls) > 1 and any(l.get("op") == "none" for l in ls):
            err("adaptations.jsonl: r/%s returned a none line beside %d other line(s); none is the whole return"
                % (sub, len(ls) - 1), shape="ledger:none-beside", where=sub)
    return by_sub


def check_verdicts(outdir, ctx, analysed, grades, unret=()):
    rows = jsonl(os.path.join(outdir, "verdicts-D.jsonl"))
    if rows is None:
        return {}
    themes = vlib.store_themes(ctx) if vlib.rooms(ctx) else None
    codes = vlib.store_codes(ctx) if vlib.rooms(ctx) else None
    readers = collections.defaultdict(list)
    grade_on = {}
    N = "verdicts-D.jsonl"
    for n, r in enumerate(rows, 1):
        sub = r.get("sub")
        if not sub:
            err("%s line %d has no sub" % (N, n), shape="verdicts:nosub", where="line %d" % n)
            continue
        if r.get("ruled_by") == "analyst":
            continue
        if "grade" in r:
            grade_on[sub] = r.get("grade")
        entries = r.get("readers") if isinstance(r.get("readers"), list) else [r]
        for e in entries:
            if not isinstance(e, dict):
                err("%s %s: a readers entry is not an object" % (N, sub), shape="verdicts:entry", where=sub)
                continue
            rid = e.get("reader")
            if not rid:
                err("%s %s: a reader's line has no reader id" % (N, sub), shape="verdicts:reader", where=sub)
            verdict_line(e, N, "%s %s" % (sub, rid or "?"), themes, sub, codes)
            readers[sub].append(e)
    for sub, es in readers.items():
        if len(es) < R_READERS:
            err("%s: r/%s has %d reader line(s); R = 2 readers per room so that a disagreement is visible (FLEET §1)"
                % (N, sub, len(es)), shape="verdicts:R", where=sub)
        if len({e.get("reader") for e in es}) != len(es):
            err("%s: r/%s carries one reader twice" % (N, sub), shape="verdicts:reader-twice", where=sub)
        g = grade_on.get(sub)
        if sub in unret:                       # an unreturned room has no labeler's grade
            continue
        if g is None:
            err("%s: r/%s has no grade beside its verdict; the labeler's grade from model-D.md sits in the same file "
                "and never replaces the verdict (§2)" % (N, sub), shape="verdicts:nograde", where=sub)
        elif g not in vlib.LABELER_GRADES:
            err("%s: r/%s grade %r is not the labeler's three" % (N, sub, g), shape="verdicts:grade", where=sub)
        elif grades.get(sub) and grades[sub] != g:
            err("%s: r/%s grade %r differs from rooms/%s/model-D.md's %r" % (N, sub, g, sub, grades[sub]),
                shape="verdicts:grade-differs", where=sub)
    if analysed is not None:
        miss = sorted(analysed - set(readers) - set(unret))
        if miss:
            err("%s has no reader line for %d rooms of the analysed set: %s; every room receives a verdict (rule 12)"
                % (N, len(miss), miss[:6]))
        stray = sorted(set(readers) - analysed)
        if stray:
            err("%s names rooms outside the analysed set: %s" % (N, stray[:6]))
    return readers


def check_raw(outdir, analysed):
    R = os.path.join(outdir, "_fleet_raw", "D2v")
    if not os.path.isdir(R):
        err("_fleet_raw/D2v/ is not in the output directory; the verdict fleet's returns are validated from it")
        return
    for f in ("arm.json", "DONE"):
        if not os.path.exists(os.path.join(R, f)):
            err("_fleet_raw/D2v/%s was not written; fleet.py writes it when every packet was tried" % f)
    if analysed is None:
        return
    for sub in sorted(analysed):
        d = os.path.join(R, sub)
        ok = glob.glob(os.path.join(d, "r*.jsonl")) if os.path.isdir(d) else []
        if len(ok) < R_READERS:
            err("_fleet_raw/D2v/%s/ holds %d validated return(s); R = 2 per room, and when reissues are exhausted "
                "the packet is rebuilt (FLEET §1)" % (sub, len(ok)), shape="raw:R", where=sub)


def check_folder_hash(outdir):
    """handoff-D/ as handoff.py hashed it at D1 (handoff-D.sha256): a labeler writes only into DROPS/D/."""
    rec = os.path.join(outdir, "handoff-D.sha256")
    if not os.path.exists(rec) or not os.path.isdir(os.path.join(outdir, "handoff-D")):
        return
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import handoff
    if handoff.folder_hash(os.path.join(outdir, "handoff-D")) != open(rec).read().strip():
        err("handoff-D/ no longer hashes to handoff-D.sha256: something wrote into the served folder after D1 "
            "(a labeler writes only into DROPS/D/<sub>/); ingest's returns are suspect until the change is found",
            shape="handoff:hash")


def check(root, outdir, ctx):
    stage = "D2"
    check_folder_hash(outdir)
    need(outdir, "adaptations.jsonl", "verdicts-D.jsonl", "ingest-D.md", "_views/rooms-x-elements.tsv",
         "notes-D2.md", "handback-D2.md", "handoff-D/VERSION", "handoff-D/VOCABULARY.json")
    got = vlib.analysed_set(stage, "the drops, the ledger and the verdicts against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    vocab = s10a.load_vocab(outdir)
    version = s10a.read_version(outdir)
    codes = vlib.store_codes(ctx) if vlib.rooms(ctx) else None
    ctx["code_theme"] = {}
    for r in jsonl(os.path.join(ctx["package"], "store", "codes.jsonl")) or []:
        ctx["code_theme"][(r.get("sub"), r.get("code_id"))] = r.get("theme_id")
    els, _ars = s10a.model_rows(outdir)
    by_sub = check_ledger(root, outdir, ctx, vocab, version, analysed)
    have, unret = check_drops(root, analysed, set(by_sub))
    grades = {}
    for sub in sorted((set(by_sub) | set(have)) - set(unret or [])):
        g = check_drop_files(root, outdir, sub, by_sub.get(sub, []), vocab, codes, els)
        if g:
            grades[sub] = g
        if sub in by_sub and not glob.glob(os.path.join(outdir, "rooms", sub, "verdict-D*")):
            err("rooms/%s/verdict-D was not copied beside model-D.md (Outputs)" % sub, shape="rooms:verdict", where=sub)
    if analysed is not None:
        silent = sorted(analysed - set(by_sub) - set(unret or []))
        if silent:
            err("adaptations.jsonl holds no line for %d rooms of the analysed set that are not marked unreturned: %s; "
                "a room with nothing to adapt returns one none line" % (len(silent), silent[:6]))
    readers = check_verdicts(outdir, ctx, analysed, grades, set(unret or []))
    check_raw(outdir, analysed)
    # the split rooms are listed for D3; the licence sentence where the rate appears
    notes = text(outdir, "notes-D2.md")
    split = sorted(s for s, es in readers.items() if len({e.get("verdict") for e in es}) > 1)
    unlisted = [s for s in split if s not in notes]
    if unlisted:
        err("notes-D2.md does not list %d of the %d rooms whose two readers differ (%s ...); they are listed for D3 "
            "to rule with the criterion in front of it (§2)" % (len(unlisted), len(split), unlisted[:5]))
    if readers:
        vlib.licence_sentence(outdir, "notes-D2.md", "the verdict disagreement rate")
    # the sample of room models, and its quotes
    models = sorted(by_sub)
    named = [s for s in models if re.search(r"\b%s\b" % re.escape(s), notes)]
    want = min(10, len(models))
    if len(named) < want:
        err("notes-D2.md names %d of the ten model-D.md files drawn by seed (%d rooms returned); each sampled room "
            "model and what it showed goes in the notes (§3)" % (len(named), len(models)))
    if models and "seed" not in notes.lower():
        err("notes-D2.md does not state the seed the ten room models were drawn by (§3)")
    quotes = [q for q in QUOTE.findall(notes) if len(q.split()) >= 5]
    if quotes:
        vlib.cites_resolve(outdir, root, quotes, "notes-D2.md")
    # counts in RUN.json, the manifest, the view
    rp = os.path.join(root, "RUN.json")
    counts = None
    if not os.path.exists(rp):
        err("RUN.json is not in the folder root; the D2 counts of accepted, reissued and unreturned rooms go into it (SCHEMA §4)")
    else:
        try:
            counts = find_counts(json.load(open(rp, encoding="utf-8")))
        except Exception as e:
            err("RUN.json will not parse: %s" % e)
        if counts is None:
            err("RUN.json holds no object with accepted, reissued and unreturned; stage D4 reconciles every room against them")
        else:
            if counts.get("accepted") != len(by_sub):
                err("RUN.json says %s rooms accepted; the ledger holds %d rooms. A count is computed from the file "
                    "that governs (rule 19)." % (counts.get("accepted"), len(by_sub)))
            if unret is not None and counts.get("unreturned") != len(unret):
                err("RUN.json says %s rooms unreturned; DROPS/D/UNRETURNED.tsv lists %d" % (counts.get("unreturned"), len(unret)))
    ents = vlib.manifest_entry(outdir, stage, "the labelers' returns and the verdict fleet")
    if ents:
        blob = json.dumps(ents).lower()
        for who in ("labeler", "reader"):
            if who not in blob:
                err("run_manifest.json's D2 entry does not record the %ss' model" % who)
    vp = os.path.join(outdir, "_views", "rooms-x-elements.tsv")
    if os.path.exists(vp):
        lines = [l.rstrip("\n") for l in open(vp, encoding="utf-8") if l.strip() and not l.startswith("#")]
        if lines:
            cols = lines[0].split("\t")
            if vocab is not None:
                bad = [c for c in cols[1:] if c not in vocab["elements"] and c not in vocab["dimensions"]]
                if bad:
                    err("_views/rooms-x-elements.tsv has columns not in the vocabulary: %s; regenerate with gen_views.py" % bad[:5])
            vrooms = {l.split("\t")[0] for l in lines[1:]}
            if by_sub and vrooms != set(by_sub):
                err("_views/rooms-x-elements.tsv rows (%d) are not the ledger's rooms (%d); regenerate with gen_views.py"
                    % (len(vrooms), len(by_sub)))
            for l in lines[1:]:
                for cell in l.split("\t")[1:]:
                    for op in filter(None, cell.split(",")):
                        if op.strip() not in vlib.OPS:
                            err("_views/rooms-x-elements.tsv cell %r is not an op" % cell, shape="view:cell", where=cell)
    ops = collections.Counter(l.get("op") for ls in by_sub.values() for l in ls)
    print("  D2: %d rooms in the ledger, %d lines, ops %s, %d unreturned, %d rooms with reader lines, %d split"
          % (len(by_sub), sum(ops.values()), dict(ops), len(unret or []), len(readers), len(split)))


# ---- the self-test ------------------------------------------------------------------------------

_w, _wj = s10a._w, s10a._wj


def plant_base(out, root):
    s10a.plant_base(out, root)
    ver = s10a.model_hash(out)
    _wj(os.path.join(out, "diary", "D2-1.jsonl"), [{"stage": "D2", "text": "checked"}])
    D = os.path.join(root, "DROPS", "D")
    drops = {
        "denmark": [{"op": "add-condition", "element": "P07", "source": "t07", "condition": "recruiting outside placers",
                     "how": "explains why the room recruited outside on night two.", "evidence": {"codes": ["c0117", "c0118"]}},
                    {"op": "absent", "observation": "unobserved", "element": "K04", "why": "no hostile neighbour is coded.", "evidence": {"codes": ["c0118"]}}],
        "asoiaf": [{"op": "instantiate", "element": "K04", "source": "t02", "how": "the border was held against a neighbour.",
                    "evidence": {"codes": ["c0011"]}}]}
    ledger = []
    for sub, ls in drops.items():
        _wj(os.path.join(D, sub, "adaptations.jsonl"), ls + [{"end": True, "lines": len(ls)}])
        cid = ls[0]["evidence"]["codes"][0]
        model = "# r/%s\n\n## D2\n\nThe room organised [P07] [%s]; [absent K04] [%s] [K04] [%s].\n\ngrade: composes\nbecause the ledger is thin.\n<!-- end -->\n" % (sub, cid, cid, cid)
        _w(os.path.join(D, sub, "model-D.md"), model)
        _w(os.path.join(D, sub, "run.json"), json.dumps({"model": "gpt-5-codex", "session": "s-1", "model_version": ver}))
        _w(os.path.join(out, "rooms", sub, "model-D.md"), model)
        _w(os.path.join(out, "rooms", sub, "verdict-D.jsonl"), "")
        for i, o in enumerate(ls, 1):
            src = o.get("source")
            ledger.append({"id": "%s-%03d" % (sub, i), "sub": sub, "op": o["op"], "element": o["element"], "source": src,
                           "lift": ["%s:%s" % (sub, src), "T3-014", "T4-003", "D2"] if src else None,
                           "condition": o.get("condition"), "statement": None, "how": o.get("how") or o.get("why"),
                           "evidence": o["evidence"], "relation": None, "portable": True, "nonportable_hits": [],
                           "kind": KIND_OF[o["op"]], "observation": o.get("observation"), "origin": "labeler", "model_version": "sha256:" + ver, "decision": "pending"})
    _wj(os.path.join(out, "adaptations.jsonl"), ledger)
    _w(os.path.join(D, "DONE"), "returned 2 unreturned 0\n")
    _w(os.path.join(out, "ingest-D.md"), "rooms returned and accepted: 2\n")
    verd = []
    raw = os.path.join(out, "_fleet_raw", "D2v")
    _w(os.path.join(raw, "arm.json"), "{}"); _w(os.path.join(raw, "DONE"), "2 packets\n")
    for sub, tid in (("denmark", "t07"), ("asoiaf", "t02")):
        for rid in ("r1", "r2"):
            line = {"sub": sub, "reader": rid, "verdict": "composes", "themes": [tid], "residue": None,
                    "cannot_tell_under": None, "sentence": "every theme is placed under an element.", "served": "a" * 64}
            verd.append(dict(line, grade="composes"))
            _wj(os.path.join(raw, sub, "%s.jsonl" % rid), [line])
    _wj(os.path.join(out, "verdicts-D.jsonl"), verd)
    _w(os.path.join(out, "_views", "rooms-x-elements.tsv"), "# generated\nroom\tK04\tP07\nasoiaf\tinstantiate\t\ndenmark\tabsent\tadd-condition\n")
    _w(os.path.join(out, "notes-D2.md"), "seed 7; sampled denmark and asoiaf. No split rooms. The figures bound whether "
                                          "the criterion decides, not whether the model is right.\n")
    _w(os.path.join(out, "handback-D2.md"), "nothing\n")
    _w(os.path.join(out, "run_manifest.json"), json.dumps([{"stage": "D2", "labelers_model": "gpt-5-codex", "readers_model": "@preset/cheap"}]))
    _w(os.path.join(root, "RUN.json"), json.dumps({"stage_D2": {"accepted": 2, "reissued": 0, "unreturned": 0}, "handoff_D": {"version": ver}}))


def _plant_bad_code(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adaptations.jsonl"))
    rows[0]["evidence"]["codes"] = ["c9999"]
    _wj(os.path.join(out, "adaptations.jsonl"), rows)


def _plant_portable(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adaptations.jsonl"))
    rows[0]["condition"] = "the artwork sits at Skagen, next to asoiaf"
    _wj(os.path.join(out, "adaptations.jsonl"), rows)


def _plant_one_reader(out, root):
    plant_base(out, root)
    rows = [r for r in jsonl(os.path.join(out, "verdicts-D.jsonl")) if not (r["sub"] == "asoiaf" and r["reader"] == "r2")]
    _wj(os.path.join(out, "verdicts-D.jsonl"), rows)


def _plant_lift(out, root):
    plant_base(out, root)
    rows = jsonl(os.path.join(out, "adaptations.jsonl"))
    rows[0]["lift"] = ["denmark:t07", "T3-099", "T4-003", "D2"]
    _wj(os.path.join(out, "adaptations.jsonl"), rows)


def _plant_element_absent(out, root):
    plant_base(out, root)
    _w(os.path.join(out, "rooms", "asoiaf", "model-D.md"), "# r/asoiaf\n\n## D2\n\nThe room held [P07] [c0011].\n\ngrade: composes\nwhy.\n<!-- end -->\n")


PLANTED = [
    ("a code the store lacks", _plant_bad_code, "not in r/denmark's codes"),
    ("portable true on a named line", _plant_portable, "portable is true while"),
    ("a room with one reader", _plant_one_reader, "R = 2 readers per room"),
    ("a lift off the placements", _plant_lift, "lifts through the placements"),
    ("adapted element not in the room model", _plant_element_absent, "never names adapted element(s)"),
]
