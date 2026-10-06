#!/usr/bin/env python3
"""verify_room.py — the scheduler's mechanical checks on one room.

    python3 verify_room.py --room rooms/<sub> [--batch NN] [--fork <name>] [--brief]

With --batch NN: the checks a fleet coder's directory must pass before the lead collects it.
Without: the checks a run must pass once the lead has closed it. Exit 0 only when every check
passes; every failure names the file and the reason. Nothing here reads a thread for its
meaning: these are the things a reader cannot see and a script can.

Per batch (before collect):
  B1  the journal exists and disposes every thread of the slice, none twice, none outside it
  B2  read.py audit: no thread claims more reading than read.py served
  B3  no code or pointer sits on an opening given as context
  B4  case.md and notes.md exist, case.md carries the contract's sections, every episode
      or exchange in the chronology carries a tag
  B5  every line the coder added to timeline.md and lexicon.md carries an item id;
      missing-id lines are surfaced for the lead to strike during collection
  B6  the coder's directory holds nothing unexpected at top level (a stray script is a note,
      not a failure), and the instrument files are unchanged since dispatch
  B7  a transcript is present, or the scheduler is told to write one from the final message

The brief (--brief, when the writer has ended):
  F1  brief/out/brief.md exists; harness claims are checked against the raw pre-week record
  F2  Evidence base and the nine contract sections are substantive Markdown sections
  F3  read_brief receipts prove body reading and active-day coverage (or a disclosed ceiling)
  F4  corrected citations resolve to the named raw item and to a body span actually served
  F5  a transcript is present and not empty
  F6  brief/_manifest.json is present and its files still hash to what it recorded

At the end (after the lead closes):
  E1  audit_fleet PASSED (branch A: --branch A)
  E2  close_run --role lead: every check; every batch: close_run --role fleet, every check
      (documented v30 C3 compatibility for a fully out-of-scope, zero-code fleet slice)
  E3  branch B: the lead's read log holds no read or find before consolidated_utc
  E4  case.md: the contract's sections; every backticked id in case.md exists in the record
      (thread or item); branch B with more than one slice: at least one [crosses NN|MM]
  E5  notes.md repeats the gate in one line (branch B); out/ledger.md has an entry per slice
  E6  (a note, not a failure) an hour written right beside a thread id that disagrees with
      the record by more than 0.1 h; the scheduler reads those lines
"""
import argparse, glob, gzip, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
YARD = os.path.dirname(HERE)

SECTIONS = ["## Chronology", "## Relations", "## Posts against comments", "## Counter-reading",
            "## Saturation", "## Selection", "## Absence"]
ID_RE = re.compile(r"`(6[0-9a-z]{4,5}|d[fg][0-9a-z]{4,5})`")   # 2017 thread ids and comment ids
ID_RX = r"\b(6[0-9a-z]{4,5}|d[fg][0-9a-z]{4,5})\b"               # the same, bare (facts files)


def all_passed(close_run_output):
    """close_run prints 'N of M checks passed.'; every check passed when N == M."""
    m = re.search(r"(\d+) of (\d+) checks passed", close_run_output)
    return bool(m) and m.group(1) == m.group(2)


def jl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def sh(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def close_run_cmd(rundir, role):
    """Use the corrected yard-level v32 gate without mutating the archived run."""
    mp = os.path.join(rundir, "_manifest.json")
    instrument = None
    if os.path.exists(mp):
        try:
            instrument = json.load(open(mp, encoding="utf-8")).get("instrument")
        except (OSError, ValueError):
            pass
    central = os.path.join(YARD, "_instrument", "v32", "close_run.py")
    if instrument == "v32" and os.path.exists(central):
        return [sys.executable, "-B", central, ".", "--role", role]
    return ["python3", "close_run.py", ".", "--role", role]


class Report:
    def __init__(self):
        self.fails, self.notes = [], []

    def fail(self, code, msg):
        self.fails.append("%s  %s" % (code, msg))

    def note(self, msg):
        self.notes.append(msg)

    def done(self):
        for n in self.notes:
            print("  " + n)
        if self.fails:
            print("FAILED (%d):" % len(self.fails))
            for f in self.fails:
                print("  - " + f)
            return 1
        print("PASSED")
        return 0


def record_ids(rec_path):
    ids, threads = set(), set()
    for r in jl(rec_path):
        if "id" in r:
            ids.add(r["id"])
            if r.get("kind") == "post":
                threads.add(r["id"])
            elif r.get("link_id"):
                threads.add(r["link_id"][3:])
    return ids, threads


def coded_threads_without_live_codes(journal, dispositions):
    retracted = {r.get("code_id") for r in journal if r.get("kind") == "retract"}
    live_threads = {r["rec"]["thread_id"] for r in journal
                    if r.get("kind") == "code" and not r["rec"].get("retracted")
                    and r["rec"].get("code_id") not in retracted}
    return sorted(t for t, d in dispositions.items()
                  if d.get("verdict") == "coded" and t not in live_threads)


def zero_code_fleet_compatibility(bdir, close_output):
    """v30 C3 requires a `none` verdict for zero codes, but fleet coders may not give
    a verdict. Accept only the exact all-out-of-scope case with every other check passed.
    Keep the copied instrument and all agent outputs immutable; disclose this exception.
    This function is used only after close_run was explicitly invoked with --role fleet.
    """
    failed = re.findall(r"^\s*FAIL\s+(C\d+)\b", close_output, re.M)
    total = re.search(r"(\d+) of (\d+) checks passed", close_output)
    if failed != ["C3"] or not total or int(total[1]) + 1 != int(total[2]):
        return False
    if "cannot verify citations — no codes were recorded" not in close_output:
        return False
    out = os.path.join(bdir, "out")
    if not os.path.isfile(os.path.join(bdir, "coder_corpus.jsonl")):
        return False
    if not os.path.isfile(os.path.join(out, "codes.jsonl")) or jl(os.path.join(out, "codes.jsonl")):
        return False
    threads = jl(os.path.join(out, "threads.jsonl"))
    journal = jl(os.path.join(out, "_journal.jsonl"))
    recorded = [r["rec"] for r in journal if r.get("kind") == "thread"]
    if any(r.get("kind") == "code" for r in journal):
        return False
    if not threads or not recorded or any(t.get("verdict") != "out_of_scope" for t in threads + recorded):
        return False
    exported_ids = [t.get("thread_id") for t in threads]
    recorded_ids = [t.get("thread_id") for t in recorded]
    return (None not in exported_ids and len(set(exported_ids)) == len(exported_ids)
            and len(set(recorded_ids)) == len(recorded_ids)
            and set(exported_ids) == set(recorded_ids))


def check_batch(run, nn, R):
    gate = json.load(open(os.path.join(run, "out", "_gate.json")))
    sl = next((s for s in gate["slices"] if s["batch"] == nn), None)
    if sl is None:
        R.fail("B1", "no slice %s in the gate" % nn); return
    bdir = os.path.join(run, "fleet", "batch_%s" % nn)
    jp = os.path.join(bdir, "out", "_journal.jsonl")
    if not os.path.exists(jp):
        R.fail("B1", "no journal at %s; the coder did not run" % os.path.relpath(jp, run)); return
    J = jl(jp)
    disp = {}
    for j in J:
        if j.get("kind") == "thread":
            t = j["rec"]["thread_id"]
            if t in disp:
                R.fail("B1", "thread %s disposed twice" % t)
            disp[t] = j["rec"]
    want = set(sl["threads"])
    missing = want - set(disp)
    stray = set(disp) - want
    if missing:
        R.fail("B1", "%d threads of the slice not disposed: %s" % (len(missing), sorted(missing)[:8]))
    if stray:
        R.fail("B1", "%d threads disposed that are not in the slice: %s" % (len(stray), sorted(stray)[:8]))
    empty_coded = coded_threads_without_live_codes(J, disp)
    if empty_coded:
        R.fail("B1", "coded threads have no live code (would fail the forest audit): %s" % empty_coded)
    codes = [j["rec"] for j in J if j.get("kind") == "code"]
    ptrs = [j["rec"] for j in J if j.get("kind") == "pointer"]
    R.note("batch %s: %d threads disposed (%d coded), %d codes, %d pointers"
           % (nn, len(disp), sum(1 for d in disp.values() if d.get("verdict") == "coded"), len(codes), len(ptrs)))
    # B2
    rc, out = sh(["python3", "read.py", "corpus.txt", "audit"], cwd=bdir)
    try:
        aud = json.loads(out)
        over = [m for m in aud.get("mismatches", []) if m.get("kind") == "overstated"]
        if not aud.get("checked"):
            R.fail("B2", "read audit could not check anything")
        if over:
            R.fail("B2", "%d threads claim more reading than was served: %s" % (len(over), over[:4]))
        R.note("read audit: %s declared from %s, %d overstated" % (aud.get("declared"), aud.get("source"), len(over)))
    except ValueError:
        R.fail("B2", "read audit did not return JSON: %s" % out[-300:])
    # B3
    ctx = {r["id"] for r in jl(os.path.join(bdir, "coder_corpus.jsonl")) if r.get("_slice_context") and "id" in r}
    for c in codes:
        if c.get("item_id") in ctx:
            R.fail("B3", "code %s sits on a context opening %s" % (c["code_id"], c["item_id"]))
    for p in ptrs:
        if p.get("item_id") in ctx:
            R.fail("B3", "pointer %s sits on a context opening" % p.get("pointer_id"))
    # B4
    case = os.path.join(bdir, "out", "case.md")
    notes = os.path.join(bdir, "out", "notes.md")
    if not os.path.exists(case) or os.path.getsize(case) < 500:
        R.fail("B4", "out/case.md missing or under 500 bytes")
    else:
        s = open(case, encoding="utf-8").read()
        for sec in SECTIONS:
            if sec not in s:
                R.fail("B4", "case.md lacks %s" % sec)
        tags = len(re.findall(r"\[(closed|inherited|unresolved)\]", s))
        if tags == 0:
            R.fail("B4", "case.md carries no [closed]/[inherited]/[unresolved] tag")
        else:
            R.note("case.md: %d words, %d edge tags" % (len(s.split()), tags))
    if not os.path.exists(notes) or os.path.getsize(notes) < 200:
        R.fail("B4", "out/notes.md missing or under 200 bytes")
    # B5: lines added to the facts files
    for name in ("timeline.md", "lexicon.md"):
        mine = os.path.join(bdir, name)
        given = os.path.join(run, "out", name)
        if not os.path.exists(mine):
            R.fail("B5", "%s missing from the batch directory" % name); continue
        a = open(given, encoding="utf-8").read().splitlines() if os.path.exists(given) else []
        b = open(mine, encoding="utf-8").read().splitlines()
        added = [l for l in b[len(a):] if l.strip() and not l.startswith("#")]
        bad = [l for l in added if not re.search(ID_RX, l)]
        if bad:
            R.note("B5 %s: %d added lines carry no item id; lead must strike them at collection: %s" %
                   (name, len(bad), bad[:2]))
        R.note("%s: +%d lines" % (name, len(added)))
    # B6
    expected = {"AGENT.md", "CONTRACT.md", "CONTRACT-fleet-coder.md", "_manifest.json", "brief.md",
                "cite.py", "close_run.py", "coder_corpus.jsonl", "corpus.txt", "corpus_manifest.json",
                "emit.py", "lexicon.md", "out", "read.py", "timeline.md", "tools", "__pycache__",
                "coder_corpus.queries.jsonl"}
    extra = sorted(set(os.listdir(bdir)) - expected)
    if extra:
        R.note("batch directory holds extra files (not a failure): %s" % extra)
    man = json.load(open(os.path.join(bdir, "_manifest.json")))
    rc, out = sh(close_run_cmd(bdir, "fleet"), cwd=bdir)
    if "C7" in out and "FAIL C7" in out:
        R.fail("B6", "instrument files changed since dispatch (close_run C7)")
    # B7
    tr = os.path.join(bdir, "out", "_transcript.jsonl")
    if not os.path.exists(tr) or os.path.getsize(tr) == 0:
        R.note("no transcript in out/_transcript.jsonl yet: copy the agent's transcript there, or "
               "write its final message as one JSON line, before close_run can pass C2")

    # B8: enforce the journal preflight even when a coder omits its requested check.
    # Run before collection, while exports do not yet exist. Final run checks continue
    # through check_end, so consolidated historical batches are not re-preflighted.
    preflight = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coder_preflight.py")
    rc, preflight_output = sh([sys.executable, "-B", preflight], cwd=bdir)
    if rc:
        R.fail("B8", "coder preflight: " + preflight_output.strip()[-4000:])
    else:
        R.note(preflight_output.strip())


def check_end(run, R, sub):
    gate_p = os.path.join(run, "out", "_gate.json")
    gate = json.load(open(gate_p)) if os.path.exists(gate_p) else {}
    branch = gate.get("branch")
    if not branch:
        R.fail("E1", "no out/_gate.json; the lead never ran the gate"); return
    # E1
    rc, out = sh(["python3", "tools/audit_fleet.py", "--run", ".", "--sub", sub] +
                 ([] if branch == "B" else ["--branch", "A"]), cwd=run)
    if rc != 0:
        R.fail("E1", "audit_fleet: " + out.strip().splitlines()[-1][:200])
    else:
        R.note("audit_fleet PASSED")
    # E2
    rc, out = sh(close_run_cmd(run, "lead"), cwd=run)
    if not all_passed(out):
        R.fail("E2", "close_run lead: " + " | ".join(l.strip() for l in out.splitlines() if "FAIL" in l)[:300])
    if branch == "B":
        for s in gate["slices"]:
            bdir = os.path.join(run, "fleet", "batch_%s" % s["batch"])
            if not os.path.exists(os.path.join(bdir, "out")):
                R.fail("E2", "batch %s has no directory; the fleet did not finish" % s["batch"]); continue
            rc, out = sh(close_run_cmd(bdir, "fleet"), cwd=bdir)
            if not all_passed(out):
                if zero_code_fleet_compatibility(bdir, out):
                    R.note("E2 compatibility: fleet %s raw v30 C3 fails only because it requires a verdict forbidden to fleet coders; "
                           "zero codes, all threads out_of_scope, matching journal dispositions, every other close check passed. "
                           "Research outputs and copied instrument unchanged." % s["batch"])
                else:
                    R.fail("E2", "close_run fleet %s: " % s["batch"] + " | ".join(l.strip() for l in out.splitlines() if "FAIL" in l)[:300])
    R.note("close_run: lead and every batch checked")
    # E3
    if branch == "B":
        cons = gate.get("consolidated_utc")
        reads = jl(os.path.join(run, "out", "_read.jsonl"))
        finds = jl(os.path.join(run, "coder_corpus.queries.jsonl"))
        # <= : the logs are second-resolution, and a read or a search in the same second as
        # the consolidation is not after it
        early = [r for r in reads if cons and (r.get("t") or r.get("at") or "") <= cons]
        early_f = [r for r in finds if cons and (r.get("t") or r.get("at") or "") <= cons]
        if early or early_f:
            R.fail("E3", "the lead read %d times and searched %d times before consolidation (%s)"
                   % (len(early), len(early_f), cons))
        else:
            R.note("lead's reads: %d, finds: %d, all after consolidation" % (len(reads), len(finds)))
    # E4
    case = os.path.join(run, "out", "case.md")
    if not os.path.exists(case):
        R.fail("E4", "no out/case.md"); return
    s = open(case, encoding="utf-8").read()
    for sec in SECTIONS:
        if sec not in s:
            R.fail("E4", "case.md lacks %s" % sec)
    ids, threads = record_ids(os.path.join(run, "coder_corpus.jsonl"))
    cited = set(ID_RE.findall(s))
    unknown = sorted(i for i in cited if i not in ids and i not in threads)
    if unknown:
        R.fail("E4", "%d backticked ids in case.md are in no record: %s" % (len(unknown), unknown[:8]))
    if branch == "B" and len(gate.get("slices", [])) > 1 and "[crosses" not in s:
        R.note("case.md marks no relation [crosses NN|MM]; the lead should say why in notes.md")
    R.note("case.md: %d words, %d ids cited, %d unknown" % (len(s.split()), len(cited), len(unknown)))
    # E5
    notes = os.path.join(run, "out", "notes.md")
    if not os.path.exists(notes):
        R.fail("E5", "no out/notes.md")
    elif branch == "B":
        n = open(notes, encoding="utf-8").read()
        if "threshold" not in n.lower() or "branch b" not in n.lower():
            R.fail("E5", "notes.md does not repeat the gate (branch B, threshold, the counts)")
        lp = os.path.join(run, "out", "ledger.md")
        if not os.path.exists(lp):
            R.fail("E5", "no out/ledger.md; collect did not run on this instrument")
        else:
            lg = open(lp, encoding="utf-8").read()
            n_entries = lg.count("\n## batch ")
            if n_entries < len(gate.get("slices", [])):
                R.fail("E5", "ledger.md has %d entries for %d slices" % (n_entries, len(gate["slices"])))
            else:
                R.note("ledger.md: %d entries" % n_entries)
    # E6: hours written as H<n> beside a thread id on the same line
    ti_p = os.path.join(run, "package", "tree_index.json")
    if os.path.exists(ti_p):
        OPEN = 1490976000
        ti = json.load(open(ti_p))
        hours = {}
        for sub_, d in ti.items():
            for tid, nodes in (d.get("index") or {}).items():
                root = nodes.get("0") if isinstance(nodes, dict) else None
                if root and root.get("created_utc"):
                    hours[tid] = (root["created_utc"] - OPEN) / 3600.0
        suspects = []
        for m in re.finditer(r"`(6[0-9a-z]{4,5})`[^`\n]{0,12}\(?H\+?(\d+(?:\.\d+)?)\)?", s):
            tid, h = m.group(1), float(m.group(2))
            if tid in hours and abs(h - hours[tid]) > 0.1:
                suspects.append((tid, h, round(hours[tid], 2)))
        if suspects:
            R.note("E6 suspect hours beside a thread id in case.md (written, record): %s; read those lines" % suspects[:6])
        else:
            R.note("hours written beside thread ids in case.md agree with the record")


BRIEF_HEADINGS = ["Vernacular", "Who talks", "Recurring formats", "Register", "Jokes with a history",
                  "Moderation and its visible traces", "The week's shape", "What I could not tell",
                  "Data problems"]

BRIEF_REVISION = "v30-brief-r1"
BRIEF_READER_VERSION = "readbrief-v30-brief-r1"
BRIEF_REFERENCE_TOKENS = 25000
BRIEF_HARD_CEILING_TOKENS = 75000
BRIEF_CEILING_MARGIN_TOKENS = 125     # reader reserves fewer than 500 response chars
PREWEEK_OPEN = 1490371200          # 2017-03-24 16:00 UTC
PREWEEK_DAYS = ["d%d" % d for d in range(7)]
REMOVED_TEXT = {"[deleted]", "[removed]"}


def _norm(t):
    t = t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", "'").replace("\u201d", "'")
    t = t.replace('"', "'").replace("\u2014", "-").replace("\u2013", "-").replace("\u2026", "...")
    return re.sub(r"\s+", " ", t).strip().lower()


def _quote_core(q):
    """A writer's quote with its own marks taken off: a leading or trailing ellipsis for a
    cut, and ' / ' for a line break."""
    q = q.replace(" / ", " ")
    q = re.sub(r"^\s*(\.\.\.|\u2026)\s*", "", q)
    q = re.sub(r"\s*(\.\.\.|\u2026)\s*$", "", q)
    return q


def _item_body(r):
    """The exact Unicode string against which read_brief reports body offsets."""
    if r.get("body") is not None:
        return r["body"]
    return (r.get("title") or "") + ("\n\n" + r["selftext"] if r.get("selftext") else "")


def _thread_of(r):
    if r.get("kind") == "post":
        return r["id"]
    link = r.get("link_id") or ""
    return link[3:] if link.startswith("t3_") else (link or "?")


def _read_records(path):
    if not os.path.exists(path):
        return []
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") if path.endswith(".gz") else op(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _actual_heading_sections(text):
    """Return Markdown ATX headings and their content, respecting heading nesting."""
    matches = list(re.finditer(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", text))
    out = {}
    for i, m in enumerate(matches):
        level = len(m.group(1))
        end = len(text)
        for nxt in matches[i + 1:]:
            if len(nxt.group(1)) <= level:
                end = nxt.start()
                break
        name = re.sub(r"[ \t]+", " ", m.group(2)).strip().lower()
        out.setdefault(name, []).append(text[m.end():end].strip())
    return out


def _substantive_markdown(s):
    words = re.findall(r"[\w]+", re.sub(r"[`*_>#~-]", " ", s), re.UNICODE)
    if len(words) < 2:
        return False
    plain = " ".join(words).lower()
    return plain not in {"none", "n a", "na", "todo", "tbd", "placeholder"}


def _all_removed_statement(text):
    low = re.sub(r"\s+", " ", text).lower()
    return bool(re.search(
        r"(?:all|every)\b.{0,80}\b(?:deleted|removed)\b|"
        r"\bno\s+(?:item\s+)?(?:body|bodies|text)\s+(?:survived|survives|is available)", low))


def _normal_with_offsets(s):
    """Collapse display whitespace while retaining each character's raw [start, end)."""
    chars, offsets = [], []
    for m in re.finditer(r"\s+|\S", s, re.UNICODE):
        token = m.group(0)
        if token.isspace():
            if chars and chars[-1] != " ":
                chars.append(" ")
                offsets.append((m.start(), m.end()))
        else:
            chars.append(token)
            offsets.append((m.start(), m.end()))
    if chars and chars[-1] == " ":
        chars.pop(); offsets.pop()
    return "".join(chars), offsets


def _merged_intervals(intervals):
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], end))
        else:
            out.append((start, end))
    return out


def _span_covered(intervals, start, end):
    return any(a <= start and b >= end for a, b in _merged_intervals(intervals))


def _citations(text):
    """The two unambiguous citation forms accepted by corrected briefs."""
    found = []
    occupied = []
    block = re.compile(r"(?m)^[ \t]*>[ \t]*(.+?)[ \t]+\(`([^`\s()]+)`\)[ \t]*$")
    for m in block.finditer(text):
        quote = m.group(1).strip()
        if quote:
            found.append((quote, m.group(2), m.start(), "block"))
            occupied.append((m.start(), m.end()))
    inline = re.compile(r'[\u201c"]([^\u201d"]+?)[\u201d"][ \t]*\(`([^`\s()]+)`\)', re.S)
    for m in inline.finditer(text):
        if any(a <= m.start() < b for a, b in occupied):
            continue
        found.append((m.group(1), m.group(2), m.start(), "inline"))
    return sorted(found, key=lambda x: x[2])


def _malformed_block_citations(text):
    accepted = re.compile(r"^[ \t]*>[ \t]*(.+?)[ \t]+\(`([^`\s()]+)`\)[ \t]*$")
    malformed = []
    for line in text.splitlines():
        if re.match(r"^[ \t]*>", line) and re.search(r"`[^`\s()]+`", line):
            if not accepted.match(line):
                malformed.append(line.strip()[:100])
    return malformed


def _raw_brief_items(bdir, R):
    rec = os.path.join(bdir, "brief_corpus.jsonl")
    if not os.path.exists(rec):
        R.fail("F3", "no brief_corpus.jsonl from which to verify read coverage")
        return {}
    try:
        rows = _read_records(rec)
    except (OSError, ValueError) as e:
        R.fail("F3", "brief_corpus.jsonl is unreadable: %s" % e)
        return {}
    items = {}
    for row in rows:
        if "id" not in row:
            continue
        iid = str(row["id"])
        if iid in items:
            R.fail("F3", "brief_corpus.jsonl repeats item id %s" % iid)
        items[iid] = row
        if _day_of(row) is None:
            R.fail("F3", "brief_corpus.jsonl item %s is outside the seven-day pre-week or lacks created_utc"
                   % iid)
    return items


def _day_of(row):
    try:
        n = int((int(row["created_utc"]) - PREWEEK_OPEN) // 86400)
    except (KeyError, TypeError, ValueError):
        return None
    return "d%d" % n if 0 <= n < 7 else None


def _reconstruct_coverage(items, reads, R, reader_version=BRIEF_READER_VERSION):
    spans = {iid: [] for iid in items}
    served_ids = set()
    substantive_text = False
    chars_served = 0
    substantive_entries = 0
    for expected_seq, entry in enumerate(reads, 1):
        if entry.get("seq") != expected_seq:
            R.fail("F3", "read log sequence is %r at entry %d" % (entry.get("seq"), expected_seq))
        if entry.get("tool") != reader_version:
            R.fail("F3", "read log entry %d has tool %r, expected %s"
                   % (expected_seq, entry.get("tool"), reader_version))
        chars = entry.get("chars", 0)
        if not isinstance(chars, int) or isinstance(chars, bool) or chars < 0:
            R.fail("F3", "read log has invalid chars value %r" % chars)
        else:
            chars_served += chars
        if entry.get("kind") not in ("item", "thread", "sample"):
            continue
        substantive_entries += 1
        item_ids = entry.get("item_ids")
        item_spans = entry.get("item_spans")
        if not isinstance(item_ids, list) or not isinstance(item_spans, list):
            R.fail("F3", "%s read lacks item_ids and item_spans receipts" % entry.get("kind"))
            continue
        span_ids = []
        for span in item_spans:
            if isinstance(span, dict) and isinstance(span.get("item_id"), str):
                if span["item_id"] not in span_ids:
                    span_ids.append(span["item_id"])
        if item_ids != span_ids:
            R.fail("F3", "%s read item_ids do not exactly describe its item_spans"
                   % entry.get("kind"))
        for iid in item_ids:
            if not isinstance(iid, str) or iid not in items:
                R.fail("F3", "%s read claims unknown item %r" % (entry.get("kind"), iid))
            else:
                served_ids.add(iid)
        for span in item_spans:
            if not isinstance(span, dict):
                R.fail("F3", "%s read has a non-object item span" % entry.get("kind")); continue
            iid, start, end = span.get("item_id"), span.get("start"), span.get("end")
            if iid not in items:
                R.fail("F3", "%s read span claims unknown item %r" % (entry.get("kind"), iid)); continue
            if iid not in item_ids:
                R.fail("F3", "%s read span for %s is absent from item_ids" % (entry.get("kind"), iid))
            body = _item_body(items[iid])
            if (not isinstance(start, int) or isinstance(start, bool) or
                    not isinstance(end, int) or isinstance(end, bool) or
                    start < 0 or end < start or end > len(body) or
                    (start == end and len(body) != 0)):
                R.fail("F3", "%s has invalid Unicode body span %r:%r for %s (%d chars)"
                       % (entry.get("kind"), start, end, iid, len(body)))
                continue
            spans[iid].append((start, end))
            if body[start:end].strip() and body[start:end].strip().lower() not in REMOVED_TEXT:
                substantive_text = True

    items_seen = {iid for iid, ivals in spans.items() if ivals}
    items_complete = {iid for iid, ivals in spans.items()
                      if ivals and _span_covered(ivals, 0, len(_item_body(items[iid])))}
    threads = {_thread_of(r) for r in items.values()}
    served_threads = {_thread_of(items[iid]) for iid in served_ids}
    by_day = {}
    for day in PREWEEK_DAYS:
        corpus = {iid for iid, row in items.items() if _day_of(row) == day}
        by_day[day] = {
            "items_in_corpus": len(corpus),
            "items_seen": len(corpus & items_seen),
            "items_complete": len(corpus & items_complete),
            "items_served": len(corpus & served_ids),
            "threads": len({_thread_of(items[iid]) for iid in corpus}),
        }
    days_with_items = [d for d in PREWEEK_DAYS if by_day[d]["items_in_corpus"]]
    days_touched = [d for d in days_with_items if by_day[d]["items_served"]]
    return {
        "items_in_corpus": len(items), "items_seen": len(items_seen),
        "items_complete": len(items_complete), "threads_in_corpus": len(threads),
        "threads_served": len(served_threads), "chars_served": chars_served,
        "tokens_read": (chars_served + 3) // 4, "days_total": 7,
        "days_with_items": days_with_items, "days_touched": len(days_touched),
        "days_unseen": [d for d in days_with_items if d not in days_touched],
        "by_day": by_day, "spans": spans, "substantive_text": substantive_text,
        "substantive_entries": substantive_entries,
    }


def _expected_receipt_coverage(out, actual, reader_version=BRIEF_READER_VERSION):
    by_day = []
    for day in PREWEEK_DAYS:
        row = actual["by_day"][day]
        by_day.append({"day": day, "items": row["items_in_corpus"],
                       "items_seen": row["items_seen"],
                       "items_complete": row["items_complete"],
                       "threads": row["threads"]})
    if actual["days_unseen"]:
        advice = "Read active days %s before going deeper." % ", ".join(actual["days_unseen"])
    else:
        advice = "All active days touched; judge whether the nine headings have enough evidence."
    return {
        "tool": reader_version,
        "corpus": os.path.abspath(os.path.join(os.path.dirname(out), "brief_corpus.txt")),
        "items_in_corpus": actual["items_in_corpus"],
        "items_seen": actual["items_seen"],
        "items_complete": actual["items_complete"],
        "threads_in_corpus": actual["threads_in_corpus"],
        "threads_served": actual["threads_served"],
        "threads_seen": actual["threads_served"],
        "threads_total": actual["threads_in_corpus"],
        "chars_served": actual["chars_served"],
        "tokens_read": actual["tokens_read"],
        "reference_tokens": BRIEF_REFERENCE_TOKENS,
        "hard_ceiling_tokens": BRIEF_HARD_CEILING_TOKENS,
        "days_total": 7,
        "days_with_items": actual["days_with_items"],
        "days_touched": actual["days_touched"],
        "days_unseen": actual["days_unseen"],
        "by_day": by_day,
        "coverage_unit": ("unique items with explicitly logged body spans; "
                          "complete items distinguished"),
        "advice": advice,
    }


def _check_evidence_receipt(out, actual, text, all_removed, R,
                            reader_version=BRIEF_READER_VERSION):
    ep = os.path.join(out, "evidence.json")
    if not os.path.exists(ep):
        R.fail("F3", "no brief/out/evidence.json; run read_brief.py brief_corpus.txt evidence")
        return
    try:
        with open(ep, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, ValueError) as e:
        R.fail("F3", "evidence.json is unreadable: %s" % e); return
    if receipt.get("version") != 1:
        R.fail("F3", "evidence.json version is %r, expected 1" % receipt.get("version"))
    coverage = receipt.get("coverage")
    if not isinstance(coverage, dict):
        R.fail("F3", "evidence.json has no coverage object"); return
    expected = _expected_receipt_coverage(out, actual, reader_version)
    missing = sorted(set(expected) - set(coverage))
    extra = sorted(set(coverage) - set(expected))
    if missing or extra:
        R.fail("F3", "evidence coverage fields differ from reader state; missing %s, unexpected %s"
               % (missing, extra))
    for key in sorted(expected):
        if key == "corpus" and isinstance(coverage.get(key), str):
            if os.path.realpath(coverage[key]) == os.path.realpath(expected[key]):
                continue
        if coverage.get(key) != expected[key]:
            R.fail("F3", "evidence coverage.%s is %r; reconstructed value is %r"
                   % (key, coverage.get(key), expected[key]))

    ceiling = expected["hard_ceiling_tokens"]
    ceiling_threshold = ceiling - BRIEF_CEILING_MARGIN_TOKENS
    if actual["days_unseen"]:
        ceiling_named = bool(re.search(r"\b(?:hard\s+)?ceiling\b", text, re.I))
        names_missing = [d for d in actual["days_unseen"]
                         if not re.search(r"(?<![\w-])%s(?!\w)" % re.escape(d), text)]
        if not (actual["tokens_read"] >= ceiling_threshold and
                ceiling_named and not names_missing):
            R.fail("F3", "active days were left unread (%s) without a truthful hard-ceiling "
                   "explanation naming every omitted day" % ", ".join(actual["days_unseen"]))
    if not actual["substantive_text"] and not all_removed:
        R.fail("F3", "the read log serves no substantive item body text")


def _check_revised_citations(text, items, spans, all_removed, R):
    cites = _citations(text)
    malformed = _malformed_block_citations(text)
    if malformed:
        R.fail("F4", "blockquote citations must end exactly with (`item_id`): %s" % malformed[:5])
    if not cites and not all_removed:
        R.fail("F4", "brief has no supported citation; use > exact quote (`item_id`) on its own "
               "line, or an inline quoted string immediately followed by (`item_id`)")
    bad = []
    for quote, iid, _, form in cites:
        row = items.get(iid)
        if row is None:
            bad.append("%s citation names unknown item %s" % (form, iid)); continue
        qnorm, _ = _normal_with_offsets(quote)
        bnorm, offsets = _normal_with_offsets(_item_body(row))
        starts, at = [], bnorm.find(qnorm) if qnorm else -1
        while at >= 0:
            starts.append(at)
            at = bnorm.find(qnorm, at + 1)
        if not starts:
            bad.append("%r is not in item %s" % (quote[:50], iid)); continue
        served = False
        for start in starts:
            raw_start = offsets[start][0]
            raw_end = offsets[start + len(qnorm) - 1][1]
            if _span_covered(spans.get(iid, []), raw_start, raw_end):
                served = True; break
        if not served:
            bad.append("%r is in item %s but its quote span was not served" % (quote[:50], iid))
    if bad:
        R.fail("F4", "%d of %d citations lack exact item-linked, served support: %s"
               % (len(bad), len(cites), bad[:5]))
    else:
        R.note("citations: %d item-linked quotes match text actually served by read_brief.py" % len(cites))
    R.note("citation receipts verify quoted support only; prose claims still require editorial review")


def _count_raw_preweek(room, R):
    raw = os.path.join(room, "record", "preweek.jsonl.gz")
    if not os.path.exists(raw):
        raw = os.path.join(room, "record", "preweek.jsonl")
    if not os.path.exists(raw):
        R.fail("F1", "harness brief cannot be checked: no record/preweek.jsonl.gz"); return None
    try:
        return sum(1 for r in _read_records(raw) if "id" in r)
    except (OSError, ValueError) as e:
        R.fail("F1", "raw pre-week record is unreadable: %s" % e); return None


def check_brief(room, R):
    bdir = os.path.join(room, "brief")
    out = os.path.join(bdir, "out")
    md = os.path.join(out, "brief.md")
    mp = os.path.join(bdir, "_manifest.json")
    if os.path.exists(mp):
        with open(mp, encoding="utf-8") as fh:
            man = json.load(fh)
    else:
        man = {}
    instrument = man.get("instrument") if man.get("instrument") in ("v30", "v31", "v32") else "v30"
    expected_revision = "%s-brief-r1" % instrument
    expected_reader = "readbrief-%s-brief-r1" % instrument
    revised = man.get("brief_revision") == expected_revision
    harness = (man.get("kind") == "harness" or
               (bool(man.get("brief")) and "harness" in str(man.get("brief"))))
    verified_harness = False
    # F1
    if not os.path.exists(md):
        R.fail("F1", "no brief/out/brief.md"); return
    with open(md, encoding="utf-8") as fh:
        text = fh.read()
    words = len(text.split())
    if harness:
        raw_count = _count_raw_preweek(room, R)
        if raw_count:
            R.fail("F1", "manifest claims a harness-written silent week, but the raw pre-week "
                   "record contains %d items" % raw_count)
        if man.get("preweek_items") != 0:
            R.fail("F1", "harness manifest preweek_items is %r, expected 0" % man.get("preweek_items"))
        if man.get("brief_revision") != expected_revision:
            R.fail("F6", "harness manifest lacks brief_revision=%r" % expected_revision)
        verified_harness = (man.get("kind") == "harness" and revised and raw_count == 0 and
                            man.get("preweek_items") == 0)
        R.note("brief written by the harness (%s): raw pre-week count %s"
               % (man.get("brief"), raw_count if raw_count is not None else "unavailable"))
        R.note("brief.md: %d words" % words)
    else:
        R.note("brief.md: %d words (length follows available evidence; no blanket floor)" % words)

    if not harness:
        if revised:
            # F2: revised briefs use real Markdown sections, including an evidence receipt in prose.
            sections = _actual_heading_sections(text)
            required = ["Evidence base"] + BRIEF_HEADINGS
            missing = [h for h in required if h.lower() not in sections]
            empty = [h for h in required if h.lower() in sections and
                     not any(_substantive_markdown(s) for s in sections[h.lower()])]
            if missing:
                R.fail("F2", "Markdown headings missing from brief.md: %s" % missing)
            if empty:
                R.fail("F2", "brief.md headings have no substantive section text: %s" % empty)
            actual_names = [re.sub(r"[ \t]+", " ", m.group(2)).strip().lower()
                            for m in re.finditer(r"(?m)^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", text)]
            required_names = {h.lower() for h in required}
            ordered_required = [h for h in actual_names if h in required_names]
            if ordered_required and ordered_required[0] != "evidence base":
                R.fail("F2", "Evidence base must precede the nine descriptive sections")
            evidence_prose = "\n\n".join(sections.get("evidence base", []))
            if evidence_prose and "(state)" not in evidence_prose.lower():
                R.fail("F2", "Evidence base must attribute its coverage figures to (state)")

            # F3: derive all coverage from raw records and served Unicode spans.
            rl = os.path.join(out, "_read.jsonl")
            try:
                reads = jl(rl)
            except (OSError, ValueError) as e:
                reads = []
                R.fail("F3", "read log is unreadable: %s" % e)
            if not reads:
                R.fail("F3", "no out/_read.jsonl: the writer did not read through read_brief.py")
            elif reads[0].get("kind") != "header":
                R.fail("F3", "the writer's first read was %r, not header" % reads[0].get("kind"))
            items = _raw_brief_items(bdir, R)
            if man.get("preweek_items") != len(items):
                R.fail("F6", "manifest preweek_items is %r; raw brief corpus contains %d"
                       % (man.get("preweek_items"), len(items)))
            if "preweek_threads" in man:
                raw_threads = len({_thread_of(row) for row in items.values()})
                if man.get("preweek_threads") != raw_threads:
                    R.fail("F6", "manifest preweek_threads is %r; raw brief corpus contains %d"
                           % (man.get("preweek_threads"), raw_threads))
            actual = _reconstruct_coverage(items, reads, R, expected_reader)
            all_removed = bool(items) and not any(
                _item_body(r).strip() and _item_body(r).strip().lower() not in REMOVED_TEXT
                for r in items.values())
            explicit_removed = all_removed and _all_removed_statement(text)
            if all_removed and not explicit_removed:
                R.fail("F4", "all item bodies are deleted/removed, but brief.md does not state that exception")
            if actual["substantive_entries"] == 0:
                R.fail("F3", "read log contains only metadata/header operations and no item, thread, or sample read")
            _check_evidence_receipt(out, actual, evidence_prose, explicit_removed, R,
                                    expected_reader)
            _check_revised_citations(text, items, actual["spans"], explicit_removed, R)
            kinds = {}
            for entry in reads:
                kinds[entry.get("kind")] = kinds.get(entry.get("kind"), 0) + 1
            R.note("read log: %s; %d of %d active days touched; %d of %d item bodies seen"
                   % (", ".join("%s x%d" % kv for kv in sorted(kinds.items())),
                      actual["days_touched"], len(actual["days_with_items"]),
                      actual["items_seen"], actual["items_in_corpus"]))
        else:
            # Compatibility path for imported briefs written before v30-brief-r1.
            low = text.lower()
            missing = [h for h in BRIEF_HEADINGS if h.lower() not in low]
            if missing:
                R.fail("F2", "headings missing from brief.md: %s" % missing)
            rl = os.path.join(out, "_read.jsonl")
            if not os.path.exists(rl):
                rl = os.path.join(out, "_read_brief.jsonl")
            reads = jl(rl)
            if not reads:
                R.fail("F3", "no read log in brief/out: the writer did not read through read_brief.py")
            else:
                if reads[0].get("kind") != "header":
                    R.fail("F3", "the writer's first read was %r, not header" % reads[0].get("kind"))
                kinds = {}
                for entry in reads:
                    kinds[entry.get("kind")] = kinds.get(entry.get("kind"), 0) + 1
                R.note("legacy read log: %s" % ", ".join(
                    "%s x%d" % kv for kv in sorted(kinds.items())))

            rec = os.path.join(bdir, "brief_corpus.jsonl")
            bodies = {}
            for row in jl(rec):
                if "id" in row:
                    bodies[row["id"]] = _norm(_item_body(row))
            allbodies = "\n".join(bodies.values())
            bad, n_q = [], 0
            quotes = []
            for para in re.split(r"\n\s*\n", text):
                for m in re.finditer(r"\u201c([^\u201d]{20,}?)\u201d", para):
                    quotes.append((m.group(1), para[m.end():m.end() + 24]))
                parts = para.split('"')
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts) and len(parts[i]) >= 20:
                        quotes.append((parts[i], parts[i + 1][:24]))
            for qraw, tail in quotes:
                q = _norm(_quote_core(qraw)); n_q += 1
                if len(q) < 20:
                    continue
                idm = re.search(r"`(6[0-9a-z]{4,5}|d[fg][0-9a-z]{4,5})`", tail)
                if idm and idm.group(1) in bodies and q in bodies[idm.group(1)]:
                    continue
                if q in allbodies:
                    continue
                bad.append("%r (%s)" % (qraw[:50], idm.group(1) if idm else "any item"))
            if bad and len(bad) > max(1, n_q // 10):
                R.fail("F4", "%d of %d legacy quotes are not in the pre-week record verbatim: %s"
                       % (len(bad), n_q, bad[:5]))
            elif bad:
                R.note("F4 legacy quotes: %d of %d found verbatim; not found: %s"
                       % (n_q - len(bad), n_q, bad[:5]))
            else:
                R.note("legacy quotes: %d of %d found verbatim in the record" % (n_q, n_q))
    # F5
    tp = os.path.join(out, "_transcript.jsonl")
    if verified_harness:
        R.note("no transcript required: revised harness was independently verified raw-zero")
    elif not (os.path.exists(tp) and os.path.getsize(tp) > 0):
        R.fail("F5", "no transcript in brief/out (_transcript.jsonl); place the session's transcript")
    # F6
    if not man:
        R.fail("F6", "no brief/_manifest.json")
    else:
        import hashlib
        drift = []
        hashes = man.get("sha256") or {}
        if (revised or harness) and not hashes:
            R.fail("F6", "corrected brief manifest has no sha256 integrity entries")
        if revised and not harness:
            required_hashes = {"read_brief.py", "cite.py", "CONTRACT.md",
                               "brief_corpus.txt", "brief_corpus.jsonl"}
            missing_hashes = sorted(required_hashes - set(hashes))
            if missing_hashes:
                R.fail("F6", "corrected brief manifest lacks integrity entries: %s" % missing_hashes)
        if harness and "out/brief.md" not in hashes:
            R.fail("F6", "harness manifest does not protect out/brief.md")
        for name, want in hashes.items():
            fp = os.path.join(bdir, name)
            if not os.path.exists(fp):
                drift.append("%s: gone" % name)
            else:
                with open(fp, "rb") as fh:
                    got = hashlib.sha256(fh.read()).hexdigest()
                if got != want:
                    drift.append("%s: changed" % name)
        if drift:
            R.fail("F6", "brief files changed since the corpus was built: %s" % drift)
        R.note("brief written by model %s on instrument %s" % (man.get("model"), man.get("instrument")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", default=".")
    ap.add_argument("--batch")
    ap.add_argument("--fork")
    ap.add_argument("--brief", action="store_true", help="check the brief stage instead of the run")
    a = ap.parse_args()
    room = os.path.abspath(a.room)
    R = Report()
    if a.brief:
        check_brief(room, R)
        return R.done()
    run = os.path.join(room, "forks", a.fork, "run") if a.fork else os.path.join(room, "run")
    if not os.path.exists(os.path.join(run, "_manifest.json")):
        print("FAILED: no run at %s" % run); return 1
    sub = json.load(open(os.path.join(run, "_manifest.json"))).get("sub")
    if a.batch:
        check_batch(run, "%02d" % int(a.batch), R)
    else:
        check_end(run, R, sub)
    return R.done()


if __name__ == "__main__":
    sys.exit(main())
