"""Handler-side. Adds rooms to aggregator/input/coders/rooms in the one layout every room has:
brief.md, case.md, codes.jsonl, themes.jsonl, threads.jsonl, pointers.jsonl, forest/{<sub>.md,
forest.jsonl, tree_index.json}; handler-only files (notes.md, _run.json, ...) beside them.
  python3 import_rooms.py late      # rooms verified in the yard after the 2026-09-24 copy
  python3 import_rooms.py legacy    # the rooms in _work/legacy (extract_legacy.py puts them there)
  python3 import_rooms.py forests   # re-render every room's forest with one tree builder
  python3 import_rooms.py room <sub> [<sub> ...]   # any verified yard room, from its archives; then ROOMS.tsv
  python3 import_rooms.py verified [<sub> ...]  # verified yard rooms of the census population not yet in the run; then ROOMS.tsv
  python3 import_rooms.py rooms_tsv # rewrite ROOMS.tsv from the rooms present: sub, codes, themes, retracted
Every forest is cut below depth CUT_DEPTH (490) in forest.jsonl; see cut_forest.
The yard is P("yard_rooms"): the study's yard, or coder/rooms/ of this repository, or a yard of yours.
"""
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from paths import P
import json, os, shutil, subprocess, sys, tempfile
R, W = P("run"), P("work")
HERE_ = os.path.dirname(os.path.abspath(__file__))
Y = P("yard_rooms")
L = W + "/legacy"
PKG = P("v37_package")
F = P("input") + "/coders/rooms"
TB = Y + "/sweden/run/tools/tree_builder.py"
LATE = "GuildWars2 brasil dbz ice_poseidon liverpoolfc newzealand osugame reddevils rwby smashbros sweden vegan".split()
SKIP = {"_transcript.jsonl", "_journal.jsonl"}

def jl(p): return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
def wjl(p, rows):
    with open(p, "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")

DEEP = """import sys, runpy, threading
sys.setrecursionlimit(200000)
threading.stack_size(512 * 1024 * 1024)
sys.argv = sys.argv[1:]
err = []
def f():
    try:
        runpy.run_path(sys.argv[0], run_name="__main__")
    except SystemExit as e:
        err.append(e.code or 0)
    except BaseException:
        import traceback; traceback.print_exc(); err.append(1)
t = threading.Thread(target=f); t.start(); t.join()
sys.exit(err[0] if err else 0)
"""


def render(sub, record=None, threads_file=None, total=None, tb=None):
    D = os.path.join(F, sub); os.makedirs(D + "/forest", exist_ok=True)
    T = tempfile.mkdtemp()
    # the tree builder recurses once per reply; very deep threads (r/counting) need a higher limit
    cmd = ["python3", "-B", "-c", DEEP, tb or TB, "--sub", sub, "--codes-file", D + "/codes.jsonl", "--out-dir", T]
    cmd += ["--record", record] if record else ["--threads-file", threads_file]
    if total is not None: cmd += ["--threads-total", str(total)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        return "FAIL " + (r.stderr.strip().splitlines() or ["?"])[-1]
    shutil.copyfile(T + "/package/forest.jsonl", D + "/forest/forest.jsonl")
    shutil.copyfile(T + "/package/tree_index.json", D + "/forest/tree_index.json")
    shutil.copyfile(T + "/trees/%s.md" % sub, D + "/forest/%s.md" % sub)
    shutil.rmtree(T)
    n = cut_forest(D + "/forest/forest.jsonl")
    return "ok" + ("; cut below depth %d: %d items, %d coded" % (CUT_DEPTH, n[0], n[1]) if n[0] else "")


# Reply chains deeper than CUT_DEPTH are cut in forest.jsonl only. Each level is two JSON levels, and
# Python 3.11's reader stops near 1,000, so a tree deeper than about 496 cannot be read by the store
# (r/counting's chains reach 1,004). 490 keeps a margin. tree_index.json and <sub>.md stay whole.
# The node at the cut carries cut_below {n_items, n_coded}; the thread carries cut_at_depth, n_cut,
# n_coded_cut. The codes on cut items stay in codes.jsonl; the store lists them in _unjoined.jsonl.
# A room that is cut keeps its whole forest beside it as forest/forest.uncut.jsonl, which no tool reads.
CUT_DEPTH = 490

def cut_forest(path):
    import threading
    tot = [0, 0]
    def work():
        rows = []
        for l in open(path, encoding="utf-8"):
            if not l.strip(): continue
            th = json.loads(l); k0, m0 = 0, 0
            st = [(th["tree"], 0)]
            while st:
                n, d = st.pop()
                if d == CUT_DEPTH and n.get("children"):
                    k = m = 0; q = list(n["children"])
                    while q:
                        x = q.pop(); k += 1; m += bool(x.get("code_ids")); q.extend(x.get("children", []))
                    n["children"] = []; n["cut_below"] = {"n_items": k, "n_coded": m}
                    k0 += k; m0 += m
                else:
                    st.extend((c, d + 1) for c in n.get("children", []))
            if k0:
                th["cut_at_depth"], th["n_cut"], th["n_coded_cut"] = CUT_DEPTH, k0, m0
                tot[0] += k0; tot[1] += m0
            rows.append(th)
        if tot[0]:
            shutil.copyfile(path, path[:-len(".jsonl")] + ".uncut.jsonl")   # the whole forest, kept beside the cut one
            wjl(path, rows)
    old = sys.getrecursionlimit(); sys.setrecursionlimit(200000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=work); t.start(); t.join()
    sys.setrecursionlimit(old)
    return tot

def late():
    for s in LATE:
        D = os.path.join(F, s); os.makedirs(D, exist_ok=True)
        src = os.path.join(Y, s, "run", "out")
        for f in os.listdir(src):
            if f not in SKIP and os.path.isfile(os.path.join(src, f)):
                shutil.copyfile(os.path.join(src, f), os.path.join(D, f))
        shutil.copyfile(os.path.join(Y, s, "brief", "out", "brief.md"), D + "/brief.md")
        print(s, render(s, record=os.path.join(Y, s, "run", "coder_corpus.jsonl")), flush=True)

def legacy_pointers(sub, mentions):
    out, n = [], 0
    for m in mentions.get(sub, {}).get("named", []):
        raw = (m.get("name_raw") or "").strip()
        if not raw.lower().lstrip("/").startswith("r/"):
            continue
        n += 1
        ids = m.get("item_ids") or []
        out.append({"pointer_id": "p%04d" % n, "batch": "01", "raw": raw,
                    "normalised": "r/" + (m.get("name") or raw.split("r/", 1)[-1]).strip("/ "),
                    "kind": "subreddit", "relation": None, "moved": None, "what_still_returns": None,
                    "what_you_cannot_see": None, "thread_id": None, "item_id": ids[0] if ids else None,
                    "start": None, "end": None, "text": m.get("quote") or m.get("text"), "code_ids": [],
                    "minted_in_stage": "case", "note": "named in the case account, section Other communities named",
                    "corpus_position": None})
    return out

def legacy():
    mentions = {r["sub"]: r for r in jl(PKG + "/mentions.jsonl")}
    have = {x.lower() for x in os.listdir(F)}
    for s in sorted(os.listdir(L)):
        S, D = os.path.join(L, s), os.path.join(F, s)
        if not os.path.isdir(S): continue
        if s.lower() in have and not os.path.exists(os.path.join(D, "_legacy")):
            if os.path.exists(os.path.join(D, "_gate.json")):   # coded in the yard too: the yard's coding stands
                print(s, "skipped: coded in the yard as well", flush=True); continue
        if os.path.exists(os.path.join(D, ".imported")):
            continue
        os.makedirs(D, exist_ok=True)
        for a, b in (("brief.md", "brief.md"), ("out/case.md", "case.md"), ("out/themes.jsonl", "themes.jsonl"),
                     ("out/notes.md", "notes.md"), ("out/_run.json", "_run.json")):
            shutil.copyfile(os.path.join(S, a), os.path.join(D, b))
        rec = os.path.join(S, "coder_corpus.jsonl"); pth = os.path.join(PKG, "threads", s + ".jsonl")
        items, total = {}, None
        if os.path.exists(rec):
            L0 = jl(rec); total = L0[0].get("_n_threads")
            for r in L0[1:]:
                if r.get("id"): items[r["id"]] = r
        else:
            for t in jl(pth):
                for it in t.get("items", []): items[it["id"]] = it
        codes = []
        for c in jl(os.path.join(S, "out/codes.jsonl")):
            it = items.get(c.get("item_id"), {})
            e = {"passage_id": c.get("passage_id"), "code_id": c["code_id"], "batch": "01",
                 "first_order": c.get("first_order"), "theme_id": c.get("theme_id"), "thread_id": c.get("thread_id"),
                 "item_id": c.get("item_id"), "item_kind": it.get("kind"), "author": it.get("author"),
                 "created_utc": it.get("created_utc"), "exchange_id": c.get("exchange_id"),
                 "discovered_at": c.get("discovered_at"), "minted_in_stage": c.get("minted_in_stage"),
                 "start": c.get("start"), "end": c.get("end"), "text": c.get("text"), "note": c.get("note"),
                 "minted_after_n_codes": c.get("minted_after_n_codes"), "corpus_position": c.get("corpus_position")}
            if c.get("retracted"): e["retracted"] = True; e["retracted_reason"] = c.get("retracted_reason")
            codes.append(e)
        wjl(D + "/codes.jsonl", codes)
        wjl(D + "/threads.jsonl", [dict(t, batch="01") for t in jl(os.path.join(S, "out/threads.jsonl"))])
        pp = os.path.join(S, "out/pointers.jsonl")
        wjl(D + "/pointers.jsonl", [dict(p, batch="01") for p in jl(pp)] if os.path.exists(pp) else legacy_pointers(s, mentions))
        noauthor = sum(1 for c in codes if c["author"] is None)
        res = render(s, record=rec, total=total) if os.path.exists(rec) else render(s, threads_file=pth)
        print(s, res, "codes", len(codes), "no_author", noauthor, flush=True)
        if res == "ok":
            open(os.path.join(D, ".imported"), "w").write("legacy\n")

def forests():
    for s in sorted(os.listdir(F)):
        if s in LATE or os.path.isdir(os.path.join(L, s)): continue
        print(s, render(s, record=os.path.join(Y, s, "run", "coder_corpus.jsonl")), flush=True)

def window():
    """window.json for every room: the window's thread and item counts from the corpus header, the
    same source for every room; case facts for the rooms whose corpus is not held."""
    facts = {r["sub"]: r for r in jl(PKG + "/case_facts.jsonl")}
    n = 0
    for s in sorted(os.listdir(F)):
        D = os.path.join(F, s)
        if not os.path.isdir(D): continue
        rec = os.path.join(L, s, "coder_corpus.jsonl") if os.path.isdir(os.path.join(L, s)) and s != "Dorset" \
            else os.path.join(Y, s, "run", "coder_corpus.jsonl")
        w = {}
        if os.path.exists(rec):
            with open(rec, encoding="utf-8") as f:
                h = json.loads(f.readline())
            w = {"threads_in_window": h.get("_n_threads"), "items_in_window": h.get("_n_items")}
        elif s in facts:
            w = {"threads_in_window": facts[s].get("threads_total"), "items_in_window": facts[s].get("items_in_window")}
        json.dump(w, open(os.path.join(D, "window.json"), "w"))
        n += 1
        if not w.get("items_in_window"): print("no window counts:", s)
    print("window.json written for", n, "rooms")

def _unpack(archive, dest):
    os.makedirs(dest, exist_ok=True)
    z = subprocess.run(["zstd", "-dc", archive], capture_output=True)
    if z.returncode:
        sys.exit("zstd failed on %s (is zstd installed?)" % archive)
    subprocess.run(["tar", "-x", "-C", dest], input=z.stdout, capture_output=True, check=True)


def import_room(s):
    """One verified yard room into aggregator/input/coders/rooms/<s>: the coder's out/ files, the brief, the forest
    rendered by the room's own tree builder, and window.json from the corpus header."""
    R0 = os.path.join(Y, s)
    st = json.load(open(os.path.join(R0, "STATE.json"))) if os.path.exists(os.path.join(R0, "STATE.json")) else {}
    T = tempfile.mkdtemp()
    run = os.path.join(R0, "run")
    if not os.path.isdir(os.path.join(run, "out")):
        if not os.path.exists(os.path.join(R0, "run.tar.zst")):
            shutil.rmtree(T); return "not coded: no run/out and no run.tar.zst (stage %s)" % st.get("stage", "?")
        _unpack(os.path.join(R0, "run.tar.zst"), T); run = os.path.join(T, "run")
    brief = os.path.join(R0, "brief", "out", "brief.md")
    if not os.path.exists(brief) and os.path.exists(os.path.join(R0, "materials.tar.zst")):
        _unpack(os.path.join(R0, "materials.tar.zst"), os.path.join(T, "m"))
        cand = [os.path.join(d, "brief.md") for d, _, fs in os.walk(os.path.join(T, "m")) if "brief.md" in fs and d.endswith(os.path.join("brief", "out"))]
        brief = cand[0] if cand else brief
    D = os.path.join(F, s); os.makedirs(D, exist_ok=True)
    out = os.path.join(run, "out")
    for f in os.listdir(out):
        if f not in SKIP and not f.startswith("._") and os.path.isfile(os.path.join(out, f)):
            shutil.copyfile(os.path.join(out, f), os.path.join(D, f))
    if os.path.exists(brief):
        shutil.copyfile(brief, os.path.join(D, "brief.md"))
    rec = os.path.join(run, "coder_corpus.jsonl")
    tb = os.path.join(run, "tools", "tree_builder.py")
    if not os.path.exists(tb):
        tb = os.path.join(os.path.dirname(os.path.dirname(HERE_)), "coder", "instrument", "v32", "tools", "tree_builder.py")
    res = render(s, record=rec, tb=tb)
    with open(rec, encoding="utf-8") as f:
        h = json.loads(f.readline())
    json.dump({"threads_in_window": h.get("_n_threads"), "items_in_window": h.get("_n_items")}, open(os.path.join(D, "window.json"), "w"))
    shutil.rmtree(T)
    return res + ("" if os.path.exists(os.path.join(D, "brief.md")) else "; no brief found")


def rooms_tsv():
    rows = []
    for s in sorted(os.listdir(F)):
        cp = os.path.join(F, s, "codes.jsonl")
        if not os.path.exists(cp): continue
        codes = jl(cp); tp = os.path.join(F, s, "themes.jsonl")
        rows.append((s, len(codes), len(jl(tp)) if os.path.exists(tp) else 0, sum(1 for c in codes if c.get("retracted"))))
    with open(os.path.join(os.path.dirname(F), "ROOMS.tsv"), "w", encoding="utf-8") as f:
        f.write("sub\tcodes\tthemes\tretracted\n")
        for r in rows: f.write("%s\t%d\t%d\t%d\n" % r)
    print("ROOMS.tsv:", len(rows), "rooms")


def room():
    for s in sys.argv[2:]:
        print(s, import_room(s), flush=True)
    rooms_tsv()


def population():
    """The census population: communities with handable = 1 (coder/census/MASTER-census.csv).
    A room outside it (screened out, silent, active only after the freeze) never enters the run."""
    import csv
    p = os.path.join(os.path.dirname(os.path.dirname(HERE_)), "coder", "census", "MASTER-census.csv")
    return {r["sub"] for r in csv.DictReader(open(p, encoding="utf-8")) if r["handable"] == "1"}


def verified():
    have = set(os.listdir(F)) if os.path.isdir(F) else set()
    pop = population()
    only = set(sys.argv[2:])
    for s in sorted(os.listdir(Y), key=str.lower):
        stf = os.path.join(Y, s, "STATE.json")
        if s in have or not os.path.exists(stf) or (only and s not in only): continue
        if json.load(open(stf)).get("stage") != "verified": continue
        if s not in pop:
            print(s, "skipped: outside the census population", flush=True); continue
        print(s, import_room(s), flush=True)
    rooms_tsv()


def lineage():
    """Handler-side only: which coding each room came from. Never copied into the run."""
    import csv
    cv = {r["sub"]: r for r in csv.DictReader(open(P("layer_a") + "/40_analysis/coder_version/coder_version.csv"))}
    with open(os.path.join(W, "LINEAGE.tsv"), "w") as f:
        f.write("sub\tsource\tinstrument\n")
        for s in sorted(os.listdir(F)):
            if not os.path.isdir(os.path.join(F, s)): continue
            if s in cv and s != "Dorset":
                f.write("%s\t%s\t%s\n" % (s, cv[s]["batch"], cv[s]["instrument"]))
            else:
                ins = json.load(open(os.path.join(Y, s, "run", "out", "_run.json"))).get("instrument", "") if os.path.exists(os.path.join(Y, s, "run", "out", "_run.json")) else ""
                f.write("%s\tyard_v30\t%s\n" % (s, ins))
    print("LINEAGE.tsv written")

{"late": late, "legacy": legacy, "forests": forests, "window": window, "lineage": lineage,
 "room": room, "verified": verified, "rooms_tsv": rooms_tsv}[sys.argv[1]]()
