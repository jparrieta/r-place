#!/usr/bin/env python3
"""room.py — one room of the yard, driven from the outside.

Every command is run in the room's own directory (rooms/<sub>/), or with --room <dir>. The
room holds the instrument, the record, the pre-week and, when one exists, the brief; nothing
here calls a model. A person or an agent of any provider runs these commands and launches the
agents between them, as CONTRACT-scheduler.md describes.

    python3 ../../_tools/room.py status                   what the room holds and what is next
    python3 ../../_tools/room.py brief   --model <id>     build brief/ from the pre-week (if no brief yet)
    python3 ../../_tools/room.py run     --model <id>     build run/ from the record and the brief
    python3 ../../_tools/room.py message <which>          print the opening message for an agent:
                                                          brief | lead | coder NN | collect NN | finish | fork
    python3 ../../_tools/room.py check   [--batch NN | --brief | --fork <name>]
                                                          the scheduler's mechanical checks (verify_room.py)
    python3 ../../_tools/room.py snapshot <name>          tar run/ to snapshots/<name>.tgz
    python3 ../../_tools/room.py fork <name> [--from after-fleet]
                                                          forks/<name>/run from a snapshot
    python3 ../../_tools/room.py note "<text>"            append a dated line to STATE.json notes
    python3 ../../_tools/room.py final --batch NN "<the coder's final message>"
                                                          save it beside the coder's notes, for the ledger

STATE.json is the room's memory. room.py rewrites it from what the files say; the scheduler
adds the things files cannot say (who ran, how long, what went wrong).
"""
import argparse, datetime, glob, gzip, hashlib, json, os, re, shutil, subprocess, sys, tarfile, time


def write_file(path, data, aside=None):
    """Write data to path, replacing the file. On a mount that refuses to open an existing
    file for writing (some synced folders do), rename the old file aside (into `aside`, or
    beside it as .old) and write a new one."""
    mode = "wb" if isinstance(data, bytes) else "w"
    try:
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "written"
    except PermissionError:
        if not os.path.exists(path):
            raise
        if aside:
            os.makedirs(aside, exist_ok=True)
            dst = os.path.join(aside, os.path.basename(path) + ".%d" % int(time.time() * 1000))
        else:
            dst = path + ".old"
        os.replace(path, dst)
        with open(path, mode, encoding=None if mode == "wb" else "utf-8") as fh:
            fh.write(data)
        return "replaced"

HERE = os.path.dirname(os.path.abspath(__file__))


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state(room):
    p = os.path.join(room, "STATE.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_state(room, st):
    st["updated"] = now()
    write_file(os.path.join(room, "STATE.json"), json.dumps(st, indent=1))


def gunzip(src, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return dst
    with gzip.open(src, "rb") as f, open(dst, "wb") as g:
        shutil.copyfileobj(f, g)
    return dst


def sh(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FAILED: %s\n%s%s" % (" ".join(cmd), r.stdout[-3000:], r.stderr[-3000:]))
    return r.stdout


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def _brief_manifest(room):
    p = os.path.join(room, "brief", "_manifest.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def _legacy_imported_brief(man):
    """build_room.py marks briefs copied from an earlier run this way. They predate the
    brief validation gate and remain usable without rewriting or retroactively validating
    them."""
    return str(man.get("brief") or "").startswith("existing:")


def _brief_validation_inputs(room):
    """Return one digest over every current file to which a brief check is bound."""
    bdir = os.path.join(room, "brief")
    names = {"_manifest.json", "out/brief.md", "out/evidence.json",
             "out/_read.jsonl", "out/_read_brief.jsonl", "out/_transcript.jsonl"}
    try:
        manifest = _brief_manifest(room)
    except (OSError, ValueError):
        manifest = {}
    root = os.path.realpath(bdir)
    for name in (manifest.get("sha256") or {}):
        if not isinstance(name, str) or not name or os.path.isabs(name):
            continue
        normalized = os.path.normpath(name)
        candidate = os.path.realpath(os.path.join(bdir, normalized))
        try:
            safe = os.path.commonpath([root, candidate]) == root
        except ValueError:
            safe = False
        if safe and normalized not in (".", ".."):
            names.add(normalized)
    files = {}
    for name in sorted(names):
        p = os.path.join(bdir, name)
        if os.path.isfile(p):
            files[name] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        else:
            files[name] = "MISSING"
    h = hashlib.sha256()
    for name, digest in sorted(files.items()):
        h.update(name.encode("utf-8") + b"\0" + digest.encode("ascii") + b"\n")
    return h.hexdigest(), files


def _brief_validation(room, man=None):
    """Describe whether the current brief files have a current coordinator check."""
    man = man if man is not None else _brief_manifest(room)
    md = os.path.join(room, "brief", "out", "brief.md")
    if not os.path.isfile(md):
        return {"required": not _legacy_imported_brief(man), "status": "missing",
                "current": False, "passed": False}
    if _legacy_imported_brief(man):
        return {"required": False, "status": "legacy imported", "current": True,
                "passed": None}
    vp = os.path.join(room, "brief", "out", "_validation.json")
    if not os.path.isfile(vp):
        return {"required": True, "status": "awaiting", "current": False,
                "passed": False}
    try:
        receipt = json.load(open(vp, encoding="utf-8"))
    except (OSError, ValueError):
        return {"required": True, "status": "stale", "current": False,
                "passed": False}
    digest, files = _brief_validation_inputs(room)
    recorded_files = receipt.get("sha256")
    current = receipt.get("digest") == digest and recorded_files == files
    if not current:
        status = "stale"
    else:
        status = "passed" if receipt.get("passed") is True else "failed"
    return {"required": True, "status": status, "current": current,
            "passed": current and receipt.get("passed") is True, "receipt": receipt,
            "digest": digest, "sha256": files}


def _write_brief_validation(room, returncode):
    man = _brief_manifest(room)
    digest, files = _brief_validation_inputs(room)
    checked = now()
    receipt = {"checked_at": checked, "checked_utc": checked,
               "result": "passed" if returncode == 0 else "failed",
               "passed": returncode == 0, "returncode": returncode,
               "digest": digest, "sha256": files,
               "instrument": man.get("instrument"), "brief_revision": man.get("brief_revision"),
               "model": man.get("model")}
    out = os.path.join(room, "brief", "out")
    os.makedirs(out, exist_ok=True)
    write_file(os.path.join(out, "_validation.json"),
               json.dumps(receipt, indent=1, ensure_ascii=False) + "\n")
    return receipt


# ---- status: read the files, write STATE.json --------------------------------------------
def refresh(room, persist=True):
    st = load_state(room)
    if (st.get('verified_utc') and st.get('materials_archive')
            and os.path.isfile(st['materials_archive'])
            and all(not os.path.isdir(os.path.join(room, name))
                    for name in ('record', 'brief', 'instrument'))):
        # Keep the verified room's saved metadata until its materials are restored.
        st['stage'] = 'verified'
        if persist:
            save_state(room, st)
        return st
    sub = st.get("sub") or os.path.basename(os.path.abspath(room))
    st["sub"] = sub
    inst = os.path.join(room, "instrument")
    if os.path.exists(os.path.join(inst, "newrun.py")):
        try:
            text = open(os.path.join(inst, "newrun.py"), encoding="utf-8").read(4096)
            m = re.search(r'^INSTRUMENT\s*=\s*["\'](v\d+)["\']', text, re.M)
            st["instrument"] = m.group(1) if m else "unknown"
        except OSError:
            st["instrument"] = "unknown"
    else:
        st["instrument"] = None
    brief_md = os.path.join(room, "brief", "out", "brief.md")
    bman = _brief_manifest(room)
    if os.path.exists(brief_md):
        src = bman.get("brief") if bman else None
        st["brief"] = src or "present"
    else:
        st["brief"] = "to write"
    if bman.get("model"):
        st["brief_model"] = bman["model"]
    elif not _legacy_imported_brief(bman):
        st.pop("brief_model", None)
    if bman.get("brief_revision"):
        st["brief_revision"] = bman["brief_revision"]
    elif not _legacy_imported_brief(bman):
        st.pop("brief_revision", None)
    bv = _brief_validation(room, bman)
    if bv["required"]:
        st["brief_verified"] = bool(bv["passed"])
        st["brief_validation"] = bv["status"]
        receipt = bv.get("receipt") or {}
        if receipt.get("checked_at"):
            st["brief_checked_at"] = receipt["checked_at"]
            st["brief_validation_digest"] = receipt.get("digest")
        else:
            st.pop("brief_checked_at", None)
            st.pop("brief_validation_digest", None)
    else:
        # Imported briefs are intentionally outside the new validation lifecycle. Do not
        # manufacture or retain a verification claim for an artifact that predates receipts.
        for key in ("brief_verified", "brief_validation", "brief_checked_at",
                    "brief_validation_digest"):
            st.pop(key, None)
    run = os.path.join(room, "run")
    stage = "new"
    if st["brief"] == "to write":
        stage = "brief to write"
        if os.path.exists(os.path.join(room, "brief", "_manifest.json")):
            stage = "brief built, writer to run"
    elif bv["required"]:
        if bv["status"] == "failed":
            stage = "brief failed validation"
        elif bv["passed"]:
            stage = "brief verified"
        else:
            stage = "brief awaiting validation"
    if os.path.exists(os.path.join(run, "_manifest.json")):
        man = json.load(open(os.path.join(run, "_manifest.json")))
        st["model"] = man.get("model")
        st["fingerprint"] = man.get("instrument_fingerprint")
        stage = "run built"
        gate_p = os.path.join(run, "out", "_gate.json")
        if os.path.exists(gate_p):
            g = json.load(open(gate_p))
            st["branch"] = g["branch"]
            st["slices"] = len(g["slices"])
            st["threshold"] = g.get("threshold")
            if g["branch"] == "B":
                coders = g.get("coders", [])
                done = [c for c in coders if c.get("collected_utc")]
                if g.get("consolidated_utc"):
                    stage = "fleet done, consolidated"
                elif coders and not coders[-1].get("collected_utc"):
                    stage = "coder %s of %d running" % (coders[-1]["batch"], len(g["slices"]))
                elif len(done) == len(g["slices"]):
                    stage = "fleet done, to consolidate"
                elif done:
                    stage = "coder %02d of %d to dispatch" % (len(done) + 1, len(g["slices"]))
                else:
                    stage = "planned, coder 01 to dispatch"
            else:
                stage = "lead reading (branch A)"
        runj = os.path.join(run, "out", "_run.json")
        if os.path.exists(runj):
            r = json.load(open(runj))
            st["verdict"] = r.get("verdict")
            st["codes"] = r.get("n_codes")
            st["themes"] = r.get("n_themes")
            stage = "closed" if r.get("verdict") else "closed once (no verdict yet)"
    snaps = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(room, "snapshots", "*.tgz")))
    st["snapshots"] = snaps
    st["forks"] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(room, "forks", "*")))
    if st.get("verified_utc"):
        stage = "verified"
    if st.get("failed"):
        stage = "failed: " + st["failed"]
    st["stage"] = stage
    if persist:
        save_state(room, st)
    return st


def nxt(st):
    s = st.get("stage", "")
    if s == "brief to write":
        return "`brief --model <id>`, then launch the writer in brief/ with `message brief`"
    if s == "brief built, writer to run":
        return "launch the writer in brief/ with `message brief`; when it ends, place its transcript in brief/out/_transcript.jsonl and `check --brief`"
    if s == "brief awaiting validation":
        return "run `check --brief`; only a current passing receipt can start the run"
    if s == "brief failed validation":
        return "correct the brief-stage failures, then run `check --brief` again"
    if s == "brief verified":
        return "`run --model <id>`"
    if s == "new":
        return "`run --model <id>` (the brief is present)"
    if s == "run built":
        return "launch the case lead with `message lead`"
    if s.startswith("planned") or s.endswith("to dispatch"):
        return "tell the lead to dispatch the next batch (`message collect NN` after a coder, or the lead already did); launch the coder with `message coder NN`"
    if s.startswith("coder") and s.endswith("running"):
        return "when the coder ends: copy its transcript, `check --batch NN`, then `message collect NN` to the lead"
    if s == "fleet done, to consolidate":
        if "after-fleet" in (st.get("snapshots") or []):
            return "snapshot taken; `message finish` to the lead (or `fork <name>` and a fresh lead there)"
        return "`snapshot after-fleet`; then `message finish` to the lead (or a fresh lead on a fork)"
    if s == "fleet done, consolidated":
        return "the lead is on steps 4 and 5; when it reports, `check`"
    if s.startswith("lead reading"):
        return "wait for the lead; when it reports, `check`"
    if s.startswith("closed"):
        return "`check`; on PASSED, `room.py note` the cost and mark verified"
    return "-"


# ---- brief and run ------------------------------------------------------------------------
def brief(room, model):
    st = refresh(room)
    bdir = os.path.join(room, "brief")
    if os.path.exists(os.path.join(bdir, "out", "brief.md")):
        print("brief exists (%s); nothing built" % st["brief"])
        return 0
    pre_gz = os.path.join(room, "record", "preweek.jsonl.gz")
    pre = gunzip(pre_gz, os.path.join(room, "record", "preweek.jsonl"))
    out = sh(["python3", os.path.join(room, "instrument", "newbrief.py"), bdir, st["sub"], pre, model], cwd=room)
    print(out.strip())
    st = refresh(room)
    st.setdefault("log", []).append({"at": now(), "event": "brief built", "model": model})
    save_state(room, st)
    return 0


def run(room, model):
    st = refresh(room)
    rdir = os.path.join(room, "run")
    if os.path.exists(os.path.join(rdir, "_manifest.json")):
        sys.exit("run/ exists (model %s). Move it aside first if it is to be rebuilt." % st.get("model"))
    brief_md = os.path.join(room, "brief", "out", "brief.md")
    if not os.path.exists(brief_md):
        sys.exit("no brief yet: run `brief --model <id>` and the brief writer first, or place a "
                 "brief.md at brief/out/brief.md")
    bv = _brief_validation(room)
    if bv["required"] and not bv["passed"]:
        if bv["status"] == "failed":
            why = "brief failed validation"
        elif bv["status"] == "stale":
            why = "brief validation is stale because a checked file changed"
        else:
            why = "brief is awaiting validation"
        sys.exit(why + "; run `check --brief` and obtain a current passing receipt first")
    rec = gunzip(os.path.join(room, "record", "coder_corpus.jsonl.gz"),
                 os.path.join(room, "record", "coder_corpus.jsonl"))
    out = sh(["python3", os.path.join(room, "instrument", "newrun.py"), rdir, st["sub"], rec, brief_md, model], cwd=room)
    print(out.strip()[-600:])
    st = refresh(room)
    st.setdefault("log", []).append({"at": now(), "event": "run built", "model": model})
    st["started"] = st.get("started") or now()
    save_state(room, st)
    print("\nnext:", nxt(st))
    return 0


# ---- messages -----------------------------------------------------------------------------
MSG = {
"brief": """Your run directory is {bdir}. Work only inside it: write nothing anywhere else, not even in a scratchpad directory the environment names. Read CONTRACT.md there and follow it. Write out/brief.md and stop.""",
"lead": """Your run directory is {rdir}. Work only inside it: write nothing anywhere else, not even in a scratchpad directory the environment names. Read AGENT.md, then CONTRACT.md, then CONTRACT-case-lead.md. You are the case lead. Run the gate. If the branch is A, read the room and do every step through emit.close(verdict=...), then send your final message. If the branch is B, do what the case lead does up to and including dispatching batch 01 with --model {model}, then stop and tell me, in a few lines: the branch, the counts it was decided on, the number of slices, and that batch 01 is dispatched. Do not run any coder yourself: I am the scheduler. I run each coder in its fleet/batch_NN directory and tell you when it has finished; you then collect it, read what it appended to the two facts files, and dispatch the next. Write nothing in the coders' directories. Keep your replies to me short.""",
"coder": """Your run directory is {rdir}/fleet/batch_{nn}. Work only inside it: write nothing anywhere else, not even in a scratchpad directory the environment names; AGENT.md's scratch rule wins. Read AGENT.md, then CONTRACT.md, then CONTRACT-fleet-coder.md. Do your slice and stop.""",
"collect": """Batch {nn} has finished: {summary}. Collect it, read what it appended to the two facts files (strike any line that is a reading, and say so in notes.md), then dispatch batch {next} with --model {model}. Reply in one line with what collect and dispatch printed.""",
"collect_last": """Batch {nn} has finished: {summary}. It is the last slice. Collect it, read and review its additions to the facts files, record your strikes and remarks in out/ledger.md, out/_lead_notes.md and notes.md, then STOP and reply in one line. Do not consolidate, pool, theme, or start steps 4 and 5. The scheduler must checkpoint this completed turn before you continue.""",
"finish": """All slices through batch {nn} have already been collected and the scheduler has saved the checkpoint. Do not collect the last batch again. Now do the rest of the case lead's work as CONTRACT-case-lead.md §2 orders it: consolidate, emit.close() once, the forest (§4), the gate (§5; on FAILED stop and report its output), step 4 over the pooled codes and the slice cases, step 5 with the counter-reading search (find and read item are open to you now), then emit.close(verdict=...). Write case.md and notes.md as the contracts say. When you have finished, send me your final message in the contract's form.""",
"fork": """Your run directory is {rdir}. Work only inside it: write nothing anywhere else, not even in a scratchpad directory the environment names. Read AGENT.md, then CONTRACT.md, then CONTRACT-case-lead.md. You are the case lead of a run whose fleet has already finished and been collected by a previous lead, but has NOT been consolidated: out/_gate.json and every fleet/batch_NN/out/ are complete, and out/timeline.md and out/lexicon.md hold what the coders left. You did not dispatch the coders: read out/ledger.md and out/_lead_notes.md first, which are the previous lead's memory of the fleet, then the coders' notes in fleet/batch_NN/out/notes.md as you need them. Do the rest of the case lead's work as CONTRACT-case-lead.md §2 orders it from consolidation onward: run tools/fleet.py consolidate once, then emit.close() once, the forest (§4), the gate (§5; on FAILED stop and report its output), step 4 over the pooled codes and the slice cases, step 5 with the counter-reading search, then emit.close(verdict=...). Write case.md and notes.md as the contracts say, and say in notes.md that you are a fork's lead. When you have finished, send me your final message in the contract's form.""",
}


def message(room, which, nn=None, model=None, summary=None, fork=None):
    st = refresh(room, persist=False)
    rdir = os.path.abspath(os.path.join(room, "forks", fork, "run") if fork else os.path.join(room, "run"))
    model = model or st.get("model") or "<model id>"
    if which == "brief":
        print(MSG["brief"].format(bdir=os.path.abspath(os.path.join(room, "brief"))))
    elif which == "lead":
        print(MSG["lead"].format(rdir=rdir, model=model))
    elif which == "coder":
        print(MSG["coder"].format(rdir=rdir, nn="%02d" % int(nn)))
    elif which == "collect":
        n = int(nn)
        summary = summary or "<codes, pointers, threads disposed, facts lines added>"
        if st.get("slices") and n == st["slices"]:
            print(MSG["collect_last"].format(nn="%02d" % n, summary=summary))
        else:
            print(MSG["collect"].format(nn="%02d" % n, summary=summary, next="%02d" % (n + 1), model=model))
    elif which == "finish":
        print(MSG["finish"].format(nn="%02d" % int(nn or st.get("slices") or 0),
                                   summary=summary or "<summary>"))
        print("Completion checklist for this resumed lead: before the final "
              "emit.close(verdict=...), read out/_gate.json and put the literal line "
              "`branch B; threshold N; items_in_window N; chars_by_people N` in "
              "out/notes.md, replacing each N with its corresponding value from "
              "the gate. Check the complete case and notes against the required "
              "headings, citations, counter-reading and completion requirements; "
              "a previous retry note does not replace that full check. Preserve "
              "the prescribed order above and all append-only records.")
    elif which == "fork":
        print(MSG["fork"].format(rdir=rdir))
    else:
        sys.exit("unknown message %r" % which)
    return 0


# ---- snapshot and fork ----------------------------------------------------------------------
def snapshot(room, name):
    """Legacy filesystem-only research snapshot; use codex_lead.py for native agent state."""
    st = refresh(room)
    if name == "after-fleet" and st.get("stage") != "fleet done, to consolidate":
        sys.exit("after-fleet requires all slices collected and no consolidation yet")
    sdir = os.path.join(room, "snapshots")
    os.makedirs(sdir, exist_ok=True)
    dst = os.path.join(sdir, "%s.tgz" % name)
    if os.path.exists(dst):
        sys.exit("snapshot %s exists" % name)
    pending = dst + ".pending"
    with tarfile.open(pending, "w:gz") as tf:
        tf.add(os.path.join(room, "run"), arcname="run")
    os.replace(pending, dst)
    st = refresh(room)
    st.setdefault("log", []).append({"at": now(), "event": "snapshot", "name": name})
    save_state(room, st)
    print("wrote", os.path.relpath(dst, room))
    return 0


def fork(room, name, source):
    st = refresh(room)
    src = os.path.join(room, "snapshots", "%s.tgz" % source)
    if not os.path.exists(src):
        sys.exit("no snapshot %s; take one with `snapshot %s` first" % (source, source))
    fdir = os.path.join(room, "forks", name)
    if os.path.exists(fdir):
        sys.exit("fork %s exists" % name)
    os.makedirs(fdir)
    with tarfile.open(src, "r:gz") as tf:
        for member in tf.getmembers():
            target = os.path.abspath(os.path.join(fdir, member.name))
            if os.path.commonpath([os.path.abspath(fdir), target]) != os.path.abspath(fdir) or not (member.isfile() or member.isdir()):
                sys.exit("unsafe member in filesystem snapshot: %s" % member.name)
        tf.extractall(fdir)
    # Reject pre-existing drift BEFORE rewriting authorized path-bearing files.
    import hashlib
    for dp, dn, fn in os.walk(os.path.join(fdir, "run")):
        if "_manifest.json" in fn:
            man = json.load(open(os.path.join(dp, "_manifest.json"), encoding="utf-8"))
            for rel, expected in (man.get("sha256") or {}).items():
                fp = os.path.join(dp, rel)
                if not os.path.isfile(fp) or hashlib.sha256(open(fp, "rb").read()).hexdigest() != expected:
                    sys.exit("snapshot instrument drift: %s; fork refused" % fp)
    rdir = os.path.join(fdir, "run")
    # the fork's run directory is elsewhere now: AGENT.md and the manifest carry absolute
    # paths of the original. Rewrite them, and record the lineage.
    old = os.path.abspath(os.path.join(room, "run"))
    new = os.path.abspath(rdir)
    rewritten = []
    for dp, dn, fn in os.walk(rdir):
        for f in fn:
            if f in ("AGENT.md", "CONTRACT.md", "CONTRACT-case-lead.md", "CONTRACT-fleet-coder.md",
                     "_manifest.json"):
                p = os.path.join(dp, f)
                s = open(p, encoding="utf-8").read()
                if old in s:
                    write_file(p, s.replace(old, new))
                    rewritten.append(p)
    # the rewritten files no longer hash to what the manifest recorded at dispatch; record the
    # parent's hashes beside the new ones so close_run C7 passes on the fork and the lineage
    # stays checkable (v30, after the audit found every fork failing C7)
    import hashlib
    for dp, dn, fn in os.walk(rdir):
        if "_manifest.json" not in fn:
            continue
        mp = os.path.join(dp, "_manifest.json")
        man = json.load(open(mp, encoding="utf-8"))
        sha = man.get("sha256") or {}
        changed = {}
        for rel, want in sha.items():
            fp = os.path.join(dp, rel)
            if os.path.exists(fp):
                got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
                if got != want:
                    if fp not in rewritten:
                        sys.exit("unexpected instrument drift while forking: %s" % fp)
                    changed[rel] = want
                    sha[rel] = got
        if changed:
            man["sha256"] = sha
            man.setdefault("forked_from_sha256", {}).update(changed)
            man["forked_from"] = {"parent_run": old, "snapshot": source, "fork": name}
            write_file(mp, json.dumps(man, indent=1, ensure_ascii=False))
    lineage = {"fork": name, "from_snapshot": source, "parent_run": old, "forked_at": now(),
               "rewritten": [os.path.relpath(p, fdir) for p in rewritten]}
    json.dump(lineage, open(os.path.join(fdir, "FORK.json"), "w"), indent=1)
    st = refresh(room)
    st.setdefault("log", []).append({"at": now(), "event": "fork", "name": name, "from": source})
    save_state(room, st)
    print("forked %s from %s -> %s" % (name, source, os.path.relpath(rdir, room)))
    print("launch a fresh lead with:  room.py message fork --fork %s" % name)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "brief", "run", "message", "check", "snapshot", "fork", "note", "final"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--room", default=".")
    ap.add_argument("--model")
    ap.add_argument("--batch")
    ap.add_argument("--summary")
    ap.add_argument("--fork")
    ap.add_argument("--from", dest="source", default="after-fleet")
    ap.add_argument("--brief", action="store_true", help="check: the brief stage instead of the run")
    a = ap.parse_args()
    room = os.path.abspath(a.room)
    if a.cmd == "status":
        st = refresh(room)
        keys = ["sub", "items_in_window", "threads", "brief", "brief_model", "brief_revision",
                "brief_verified", "brief_validation", "instrument", "model", "branch", "slices",
                "stage", "verdict", "codes", "snapshots", "forks"]
        for k in keys:
            if k in st:
                print("%-16s %s" % (k, st[k]))
        print("%-16s %s" % ("next", nxt(st)))
        return 0
    if a.cmd == "brief":
        if not a.model:
            sys.exit("brief needs --model <id> (the brief writer's model is a condition of the brief)")
        return brief(room, a.model)
    if a.cmd == "run":
        if not a.model:
            sys.exit("run needs --model <id>")
        return run(room, a.model)
    if a.cmd == "message":
        return message(room, a.arg, nn=a.batch, model=a.model, summary=a.summary, fork=a.fork)
    if a.cmd == "check":
        cmd = ["python3", os.path.join(HERE, "verify_room.py"), "--room", room]
        if a.batch:
            cmd += ["--batch", a.batch]
        if a.fork:
            cmd += ["--fork", a.fork]
        if a.brief:
            cmd += ["--brief"]
        r = subprocess.run(cmd)
        if a.brief:
            if not _legacy_imported_brief(_brief_manifest(room)):
                _write_brief_validation(room, r.returncode)
            refresh(room)
        return r.returncode
    if a.cmd == "snapshot":
        return snapshot(room, a.arg or "after-fleet")
    if a.cmd == "fork":
        return fork(room, a.arg, a.source)
    if a.cmd == "final":
        # the coder's final message, saved beside its notes so that collect can put it in the ledger
        if not a.batch:
            sys.exit("final needs --batch NN and the message as the argument (or on stdin)")
        text = a.arg if a.arg else sys.stdin.read()
        bdir = os.path.join(room, "forks", a.fork, "run") if a.fork else os.path.join(room, "run")
        p = os.path.join(bdir, "fleet", "batch_%02d" % int(a.batch), "out", "final_message.md")
        if not os.path.isdir(os.path.dirname(p)):
            sys.exit("no such batch directory: %s" % os.path.dirname(p))
        write_file(p, text.strip() + "\n")
        print("saved", os.path.relpath(p, room))
        return 0
    if a.cmd == "note":
        st = refresh(room)
        st.setdefault("notes", []).append({"at": now(), "note": a.arg})
        save_state(room, st)
        return 0


if __name__ == "__main__":
    sys.exit(main())
