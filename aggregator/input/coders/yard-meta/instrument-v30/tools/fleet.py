#!/usr/bin/env python3
"""fleet.py — the case lead's harness for branch B, instrument v30.

Run from the case lead's run directory (the one newrun.py built). Four commands, in order:

    python3 tools/fleet.py plan       [--threshold 500] [--budget 500] [--floor 25]
    python3 tools/fleet.py dispatch   --batch NN --model <model id>
    python3 tools/fleet.py collect    --batch NN
    python3 tools/fleet.py consolidate
    python3 tools/fleet.py status

`plan` reads the record and corpus_manifest.json, decides the branch (B when the in-window
item count exceeds the threshold), cuts the threads into slices, and writes out/_gate.json:
the branch, the threshold, the two counts, one line per slice with its first and last thread
and its timestamps, and an empty coders list. It also starts out/timeline.md and
out/lexicon.md as empty files with a header, unless they exist. Slices are whole threads in
corpus order; a slice ends at the last thread that fits the budget of in-window items; a
thread larger than the budget is a slice by itself; a slice of fewer than `floor` items joins
the slice before it (or, if it is the first, the one after), so no coder is dispatched for a
handful of comments stranded ahead of an oversized thread.

`dispatch` builds fleet/batch_NN/ for one coder: the slice's threads as its record, plus the
opening post of every earlier-slice thread that was still receiving replies during this
slice's span, marked as context (never coded: emit refuses it). Its code ids continue from
the previous batch's last id. timeline.md and lexicon.md are copied in as the lead's out/
holds them at that moment, so dispatch batch NN after the lead has checked what batch NN-1
appended. One line per coder goes into _gate.json.

`collect`, after a coder has finished: brings its timeline.md and lexicon.md back into the
lead's out/, so the lead can read what the coder appended before the next dispatch. The next
dispatch refuses until the previous batch is collected.

`consolidate`, after the last coder: closes each batch's emit (writing its codes, threads
and pointers files), copies them and each batch's read log into staging/, pools them into
package/codes.jsonl, package/threads.jsonl and package/pointers.jsonl, and writes the lead's
out/_journal.jsonl so that the lead's emit holds every fleet code and can theme it.

Nothing here reads a coder's case or notes, and nothing here interprets anything.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OPEN = 1490976000
END = 1491238800 + 24 * 3600


def jl(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def wjl(path, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def tid_of(r):
    return r["id"] if r.get("kind") == "post" else (r.get("link_id") or "t3_?")[3:]


def load_record(run):
    path = os.path.join(run, "coder_corpus.jsonl")
    header, items = None, []
    for r in jl(path):
        if "id" in r:
            items.append(r)
        elif "_thread_index" in r:
            header = r
    return header, items


def opened_at(rs):
    """The renderer's key: a thread is placed at its first in-window item, or, when it has
    none, at its earliest item. The slices follow the corpus the coder reads."""
    inw = [r.get("created_utc") or 0 for r in rs if not r.get("_context")]
    return min(inw) if inw else min(r.get("created_utc") or 0 for r in rs)


def threads_in_order(items):
    """thread id -> its items in time order; threads in corpus order, the order the
    renderer prints them and the coder contract fixes."""
    by = {}
    for r in items:
        by.setdefault(tid_of(r), []).append(r)
    for rs in by.values():
        rs.sort(key=lambda r: (r.get("created_utc") or 0, r.get("id") or ""))
    order = sorted(by, key=lambda t: (opened_at(by[t]), t))
    return by, order


def inwin(r):
    return not r.get("_context")


# ---- plan ---------------------------------------------------------------------------------
def plan(a):
    run = a.run
    man_path = os.path.join(run, "corpus_manifest.json")
    if not os.path.exists(man_path):
        sys.exit("no corpus_manifest.json in %s; newrun.py writes it" % run)
    man = json.load(open(man_path, encoding="utf-8"))
    gate_path = os.path.join(run, "out", "_gate.json")
    if os.path.exists(gate_path) and not a.force:
        sys.exit("REFUSING: %s exists. The gate is decided once; --force to redo it before "
                 "any coder has been dispatched." % gate_path)
    header, items = load_record(run)
    by, order = threads_in_order(items)
    n_in = man["items_in_window"]
    branch = "B" if n_in > a.threshold else "A"
    slices = []
    if branch == "B":
        cur, cur_items, cur_chars = [], 0, 0
        for t in order:
            rs = by[t]
            n = sum(1 for r in rs if inwin(r))
            ch = sum(len(r.get("body") or r.get("selftext") or "") for r in rs if inwin(r))
            if cur and cur_items + n > a.budget:
                slices.append((cur, cur_items, cur_chars))
                cur, cur_items, cur_chars = [], 0, 0
            cur.append(t); cur_items += n; cur_chars += ch
        if cur:
            slices.append((cur, cur_items, cur_chars))
        # v30: fold any slice under the floor into its neighbour. Whole threads still never
        # split; the neighbour just grows by a few items.
        folded = []
        for sl in slices:
            if sl[1] < a.floor and folded:
                p = folded.pop()
                folded.append((p[0] + sl[0], p[1] + sl[1], p[2] + sl[2]))
            else:
                folded.append(sl)
        if len(folded) > 1 and folded[0][1] < a.floor:
            a0, a1 = folded[0], folded[1]
            folded = [(a0[0] + a1[0], a0[1] + a1[1], a0[2] + a1[2])] + folded[2:]
        slices = folded
    rows = []
    for i, (ts, n, ch) in enumerate(slices, 1):
        first, last = ts[0], ts[-1]
        start = opened_at(by[first])
        last_open = opened_at(by[last])
        last_item = max(r.get("created_utc") or 0 for t in ts for r in by[t])
        rows.append({"batch": "%02d" % i, "first_thread": first, "last_thread": last,
                     "n_threads": len(ts), "items_in_window": n, "chars_in_window": ch,
                     "start_utc": start, "last_opening_utc": last_open,
                     "last_item_utc": last_item,
                     "start_hour": round((start - OPEN) / 3600.0, 2),
                     "last_opening_hour": round((last_open - OPEN) / 3600.0, 2),
                     "threads": ts})
    gate = {"instrument": "v30", "sub": man["sub"], "branch": branch,
            "threshold": a.threshold, "budget_items": a.budget, "floor_items": a.floor,
            "items_in_window": n_in, "items_by_people": man.get("items_by_people"),
            "chars_by_people": man["chars_by_people"], "threads": man["threads"],
            "decided_utc": now(),
            "rule": "branch B when items_in_window > threshold; slices are whole threads in "
                    "corpus order, at most budget_items in-window items each, a larger "
                    "thread a slice by itself, a slice under floor_items folded into its "
                    "neighbour",
            "slices": rows, "coders": []}
    os.makedirs(os.path.join(run, "out"), exist_ok=True)
    json.dump(gate, open(gate_path, "w", encoding="utf-8"), indent=1)
    for name, head in (("timeline.md", "# timeline — r/%s\n\nFacts only: stickies, moderator "
                        "posts, edits, with times and item ids. One line each, in time order. "
                        "Started by the case lead from the brief; extended by each coder.\n\n"),
                       ("lexicon.md", "# lexicon — r/%s\n\nOne term per line, with the item id "
                        "of its first use. No gloss. Started by the case lead from the brief; "
                        "extended by each coder.\n\n")):
        p = os.path.join(run, "out", name)
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(head % man["sub"])
            if name == "timeline.md":
                # v30: the harness seeds the timeline with what the metadata already says,
                # every stickied or moderator-distinguished post, so coders extend a record
                # of facts instead of starting one
                lines = []
                for t in order:
                    post = next((r for r in by[t] if r.get("kind") == "post"), None)
                    if not post or not (post.get("stickied") or post.get("distinguished")):
                        continue
                    utc = post.get("created_utc") or 0
                    marks = " ".join(m for m in ("[sticky@retrieval]" if post.get("stickied") else "",
                                                 "[%s]" % post["distinguished"] if post.get("distinguished") else "") if m)
                    lines.append("- H%+.2f %s %s post by %s: %s (%s)" % (
                        (utc - OPEN) / 3600.0,
                        datetime.datetime.utcfromtimestamp(utc).strftime("%m-%d %H:%M"),
                        marks, post.get("author") or "[deleted]",
                        " ".join((post.get("title") or "").split())[:120], t))
                if lines:
                    with open(p, "a", encoding="utf-8") as fh:
                        fh.write("## seeded by the harness from the record's metadata (sticky and moderator marks "
                                 "are as of retrieval)\n\n" + "\n".join(lines) + "\n\n")
    print("branch %s: %d in-window items against a threshold of %d; budget %d items per slice"
          % (branch, n_in, a.threshold, a.budget))
    for r in rows:
        print("  batch %s  threads %4d  items %4d  chars %7d  h%+7.2f .. h%+7.2f  %s .. %s"
              % (r["batch"], r["n_threads"], r["items_in_window"], r["chars_in_window"],
                 r["start_hour"], r["last_opening_hour"], r["first_thread"], r["last_thread"]))
    print("wrote %s; started out/timeline.md and out/lexicon.md" % os.path.relpath(gate_path, run))
    return 0


# ---- dispatch -----------------------------------------------------------------------------
def dispatch(a):
    run = a.run
    gate_path = os.path.join(run, "out", "_gate.json")
    gate = json.load(open(gate_path, encoding="utf-8"))
    if gate["branch"] != "B":
        sys.exit("branch %s: there is no fleet to dispatch" % gate["branch"])
    want = "%02d" % a.batch
    sl = next((s for s in gate["slices"] if s["batch"] == want), None)
    if sl is None:
        sys.exit("no slice %s in the gate (%d slices)" % (want, len(gate["slices"])))
    done = {c["batch"] for c in gate["coders"]}
    prev = "%02d" % (a.batch - 1)
    if a.batch > 1 and prev not in done:
        sys.exit("batch %s has not been dispatched; the fleet is serial" % prev)
    if want in done:
        sys.exit("batch %s was already dispatched" % want)
    if a.batch > 1:
        pc = next(c for c in gate["coders"] if c["batch"] == prev)
        if not pc.get("collected_utc"):
            sys.exit("batch %s has not been collected; run collect --batch %s and read what it "
                     "appended to out/timeline.md and out/lexicon.md first" % (prev, prev))
    header, items = load_record(run)
    by, order = threads_in_order(items)
    mine = set(sl["threads"])
    span_lo, span_hi = sl["start_utc"], min(sl["last_item_utc"], END)
    earlier = [s for s in gate["slices"] if int(s["batch"]) < a.batch]
    rows = []
    n_ctx = 0
    # openings of earlier-slice threads still receiving replies in this slice's span
    for s in earlier:
        for t in s["threads"]:
            rs = by[t]
            active = any(span_lo <= (r.get("created_utc") or 0) <= span_hi for r in rs
                         if r.get("kind") != "post")
            if not active:
                continue
            post = next((r for r in rs if r.get("kind") == "post"), None)
            if post is None:
                continue
            c = dict(post)
            c["_context"] = True
            c["_slice_context"] = True
            rows.append(c)
            n_ctx += 1
    for t in order:
        if t in mine:
            rows.extend(by[t])
    if header is not None:
        h = dict(header)
        h["_thread_index"] = [x for x in header.get("_thread_index", []) if x["thread_id"] in mine]
        h["_slice"] = {"batch": want, "first_thread": sl["first_thread"],
                       "last_thread": sl["last_thread"], "n_threads": sl["n_threads"]}
        rows = [h] + rows
    tmp = os.path.join(run, "fleet", "_slice_%s.jsonl" % want)
    wjl(tmp, rows)
    # ids continue from the previous batch
    code_start, ptr_start = 1, 1
    if a.batch > 1:
        pj = os.path.join(run, "fleet", "batch_%s" % prev, "out", "_journal.jsonl")
        mx_c = mx_p = 0
        for r in jl(pj):
            if r.get("kind") == "code":
                mx_c = max(mx_c, int(r["rec"]["code_id"][1:]))
            elif r.get("kind") == "pointer":
                mx_p = max(mx_p, int(r["rec"]["pointer_id"][1:]))
        pm = json.load(open(os.path.join(run, "fleet", "batch_%s" % prev, "_manifest.json")))
        code_start = max(mx_c + 1, int(pm.get("code_id_start") or 1))
        ptr_start = max(mx_p + 1, int(pm.get("pointer_id_start") or 1))
    inst = json.load(open(os.path.join(run, "_manifest.json"), encoding="utf-8")).get("instrument_dir")
    if not inst or not os.path.exists(os.path.join(inst, "newrun.py")):
        sys.exit("the instrument folder recorded in _manifest.json (%s) is not there; dispatch "
                 "needs it for the contracts and the renderer" % inst)
    sys.path.insert(0, inst)
    import newrun
    note = ("slice %s of %d: %d threads in corpus order, the first %s and the last %s, %d "
            "in-window items, hours %+.2f to %+.2f by first in-window item; %d openings of "
            "earlier slices' threads given as context, marked"
            % (want, len(gate["slices"]), sl["n_threads"], sl["first_thread"], sl["last_thread"],
               sl["items_in_window"], sl["start_hour"], sl["last_opening_hour"], n_ctx))
    rundir, man, stats = newrun.build_fleet(run, a.batch, tmp, a.model, code_start, ptr_start,
                                            note)
    os.remove(tmp)
    gate["coders"].append({"batch": want, "model": a.model, "dispatched_utc": now(),
                           "run_dir": os.path.relpath(rundir, run),
                           "code_id_start": code_start, "pointer_id_start": ptr_start,
                           "context_openings": n_ctx, "instrument_fingerprint":
                           man["instrument_fingerprint"]})
    json.dump(gate, open(gate_path, "w", encoding="utf-8"), indent=1)
    print("dispatched batch %s -> %s" % (want, os.path.relpath(rundir, run)))
    print("  %s" % note)
    print("  code ids from c%04d, pointer ids from p%04d" % (code_start, ptr_start))
    print("  rendered: %d items (%d in window), %d threads" % (stats["items"],
                                                              stats["items_in_window"],
                                                              stats["threads"]))
    return 0


# ---- redispatch ---------------------------------------------------------------------------
def redispatch(a):
    """v30. A coder that failed its slice (wrote against scope, stopped short, wrote outside
    its directory) is not repaired; its directory is set aside whole under fleet/_failed/ and
    the slice is dispatched again, to a fresh coder, with the same ids. Only the last dispatched
    batch can be redone, and only before it is collected: a collected batch is in the facts
    files the next coder read."""
    run = a.run
    gate_path = os.path.join(run, "out", "_gate.json")
    gate = json.load(open(gate_path, encoding="utf-8"))
    want = "%02d" % a.batch
    coders = gate["coders"]
    if not coders or coders[-1]["batch"] != want:
        sys.exit("only the last dispatched batch can be redispatched; the last is %s"
                 % (coders[-1]["batch"] if coders else "none"))
    if coders[-1].get("collected_utc"):
        sys.exit("batch %s was collected; its facts lines reached the next coder. Not redone."
                 % want)
    bdir = os.path.join(run, "fleet", "batch_%s" % want)
    failed = os.path.join(run, "fleet", "_failed")
    os.makedirs(failed, exist_ok=True)
    dst = os.path.join(failed, "batch_%s_%s" % (want, now().replace(":", "").replace("-", "")))
    if os.path.exists(bdir):
        shutil.move(bdir, dst)
    gate.setdefault("redispatched", []).append({"batch": want, "set_aside": os.path.relpath(dst, run),
                                                "was": coders[-1], "at": now()})
    gate["coders"] = coders[:-1]
    json.dump(gate, open(gate_path, "w", encoding="utf-8"), indent=1)
    print("batch %s set aside as %s" % (want, os.path.relpath(dst, run)))
    return dispatch(a)


# ---- collect ------------------------------------------------------------------------------
def collect(a):
    run = a.run
    gate_path = os.path.join(run, "out", "_gate.json")
    gate = json.load(open(gate_path, encoding="utf-8"))
    want = "%02d" % a.batch
    c = next((c for c in gate["coders"] if c["batch"] == want), None)
    if c is None:
        sys.exit("batch %s was not dispatched" % want)
    bdir = os.path.join(run, "fleet", "batch_%s" % want)
    if not os.path.exists(os.path.join(bdir, "out", "_journal.jsonl")):
        sys.exit("batch %s has no journal yet; it has not run" % want)
    if c.get("collected_utc") and not getattr(a, "force", False):
        sys.exit("batch %s was collected at %s; a second collect would append a second ledger "
                 "entry. Pass --force if the batch was re-run in place." % (want, c["collected_utc"]))
    added = {}
    for f in ("timeline.md", "lexicon.md"):
        src = os.path.join(bdir, f); dst = os.path.join(run, "out", f)
        before = open(dst, encoding="utf-8").read()
        after = open(src, encoding="utf-8").read()
        if not after.startswith(before.rstrip("\n")):
            print("NOTE: batch %s rewrote %s rather than appending to it; the lead's copy is "
                  "replaced and the difference is worth a look" % (want, f))
        new_lines = [l for l in after.splitlines() if l.strip() and l not in before.splitlines()]
        added[f] = new_lines
        with open(dst, "w", encoding="utf-8") as fo:
            fo.write(after)
    c["collected_utc"] = now()
    J = jl(os.path.join(bdir, "out", "_journal.jsonl"))
    nc = sum(1 for r in J if r.get("kind") == "code")
    c["codes"] = nc
    json.dump(gate, open(gate_path, "w", encoding="utf-8"), indent=1)
    ledger_entry(run, gate, want, bdir, J, added)
    print("collected batch %s: %d codes; timeline +%d lines, lexicon +%d lines -> out/; "
          "out/ledger.md extended" % (want, nc, len(added["timeline.md"]), len(added["lexicon.md"])))
    for f, ls in added.items():
        for l in ls:
            print("  %s: %s" % (f, l[:120]))
    return 0


def _section(md, title):
    """The text of a `## <title>` section of a markdown file, without its heading."""
    lines = md.splitlines()
    out, on = [], False
    for l in lines:
        if l.startswith("## "):
            if on:
                break
            on = l[3:].strip().lower().startswith(title.lower())
            continue
        if on:
            out.append(l)
    return "\n".join(out).strip()


def ledger_entry(run, gate, want, bdir, J, added):
    """v30: the lead's memory of the fleet, kept by the harness. One entry per collected batch:
    the slice, the counts, the facts lines added, the coder's final message if the scheduler
    saved it, and, from the coder's case and notes, every episode tagged [unresolved] or
    [inherited], the anomalies and the data problems, copied whole. The lead writes its strikes
    under the entry. A fork's fresh lead reads this file first."""
    sl = next((x for x in gate["slices"] if x["batch"] == want), {})
    disp = {}
    for r in J:
        if r.get("kind") == "thread":
            disp[r["rec"]["thread_id"]] = r["rec"].get("verdict")
    n_ptr = sum(1 for r in J if r.get("kind") == "pointer")
    n_code = sum(1 for r in J if r.get("kind") == "code")
    case = open(os.path.join(bdir, "out", "case.md"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(bdir, "out", "case.md")) else ""
    notes = open(os.path.join(bdir, "out", "notes.md"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(bdir, "out", "notes.md")) else ""
    fm_p = os.path.join(bdir, "out", "final_message.md")
    final = open(fm_p, encoding="utf-8").read().strip() if os.path.exists(fm_p) else "(not saved)"
    tagged = [l.strip() for l in case.splitlines() if "[unresolved]" in l or "[inherited]" in l]
    L = []
    L.append("## batch %s  hours %+.2f to %+.2f  threads %d  (collected %s)" % (
        want, sl.get("start_hour", 0), sl.get("last_opening_hour", 0), sl.get("n_threads", 0), now()))
    L.append("")
    L.append("- disposed %d: coded %d, out of scope %d; codes %d; pointers %d" % (
        len(disp), sum(1 for v in disp.values() if v == "coded"),
        sum(1 for v in disp.values() if v == "out_of_scope"), n_code, n_ptr))
    L.append("- coded threads: %s" % ", ".join(t for t, v in disp.items() if v == "coded") if any(v == "coded" for v in disp.values()) else "- coded threads: none")
    for f, ls in added.items():
        L.append("- %s +%d: %s" % (f, len(ls), " | ".join(l.strip()[:100] for l in ls) if ls else "nothing"))
    L.append("")
    L.append("**Coder's final message.** " + final.replace("\n", " ")[:2000])
    L.append("")
    L.append("**Episodes the coder tagged [unresolved] or [inherited]** (from its case.md):")
    L += (["- " + t[:300] for t in tagged] if tagged else ["- none tagged"])
    L.append("")
    for title in ("Anomalies and leads", "Data problems"):
        sec = _section(notes, title)
        L.append("**%s** (from its notes.md):" % title)
        L.append(sec if sec else "(section absent or empty)")
        L.append("")
    L.append("**Lead's strikes and remarks at collect:** (the lead writes here: which facts lines "
             "it struck and why, what it will carry to step 5; nothing else)")
    L.append("")
    lp = os.path.join(run, "out", "ledger.md")
    if not os.path.exists(lp):
        head = ("# ledger — r/%s\n\nThe case lead's memory of the fleet, kept by the harness at every "
                "`collect` and extended by the lead by hand under each entry. A fork's lead reads it "
                "first. Nothing here is a code or a citation; it is what each slice left open, what "
                "its coder flagged, and what the lead decided at the time.\n\n" % gate["sub"])
        open(lp, "w", encoding="utf-8").write(head)
    with open(lp, "a", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# ---- consolidate --------------------------------------------------------------------------
def consolidate(a):
    run = a.run
    gate_path = os.path.join(run, "out", "_gate.json")
    gate = json.load(open(gate_path, encoding="utf-8"))
    batches = sorted(c["batch"] for c in gate["coders"])
    if not batches:
        sys.exit("no coder has been dispatched")
    missing = [s["batch"] for s in gate["slices"] if s["batch"] not in batches]
    if missing and not a.partial:
        sys.exit("slices not yet coded: %s (--partial to consolidate what exists)" % missing)
    sys.path.insert(0, run)               # the run's own emit.py, as dispatched
    from emit import Emit
    pool_codes, pool_threads, pool_ptrs, journal = [], [], [], []
    seq = 0
    lead_journal = os.path.join(run, "out", "_journal.jsonl")
    lead_existing = jl(lead_journal)
    if any(r.get("kind") in ("code", "theme", "thread", "pointer") for r in lead_existing):
        sys.exit("REFUSING: the lead's out/_journal.jsonl already holds codes, themes, threads "
                 "or pointers; consolidation runs once, before the lead's step 4")
    for r in lead_existing:
        seq += 1
        r["seq"] = seq
        journal.append(r)
    report = []
    for b in batches:
        bdir = os.path.join(run, "fleet", "batch_%s" % b)
        bout = os.path.join(bdir, "out")
        if not os.path.exists(os.path.join(bout, "_journal.jsonl")):
            sys.exit("batch %s has no journal; it has not run" % b)
        if not next(c for c in gate["coders"] if c["batch"] == b).get("collected_utc"):
            sys.exit("batch %s has not been collected" % b)
        # the batch's own close: writes its four files from its journal, reconciles read=
        e = Emit(bout, corpus_path=os.path.join(bdir, "coder_corpus.jsonl"))
        try:
            e.close()
        except ValueError as ex:
            sys.exit("batch %s cannot be closed: %s. verify_room B2 should have caught this "
                     "at check --batch %s; nothing was consolidated." % (b, ex, b))
        codes, threads, ptrs = jl(os.path.join(bout, "codes.jsonl")), \
            jl(os.path.join(bout, "threads.jsonl")), jl(os.path.join(bout, "pointers.jsonl"))
        for name, rows in (("codes", codes), ("threads", threads), ("pointers", ptrs)):
            wjl(os.path.join(run, "staging", "%s_batch_%s.jsonl" % (name, b)), rows)
        rl = os.path.join(bout, "_read.jsonl")
        if os.path.exists(rl):
            shutil.copy2(rl, os.path.join(run, "staging", "read_batch_%s.jsonl" % b))
        pool_codes += codes; pool_threads += threads; pool_ptrs += ptrs
        for r in jl(os.path.join(bout, "_journal.jsonl")):
            if r.get("kind") in ("theme", "theme_add"):
                sys.exit("batch %s minted a theme; a fleet coder does not do step 4" % b)
            seq += 1
            r = dict(r); r["seq"] = seq; r["batch"] = b
            # a coder's stage marks and closes are the coder's: kept for the record, marked
            # so the lead's Emit does not adopt them as its own state (v30)
            if r.get("kind") in ("stage", "close"):
                r["kind"] = "coder_" + r["kind"]
            journal.append(r)
        report.append((b, len(codes), len(threads), len(ptrs)))
    # uniqueness across the pool
    ids = [c["code_id"] for c in pool_codes]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        sys.exit("code ids collide across batches: %s; the batches were not dispatched in "
                 "sequence" % dup[:10])
    tids = [t["thread_id"] for t in pool_threads]
    dupt = sorted({i for i in tids if tids.count(i) > 1})
    if dupt:
        sys.exit("threads disposed in two batches: %s" % dupt[:10])
    wjl(os.path.join(run, "package", "codes.jsonl"), pool_codes)
    wjl(os.path.join(run, "package", "threads.jsonl"), pool_threads)
    wjl(os.path.join(run, "package", "pointers.jsonl"), pool_ptrs)
    wjl(lead_journal, journal)
    gate["consolidated_utc"] = now()
    gate["pool"] = {"codes": len(pool_codes), "threads": len(pool_threads),
                    "pointers": len(pool_ptrs), "batches": batches}
    json.dump(gate, open(gate_path, "w", encoding="utf-8"), indent=1)
    codes_by_thread(run, gate, pool_codes)
    for b, nc, nt, np_ in report:
        print("  batch %s  codes %4d  threads %4d  pointers %3d" % (b, nc, nt, np_))
    print("pool: %d codes, %d threads, %d pointers -> package/; the lead's journal holds them; "
          "package/codes_by_thread.md written" % (len(pool_codes), len(pool_threads), len(pool_ptrs)))
    return 0


def codes_by_thread(run, gate, pool_codes):
    """v30: the pool in the shape step 4 reads it: every code's first-order line under its
    thread, threads in corpus order with their slice, hour and title, items with their hour.
    A lead reads this in passes, one per slice, and not codes.jsonl."""
    header, items = load_record(run)
    by, order = threads_in_order(items)
    rec = {r["id"]: r for r in items if "id" in r}
    slice_of = {t: s["batch"] for s in gate["slices"] for t in s["threads"]}
    codes = collections.defaultdict(list)
    for c in pool_codes:
        if not c.get("retracted"):
            codes[c.get("thread_id")].append(c)
    L = ["# codes by thread — r/%s" % gate["sub"],
         "# %d codes on %d threads, threads in corpus order (time of first in-window item); each code's"
         % (sum(len(v) for v in codes.values()), len(codes)),
         "# first-order line with its id, item and hour. Read one slice at a time for step 4.",
         "# Retracted codes are not here; the pool is package/codes.jsonl.", ""]
    cur = None
    for t in order:
        if t not in codes:
            continue
        b = slice_of.get(t, "?")
        if b != cur:
            cur = b
            sl = next((x for x in gate["slices"] if x["batch"] == b), {})
            L.append("")
            L.append("# ---- slice %s  hours %+.2f to %+.2f ----" % (b, sl.get("start_hour", 0), sl.get("last_opening_hour", 0)))
            L.append("")
        post = next((r for r in by[t] if r.get("kind") == "post"), None)
        title = " ".join((post.get("title") or "").split())[:140] if post else "[submission outside the record]"
        first = min((r.get("created_utc") or 0) for r in by[t] if not r.get("_context")) if any(not r.get("_context") for r in by[t]) else 0
        L.append("## %s  H%+.2f  %s  (%d codes)" % (t, (first - OPEN) / 3600.0, title, len(codes[t])))
        for c in sorted(codes[t], key=lambda c: (rec.get(c.get("item_id"), {}).get("created_utc") or 0, c["code_id"])):
            it = rec.get(c.get("item_id"), {})
            h = (it.get("created_utc") or 0)
            L.append("- %s  %s  H%+.2f  %s" % (c["code_id"], c.get("item_id"), (h - OPEN) / 3600.0 if h else 0,
                                            " ".join((c.get("first_order") or "").split())))
        L.append("")
    os.makedirs(os.path.join(run, "package"), exist_ok=True)
    open(os.path.join(run, "package", "codes_by_thread.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def status(a):
    gate_path = os.path.join(a.run, "out", "_gate.json")
    if not os.path.exists(gate_path):
        print("no gate yet: run plan"); return 0
    gate = json.load(open(gate_path, encoding="utf-8"))
    done = {c["batch"] for c in gate["coders"]}
    print("branch %s, %d slices, %d dispatched%s" % (gate["branch"], len(gate["slices"]), len(done),
          ", consolidated %s" % gate["consolidated_utc"] if gate.get("consolidated_utc") else ""))
    for s in gate["slices"]:
        b = s["batch"]
        j = os.path.join(a.run, "fleet", "batch_%s" % b, "out", "_journal.jsonl")
        n = sum(1 for r in jl(j) if r.get("kind") == "code") if os.path.exists(j) else None
        st = "not dispatched" if b not in done else ("dispatched, %s codes so far" % n)
        print("  batch %s  %s" % (b, st))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "dispatch", "redispatch", "collect", "consolidate",
                                    "status"])
    ap.add_argument("--run", default=".", help="the case lead's run directory")
    ap.add_argument("--threshold", type=int, default=500,
                    help="plan: items in the window above which the room is branch B")
    ap.add_argument("--budget", type=int, default=500,
                    help="plan: in-window items per slice, whole threads, never split")
    ap.add_argument("--floor", type=int, default=25,
                    help="plan: a slice below this many items folds into the slice before it")
    ap.add_argument("--batch", type=int, help="dispatch/redispatch/collect: the batch number")
    ap.add_argument("--model", help="dispatch/redispatch: the model id written into the manifest")
    ap.add_argument("--force", action="store_true",
                    help="plan: decide the gate again; collect: collect a batch a second time")
    ap.add_argument("--partial", action="store_true",
                    help="consolidate: pool the batches collected so far, for a test only")
    a = ap.parse_args()
    if a.cmd == "dispatch" and (a.batch is None or not a.model):
        sys.exit("dispatch needs --batch NN and --model <model id>")
    if a.cmd == "collect" and a.batch is None:
        sys.exit("collect needs --batch NN")
    if a.cmd == "redispatch" and (a.batch is None or not a.model):
        sys.exit("redispatch needs --batch NN and --model <model id>")
    return {"plan": plan, "dispatch": dispatch, "redispatch": redispatch, "collect": collect,
            "consolidate": consolidate, "status": status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
