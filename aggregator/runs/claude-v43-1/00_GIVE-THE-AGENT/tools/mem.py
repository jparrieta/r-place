#!/usr/bin/env python3
"""mem.py, v43: the store and your own files, one page at a time. Every call is logged (rule 1).

    python3 tools/mem.py <verb> [args] [--limit N] [--offset N | --page N] [--json] [--stage NN]
                                       [--root .] [--out out]
    python3 tools/mem.py help [verb]   this page, or the lines of it naming one verb

The tiers: first-order concept (a code, <sub>/cNNNN), second-order theme (tNN within a room,
<sub>/tNN), third-order theme (T3-NNN), fourth-order theme (T4-NNN), aggregate dimension (D1, D01).
A room is named bare, as r/<sub> or as <sub>/, in any case.

  the store, one room
    room <sub> [--no-canvas] [--size]  the room on one page: facts, threads, coded share, its
                                       second-order themes, and what it made (the six canvas
                                       fields). --no-canvas is the page the fleets and readers are
                                       served (rule 7); --size the bytes of forest, codes, themes
    case <sub>                         the coder's case.md, paged
    brief <sub>                        the room's pre-event week
    forest <sub> [thread_id]           the rendered forest, whole room or one thread
    when <sub>                         the room's coded hours as one line, 4-hour bins over 0..96
    canvas <sub>                       the six canvas fields, each linked artwork's placement by
                                       hour aligned like `when`, and the share of the room's region
                                       placed by its window and pre-event members (pixels.csv)
    compare <sub> <sub> [--grep re]    two rooms side by side before any placement: facts, `when`,
                                       second-order themes, named rooms, canvas; --grep the
                                       concept labels matching it in each
    note <sub>                         your own room note, out/rooms/<sub>.md

  concepts and themes
    codes --sub S [--second tNN]       first-order concepts of a room, or of one second-order theme
    codes --third T3-007               every concept under a third-order theme (overlay)
    codes --fourth T4-003              every concept under a fourth-order theme (overlay)
    codes --dimension D1               every concept under an aggregate dimension (overlay)
    codes --grep <re> [--by-room]      concepts whose words, label or note match; --by-room counts
                                       per room with the first hour
    theme <sub>/<tNN or label words>   a second-order theme, its note, its concepts and where it was
                                       placed; label words match a substring, any case
    themes --grep <re> [--rooms a,b]   second-order themes whose label or note match, with the
                                       count per room; without --grep every theme of --rooms
    after <sub>/<code_id>              what answered this concept and what it answered, intervals
    pairs --level second|third|fourth|dimension [--sub S] [--top N]
                                       transition counts from the ledger, lifted; the limit printed

  the room facts
    facts                              the fields of rooms.jsonl with their non-null counts
    facts --field F [--summary] [--sort asc|desc] [--where "F>v"] [--nulls] [--top N]
                                       one field over the rooms: sorted list, or n, nulls, min,
                                       quartiles, max; --where filters (>, <, >=, <=, ==, !=;
                                       repeatable); --nulls names the rooms where F is null.
                                       px_window_share and px_pre_share come from pixels.csv
    facts --slope X Y                  the log-log OLS slope of Y on X over rooms with both > 0

  your own files
    notes --grep <re> [--field <name>] your room notes (out/rooms/*.md) lines matching, with the
                                       room; --field keeps one line of the form (doing, made, ...)
    progress [--stage A1]              the declared order (out/order-A1.txt, else
                                       sorted), each room read, noted or pending, the last room opened
    next                               the next room to read (A1: the first room of the declared order; B1 with
                                       --stage B1: the room the stopping rule asks for, in B1's seeded order, with a second-order
                                       theme neither placed nor in unplaced-B1.jsonl)
                                       at A1 it names the room with no note, and its block; never take it
                                       from memory
    neighbours <sub> [--kind canvas|mention|shared] [--top N] [--json] | neighbours --summary
                                       rooms that share an artwork, border or overlap on the atlas
                                       outline, or name each other (package/store/neighbours.jsonl)
    progress --plan [MB]               and the pending rooms cut into blocks of about MB (3)
    scheme [--brief] [T3-id]           one line per third-order theme (id, label, gloss, members,
                                       family): scheme_current overlaid on the latest frozen scheme;
                                       with an id, that theme whole
    where <T3-id>                      every room and second-order theme on a third-order theme,
                                       with its fourth-order theme and dimension
    rooms --with <id> | --without <id> rooms holding or lacking a third- or fourth-order theme, a
                                       dimension, an element or an adaptation key
    contrast <sub> <sub>               the diff of two rooms' placements and adaptation sets
    adaptations --element <id> [--kind k]   every ledger line touching one element, across rooms
    finding <id> | findings --touching <element>
    question <slug>                    one open distinction
    table --from 3rd|2nd | --room <sub>   projections of the data structure
    view [name] [--grep re] [--room sub]  a generated view in out/_views/, filtered; no name lists
    wiki [page]                        a generated wiki page (rooms/<sub>, model/<id>); no page lists
    shelf [name] [--grep re] [--page N]   the read tier, or one work whole, grepped or paged;
                                       shelf --list the on-request tier
    contract --section <n>             one section of the contract by its index
    diff-scheme <snap> | diff-model <snap>  scheme_v2, or the elements and arrows, now against the copy a snap kept
    diary [--last [N]] | diary --grep <id>   the running record's tail (N defaults to 5), or every
                                       entry naming an id
    asks [<id>] [--open]               your questions to the principal investigator and the answers
                                       that came back (out/asks.jsonl, out/_answers/<id>.md)

  the package checks (stage A1)
    audit [frame|rooms|retracted|build]   the census count, the six files of every room, the
                                       retracted concepts and the store's build figures, recomputed
                                       from the raw files of package/, each figure with its file

  the writers (each refuses outside its stages; --dry-run shows the line and writes nothing)
    log "<text>" [--kind k] [--ids a,b]   the only writer to the diary (rule 20); harness-stamped.
                                       kinds: opened, dropped, merged, split, kept, move,
                                       abductive, question, comparison, note, helper, minted,
                                       placed, unplaced, pause, ask, and any
                                       other `log --kind` a stage file of this folder names
    ask "<question>" --assume "<what you do meanwhile>" [--ids a,b]   a question for the principal
                                       investigator, at any stage: it reaches him at once; you go on
                                       with your stated assumption (out/asks.jsonl, diary kind ask)
    idea "<label>" --trigger <sub>:<tNN>   a prospective third-order theme, stamped (ideas-<ST>.jsonl), before any mint
    mint --label "..." --trigger <sub>:<tNN> [T3-id]   a theme_discovery line; at B1 the new theme in
                                       scheme_current with its trigger as first member; after B1 the
                                       stamp only, the theme written into scheme_v2.jsonl (C1 to D6)
    place <sub>:<tNN> --theme T3-NNN     put a second-order theme into a third-order theme; rewrites
                                       scheme_current atomically and logs kind placed (B1; after the
                                       freeze, reassign)
    unplace <sub>:<tNN> [--theme T3-NNN] take it out of one third-order theme, or of all
    reassign <sub>:<tNN> --theme T3-a[,T3-b] --reason "..."   re-place a second-order theme under
                                       scheme v2 after a recut: rewrites its line of assignments_final.jsonl
                                       in place, the move recorded on the line, and logs kind move (C1 to D6)
    adjudicate <adaptation-id> --decision accept|modify|reject|particular|pending --reason "..."
                                       [--revised ...] [--pair id] [--kind k]   stage D3's writer

Old names still work: --case-theme for --second, --theme for --third, --chunk for --fourth;
pairs --level case_theme|theme|chunk for second|third|fourth.

The overlay. Placements, fourth-order themes and dimensions are yours and live in out/. mem.py
reads the latest frozen scheme (scheme_v2 > scheme_final > scheme), with scheme_current.jsonl
(out/scheme/ or out/) laid over it when it is newer or no frozen scheme exists;
assignments_final.jsonl (else assign_final.jsonl, else the members of scheme_current, and says
which); fourth/fourth.jsonl and dimensions.jsonl; and joins them at query time. Nothing in
package/ is ever rewritten.

Pages are --limit lines (80); every page ends with a marker: the lines shown and the total, and
the --offset of the next page. A wrong room, theme or id is refused with the nearest name.
Log: out/_mem_reads-NN.jsonl, one line per call (verb, args, every option, offset, limit, lines
served, total). NN is --stage, else the .stage file the harness writes in the folder root at
every hand-over, else $STAGE, else "xx".
"""
import argparse, collections, csv, datetime, difflib, glob, json, math, os, re, sys


class Refuse(Exception):
    """A call that cannot be answered: printed as it stands, logged, exit 1."""


KINDS = ("opened", "dropped", "merged", "split", "kept", "move", "abductive", "question", "comparison",
         "note", "helper", "minted", "placed", "unplaced", "pause", "ask")
KIND_DOC = re.compile(r"log[^`\n]*?--kind ([a-z][a-z|-]*)")


def log_kinds(root):
    """The documented kinds: the built-in list and every `log ... --kind a|b` in the standing
    documents and the stage files of this folder, so a kind a stage file adds is accepted."""
    kinds = list(KINDS)
    for p in [os.path.join(root, f) for f in ("STANDING-INSTRUCTIONS.md", "CLAUDE.md", "AGENT.md")] + \
            sorted(glob.glob(os.path.join(root, "stages", "STAGE-*.md"))):
        try:
            txt = open(p, encoding="utf-8").read()
        except OSError:
            continue
        for m in KIND_DOC.finditer(txt):
            for k in m.group(1).split("|"):
                if len(k) > 1 and k not in kinds:          # "a|b" placeholders are not kinds
                    kinds.append(k)
    return kinds
DECISIONS = ("accept", "modify", "reject", "particular", "pending")
MINT_STAGES = ("B1", "C1", "C2", "C3", "C4", "C5", "D3", "D6")   # after B1 a mint is the discovery's stamp
ADJ_STAGES = ("D3",)
RECUT_STAGES = ("C1", "C2", "C3", "C4", "C5", "D3", "D6")
LEVELS = {"second": "second", "third": "third", "fourth": "fourth", "dimension": "dimension",
          "case_theme": "second", "case-theme": "second", "2nd": "second",
          "theme": "third", "3rd": "third", "chunk": "fourth", "4th": "fourth",
          "dim": "dimension", "dimensions": "dimension"}
CANVAS = ("canvas_entries", "canvas_area_px", "canvas_centre", "canvas_ring", "canvas_artwork",
          "canvas_source")
GLYPH = " ▁▂▃▄▅▆▇█"
NBINS = 25                   # 4-hour bins over hours 0..99; hour 96 falls in the last
AXIS = [" " + "0     24    48    72    96", " " + " " * 18 + "^ freeze h73"]


def jl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def clip(s, n):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[:n - 1] + "…"


def nearest(word, options, n=1):
    """The closest names, case-insensitive; [] when nothing is close."""
    opts = [str(o) for o in options if o]
    low = {}
    for o in opts:
        low.setdefault(o.lower(), o)
    return [low[m] for m in difflib.get_close_matches(str(word).lower(), list(low), n=n, cutoff=0.5)]


def mean_hint(word, options):
    m = nearest(word, options)
    return " (did you mean %s?)" % m[0] if m else ""


def spark(bins, mx=None):
    mx = mx or max(bins) or 1
    return "|" + "".join(GLYPH[max(1, min(8, int(round(8 * b / mx))))] if b else "·" for b in bins) + "|"


def hour_bins(hours):
    bins, outside = [0] * NBINS, 0
    for h in hours:
        if h is None:
            continue
        if 0 <= h < 4 * NBINS:
            bins[int(h // 4)] += 1
        else:
            outside += 1
    return bins, outside


def canvas_lines(r):
    """What the room made, from rooms.jsonl's six canvas fields, joined at build (the contract's
    §4 and rule 7). One line, plus the sentence a reader must see beside any canvas figure."""
    if not any(k in r for k in CANVAS):
        return ["made: (no canvas fields in rooms.jsonl; the build did not join the canvas)"]
    if all(r.get(k) is None for k in CANVAS):
        return ["made: six nulls (the atlas holds no artwork for this room: nothing survived the "
                "freeze, or it was never linked)"]
    return ["made: entries %s  area_px %s  centre %s  ring %s  artwork %s"
            % (r.get("canvas_entries"), r.get("canvas_area_px"),
               json.dumps(r.get("canvas_centre")), r.get("canvas_ring"),
               clip(r.get("canvas_artwork"), 60)),
            "      what survived the freeze; declare where it shaped your reading "
            "(rule 7; source: %s)" % clip(r.get("canvas_source"), 40)]


def _norm_scheme_row(r):
    r = dict(r)
    r["id"] = r.get("id") or r.get("theme")
    r["name"] = r.get("name") or r.get("label")
    return r


class Store:
    def __init__(self, root, out):
        self.root, self.out = root, out
        self.S = os.path.join(root, "package", "store")
        self._cache = {}

    def rows(self, name):
        if name not in self._cache:
            self._cache[name] = jl(os.path.join(self.S, name + ".jsonl"))
        return self._cache[name]

    def subs(self):
        s = [r["sub"] for r in self.rows("rooms")]
        return s or sorted({c["sub"] for c in self.rows("codes")})

    def room(self, name):
        """The canonical room name for r/<sub>, <sub>/ or <sub> in any case; refuses otherwise."""
        if not name:
            raise Refuse("this verb needs a room: mem.py help")
        n = str(name).strip()
        n = re.sub(r"^/?r/", "", n, flags=re.I).strip("/")
        subs = self.subs()
        if n in subs:
            return n
        low = {s.lower(): s for s in subs}
        if n.lower() in low:
            return low[n.lower()]
        raise Refuse("no such room: %s%s" % (name, mean_hint(n, subs)))

    def room_row(self, sub):
        return next((x for x in self.rows("rooms") if x["sub"] == sub), None)

    # ---- overlay ------------------------------------------------------------------------------
    def scheme_files(self):
        frozen = current = None
        for f in ("scheme_v2.jsonl", "scheme_final.jsonl", "scheme.jsonl"):
            for d in ("", "scheme"):
                p = os.path.join(self.out, d, f)
                if os.path.exists(p) and frozen is None:
                    frozen = p
            if frozen:
                break
        for d in ("scheme", ""):
            p = os.path.join(self.out, d, "scheme_current.jsonl")
            if os.path.exists(p):
                current = p
                break
        return frozen, current

    def overlay(self):
        if "ov" in self._cache:
            return self._cache["ov"]
        ov = {"scheme_file": None, "frozen_file": None, "current_file": None, "scheme": {},
              "frozen": {}, "current": {}, "assign_file": None, "placed": {}, "chunk_of": {},
              "chunks": {}, "dim_of": {}, "dims": {}, "families": {}, "notes": []}
        frozen, current = self.scheme_files()
        rel = lambda p: os.path.relpath(p, self.out)
        if frozen:
            ov["frozen_file"] = rel(frozen)
            for r in jl(frozen):
                r = _norm_scheme_row(r)
                if r["id"]:
                    ov["frozen"][r["id"]] = r
        if current:
            ov["current_file"] = rel(current)
            for r in jl(current):
                r = _norm_scheme_row(r)
                if r["id"]:
                    ov["current"][r["id"]] = r
        ov["scheme"] = {k: dict(v) for k, v in ov["frozen"].items()}
        use_current = current and (not frozen or os.path.getmtime(current) > os.path.getmtime(frozen))
        if use_current:
            for k, v in ov["current"].items():
                ov["scheme"].setdefault(k, {}).update({x: y for x, y in v.items() if y not in (None, "", [])})
            ov["scheme_file"] = ov["current_file"] + (" over " + ov["frozen_file"] if frozen else "")
        else:
            ov["scheme_file"] = ov["frozen_file"]
        for r in jl(os.path.join(self.out, "families.jsonl")):
            for t in r.get("themes") or []:
                ov["families"][t] = r.get("family")
        for f in ("assignments_final.jsonl", "assign_final.jsonl"):
            p = os.path.join(self.out, f)
            if os.path.exists(p):
                ov["assign_file"] = f
                for r in jl(p):                      # last write wins on (sub, theme)
                    so = r.get("third_order") or r.get("second_order")
                    if isinstance(so, str):
                        so = [so]
                    ov["placed"][(r["sub"], r.get("theme_id") or r.get("case_theme"))] = so or []
                if f == "assign_final.jsonl":
                    ov["notes"].append("placements are from assign_final.jsonl, the adjudicated "
                                       "line; assignments_final.jsonl does not exist yet")
                break
        if not ov["assign_file"] and current:
            n = self._placed_from_current(ov)
            if n:
                ov["assign_file"] = ov["current_file"] + " members"
                ov["notes"].append("placements are the working grouping in %s (%d second-order "
                                   "themes), not a fleet's" % (ov["current_file"], n))
        for r in jl(os.path.join(self.out, "fourth", "fourth.jsonl")):
            if r.get("id"):
                ov["chunks"][r["id"]] = r
                for m in r.get("members", []):
                    ov["chunk_of"][m] = r["id"]
        for r in jl(os.path.join(self.out, "dimensions.jsonl")):
            if r.get("id"):
                ov["dims"][r["id"]] = r
                for m in r.get("members", []):
                    ov["dim_of"].setdefault(m, []).append(r["id"])
        if not ov["assign_file"]:
            ov["notes"].append("no placements yet: out/ holds no assignments file")
        self._cache["ov"] = ov
        return ov

    def _placed_from_current(self, ov):
        by_label = {(t["sub"], (t.get("second_order") or "").strip().lower()): t["theme_id"]
                    for t in self.rows("themes")}
        code_theme = {(c["sub"], c["code_id"]): c.get("theme_id") for c in self.rows("codes")}
        n = 0
        for tid, r in ov["current"].items():
            for m in r.get("members") or []:
                if not isinstance(m, dict) or not m.get("sub"):
                    continue
                th = m.get("theme_id") or by_label.get((m["sub"], (m.get("second_order") or "").strip().lower()))
                if not th:
                    th = next((code_theme.get((m["sub"], c)) for c in m.get("codes") or []
                               if code_theme.get((m["sub"], c))), None)
                if th:
                    ov["placed"].setdefault((m["sub"], th), [])
                    if tid not in ov["placed"][(m["sub"], th)]:
                        ov["placed"][(m["sub"], th)].append(tid)
                        n += 1
        return n

    def dims_of_third(self, s):
        ov = self.overlay()
        return ov["dim_of"].get(ov["chunk_of"].get(s), [])

    def placement(self, sub, theme_id):
        ov = self.overlay()
        so = ov["placed"].get((sub, theme_id), [])
        return [{"so": s, "name": ov["scheme"].get(s, {}).get("name"),
                 "chunk": ov["chunk_of"].get(s), "dims": self.dims_of_third(s)} for s in so]

    def known_third(self):
        ov = self.overlay()
        return set(ov["scheme"]) | {x for v in ov["placed"].values() for x in v}

    def check_id(self, key, what="id"):
        """Refuse an id that names nothing in the overlay, the model or the ledger."""
        ov = self.overlay()
        pool = set(self.known_third()) | set(ov["chunks"]) | set(ov["dims"])
        pool |= {r.get("id") for r in jl(os.path.join(self.out, "model", "elements.jsonl"))}
        pool |= {r.get("id") for r in jl(os.path.join(self.out, "model", "arrows.jsonl"))}
        led = jl(os.path.join(self.out, "adaptations.jsonl"))
        pool |= {l.get("element") for l in led} | {l.get("id") for l in led}
        keys = {"%s:%s:%s" % (l["op"], l.get("element"), (l.get("lift") or [None, None])[1]) for l in led}
        pool.discard(None)
        if key in pool or any(k == key or k.startswith(key) for k in keys):
            return
        raise Refuse("no such %s: %s is not a third- or fourth-order theme, a dimension, an element "
                     "or an adaptation key in out/%s" % (what, key, mean_hint(key, pool | keys)))


def fmt_place(pl):
    if not pl:
        return "unplaced"
    return "; ".join("%s%s%s%s" % (p["so"], " " + clip(p["name"], 40) if p["name"] else "",
                                    " ⊂ " + p["chunk"] if p["chunk"] else "",
                                    " ⊂ " + ",".join(p["dims"]) if p["dims"] else "") for p in pl)


def code_line(c):
    # participant words are not clipped: rule 3 requires a quote taken from this tier to be
    # verbatim, and a fleet or reader agent working from this page has no other access to the
    # untruncated text. The label is a summary the coder wrote and is clipped as before.
    where = "%s:%s" % (c.get("thread_id") or "?", c.get("coord") or "-")
    return "%-6s %-20s %-4s h%+7.2f %-18s @%-14s | %s | %s" % (
        c["code_id"], clip(c["sub"], 20), c.get("theme_id") or c.get("case_theme_id") or "?",
        c["hour"] if c.get("hour") is not None else float("nan"),
        clip(c.get("author") or "?", 18), where,
        clip((c.get("first_order") or c.get("label") or ""), 60), " ".join(str(c.get("text") or "").split()))


def tid_of(c):
    return c.get("theme_id") or c.get("case_theme_id")


def label_of(t):
    return t.get("second_order") or t.get("label") or ""


# ---- the store, one room --------------------------------------------------------------------
def v_room(st, a):
    sub = st.room(a.arg1)
    r = st.room_row(sub)
    if not r:
        raise Refuse("r/%s has concepts in the store but no line in rooms.jsonl" % sub)
    if a.size:
        forest, codes, themes = room_bytes(st, sub)
        return ["r/%s  bytes: forest %d  codes %d  second-order themes %d  total %d"
                % (sub, forest, codes, themes, forest + codes + themes),
                "(the payload one fleet agent reads at stage D, before the brief)"]
    th = [t for t in st.rows("threads") if t["sub"] == sub]
    cts = [t for t in st.rows("themes") if t["sub"] == sub]
    if a.json:
        row = {k: v for k, v in r.items() if not (a.no_canvas and k in CANVAS)}
        row["second_order_themes"] = [{"theme_id": t["theme_id"], "label": label_of(t),
                                       "n_codes": t.get("n_codes"),
                                       "placed": [p["so"] for p in st.placement(sub, t["theme_id"])]} for t in cts]
        row["threads"] = [t["thread_id"] for t in th]
        return [json.dumps(row, ensure_ascii=False)]
    L = ["r/%s  threads %s/%s coded (%s disposed, %s read in full, %s out of scope)  items in window %s (coded %s, share %s)"
         % (sub, r.get("threads_coded"), r.get("threads_total"), r.get("threads_disposed"),
            r.get("threads_read_in_full"), r.get("threads_out_of_scope"),
            r.get("items_in_window"), r.get("items_coded"), r.get("item_coded_share")),
         "first code h%+.2f  median h%+.2f  last h%+.2f  coded authors %s  top1 %s  herfindahl %s"
         % (r.get("onset_first_code_hour") or 0, r.get("onset_median_code_hour") or 0,
            r.get("onset_last_code_hour") or 0, r.get("coded_authors"), r.get("top1_share"),
            r.get("herfindahl")),
         "subreddits named %s  off-platform pointers %s  pointers %s"
         % (r.get("n_subreddits_named"), r.get("n_off_platform"), r.get("pointers")),
         "forest: %s" % json.dumps(r.get("forest"))]
    L += (["made: withheld on this page (--no-canvas; rule 7)"] if a.no_canvas else canvas_lines(r))
    L.append("")
    L.append("threads (%d):" % len(th))
    for t in sorted(th, key=lambda t: t.get("opened_hour") or 0):
        op = "↑?" if t.get("op_score") is None else "↑%d" % t["op_score"]
        if t.get("op_stickied"):
            op += " [sticky]"
        if t.get("op_distinguished"):
            op += " [%s]" % t["op_distinguished"]
        if t.get("op_flair"):
            op += " {%s}" % clip(t["op_flair"], 20)
        L.append("  %-8s h%+7.2f  %2d/%-3d coded  depth %d  %-16s %s  %s%s" % (
            t["thread_id"], t.get("opened_hour") or 0, t.get("n_coded", t.get("n_items_coded", 0)), t["n_items"],
            t.get("depth", 0), clip(t.get("opener"), 16), clip(t.get("title"), 60), op,
            "  [opener also in %s]" % ",".join(t["opener_elsewhere"][:4])
            if t.get("opener_elsewhere") else ""))
    L.append("")
    L.append("second-order themes (%d):" % len(cts))
    for t in cts:
        L.append("  %-4s %2d codes  h%+6.1f..%+6.1f  %s  -> %s" % (
            t["theme_id"], t.get("n_codes", len(t.get("code_ids", []))), t.get("first_hour") or 0, t.get("last_hour") or 0,
            clip(label_of(t), 70), fmt_place(st.placement(t["sub"], t["theme_id"]))))
    return L


def _read_lines(p):
    return open(p, encoding="utf-8").read().splitlines()


def v_case(st, a):
    sub = st.room(a.arg1)
    p = os.path.join(st.root, "package", sub, "case.md")
    if not os.path.exists(p):
        raise Refuse("no case.md for r/%s in package/%s/" % (sub, sub))
    return _read_lines(p)


def v_brief(st, a):
    sub = st.room(a.arg1)
    p = os.path.join(st.root, "package", sub, "brief.md")
    if not os.path.exists(p):
        p = os.path.join(st.S, "briefs", "%s.md" % sub)
    if not os.path.exists(p):
        raise Refuse("no brief for r/%s" % sub)
    return _read_lines(p)


def v_forest(st, a):
    sub = st.room(a.arg1)
    p = os.path.join(st.root, "trees", "%s.md" % sub)
    if not os.path.exists(p):
        raise Refuse("no forest for r/%s (trees/%s.md is absent)" % (sub, sub))
    txt = _read_lines(p)
    if not a.arg2:
        return txt
    ids = [m.group(1) for m in (re.match(r"^=== THREAD ([^:\s]+):", l) for l in txt) if m]
    if a.arg2 not in ids:
        raise Refuse("thread %s is not in the forest of r/%s (%d threads)%s"
                     % (a.arg2, sub, len(ids), mean_hint(a.arg2, ids)))
    out, on = [], False
    for line in txt:
        if line.startswith("=== THREAD "):
            on = line.startswith("=== THREAD %s:" % a.arg2)
        if on or line.startswith("#"):
            out.append(line)
    return out


def v_when(st, a):
    sub = st.room(a.arg1)
    its = [i for i in st.rows("items") if i["sub"] == sub]
    if not its:
        raise Refuse("no items for r/%s in items.jsonl" % sub)
    return when_lines(sub, its)


def when_lines(sub, its, mx=None):
    bins, outside = hour_bins(i["hour"] for i in its if i.get("codes"))
    scale = "; drawn on the shared scale, max %d" % mx if mx else ""
    return ["r/%s coded items by 4-hour bin, h0..h99 (max %d per bin; %d outside the window%s)"
            % (sub, max(bins), outside, scale), spark(bins, mx)] + AXIS + [" ".join("%d" % b for b in bins)]


def room_bytes(st, sub):
    fp = os.path.join(st.root, "trees", "%s.md" % sub)
    forest = os.path.getsize(fp) if os.path.exists(fp) else 0
    codes = sum(len(code_line(c).encode("utf-8")) + 1 for c in st.rows("codes") if c["sub"] == sub)
    themes = sum(len(json.dumps(t, ensure_ascii=False).encode("utf-8")) + 1 for t in st.rows("themes") if t["sub"] == sub)
    return forest, codes, themes


def _manifest_caveat(st):
    for p in (os.path.join(st.root, "package", "canvas", "DATA-manifest-canvas.md"),
              os.path.join(st.root, "package", "DATA-manifest-canvas.md")):
        if os.path.exists(p):
            t = " ".join(open(p, encoding="utf-8").read().split())
            m = re.search(r"\*\*(A per-community rate is fine; a canvas-wide total is not\.)\*\*", t)
            if m:
                return "%s Regions overlap and a contested pixel counts for every room that claims it (%s)." % (
                    m.group(1), os.path.relpath(p, st.root))
    return ("A per-community rate is fine; a canvas-wide total is not. Regions overlap and a contested "
            "pixel counts for every room that claims it (DATA-manifest-canvas.md).")


def pixel_sums(st):
    if "px" in st._cache:
        return st._cache["px"]
    out = {}
    p = os.path.join(st.root, "package", "pixels.csv")
    if not os.path.exists(p):
        p = os.path.join(st.root, "package", "canvas", "pixels.csv")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                s = out.setdefault(r["sub"], {"any": 0.0, "pre": 0.0, "window": 0.0, "hours": 0})
                for k, col in (("any", "px_in_region_any"), ("pre", "px_by_pre_members"),
                               ("window", "px_by_window_members")):
                    try:
                        s[k] += float(r.get(col) or 0)
                    except ValueError:
                        pass
                s["hours"] += 1
    st._cache["px"] = (out, p if os.path.exists(p) else None)
    return st._cache["px"]


def px_shares(st, sub):
    sums, _ = pixel_sums(st)
    s = sums.get(sub)
    if not s or not s["any"]:
        return None, None
    return round(s["window"] / s["any"], 3), round(s["pre"] / s["any"], 3)


def artworks_of(st, sub):
    p = os.path.join(st.root, "package", "canvas", "artworks.jsonl")
    rows = jl(p)
    low = sub.lower()
    return [w for w in rows if low in [str(x).lower() for x in (w.get("subreddits") or []) + (w.get("subreddits_in_frame") or [])]], os.path.exists(p)


def canvas_block(st, sub, with_caveat=True):
    r = st.room_row(sub) or {}
    L = ["r/%s on the canvas" % sub] + canvas_lines(r)
    arts, have = artworks_of(st, sub)
    if not have:
        L.append("artworks: package/canvas/artworks.jsonl is absent")
    else:
        L.append("artworks linked (%d):" % len(arts))
        for w in arts:
            hrs = w.get("placements_by_hour_0_96") or []
            bins = [0] * NBINS
            for h, n in enumerate(hrs):
                if 0 <= h < 4 * NBINS:
                    bins[h // 4] += n or 0
            L.append("  %s %s  pixels %s  placements %s (smallest polygon %s)  placers %s  h%s..h%s%s"
                     % (w.get("artwork_id"), clip(w.get("name"), 40), w.get("pixels_covered"),
                        w.get("placements"), w.get("placements_smallest_polygon"),
                        w.get("distinct_placers"), w.get("first_hour"), w.get("last_hour"),
                        "  shared with %s" % ",".join(x for x in w.get("subreddits") or [] if str(x).lower() != sub.lower())
                        if len(w.get("subreddits") or []) > 1 else ""))
            L.append("  " + spark(bins) + "  max %d per 4 hours" % max(bins))
        if arts:
            L += ["  " + x for x in AXIS]
    sums, pp = pixel_sums(st)
    s = sums.get(sub)
    if pp is None:
        L.append("pixels: package/pixels.csv is absent")
    elif not s:
        L.append("pixels: no rows for r/%s in pixels.csv" % sub)
    else:
        w, pre = px_shares(st, sub)
        L.append("pixels (%d hours, -16..72): in region %d; by window members %d (share %s); by "
                 "pre-event members %d (share %s)" % (s["hours"], s["any"], s["window"], w, s["pre"], pre))
    if with_caveat:
        L.append("caveat: " + _manifest_caveat(st))
        L.append("rule 7: you may use this; declare where it shaped a reading.")
    return L


TIE_NAMES = ("both-ways", "one-way", "shared", "overlap", "border", "-")


def _tie_rank(r):
    """The ranking of ties: named both ways, named one way, shared artwork, overlap, border."""
    m = r.get("mention")
    if m:
        return 0 if m.get("reciprocal") else 1
    if r.get("shared_artworks"):
        return 2
    if r.get("overlap_px"):
        return 3
    return 4 if r.get("border_px") else 5


def v_neighbours(st, a):
    """neighbours <sub> [--kind canvas|mention|shared] [--top N] | neighbours --summary"""
    rows = st.rows("neighbours")
    if not rows:
        raise Refuse("package/store/neighbours.jsonl is absent or empty: the build had no atlas outlines "
                     "(INPUT/canvas/atlas_2017.json); only the mention graph (mem.py pairs, relations.jsonl) is here")
    if a.summary or not a.arg1:
        deg = collections.Counter(r["sub"] for r in rows)
        L = ["neighbours.jsonl: %d ordered pairs over %d rooms; shared artwork %d, border %d, overlap %d, named %d"
             % (len(rows), len(deg), sum(1 for r in rows if r["shared_artworks"]), sum(1 for r in rows if r["border_px"]),
                sum(1 for r in rows if r["overlap_px"]), sum(1 for r in rows if r["mention"]))]
        L.append("most neighbours: " + ", ".join("%s %d" % kv for kv in deg.most_common(a.top or 20)))
        L.append("the rooms of the frame with none: %d" % len(set(st.subs()) - set(deg)))
        return L
    sub = st.room(a.arg1)
    sel = [r for r in rows if r["sub"] == sub]
    k = (a.kind or "all").lower()
    if k == "canvas":
        sel = [r for r in sel if r["border_px"] or r["overlap_px"] or r["shared_artworks"]]
    elif k == "mention":
        sel = [r for r in sel if r["mention"]]
    elif k == "shared":
        sel = [r for r in sel if r["shared_artworks"]]
    elif k != "all":
        raise Refuse("--kind is canvas, mention, shared or all")
    sel.sort(key=lambda r: (_tie_rank(r), -((r["mention"] or {}).get("n") or 0), -len(r["shared_artworks"]),
                            -(r["overlap_px"] + r["border_px"]), r["other"]))
    if a.top:
        sel = sel[:a.top]
    if a.json:
        return [json.dumps(r, ensure_ascii=False) for r in sel]
    L = ["r/%s: %d neighbours (%s), ranked: named both ways, named one way (a claim), shared artwork, overlap, "
         "border; the last three are the canvas, the outcome" % (sub, len(sel), k),
         "  %-9s %-22s %-10s %7s %8s  %s" % ("tie", "other", "shared", "border", "overlap", "named")]
    for r in sel:
        m = r["mention"]
        L.append("  %-9s %-22s %-10s %7d %8d  %s" % (TIE_NAMES[_tie_rank(r)], clip(r["other"], 22),
                                                  ",".join(map(str, r["shared_artworks"])) or "-",
                                             r["border_px"], r["overlap_px"],
                                             ("%s %s x%s%s" % (m["direction"], m["label"], m["n"], ", reciprocal" if m["reciprocal"] else "")) if m else "-"))
    L.append("caveat: the atlas outline is one annotator's, drawn after the event; a border is where two outlines "
             "meet, not a negotiation. rule 7: declare where it shaped a reading.")
    return L


def v_canvas(st, a):
    return canvas_block(st, st.room(a.arg1))


def v_note(st, a):
    sub = st.room(a.arg1)
    p = os.path.join(st.out, "rooms", "%s.md" % sub)
    if not os.path.exists(p):
        return ["no note yet: %s" % os.path.relpath(p, st.root)]
    return _read_lines(p)


# ---- concepts and themes ------------------------------------------------------------------------
def _third_id(st, key):
    ov = st.overlay()
    if key not in st.known_third():
        raise Refuse("no third-order theme %s in %s%s" % (key, ov["scheme_file"] or "out/ (no scheme yet)",
                                                          mean_hint(key, st.known_third())))
    return key


def v_codes(st, a):
    codes = st.rows("codes")
    ov = st.overlay()
    second = a.second or a.case_theme
    third = a.third or a.theme
    fourth = a.fourth or a.chunk
    if a.sub:
        sub = st.room(a.sub)
        if second and not any(t["sub"] == sub and t["theme_id"] == second for t in st.rows("themes")):
            raise Refuse("no second-order theme %s in r/%s%s" % (
                second, sub, mean_hint(second, [t["theme_id"] for t in st.rows("themes") if t["sub"] == sub])))
        sel = [c for c in codes if c["sub"] == sub and (not second or tid_of(c) == second)]
        head = "concepts of r/%s%s" % (sub, " second-order theme " + second if second else "")
    elif third:
        _third_id(st, third)
        keys = {k for k, v in ov["placed"].items() if third in v}
        sel = [c for c in codes if (c["sub"], tid_of(c)) in keys]
        head = "concepts on %s %s (%d second-order themes; %s)" % (
            third, clip(ov["scheme"].get(third, {}).get("name"), 50), len(keys),
            ov["assign_file"] or "no placements")
    elif fourth:
        if fourth not in ov["chunks"]:
            raise Refuse("no fourth-order theme %s in fourth/fourth.jsonl%s" % (fourth, mean_hint(fourth, ov["chunks"])))
        members = set(ov["chunks"][fourth].get("members", []))
        keys = {k for k, v in ov["placed"].items() if set(v) & members}
        sel = [c for c in codes if (c["sub"], tid_of(c)) in keys]
        head = "concepts under %s %s (third-order %s; %d second-order themes)" % (
            fourth, clip(ov["chunks"][fourth].get("name"), 50), ",".join(sorted(members)), len(keys))
    elif a.dimension:
        if a.dimension not in ov["dims"]:
            raise Refuse("no dimension %s in dimensions.jsonl%s" % (a.dimension, mean_hint(a.dimension, ov["dims"])))
        t4 = set(ov["dims"][a.dimension].get("members", []))
        t3 = {s for s, c in ov["chunk_of"].items() if c in t4}
        keys = {k for k, v in ov["placed"].items() if set(v) & t3}
        sel = [c for c in codes if (c["sub"], tid_of(c)) in keys]
        head = "concepts under %s %s (fourth-order %s; %d second-order themes)" % (
            a.dimension, clip(ov["dims"][a.dimension].get("label") or ov["dims"][a.dimension].get("name"), 40),
            ",".join(sorted(t4)), len(keys))
    elif a.grep:
        rx = re.compile(a.grep, re.I)
        sel = [c for c in codes if rx.search(" ".join(str(c.get(k) or "") for k in
                                                       ("first_order", "label", "text", "note", "coder_note")))]
        head = "concepts matching /%s/" % a.grep
    else:
        raise Refuse("codes needs --sub, --third, --fourth, --dimension or --grep")
    sel.sort(key=lambda c: (c["sub"], c["hour"] if c.get("hour") is not None else 1e9))
    rooms = len({c["sub"] for c in sel})
    if a.by_room:
        per = collections.OrderedDict()
        for c in sel:
            p = per.setdefault(c["sub"], [0, None])
            p[0] += 1
            if c.get("hour") is not None and (p[1] is None or c["hour"] < p[1]):
                p[1] = c["hour"]
        L = ["%s: %d concepts in %d rooms" % (head, len(sel), rooms), "%-24s %6s  %s" % ("room", "n", "first hour")]
        for s, (n, h) in sorted(per.items(), key=lambda kv: (-kv[1][0], kv[0])):
            L.append("%-24s %6d  %s" % (s, n, "h%+.2f" % h if h is not None else "-"))
        return L
    if a.json:
        return [json.dumps(c, ensure_ascii=False) for c in sel]
    return ["%s: %d concepts in %d rooms" % (head, len(sel), rooms)] + [code_line(c) for c in sel]


def _find_theme(st, sub, key):
    cts = [t for t in st.rows("themes") if t["sub"] == sub]
    exact = [t for t in cts if t["theme_id"] == key or label_of(t) == key]
    if exact:
        return exact
    k = key.lower()
    return [t for t in cts if k in label_of(t).lower()]


def v_theme(st, a):
    sub, _, key = (a.arg1 or "").partition("/")
    if not key:
        raise Refuse("theme needs <sub>/<tNN or label words>")
    sub = st.room(sub)
    cts = _find_theme(st, sub, key)
    if not cts:
        allt = [t for t in st.rows("themes") if t["sub"] == sub]
        hint = nearest(key, [t["theme_id"] for t in allt] + [label_of(t) for t in allt])
        raise Refuse("no second-order theme %r in r/%s (%d themes)%s" % (
            key, sub, len(allt), " (did you mean %s?)" % hint[0] if hint else ""))
    if len(cts) > 1:
        return ["%d second-order themes of r/%s match %r; name one by id:" % (len(cts), sub, key)] + \
            ["  %s/%-4s %2s codes  %s" % (sub, t["theme_id"], t.get("n_codes", ""), clip(label_of(t), 90)) for t in cts]
    t = cts[0]
    codes = {c["code_id"]: c for c in st.rows("codes") if c["sub"] == sub}
    L = ["r/%s %s  %s  (%d codes, h%+.1f..%+.1f, threads %s)" % (
        sub, t["theme_id"], label_of(t), t.get("n_codes", len(t.get("code_ids", []))), t.get("first_hour") or 0,
        t.get("last_hour") or 0, ",".join(t.get("threads", []))),
         "placed: " + fmt_place(st.placement(sub, t["theme_id"])), "",
         "note: " + (t.get("theme_note") or ""), ""]
    for cid in t.get("code_ids") or [c["code_id"] for c in codes.values() if tid_of(c) == t["theme_id"]]:
        c = codes.get(cid)
        if c:
            L.append(code_line(c))
            if c.get("coder_note"):
                L.append("       coder: " + clip(c["coder_note"], 130))
    return L


def v_themes(st, a):
    rooms = None
    if a.rooms:
        rooms = [st.room(x) for x in a.rooms.split(",") if x.strip()]
    elif not a.grep:
        raise Refuse("themes needs --grep <re> or --rooms a,b")
    rx = re.compile(a.grep, re.I) if a.grep else None
    sel = [t for t in st.rows("themes") if (rooms is None or t["sub"] in rooms)
           and (rx is None or rx.search(label_of(t) + " " + str(t.get("theme_note") or "")))]
    if a.json:
        return [json.dumps(t, ensure_ascii=False) for t in sel]
    per = collections.Counter(t["sub"] for t in sel)
    L = ["second-order themes%s%s: %d in %d rooms" % (" matching /%s/" % a.grep if a.grep else "",
                                                      " in " + ",".join(rooms) if rooms else "", len(sel), len(per))]
    top = sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))
    L.append("per room (top 20 of %d): " % len(top) + ", ".join("%s %d" % kv for kv in top[:20]))
    for t in sel:
        where = ""
        if rx and not rx.search(label_of(t)):
            where = "  [note]"
        L.append("  %s/%-4s %3s codes  %s%s  -> %s" % (t["sub"], t["theme_id"], t.get("n_codes", ""),
                                                       clip(label_of(t), 80), where,
                                                       fmt_place(st.placement(t["sub"], t["theme_id"]))))
    return L


def v_after(st, a):
    sub, _, cid = (a.arg1 or "").partition("/")
    sub = st.room(sub)
    codes = {c["code_id"]: c for c in st.rows("codes") if c["sub"] == sub}
    if cid not in codes:
        raise Refuse("no concept %s in r/%s%s" % (cid, sub, mean_hint(cid, codes)))
    tr = [r for r in st.rows("transitions") if r["sub"] == sub]
    ans = [r for r in tr if cid in r["from_codes"]]
    was = [r for r in tr if cid in r["to_codes"]]
    L = [code_line(codes[cid]), ""]
    L.append("answered by (%d):" % len(ans))
    for r in sorted(ans, key=lambda r: r["interval_s"]):
        for x in r["to_codes"]:
            L.append("  +%-8s hops %d  %s  %s" % ("%.0fs" % r["interval_s"], r["hops"],
                                                  "same author" if r["same_author"] else "        ",
                                                  code_line(codes[x]) if x in codes else x))
    L.append("was an answer to (%d):" % len(was))
    for r in was:
        for x in r["from_codes"]:
            L.append("  -%-8s hops %d  %s" % ("%.0fs" % r["interval_s"], r["hops"],
                                              code_line(codes[x]) if x in codes else x))
    L.append("")
    L.append("limit: " + (tr[0]["limit"] if tr else "a reply is a reply: posted after, not caused by"))
    return L


def v_pairs(st, a):
    ov = st.overlay()
    level = LEVELS.get((a.level or "second").lower())
    if not level:
        raise Refuse("no such level: %s; one of second, third, fourth, dimension (old names "
                      "case_theme, theme, chunk still work)" % a.level)
    sub = st.room(a.sub) if a.sub else None

    def lift(sub_, tids):
        if level == "second":
            return {"%s/%s" % (sub_, t) for t in tids}
        out = set()
        for t in tids:
            for s in ov["placed"].get((sub_, t), []):
                if level == "third":
                    out.add(s)
                elif level == "fourth":
                    out.add(ov["chunk_of"].get(s) or "∅")
                else:
                    out |= set(st.dims_of_third(s) or ["∅"])
        return out
    cnt, rooms = collections.Counter(), collections.defaultdict(set)
    n = n_lifted = 0
    for r in st.rows("transitions"):
        if sub and r["sub"] != sub:
            continue
        n += 1
        xs = lift(r["sub"], r.get("from_case_themes", r.get("from_themes", [])))
        ys = lift(r["sub"], r.get("to_case_themes", r.get("to_themes", [])))
        if xs and ys:
            n_lifted += 1
        for x in xs:
            for y in ys:
                cnt[(x, y)] += 1
                rooms[(x, y)].add(r["sub"])
    top = a.top or 40
    where = " in r/" + sub if sub else ""
    if level == "second":
        head = ("transition pairs at level second%s: %d transitions, %d distinct pairs (second-order "
                "themes are the coder's; no placement is needed)" % (where, n, len(cnt)))
    elif not ov["assign_file"]:
        head = ("transition pairs at level %s%s: %d transitions, none lifted: no placements yet (out/ "
                "holds no assignments file and no working grouping)" % (level, where, n))
    else:
        head = ("transition pairs at level %s%s: %d transitions, %d with both ends placed, %d distinct "
                "pairs (placements from %s)" % (level, where, n, n_lifted, len(cnt), ov["assign_file"]))
    L = [head, "%-34s %-34s %6s %6s" % ("from", "to", "n", "rooms")]
    for (x, y), c in cnt.most_common(top):
        L.append("%-34s %-34s %6d %6d" % (clip(x, 34), clip(y, 34), c, len(rooms[(x, y)])))
    L.append("")
    L.append("limit: a reply is a reply: posted after, not caused by. Counts are of coded turns "
             "answering coded turns; rule 4 says counts are of communities, and the rooms column "
             "is the one to report.")
    return L


# ---- the room facts -----------------------------------------------------------------------------
def _field(st, r, f):
    if f in ("px_window_share", "px_pre_share"):
        w, p = px_shares(st, r["sub"])
        return w if f == "px_window_share" else p
    v = r
    for part in f.split("."):
        v = v.get(part) if isinstance(v, dict) else None
    return v


def _num(v):
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _quart(xs):
    xs = sorted(xs)

    def q(p):
        k = (len(xs) - 1) * p
        lo, hi = int(math.floor(k)), int(math.ceil(k))
        return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
    return q(0), q(.25), q(.5), q(.75), q(1)


WHERE = re.compile(r"^\s*([\w.]+)\s*(>=|<=|==|!=|>|<)\s*(.+?)\s*$")


def _passes(st, r, conds):
    for f, op, v in conds:
        x = _field(st, r, f)
        if v.lower() in ("null", "none"):
            ok = (x is None) if op == "==" else (x is not None) if op == "!=" else False
        else:
            xn, vn = _num(x), _num(v)
            if xn is not None and vn is not None:
                a_, b_ = xn, vn
            else:
                a_, b_ = str(x), v.strip("\"'")
                if op not in ("==", "!="):
                    return False
            ok = {">": a_ > b_, "<": a_ < b_, ">=": a_ >= b_, "<=": a_ <= b_, "==": a_ == b_, "!=": a_ != b_}[op]
        if not ok:
            return False
    return True


def fmtv(v):
    if isinstance(v, float):
        return ("%.3f" % v).rstrip("0").rstrip(".") if v != int(v) else "%d" % v
    return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)


def v_facts(st, a):
    rows = st.rows("rooms")
    if not rows:
        raise Refuse("rooms.jsonl holds no rooms")
    fields = collections.OrderedDict()
    for r in rows:
        for k, v in r.items():
            if isinstance(v, dict):
                for k2 in v:
                    fields.setdefault("%s.%s" % (k, k2), None)
            else:
                fields.setdefault(k, None)
    fields.setdefault("px_window_share", None)
    fields.setdefault("px_pre_share", None)
    conds = []
    for w in a.where or []:
        m = WHERE.match(w)
        if not m:
            raise Refuse("--where %r: write it as F>v, F<v, F>=v, F<=v, F==v or F!=v (v may be null)" % w)
        if m.group(1) not in fields:
            raise Refuse("no field %s in rooms.jsonl%s" % (m.group(1), mean_hint(m.group(1), fields)))
        conds.append(m.groups())
    rows = [r for r in rows if _passes(st, r, conds)]
    wtxt = (" where " + " and ".join("".join(c) for c in conds)) if conds else ""
    if a.slope:
        x, y = a.slope
        for f in (x, y):
            if f not in fields:
                raise Refuse("no field %s in rooms.jsonl%s" % (f, mean_hint(f, fields)))
        pts = [(math.log(_num(_field(st, r, x))), math.log(_num(_field(st, r, y)))) for r in rows
               if (_num(_field(st, r, x)) or 0) > 0 and (_num(_field(st, r, y)) or 0) > 0]
        L = ["log-log OLS slope of %s on %s%s: %d of %d rooms have both > 0" % (y, x, wtxt, len(pts), len(rows))]
        if len(pts) < 3:
            return L + ["too few rooms for a slope (need 3)"]
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        sxx = sum((p[0] - mx) ** 2 for p in pts)
        if not sxx:
            return L + ["%s does not vary over these rooms; no slope" % x]
        b = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
        c = my - b * mx
        ss = sum((p[1] - my) ** 2 for p in pts)
        r2 = 1 - sum((p[1] - (c + b * p[0])) ** 2 for p in pts) / ss if ss else float("nan")
        return L + ["slope %.3f  intercept %.3f  r2 %.3f  (log %s = %.3f + %.3f log %s)" % (b, c, r2, y, c, b, x)]
    if not a.field:
        L = ["rooms.jsonl: %d rooms%s; %d fields (non-null count; min..max where numeric)" % (len(rows), wtxt, len(fields))]
        for f in fields:
            vals = [_field(st, r, f) for r in rows]
            nn = [v for v in vals if v is not None]
            nums = [_num(v) for v in nn if _num(v) is not None and not isinstance(v, str)]
            L.append("  %-36s %4d%s" % (f, len(nn), "  %s..%s" % (fmtv(min(nums)), fmtv(max(nums))) if nums and len(nums) == len(nn) else ""))
        return L
    f = a.field
    if f not in fields:
        raise Refuse("no field %s in rooms.jsonl%s" % (f, mean_hint(f, fields)))
    vals = [(r["sub"], _field(st, r, f)) for r in rows]
    nulls = [s for s, v in vals if v is None]
    if a.nulls:
        return ["%s is null in %d of %d rooms%s:" % (f, len(nulls), len(vals), wtxt)] + ["  " + s for s in nulls]
    have = [(s, v) for s, v in vals if v is not None]
    nums = [(s, _num(v)) for s, v in have if _num(v) is not None and not isinstance(v, str)]
    numeric = bool(have) and len(nums) == len(have)
    if a.summary:
        L = ["%s over %d rooms%s: n %d, nulls %d" % (f, len(vals), wtxt, len(have), len(nulls))]
        if numeric and nums:
            q = _quart([v for _, v in nums])
            L.append("min %s  q1 %s  median %s  q3 %s  max %s  mean %s" % tuple(
                fmtv(x) for x in q + (sum(v for _, v in nums) / len(nums),)))
        else:
            c = collections.Counter(fmtv(v) for _, v in have)
            L += ["  %-40s %d" % (clip(k, 40), n) for k, n in c.most_common(a.top or 20)]
        return L
    desc = (a.sort or "desc") == "desc"
    if numeric:
        srt = sorted(nums, key=lambda kv: kv[1], reverse=desc)
    else:
        srt = sorted(have, key=lambda kv: str(kv[1]), reverse=desc)
    if a.top:
        srt = srt[:a.top]
    if a.json:
        if not (a.sort or a.top):
            return [json.dumps({"sub": s, f: v}, ensure_ascii=False) for s, v in vals]
        return [json.dumps({"sub": s, f: v}, ensure_ascii=False) for s, v in srt]
    L = ["%s, %s, %d rooms with a value%s (%d null; --nulls names them)" % (f, "descending" if desc else "ascending",
                                                                           len(have), wtxt, len(nulls))]
    L += ["  %-24s %s" % (s, fmtv(v)) for s, v in srt]
    return L


# ---- your own files ------------------------------------------------------------------------------
NOTE_FIELD = re.compile(r"^([a-z][a-z ]{0,14}):\s")


def v_notes(st, a):
    if not a.grep:
        raise Refuse("notes needs --grep <re> [--field <name>]")
    d = os.path.join(st.out, "rooms")
    if not os.path.isdir(d):
        raise Refuse("no room notes yet: %s is absent" % os.path.relpath(d, st.root))
    rx = re.compile(a.grep, re.I)
    L, hits, rooms, seen_fields = [], 0, set(), set()
    for fn in sorted(os.listdir(d)):
        if fn.startswith("_") or not fn.endswith(".md"):
            continue
        sub, field = fn[:-3], "header"
        for line in open(os.path.join(d, fn), encoding="utf-8"):
            line = line.rstrip("\n")
            m = NOTE_FIELD.match(line)
            if m:
                field = m.group(1).strip()
            elif line.startswith("#"):
                field = "header"
            seen_fields.add(field)
            if a.field and field != a.field.lower():
                continue
            if rx.search(line):
                hits += 1
                rooms.add(sub)
                L.append("%-20s %-10s %s" % (clip(sub, 20), field, clip(line.strip(), 150)))
    if a.field and a.field.lower() not in seen_fields:
        raise Refuse("no note line of the form %s:%s" % (a.field, mean_hint(a.field, seen_fields - {"header"})))
    return ["room notes matching /%s/%s: %d lines in %d rooms" % (a.grep, " in " + a.field if a.field else "", hits, len(rooms))] + L


def _order_file(st, subs):
    """out/order-A1.txt: one line per room, `<block><TAB><sub>` (or `<sub>`), in reading order."""
    p = os.path.join(st.out, "order-A1.txt")
    if not os.path.exists(p):
        return None, {}
    low = {s.lower(): s for s in subs}
    order, block = [], {}
    for line in open(p, encoding="utf-8"):
        f = line.strip().split("\t") if "\t" in line else line.split()
        if not f or f[0].startswith("#"):
            continue
        name = f[-1].strip().lower()
        s = low.get(name[2:] if name.startswith("r/") else name)
        if s and s not in order:
            order.append(s)
            block[s] = f[0] if len(f) > 1 else ""
    return (order or None), block


def _declared_order(st, subs):
    o, _ = _order_file(st, subs)
    if o:
        return o, "declared in out/order-A1.txt"
    return None, "out/order-A1.txt is absent or names no room of the analysed set"


def _next_b1(st, analysed):
    """Stage B1: the next room the stopping rule asks for (tools/saturation.py): the seeded random order,
    rounds, markers, the draw, then the PI's decision."""
    import vlib
    import saturation
    order, done, left = vlib.b1_progress(st.out, st.rows("themes"), set(analysed))
    if order is None:
        return ["no rooms to read: the analysed set is empty (dropped.jsonl)"]
    R = saturation.replay(st.root, st.out, "B1")
    L = saturation.status_lines(R)
    if R["next"] and left.get(R["next"]):
        L.append("r/%s: %d second-order theme(s) not yet placed: %s" % (R["next"], len(left[R["next"]]),
                                                                    ", ".join(map(str, left[R["next"]][:8]))))
    return L


def v_next(st, a):
    subs = st.subs()
    dropped = {d.get("sub") for d in jl(os.path.join(st.out, "dropped.jsonl"))}
    analysed = [s for s in subs if s not in dropped]
    if str(a.stage).upper() == "B1":
        return _next_b1(st, analysed)
    order, why = _declared_order(st, analysed)
    if order is None:
        return ["no declared order yet (%s): write out/order-A1.txt, one line per room, `<block><TAB><sub>`" % why]
    _, block = _order_file(st, analysed)
    def _is_noted(s):
        p = os.path.join(st.out, "rooms", "%s.md" % s)
        return os.path.exists(p) and os.path.getsize(p) >= 200      # under 200 bytes is a placeholder
    noted = [s for s in order if _is_noted(s)]
    pending = [s for s in order if s not in noted]
    last = max((order.index(s) for s in noted), default=-1)
    gaps = [s for s in order[:last] if s not in noted] if last >= 0 else []
    L = []
    if pending:
        s = pending[0]
        L.append("next: %s%s   (%d of %d noted; order %s)" % (s, "  block %s" % block[s] if block.get(s) else "",
                                                             len(noted), len(order), why))
    else:
        L.append("every room of the declared order has a note (%d)" % len(order))
    if gaps:
        L.append("skipped: %d room(s) before the last one noted have no note: %s" % (len(gaps), ", ".join(gaps[:10])))
    return L


def v_progress(st, a):
    subs = st.subs()
    dp = os.path.join(st.out, "dropped.jsonl")
    dropped = {d.get("sub") for d in jl(dp)}
    analysed = [s for s in subs if s not in dropped]
    order, why = _declared_order(st, analysed)
    if order is None:
        order, why = sorted(analysed), "sorted (%s)" % why
    else:
        rest = sorted(s for s in analysed if s not in order)
        if rest:
            why += "; %d rooms outside it appended, sorted" % len(rest)
        order += rest
    stage = a.stage
    diary = [l for l in _diary_lines(st) if str(l.get("stage")) == stage]
    opened = {}
    last = None
    for l in diary:
        if l.get("kind") == "opened":
            for i in l.get("ids") or []:
                try:
                    s = st.room(i)
                except Refuse:
                    continue
                opened[s] = l.get("t")
                last = (s, l.get("t"))
    status = {}
    for s in order:
        np_ = os.path.join(st.out, "rooms", "%s.md" % s)
        noted = os.path.exists(np_) and os.path.getsize(np_) >= 200     # as next and the stopping rule count it
        status[s] = "noted" if noted else "read" if s in opened else "pending"
    c = collections.Counter(status.values())
    L = ["progress at stage %s: %d rooms in the analysed set (%d dropped); order %s" % (stage, len(order), len(dropped & set(subs)), why),
         "noted %d, read and not noted %d, pending %d; last opened: %s" % (
             c["noted"], c["read"], c["pending"], "%s at %s" % last if last else "none")]
    nxt = next((s for s in order if status[s] == "pending"), None)
    if nxt:
        L.append("next in the order: %s" % nxt)
    if a.plan:
        cap = int(float(a.plan) * 1e6)
        blocks, cur, size = [], [], 0
        for s in (x for x in order if status[x] == "pending"):
            b = sum(room_bytes(st, s))
            if cur and size + b > cap:
                blocks.append((cur, size))
                cur, size = [], 0
            cur.append(s)
            size += b
        if cur:
            blocks.append((cur, size))
        L.append("plan: the pending rooms in blocks of about %s MB (forest, codes and themes bytes; a room "
                 "above the cap is a block of its own): %d blocks" % (a.plan, len(blocks)))
        L += ["  block %d  %.2f MB  %d rooms: %s" % (k, sz / 1e6, len(b), ", ".join(b)) for k, (b, sz) in enumerate(blocks, 1)]
        return L
    for i, s in enumerate(order, 1):
        L.append("%4d. %-24s %-8s%s" % (i, s, status[s], "  opened %s" % opened[s] if s in opened else ""))
    return L


def v_scheme(st, a):
    ov = st.overlay()
    if not ov["scheme"]:
        raise Refuse("no scheme yet: out/ holds no scheme_current.jsonl (out/scheme/ or out/) and no frozen scheme")
    members = collections.Counter()
    for (s, t), v in ov["placed"].items():
        for x in v:
            members[x] += 1
    if a.arg1:
        tid = a.arg1
        if tid not in ov["scheme"]:
            raise Refuse("no third-order theme %s in %s%s" % (tid, ov["scheme_file"], mean_hint(tid, ov["scheme"])))
        r = ov["scheme"][tid]
        L = ["%s  %s  (%s; family %s; %d second-order themes placed)" % (tid, r.get("name"), ov["scheme_file"],
                                                                         ov["families"].get(tid) or r.get("family") or "-", members[tid])]
        for k, v in r.items():
            if k in ("id", "theme", "name", "label"):
                continue
            if k == "members" and isinstance(v, list):
                L.append("members (%d):" % len(v))
                L += ["  %s  %s  %s" % (m.get("sub"), clip(m.get("second_order"), 70), ",".join(m.get("codes") or []))
                      if isinstance(m, dict) else "  %s" % m for m in v]
                continue
            L.append("%s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
        return L
    L = ["third-order themes: %d (%s)%s" % (len(ov["scheme"]), ov["scheme_file"],
                                            "; in the working file only: %d" % len(set(ov["current"]) - set(ov["frozen"]))
                                            if ov["current"] and ov["frozen"] else "")]
    L.append("%-8s %-6s %5s  %s" % ("id", "family", "memb", "label: gloss"))
    for tid in sorted(ov["scheme"]):
        r = ov["scheme"][tid]
        n = len(r["members"]) if isinstance(r.get("members"), list) else members[tid]
        L.append("%-8s %-6s %5d  %s%s" % (tid, ov["families"].get(tid) or r.get("family") or "-", n,
                                          clip(r.get("name"), 50), (": " + clip(r.get("gloss"), 70)) if r.get("gloss") and a.brief is not None else ""))
    return L


def v_where(st, a):
    ov = st.overlay()
    S = a.arg1
    if not S:
        raise Refuse("where needs a third-order theme id")
    _third_id(st, S)
    keys = sorted(k for k, v in ov["placed"].items() if S in v)
    sc = ov["scheme"].get(S, {})
    L = ["%s %s  fourth-order %s  dimensions %s  (%s)" % (S, clip(sc.get("name"), 60), ov["chunk_of"].get(S),
                                                          ",".join(st.dims_of_third(S)) or "-",
                                                          ov["assign_file"] or "no placements"),
         "%d second-order themes in %d rooms" % (len(keys), len({k[0] for k in keys})), ""]
    cts = {(t["sub"], t["theme_id"]): t for t in st.rows("themes")}
    for k in keys:
        t = cts.get(k, {})
        L.append("  %-20s %-4s %2d codes  %s" % (clip(k[0], 20), t.get("theme_id", k[1] or "?"),
                                                 t.get("n_codes", 0), clip(label_of(t), 90)))
    return L


def v_shelf(st, a):
    """shelf: the read tier that has arrived (shelves/read/), one line per work; shelf <name>: that
    work whole, from either tier; shelf --list: the on-request tier (shelves/on-request/)."""
    base = os.path.join(st.root, "shelves")
    tiers = {"read": os.path.join(base, "read"), "on-request": os.path.join(base, "on-request")}
    if not a.arg1:
        want = "on-request" if a.list else "read"
        d = tiers[want]
        if not os.path.isdir(d) or not os.listdir(d):
            return ["no %s shelf yet: nothing has arrived" % want]
        L = ["shelf, %s tier:" % want]
        for f in sorted(os.listdir(d)):
            first = ""
            try:
                first = next((l.strip("# ").strip() for l in open(os.path.join(d, f), encoding="utf-8") if l.strip()), "")
            except (OSError, UnicodeDecodeError):
                pass
            L.append("  %-50s %s" % (os.path.splitext(f)[0], clip(first, 90)))
        return L
    name = a.arg1 if a.arg1.endswith(".md") else a.arg1 + ".md"
    names = []
    for d in tiers.values():
        p = os.path.join(d, name)
        if os.path.exists(p):
            txt = _read_lines(p)
            if a.grep:
                rx = re.compile(a.grep, re.I)
                hits = ["%5d: %s" % (i, l) for i, l in enumerate(txt, 1) if rx.search(l)]
                return ["%s: %d lines match /%s/ (of %d; --page N with --limit L opens the page, "
                        "line n is on page (n-1)//L+1)" % (a.arg1, len(hits), a.grep, len(txt))] + hits
            return txt
        if os.path.isdir(d):
            names += [os.path.splitext(f)[0] for f in os.listdir(d)]
    raise Refuse("not on the shelf: %s%s" % (a.arg1, mean_hint(a.arg1, names)))


# ---- the writers --------------------------------------------------------------------------------
def _stamp():
    return datetime.datetime.utcnow().isoformat(timespec="seconds")


def _leg(st):
    p = os.path.join(st.root, ".leg")
    return open(p).read().strip() if os.path.exists(p) else "?"


def _part_key(f):
    """A diary part's sort key: the stage, then the part number as a number, so A1-10 follows A1-9
    (J, 2026-10-07, after A1's handback: a name sort put A1-10 between A1-1 and A1-2)."""
    stem = f[:-len(".jsonl")] if f.endswith(".jsonl") else f
    head, _, n = stem.rpartition("-")
    return (head, int(n)) if n.isdigit() else (stem, 0)


def _diary_path(st, stage):
    d = os.path.join(st.out, "diary")
    parts = sorted((f for f in os.listdir(d) if f.startswith("%s-" % stage) and f.endswith(".jsonl")), key=_part_key) \
        if os.path.isdir(d) else []
    if not parts:
        return os.path.join(d, "%s-1.jsonl" % stage)
    last = os.path.join(d, parts[-1])
    words = sum(len(json.loads(l).get("text", "").split()) for l in open(last, encoding="utf-8") if l.strip())
    if words >= 1500:
        k = int(parts[-1].rsplit("-", 1)[1].split(".")[0]) + 1
        return os.path.join(d, "%s-%d.jsonl" % (stage, k))
    return last


def v_log(st, a):
    """log "<text>" [--kind ...] [--ids a,b]: the only writer to the diary; stamped by the harness."""
    if not a.arg1:
        raise Refuse("log needs the text: mem.py log \"<text>\" [--kind k] [--ids a,b]")
    kind = a.kind or "note"
    kinds = log_kinds(st.root)
    if kind not in kinds:
        raise Refuse("no such kind: %s; one of %s" % (kind, ", ".join(kinds)))
    rooms = {s.lower(): s for s in st.subs()}
    ids = [x.strip() for x in (a.ids or "").split(",") if x.strip()]
    ids = [rooms.get((x[2:] if x.lower().startswith("r/") else x).lower(), x) for x in ids]   # a room by its frame spelling
    line = {"t": _stamp(), "stage": a.stage, "leg": _leg(st), "kind": kind, "ids": ids, "text": a.arg1}
    p = _diary_path(st, a.stage)
    if getattr(a, "dry_run", False):
        return ["dry run, nothing written; would append to %s:" % os.path.relpath(p, st.out),
                json.dumps(line, ensure_ascii=False)]
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    if kind in ("merged", "split"):      # a merge or a split is a new kind for the stopping rule (J, 2026-09-29)
        _kinds_ledger(st, a.stage, [(None, "%s:%s" % (kind, "+".join(sorted(i for i in ids if i.startswith("T3-")))
                                                     or line["t"]), kind)])
    return ["logged to %s" % os.path.relpath(p, st.out)]


def _diary_lines(st):
    d = os.path.join(st.out, "diary")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d), key=_part_key):
        if f.endswith(".jsonl"):
            out += jl(os.path.join(d, f))
    return out


def v_diary(st, a):
    lines = _diary_lines(st)
    if a.grep:
        rx = re.compile(a.grep, re.I)
        lines = [l for l in lines if rx.search(l.get("text", "")) or a.grep in (l.get("ids") or [])]
        if not lines:
            return ["no diary entry names /%s/" % a.grep]
    else:
        lines = lines[-(a.last or 5):]
    return ["%s %s %s %-10s %s %s" % (l.get("t", "?"), l.get("stage"), l.get("leg"), l.get("kind"),
                                      ",".join(l.get("ids") or []), l.get("text")) for l in lines] or ["(no diary yet)"]


def _stage_guard(a, verb, allowed):
    if a.stage not in allowed:
        raise Refuse("%s writes only at stage %s; this call's stage is %s (from --stage, the .stage "
                     "file or $STAGE)" % (verb, " or ".join(allowed), a.stage))


def v_mint(st, a):
    """mint --label "..." --trigger <sub>:<theme>: a theme_discovery line stamped by the harness."""
    _stage_guard(a, "mint", MINT_STAGES)
    if not a.label or not a.trigger:
        raise Refuse("mint needs --label \"...\" and --trigger <sub>:<tNN>")
    tsub, _, tth = a.trigger.replace("/", ":").partition(":")
    tsub = st.room(tsub)
    if not tth or not any(t["sub"] == tsub and t["theme_id"] == tth for t in st.rows("themes")):
        raise Refuse("the trigger %s names no second-order theme of r/%s%s" % (
            a.trigger, tsub, mean_hint(tth, [t["theme_id"] for t in st.rows("themes") if t["sub"] == tsub])))
    p = os.path.join(st.out, "theme_discovery.jsonl")
    existing = jl(p)
    import vlib
    minted = {r.get("theme") for r in existing} | {r.get("theme") for r in jl(_scheme_path(st))} | (vlib.load_scheme(st.out)[0] or set())
    if a.arg1:
        if not re.match(r"^T3-\d{3}$", a.arg1):
            raise Refuse("a third-order theme id is T3-NNN; %s is not" % a.arg1)
        if a.arg1 in minted:
            raise Refuse("%s is already minted (theme_discovery.jsonl or scheme_current); a theme is minted once" % a.arg1)
        tid = a.arg1
    else:
        k = len(existing) + 1
        while "T3-%03d" % k in minted:
            k += 1
        tid = "T3-%03d" % k
    reads = [r for r in jl(os.path.join(st.out, "_mem_reads-%s.jsonl" % a.stage)) if not r.get("refused")]
    rooms_read = len({r["args"][0] for r in reads if r.get("verb") == "room" and r.get("args")})
    themes_read = sum(1 for r in reads if r.get("verb") == "theme")
    codes_read = sum(r.get("lines", 0) for r in reads if r.get("verb") == "codes")
    tok = os.path.join(st.root, ".tokens_read")
    tokens = int(open(tok).read().strip() or 0) if os.path.exists(tok) else None
    line = {"theme": tid, "label": a.label, "t": _stamp(), "stage": a.stage, "leg": _leg(st),
            "sub": tsub, "trigger": "%s:%s" % (tsub, tth),
            "rooms_read": rooms_read, "themes_read": themes_read, "codes_read": codes_read, "tokens_read": tokens}
    line.update(_words_read(st, a.stage))
    if a.dry_run:
        return ["dry run, nothing written; would append to theme_discovery.jsonl:", json.dumps(line, ensure_ascii=False)]
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    _kinds_ledger(st, a.stage, [(tsub, tid, "minted")])
    if a.stage != "B1":          # after the freeze the scheme is scheme_v2.jsonl: the mint is the stamp, and the
        v_log(st, argparse.Namespace(arg1="minted %s %s (trigger %s)" % (tid, a.label, line["trigger"]), kind="minted",
                                     ids=tid, stage=a.stage, dry_run=False))   # theme is written there by you
        return ["minted %s (theme_discovery.jsonl); write it into scheme_v2.jsonl with its gate, then move its "
                "members with mem.py reassign" % tid]
    _scheme_edit(st, lambda rows: rows + [{"theme": tid, "label": a.label, "members": [
        {"sub": tsub, "theme_id": tth, "second_order": _second_label(st, tsub, tth)}]}])
    v_log(st, argparse.Namespace(arg1="minted %s %s (trigger %s)" % (tid, a.label, line["trigger"]), kind="minted",
                                 ids=tid, stage=a.stage, dry_run=False))
    return ["minted %s; its trigger is its first member in %s" % (tid, os.path.relpath(_scheme_path(st), st.root))]


def _words_read(st, stage):
    """The stopping rule's stamp (tools/saturation.py): words of the rooms read whole, and in average rooms.
    Only stage B1 runs the rule (A1 counts no kinds: J, 2026-09-29); elsewhere there is no stamp."""
    if str(stage).upper() != "B1":
        return {}
    try:
        import saturation
        R = saturation.replay(st.root, st.out, str(stage).upper())
        w = saturation.words(saturation.store(st.root))
        return {"words_read": sum(w[s] for s in R["seq"]), "avg_rooms_read": R["now"]["x"],
                "rooms_read_whole": R["now"]["rooms_read"]}
    except Exception:
        return {}


def _kinds_ledger(st, stage, events):
    """kinds-B1.jsonl, the stopping rule's record of kinds (J, 2026-09-29): one line per kind met, stamped with
    the room being read when it was met (`at`, the room saturation.py names next). Append only: a later merge,
    split or unplace never rewrites a line, so the rule's past stays as it was read. A merge or a split is
    itself a new kind. After the walk has stopped or while it waits for the PI, `at` is null and the line does
    not count. events: [(sub, kind, event)]."""
    if str(stage).upper() != "B1" or not events:
        return
    at = None
    try:
        import saturation
        at = saturation.replay(st.root, st.out, "B1")["next"]
    except Exception:
        at = None
    with open(os.path.join(st.out, "kinds-B1.jsonl"), "a", encoding="utf-8") as f:
        for sub, kind, event in events:
            f.write(json.dumps({"t": _stamp(), "leg": _leg(st), "at": at, "sub": sub, "kind": kind,
                                "event": event}, ensure_ascii=False) + "\n")


def v_idea(st, a):
    """idea "<label>" --trigger <sub>:<tNN>: a prospective third-order theme, stamped when first thought of."""
    _stage_guard(a, "idea", MINT_STAGES)
    if not a.arg1 or not a.trigger:
        raise Refuse("idea needs the label and --trigger <sub>:<tNN>")
    tsub, _, tth = a.trigger.replace("/", ":").partition(":")
    tsub = st.room(tsub)
    if not tth or not any(t["sub"] == tsub and t["theme_id"] == tth for t in st.rows("themes")):
        raise Refuse("the trigger %s names no second-order theme of r/%s" % (a.trigger, tsub))
    reads = [r for r in jl(os.path.join(st.out, "_mem_reads-%s.jsonl" % a.stage)) if not r.get("refused")]
    line = {"t": _stamp(), "stage": a.stage, "leg": _leg(st), "label": a.arg1, "trigger": "%s:%s" % (tsub, tth),
            "themes_read": sum(1 for r in reads if r.get("verb") == "theme")}
    line.update(_words_read(st, a.stage))
    with open(os.path.join(st.out, "ideas-%s.jsonl" % a.stage), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return ["idea logged to ideas-%s.jsonl: %s" % (a.stage, a.arg1)]


def _scheme_path(st):
    cur = st.scheme_files()[1]
    return cur or os.path.join(st.out, "scheme", "scheme_current.jsonl")


def _second_label(st, sub, tth):
    t = next((t for t in st.rows("themes") if t["sub"] == sub and t["theme_id"] == tth), {})
    return t.get("second_order") or label_of(t)


def _scheme_edit(st, fn):
    """Rewrite scheme_current.jsonl atomically: read, apply fn to the rows, write a temporary file,
    rename it over the old one. A crash leaves the old file or the new one, never half of either."""
    p = _scheme_path(st)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    rows = fn(jl(p))
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    st._cache.pop("ov", None)


def _member_is(m, sub, tth, label):
    return isinstance(m, dict) and m.get("sub") == sub and (
        m.get("theme_id") == tth or (label and (m.get("second_order") or "").strip().lower() == label.strip().lower()))


def v_place(st, a):
    """place <sub>:<tNN> --theme T3-NNN: move a second-order theme into a third-order theme."""
    _stage_guard(a, "place", ("B1",))
    if not a.arg1 or not a.theme:
        raise Refuse("place needs <sub>:<tNN> and --theme T3-NNN")
    sub, _, tth = a.arg1.replace("/", ":").partition(":")
    sub = st.room(sub)
    if not any(t["sub"] == sub and t["theme_id"] == tth for t in st.rows("themes")):
        raise Refuse("%s names no second-order theme of r/%s" % (a.arg1, sub))
    rows = jl(_scheme_path(st))
    if not any(r.get("theme") == a.theme for r in rows):
        raise Refuse("%s is not in scheme_current; mint it first%s" % (
            a.theme, mean_hint(a.theme, [r.get("theme") for r in rows if r.get("theme")])))
    lab = _second_label(st, sub, tth)
    was = [r["theme"] for r in rows if any(_member_is(m, sub, tth, lab) for m in r.get("members") or [])]
    if a.dry_run:
        return ["dry run: would place %s:%s in %s (now in %s)" % (sub, tth, a.theme, ", ".join(was) or "none")]

    def fn(rows):
        for r in rows:
            if r.get("theme") == a.theme and not any(_member_is(m, sub, tth, lab) for m in r.get("members") or []):
                r.setdefault("members", []).append({"sub": sub, "theme_id": tth, "second_order": lab})
        return rows
    _kinds_ledger(st, a.stage, [(sub, a.theme, "placed")])
    _scheme_edit(st, fn)
    v_log(st, argparse.Namespace(arg1="placed %s:%s in %s%s" % (sub, tth, a.theme,
                                 " (also in %s)" % ", ".join(w for w in was if w != a.theme) if was else ""),
                                 kind="placed", ids="%s,%s:%s" % (a.theme, sub, tth), stage=a.stage, dry_run=False))
    return ["placed %s:%s in %s%s" % (sub, tth, a.theme,
            "; it stays in %s until you unplace it there" % ", ".join(w for w in was if w != a.theme)
            if [w for w in was if w != a.theme] else "")]


def v_unplace(st, a):
    """unplace <sub>:<tNN> [--theme T3-NNN]: take a second-order theme out of one third-order theme,
    or out of every one when --theme is absent."""
    _stage_guard(a, "unplace", ("B1",))
    if not a.arg1:
        raise Refuse("unplace needs <sub>:<tNN> [--theme T3-NNN]")
    sub, _, tth = a.arg1.replace("/", ":").partition(":")
    sub = st.room(sub)
    lab = _second_label(st, sub, tth)
    rows = jl(_scheme_path(st))
    hit = [r["theme"] for r in rows if (not a.theme or r.get("theme") == a.theme)
           and any(_member_is(m, sub, tth, lab) for m in r.get("members") or [])]
    if not hit:
        raise Refuse("%s:%s is not placed in %s" % (sub, tth, a.theme or "any third-order theme"))
    if a.dry_run:
        return ["dry run: would take %s:%s out of %s" % (sub, tth, ", ".join(hit))]

    def fn(rows):
        for r in rows:
            if r.get("theme") in hit:
                r["members"] = [m for m in r.get("members") or [] if not _member_is(m, sub, tth, lab)]
        return rows
    _scheme_edit(st, fn)
    v_log(st, argparse.Namespace(arg1="unplaced %s:%s from %s" % (sub, tth, ", ".join(hit)), kind="unplaced",
                                 ids=",".join(hit + ["%s:%s" % (sub, tth)]), stage=a.stage, dry_run=False))
    return ["unplaced %s:%s from %s" % (sub, tth, ", ".join(hit))]


def v_reassign(st, a):
    """reassign <sub>:<tNN> --theme T3-a[,T3-b] --reason "...": a recut's re-placement. Rewrites that second-order
    theme's line of assignments_final.jsonl in place (the file stays one line per theme) and records the move."""
    _stage_guard(a, "reassign", RECUT_STAGES)
    if not a.arg1 or not a.theme or not a.reason:
        raise Refuse("reassign needs <sub>:<tNN>, --theme T3-NNN[,T3-MMM] and --reason \"...\"")
    sub, _, tth = a.arg1.replace("/", ":").partition(":")
    sub = st.room(sub)
    if not any(t["sub"] == sub and t["theme_id"] == tth for t in st.rows("themes")):
        raise Refuse("%s names no second-order theme of r/%s" % (a.arg1, sub))
    import vlib
    ids, name = vlib.load_scheme(st.out)
    to = [x.strip() for x in a.theme.split(",") if x.strip()]
    bad = [x for x in to if not ids or x not in ids]
    if bad:
        raise Refuse("%s not in %s; a theme a recut makes is written there first, with its gate" % (
            ", ".join(bad), name or "scheme_v2.jsonl"))
    p = os.path.join(st.out, "assignments_final.jsonl")
    rows = jl(p)
    hit = [r for r in rows if r.get("sub") == sub and r.get("theme_id") == tth]
    if not hit:
        raise Refuse("assignments_final.jsonl has no line for %s:%s; stage C1 writes one per second-order theme "
                     "before any recut" % (sub, tth))
    was = hit[-1].get("third_order")
    if a.dry_run:
        return ["dry run: would move %s:%s from %s to %s" % (sub, tth, was, ", ".join(to))]
    for r in hit:
        r["third_order"] = to
        r.setdefault("moves", []).append({"from": was, "to": to, "stage": a.stage, "leg": _leg(st), "t": _stamp(),
                                          "why": a.reason})
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    if a.stage == "C1":                  # C1 keeps its overlay of changed lines beside the whole file (C1 section 9)
        ov = os.path.join(st.out, "assign_revisions_only.jsonl")
        keep = [r for r in jl(ov) if not (r.get("sub") == sub and r.get("theme_id") == tth)]
        with open(ov + ".tmp", "w", encoding="utf-8") as f:
            for r in keep + [hit[-1]]:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(ov + ".tmp", ov)
    st._cache.pop("ov", None)
    v_log(st, argparse.Namespace(arg1="reassigned %s:%s from %s to %s: %s" % (sub, tth, was, ", ".join(to), a.reason),
                                 kind="move", ids=",".join(to + ["%s:%s" % (sub, tth)]), stage=a.stage, dry_run=False))
    return ["moved %s:%s from %s to %s in assignments_final.jsonl" % (sub, tth, was, ", ".join(to))]


def v_adjudicate(st, a):
    """adjudicate <adaptation-id> --decision accept|modify|reject|particular|pending --reason "..." """
    _stage_guard(a, "adjudicate", ADJ_STAGES)
    if not a.arg1 or not a.decision or not a.reason:
        raise Refuse("adjudicate needs the adaptation id, --decision and --reason")
    if a.decision not in DECISIONS:
        raise Refuse("no such decision: %s; one of %s" % (a.decision, ", ".join(DECISIONS)))
    ids = {l.get("id") for l in jl(os.path.join(st.out, "adaptations.jsonl"))}
    ids |= {l.get("id") for l in jl(os.path.join(st.out, "adaptations-recheck.jsonl"))}
    ids.discard(None)
    if not ids:
        raise Refuse("no adaptations ledger yet (out/adaptations.jsonl); ingest.py D writes it")
    for x in [a.arg1] + ([a.pair] if a.pair else []):
        if x not in ids:
            raise Refuse("no adaptation %s in the ledger%s" % (x, mean_hint(x, ids)))
    line = {"adaptation": a.arg1, "decision": a.decision, "reason": a.reason, "revised": a.revised,
            "pair": a.pair, "kind": a.kind, "t": _stamp(), "stage": a.stage, "leg": _leg(st)}
    if a.dry_run:
        return ["dry run, nothing written; would append to adjudications.jsonl:", json.dumps(line, ensure_ascii=False)]
    with open(os.path.join(st.out, "adjudications.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    v_log(st, argparse.Namespace(arg1="adjudicated %s: %s (%s)" % (a.arg1, a.decision, a.reason), kind="note",
                                 ids=a.arg1, stage=a.stage, dry_run=False))
    return ["adjudicated %s: %s" % (a.arg1, a.decision)]


# ---- the model and the ledger ---------------------------------------------------------------------
def v_adaptations(st, a):
    """adaptations --element <id> [--kind k]: every ledger line touching an element, across rooms."""
    el = a.element or a.arg1
    if not el:
        raise Refuse("adaptations needs --element <id>")
    adj = {r["adaptation"]: r for r in jl(os.path.join(st.out, "adjudications.jsonl"))}
    lines = jl(os.path.join(st.out, "adaptations.jsonl"))
    if not lines:
        raise Refuse("no adaptations ledger yet (out/adaptations.jsonl)")
    els = {l.get("element") for l in lines}
    if el not in els:
        raise Refuse("no ledger line touches %s%s" % (el, mean_hint(el, els)))
    sel = [l for l in lines if l.get("element") == el and (not a.kind or l.get("kind") == a.kind)]
    sel.sort(key=lambda l: (l["op"], l["sub"]))
    L = ["adaptations touching %s: %d lines in %d rooms" % (el, len(sel), len({l["sub"] for l in sel}))]
    for l in sel:
        d = adj.get(l["id"], {}).get("decision", l.get("decision"))
        L.append("%-14s %-13s %-14s %-22s %-10s %s%s  [%s]" % (
            l["id"], l["op"], clip(l.get("source"), 14), clip(" > ".join(x or "-" for x in (l.get("lift") or [])[1:]), 22),
            d, clip(l.get("how"), 90), "" if l.get("portable", True) else " NONPORTABLE", ",".join((l.get("evidence") or {}).get("codes", []))))
    return L


def v_rooms(st, a):
    """rooms --with <id> | --without <id>: rooms holding or lacking a theme, element or adaptation key."""
    ov = st.overlay()
    key = a.with_ or a.without
    if not key:
        raise Refuse("rooms needs --with <id> or --without <id>")
    st.check_id(key)
    holders = set()
    if key.startswith("T3-"):
        holders = {s for (s, t), v in ov["placed"].items() if key in v}
    elif key.startswith("T4-"):
        members = set(ov["chunks"].get(key, {}).get("members", []))
        holders = {s for (s, t), v in ov["placed"].items() if set(v) & members}
    elif key in ov["dims"]:
        holders = {s for (s, t), v in ov["placed"].items() if any(key in st.dims_of_third(x) for x in v)}
    else:
        for l in jl(os.path.join(st.out, "adaptations.jsonl")):
            k = "%s:%s:%s" % (l["op"], l.get("element"), (l.get("lift") or [None, None])[1])
            if l.get("element") == key or l.get("id") == key or k == key or k.startswith(key):
                holders.add(l["sub"])
    rooms = sorted(st.subs())
    sel = sorted(holders) if a.with_ else [r for r in rooms if r not in holders]
    return ["rooms %s %s: %d of %d" % ("with" if a.with_ else "without", key, len(sel), len(rooms))] + ["  " + r for r in sel]


def v_contrast(st, a):
    """contrast <sub> <sub>: the two rooms' placements side by side, and their adaptation sets."""
    ov = st.overlay()
    A_, B_ = st.room(a.arg1), st.room(a.arg2)

    def col(sub):
        return {x for (s, t), v in ov["placed"].items() if s == sub for x in v}
    A, B = col(A_), col(B_)
    L = ["contrast r/%s against r/%s" % (A_, B_),
         "third-order themes: shared %d, only %s %d, only %s %d" % (len(A & B), A_, len(A - B), B_, len(B - A))]
    for name, S in (("shared", A & B), ("only " + A_, A - B), ("only " + B_, B - A)):
        L.append("  %s: %s" % (name, ", ".join("%s %s" % (x, clip(ov["scheme"].get(x, {}).get("name"), 30)) for x in sorted(S))))
    led = jl(os.path.join(st.out, "adaptations.jsonl"))
    if led:
        def keys(sub):
            return {"%s:%s:%s" % (l["op"], l.get("element"), (l.get("lift") or [None, None])[1]) for l in led if l["sub"] == sub}
        KA, KB = keys(A_), keys(B_)
        L += ["adaptation keys (level 3): shared %d, only %s %d, only %s %d" % (len(KA & KB), A_, len(KA - KB), B_, len(KB - KA))]
        for name, S in (("shared", KA & KB), ("only " + A_, KA - KB), ("only " + B_, KB - KA)):
            L.append("  %s: %s" % (name, ", ".join(sorted(S))))
    return L


FACT_LINE = ("threads_coded", "threads_total", "items_in_store", "items_coded", "codes", "themes",
             "onset_first_code_hour", "onset_median_code_hour", "onset_last_code_hour", "coded_authors",
             "top1_share", "n_subreddits_named", "n_off_platform")


def v_compare(st, a):
    A_, B_ = st.room(a.arg1), st.room(a.arg2)
    L = ["compare r/%s and r/%s (before any placement: facts, time, themes, names, canvas)" % (A_, B_), ""]
    L.append("%-24s %14s %14s" % ("field", clip(A_, 14), clip(B_, 14)))
    ra, rb = st.room_row(A_) or {}, st.room_row(B_) or {}
    for f in FACT_LINE:
        L.append("%-24s %14s %14s" % (f, fmtv(ra.get(f)), fmtv(rb.get(f))))
    L.append("")
    its2 = {s: [i for i in st.rows("items") if i["sub"] == s] for s in (A_, B_)}
    mx = max([max(hour_bins(i["hour"] for i in v if i.get("codes"))[0]) for v in its2.values() if v] or [0]) or None
    for s in (A_, B_):
        L += when_lines(s, its2[s], mx) if its2[s] else ["r/%s: no items" % s]
    L.append("")
    for s in (A_, B_):
        cts = [t for t in st.rows("themes") if t["sub"] == s]
        L.append("r/%s second-order themes (%d):" % (s, len(cts)))
        L += ["  %-4s %3s  %s" % (t["theme_id"], t.get("n_codes", ""), clip(label_of(t), 90)) for t in cts]
    L.append("")
    for s in (A_, B_):
        c = collections.Counter((p.get("normalised") or p.get("raw") or "?") for p in st.rows("pointers")
                                if p.get("sub") == s and p.get("kind") == "subreddit")
        L.append("r/%s names (%d rooms): %s" % (s, len(c), ", ".join("%s %d" % kv for kv in c.most_common(12)) or "-"))
    na = {(p.get("normalised") or "").lower() for p in st.rows("pointers") if p.get("sub") == A_ and p.get("kind") == "subreddit"} - {""}   # v42: normalised may be null
    nb = {(p.get("normalised") or "").lower() for p in st.rows("pointers") if p.get("sub") == B_ and p.get("kind") == "subreddit"} - {""}
    L.append("named by both: %s" % (", ".join(sorted(na & nb - {""})) or "-"))
    L.append("")
    for s in (A_, B_):
        L += ["r/%s %s" % (s, x) for x in canvas_lines(st.room_row(s) or {})[:1]]
        w, p = px_shares(st, s)
        L.append("      region placed by window members %s, by pre-event members %s (pixels.csv)" % (w, p))
    L.append("caveat: " + _manifest_caveat(st))
    if a.grep:
        rx = re.compile(a.grep, re.I)
        L.append("")
        la = {c.get("first_order") for c in st.rows("codes") if c["sub"] == A_ and rx.search(str(c.get("first_order") or ""))}
        lb = {c.get("first_order") for c in st.rows("codes") if c["sub"] == B_ and rx.search(str(c.get("first_order") or ""))}
        L.append("concept labels matching /%s/: r/%s %d, r/%s %d, the same label in both %d" % (
            a.grep, A_, len(la), B_, len(lb), len(la & lb)))
        for s, S in ((A_, la), (B_, lb)):
            L += ["  %-14s %s" % (clip(s, 14), clip(x, 110)) for x in sorted(S)]
    return L


def v_finding(st, a):
    lines = jl(os.path.join(st.out, "findings.jsonl"))
    if a.verb == "finding":
        sel = [l for l in lines if l.get("id") == a.arg1][-1:]   # the latest line for the id
        if not sel:
            raise Refuse("no finding %s in findings.jsonl%s" % (a.arg1, mean_hint(a.arg1, {l.get("id") for l in lines})))
    else:
        el = a.touching or a.arg1
        if not el:
            raise Refuse("findings needs --touching <element>")
        sel = [l for l in lines if el in json.dumps(l.get("evidence", [])) or el in (l.get("statement") or "") or el in json.dumps(l.get("elements", []))]
    return [json.dumps(l, ensure_ascii=False) for l in sel] or ["(no finding touches %s)" % (a.touching or a.arg1)]


def v_question(st, a):
    d = os.path.join(st.out, "_questions")
    p = os.path.join(d, "%s.md" % a.arg1)
    if not os.path.exists(p):
        names = [f[:-3] for f in os.listdir(d)] if os.path.isdir(d) else []
        raise Refuse("no question file %s%s" % (a.arg1, mean_hint(a.arg1 or "", names)))
    return _read_lines(p)


def _asks(st):
    return jl(os.path.join(st.out, "asks.jsonl"))


def _answer(st, qid):
    p = os.path.join(st.out, "_answers", "%s.md" % qid)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None


def v_ask(st, a):
    """ask "<question>" --assume "<what you do meanwhile>" [--ids a,b]: a question for the principal
    investigator (v43, J 2026-10-04). It reaches him at once; the work does not wait for it."""
    if not a.arg1:
        raise Refuse('ask needs the question: mem.py ask "<question>" --assume "<what you will do meanwhile>"')
    if not a.assume:
        raise Refuse("ask needs --assume: what you will do until the answer comes, so the work goes on")
    rows = _asks(st)
    qid = "Q%s-%03d" % (a.stage, 1 + sum(1 for r in rows if r.get("stage") == a.stage))
    rooms = {x.lower(): x for x in st.subs()}
    ids = [x.strip() for x in (a.ids or "").split(",") if x.strip()]
    ids = [rooms.get((x[2:] if x.lower().startswith("r/") else x).lower(), x) for x in ids]
    line = {"id": qid, "t": _stamp(), "stage": a.stage, "leg": _leg(st), "question": a.arg1,
            "assumption": a.assume, "ids": ids}
    diary = {"t": line["t"], "stage": a.stage, "leg": line["leg"], "kind": "ask", "ids": [qid] + ids,
             "text": "asked %s: %s | meanwhile: %s" % (qid, a.arg1, a.assume)}
    p = _diary_path(st, a.stage)
    if getattr(a, "dry_run", False):
        return ["dry run, nothing written; would append to asks.jsonl and %s:" % os.path.relpath(p, st.out),
                json.dumps(line, ensure_ascii=False)]
    os.makedirs(st.out, exist_ok=True)
    with open(os.path.join(st.out, "asks.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(diary, ensure_ascii=False) + "\n")
    return ["asked %s; it goes to the principal investigator now. Go on with what you said you would do, "
            "name %s on the work that rests on it, and read the answer with mem.py asks %s when it comes "
            "(a leg's first message names answers that are waiting)." % (qid, qid, qid)]


def v_asks(st, a):
    """asks [<id>] [--open]: the questions asked and the answers that came back."""
    rows = _asks(st)
    if a.arg1:
        rows_ = [r for r in rows if r.get("id") == a.arg1]
        if not rows_:
            raise Refuse("no question %s%s" % (a.arg1, mean_hint(a.arg1, {r.get("id") for r in rows})))
        rows = rows_
    out = []
    for r in rows:
        ans = _answer(st, r.get("id"))
        if a.open_only and ans:
            continue
        out.append("%s %s leg %s, %s" % (r.get("id"), r.get("t"), r.get("leg"), "answered" if ans else "open"))
        out.append("  question:  " + (r.get("question") or ""))
        out.append("  meanwhile: " + (r.get("assumption") or ""))
        if ans:
            out += ["  answer:"] + ["    " + l for l in ans.split("\n")]
    if not out:
        return ["(no question asked yet)" if not rows else "(no open question)"]
    return out


def v_audit(st, a):
    """audit [frame|rooms|retracted|build]: stage A1's package checks from the raw files (v43)."""
    P = os.path.join(st.root, "package")
    want = (a.arg1 or "all").lower()
    if want not in ("all", "frame", "rooms", "retracted", "build"):
        raise Refuse("audit takes frame, rooms, retracted or build, or nothing for all four")
    rooms = st.rows("rooms")
    subs = [r["sub"] for r in rooms]
    codes, themes = st.rows("codes"), st.rows("themes")
    L = []
    if want in ("all", "frame"):
        fm = os.path.join(P, "FRAME.md")
        txt = open(fm, encoding="utf-8").read() if os.path.exists(fm) else ""
        m = re.search(r"Copy date: (\S+)\. Rooms: (\d+)\. Hash[^`]*`([0-9a-f]+)`", txt)
        L.append("frame: package/FRAME.md: " + ("copy date %s, %s rooms, hash %s" % m.groups() if m else "absent or without its copy-date line"))
        folders = {d for d in os.listdir(P) if os.path.isdir(os.path.join(P, d)) and d not in ("store", "canvas")
                   and not d.startswith((".", "_"))} if os.path.isdir(P) else set()
        cs, ts = {c.get("sub") for c in codes}, {t.get("sub") for t in themes}
        L.append("frame: store/rooms.jsonl %d rooms; room folders under package/ %d; rooms in store/codes.jsonl %d; "
                 "in store/themes.jsonl %d" % (len(subs), len(folders), len(cs), len(ts)))
        for name, sel in (("in rooms.jsonl, no folder", sorted(set(subs) - folders)),
                          ("a folder, not in rooms.jsonl", sorted(folders - set(subs))),
                          ("in rooms.jsonl, no concept in the store", sorted(set(subs) - cs)),
                          ("in rooms.jsonl, no second-order theme in the store", sorted(set(subs) - ts))):
            if sel:
                L.append("frame: %s (%d): %s" % (name, len(sel), ", ".join(sel)))
        if m and int(m.group(2)) != len(subs):
            L.append("frame: MISMATCH: FRAME.md says %s rooms, rooms.jsonl holds %d" % (m.group(2), len(subs)))
        L.append("frame: the hash covers each room's own forest in the handler's input, which the package does not "
                 "hold; the handler checks it at the build, not this verb")
    if want in ("all", "rooms"):
        six = ("brief.md", "case.md", "codes.jsonl", "themes.jsonl", "threads.jsonl", "pointers.jsonl")
        miss = []
        for sub in subs:
            m_ = [f for f in six if not os.path.exists(os.path.join(P, sub, f))]
            if not os.path.exists(os.path.join(st.root, "trees", sub + ".md")):
                m_.append("trees/%s.md" % sub)
            if m_:
                miss.append("%s: %s" % (sub, ", ".join(m_)))
        L.append("rooms: %d of %d hold the six files under package/<sub>/ and a forest in trees/"
                 % (len(subs) - len(miss), len(subs)))
        L += ["rooms: missing in " + x for x in miss]
    if want in ("all", "retracted"):
        lines_ = ret_ = 0
        per = {}
        for sub in subs:
            p_ = os.path.join(P, sub, "codes.jsonl")
            rs = jl(p_) if os.path.exists(p_) else []
            per[sub] = (len(rs), sum(1 for c in rs if c.get("retracted")))
            lines_ += per[sub][0]; ret_ += per[sub][1]
        rp = os.path.join(st.S, "_retracted.jsonl")
        rlist = jl(rp) if os.path.exists(rp) else []
        bp = os.path.join(st.S, "_build.json")
        b = json.load(open(bp)) if os.path.exists(bp) else {}
        rd = os.path.join(st.S, "README-store.md")
        rm = re.search(r"(\d[\d,]*) retracted by the coder and dropped\)", open(rd, encoding="utf-8").read()) if os.path.exists(rd) else None
        L.append("retracted: the coders' package/<sub>/codes.jsonl: %d lines, %d retracted; store/_retracted.jsonl %d; "
                 "_build.json codes_retracted_dropped %s; README-store.md %s"
                 % (lines_, ret_, len(rlist), b.get("codes_retracted_dropped", "absent"), rm.group(1) if rm else "absent"))
        L.append("retracted: store/codes.jsonl %d against the coders' lines less their retractions %d: %s"
                 % (len(codes), lines_ - ret_, "match" if len(codes) == lines_ - ret_ else "MISMATCH"))
        by = collections.Counter(c.get("sub") for c in codes)
        rby = collections.Counter(r.get("sub") for r in rlist)
        bad = [s for s in subs if per[s][0] and (by[s] != per[s][0] - per[s][1] or rby[s] != per[s][1])]
        for s in bad[:40]:
            L.append("retracted: MISMATCH %s: coder %d lines, %d retracted; store %d concepts, %d in _retracted.jsonl"
                     % (s, per[s][0], per[s][1], by[s], rby[s]))
        if len(bad) > 40:
            L.append("retracted: and %d more rooms" % (len(bad) - 40))
    if want in ("all", "build"):
        bp = os.path.join(st.S, "_build.json")
        b = json.load(open(bp)) if os.path.exists(bp) else {}
        items = st.rows("items")
        up = os.path.join(st.S, "_unjoined.jsonl")
        got = {"communities": len(rooms), "codes": len(codes), "themes": len(themes),
               "threads": len(st.rows("threads")), "items": len(items),
               "items_coded": sum(1 for i in items if i.get("codes")),
               "items_bridge": sum(1 for i in items if i.get("state") == "bridge"),
               "items_dropped": sum(1 for i in items if i.get("state") == "dropped"),
               "pointers": len(st.rows("pointers")), "codes_unjoined": len(jl(up)) if os.path.exists(up) else 0,
               "briefs": sum(1 for r in rooms if r.get("brief"))}
        for k, v in got.items():
            L.append("build: %-14s store/_build.json %s, recomputed from the store %d%s"
                     % (k, b.get(k, "absent"), v, "" if b.get(k) == v else "  MISMATCH"))
    return L


def v_contract(st, a):
    """contract --section <n>: one section of CONTRACT-aggregator.md by its index."""
    p = os.path.join(st.root, "CONTRACT-aggregator.md")
    if not os.path.exists(p):
        raise Refuse("CONTRACT-aggregator.md is not in the folder root")
    txt = open(p, encoding="utf-8").read().split("\n")
    want = str(a.section or a.arg1 or "")
    heads = [i for i, l in enumerate(txt) if l.startswith("## ")]
    for k, i in enumerate(heads):
        title = txt[i][3:]
        if want and (title.startswith(want + ".") or want.lower() in title.lower()):
            j = heads[k + 1] if k + 1 < len(heads) else len(txt)
            return txt[i:j]
    return ["no section %s; sections: " % want] + ["  " + txt[i][3:] for i in heads]


def _stale(st, view):
    """A line saying the view is older than your working files, or nothing."""
    t = os.path.getmtime(view)
    newer = [os.path.relpath(q, st.root) for q in (st.scheme_files()[1],
             os.path.join(st.out, "fourth", "fourth.jsonl"), os.path.join(st.out, "dimensions.jsonl"),
             os.path.join(st.out, "model", "elements.jsonl")) if q and os.path.exists(q) and os.path.getmtime(q) > t]
    if not newer:
        return []
    return ["note: this view was written at the last close; %s changed since. The live overlay "
            "verbs (scheme, where, theme, room) read the working files." % ", ".join(newer)]


def v_table(st, a):
    """table --from 3rd|2nd | --room <sub>: projections of the data structure."""
    p = os.path.join(st.out, "_views", "data-structure.tsv")
    if not os.path.exists(p):
        raise Refuse("no data-structure view yet; gen_views.py writes it at every close")
    with open(p, encoding="utf-8", newline="\n") as f:
        rows = [(l.rstrip("\n").split("\t") + [""] * 12)[:12] for l in f][2:]
    stale = _stale(st, p)
    if a.room or a.arg1 and not a.from_:
        sub = st.room(a.room or a.arg1)
        sel = [r for r in rows if r[0] == sub]
        return stale + ["r/%s: %d concepts" % (sub, len(sel))] + ["%s | %s | %s | %s | %s" % (r[3], r[5], r[7] or r[6], r[9], r[11]) for r in sel]
    lvl = {"3rd": "3rd", "third": "3rd", "2nd": "2nd", "second": "2nd"}.get(a.from_ or "3rd")
    if not lvl:
        raise Refuse("table --from takes 3rd or 2nd, not %s" % a.from_)
    seen, L = set(), []
    for r in rows:
        key = (r[6], r[8], r[10]) if lvl == "3rd" else (r[5], r[6], r[8], r[10])
        if key in seen or not any(key):
            continue
        seen.add(key)
        L.append(" | ".join(x for x in ((r[5] if lvl == "2nd" else None), r[7] or r[6], r[9], r[11]) if x))
    return stale + ["data structure from %s (%d rows)" % (lvl, len(L))] + L


def v_view(st, a):
    d = os.path.join(st.out, "_views")
    if not os.path.isdir(d):
        raise Refuse("no views yet: out/_views/ is absent; gen_views.py writes it at every close")
    files = sorted(f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f)))
    if not a.arg1:
        L = ["views in out/_views/ (%d):" % len(files)]
        for f in files:
            n = sum(1 for _ in open(os.path.join(d, f), encoding="utf-8", errors="replace"))
            L.append("  %-40s %8d bytes %7d lines" % (f, os.path.getsize(os.path.join(d, f)), n))
        return L
    cand = [a.arg1] if a.arg1 in files else [a.arg1 + ext for ext in (".tsv", ".md") if a.arg1 + ext in files]
    if not cand:
        raise Refuse("no view %s in out/_views/%s" % (a.arg1, mean_hint(a.arg1, [os.path.splitext(f)[0] for f in files])))
    p = os.path.join(d, cand[0])
    with open(p, encoding="utf-8", errors="replace", newline="\n") as f:
        txt = [l.rstrip("\n") for l in f]
    if not (a.grep or a.room):
        return txt
    head = [l for l in txt[:2] if l.startswith("#") or "\t" in l][:2] if p.endswith(".tsv") else []
    rx = re.compile(a.grep, re.I) if a.grep else None
    sub = st.room(a.room) if a.room else None
    body = txt[len(head):]
    sel = []
    for l in body:
        if sub and not (l.split("\t")[0] == sub if p.endswith(".tsv") else re.search(r"\b%s\b" % re.escape(sub), l, re.I)):
            continue
        if rx and not rx.search(l):
            continue
        sel.append(l)
    return ["%s: %d of %d lines%s%s" % (cand[0], len(sel), len(body), " in r/" + sub if sub else "",
                                        " matching /%s/" % a.grep if a.grep else "")] + head[-1:] + sel


def v_wiki(st, a):
    d = os.path.join(st.out, "_wiki")
    if not os.path.isdir(d):
        raise Refuse("no wiki yet: out/_wiki/ is absent; gen_views.py writes it at every close")
    pages = []
    for base, _, fs in os.walk(d):
        pages += [os.path.relpath(os.path.join(base, f), d)[:-3] for f in fs if f.endswith(".md")]
    if not a.arg1:
        per = collections.Counter(p.split("/")[0] if "/" in p else "." for p in pages)
        return ["wiki pages in out/_wiki/: %d (%s); open one with mem.py wiki rooms/<sub> or model/<id>"
                % (len(pages), ", ".join("%s %d" % kv for kv in sorted(per.items())))]
    want = a.arg1[:-3] if a.arg1.endswith(".md") else a.arg1
    for c in (want, "rooms/" + want, "model/" + want):
        if c in pages:
            q = os.path.join(d, c + ".md")
            return _stale(st, q) + _read_lines(q)
    raise Refuse("no wiki page %s%s" % (a.arg1, mean_hint(want, pages + [p.split("/")[-1] for p in pages])))


def v_diff(st, a):
    """diff-scheme <cut> | diff-model <cut>: the file now against its copy in _snap/<cut>/."""
    files = ["scheme_v2.jsonl"] if a.verb == "diff-scheme" else [os.path.join("model", "elements.jsonl"),
                                                                 os.path.join("model", "arrows.jsonl")]
    cut = os.path.join(st.out, "_snap", a.arg1 or "")
    if not a.arg1 or not os.path.isdir(cut):
        snaps = sorted(x for x in os.listdir(os.path.join(st.out, "_snap"))
                       if os.path.isdir(os.path.join(st.out, "_snap", x))) if os.path.isdir(os.path.join(st.out, "_snap")) else []
        raise Refuse("no snap copy %s in out/_snap/ (tools/snap.py writes one per snap)%s" % (a.arg1, mean_hint(a.arg1 or "", snaps)))
    L = []
    for which in files:
        A = {r.get("id"): r for r in jl(os.path.join(cut, which))}
        B = {r.get("id"): r for r in jl(os.path.join(st.out, which))}
        L.append("%s: then %d, now %d" % (which, len(A), len(B)))
        for k in sorted(set(A) | set(B), key=str):
            if k not in A:
                L.append("+ %s %s" % (k, clip(B[k].get("name") or B[k].get("statement") or B[k].get("mechanism"), 80)))
            elif k not in B:
                L.append("- %s %s" % (k, clip(A[k].get("name") or A[k].get("statement") or A[k].get("mechanism"), 80)))
            elif A[k] != B[k]:
                L.append("~ %s %s" % (k, ", ".join(f for f in set(A[k]) | set(B[k]) if A[k].get(f) != B[k].get(f))))
    return L


VERBS = {"room": v_room, "case": v_case, "brief": v_brief, "forest": v_forest, "when": v_when,
         "canvas": v_canvas, "neighbours": v_neighbours, "compare": v_compare, "note": v_note, "codes": v_codes, "theme": v_theme,
         "themes": v_themes, "after": v_after, "pairs": v_pairs, "facts": v_facts, "notes": v_notes,
         "progress": v_progress, "next": v_next, "scheme": v_scheme, "where": v_where, "shelf": v_shelf,
         "log": v_log, "diary": v_diary, "mint": v_mint, "idea": v_idea, "place": v_place, "unplace": v_unplace, "reassign": v_reassign,
         "adjudicate": v_adjudicate,
         "adaptations": v_adaptations, "rooms": v_rooms, "contrast": v_contrast, "finding": v_finding,
         "findings": v_finding, "question": v_question, "contract": v_contract, "table": v_table,
         "view": v_view, "wiki": v_wiki, "diff-scheme": v_diff, "diff-model": v_diff,
         "ask": v_ask, "asks": v_asks, "audit": v_audit}
OVERLAY_VERBS = ("room", "codes", "theme", "themes", "where", "pairs", "scheme", "rooms", "contrast")


def parser():
    ap = argparse.ArgumentParser(add_help=False, prog="mem.py")
    ap.add_argument("verb", nargs="?")
    ap.add_argument("arg1", nargs="?")
    ap.add_argument("arg2", nargs="?")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--stage", default=None)
    ap.add_argument("--limit", type=int, default=80)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--page", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sub"); ap.add_argument("--room")
    ap.add_argument("--second"); ap.add_argument("--case-theme", dest="case_theme")
    ap.add_argument("--third"); ap.add_argument("--theme")
    ap.add_argument("--fourth"); ap.add_argument("--chunk")
    ap.add_argument("--dimension")
    ap.add_argument("--grep"); ap.add_argument("--level"); ap.add_argument("--top", type=int)
    ap.add_argument("--by-room", dest="by_room", action="store_true")
    ap.add_argument("--rooms")
    ap.add_argument("--field"); ap.add_argument("--summary", action="store_true")
    ap.add_argument("--sort", choices=["asc", "desc"]); ap.add_argument("--where", action="append")
    ap.add_argument("--nulls", action="store_true"); ap.add_argument("--slope", nargs=2, metavar=("X", "Y"))
    ap.add_argument("--brief", action="store_const", const=True, default=None)
    ap.add_argument("--kind"); ap.add_argument("--ids"); ap.add_argument("--label"); ap.add_argument("--trigger")
    ap.add_argument("--decision"); ap.add_argument("--reason"); ap.add_argument("--revised"); ap.add_argument("--pair")
    ap.add_argument("--dry-run", dest="dry_run", action="store_true")
    ap.add_argument("--element"); ap.add_argument("--with", dest="with_"); ap.add_argument("--without")
    ap.add_argument("--touching"); ap.add_argument("--section"); ap.add_argument("--from", dest="from_")
    ap.add_argument("--last", type=int, nargs="?", const=5)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-canvas", dest="no_canvas", action="store_true")
    ap.add_argument("--size", action="store_true")
    ap.add_argument("--plan", nargs="?", const="3", default=None)
    ap.add_argument("--assume"); ap.add_argument("--open", dest="open_only", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    return ap


def help_lines(verb):
    doc = __doc__.split("\n")
    if not verb:
        return doc
    rx = re.compile(r"^\s{2,6}%s\b" % re.escape(verb))
    out, on = [], False
    for l in doc:
        if rx.match(l):
            on = True
            out.append(l)
        elif on and l.startswith(" " * 20) and l.strip():
            out.append(l)
        else:
            on = False
    return out or ["no verb %s%s" % (verb, mean_hint(verb, VERBS))]


def main(argv=None):
    ap = parser()
    a, extra = ap.parse_known_intermixed_args(argv)
    if extra:
        print("mem.py: unrecognised %s; mem.py help lists the options" % " ".join(extra), file=sys.stderr)
        return 2
    if a.help or not a.verb or a.verb == "help":
        print("\n".join(help_lines(a.arg1 if a.verb == "help" else None)))
        return 0
    if a.verb not in VERBS:
        print("no such verb: %s%s; mem.py help lists them" % (a.verb, mean_hint(a.verb, VERBS)), file=sys.stderr)
        return 2
    out = a.out or os.path.join(a.root, "out")
    if not a.stage:
        # a session shared by several stages keeps its process environment, so $STAGE can be
        # stale there; the harness rewrites .stage at every hand-over, and it wins
        sp = os.path.join(a.root, ".stage")
        a.stage = (open(sp).read().strip() if os.path.exists(sp) else "") or os.environ.get("STAGE") or "xx"
    a.stage = a.stage.upper()
    if a.page:
        if a.page < 1:
            print("--page counts from 1", file=sys.stderr)
            return 2
        a.offset = (a.page - 1) * a.limit
    st = Store(a.root, out)
    refused, rc = None, 0
    try:
        lines = VERBS[a.verb](st, a)
    except Refuse as e:
        refused, lines, rc = str(e), [str(e)], 1
    except re.error as e:
        refused, lines, rc = "not a regular expression: %s" % e, ["not a regular expression: %s" % e], 1
    total = len(lines)
    if refused is None and a.offset and a.offset >= total:
        refused = "--offset %d is past the end: the output has %d lines" % (a.offset, total)
        lines, rc = [refused], 1
        page = lines
    else:
        end = a.offset + a.limit
        if not refused and a.verb == "forest" and not a.arg2:
            # a forest page ends at a thread boundary, so no thread is cut in two (up to four pages)
            while end < total and not lines[end].startswith("=== THREAD ") and end < a.offset + 4 * a.limit:
                end += 1
        page = lines if refused else lines[a.offset:end]
    for l in page:
        print(l)
    if not refused:
        rest = total - a.offset - len(page)
        if rest > 0:
            print("[lines %d-%d of %d; %d more: --offset %d]" % (a.offset + 1, a.offset + len(page), total, rest,
                                                                a.offset + len(page)))
        else:
            print("[end: lines %d-%d of %d]" % (a.offset + 1 if page else 0, a.offset + len(page), total))
        for n in (st.overlay()["notes"] if a.verb in OVERLAY_VERBS else []):
            print("note: " + n)
    defaults = vars(parser().parse_args([]))
    opts = {k.rstrip("_"): v for k, v in vars(a).items()
            if k not in ("verb", "arg1", "arg2", "root", "out", "stage", "help", "offset", "limit")
            and v != defaults.get(k)}
    try:                                   # the log names a room by its frame spelling, as cite.py's does
        rooms = {s.lower(): s for s in st.subs()}
        canon = lambda x: rooms.get((x[2:] if str(x).lower().startswith("r/") else str(x)).lower(), x) if x else x
        for k in ("sub", "room"):
            if opts.get(k):
                opts[k] = canon(opts[k])
        a.arg1, a.arg2 = canon(a.arg1), canon(a.arg2)
    except Exception:
        pass
    try:
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "_mem_reads-%s.jsonl" % a.stage), "a", encoding="utf-8") as f:
            f.write(json.dumps({"t": _stamp(), "stage": a.stage, "verb": a.verb,
                                "args": [x for x in (a.arg1, a.arg2) if x], "opts": opts,
                                "offset": a.offset, "limit": a.limit,
                                "lines": 0 if refused else len(page), "total": total,
                                "refused": refused}, ensure_ascii=False) + "\n")
    except OSError as e:
        print("note: the read log could not be written: %s" % e, file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
