#!/usr/bin/env python3
"""test_verbs.py: the analyst's verbs over a small self-contained store, one assertion per behaviour.

    python3 tools/tests/test_verbs.py              # builds its own three-room store in a temp folder
    python3 tools/tests/test_verbs.py --run RUN    # also smoke-tests the verbs on a copy of a real run
                                                   # (RUN holds package/ and trees/), with a fake canvas

Each check prints ok or FAIL with the output that failed it; exit 1 if any failed. Stdlib only.
"""
import json, os, shutil, subprocess, sys, tempfile

T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # tools/
INS = os.path.dirname(T)
PY = sys.executable
FAILS = []


def run(tool, *args, cwd):
    r = subprocess.run([PY, os.path.join(T, tool)] + [str(a) for a in args], cwd=cwd,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def check(name, cond, got=""):
    print("%-4s %s" % ("ok" if cond else "FAIL", name))
    if not cond:
        FAILS.append(name)
        print("     " + "\n     ".join(str(got).splitlines()[:12]))


def mem(*a, cwd):
    return run("mem.py", *a, cwd=cwd)


def wjl(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def w(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def build(root):
    """Three rooms: denmark and sweden coded, armenia with one theme; items, threads, a forest, a
    canvas, pointers, transitions; out/ with notes, a diary, a working scheme and views."""
    S = os.path.join(root, "package", "store")
    rooms = []
    for i, (sub, n) in enumerate((("denmark", 6), ("sweden", 4), ("armenia", 2))):
        rooms.append({"sub": sub, "threads_total": 10 + i, "threads_coded": 2, "items_in_store": n * 2,
                      "items_coded": n, "codes": n, "themes": 2 if n > 2 else 1, "items_in_window": None if sub == "armenia" else 100 * (i + 1),
                      "onset_first_code_hour": 2.0 + i, "coded_authors": n, "top1_share": 0.2,
                      "n_subreddits_named": 2, "n_off_platform": i,
                      "forest": {"coverage_of_coded_items": 0.5 + 0.1 * i},
                      "canvas_entries": None if sub == "armenia" else 1,
                      "canvas_area_px": None if sub == "armenia" else 300 + i,
                      "canvas_centre": None if sub == "armenia" else [10, 20],
                      "canvas_ring": None if sub == "armenia" else "centre",
                      "canvas_artwork": None if sub == "armenia" else "%s flag" % sub,
                      "canvas_source": None if sub == "armenia" else "placeAtlas 2017"})
    wjl(os.path.join(S, "rooms.jsonl"), rooms)
    codes, items, themes, threads, trans = [], [], [], [], []
    labels = {"denmark": ["calling for hands on the flag", "defending the flag border"],
              "sweden": ["making the Swedish flag", "a truce with Denmark"], "armenia": ["hearts and flags"]}
    for sub, n in (("denmark", 6), ("sweden", 4), ("armenia", 2)):
        th = "%s1" % sub[:2]
        threads.append({"sub": sub, "thread_id": th, "title": "the %s thread" % sub, "opener": "op",
                        "opened_hour": 1.0, "n_items": n + 1, "n_coded": n, "depth": 2})
        items.append({"sub": sub, "thread_id": th, "item_id": th, "coord": "0", "parent_id": None,
                      "author": "op", "created_utc": 1000, "hour": 1.0, "state": "dropped", "codes": []})
        for k in range(n):
            cid = "c%04d" % (k + 1)
            tid = "t%02d" % (1 + k % len(labels[sub]))
            iid = "%s-i%d" % (sub, k)
            parent = th if k == 0 else "%s-i%d" % (sub, k - 1)
            items.append({"sub": sub, "thread_id": th, "item_id": iid, "coord": "0" + ".1" * (k + 1),
                          "parent_id": parent, "author": "a%d" % k, "created_utc": 2000 + k * 3600,
                          "hour": 2.0 + 10 * k, "state": "coded", "codes": [cid]})
            codes.append({"sub": sub, "code_id": cid, "theme_id": tid, "first_order": "%s label %d" % (labels[sub][int(tid[1:]) - 1], k),
                          "text": "we place the %s flag number %d" % (sub, k), "item_id": iid, "thread_id": th,
                          "author": "a%d" % k, "hour": 2.0 + 10 * k, "coord": "0" + ".1" * (k + 1),
                          "note": "coder note %d" % k})
            if k:
                trans.append({"id": "%s:%d" % (th, k), "sub": sub, "thread_id": th,
                              "from_codes": ["c%04d" % k], "to_codes": [cid],
                              "from_case_themes": ["t%02d" % (1 + (k - 1) % len(labels[sub]))], "to_case_themes": [tid],
                              "same_author": False, "interval_s": 3600.0, "hops": 1,
                              "limit": "a reply is a reply: posted after, not caused by"})
        for j, lab in enumerate(labels[sub], 1):
            tid = "t%02d" % j
            themes.append({"sub": sub, "theme_id": tid, "second_order": lab, "theme_note": "note on %s" % lab,
                           "n_codes": sum(1 for c in codes if c["sub"] == sub and c["theme_id"] == tid),
                           "code_ids": [c["code_id"] for c in codes if c["sub"] == sub and c["theme_id"] == tid],
                           "threads": [th], "first_hour": 2.0, "last_hour": 50.0})
        w(os.path.join(root, "package", sub, "case.md"), "# case of %s\n" % sub + "".join("line %d of the case\n" % i for i in range(1, 121)))
        w(os.path.join(root, "package", sub, "brief.md"), "# brief of %s\n" % sub)
        forest = ["# forest of %s" % sub, "=== THREAD %s: \"the %s thread\" (H1.00) ===" % (th, sub)]
        forest += ["[0.1] line %d" % k for k in range(40)]
        w(os.path.join(root, "trees", "%s.md" % sub), "\n".join(forest) + "\n")
    wjl(os.path.join(S, "codes.jsonl"), codes)
    wjl(os.path.join(S, "items.jsonl"), items)
    wjl(os.path.join(S, "themes.jsonl"), themes)
    wjl(os.path.join(S, "threads.jsonl"), threads)
    wjl(os.path.join(S, "transitions.jsonl"), trans)
    wjl(os.path.join(S, "pointers.jsonl"), [
        {"sub": "denmark", "kind": "subreddit", "normalised": "r/sweden"},
        {"sub": "denmark", "kind": "subreddit", "normalised": "r/norge"},
        {"sub": "sweden", "kind": "subreddit", "normalised": "r/norge"}])
    wjl(os.path.join(root, "package", "canvas", "artworks.jsonl"), [
        {"artwork_id": "a1", "name": "Dannebrog", "subreddits": ["denmark"], "subreddits_in_frame": ["denmark"],
         "pixels_covered": 310, "placements": 500, "placements_smallest_polygon": 400, "distinct_placers": 40,
         "first_hour": 2, "last_hour": 72, "placements_by_hour_0_96": [0, 0] + [7] * 71 + [0] * 24},
        {"artwork_id": "a2", "name": "Nordic cross", "subreddits": ["denmark", "sweden"], "subreddits_in_frame": ["denmark", "sweden"],
         "pixels_covered": 50, "placements": 60, "placements_smallest_polygon": 60, "distinct_placers": 9,
         "first_hour": 30, "last_hour": 40, "placements_by_hour_0_96": [0] * 30 + [6] * 10 + [0] * 57}])
    w(os.path.join(root, "package", "pixels.csv"),
      "sub,hour_since_open,px_in_region_any,px_by_pre_members,px_by_window_members\n"
      "denmark,-1,100,10,40\ndenmark,0,100,10,60\nsweden,0,50,5,5\n")
    w(os.path.join(root, "package", "canvas", "DATA-manifest-canvas.md"),
      "# The canvas\n\n**A per-community rate is fine; a canvas-wide total is not.**\n")
    out = os.path.join(root, "out")
    w(os.path.join(out, "rooms", "denmark.md"), "# r/denmark (read x)\ndoing:      placing the flag\nmade:       a flag that held\n"
      "week:       the subreddit's ordinary week of news and questions before the canvas opened, then the call\n"
      "ended:      the coordinating stopped when the canvas froze\n")
    w(os.path.join(out, "rooms", "_lexicon.md"), "flag everywhere\n")
    w(os.path.join(out, "notes-A1.md"), "# notes\n\n## Block order\nsweden first, then r/denmark.\n\n## Expect\narmenia\n")
    w(os.path.join(out, "order-A1.txt"), "01\tsweden\n01\tr/denmark\n")
    wjl(os.path.join(out, "dropped.jsonl"), [])
    wjl(os.path.join(out, "families.jsonl"), [{"family": "G01", "name": "work", "themes": ["T3-001", "T3-002"]}])
    wjl(os.path.join(out, "scheme", "scheme_current.jsonl"), [
        {"theme": "T3-001", "label": "calling people in", "gloss": "asking others to place",
         "members": [{"sub": "denmark", "second_order": "calling for hands on the flag", "codes": ["c0001"]},
                     {"sub": "sweden", "second_order": "making the Swedish flag", "codes": ["c0001"]}]},
        {"theme": "T3-002", "label": "holding the border", "gloss": "defending",
         "members": [{"sub": "denmark", "codes": ["c0002"]}]}])
    w(os.path.join(out, "_head.md"), "# head\nT3-001 and r/denmark and denmark/c0001\n")
    w(os.path.join(root, "shelves", "read", "lewin-1999.md"), "# Lewin 1999\n" + "".join("line %d\n" % i for i in range(1, 11)) + "coevolution here\n")
    w(os.path.join(root, ".stage"), "B1\n")
    return out


def main():
    root = tempfile.mkdtemp(prefix="verbs-")
    out = build(root)
    c = lambda *a: mem(*a, cwd=root)

    # ---- bug 1: table pads short rows ------------------------------------------------------
    w(os.path.join(out, "_views", "data-structure.tsv"),
      "# generated\nroom\tcode_id\tquote\tfirst_order\ttheme_id\tsecond_order\tthird_id\tthird\n"
      "denmark\tc0001\ta quote\rwith a return\tlab\tt01\tcalling\tT3-001\tcalling people in\n"
      "denmark\tc0002\tshort row\n")
    for lvl in ("2nd", "3rd"):
        rc, o = c("table", "--from", lvl)
        check("table --from %s pads short rows" % lvl, rc == 0 and "Traceback" not in o, o)

    # ---- bug 2: the log records lines served, offset, limit and every option ---------------
    c("case", "denmark", "--limit", "7", "--offset", "3")
    c("rooms", "--with", "T3-001")
    logs = [json.loads(l) for l in open(os.path.join(out, "_mem_reads-B1.jsonl"))]
    case = next(l for l in logs if l["verb"] == "case")
    rooms_ = next(l for l in logs if l["verb"] == "rooms")
    check("the log records lines served, offset and limit",
          case["lines"] == 7 and case["offset"] == 3 and case["limit"] == 7 and case["total"] == 121, case)
    check("the log records every option (rooms --with)", rooms_["opts"].get("with") == "T3-001", rooms_)

    # ---- bug 3: cite says how many match and how many are shown -----------------------------
    rc, o = run("cite.py", "--grep", "flag", "--n", "2", cwd=root)
    check("cite --grep --n: 'N match; K shown'", "12 match; 2 shown" in o, o)
    rc, o = run("cite.py", "--resolve", "we place the", "--n", "3", cwd=root)
    check("cite --resolve --n: count and shown", "12 code(s) hold these words; 3 shown" in o, o)

    # ---- bug 4 and m: mint and adjudicate refuse outside their stages; --dry-run ---------------
    rc, o = c("mint", "--label", "x", "--trigger", "denmark:t01", "--stage", "B3")
    check("mint refuses at B3", rc == 1 and "only at stage B1" in o, o)
    rc, o = c("mint", "--label", "x", "--trigger", "denmark:t09", "--gate", "g", "--codes", "c0001", "--stage", "B1")
    check("mint refuses a trigger the store lacks", rc == 1 and "names no second-order theme" in o, o)
    rc, o = c("mint", "--label", "x", "--trigger", "denmark:t01", "--gate", "g", "--codes", "c0001", "--dry-run")
    check("mint --dry-run writes nothing", rc == 0 and "dry run" in o and not os.path.exists(os.path.join(out, "theme_discovery.jsonl")), o)
    rc, o = c("mint", "--label", "calling", "--trigger", "Denmark:t01", "--gate", "a call for hands", "--codes", "c0001")
    check("mint at B1 writes a line and a diary line", rc == 0 and "minted T3-003" in o and os.path.exists(os.path.join(out, "theme_discovery.jsonl")), o)
    sc = os.path.join(out, "scheme", "scheme_current.jsonl")
    check("mint puts the theme in scheme_current with its trigger", os.path.exists(sc) and
          any(r.get("theme") == "T3-003" and r["members"] and r["members"][0].get("theme_id") == "t01"
              for r in map(json.loads, open(sc))), open(sc).read() if os.path.exists(sc) else "absent")
    rc, o = c("diary", "--grep", "T3-003")
    check("mint logs kind minted", "minted" in o and " split " not in o, o)
    rc, o = c("mint", "T3-005", "--label", "later", "--trigger", "denmark:t01", "--gate", "g", "--codes", "c0003")
    check("mint accepts the positional id after options", rc == 0 and "minted T3-005" in o, o)
    rc, o = c("unplace", "denmark:t01", "--theme", "T3-005")
    check("unplace takes a member out", rc == 0 and "unplaced" in o, o)
    rc, o = c("place", "denmark:t01", "--theme", "T3-009", "--codes", "c0001")
    check("place refuses an unminted theme", rc == 1 and "mint it first" in o, o)
    rc, o = c("place", "denmark:t01", "--theme", "T3-005", "--codes", "c0003")
    check("place puts a member back and says where else it sits", rc == 0 and "placed" in o and "T3-003" in o, o)
    check("scheme_current has no .tmp left", not os.path.exists(sc + ".tmp"), "")
    rc, o = c("log", "x", "--kind", "a", "--dry-run")
    check("a one-letter placeholder is not a kind", rc == 1, o)
    rc, o = c("adjudicate", "denmark-001", "--decision", "accept", "--reason", "r")
    check("adjudicate refuses outside D3", rc == 1 and "only at stage D3" in o, o)
    wjl(os.path.join(out, "adaptations.jsonl"), [{"id": "denmark-001", "sub": "denmark", "op": "instantiate", "element": "P07",
                                                   "lift": ["t01", "T3-001", None, None], "how": "x", "decision": "pending"}])
    rc, o = c("adjudicate", "denmark-009", "--decision", "accept", "--reason", "r", "--stage", "D3")
    check("adjudicate refuses an id the ledger lacks", rc == 1 and "no adaptation denmark-009" in o and "did you mean denmark-001" in o, o)
    rc, o = c("adjudicate", "denmark-001", "--decision", "accept", "--reason", "r", "--stage", "D3", "--dry-run")
    check("adjudicate --dry-run writes nothing", rc == 0 and not os.path.exists(os.path.join(out, "adjudications.jsonl")), o)

    # ---- bug 5: log --kind is checked ------------------------------------------------------
    rc, o = c("log", "hello", "--kind", "bogus")
    check("log refuses an unknown kind with the list", rc == 1 and "opened" in o and "helper" in o, o)
    rc, o = c("log", "hello", "--kind", "move", "--dry-run")
    check("log --dry-run", rc == 0 and "dry run" in o, o)
    rc, o = c("log", "opened sweden", "--kind", "opened", "--ids", "sweden", "--stage", "A1")
    check("log --kind opened writes", rc == 0 and "logged" in o, o)

    # ---- bug 6: links resolves rooms and concepts; validate --open fails on it at A1 --------
    rc, o = run("links.py", cwd=root)
    check("links: a clean head passes", rc == 0, o)
    with open(os.path.join(out, "_head.md"), "a") as f:
        f.write("r/denmrk and sweden:c0099 and denmark/t07\n")
    rc, o = run("links.py", cwd=root)
    check("links: a wrong room, concept and theme fail", rc == 1 and "r/denmrk" in o and "sweden/c0099" in o and "denmark/t07" in o, o)
    if os.path.isdir(os.path.join(INS, "stages")):
        os.symlink(os.path.join(INS, "stages"), os.path.join(root, "stages"))
        rc, o = run("validate.py", "--open", "A1", ".", cwd=root)
        check("validate --open A1 exits 1 when a link fails", rc == 1 and "links.py found ids" in o, o)
        w(os.path.join(out, "_head.md"), "# head\nT3-001 and r/denmark\n")
        rc, o = run("validate.py", "--open", "A1", ".", cwd=root)
        check("validate --open A1 names its inputs and prints the counts (bug 15)",
              "census 3 rooms" in o and "HOW-TO-RUN.md" in o and "concepts 12 census" in o, o)

    # ---- bug 7: packets B2 and B4 read {"item": ...}; B2 honours --scheme and --to ----------
    contract = os.path.join(INS, "CONTRACT-aggregator.md")
    if os.path.exists(contract):
        shutil.copy(contract, root)
        wjl(os.path.join(out, "scheme_final.jsonl"), [{"id": "T3-001", "name": "calling", "gloss": "g"},
                                                      {"id": "T3-002", "name": "holding", "gloss": "g"}])
        wjl(os.path.join(out, "author_items.jsonl"), [{"item": "denmark/t01"}, {"sub": "sweden", "theme_id": "t02"}])
        wjl(os.path.join(out, "sample-B4.jsonl"), [{"item": "denmark/t02"}, "sweden/t01"])
        rc, o = run("packets.py", "B2", "--scheme", "out/scheme_final.jsonl", "--families", "out/families.jsonl",
                    "--to", os.path.join(root, "p03"), cwd=root)
        check("packets B2 --scheme --to, items as {item}", rc == 0 and os.path.exists(os.path.join(root, "p03", "P03-r1.md"))
              and "scheme_final" in o, o)
        rc, o = run("packets.py", "B4", cwd=root)
        check("packets B4 with {item} lines", rc == 0 and "1 packets" in o, o)
        os.remove(os.path.join(out, "scheme_final.jsonl"))          # back to stage B1: no frozen scheme

    # ---- bug 8: ingest with no drop folder ------------------------------------------------
    rc, o = run("ingest.py", "D", cwd=root)
    check("ingest D with no DROPS/D: one line, exit 1", rc == 1 and "absent" in o and "Traceback" not in o, o)

    # ---- bug 9: levels ---------------------------------------------------------------------
    rc, o = c("pairs", "--level", "second")
    check("pairs --level second says no placement is needed", rc == 0 and "no placement is needed" in o and "(no placements)" not in o, o)
    rc, o = c("pairs", "--level", "theme")
    check("pairs --level theme is third (old name)", rc == 0 and "level third" in o and "T3-001" in o, o)
    rc, o = c("pairs", "--level", "bogus")
    check("pairs refuses an unknown level with the list", rc == 1 and "second, third, fourth, dimension" in o, o)
    rc, o = c("help")
    check("help speaks the tiers, not chunk or case theme", "chunk" not in o.split("Old names")[0] and "second-order theme" in o and "S07" not in o, o)

    # ---- bug 10: diary --last with no N ----------------------------------------------------
    rc, o = c("diary", "--last")
    check("diary --last defaults to 5", rc == 0 and "opened sweden" in o, o)
    kl = os.path.join(out, "kinds-B1.jsonl")
    led = [json.loads(l) for l in open(kl)] if os.path.exists(kl) else []
    check("mint and place at B1 append to the kinds ledger, append only",
          [r["event"] for r in led] == ["minted", "minted", "placed"] and all("at" in r for r in led), json.dumps(led))
    rc, o = c("log", "merged T3-005 into T3-003", "--kind", "merged", "--ids", "T3-003,T3-005")
    led = [json.loads(l) for l in open(kl)] if os.path.exists(kl) else []
    check("a logged merge is a new kind in the ledger", rc == 0 and led and led[-1]["kind"] == "merged:T3-003+T3-005", json.dumps(led[-1:]))
    rc, o = c("mint", "--label", "at C1", "--trigger", "denmark:t01", "--gate", "g", "--stage", "C1", "--dry-run")
    check("mint runs at C1 (no stopping-rule stamp there)", rc == 0 and "dry run" in o and "words_read" not in o, o)
    rc, o = c("idea", "an idea at D3", "--trigger", "denmark:t01", "--stage", "D3")
    check("idea runs at D3", rc == 0 and "idea logged" in o, o)
    af = os.path.join(out, "assignments_final.jsonl")
    wjl(af, [{"sub": "denmark", "theme_id": "t01", "third_order": ["T3-001"], "confidence": "clear", "read": "whole"}])
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-002", "--codes", "c0001", "--reason", "the split", "--stage", "C2")
    rows = [json.loads(l) for l in open(af)]
    check("reassign at C2 rewrites the line in place, the move on it", rc == 0 and len(rows) == 1 and
          rows[0]["third_order"] == ["T3-002"] and rows[0]["moves"][0]["from"] == ["T3-001"], o)
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-099", "--codes", "c0001", "--reason", "x", "--stage", "C2")
    check("reassign refuses a theme the scheme lacks", rc == 1 and "not in" in o, o)
    rc, o = c("reassign", "denmark:t01", "--theme", "T3-002", "--reason", "x", "--stage", "B1")
    check("reassign refuses before C1", rc == 1, o)
    rc, o = c("place", "denmark:t01", "--theme", "T3-002", "--stage", "C1")
    check("place refuses after the freeze", rc == 1, o)
    os.replace(af, af + ".reassign-test")      # later tests read the working grouping, not a fleet's

    # ---- bug 11: silent empty results ------------------------------------------------------
    rc, o = c("room", "Denmrk")
    check("a wrong room says so, with the nearest", rc == 1 and "did you mean denmark" in o, o)
    rc, o = c("room", "R/DENMARK")
    check("a room in any case, as r/<sub>", rc == 0 and o.startswith("r/denmark"), o)
    rc, o = c("rooms", "--without", "T3-999")
    check("rooms --without an id that does not exist", rc == 1 and "no such id" in o, o)
    rc, o = c("forest", "denmark", "zz1")
    check("forest with a wrong thread", rc == 1 and "not in the forest" in o, o)
    rc, o = c("forest", "denmark", "--offset", "500")
    check("an offset past the end", rc == 1 and "past the end" in o, o)
    rc, o = c("codes", "--third", "T3-099")
    check("codes --third with a wrong id", rc == 1 and "did you mean" in o, o)

    # ---- bug 12 and 13: thread id on code lines; theme by label words --------------------------
    rc, o = c("codes", "--sub", "denmark")
    check("code lines carry the thread id", "@de1:0.1" in o, o)
    rc, o = c("theme", "denmark/DEFENDING")
    check("theme by a label substring, any case", rc == 0 and "r/denmark t02" in o, o)

    # ---- bug 14: self-test --summary, independent of the cwd and of tools/tests/ ---------------
    cp = tempfile.mkdtemp(prefix="tools-")
    shutil.copytree(T, os.path.join(cp, "tools"), ignore=shutil.ignore_patterns("tests", "__pycache__"))
    r = subprocess.run([PY, os.path.join(cp, "tools", "validate.py"), "--self-test", "--summary"], cwd=root,
                       capture_output=True, text=True)
    check("self-test --summary from a run folder, without tools/tests/", r.returncode == 0 and
          r.stdout.strip().endswith("planted defects)") and len(r.stdout.strip().splitlines()) <= 3, r.stdout[-800:])
    shutil.rmtree(cp, ignore_errors=True)

    # ---- new verbs -------------------------------------------------------------------------
    rc, o = c("case", "denmark", "--page", "2", "--limit", "50")
    check("case, paged", rc == 0 and "line 50 of the case" in o and "[lines 51-100 of 121" in o, o)
    rc, o = c("canvas", "denmark")
    check("canvas: fields, artworks with bars, pixel shares, caveat",
          "Dannebrog" in o and "shared with sweden" in o and "share 0.5" in o and "share 0.1" in o
          and "per-community rate" in o and "^ freeze h73" in o, o)
    rc, o = c("canvas", "armenia")
    check("canvas: a room with six nulls says so", "six nulls" in o and "no rows for r/armenia" in o, o)
    rc, o = c("facts", "--field", "codes", "--summary")
    check("facts --summary", "n 3, nulls 0" in o and "median 4" in o, o)
    rc, o = c("facts", "--field", "items_in_window", "--nulls")
    check("facts --nulls", "null in 1 of 3" in o and "armenia" in o, o)
    rc, o = c("facts", "--field", "codes", "--where", "codes>2", "--sort", "asc", "--top", "1")
    check("facts --where --sort --top", "sweden" in o and "denmark" not in o.split("\n", 1)[1], o)
    rc, o = c("facts", "--slope", "items_in_store", "codes")
    check("facts --slope", "slope 1.000" in o, o)
    rc, o = c("facts", "--field", "px_window_share")
    check("facts reads pixel shares", "denmark                  0.5" in o, o)
    rc, o = c("facts", "--field", "codez")
    check("facts: a wrong field", rc == 1 and "did you mean codes" in o, o)
    rc, o = c("facts", "--field", "codes", "--json")
    check("facts --json", json.loads(o.splitlines()[0])["sub"] == "denmark", o)
    rc, o = c("notes", "--grep", "flag", "--field", "made")
    check("notes --grep --field, skipping _ files", "denmark" in o and "made" in o and "everywhere" not in o, o)
    rc, o = c("progress", "--stage", "A1")
    check("progress: the declared order, read and pending",
          "declared in out/order-A1.txt" in o and "1. sweden                   read" in o and "2. denmark                  noted" in o, o)
    rc, o = c("scheme", "--brief")
    check("scheme --brief at B1 from out/scheme/scheme_current.jsonl",
          any(l.startswith("T3-001") and "G01" in l and l.split()[2] == "2" and "calling people in: asking others to place" in l
              for l in o.splitlines()), o)
    rc, o = c("where", "T3-001")
    check("where reads the working grouping's members at B1", "2 second-order themes in 2 rooms" in o, o)
    rc, o = c("themes", "--grep", "flag")
    check("themes --grep with counts per room", "per room (top 20 of 3): denmark 2" in o and "sweden/t01" in o, o)
    rc, o = c("themes", "--rooms", "armenia", "--json")
    check("themes --json", json.loads(o.splitlines()[0])["theme_id"] == "t01", o)
    rc, o = c("compare", "denmark", "sweden", "--grep", "flag")
    check("compare: facts, when, themes, names, canvas, shared labels",
          "named by both: r/norge" in o and "^ freeze h73" in o and "concept labels matching /flag/" in o, o)
    rc, o = c("codes", "--grep", "flag", "--by-room")
    check("codes --grep --by-room", "denmark                       6  h+2.00" in o, o)
    rc, o = c("codes", "--sub", "sweden", "--json")
    check("codes --json", json.loads(o.splitlines()[0])["sub"] == "sweden", o)
    rc, o = c("room", "sweden", "--json")
    check("room --json", json.loads(o.splitlines()[0])["sub"] == "sweden", o)
    rc, o = c("shelf", "lewin-1999", "--grep", "coevolution")
    check("shelf --grep with line numbers", "12: coevolution here" in o, o)
    rc, o = c("shelf", "lewin-1999", "--page", "2", "--limit", "5")
    check("shelf --page", "line 5" in o and "[lines 6-10 of 12" in o, o)
    run("gen_views.py", "B1", "--root", ".", cwd=root)
    rc, o = c("view", "data-structure", "--room", "sweden", "--grep", "flag")
    check("view with --room and --grep", rc == 0 and "4 of 12 lines in r/sweden" in o, o)
    rc, o = c("wiki", "denmark")
    check("wiki page by room", rc == 0 and "# r/denmark" in o, o)
    rc, o = run("cite.py", "--room", "denmark", "--code", "c0003", "--context", "1", cwd=root)
    check("cite --context: parent, quote and replies with coded passages",
          "QUOTE" in o and "parent" in o and "reply" in o and "we place the denmark flag number 3" in o, o)
    rc, o = run("cite.py", "--room", "Denmrk", "--code", "c0003", cwd=root)
    check("cite refuses a wrong room with the nearest", rc == 1 and "did you mean denmark" in o, o)

    # v43: a question for the principal investigator, and the package checks of stage A1
    rc, o = mem("ask", "is r/denmark one room or two?", "--stage", "A1", cwd=root)
    check("ask refuses without --assume", rc == 1 and "--assume" in o, o)
    rc, o = mem("ask", "is r/denmark one room or two?", "--assume", "one room", "--ids", "r/denmark", "--stage", "A1", cwd=root)
    check("ask writes asks.jsonl and names the id", rc == 0 and "asked QA1-001" in o and os.path.exists(os.path.join(out, "asks.jsonl")), o)
    rc, o = mem("diary", "--grep", "QA1-001", "--stage", "A1", cwd=root)
    check("the diary carries the question as kind ask", rc == 0 and " ask " in o and "meanwhile: one room" in o, o)
    rc, o = mem("asks", "--open", "--stage", "A1", cwd=root)
    check("asks --open lists an open question with what is done meanwhile", rc == 0 and "QA1-001" in o and "meanwhile: one room" in o, o)
    w(os.path.join(out, "_answers", "QA1-001.md"), "one room; the second name is an alias\n")
    rc, o = mem("asks", "QA1-001", "--stage", "A1", cwd=root)
    check("asks <id> shows the answer", rc == 0 and "answered" in o and "an alias" in o, o)
    rc, o = mem("asks", "--open", "--stage", "A1", cwd=root)
    check("an answered question leaves asks --open", rc == 0 and "QA1-001" not in o, o)
    rc, o = mem("asks", "QA1-009", "--stage", "A1", cwd=root)
    check("asks refuses an unknown id with the nearest", rc == 1 and "QA1-001" in o, o)
    rc, o = mem("audit", "--stage", "A1", cwd=root)
    check("audit runs its four checks and names their files", rc == 0 and "frame: package/FRAME.md" in o and "rooms:" in o
          and "retracted:" in o and "build:" in o and "Traceback" not in o, o)
    rc, o = mem("audit", "nonsense", "--stage", "A1", cwd=root)
    check("audit refuses an unknown check", rc == 1 and "frame, rooms, retracted or build" in o, o)

    shutil.rmtree(root, ignore_errors=True)
    if "--run" in sys.argv:
        smoke(sys.argv[sys.argv.index("--run") + 1])
    print("\nverbs: %d failed" % len(FAILS))
    return 1 if FAILS else 0


def smoke(src):
    """Every read verb once over a copy of a real run, with a fake canvas joined; none may crash."""
    root = tempfile.mkdtemp(prefix="realrun-")
    shutil.copytree(src, root, dirs_exist_ok=True)
    subs = [json.loads(l)["sub"] for l in open(os.path.join(root, "package", "store", "rooms.jsonl"))]
    wjl(os.path.join(root, "package", "case_facts_outcome.jsonl"),
        [{"sub": s, "canvas_entries": 1, "canvas_area_px": 100 + i, "canvas_centre": [i, i], "canvas_ring": "edge",
          "canvas_artwork": "%s art" % s, "canvas_source": "fake"} for i, s in enumerate(subs[:-1])])
    wjl(os.path.join(root, "package", "canvas", "artworks.jsonl"),
        [{"artwork_id": "a%d" % i, "name": "%s art" % s, "subreddits": [s], "subreddits_in_frame": [s], "pixels_covered": 100,
          "centre": [i, i], "placements": 50, "placements_smallest_polygon": 40, "distinct_placers": 5,
          "first_hour": 1, "last_hour": 70, "placements_by_hour_0_96": [1] * 73 + [0] * 24} for i, s in enumerate(subs)])
    w(os.path.join(root, "package", "pixels.csv"), "sub,hour_since_open,px_in_region_any,px_by_pre_members,px_by_window_members\n"
      + "".join("%s,%d,10,2,4\n" % (s, h) for s in subs for h in range(-16, 73)))
    run("build_store.py", "--root", root, "--join-canvas", "package/case_facts_outcome.jsonl", cwd="/")
    a, b = subs[0], subs[-1]
    calls = [("room", a), ("room", a, "--no-canvas"), ("case", a), ("brief", a), ("forest", a), ("when", a), ("canvas", a),
             ("compare", a, b, "--grep", "flag"), ("codes", "--sub", a), ("codes", "--grep", "flag", "--by-room"),
             ("themes", "--grep", "flag"), ("facts",), ("facts", "--field", "codes", "--summary"),
             ("facts", "--slope", "items_in_store", "codes"), ("pairs", "--level", "fourth"), ("scheme", "--brief"),
             ("progress",), ("progress", "--plan"), ("progress", "--plan", "0.001"), ("forest", a, "--limit", "3"), ("view",), ("wiki",), ("diary", "--last"), ("table", "--from", "2nd")]
    for call in calls:
        rc, o = mem(*call, "--stage", "A1", cwd=root)
        check("real run: mem.py %s" % " ".join(call), "Traceback" not in o and (rc == 0 or "no " in o), o)
    rc, o = run("cite.py", "--room", a, "--code", "c0002", "--context", "2", "--stage", "A1", cwd=root)
    check("real run: cite --context", "Traceback" not in o, o)
    shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
