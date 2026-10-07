"""checks/stage_A1.py: the close-check of stage A1, the reading, v38.

Written from stages/STAGE-A1-reading-room-notes.md (its Outputs block, its numbered sections 1 to 6, its
Close section) and from the v37 check it descends from (_v37-source/tools/validate.py, stage01).
What it checks is the SHAPE of the stage's files: existence, parse, ids that resolve, counts that
reconcile. It cannot check whether a judgement is right.

Stage A1 runs in legs: a first leg for the checks, the screen and what is written before reading,
then one leg per room block. The files of the first leg are required at every close. The files
of the last block (`coordinating-rule-A1.md`, `organizing_end-A1.jsonl`, `_head.md`,
`handback-A1.md`) are required once any of them, or `handback-A1.md`, exists; until then the check
prints the reading's progress (notes over the analysed set) and does not fail an unfinished
block. Stage B1's open-check catches a stage A1 that never wrote them.

Files the stage names without giving fields, checked for existence and parse only:
`lexicon-A1.md`, `running-A1.md`, `contrast.md`, `coordinating-rule-A1.md` (prose; only the
concept ids it cites are resolved), `departures.jsonl`, `defects.jsonl`, `handback-A1.md`.

Not carried from v37's stage01:
- `rooms_index.md` as a required output (v38 serves notes through `mem.py note`; the rename
  table).
- `package/case_facts_outcome.jsonl` and its six keys (v38 joins the canvas fields into the
  store's `rooms.jsonl`, which is checked instead).
- `package/pixels.csv` and its five columns (v38 names `canvas/artworks.jsonl`; existence only).
- the census from `package/case_facts.jsonl` (v38: `package/store/rooms.jsonl`, through vlib).
"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need

NOTE_LINES = ("doing:", "week:", "named:", "goal:", "unsettled:", "coder unsure:", "carrying:", "not this:",
              "ended:", "made:")
# `struck by:` is the note's one free line (stage A1 section 4): allowed anywhere, never required.
HEADER_BITS = ("coded share", "off-platform pointers")
CODE_ID = re.compile(r"\bc\d{4}\b")
MANIFEST_KEYS = ("stage", "written_utc", "package_sha256", "tools_commit", "model", "decoding")
END_KEYS = ("sub", "organizing_end_hour", "aftermath_share", "coordinating_turns", "turns_after_73",
            "work_remained", "work_remained_codes", "last_coordinating_code", "aftermath_coordinating_codes")
WORK_REMAINED = ("kept", "lost", "silent")


QUOTED = re.compile("[\"“]([^\"”\n]{0,400})[\"”]")


def note_problems(sub, t, codes=None):
    """The problems of one room note in the fixed form of section 4, as (level, message, shape,
    where). The close-check reports them; the harness's PostToolUse hook returns them to the
    analyst the moment the note is written."""
    out = []
    base = "rooms/%s.md" % sub

    def e(msg, shape, where=base):
        out.append(("err", msg, shape, where))

    def w(msg, shape, where=base):
        out.append(("warn", msg, shape, where))
    if len(t.encode("utf-8")) < 200:
        e("%s is under 200 bytes: a note that short is a placeholder; write the room's note in "
          "the fixed form of stage A1 section 4" % base, "note:placeholder")
        return out
    first = t.lstrip().split("\n", 1)[0]
    if not first.startswith("# r/%s" % sub):
        e("%s: the first line must be `# r/%s  (read <ISO>)   coded share <n>   off-platform pointers <n>`"
          "; it starts %r" % (base, sub, first[:40]), "note:header")
    else:
        lacking = [b for b in HEADER_BITS if b not in first]
        if lacking:
            e("%s: the header line lacks %s; the figures come from rooms.jsonl, a null written as "
              "null" % (base, lacking), "note:header-figures")
        if "(read " not in first:
            e("%s: the header carries no `(read <ISO>)` date" % base, "note:undated")
    missing = [h for h in NOTE_LINES if not re.search(r"^%s" % re.escape(h), t, re.M)]
    if missing:
        e("%s lacks the fixed line(s) %s; every note has the fixed lines of stage A1 section 4"
          % (base, missing), "note:lines")
    m = re.search(r"^carrying:(.*)$", t, re.M)
    if m:
        ids = CODE_ID.findall(m.group(1))
        if len(ids) < 3:
            e("%s: `carrying:` names %d concept id(s); it names three, ids only (c0117 form)"
              % (base, len(ids)), "note:carrying-count")
        for cid in ids:
            if codes and (sub, cid) not in codes:
                e("%s: `carrying:` names %s, which is not a concept of r/%s in the store" % (base, cid, sub),
                  "note:carrying-unresolved", "%s %s" % (base, cid))
    made = re.search(r"^made:", t, re.M)
    if made:
        after = t[made.end():]
        if re.search(r"^(doing|week|named|goal|unsettled|coder unsure|carrying|not this|ended):", after, re.M):
            e("%s: `made:` is not the last of the fixed lines; it is written last, after the forest and "
              "the concepts (rule 7)" % base, "note:made-not-last")
    words = len(t.split())
    if words > 350:
        w("%s is %d words; the form is under 350" % (base, words), "note:long")
    quoted = [q for line in t.splitlines() if not line.startswith("struck by:")
              for q in QUOTED.findall(line) if len(q.split()) >= 4]
    if quoted:
        w("%s quotes the room (%d run(s) of four words or more in quotation marks, first %r); the note carries "
          "concept ids in brackets and no quotes; only `struck by:` holds the room's words"
          % (base, len(quoted), quoted[0][:50]), "note:quotes")
    return out


def _recompute_ends(ctx, ends):
    """Section 5: the hour, the turns after hour 73 and the aftermath share, recomputed from the store's hours
    and the ids each line names; a difference is an error."""
    subs = {r.get("sub") for r in ends if r.get("sub")}
    p = os.path.join(ctx["package"], "store", "codes.jsonl")
    if not subs or not os.path.exists(p):
        return
    hour, after = {}, collections.defaultdict(set)
    for line in open(p, encoding="utf-8"):
        if not line.strip():
            continue
        c = json.loads(line)
        if c.get("sub") not in subs:
            continue
        hour[(c["sub"], c.get("code_id"))] = (c.get("hour"), c.get("item_id"))
        if isinstance(c.get("hour"), (int, float)) and c["hour"] > 73:
            after[c["sub"]].add(c.get("item_id") or c.get("code_id"))
    for r in ends:
        sub = r.get("sub")
        if sub not in subs or "last_coordinating_code" not in r:
            continue
        lc, eh = r.get("last_coordinating_code"), r.get("organizing_end_hour")
        if lc is None:
            if eh is not None:
                err("organizing_end-A1.jsonl %r: an hour with no last_coordinating_code" % sub, shape="end:recompute", where=sub)
        elif (sub, lc) not in hour:
            err("organizing_end-A1.jsonl %r: last_coordinating_code %s is not a concept of the room" % (sub, lc),
                shape="end:recompute", where=sub)
        elif isinstance(hour[(sub, lc)][0], (int, float)) and eh != hour[(sub, lc)][0]:
            err("organizing_end-A1.jsonl %r: organizing_end_hour %s, but %s is at hour %s in the store"
                % (sub, eh, lc, hour[(sub, lc)][0]), shape="end:recompute", where=sub)
        ac = r.get("aftermath_coordinating_codes") or []
        bad = [c for c in ac if (sub, c) not in hour or not (isinstance(hour[(sub, c)][0], (int, float)) and hour[(sub, c)][0] > 73)]
        if bad:
            err("organizing_end-A1.jsonl %r: aftermath_coordinating_codes %s are not concepts of the room after hour 73"
                % (sub, bad[:4]), shape="end:recompute", where=sub)
        late = [c for c in ac if (sub, c) in hour and isinstance(hour[(sub, c)][0], (int, float))
                and isinstance(eh, (int, float)) and hour[(sub, c)][0] > eh]
        if late:
            err("organizing_end-A1.jsonl %r: aftermath coordinating concept(s) %s come after organizing_end_hour %s, "
                "which is the last coordinating turn" % (sub, late[:3], eh), shape="end:recompute", where=sub)
        wbad = [c for c in (r.get("work_remained_codes") or []) if (sub, c) not in hour]
        if wbad:
            err("organizing_end-A1.jsonl %r: work_remained_codes %s are not concepts of the room" % (sub, wbad[:4]),
                shape="end:work-cite", where=sub)
        n_after = len(after.get(sub, set()))
        if r.get("turns_after_73") != n_after:
            err("organizing_end-A1.jsonl %r: turns_after_73 is %s; the store holds %d coded items after hour 73"
                % (sub, r.get("turns_after_73"), n_after), shape="end:recompute", where=sub)
        coord = len({hour[(sub, c)][1] or c for c in ac if (sub, c) in hour})
        share = round(coord / n_after, 3) if n_after else None
        a = r.get("aftermath_share")
        if (share is None) != (a is None) or (share is not None and abs(a - share) > 0.01):
            err("organizing_end-A1.jsonl %r: aftermath_share is %s; the named ids give %s" % (sub, a, share),
                shape="end:recompute", where=sub)


def _is_last_leg(outdir, root=None):
    """A1c is the last leg. With a leg open the step says so; without one (the self-test) the handback does.
    The coordinating rule is written in the last reading block (section 5), so it is no sign of A1c."""
    step = vlib.current_step(root)
    if step:
        return step == "A1c"
    return os.path.exists(os.path.join(outdir, "handback-A1.md"))


def _num_or_null(v):
    return v is None or (isinstance(v, (int, float)) and not isinstance(v, bool))


def _check_notes(outdir, ctx, analysed, frame):
    """rooms/<sub>.md: one per room of the analysed set, in the fixed form of section 4."""
    rooms_dir = os.path.join(outdir, "rooms")
    notes = sorted(p for p in glob.glob(os.path.join(rooms_dir, "*.md")) if not os.path.basename(p).startswith("_"))
    noted = {}
    for n in notes:
        noted[os.path.basename(n)[:-3]] = n
    codes = vlib.store_codes(ctx)
    for sub, p in sorted(noted.items()):
        t = open(p, encoding="utf-8", errors="replace").read()
        for level, msg, shape, where in note_problems(sub, t, codes):
            (err if level == "err" else warn)(msg, shape=shape, where=where)
    if frame is not None:
        stray = sorted(set(noted) - frame)
        if stray:
            err("out/rooms/ holds notes for names not in the frame: %s; a note is for a room of the "
                "analysed set" % stray[:6])
    if analysed is not None:
        dropped_noted = sorted(set(noted) & (frame - analysed))
        if dropped_noted:
            warn("out/rooms/ holds notes for dropped rooms: %s" % dropped_noted[:6])
    return noted


def _order(outdir, analysed, frame):
    p = os.path.join(outdir, "order-A1.txt")
    if not os.path.exists(p):
        if glob.glob(os.path.join(outdir, "rooms", "*.md")):
            err("order-A1.txt is absent; section 3 writes the reading order there, one line per room, "
                "`<block><TAB><sub>`, before the first room is opened", shape="order:absent")
        else:
            warn("order-A1.txt is not written yet; section 3 writes it before the first room is opened")
        return None
    order, seen = [], set()
    for i, line in enumerate(open(p, encoding="utf-8"), 1):
        f = line.strip().split("\t") if "\t" in line else line.split()
        if not f or f[0].startswith("#"):
            continue
        s = vlib.canon(f[-1], frame)
        if s in seen:
            err("order-A1.txt line %d names r/%s twice" % (i, s), shape="order:twice", where=s)
            continue
        if frame is not None and s not in frame:
            err("order-A1.txt line %d names %r, which is not a room of the frame" % (i, s), shape="order:notinframe", where=s)
            continue
        seen.add(s)
        if analysed is not None and s not in analysed:
            err("order-A1.txt line %d names r/%s, a dropped room; the order holds the analysed set only" % (i, s),
                shape="order:dropped", where=s)
            continue
        order.append(s)
    if analysed is not None:
        miss = sorted(analysed - seen)
        if miss:
            err("order-A1.txt leaves out %d room(s) of the analysed set (%s); every room is in the order once"
                % (len(miss), ", ".join(miss[:6])), shape="order:missing", where=miss[0])
    return order


def _stamp(t):
    return str(t or "").replace("Z", "")[:19]


def _check_codes_read(outdir, noted):
    reads = {}
    for r in jsonl(os.path.join(outdir, "_mem_reads-A1.jsonl")) or []:
        if r.get("verb") == "codes" and not r.get("refused"):
            s = (r.get("opts") or {}).get("sub")
            if s:
                reads.setdefault(vlib.canon(s).lower(), []).append(_stamp(r.get("t")))
    for r in jsonl(os.path.join(outdir, "_cite_reads-A1.jsonl")) or []:
        s = (r.get("opts") or {}).get("room")
        if s and not str(r.get("verdict") or "").startswith(("no such", "REJECT")):
            reads.setdefault(vlib.canon(s).lower(), []).append(_stamp(r.get("t")))
    notes_t = {}
    for d in vlib.diary_lines(outdir, "A1"):
        ids = [vlib.canon(i).lower() for i in (d.get("ids") or [])]
        if d.get("kind") == "note" and len(ids) == 1:      # the note line names its one room (section 4)
            notes_t.setdefault(ids[0], _stamp(d.get("t")))
    for sub in sorted(noted):
        ts = reads.get(sub.lower())
        if not ts:
            err("rooms/%s.md: no `mem.py codes --sub %s` or `cite.py --room %s` call is logged for this room; section "
                "4 reads the concepts before the account" % (sub, sub, sub), shape="note:codes-unread", where=sub)
        elif sub.lower() in notes_t and min(ts) > notes_t[sub.lower()]:
            err("rooms/%s.md: its concepts were first read at %s, after the note line at %s; section 4 reads them "
                "before the note" % (sub, min(ts), notes_t[sub.lower()]), shape="note:codes-late", where=sub)


def _check_leads(outdir, frame, last):
    p = os.path.join(outdir, "leads-A1.jsonl")
    if not os.path.exists(p):
        if last:
            err("leads-A1.jsonl is absent; section 4 writes it, empty when no tie was left unchecked")
        return
    for i, r in enumerate(jsonl(p) or [], 1):
        w = "leads-A1.jsonl line %d" % i
        for k in ("sub", "other"):
            if r.get(k):
                r[k] = vlib.canon(r[k], frame)
        if r.get("sub") and r.get("sub") == r.get("other"):
            err("%s names r/%s on both sides; a lead ties two rooms" % (w, r["sub"]), shape="leads:self", where=w)
        for k in ("sub", "other", "why"):
            if not str(r.get(k) or "").strip():
                err("%s has no %s; a lead is {sub, other, why, item}" % (w, k), shape="leads:field", where=w)
        for k in ("sub", "other"):
            if frame is not None and r.get(k) and r[k] not in frame:
                err("%s: %s %r is not a room of the frame" % (w, k, r[k]), shape="leads:notinframe", where=w)


def _covered(spans, total):
    """True when the served line spans [offset, offset+lines) cover 0..total."""
    if not total:
        return True
    end = 0
    for a, b in sorted(spans):
        if a > end:
            return False
        end = max(end, b)
    return end >= total


def _check_catchup_reads(outdir, root):
    """The catch-up pass (blocks 20 on, J 2026-10-07): every room whose note this leg amends has its case.md and
    brief.md served whole by mem.py, and served before the note line. The read log is written by mem.py, not by
    the analyst, so a cut route shows here whatever the diary says (J, 2026-10-07, after A1's handback)."""
    p = os.path.join(root or ".", ".leg")
    leg = open(p, encoding="utf-8").read().strip() if os.path.exists(p) else ""
    m = re.match(r"^A1b-(\d+)", leg)
    if not m or int(m.group(1)) < 20:
        return
    base = "A1b-%02d" % int(m.group(1))
    block = set()
    for line in (text(outdir, "order-A1.txt") or "").splitlines():
        b = re.match(r"^#(\d+)\t(\S+)", line)
        if b and int(b.group(1)) == int(m.group(1)):
            block.add(vlib.canon(b.group(2)).lower())
    diary = [d for d in vlib.diary_lines(outdir, "A1")]
    pass_start = min((_stamp(d.get("t")) for d in diary if re.match(r"^A1b-([2-9]\d|\d{3})", str(d.get("leg") or ""))),
                     default="")
    notes_t = {}
    for d in diary:
        if not str(d.get("leg") or "").startswith(base):
            continue
        ids = [vlib.canon(i).lower() for i in (d.get("ids") or [])]
        if d.get("kind") == "note" and len(ids) == 1:
            notes_t[ids[0]] = max(notes_t.get(ids[0], ""), _stamp(d.get("t")))
    spans, whole_at = {}, {}
    for r in jsonl(os.path.join(outdir, "_mem_reads-A1.jsonl")) or []:
        if r.get("verb") not in ("case", "brief") or r.get("refused") or not r.get("args"):
            continue
        t = _stamp(r.get("t"))
        if pass_start and t < pass_start:
            continue
        k = (r["verb"], vlib.canon(r["args"][0]).lower())
        off = int(r.get("offset") or 0)
        spans.setdefault(k, []).append((off, off + int(r.get("lines") or 0)))
        if k not in whole_at and _covered(spans[k], int(r.get("total") or 0)):
            whole_at[k] = t
    for sub in sorted(notes_t):
        for verb, f in (("case", "case.md"), ("brief", "brief.md")):
            w = whole_at.get((verb, sub))
            if w is None:
                served = sum(b - a for a, b in spans.get((verb, sub), []))
                err("rooms/%s.md: amended in %s, but %s was not served whole in the catch-up pass (%s); read it whole "
                    "with mem.py %s %s before the note (J, 2026-10-07)"
                    % (sub, base, f, "never served" if not spans.get((verb, sub)) else "%d lines served, not covering the file" % served,
                       verb, sub), shape="catchup:not-whole", where=sub)
            elif w > notes_t[sub]:
                err("rooms/%s.md: its note line at %s comes before %s was served whole at %s; the file is read whole "
                    "before the note is amended" % (sub, notes_t[sub], f, w), shape="catchup:late", where=sub)
    for sub in sorted(block - set(notes_t)):
        warn("block %s: r/%s has no note line in this leg; it is still to be read in the catch-up pass" % (m.group(1), sub),
             shape="catchup:pending", where=sub)


def check(root, outdir, ctx):
    need(outdir, "notes-A1.md", "contrast.md", "dropped.jsonl", "departures.jsonl", "defects.jsonl",
         "run_manifest.json")
    last = _is_last_leg(outdir, root)
    frame = vlib.frame("A1", "the frame, the screen and every room note against it", ctx)
    sets = vlib.analysed_set("A1", "the analysed set", outdir, ctx)
    analysed = sets[0] if sets else None

    # the screen (section 2): every drop names a room of the frame, with a why
    dropped = jsonl(os.path.join(outdir, "dropped.jsonl"))
    if dropped is not None:
        seen = set()
        for d in dropped:
            sub = d.get("sub")
            if not sub:
                err("dropped.jsonl: a line has no `sub`; every drop is {\"sub\": ..., \"why\": ...}",
                    shape="dropped:nosub", where=json.dumps(d)[:60])
                continue
            if frame is not None and sub not in frame:
                err("dropped.jsonl names %r, which is not in the frame (store/rooms.jsonl)" % sub,
                    shape="dropped:notinframe", where=sub)
            if not (d.get("why") or "").strip():
                err("dropped.jsonl line for %r carries no why; contract section 5 asks for the reason on "
                    "every drop" % sub, shape="dropped:nowhy", where=sub)
            if sub in seen:
                err("dropped.jsonl drops %r twice" % sub, shape="dropped:dup", where=sub)
            seen.add(sub)
        if frame is not None:
            n = len(frame)
            print("  frame %d, dropped %d, analysed %d%s" % (
                n, len(seen), n - len(seen & frame),
                "" if seen else " : dropped.jsonl is written and empty, so the screen ran and dropped nothing"))

    # the store, present and whole (section 1): the six canvas fields on every room of the frame
    rows = vlib.rooms(ctx) or []
    if rows:
        lacking = [r.get("sub") for r in rows if not all(k in r for k in vlib.CANVAS)]
        if lacking:
            err("package/store/rooms.jsonl: %d room(s) lack one of the six canvas fields (%s ...); the build "
                "joins them in (`build_store.py --join-canvas`), and a room of the frame with no canvas line "
                "is a defect line in defects.jsonl" % (len(lacking), lacking[:5]))
    if not glob.glob(os.path.join(ctx["package"], "**", "artworks.jsonl"), recursive=True):
        warn("canvas/artworks.jsonl is not under the package; stage A1 reads it beside each room's account "
             "(section 1, the canvas)")

    # the notes (section 4)
    noted = _check_notes(outdir, ctx, analysed, frame)
    if noted:
        need(outdir, "lexicon-A1.md", "running-A1.md")
        for n in ("lexicon-A1.md", "running-A1.md"):
            if os.path.exists(os.path.join(outdir, n)) and not text(outdir, n).strip():
                err("%s is empty; it is appended at every block (section 4)" % n)
    if analysed is not None:
        done = sorted(set(noted) & analysed)
        left = sorted(analysed - set(noted))
        print("  room notes %d over an analysed set of %d" % (len(done), len(analysed)))
        if left and last:
            err("%d room(s) of the analysed set have no note in out/rooms/ (%s ...): the last block closes "
                "only when every room is read whole and written about; a room read and not written about "
                "is a room not read" % (len(left), ", ".join(left[:6])))
        elif left:
            print("  %d room(s) still to note; the stage closes when every room of the analysed set has one"
                  % len(left))

    # the order on disk (section 3): out/order-A1.txt, every room of the analysed set once
    order = _order(outdir, analysed, frame)
    # no room left behind (section 4): every room before the last one noted has its note, at every block
    if order and noted:
        real = {s for s, p in noted.items() if os.path.getsize(p) >= 200}      # a placeholder is not a note
        pos = max((order.index(s) for s in real if s in order), default=-1)
        gaps = [s for s in order[:pos] if s not in real] if pos >= 0 else []
        if gaps:
            err("%d room(s) before the last one noted in order-A1.txt have no note (%s): a room was skipped; read it "
                "now (`mem.py next` names it), before the block closes" % (len(gaps), ", ".join(gaps[:6])),
                shape="order:gap", where=gaps[0])
    # the concepts read before the note (section 4): a logged codes or cite call for the room
    _check_codes_read(outdir, noted)
    _check_catchup_reads(outdir, root)
    # leads (section 4): parse; required at the last block
    _check_leads(outdir, frame, last)

    # the diary: a room opened is logged before its note is written (moments to log; rule 1)
    diary = vlib.diary_lines(outdir, "A1")
    opened, noted_line = set(), set()
    for d in diary:
        for i in d.get("ids") or []:
            (noted_line if d.get("kind") == "note" else opened).add(vlib.canon(i))
    for sub in sorted(noted):
        if vlib.canon(sub) not in opened:
            err("rooms/%s.md exists but the diary holds no stage-A1 line naming %s; log `mem.py log --kind opened "
                "--ids %s` before the note and a `note` line after it (rule 20)" % (sub, sub, sub),
                shape="diary:room-unlogged", where=sub)
        elif vlib.canon(sub) not in noted_line:
            err("rooms/%s.md exists and the diary holds no `note` line for it; after the note, `mem.py log \"noted\" "
                "--kind note --ids %s` (section 4)" % (sub, sub), shape="diary:note-unlogged", where=sub)

    # notes-A1.md (sections 1, 3, 6)
    n1 = text(outdir, "notes-A1.md")
    if not n1.strip():
        err("notes-A1.md is empty; the order, the contrast, the three sentences and every check of section 1 "
            "go there")
    else:
        low = n1.lower()
        if "self-test" not in low and "self test" not in low:
            warn("notes-A1.md does not mention the self-test; section 1 runs `validate.py --self-test` once "
                 "and pastes its report there")
        if "concept_reach_threshold" not in n1:
            err("notes-A1.md does not declare `concept_reach_threshold`; section 1 (the instrument's shape) "
                "writes it there and the contract's section 5 uses it at C2 to D3")
    if not text(outdir, "contrast.md").strip():
        err("contrast.md is empty; section 3 writes the onset contrast there, with the rule that defines each "
            "side, the named members and the size of each")
    elif frame is not None:
        ct = text(outdir, "contrast.md")
        if not any(re.search(r"\b%s\b" % re.escape(s), ct) for s in frame):
            err("contrast.md names no room of the frame; section 3 asks for the named members of each side")

    # run_manifest.json (section 6)
    ents = vlib.manifest_entry(outdir, "A1", "the reading")
    if ents:
        e = ents[0]
        for k in MANIFEST_KEYS:
            if k not in e or e[k] in (None, ""):
                err("run_manifest.json stage-A1 entry lacks `%s`; section 6 gives the entry's form, with the "
                    "package hash from package/FRAME.md and the tools commit" % k,
                    shape="manifest:missing-key", where=k)
        if e.get("package_sha256") and not re.fullmatch(r"[0-9a-f]{64}", str(e["package_sha256"])):
            err("run_manifest.json stage-A1 entry: package_sha256 is not a 64-character hex digest")
        if not isinstance(e.get("decoding"), dict):
            err("run_manifest.json stage-A1 entry: `decoding` is not an object (temperature, top_p)")

    # the ledgers opened here (Outputs): parse, and a line carries its stage
    for name in ("departures.jsonl", "defects.jsonl"):
        rows = jsonl(os.path.join(outdir, name))
        if rows is None:
            continue
        if not rows:
            print("  %s is written and empty" % name)
            continue
        for r in rows:
            if "stage" not in r:
                err("%s: a line carries no `stage`; every ledger line names the stage that wrote it" % name,
                    shape="ledger:nostage:%s" % name, where=json.dumps(r)[:60])
        print("  %s carries %d line(s)" % (name, len(rows)))

    # the last block (section 5, Close)
    if last:
        need(outdir, "coordinating-rule-A1.md", "organizing_end-A1.jsonl", "_head.md", "handback-A1.md")
        cr = text(outdir, "coordinating-rule-A1.md")
        if os.path.exists(os.path.join(outdir, "coordinating-rule-A1.md")):
            ids = CODE_ID.findall(cr)
            if len(set(ids)) < 20:
                err("coordinating-rule-A1.md cites %d distinct concept ids; section 5 asks for ten on each "
                    "side as examples" % len(set(ids)))
            codes = vlib.store_codes(ctx)
            if codes:
                known = {c for _, c in codes}
                bad = sorted({c for c in ids if c not in known})
                if bad:
                    err("coordinating-rule-A1.md cites concept ids the store does not hold: %s" % bad[:6])
        ends = jsonl(os.path.join(outdir, "organizing_end-A1.jsonl"))
        if ends is not None:
            seen = set()
            for r in ends:
                sub = r.get("sub")
                where = sub or json.dumps(r)[:60]
                lacking = [k for k in END_KEYS if k not in r]
                if lacking:
                    err("organizing_end-A1.jsonl line for %r lacks %s; section 5 gives the nine fields"
                        % (sub, lacking), shape="end:keys", where=where)
                if analysed is not None and sub not in analysed:
                    err("organizing_end-A1.jsonl names %r, which is not in the analysed set" % sub,
                        shape="end:notanalysed", where=where)
                if sub in seen:
                    err("organizing_end-A1.jsonl holds %r twice; one line per room" % sub, shape="end:dup", where=where)
                seen.add(sub)
                if not _num_or_null(r.get("organizing_end_hour")):
                    err("organizing_end-A1.jsonl %r: organizing_end_hour is not a number or null" % sub,
                        shape="end:hour", where=where)
                a = r.get("aftermath_share")
                if not _num_or_null(a) or (a is not None and not 0 <= a <= 1):
                    err("organizing_end-A1.jsonl %r: aftermath_share is not a share in [0, 1] or null" % sub,
                        shape="end:share", where=where)
                for k in ("coordinating_turns", "turns_after_73"):
                    v = r.get(k)
                    if not (isinstance(v, int) and not isinstance(v, bool) and v >= 0):
                        err("organizing_end-A1.jsonl %r: %s is not a non-negative integer" % (sub, k),
                            shape="end:int", where=where)
                wr, wc = r.get("work_remained"), r.get("work_remained_codes")
                if "work_remained" in r and wr not in WORK_REMAINED:
                    err("organizing_end-A1.jsonl %r: work_remained is %r, not kept, lost or silent" % (sub, wr),
                        shape="end:work", where=where)
                elif "work_remained" in r and not isinstance(wc, list):
                    err("organizing_end-A1.jsonl %r: work_remained_codes is not a list" % sub, shape="end:work", where=where)
                elif wr in ("kept", "lost") and not wc:
                    err("organizing_end-A1.jsonl %r: work_remained is %s but no concept says so; a claim from the record "
                        "cites the record, and a room that never says is silent" % (sub, wr), shape="end:work-cite", where=where)
                elif wr == "silent" and wc:
                    err("organizing_end-A1.jsonl %r: work_remained is silent but cites concepts; silent means the record "
                        "never says" % sub, shape="end:work-cite", where=where)
            _recompute_ends(ctx, ends)
            if analysed is not None:
                left = sorted(analysed - seen)
                if left:
                    err("organizing_end-A1.jsonl has no line for %d room(s) of the analysed set (%s ...); one "
                        "line per room, from the forest and never from the canvas"
                        % (len(left), ", ".join(left[:6])))
            print("  organizing_end-A1.jsonl: %d lines" % len(ends))
    else:
        if not os.path.exists(os.path.join(outdir, "_head.md")):
            if vlib.current_step(root) in (None, "A1a"):
                warn("_head.md is not written yet; it is written at the close of the first leg, A1a")
            else:
                err("_head.md is not written; it was due at the close of A1a, and every leg opens with it",
                    shape="head:missing")


# ---- the self-test ------------------------------------------------------------------------------

def _w(outdir, name, content=""):
    p = os.path.join(outdir, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def _wj(outdir, name, rows):
    _w(outdir, name, "".join(json.dumps(r) + "\n" for r in rows))


def _note(sub, carrying="c0117, c0118, c0117", made_last=True):
    body = ("# r/%s  (read 2026-09-24T10:00:00Z)   coded share 0.41   off-platform pointers 2\n"
            "doing:      calling for hands at the border and recruiting outside [c0117] [c0118]\n"
            "week:       hour 0 a call, hour 20 a plan, hour 60 a defence, hour 73 the freeze\n"
            "named:      the neighbours, for the border\n"
            "goal:       hold the flag, settled by hour 20, never changed\n"
            "unsettled:  whether to expand north\n"
            "coder unsure: none\n"
            "carrying:   %s\n"
            "not this:   that the room was large\n"
            "ended:      hour 71, then recounting\n" % (sub, carrying))
    if made_last:
        body += "made:       the flag held at the freeze, against a doing line that says the same\n"
    else:
        body = body.replace("ended:", "made:       the flag held\nended:")
    return body


def _base(outdir, root, subs=("denmark", "asoiaf", "sweden"), last=True):
    store = os.path.join(root, "package", "store", "rooms.jsonl")
    rows = [dict({"sub": s}, **{k: 1 for k in vlib.CANVAS}) for s in subs]
    open(store, "w", encoding="utf-8").write("".join(json.dumps(r) + "\n" for r in rows))
    _wj(outdir, "dropped.jsonl", [{"sub": "sweden", "why": "wrote nothing about the event"}])
    _w(outdir, "notes-A1.md", "# notes\nself-test pasted here.\nconcept_reach_threshold: 400\n")
    _w(outdir, "contrast.md", "# onset contrast\nearly: denmark. late: asoiaf.\n")
    _w(outdir, "departures.jsonl", "")
    _w(outdir, "defects.jsonl", "")
    _w(outdir, "lexicon-A1.md", "border  denmark  i0001\n")
    _w(outdir, "running-A1.md", "calls for hands  (denmark)\n")
    _w(outdir, "run_manifest.json", json.dumps([{
        "stage": "A1", "written_utc": "2026-09-24T10:00:00Z", "package_sha256": "a" * 64,
        "tools_commit": "abc123", "model": "opus", "decoding": {"temperature": 0.0, "top_p": 1.0},
        "seeds": {}, "n_agents": None, "notes": ""}]))
    _w(outdir, "rooms/denmark.md", _note("denmark"))
    _w(outdir, "rooms/asoiaf.md", _note("asoiaf", carrying="c0011, c0011, c0011"))
    _w(outdir, "order-A1.txt", "01\tdenmark\n01\tasoiaf\n")
    _wj(outdir, "_mem_reads-A1.jsonl", [
        {"t": "2026-09-24T09:58:00Z", "verb": "codes", "opts": {"sub": "denmark"}},
        {"t": "2026-09-24T09:59:00Z", "verb": "codes", "opts": {"sub": "asoiaf"}}])
    _wj(outdir, "diary/A1-1.jsonl", [
        {"t": "2026-09-24T10:00:00Z", "stage": "A1", "leg": "A1-block-1", "kind": "opened", "ids": ["denmark"], "text": "opened"},
        {"t": "2026-09-24T10:01:00Z", "stage": "A1", "leg": "A1-block-1", "kind": "opened", "ids": ["asoiaf"], "text": "opened"},
        {"t": "2026-09-24T10:30:00Z", "stage": "A1", "leg": "A1-block-1", "kind": "note", "ids": ["denmark"], "text": "noted"},
        {"t": "2026-09-24T10:31:00Z", "stage": "A1", "leg": "A1-block-1", "kind": "note", "ids": ["asoiaf"], "text": "noted"}])
    if last:
        # the fixture store holds three concepts; the rule cites twenty, so the store copy gets more
        cp = os.path.join(root, "package", "store", "codes.jsonl")
        with open(cp, "a", encoding="utf-8") as f:
            for i in list(range(100, 110)) + list(range(12, 19)):
                h = {108: 71, 109: 80}.get(i, 60 + i - 100 if i >= 100 else 50 + i - 12)
                f.write(json.dumps({"sub": "denmark" if i >= 100 else "asoiaf", "code_id": "c%04d" % i,
                                    "theme_id": "t07", "first_order": "x", "text": "words %d" % i,
                                    "hour": h, "item_id": "i%04d" % i}) + "\n")
        ids_a = " ".join("c%04d" % i for i in range(100, 110))
        ids_b = " ".join("c%04d" % i for i in range(117, 119)) + " " + " ".join("c%04d" % i for i in range(11, 19))
        _w(outdir, "coordinating-rule-A1.md", "# rule\ncounts: %s\ndoes not: %s\n" % (ids_a, ids_b))
        _wj(outdir, "organizing_end-A1.jsonl", [
            {"sub": "denmark", "organizing_end_hour": 71, "aftermath_share": 0.0, "coordinating_turns": 40, "turns_after_73": 1,
             "work_remained": "kept", "work_remained_codes": ["c0117"], "last_coordinating_code": "c0108",
             "aftermath_coordinating_codes": []},
            {"sub": "asoiaf", "organizing_end_hour": 56, "aftermath_share": None, "coordinating_turns": 12, "turns_after_73": 0,
             "work_remained": "silent", "work_remained_codes": [], "last_coordinating_code": "c0018",
             "aftermath_coordinating_codes": []}])
        _w(outdir, "_head.md", "# head\n")
        _w(outdir, "handback-A1.md", "# handback\n")
        _wj(outdir, "leads-A1.jsonl", [{"sub": "denmark", "other": "asoiaf", "why": "named once", "item": "i0001"}])


def _plant_missing_note(outdir, root):
    _base(outdir, root)
    os.remove(os.path.join(outdir, "rooms", "asoiaf.md"))


def _plant_bad_lines(outdir, root):
    _base(outdir, root)
    t = open(os.path.join(outdir, "rooms", "denmark.md")).read().replace("goal:      ", "aim:       ")
    _w(outdir, "rooms/denmark.md", t)


def _plant_carrying(outdir, root):
    _base(outdir, root)
    _w(outdir, "rooms/denmark.md", _note("denmark", carrying="c0117, c0118, c9999"))


def _plant_end_missing(outdir, root):
    _base(outdir, root)
    _wj(outdir, "organizing_end-A1.jsonl", [
        {"sub": "denmark", "organizing_end_hour": 71, "aftermath_share": 0.1, "coordinating_turns": 40, "turns_after_73": 5,
         "work_remained": "kept", "work_remained_codes": ["c0117"]}])


def _plant_end_hour_wrong(outdir, root):
    _base(outdir, root)
    rows = jsonl(os.path.join(outdir, "organizing_end-A1.jsonl"))
    rows[0]["organizing_end_hour"] = 73
    _wj(outdir, "organizing_end-A1.jsonl", rows)


def _plant_work_uncited(outdir, root):
    _base(outdir, root)
    _wj(outdir, "organizing_end-A1.jsonl", [
        {"sub": "denmark", "organizing_end_hour": 71, "aftermath_share": 0.1, "coordinating_turns": 40, "turns_after_73": 5,
         "work_remained": "lost", "work_remained_codes": []},
        {"sub": "asoiaf", "organizing_end_hour": 60, "aftermath_share": None, "coordinating_turns": 12, "turns_after_73": 0,
         "work_remained": "silent", "work_remained_codes": []}])


def _plant_dropped(outdir, root):
    _base(outdir, root)
    _wj(outdir, "dropped.jsonl", [{"sub": "narnia", "why": "x"}])


def _plant_unlogged(outdir, root):
    _base(outdir, root)
    _wj(outdir, "diary/A1-1.jsonl", [
        {"t": "2026-09-24T10:00:00Z", "stage": "A1", "leg": "A1-block-1", "kind": "opened", "ids": ["denmark"], "text": "opened"}])


def _plant_threshold(outdir, root):
    _base(outdir, root)
    _w(outdir, "notes-A1.md", "# notes\nself-test pasted here.\n")


def _plant_gap(outdir, root):
    _base(outdir, root, last=False)
    os.remove(os.path.join(outdir, "rooms", "denmark.md"))


def _plant_codes_unread(outdir, root):
    _base(outdir, root)
    _wj(outdir, "_mem_reads-A1.jsonl", [{"t": "2026-09-24T09:58:00Z", "verb": "codes", "opts": {"sub": "denmark"}}])


def _plant_lead(outdir, root):
    _base(outdir, root)
    _wj(outdir, "leads-A1.jsonl", [{"sub": "denmark", "other": "asoiaf", "item": "i0001"}])


def _plant_order_missing(outdir, root):
    _base(outdir, root)
    _w(outdir, "order-A1.txt", "01\tdenmark\n")


PLANTED = [
    ("a room of the analysed set unnoted", _plant_missing_note, "have no note in out/rooms/"),
    ("a note lacking a fixed line", _plant_bad_lines, "lacks the fixed line(s)"),
    ("carrying names an unknown code", _plant_carrying, "is not a concept of r/denmark"),
    ("organizing_end short a room", _plant_end_missing, "organizing_end-A1.jsonl has no line for"),
    ("work lost with nothing said", _plant_work_uncited, "but no concept says so"),
    ("an end hour the store does not give", _plant_end_hour_wrong, "is at hour 71 in the store"),
    ("a drop outside the frame", _plant_dropped, "which is not in the frame"),
    ("a room opened and not logged", _plant_unlogged, "the diary holds no stage-A1 line naming"),
    ("no concept_reach_threshold", _plant_threshold, "does not declare `concept_reach_threshold`"),
    ("a room skipped in the order", _plant_gap, "a room was skipped"),
    ("a room's concepts never read", _plant_codes_unread, "no `mem.py codes --sub asoiaf`"),
    ("a lead without why", _plant_lead, "has no why"),
    ("the order short a room", _plant_order_missing, "leaves out 1 room"),
]
