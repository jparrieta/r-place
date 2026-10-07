#!/usr/bin/env python3
"""build_store.py, v38: stage 00, the joined store from the coders' documents.

    python3 tools/build_store.py --input RUN/INPUT/coders --root RUN [--rooms ROOMS.tsv]
    python3 tools/build_store.py --root RUN --join-canvas package/case_facts_outcome.jsonl
    python3 tools/build_store.py --root RUN --readme-only

Reads, per room in `<input>/ROOMS.tsv`, `<input>/rooms/<sub>/`, the files every room has:
brief.md, case.md, codes.jsonl, themes.jsonl, threads.jsonl, pointers.jsonl, window.json (the
window's thread and item counts) and `forest/` (forest.jsonl, tree_index.json, <sub>.md, one
renderer for every room). Any other file in a room folder is the handler's and is not read or
copied. Writes under --root:

    package/<sub>/                 the coder's documents, copied whole (brief.md, case.md,
                                   themes.jsonl, codes.jsonl, threads.jsonl, pointers.jsonl)
    package/forest.jsonl           every coded thread of every room as a tree
    package/tree_index.json        coordinate -> item, per room, with the header counts
    trees/<sub>.md                 the rendered forest
    package/store/codes.jsonl      every first-order concept, joined: second-order theme id, item,
                                   thread, author, hour since open, forest coordinate, state, the
                                   participant's words with offsets. Retracted concepts are not here.
    package/store/themes.jsonl     every second-order theme with its note, codes, items, threads, hours
    package/store/items.jsonl      every item of every coded thread (no body: the record's text
                                   stays with the record), with its codes, coordinate, state, meta
    package/store/threads.jsonl    every coded thread: opener, hours, depth, codes, themes, verdict
    package/store/rooms.jsonl      one line per room: the coder's run facts and the store counts
    package/store/pointers.jsonl   every pointer the coder wrote, as written (relations.py reads it)
    package/store/_unjoined.jsonl  every code whose item the forest does not hold
    package/store/_retracted.jsonl every retracted code, listed and dropped
    package/store/_build.json, README-store.md

Hard assertions: every code's theme_id names a theme of its room; a room's forest holds every
coded thread the codes name. A theme whose n_codes differs from the codes that name it is
reported, not fatal: n_codes_coder keeps the coder's figure and n_codes the store's count after
retraction. Deterministic. Nothing here reads a model or an assignment file; the store is built
once, before stage A1, and never rebuilt during a run.

The canvas (rule 7): no input file may carry a canvas field. The six fields are joined into
rooms.jsonl, and nowhere else, by --join-canvas after the build.
"""
import argparse, collections, json, os, shutil, sys

OPEN_UTC = 1490976000      # 2017-03-31 16:00:00 UTC, hour 0 of the window
FREEZE_UTC = OPEN_UTC + 73 * 3600
END_UTC = OPEN_UTC + 97 * 3600
CANVAS_FIELDS = ("canvas_entries", "canvas_area_px", "canvas_centre", "canvas_ring",
                 "canvas_artwork", "canvas_source")
LIMIT = "a reply is a reply: posted after, not caused by"
PROSE = ("brief.md", "case.md")
COPY_JSON = ("themes.jsonl", "codes.jsonl", "threads.jsonl", "pointers.jsonl")
CODE_KEEP = ("code_id", "theme_id", "first_order", "text", "start", "end", "item_id", "thread_id",
             "item_kind", "author", "created_utc", "batch", "discovered_at", "minted_in_stage",
             "exchange_id", "note", "passage_id")


def jl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def wjl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def hour(utc):
    return None if utc is None else round((utc - OPEN_UTC) / 3600.0, 2)


def walk(node, out):
    out.append(node)
    for c in node.get("children", []):
        walk(c, out)


def median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else round((xs[n // 2 - 1] + xs[n // 2]) / 2.0, 2)


def build_room(sub, D, S_forest, S_tree, fout):
    """One room. Returns (codes, themes, items, threads, room, pointers, unjoined, retracted)."""
    codes_all = jl(os.path.join(D, "codes.jsonl"))
    themes = jl(os.path.join(D, "themes.jsonl"))
    cthreads = {t["thread_id"]: t for t in jl(os.path.join(D, "threads.jsonl"))}
    pointers = jl(os.path.join(D, "pointers.jsonl"))
    wp = os.path.join(D, "window.json")
    window = json.load(open(wp)) if os.path.exists(wp) else {}
    for k in CANVAS_FIELDS:
        if k in window:
            sys.exit("rule 7: %s/window.json carries %s; the store will not be built" % (sub, k))
    forest = jl(os.path.join(D, "forest", "forest.jsonl"))
    tindex = json.load(open(os.path.join(D, "forest", "tree_index.json")))
    tindex = tindex.get(sub) or next(iter(tindex.values()))
    with open(os.path.join(D, "forest", "%s.md" % sub), encoding="utf-8") as fi, \
            open(os.path.join(S_tree, "%s.md" % sub), "w", encoding="utf-8") as fo:
        fo.write(fi.read())

    # --- retracted out, the join code -> theme ---------------------------------------------
    retracted = [dict(c, sub=sub) for c in codes_all if c.get("retracted")]
    codes = [c for c in codes_all if not c.get("retracted")]
    theme_by_id = {}
    for t in themes:
        if t["theme_id"] in theme_by_id:
            sys.exit("%s: two themes share theme_id %s" % (sub, t["theme_id"]))
        theme_by_id[t["theme_id"]] = t
    codes_by_theme = collections.defaultdict(list)
    for c in codes:
        if c.get("theme_id") not in theme_by_id:
            sys.exit("join failed: %s/%s names theme %r that themes.jsonl lacks"
                     % (sub, c["code_id"], c.get("theme_id")))
        codes_by_theme[c["theme_id"]].append(c["code_id"])
    all_by_theme = collections.Counter(c.get("theme_id") for c in codes_all)
    mismatches = [(t["theme_id"], t.get("n_codes"), all_by_theme.get(t["theme_id"], 0))
                  for t in themes if t.get("n_codes") != all_by_theme.get(t["theme_id"], 0)]

    # --- items and threads from the forest ---------------------------------------------------
    node_of = {}
    items, threads = [], []
    for th in forest:
        th = dict(th)
        th["sub"] = sub
        fout.write(json.dumps(th, ensure_ascii=False) + "\n")
        nodes = []
        walk(th["tree"], nodes)
        authors, coded_hours, depth = set(), [], 0
        root = th["tree"]
        for n in nodes:
            coord = n["coord"]
            d = 0 if coord == "0" else coord.count(".") + 1
            depth = max(depth, d)
            it = {"sub": sub, "thread_id": th["thread_id"], "item_id": n["item_id"],
                  "coord": coord, "parent_id": n.get("parent_id"), "author": n.get("author"),
                  "created_utc": n.get("created_utc"), "hour": hour(n.get("created_utc")),
                  "state": n.get("state"), "codes": n.get("code_ids", []),
                  "dt_parent_sec": n.get("dt_parent_sec"), "dt_thread_sec": n.get("dt_thread_sec"),
                  "collapsed_n": n.get("collapsed_n", 0), "coverage": n.get("coverage"),
                  "depth": d, "meta": n.get("meta") or {}}
            if it["created_utc"] is None:                 # forest nodes carry no utc; the index does
                ix = tindex.get("index", {}).get(th["thread_id"], {}).get(coord)
                if ix:
                    it["created_utc"] = ix.get("created_utc")
                    it["hour"] = hour(ix.get("created_utc"))
            items.append(it)
            node_of[n["item_id"]] = it
            if it["author"] not in (None, "[deleted]"):
                authors.add(it["author"])
            if it["codes"] and it["hour"] is not None:
                coded_hours.append(it["hour"])
        ct = cthreads.get(th["thread_id"], {})
        rmeta = root.get("meta") or {}
        code_ids = [cid for n in nodes for cid in n.get("code_ids", [])]
        threads.append({
            "sub": sub, "thread_id": th["thread_id"], "title": th.get("title"),
            "opener": root.get("author"), "opened_hour": th.get("hours_since_open"),
            "last_hour": max((i["hour"] for i in items if i["thread_id"] == th["thread_id"]
                              and i["hour"] is not None), default=None),
            "n_items": th.get("n_items"), "n_coded": th.get("n_coded"),
            "n_dropped": th.get("n_dropped"), "n_authors": len(authors), "depth": depth,
            "first_code_hour": min(coded_hours) if coded_hours else None,
            "last_code_hour": max(coded_hours) if coded_hours else None,
            "codes": code_ids,
            "themes": sorted({theme_by_id[c["theme_id"]]["theme_id"] for c in codes
                              if c["code_id"] in set(code_ids)}),
            "read": ct.get("read"), "verdict": ct.get("verdict"), "reason": ct.get("reason"),
            "batch": ct.get("batch"),
            "op_score": rmeta.get("score"), "op_stickied": bool(rmeta.get("stickied")),
            "op_distinguished": rmeta.get("distinguished"), "op_flair": rmeta.get("link_flair_text"),
            "retrieved_on": th.get("retrieved_on")})
    coded_thread_ids = {t["thread_id"] for t in threads}
    missing = sorted({c["thread_id"] for c in codes} - coded_thread_ids)
    if missing:   # the record holds no such thread: its codes are kept and listed as unjoined
        print("%s: the forest lacks coded threads %s; their codes go to _unjoined.jsonl" % (sub, missing[:5]))

    # --- codes ---------------------------------------------------------------------------------
    code_rows, unjoined = [], []
    for c in codes:
        it = node_of.get(c["item_id"])
        if it is None:
            unjoined.append({"sub": sub, "code_id": c["code_id"], "item_id": c["item_id"],
                             "thread_id": c["thread_id"], "why": "the forest holds no such item"})
        row = {"sub": sub}
        row.update({k: c.get(k) for k in CODE_KEEP})
        row.update({"hour": hour(c.get("created_utc")),
                    "coord": it["coord"] if it else None,
                    "state": it["state"] if it else "unjoined",
                    "second_order": theme_by_id[c["theme_id"]].get("second_order")})
        code_rows.append(row)
    by_id = {r["code_id"]: r for r in code_rows}
    theme_rows = []
    for t in themes:
        ids = codes_by_theme.get(t["theme_id"], [])
        rows = [by_id[i] for i in ids]
        hrs = [r["hour"] for r in rows if r["hour"] is not None]
        theme_rows.append({"sub": sub, "theme_id": t["theme_id"], "second_order": t.get("second_order"),
                           "theme_note": t.get("theme_note"), "n_codes": len(ids),
                           "n_codes_coder": t.get("n_codes"), "code_ids": ids,
                           "items": sorted({r["item_id"] for r in rows}),
                           "threads": sorted({r["thread_id"] for r in rows if r["thread_id"]}),
                           "first_hour": min(hrs) if hrs else None,
                           "last_hour": max(hrs) if hrs else None,
                           "regrouped_from": t.get("regrouped_from")})

    # --- the room ------------------------------------------------------------------------------
    hrs = sorted(r["hour"] for r in code_rows if r["hour"] is not None)
    auth = collections.Counter(r["author"] for r in code_rows
                               if r["author"] not in (None, "[deleted]"))
    ntot = sum(auth.values())
    counts = tindex.get("counts", {})
    disp = list(cthreads.values())
    room = {
        "sub": sub,
        "threads_total": window.get("threads_in_window") or counts.get("threads_total_in_window"),
        "items_in_window": window.get("items_in_window"),
        "threads_disposed": len(disp),
        "threads_read_in_full": sum(1 for t in disp if t.get("read") == "full"),
        "threads_triaged": sum(1 for t in disp if t.get("read") == "triaged"),
        "threads_out_of_scope": sum(1 for t in disp if t.get("verdict") == "out_of_scope"),
        "threads_coded": len(threads),
        "threads_in_store": len(threads), "items_in_store": len(items),
        "items_coded": sum(1 for i in items if i["codes"]),
        "codes": len(code_rows), "codes_retracted": len(retracted), "themes": len(theme_rows),
        "pointers": len(pointers),
        "n_subreddits_named": len({(p.get("normalised") or "").lower() for p in pointers
                                   if p.get("kind") == "subreddit"}),
        "n_off_platform": sum(1 for p in pointers if p.get("kind") == "off_platform"),
        "onset_first_code_hour": hrs[0] if hrs else None,
        "onset_median_code_hour": median(hrs), "onset_last_code_hour": hrs[-1] if hrs else None,
        "coded_authors": len(auth),
        "top1_share": round(auth.most_common(1)[0][1] / ntot, 3) if ntot else None,
        "herfindahl": round(sum((v / ntot) ** 2 for v in auth.values()), 3) if ntot else None,
        "n_named_neighbours": len({p.get("normalised") for p in pointers
                                   if p.get("kind") == "subreddit"}),
        "forest": counts, "brief": os.path.exists(os.path.join(D, "brief.md")),
        "n_codes_mismatch_themes": len(mismatches),
    }
    room["thread_coded_share"] = (round(len(threads) / room["threads_total"], 3)
                                  if room["threads_total"] else None)
    room["item_coded_share"] = (round(room["items_coded"] / room["items_in_window"], 3)
                                if room["items_in_window"] else None)
    for p in pointers:
        p["sub"] = sub
    return code_rows, theme_rows, items, threads, room, pointers, unjoined, retracted, mismatches


def join_canvas(R, outcome_path):
    S = os.path.join(R, "package", "store")
    rp = os.path.join(S, "rooms.jsonl")
    if not os.path.exists(rp):
        sys.exit("no %s to join into; build the store first" % rp)
    if not os.path.exists(outcome_path) and os.path.exists(os.path.join(R, outcome_path)):
        outcome_path = os.path.join(R, outcome_path)      # a path relative to --root
    if not os.path.exists(outcome_path):
        sys.exit("no such outcome file: %s (nor under %s)" % (outcome_path, R))
    out = {r["sub"]: r for r in jl(outcome_path)}
    rooms = jl(rp)
    joined = missing = 0
    for r in rooms:
        o = out.get(r["sub"])
        if o is None:
            missing += 1
            for k in CANVAS_FIELDS:
                r[k] = None
            continue
        for k in CANVAS_FIELDS:
            r[k] = o.get(k)
        joined += 1
    wjl(rp, rooms)
    bp = os.path.join(S, "_build.json")
    b = json.load(open(bp)) if os.path.exists(bp) else {}
    b["canvas"] = {"joined_from": os.path.relpath(outcome_path, R), "rooms_joined": joined,
                   "rooms_without_outcome_line": missing, "fields": list(CANVAS_FIELDS)}
    with open(bp, "w") as f:
        json.dump(b, f, indent=1, ensure_ascii=False)
    write_readme(R, b)
    print("canvas joined into rooms.jsonl: %d rooms, %d without an outcome line (six nulls)"
          % (joined, missing))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=None, help="RUN/INPUT/coders")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rooms", default=None, help="ROOMS.tsv (default <input>/ROOMS.tsv)")
    ap.add_argument("--only", default=None, help="comma-separated subs, for a test build")
    ap.add_argument("--readme-only", action="store_true")
    ap.add_argument("--join-canvas", default=None, metavar="OUTCOME_JSONL")
    ap.add_argument("--frame-date", default=None, help="the copy date (default today)")
    a = ap.parse_args()
    R = a.root
    P = os.path.join(R, "package")
    S = os.path.join(P, "store")
    T = os.path.join(R, "trees")
    os.makedirs(S, exist_ok=True)
    os.makedirs(T, exist_ok=True)
    if a.readme_only:
        write_readme(R, json.load(open(os.path.join(S, "_build.json"))))
        return 0
    if a.join_canvas:
        return join_canvas(R, a.join_canvas)
    if not a.input:
        sys.exit("--input is required for a build")
    rooms_tsv = a.rooms or os.path.join(a.input, "ROOMS.tsv")
    subs = [l.split("\t")[0] for l in open(rooms_tsv, encoding="utf-8").read().splitlines()[1:]
            if l.strip()]
    if a.only:
        want = set(a.only.split(","))
        subs = [s for s in subs if s in want]
    subs = sorted(subs)

    codes, themes, items, threads, rooms, pointers, unjoined, retracted = ([] for _ in range(8))
    mism = {}
    index_all = {}
    with open(os.path.join(P, "forest.jsonl"), "w", encoding="utf-8") as fout:
        for sub in subs:
            D = os.path.join(a.input, "rooms", sub)
            if not os.path.isdir(D):
                sys.exit("no such room directory: %s" % D)
            # the coder's documents, copied whole
            dst = os.path.join(P, sub)
            os.makedirs(dst, exist_ok=True)
            for f in PROSE + COPY_JSON:
                src = os.path.join(D, f)
                if os.path.exists(src):
                    shutil.copyfile(src, os.path.join(dst, f))
            c, t, i, th, r, p, u, rt, mm = build_room(sub, D, P, T, fout)
            codes += c; themes += t; items += i; threads += th; rooms.append(r)
            pointers += p; unjoined += u; retracted += rt
            if mm:
                mism[sub] = mm
            ti = json.load(open(os.path.join(D, "forest", "tree_index.json")))
            index_all[sub] = ti.get(sub) or next(iter(ti.values()))
    with open(os.path.join(P, "tree_index.json"), "w", encoding="utf-8") as f:
        json.dump(index_all, f, ensure_ascii=False)

    wjl(os.path.join(S, "codes.jsonl"), codes)
    wjl(os.path.join(S, "themes.jsonl"), themes)
    wjl(os.path.join(S, "items.jsonl"), items)
    wjl(os.path.join(S, "threads.jsonl"), threads)
    wjl(os.path.join(S, "rooms.jsonl"), rooms)
    wjl(os.path.join(S, "pointers.jsonl"), pointers)
    wjl(os.path.join(S, "_unjoined.jsonl"), unjoined)
    wjl(os.path.join(S, "_retracted.jsonl"), retracted)
    build = {
        "input": os.path.relpath(a.input, R), "rooms_tsv": os.path.relpath(rooms_tsv, R),
        "communities": len(subs), "codes": len(codes), "codes_retracted_dropped": len(retracted),
        "themes": len(themes), "threads": len(threads), "items": len(items),
        "items_coded": sum(1 for i in items if i["codes"]),
        "items_bridge": sum(1 for i in items if i["state"] == "bridge"),
        "items_removed": sum(1 for i in items if i["state"] == "removed"),
        "items_dropped": sum(1 for i in items if i["state"] == "dropped"),
        "pointers": len(pointers), "codes_unjoined": len(unjoined),
        "codes_unjoined_by_sub": dict(collections.Counter(u["sub"] for u in unjoined)),
        "themes_n_codes_mismatch": {s: [list(x) for x in v] for s, v in mism.items()},
        "briefs": sum(1 for r in rooms if r["brief"]),
        "open_utc": OPEN_UTC, "freeze_utc": FREEZE_UTC, "end_utc": END_UTC,
    }
    with open(os.path.join(S, "_build.json"), "w") as f:
        json.dump(build, f, indent=1, ensure_ascii=False)
    # the frame: date, count, and one hash over every room's six files and forest, in sorted order
    import hashlib, datetime
    h = hashlib.sha256()
    for sub in subs:
        D = os.path.join(a.input, "rooms", sub)
        for f in PROSE + COPY_JSON + ("forest/forest.jsonl",):
            fp = os.path.join(D, f)
            if os.path.exists(fp):
                h.update(("%s/%s\n" % (sub, f)).encode()); h.update(open(fp, "rb").read())
    frame_date = a.frame_date or datetime.date.today().isoformat()
    with open(os.path.join(P, "FRAME.md"), "w", encoding="utf-8") as f:
        f.write("# The frame\n\nCopy date: %s. Rooms: %d. Hash (sha256 over each room's six files and "
                "forest, rooms in sorted order): `%s`.\n\nThe rooms are those whose coding had finished "
                "by the copy date, of a population of 706 (contract §5; the census names the rooms not coded). The list is `store/rooms.jsonl`.\n"
                % (frame_date, len(subs), h.hexdigest()))
    build["frame"] = {"date": frame_date, "rooms": len(subs), "sha256": h.hexdigest()}
    with open(os.path.join(S, "_build.json"), "w") as f:
        json.dump(build, f, indent=1, ensure_ascii=False)
    write_readme(R, build)
    for k in ("communities", "codes", "codes_retracted_dropped", "themes", "threads", "items",
              "items_coded", "items_bridge", "items_dropped", "pointers", "codes_unjoined",
              "briefs"):
        print("%-24s %s" % (k, build[k]))
    if mism:
        print("themes whose coder n_codes differs from the codes naming them: %d rooms (see _build.json)"
              % len(mism))
    print("store written to %s" % S)
    return 0


def write_readme(R, b):
    S = os.path.join(R, "package", "store")
    canvas = ("joined: %d rooms, %d with six nulls" % (b["canvas"]["rooms_joined"],
                                                       b["canvas"]["rooms_without_outcome_line"])
              if b.get("canvas") else "not yet joined")
    txt = """# The store: what each file is, and what none of them is

Built by `tools/build_store.py` at stage 00 from the coders' documents, one run per room.
Read-only: nothing in a run
rewrites it. `tools/mem.py` reads it one page at a time and overlays your own tier files from
`out/` at query time, so a placement, fourth-order theme or dimension shown by `mem.py` is always
the current one.

**The clock.** `hour` is hours since the canvas opened, %(open_utc)d UTC (2017-03-31 16:00).
Placement stopped at hour 73; the window ends at 97. Negative hours are the pre-event week. Hour 0 is when the canvas opened; the placement record also holds Reddit's tests before the opening, from about hour -16, made while the canvas was closed to users (J, 2026-10-07).

**The limit that holds on every row that has a parent.** %(limit)s. An interval between two
posts is elapsed time, never the speed of a decision.

## Files

| file | one line per | keys |
|---|---|---|
| `codes.jsonl` | first-order concept (%(codes)d; %(codes_retracted_dropped)d retracted by the coder and dropped) | `sub`, `code_id`, `theme_id`, `second_order`, `first_order`, `text` (the participant's words), `start`, `end`, `item_id`, `thread_id`, `item_kind`, `author`, `created_utc`, `hour`, `coord` (forest coordinate), `state` (coded / unjoined), `batch`, `discovered_at`, `minted_in_stage`, `exchange_id`, `note` |
| `themes.jsonl` | second-order theme (%(themes)d) | `sub`, `theme_id`, `second_order`, `theme_note`, `n_codes` (after retraction), `n_codes_coder`, `code_ids`, `items`, `threads`, `first_hour`, `last_hour`, `regrouped_from` |
| `items.jsonl` | item of a coded thread (%(items)d; no body) | `sub`, `thread_id`, `item_id`, `coord`, `parent_id`, `author`, `created_utc`, `hour`, `state` (coded / bridge / removed / dropped), `codes`, `dt_parent_sec`, `dt_thread_sec`, `depth`, `meta` |
| `threads.jsonl` | coded thread (%(threads)d) | `sub`, `thread_id`, `title`, `opener`, `opened_hour`, `last_hour`, `n_items`, `n_coded`, `n_dropped`, `n_authors`, `depth`, `first_code_hour`, `last_code_hour`, `codes`, `themes`, `read`, `verdict`, `reason` (the coder's disposition), `op_score`, `op_stickied`, `op_distinguished`, `op_flair` |
| `rooms.jsonl` | room (%(communities)d) | the window (`threads_total`, `items_in_window`), the coder's dispositions (`threads_disposed`, `threads_read_in_full`, `threads_triaged`, `threads_out_of_scope`, `threads_coded`), `n_subreddits_named`, `n_off_platform`, the store counts, the onset hours, `coded_authors`, `top1_share`, `herfindahl`, `n_named_neighbours`, `forest` (the header counts); and, once the build joins them, the six canvas fields (%(canvas)s) |
| `pointers.jsonl` | pointer the coder wrote (%(pointers)d) | as written, plus `sub`; `relations.py` builds the mention graph from it |
| `transitions.jsonl` | coded turn answering a coded turn | written by `tools/transitions.py` |
| `_unjoined.jsonl` | code whose item the forest does not hold (%(codes_unjoined)d) | `sub`, `code_id`, `item_id`, `thread_id` |
| `_retracted.jsonl` | code the coder retracted (%(codes_retracted_dropped)d) | the line as the coder wrote it; not in `codes.jsonl` |

## What the record holds, and what it does not

The threads here are **the threads the coders' codes point at**, with every item of each such
thread (%(items)d items in %(threads)d threads), but not their text: the participant's words the
store carries are the coded passages (`codes.jsonl`: `text`, `start`, `end`), and `cite.py` quotes
from them. `rooms.jsonl` carries `threads_total` and `items_in_window` for the whole window and
the forest header of every `trees/<sub>.md` repeats the counts. The coder's own documents are in
`package/<sub>/`: the pre-event brief (%(briefs)d present), the case account, and the codes,
themes, thread dispositions and pointers as the coder wrote them. A pointer with `relation` null
was named in the case account and carries no relation label.

`meta` on an item: `score` (kept at 0 and below), `distinguished`, `stickied`, `edited`,
`link_flair_text`, `author_flair_text`, `retrieved_on`. The score and `stickied` are snapshots
taken at retrieval, weeks after the event: lower bounds with no timing. `distinguished` is reliable.

## What is not here

No canvas field outside `rooms.jsonl` (rule 7: joined there by `--join-canvas`, shown by `mem.py
room`, withheld by `--no-canvas`; a use is declared, rule 7). No third-order theme, fourth-order theme or
dimension: those are yours, in `out/`, and `mem.py` joins them for you. No item body. No
interpretation.
""" % {"open_utc": b["open_utc"], "limit": LIMIT, "codes": b["codes"], "canvas": canvas,
       "codes_retracted_dropped": b["codes_retracted_dropped"], "themes": b["themes"],
       "items": b["items"], "threads": b["threads"], "communities": b["communities"],
       "briefs": b["briefs"], "codes_unjoined": b["codes_unjoined"], "pointers": b["pointers"]}
    for extra in ("_README-transitions.md", "_README-relations.md", "_README-neighbours.md"):
        p = os.path.join(S, extra)
        if os.path.exists(p):
            txt += "\n" + open(p, encoding="utf-8").read()
    with open(os.path.join(S, "README-store.md"), "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    sys.exit(main())
