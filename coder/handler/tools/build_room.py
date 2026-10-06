#!/usr/bin/env python3
"""build_room.py — make one room of the yard from a raw24 collection.

    python3 build_room.py --sub <sub> --raw <raw24/<sub>.jsonl> --out rooms/<sub> \
        --instrument _instrument/v32 [--brief <brief.md> --brief-source "<where it came from>"]

Writes:
    rooms/<sub>/instrument/                 the selected instrument, whole
    rooms/<sub>/record/coder_corpus.jsonl.gz    the 97-hour cut, threads whole, context marked
    rooms/<sub>/record/preweek.jsonl.gz     the seven days before the canvas, for the brief writer
    rooms/<sub>/record/cut_stats.json       the counts the gate will read, computed here too
    rooms/<sub>/record/openings.md          the openings file the lead reads (plus titles and
                                            digest files above 1,500 threads)
    rooms/<sub>/brief/out/brief.md          only when --brief is given (an existing brief)
    rooms/<sub>/STATE.json, ROOM.md

Idempotent: a room whose STATE.json says built is skipped unless --force.
"""
import argparse, collections, datetime, gzip, importlib, json, os, re, shutil, sys

OPEN = 1490976000
FRZ = 1491238800
END = FRZ + 24 * 3600
PRE = OPEN - 7 * 86400


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stream_cut(CW, inp, outp):
    """cut_window_v30.cut(), in two passes over the file so that a raw24 collection of
    hundreds of megabytes does not have to sit in memory whole. Same output, byte for byte:
    the same header, the same items in the same order with the same marks."""
    keep = set()
    with open(inp, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if "id" in r and CW.OPEN <= r.get("created_utc", 0) <= CW.END:
                keep.add(CW.thread_of(r))
    n_threads_in = set()
    n_items_in = 0
    kept, ctx_before, ctx_after = [], 0, 0
    with open(inp, encoding="utf-8") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if "id" not in r:
                continue
            n_items_in += 1
            t = CW.thread_of(r)
            n_threads_in.add(t)
            if t not in keep:
                continue
            if r["created_utc"] < CW.OPEN:
                r["_context"] = True; ctx_before += 1
            elif r["created_utc"] > CW.END:
                r["_context"] = True; ctx_after += 1
            else:
                r.pop("_context", None)
            kept.append(r)
    kept.sort(key=lambda r: (r["created_utc"], r["id"]))
    bysize = collections.defaultdict(lambda: [0, 0])
    for r in kept:
        if r.get("_context"):
            continue
        e = bysize[CW.thread_of(r)]
        e[0] += 1
        e[1] += len(CW.body(r) or "")
    total = sum(v[1] for v in bysize.values()) or 1
    order = sorted(bysize.items(), key=lambda kv: -kv[1][1])
    index, cum = [], 0
    for rank, (tid, (n, c)) in enumerate(order, 1):
        cum += c
        index.append({"thread_id": tid, "index_rank": rank, "items": n,
                      "chars": c, "cum_text_share": round(cum / total, 4)})
    header = {"_thread_index": index, "_n_threads": len(bysize),
              "_n_items": sum(1 for r in kept if not r.get("_context")),
              "_n_context_items": ctx_before + ctx_after,
              "_n_context_before": ctx_before, "_n_context_after": ctx_after,
              "_window_utc": CW.LABEL, "_window_revision": CW.WINDOW_REVISION, "_cut": CW.VERSION}
    with open(outp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(header, ensure_ascii=False) + "\n")
        for r in kept:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {"threads_in": len(n_threads_in), "threads_kept": len(bysize),
            "threads_dropped": len(n_threads_in) - len(keep), "items_in": n_items_in,
            "items_kept": len(kept), "items_in_window": header["_n_items"],
            "context_before": ctx_before, "context_after": ctx_after}


def is_bot(r):
    a = (r.get("author") or "").lower()
    return a == "automoderator" or a.endswith("bot")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sub", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--brief")
    ap.add_argument("--brief-source", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    room = os.path.abspath(a.out)
    sp = os.path.join(room, "STATE.json")
    if os.path.exists(sp) and not a.force:
        st = json.load(open(sp))
        if st.get("built"):
            print("skip", a.sub, "(built)")
            return 0
    os.makedirs(os.path.join(room, "record"), exist_ok=True)
    inst = os.path.abspath(a.instrument)
    sys.path.insert(0, inst)
    version = os.path.basename(inst.rstrip(os.sep))
    if not re.fullmatch(r"v\d+", version):
        raise SystemExit("instrument directory must end in v<integer>: %s" % inst)
    CW = importlib.import_module("cut_window_%s" % version)
    tmp = os.path.join(room, "record", "coder_corpus.jsonl")
    stats = stream_cut(CW, a.raw, tmp)
    # counts the gate reads (as newrun computes them): in-window items, by people, chars
    n_in = n_people = chars = 0
    threads = set()
    with open(tmp, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if "id" not in r or r.get("_context"):
                continue
            n_in += 1
            threads.add(r["id"] if r.get("kind") == "post" else (r.get("link_id") or "?")[3:])
            if not is_bot(r):
                n_people += 1
                chars += len(r.get("body") or r.get("selftext") or "")
    RO = importlib.import_module("render_openings_%s" % version)
    ost = RO.write(tmp, a.sub, os.path.join(room, "record"))
    with open(tmp, "rb") as f, gzip.open(tmp + ".gz", "wb", compresslevel=6) as g:
        shutil.copyfileobj(f, g)
    os.remove(tmp)
    # the pre-week
    pre_n = 0
    pre_p = os.path.join(room, "record", "preweek.jsonl.gz")
    with open(a.raw, encoding="utf-8") as fh, gzip.open(pre_p, "wt", encoding="utf-8", compresslevel=6) as g:
        for line in fh:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if "id" in r and PRE <= r.get("created_utc", 0) < OPEN:
                g.write(line if line.endswith("\n") else line + "\n")
                pre_n += 1
    cs = {"sub": a.sub, "cut": stats, "openings": ost, "items_in_window": n_in, "items_by_people": n_people,
          "chars_by_people": chars, "threads_in_window": len(threads), "preweek_items": pre_n,
          "window_utc": ["2017-03-31 16:00", "2017-04-04 17:00"], "built": now()}
    json.dump(cs, open(os.path.join(room, "record", "cut_stats.json"), "w"), indent=1)
    # the instrument
    idst = os.path.join(room, "instrument")
    if os.path.exists(idst):
        shutil.rmtree(idst)
    shutil.copytree(inst, idst, ignore=shutil.ignore_patterns("__pycache__"))
    # an existing brief
    brief = "to write"
    if a.brief and os.path.exists(a.brief):
        bo = os.path.join(room, "brief", "out")
        os.makedirs(bo, exist_ok=True)
        shutil.copy2(a.brief, os.path.join(bo, "brief.md"))
        json.dump({"sub": a.sub, "brief": "existing: %s" % (a.brief_source or "earlier run"),
                   "copied": now()}, open(os.path.join(room, "brief", "_manifest.json"), "w"), indent=1)
        brief = "existing: %s" % (a.brief_source or "earlier run")
    st = {"sub": a.sub, "built": now(), "instrument": version,
          "items_in_window": n_in, "items_by_people": n_people, "chars_by_people": chars,
          "threads": len(threads), "preweek_items": pre_n, "brief": brief,
          "expected_branch": "B" if n_in > 500 else "A",
          "expected_slices": max(1, -(-n_in // 500)) if n_in > 500 else 1,
          "stage": "new" if brief != "to write" else "brief to write", "log": [], "notes": []}
    json.dump(st, open(sp, "w"), indent=1)
    open(os.path.join(room, "ROOM.md"), "w", encoding="utf-8").write(ROOM_MD.format(
        sub=a.sub, n_in=n_in, threads=len(threads), chars=chars, pre=pre_n, brief=brief,
        instrument=version,
        branch=st["expected_branch"], slices=st["expected_slices"]))
    print("built", a.sub, "items", n_in, "threads", len(threads), "pre", pre_n, "brief", brief)
    return 0


ROOM_MD = """# r/{sub}

| | |
|---|---|
| items in the 97-hour window | {n_in} |
| threads with an in-window item | {threads} |
| chars of people's text in window | {chars} |
| items in the seven days before | {pre} |
| brief | {brief} |
| expected branch at threshold 500 | {branch}, about {slices} slice(s) |

What is here: `instrument/` ({instrument}, whole), `record/coder_corpus.jsonl.gz` (the cut the coders
read; `run/` is built from it), `record/openings.md` (every thread's metadata, counts, title
and opening text: what the case lead reads first), `record/preweek.jsonl.gz` (what the brief
writer reads),
`brief/` (the brief stage; `brief/out/brief.md` when one exists), and once started `run/`,
`snapshots/`, `forks/`. `STATE.json` is the room's memory; `room.py status` reads the files and
rewrites it.

To run this room, from this directory (`T` is `../../_tools/room.py`):

    python3 $T status
    python3 $T brief --model <id>          # only if the brief is to write; then launch the
    python3 $T message brief               #   brief writer with this message; then `check`
    python3 $T run --model <id>            # builds run/ from the record and the brief
    python3 $T message lead                # launch the case lead with this message
    python3 $T message coder --batch 01    # branch B: launch each coder with this, in turn
    python3 $T check --batch 01            # after each coder, before the lead collects
    python3 $T message collect --batch 01 --summary "..."   # to the lead
    python3 $T snapshot after-fleet        # when the last coder is collected (the fork point)
    python3 $T message finish --batch NN   # the lead's step 4 and 5, or:
    python3 $T fork <name>; python3 $T message fork --fork <name>
    python3 $T check                       # when the lead has closed

`../../CONTRACT-scheduler.md` says what the scheduler does between these commands and what it
looks for. `../../README.md` says how to do it in Claude Code or any other agent runner.
"""

if __name__ == "__main__":
    sys.exit(main())
