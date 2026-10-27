"""checks/stage_E1.py: the close-check of stage E1, the audit, v38.

Written from stages/STAGE-E1-formalizing-audit.md (its Outputs block, sections 1 to 9, its Close
section), from SCHEMA-adaptations.md section 8 (the reconstruction), from the docstrings of
tools/probe.py, tools/links.py and tools/snap.py, and from the v37 check it descends from
(_v37-source/tools/validate.py, stage18). This is the one check allowed to read _snap/, _probe/
and _transcripts/, because the stage file says the audit reads them.

The stage runs the scripts leg first, then one leg per audit section, then the reconstruction
sample's three legs, then the experience. So: notes-E1.md and audit-E1/ (with at least one
script) are required at every leg; once experience-E1.md exists, every output the stage file
names is required and the manifest's last line must name it; before that the remainder is a
warning. Every file that exists is checked whatever the leg.

What is checked:
  1. audit-E1.md: the composition diagnostics of prior.md section 3 named and their thresholds
     reported (does-not-compose, particulars, corrections met twice); the composition verdict in
     the contract's words (composed, or compiled in Kozlowski and Klein's sense); the orderings by
     snap, the departures, the forks, the coverage, the manifest, the moves, the transcript, the
     load-bearing test, the unplaced, all present by name; every figure said to be self-reported
     in that word; the licence sentence where fidelity appears (rule 17); intra-rater never
     written; the analysed set's count stated; every element, arrow, theme and branch id resolving;
     every quoted passage with a citation resolving to a participant's words in the store; the
     methods paragraph last, with the four departures (the tier split, no overlap, the census,
     the in-sample return), the canvas, the archive.
  2. audit-E1/: at least one script, each with an output beside it (warning where none).
  3. The orderings proved by snaps: every D4 cut snap precedes projections-D4.jsonl and the
     chunk-share tree (no cut snap lists either); branches.jsonl as it stands is what the last
     cut snap hashed; a stage-C5 snap exists listing model/elements.jsonl; a stage-B2 snap lists
     the scheme; package/sealed.jsonl's hashes hold. What moved after a snap is what the audit
     must say, so a movement is printed, not an error, except at D4.
  4. probes-E1.md: every _probe/NN-L.answers.md has its NN-L.json score (probe.py --score ran over
     every answer file); the file reports failures per stage, naming each stage that has probes.
  5. links.py runs clean over the head, the questions and the views.
  6. reconstruction-E1.jsonl: one line per sampled room, sub in the analysed set, branch in
     branches.jsonl, verdict one of the four, a fidelity in [0, 1]; every sampled room named in
     notes-E1.md; the sample size against thirty. The stage file gives no fields beyond these, so
     nothing more is checked.
  7. expectations-E1.md: the replication score by branch and by verdict, and stage D5's survival
     figures beside it. The counts rule: stage D4 section 4's four counts sum to n_analysed.
  8. experience-E1.md: eleven sections, cited to files and the diary; its length (warning);
     handback-E1.md not short (warning); run_manifest.json's last entry names experience-E1.md,
     its hash and the model.
  9. The ledgers the audit reads whole exist (departures, defects, findings, tier_history,
     run_manifest); _transcripts/INDEX.md (warning); fork_comparison files present or absent
     (printed); the diary covers the stages (warning).

Not carried from v37 stage18:
  - _snap/D5-names, 17-names, 17-activation, 16-cut and cluster_report-16: the naming snap and the
    two clusterings are gone; the D4 cut snaps are per cut and harness-owned.
  - objections.jsonl among the ledgers: no such file in v38.
  - diary-*.md counted to eighteen: the v38 diary is out/diary/NN-k.jsonl, counted by stage.
  - EXPERIENCE.md: renamed experience-E1.md; audit.md: audit-E1.md; handback-18: handback-E1.
  - the word "chronology" (check_chronology.py): no v38 tool; the clocks are done by hand and
    logged, checked here only as the word "clocks".
"""
import collections, glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlib
from vlib import err, warn, jsonl, text, need
from checks import stage_D4 as s11
from checks import stage_D5 as s12

FINAL = ("audit-E1.md", "reconstruction-E1.jsonl", "expectations-E1.md", "probes-E1.md",
         "experience-E1.md", "handback-E1.md")
AUDIT_WORDS = (
    ("snap", "the orderings are verified from the snaps (section 1)"),
    ("self-reported", "every other claim about the order of work is self-reported, in that word"),
    ("departure", "every departure is reported with what following the provision would have cost"),
    ("fork", "the forks are reported from the two comparison files, or their absence"),
    ("coverage", "rooms read whole, by stage and in total, from the read logs"),
    ("manifest", "run_manifest.json names the model, seed and decoding behind every figure"),
    ("clocks", "the coder's hour against the item's own time, done by hand and logged"),
    ("transcript", "the diary against the transcript for legs drawn by seed"),
    ("load-bearing", "which stage was load-bearing (section 6)"),
    ("unplaced", "the unplaced, read and not only counted"),
    ("cite.py", "every quote resolves through cite.py --resolve"),
    ("links.py", "every id in the head, the questions and the views resolves through links.py"),
    ("kozlowski", "the stated level and composition or compilation claim in Kozlowski and Klein's terms"),
    ("claims-e1.md", "every proposition and branch against the kind of claim it declares and the kind of validation "
                     "it received, in claims-E1.md (section 1)"),
)
SHARES = (("does-not-compose", r"does-not-compose"),
          ("particulars", r"particular"),
          ("corrections met twice", r"met twice"))
QUOTE_PAT = re.compile(r"[\"“]([^\"”]{6,300})[\"”]\s*\[([A-Za-z0-9_]+)/(c\d{3,5})\]")
ID_PAT = re.compile(r"\b(T3-\d{3}|T4-\d{2,3}|[PKCR]\d{2}|A\d{2}|F-\d{3}|FP-\d{2,3}|N\d{2,3}|[FG]\d{2,3})\b")
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10, "twelve": 12, "fifteen": 15, "twenty": 20}


# ---- helpers vlib lacks ------------------------------------------------------------------------

def prior_shares(outdir):
    """prior.md section 3's three thresholds as written (the number or the word), or None each."""
    t = text(outdir, "prior.md")
    if not t:
        return None
    sec = re.search(r"##\s*3\.(.*?)(?=\n##\s*\d|\Z)", t, re.S)
    body = sec.group(1) if sec else t
    out = {}
    for key, pat in (("does-not-compose", r"does-not-compose[^\n]*?([\d.]+|[a-z]+)\s*per cent"),
                     ("particulars", r"particular[^\n]*?([\d.]+|[a-z]+)\s*per cent"),
                     ):
        m = re.search(pat, body, re.I)
        out[key] = m.group(1) if m else None
    return out


def snap_files(outdir, stage):
    """_snap/NN-*.sha256 for a stage, oldest first by the header's time (else by name)."""
    out = []
    for p in glob.glob(os.path.join(outdir, "_snap", "%s-*.sha256" % stage)):
        t = ""
        with open(p, encoding="utf-8") as f:
            first = f.readline()
        m = re.search(r" at (\S+)", first)
        if m:
            t = m.group(1)
        out.append((t, os.path.basename(p)))
    return [b for _t, b in sorted(out)]


def snap_lists(outdir, snap_name):
    """{file: hash} for a snap."""
    got = {}
    for line in open(os.path.join(outdir, "_snap", snap_name), encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.rstrip("\n").split("  ", 3)
        if len(parts) == 4:
            got[parts[3]] = parts[0]
    return got


def check_quote_shares(root, au):
    """The handler's quote check (check_quotes.py) arrives as quote-check-E1.json in the analyst's folder; audit-E1.md
    reports both shares as the file gives them (section 1, audit 2026-09-29b)."""
    p = os.path.join(root, "quote-check-E1.json")
    if not os.path.exists(p):
        warn("quote-check-E1.json is not in the folder: the handler runs check_quotes.py before E1 opens (the E1 card); "
             "say in audit-E1.md that it did not arrive")
        return
    try:
        q = json.load(open(p, encoding="utf-8"))
    except ValueError:
        err("quote-check-E1.json does not parse; the handler reruns check_quotes.py", shape="quotes:parse")
        return
    for k in ("code_quote_found_share", "case_quote_found_share"):
        v = q.get(k)
        if not isinstance(v, (int, float)):
            continue
        forms = {"%.4f" % v, "%.3f" % v, "%.2f" % v, "%.1f%%" % (100 * v), "%.0f%%" % (100 * v), "%.1f per cent" % (100 * v)}
        if not any(f in au for f in forms):
            err("audit-E1.md does not report %s from quote-check-E1.json (%s): report both shares (section 1)"
                % (k, v), shape="quotes:share", where=k)


def check_audit(outdir, root, ctx, by_id):
    au = text(outdir, "audit-E1.md")
    if not au:
        return
    check_quote_shares(root, au)
    low = au.lower()
    for word, why in AUDIT_WORDS:
        if word not in low:
            err("audit-E1.md does not mention %s; %s" % (word, why))
    if not re.search(r"^composition_status:\s*(supported|unsupported|unresolved)\s*$", au, re.M):
        err("audit-E1.md gives no composition verdict: write composition_status: supported | unsupported | unresolved, with evidence and scope")
    # the composition diagnostics
    ps = prior_shares(outdir)
    if ps is None:
        err("prior.md is not in the output directory; composition criteria are recorded there and the "
            "audit recomputes each against it")
    for label, pat in SHARES:
        if not re.search(pat, low):
            err("audit-E1.md does not report the composition diagnostic %r against prior.md section 3 (section 3: "
                "rooms does-not-compose, adaptation lines that are particulars, corrections met twice)" % label)
        elif ps:
            thr = ps.get({"does-not-compose": "does-not-compose", "particulars": "particulars",
                          "corrections met twice": "met twice"}[label])
            if thr:
                forms = {thr, thr.lower()}
                if thr.lower() in NUMWORDS:
                    forms.add(str(NUMWORDS[thr.lower()]))
                elif thr.isdigit() and int(thr) in NUMWORDS.values():
                    forms |= {w for w, n in NUMWORDS.items() if n == int(thr)}
                if not any(re.search(r"(?<![\d.])%s(?![\d])" % re.escape(f), low) for f in forms):
                    err("audit-E1.md does not restate prior.md's threshold %s for %r; the pre-registered number is "
                        "reported beside the recomputed share" % (thr, label))
    if not re.search(r"per cent|%", low):
        err("audit-E1.md reports no share as a percentage; the three shares are recomputed from verdicts-D.jsonl "
            "and adjudications.jsonl")
    # rule 17 where fidelity appears; the names that are banned
    if re.search(r"fidelity|transmission", low):
        vlib.licence_sentence(outdir, "audit-E1.md", "fidelity or transmission figures")
    if re.search(r"intra-?rater", low):
        err("audit-E1.md calls a figure intra-rater; readers in fresh contexts are instances of one model, not "
            "two minds, and none of the figures is reliability (section 1)")
    elif "reliability" in low:
        warn("audit-E1.md uses the word reliability; FLEET.md section 2 says none of the figures is called that")
    # the counts rule: the census stated, the analysed set's count
    fc = s11.four_counts(outdir, root, ctx, stage="E1")
    if fc is not None:
        analysed, in_branch, unad, rest, unret = fc
        n = len(analysed)
        print("  stage D4 section 4 recomputed: %d + %d + %d + %d = %d, analysed %d"
              % (len(in_branch), len(unad), len(rest), len(unret), len(in_branch | unad | rest | unret), n))
        if not re.search(r"(?<![\d.])%d(?![\d])" % n, au):
            err("audit-E1.md never states %d, the analysed set's count; the census is stated twice and stage D4 "
                "section 4's four counts sum to n_analysed (the counts rule, section 1)" % n)
    # the methods paragraph, last
    heads = [(m.start(), m.group(0)) for m in re.finditer(r"^#+ .*$", au, re.M)]
    mh = [(p, h) for p, h in heads if "method" in h.lower()]
    if not mh:
        err("audit-E1.md has no methods paragraph heading; it is the last section, written for the paper "
            "(section 8)")
    else:
        if mh[-1][0] != heads[-1][0]:
            err("audit-E1.md: the methods paragraph is not its last section (section 8)")
        mp = au[mh[-1][0]:].lower()
        for word, why in (("census", "the census in place of sampling"),
                          ("in-sample", "the in-sample return, with the tier named"),
                          ("overlap", "no overlap between the coders' collection and the analysis"),
                          ("coder", "the tier split between coders and analyst"),
                          ("canvas", "what the canvas is and is not"),
                          ("archiv", "everything is archived with no promise that a rerun reproduces it")):
            if word not in mp:
                err("audit-E1.md's methods paragraph does not state %s (section 8: the four departures, the "
                    "canvas, the archive)" % why)
    # ids and quotes
    el, ar = s11.elements(outdir)
    scheme, _ = vlib.load_scheme(outdir)
    fourth = s11.fourth_ids(outdir)
    # F01 is a branch (or G01 a family), F-001 a finding, N01 a proposition; FP- lives in form_pass-C1.md prose
    findings = {r.get("id") for r in (jsonl(os.path.join(outdir, "findings.jsonl")) or []) if r.get("id")}
    props = {r.get("id") for r in (jsonl(os.path.join(outdir, "propositions.jsonl")) or []) if r.get("id")}
    for x in sorted(set(ID_PAT.findall(au))):
        pool = {"T3": scheme, "T4": fourth, "A": ar}.get(x[:2] if x.startswith("T") else x[0])
        if x[0] in "PKCR":
            pool = el
        elif x.startswith("FP-"):
            pool = None
        elif x.startswith("F-"):
            pool = findings
        elif x[0] == "N":
            pool = props
        elif x[0] in "FG":
            pool = set(by_id)
        if pool is not None and x not in pool:
            err("audit-E1.md names %s, which resolves to nothing (the model, the scheme, the fourth-order "
                "themes, the branches)" % x, shape="audit-E1.md: id unresolved", where=x)
    quotes = [q for q, _s, _c in QUOTE_PAT.findall(au)]
    if quotes:
        vlib.cites_resolve(outdir, root, quotes, "audit-E1.md")
    codes = vlib.store_codes(ctx)
    for _q, sub, cid in QUOTE_PAT.findall(au):
        if (sub, cid) not in codes:
            err("audit-E1.md cites [%s/%s], which is not a concept in the store" % (sub, cid),
                shape="audit-E1.md: citation unresolved", where="%s/%s" % (sub, cid))


def check_scripts(outdir):
    d = os.path.join(outdir, "audit-E1")
    if not os.path.isdir(d):
        err("audit-E1/ was not written; every script goes there with its output, so that a stranger can rerun it")
        return
    files = sorted(os.listdir(d))
    scripts = [f for f in files if f.endswith(".py") or f.endswith(".sh")]
    if not scripts:
        err("audit-E1/ holds no script; the audit's figures are computed by scripts declared in the stage file, "
            "not chosen by what fits")
    for s in scripts:
        stem = os.path.splitext(s)[0]
        if not any(f != s and os.path.splitext(f)[0] == stem for f in files):
            warn("audit-E1/%s has no output beside it (same stem, another extension); a script travels with "
                 "its output" % s)


def check_orderings(outdir, ctx, by_id):
    cuts = snap_files(outdir, "D4")
    # a move's snap (snap.py D4 move-<move>-<n>) or a named cut's snap (done.sh D4 --cut) both count
    cuts = [c for c in cuts if "-cut-" in c or c.startswith("D4-move-")]
    if by_id and not cuts:
        err("_snap/ holds no D4 move or cut snap and branches.jsonl declares %d branches; every move is snapped "
            "(snap.py D4 move-<move>-<n>) before anything is projected, and the snap line is the record" % len(by_id))
    prev_branches = None
    for c in cuts:
        listed = snap_lists(outdir, c)
        # J, 27 Oct 2026 18:45 Berlin (QE1-001): a snap is a branch cut only where it changed branches.jsonl
        # from the previous snap; a snap that leaves the branches as they were (the room forms, D4a-05 to
        # D4a-08) is printed as a finding, not an error.
        b = listed.get("branches.jsonl")
        is_branch_cut = b is not None and b != prev_branches
        if b is not None:
            prev_branches = b
        for f in ("projections-D4.jsonl", "chunk-share-D4.jsonl", "chunk-share-D4.md"):
            if f in listed and not is_branch_cut:
                print("  finding: _snap/%s lists %s, with branches.jsonl as at the previous snap: not a branch cut "
                      "(the room forms after the projection, by J's ruling; QE1-001)" % (c, f))
                continue
            if f in listed:
                err("_snap/%s lists %s: the projection or the comparison existed before this cut was snapped; the "
                    "cut was made with the verdicts or the canvas in view (stage D4 section 6), and the audit "
                    "names it as a defect" % (c, f), shape="D4 cut snapped after the projection", where=c)
    if cuts:
        vlib.snap_matches(outdir, cuts[-1], "branches.jsonl", "E1",
                          "every cut having been snapped before the projection; a cut after the last snap is unrecorded")
    for stage, fname, what in (("C5", "model/elements.jsonl", "the model hashed at C5's close before D1"),
                               ("B2", None, "the scheme frozen before B3's first batch")):
        snaps = snap_files(outdir, stage)
        if not snaps:
            err("_snap/ holds no stage-%s snap; %s is proved by that snap and by nothing else" % (stage, what))
            continue
        listed = snap_lists(outdir, snaps[-1])
        names = [fname] if fname else [n for n in listed if n.startswith("scheme")]
        if not names or not all(n in listed for n in names):
            err("_snap/%s does not list %s; %s cannot be proved from it" % (snaps[-1], fname or "a scheme file", what))
            continue
        for n in names:
            p = os.path.join(outdir, n)
            state = "gone" if not os.path.exists(p) else ("unchanged" if vlib.sha(p) == listed[n] else "moved after the snap")
            print("  ordering: %s, %s in _snap/%s: %s" % (what, n, snaps[-1], state))
    sealed = jsonl(os.path.join(ctx["package"], "sealed.jsonl")) or []
    for srow in sealed:
        f = srow.get("file")
        if not f:
            continue
        for q in (os.path.join(ctx["root"], f), os.path.join(outdir, f), os.path.join(ctx["package"], f)):
            if os.path.exists(q):
                if vlib.sha(q) != srow.get("sha256"):
                    err("%s does not match its hash in package/sealed.jsonl; prior.md and the sealed files are "
                        "amended only by a logged departure" % f)
                break


def check_probes(outdir):
    pd = os.path.join(outdir, "_probe")
    answers = sorted(glob.glob(os.path.join(pd, "*.answers.md")))
    stages = set()
    for a in answers:
        base = a[:-len(".answers.md")]
        stages.add(os.path.basename(base).split("-")[0])
        if not os.path.exists(base + ".json"):
            err("_probe/%s has no score file %s.json; probes-E1.md is probe.py NN --leg L --score over every "
                "answer file" % (os.path.basename(a), os.path.basename(base)),
                shape="probe answers unscored", where=os.path.basename(a))
    pm = text(outdir, "probes-E1.md")
    if not pm:
        return
    low = pm.lower()
    if not re.search(r"per stage|by stage|per question|by question", low):
        err("probes-E1.md does not report recall failures per stage and per question")
    for s in sorted(stages):
        if not re.search(r"(?<![\w-])%s(?![\d])" % re.escape(s), pm):
            err("probes-E1.md does not report stage %s, which has probe answers in _probe/" % s,
                shape="probes-E1.md: stage missing", where=s)
    if not answers:
        warn("_probe/ holds no answer file; the recall probe ran at no close, and probes-E1.md can only say so")


def check_links(root, outdir):
    tools = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lp = os.path.join(tools, "links.py")
    if not os.path.exists(lp):
        err("tools/links.py is not beside validate.py; every id in the head, the questions and the views is "
            "resolved through it")
        return
    r = subprocess.run([sys.executable, lp, "--root", root, "--out", outdir], capture_output=True, text=True)
    if r.returncode:
        err("links.py finds ids that do not resolve: %s" % (r.stdout.strip().splitlines() or ["?"])[0][:160])


def check_reconstruction(outdir, ctx, by_id):
    # The stage file names sub, branch, verdict and the fidelity score; nothing more is fixed, so
    # only those are checked.
    rows = jsonl(os.path.join(outdir, "reconstruction-E1.jsonl"))
    if rows is None:
        return
    got = vlib.analysed_set("E1", "the reconstruction sample against the analysed set", outdir, ctx)
    analysed = got[0] if got else None
    notes = text(outdir, "notes-E1.md")
    subs = []
    for i, r in enumerate(rows, 1):
        sub = r.get("sub")
        subs.append(sub)
        if analysed is not None and sub not in analysed:
            err("reconstruction-E1.jsonl line %d: sub %r is not in the analysed set" % (i, sub),
                shape="reconstruction-E1.jsonl: sub outside the analysed set", where=str(sub))
        if r.get("branch") not in by_id and r.get("branch") not in (None, "none", "unadapted"):
            err("reconstruction-E1.jsonl %s: branch %r is not in branches.jsonl; fidelity is reported by branch"
                % (sub, r.get("branch")), shape="reconstruction-E1.jsonl: branch unresolved", where=str(sub))
        if r.get("verdict") not in vlib.VERDICTS:
            err("reconstruction-E1.jsonl %s: verdict %r is not one of the four; fidelity is reported by verdict"
                % (sub, r.get("verdict")), shape="reconstruction-E1.jsonl: verdict outside the four", where=str(sub))
        fid = r.get("fidelity", r.get("score"))
        if not isinstance(fid, (int, float)) or not 0 <= fid <= 1:
            err("reconstruction-E1.jsonl %s: fidelity %r is not a share in [0, 1] (claims the skeleton accounts "
                "for, over the case's claims)" % (sub, fid), shape="reconstruction-E1.jsonl: fidelity", where=str(sub))
        if sub and notes and not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(str(sub)), notes):
            err("reconstruction-E1.jsonl samples %s, which notes-E1.md does not name; the thirty are named before "
                "any is opened (section 4)" % sub, shape="reconstruction-E1.jsonl: sampled room not named", where=str(sub))
    dup = [s for s, n in collections.Counter(subs).items() if n > 1]
    if dup:
        err("reconstruction-E1.jsonl holds two lines for %s" % dup[:5])
    if analysed is not None:
        want = min(30, len(analysed))
        if len(rows) != want:
            warn("reconstruction-E1.jsonl holds %d rooms; the sample is thirty by seed (or the whole analysed set "
                 "below thirty), stratified by branch and by verdict" % len(rows))
    if not notes:
        err("notes-E1.md was not written; the sample is named there before any room is opened")


def check_expectations(outdir):
    t = text(outdir, "expectations-E1.md")
    if not t:
        return
    low = t.lower()
    for word, why in (("replication score", "the score by branch and by verdict is the replication score"),
                      ("by branch", "the score by branch"),
                      ("by verdict", "the score by verdict"),
                      ("in-sample", "all tiers use the same corpus; uncited material is an additional in-sample check"),
                      ("survival", "stage D5's survival figures per branch beside it, from the record")):
        if word not in low:
            err("expectations-E1.md does not report %s (section 3)" % why)
    field = [r.get("id") for r in (jsonl(os.path.join(outdir, "sealed", "FIELD.jsonl")) or []) if r.get("id")]
    if field:
        m = re.search(r"^#+\s*The field's entries\s*$(.*?)(?=^#|\Z)", t, re.M | re.S | re.I)
        if not m:
            err("expectations-E1.md has no heading `The field's entries` for the %d tentative entries (section 3)"
                % len(field), shape="field:section")
        else:
            missing = [i for i in field if not re.search(r"\b%s\b" % re.escape(i), m.group(1))]
            if missing:
                err("expectations-E1.md, The field's entries, does not report %s" % ", ".join(missing[:5]),
                    shape="field:unreported")
            if "other" not in m.group(1).lower():
                err("expectations-E1.md, The field's entries, sets no share beside the model's other elements; "
                    "that comparison shows whether the tentative mark drew answers (section 3)", shape="field:beside")
    if not os.path.exists(os.path.join(outdir, "sealed", "EXPECTATIONS.jsonl")):
        warn("sealed/EXPECTATIONS.jsonl is absent; expectations-E1.md is EXPECTATIONS.jsonl against the ledger "
             "and the verdicts")


def check_experience_and_manifest(outdir):
    ex = text(outdir, "experience-E1.md")
    if ex:
        heads = re.findall(r"^#{1,3} .+$", ex, re.M)
        if len(heads) < 11:
            err("experience-E1.md has %d headings; eleven sections, in the stage file's order (section 9)" % len(heads))
        if "diary" not in ex.lower():
            warn("experience-E1.md never cites the diary; it is cited to files and diary entries")
        if len(ex.split()) < 1500:
            warn("experience-E1.md is %d words; it is written from every stage's diary and handback and is not short"
                 % len(ex.split()))
        ents = vlib.manifest_entry(outdir, "E1", "experience-E1.md")
        if ents:
            last = ents[-1]
            blob = json.dumps(last)
            if "experience-E1.md" not in blob:
                err("run_manifest.json's stage-E1 entry does not name experience-E1.md; the last line names it, "
                    "its hash and the model that wrote it")
            else:
                want = vlib.sha(os.path.join(outdir, "experience-E1.md"))
                if want not in blob:
                    err("run_manifest.json's stage-E1 entry does not carry experience-E1.md's sha256 as it stands "
                        "(%s); rehash after the last edit" % want[:12])
                if not last.get("model"):
                    err("run_manifest.json's stage-E1 entry names no model")
    hb = text(outdir, "handback-E1.md")
    if hb and len(hb.split()) < 800:
        warn("handback-E1.md is %d words; it is not short, since anything not written down goes there or nowhere"
             % len(hb.split()))


def check_ledgers(outdir, root):
    for f in ("departures.jsonl", "defects.jsonl", "findings.jsonl", "run_manifest.json", "tier_history.jsonl"):
        if not os.path.exists(os.path.join(outdir, f)):
            err("%s is not in the output directory; the audit reads it whole (section 2)" % f)
    if not os.path.exists(os.path.join(outdir, "_transcripts", "INDEX.md")):
        warn("_transcripts/INDEX.md is absent; the diary against the transcript needs the transcripts the operator "
             "places there")
    for fc in ("fork_comparison-C2.json", "fork_comparison-D.json"):
        present = os.path.exists(os.path.join(root, fc)) or os.path.exists(os.path.join(outdir, fc))
        print("  %s: %s" % (fc, "present" if present else "absent (no fork, or not shipped)"))
    stages = set()
    for p in glob.glob(os.path.join(outdir, "diary", "*.jsonl")):
        for r in jsonl(p) or []:
            if r.get("stage"):
                stages.add(str(r["stage"]))
    if len(stages) < 17:          # every stage before E1 (18 stages; E2 follows)
        warn("the diary holds lines for %d stages; the experience is written from every stage's diary" % len(stages))


def check(root, outdir, ctx):
    need(outdir, "notes-E1.md")
    vlib.model_moved(outdir, "D3", "E1")
    vlib.tree_moved(outdir)
    if not vlib.frozen_hash(outdir, "D3"):
        err("E1 requires the validated D3 model closure hash", shape="model:unfrozen")
    by_id = {b["id"]: b for b in s11.branches(outdir) if b.get("id")}
    final = os.path.exists(os.path.join(outdir, "experience-E1.md"))
    if final:
        need(outdir, *FINAL)
    else:
        missing = [n for n in FINAL if not os.path.exists(os.path.join(outdir, n))]
        if missing:
            warn("stage E1 outputs not written yet: %s; the experience is written last, and the stage does not "
                 "close without every one" % ", ".join(missing))
    check_scripts(outdir)
    check_audit(outdir, root, ctx, by_id)
    check_orderings(outdir, ctx, by_id)
    check_probes(outdir)
    check_links(root, outdir)
    check_reconstruction(outdir, ctx, by_id)
    check_expectations(outdir)
    check_experience_and_manifest(outdir)
    check_ledgers(outdir, root)
    # the diary's lines for the stage are checked by validate.py's common checks (rule 20)


# ---- the planted fixture ----------------------------------------------------------------------

AUDIT = """# audit-E1

composition_status: supported

## 1. Scripts over the record
Every quote resolved through cite.py --resolve; every id through links.py. The snap of each D4 cut precedes
projections-D4.jsonl; the scheme snap at B2 holds; every other ordering is self-reported. Coverage: 3 rooms read
whole. The clocks agree on 2 of 3 concepts. The manifest names the model behind every figure. The moves: one
relating at D4. The diary against the transcript: no entry unborne. Fidelity at B2 was 0.8: it bounds whether
the instrument decides, not whether it is right. Probe failures: none. The unplaced: sweden's themes, none.
Claims against their evidence: N12 (pattern) validated by its counts, F01 (pattern) by the ledger; claims-E1.md.

## 2. The ledgers
No departure; no fork (fork_comparison-C2.json absent). The counts rule: n_analysed = 3, the census 3 of 3,
and stage D4's four counts 2 + 1 + 0 + 0 = 3.

## 3. The three shares
does-not-compose: 1 of 3 rooms, 33 per cent, above prior.md's 15 per cent. Particulars: 0 per cent of lines, under
50 per cent. Corrections met twice: 0, under ten. Verdict: the model is compiled in Kozlowski and Klein's sense,
not composed, the does-not-compose share crossed.

## 6. Load-bearing
Every stage was load-bearing. "hold the line" [asoiaf/c0011] carried A01 and P07 in F01.

## 8. The methods paragraph
The coders built the first two tiers and the analyst the rest, with no overlap between the coders' collection
and the analysis; a census of the frame in place of sampling; an in-sample return at the second-order tier. The
canvas is what the drawing left behind, not a score; the analyst held every room's outcome while building.
Everything is archived with no promise that a rerun reproduces it.
"""
EXPERIENCE = "# experience-E1\n\n" + "".join("## %d. Section %d\nCited to the diary, E1-1.\n\n" % (i, i) for i in range(1, 12))


def base(outdir, root):
    s12.base(outdir, root)
    _w, _wj = s11._w, s11._wj
    _w(outdir, "_closes/model-D3.sha256", vlib.model_hash(outdir) + "\n")
    _w(outdir, "_closes/tree-D4.sha256", vlib.tree_hash(outdir) + "\n")
    # the D4 cut snap: taken after branches.jsonl, before the projection, so the fixture removes the
    # projection and the comparison, snaps, and writes them back
    proj = {n: open(os.path.join(outdir, n), encoding="utf-8").read()
            for n in ("projections-D4.jsonl", "chunk-share-D4.jsonl", "chunk-share-D4.md")}
    for n in proj:
        os.remove(os.path.join(outdir, n))
    tools = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for stage, label in (("B2", "scheme-B2-1-x"), ("C5", "close-C5-1-x"), ("D4", "cut-relating-D4-cut-1-x")):
        subprocess.run([sys.executable, os.path.join(tools, "snap.py"), stage, label, "--out", outdir],
                       check=True, stdout=subprocess.DEVNULL)
    for n, c in proj.items():
        _w(outdir, n, c)
    _w(outdir, "notes-E1.md", "# notes-E1\n\nThe sample, by seed 0: denmark, asoiaf, sweden.\n")
    _w(outdir, "audit-E1/quotes.py", "print('quotes')\n")
    _w(outdir, "audit-E1/quotes.txt", "3 quotes, 3 resolve\n")
    _w(outdir, "audit-E1.md", AUDIT)
    _wj(outdir, "reconstruction-E1.jsonl", [
        {"sub": "denmark", "branch": "F01", "verdict": "composes", "fidelity": 0.9, "claims": 10, "accounted": 9},
        {"sub": "asoiaf", "branch": "F01", "verdict": "does-not-compose", "fidelity": 0.4, "claims": 10, "accounted": 4},
        {"sub": "sweden", "branch": "none", "verdict": "composes", "fidelity": 1.0, "claims": 4, "accounted": 4}])
    _w(outdir, "expectations-E1.md", "# expectations-E1\n\nThe replication score by branch (F01 0.65) and by verdict; "
                                     "in-sample at every tier, including uncited material. Survival per branch: F01 70.\n")
    _w(outdir, "_probe/D4-D4a-01.answers.md", "goal: x\n")
    _w(outdir, "_probe/D4-D4a-01.json", json.dumps({"misses": [], "score": 1.0}))
    _w(outdir, "probes-E1.md", "# probes-E1\n\nRecall failures per stage and per question: stage D4, 0 misses.\n")
    _w(outdir, "experience-E1.md", EXPERIENCE)
    _w(outdir, "handback-E1.md", "# handback-E1\n\n" + "word " * 900)

    _wj(outdir, "departures.jsonl", [])
    _w(outdir, "run_manifest.json", json.dumps([
        {"stage": "D2", "model": "cheap", "seed": 0},
        {"stage": "E1", "file": "experience-E1.md", "sha256": vlib.sha(os.path.join(outdir, "experience-E1.md")),
         "model": "opus"}]))


def _plant_share_missing(outdir, root):
    base(outdir, root)
    s11._w(outdir, "audit-E1.md", AUDIT.replace("Corrections met twice: 0, under ten.", "No corrections recur."))


def _plant_no_verdict(outdir, root):
    base(outdir, root)
    s11._w(outdir, "audit-E1.md", AUDIT.replace("composition_status: supported",
                                                "Verdict: fine, per Kozlowski."))


def _plant_probe_unscored(outdir, root):
    base(outdir, root)
    os.remove(os.path.join(outdir, "_probe", "D4-D4a-01.json"))


def _plant_quote_unresolved(outdir, root):
    base(outdir, root)
    s11._w(outdir, "audit-E1.md", AUDIT.replace('"hold the line" [asoiaf/c0011]', '"defending" [asoiaf/c0011]'))


def _plant_id_unresolved(outdir, root):
    base(outdir, root)
    s11._w(outdir, "audit-E1.md", AUDIT.replace("carried A01 and P07", "carried A01, P07 and K09"))


def _plant_methods_not_last(outdir, root):
    base(outdir, root)
    s11._w(outdir, "audit-E1.md", AUDIT + "\n## 9. Afterword\nMore.\n")


def _plant_cut_after_projection(outdir, root):
    base(outdir, root)
    tools = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, os.path.join(tools, "snap.py"), "D4", "cut-splitting-D4-cut-2-y", "--out", outdir],
                   check=True, stdout=subprocess.DEVNULL)


def _plant_manifest_stale(outdir, root):
    base(outdir, root)
    s11._w(outdir, "experience-E1.md", EXPERIENCE + "\nOne more line after the hash.\n")


def _plant_sample_unnamed(outdir, root):
    base(outdir, root)
    s11._w(outdir, "notes-E1.md", "# notes-E1\n\nThe sample, by seed 0: denmark, asoiaf.\n")


def _plant_field_unscored(outdir, root):
    base(outdir, root)
    s11._wj(outdir, "sealed/FIELD.jsonl", [{"id": "A09", "kind": "order", "origin": "from-field"}])


PLANTED = [
    ("a field entry not scored apart", _plant_field_unscored, "The field's entries"),
    ("composition diagnostic missing", _plant_share_missing, "does not report the composition diagnostic 'corrections met twice'"),
    ("no composition verdict", _plant_no_verdict, "gives no composition verdict"),
    ("probe answers unscored", _plant_probe_unscored, "has no score file"),
    ("quote unresolved", _plant_quote_unresolved, "quote does not resolve to a participant's words"),
    ("id unresolved", _plant_id_unresolved, "names K09, which resolves to nothing"),
    ("methods paragraph not last", _plant_methods_not_last, "methods paragraph is not its last section"),
    ("cut snapped after projection", _plant_cut_after_projection, "existed before this cut was snapped"),
    ("manifest hash stale", _plant_manifest_stale, "does not carry experience-E1.md's sha256"),
    ("sampled room unnamed", _plant_sample_unnamed, "which notes-E1.md does not name"),
]
