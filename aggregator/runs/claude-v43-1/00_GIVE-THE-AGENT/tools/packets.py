#!/usr/bin/env python3
"""packets.py, v38: what a fleet reader is served, assembled by script so that every reader gets
the same page and nothing on it is the canvas, a room note or another reader's output (rule 7).
Every packet ends with the end line and the line telling the reader to confirm it reached it;
every shared page (index.md, the family pages) and every packet of B2, B4, E1 and files is
asserted under FLEET.md's 50 KB ceiling; a B3 batch packet is held instead to B2's packet shape,
at most 15 items and 180,000 bytes of item text (J, 2026-10-12); every build writes MANIFEST.json
beside the packets, which fleet.py reads for the item count.

    python3 tools/packets.py scheme [--scheme F] [--families F] --to DIR [--exemplars]
        the shared pages: index.md (rule 0 in the contract's words, then every family with every
        third-order theme's id, name, gloss and tier) and one page per family, G03.md, with each
        theme's full tests (gate, gate_parts, must_show, must_not_show, decide_when_both,
        discriminators, varies, is_not); exemplars only with --exemplars (stage B3's declared arm)

    python3 tools/packets.py B2 --round K [--items out/author_items.jsonl] [--scheme F] [--families F] [--to DIR]
    python3 tools/packets.py B2 --round gold --items out/gold_items.jsonl        on scheme_final.jsonl
    python3 tools/packets.py B2 --round stab-1|stab-2 --items out/gold_items.jsonl --brief out/brief-stab-1.md
        _packets-B2/round-K/ (or --to DIR): the shared pages from the current scheme (--scheme,
        else scheme_current.jsonl in out/scheme/ or out/, else scheme.jsonl), no exemplars, and one
        packet P03-rK.md holding the hard set's items (label, theme_note, concepts with the
        participants' words), shuffled under --seed. With --to and no --round the round is 1.

    python3 tools/packets.py B3 [--batches out/batches-B3.jsonl] [--exemplars] [--only B017]
                                [--scheme F] [--families F] [--to DIR]
        _packets-B3/ (or --to DIR): the shared pages from scheme_final.jsonl (or --scheme), and one file per
        line of batches-B3.jsonl, never split into parts: the sibling block (labels of all its second-order
        themes, labels only) for every room the packet holds an item from, so a reader sees each room's full
        theme list, then the items in the batch's order (duplicates and gold copies rendered as separate
        items), each numbered by position. B3 uses B2's packet shape (J, 2026-10-12): every packet is
        self-contained, at most 15 items and at most 180,000 bytes of item text; a room may be spread over
        several packets, and no item is split across two. MANIFEST.json records each packet's own "items"
        and "item_bytes" and no group, part or parts. A batch over either cap is refused before any file is
        written (redraw the batches); an item that alone exceeds 180,000 bytes stops the build: ask J. The
        shared pages are not counted toward the cap and stay under the 50 KB ceiling. The gold key never
        reaches the folder: batches carry items, and the packet shows no tag.

    python3 tools/packets.py B4 [--sample out/sample-B4.jsonl] [--scheme F] [--families F] [--to DIR]
        _packets-B4/ (or --to DIR): the shared pages from scheme_final.jsonl (or --scheme) (exemplars only with --exemplars,
        the same arm as B3), and one packet per reader group of the blind sample; no ruling, no
        disagreement, no hint that the items were decided before

    python3 tools/packets.py E1 [--sample out/reconstruction-sample-E1.jsonl]
        _packets-E1/: per sampled room, the skeleton from rebuild.py, the coder's case.md and the
        room's second-order themes; never model-D.md, the canvas or your notes

    python3 tools/packets.py files --stage NN --name C2-reviewer FILE [FILE ...]
        _packets-NN/<name>.md: the named files concatenated with their names as headings, for the
        stages whose one packet is a set of your own files (C2's reviewer, C5's readers)

An item is named as "<sub>/<theme_id>", {"sub", "theme_id"} or {"item": "<sub>/<theme_id>"}.
A path given to --scheme, --families, --items, --batches or --sample is taken as given, else under
out/. Options for every verb: --root . --out out --seed N (default 0) --per-packet N (B2, B4).
It reads out/ and the store and writes under out/_packets-NN/; it logs nothing, and it analyses
nothing: the readers' reads are yours to log under rule 1.
"""
import argparse, collections, datetime, glob, hashlib, json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CEILING = 50 * 1024
B3_ITEMS = 15                    # J, 2026-10-12: stage B3 uses B2's packet shape
B3_ITEM_BYTES = 180000
END = ("This is the end of the packet. Confirm you reached it by returning your lines and then the "
       "end marker the return specification names. END OF PACKET")
CANVAS = re.compile(r"\bcanvas_[a-z_]+\b")
TESTS = ("gate", "gate_parts", "must_show", "must_not_show", "decide_when_both", "varies", "is_not")
COUNT_04 = {"count_key": "position", "count_exclude": ["primary", "revises", "predicted_confusion"]}


def jl(p, need=True):
    if not os.path.exists(p):
        if need:
            sys.exit("no such file: %s" % p)
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def rule0(root):
    """Rule 0 in the contract's words, read from the contract, never restated here."""
    for p in (os.path.join(root, "CONTRACT-aggregator.md"), os.path.join(HERE, "..", "CONTRACT-aggregator.md")):
        if os.path.exists(p):
            t = open(p, encoding="utf-8").read()
            m = re.search(r"^0\. (\*\*Single placement.*?)(?=^1\. )", t, re.S | re.M)
            if m:
                return "Rule 0. " + " ".join(m.group(1).split())
    sys.exit("rule 0 was not found in CONTRACT-aggregator.md; the packets carry it in the contract's words")


def write(path, text, manifest, name, items, rule=None, ceiling=CEILING):
    """Write one served file and its MANIFEST entry. ceiling=None for a B3 batch packet, which is held to its
    item count and item bytes instead (v04 asserts them before writing)."""
    b = text.encode("utf-8")
    if CANVAS.search(text):
        sys.exit("%s carries a canvas field; nothing served carries the canvas (rule 7)" % path)
    if ceiling is not None and len(b) > ceiling:
        sys.exit("%s is %d bytes, over the 50 KB ceiling (FLEET.md); cut the batch or the scheme page" % (path, len(b)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    supersede_siblings(path, manifest)
    open(path, "w", encoding="utf-8").write(text)
    if manifest is not None and items is not None:
        e = {"items": items, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        e.update(rule or {})
        manifest[name] = e


def supersede_siblings(path, manifest):
    """A batch rebuilt whole leaves its old parts, and a batch rebuilt in parts leaves its old whole
    file; either would reach a reader beside the new one. They move to _superseded/<utc>/ (never
    deleted) and leave the manifest."""
    d, base = os.path.dirname(path), os.path.splitext(os.path.basename(path))[0]
    m = re.match(r"^(.*)-p\d+$", base)
    stale = ([os.path.join(d, m.group(1) + ".md")] if m else glob.glob(os.path.join(d, base + "-p*.md")))
    stale = [x for x in stale if os.path.exists(x)]
    if not stale:
        return
    to = os.path.join(d, "_superseded", datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"))
    os.makedirs(to, exist_ok=True)
    mp = os.path.join(d, "MANIFEST.json")
    old = json.load(open(mp)) if os.path.exists(mp) else {}
    for x in stale:
        n = os.path.splitext(os.path.basename(x))[0]
        os.replace(x, os.path.join(to, os.path.basename(x)))
        old.pop(n, None)
        if manifest is not None:
            manifest.pop(n, None)
    json.dump(old, open(mp, "w"), indent=1)


def save_manifest(d, manifest):
    p = os.path.join(d, "MANIFEST.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(manifest)
    json.dump(old, open(p, "w"), indent=1)


class Store:
    def __init__(self, root, out=None):
        S = os.path.join(root, "package", "store")
        import vlib                                  # the split layer, out/recut/ (J, 2026-10-12, QB2-010)
        lay = lambda n: vlib.recut_overlay(n, jl(os.path.join(S, n + ".jsonl")), out)
        self.themes = {(t["sub"], t["theme_id"]): t for t in lay("themes")}
        self.by_sub = collections.defaultdict(list)
        for t in self.themes.values():
            self.by_sub[t["sub"]].append(t)
        self.codes = {(c["sub"], c["code_id"]): c for c in lay("codes")}

    def item(self, sub, tid, pos=None):
        t = self.themes.get((sub, tid))
        head = "### %s%s/%s" % ("%d. " % pos if pos is not None else "", sub, tid)
        if t is None:
            return [head, "", "(this second-order theme is not in the store)", ""]
        L = [head, "", "label: %s" % (t.get("second_order") or ""), "",
             "note: %s" % " ".join(str(t.get("theme_note") or "").split()), ""]
        for cid in t.get("code_ids") or []:
            c = self.codes.get((sub, cid))
            if not c:
                continue
            L.append("- %s  %s" % (cid, c.get("first_order") or ""))
            L.append("    \"%s\"" % " ".join(str(c.get("text") or "").split()))
        L.append("")
        return L

    def sibling(self, sub):
        ts = sorted(self.by_sub.get(sub, []), key=lambda t: t["theme_id"])
        return (["## r/%s" % sub, "", "sibling block, the labels of all %d second-order themes of this room "
                 "(labels only):" % len(ts)] + ["- %s %s" % (t["theme_id"], t.get("second_order") or "") for t in ts] + [""])


def path_in(out, f):
    """A path as given when it exists, else under out/."""
    return f if f and (os.path.isabs(f) or os.path.exists(f)) else os.path.join(out, f)


def load_scheme(out, prefer):
    for f in prefer:
        for p in (path_in(out, f), os.path.join(out, "scheme", f)):
            if os.path.exists(p):
                rows = []
                for r in jl(p):
                    r = dict(r)
                    r["id"] = r.get("id") or r.get("theme")
                    r["name"] = r.get("name") or r.get("label")
                    rows.append(r)
                return rows, os.path.relpath(p, out) if not os.path.isabs(f) else p
    sys.exit("none of %s in %s" % (", ".join(prefer), out))


def scheme_pages(root, out, to, scheme_rows, families, exemplars):
    by_id = {s["id"]: s for s in scheme_rows}
    L = ["# The scheme: index", "", rule0(root), "",
         "Every family below has its own page (`<family>.md`) with each theme's full tests. Read this "
         "index whole; open a family's page before placing anything into it, and record the families "
         "you opened on the line you return (`families_opened`).", ""]
    seen = set()
    for f in families:
        L += ["## %s  %s" % (f["family"], f.get("name") or ""), ""]
        for t in f.get("themes") or []:
            s = by_id.get(t)
            if not s:
                L.append("- %s  (not in the scheme file)" % t)
                continue
            seen.add(t)
            L.append("- **%s**%s  %s: %s" % (s["id"], " [rare]" if s.get("tier") == "rare" else "",
                                             s.get("name") or "", s.get("gloss") or ""))
        L.append("")
    stray = [s for s in scheme_rows if s["id"] not in seen]
    if stray:
        L += ["## themes in no family", ""] + ["- **%s**  %s: %s" % (s["id"], s.get("name") or "", s.get("gloss") or "")
                                              for s in stray] + [""]
    write(os.path.join(to, "index.md"), "\n".join(L), None, None, None)
    for f in families:
        P = ["# Family %s  %s" % (f["family"], f.get("name") or ""), "",
             "The full tests of every theme in this family. A placement rests on the gate; the "
             "discriminators say what separates a theme from its nearest neighbours.", ""]
        for t in f.get("themes") or []:
            s = by_id.get(t)
            if not s:
                continue
            P += ["## %s  %s%s" % (s["id"], s.get("name") or "", "  [rare]" if s.get("tier") == "rare" else ""), "",
                  "gloss: %s" % (s.get("gloss") or "")]
            for k in TESTS:
                v = s.get(k)
                if v not in (None, "", []):
                    P.append("%s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
            for d in s.get("discriminators") or []:
                P.append("vs %s: %s" % (d.get("vs"), d.get("question")))
            if exemplars:
                for e in s.get("exemplars") or []:
                    P.append("exemplar (r/%s, %s): \"%s\"" % (e.get("sub"), e.get("code_id"), e.get("quote")))
            P.append("")
        write(os.path.join(to, "%s.md" % f["family"]), "\n".join(P), None, None, None)
    return len(families)


def key_of(x):
    """(sub, theme_id) from "sub/tNN", {"sub", "theme_id"} or {"item": "sub/tNN"}."""
    if isinstance(x, str):
        if "/" not in x:
            sys.exit("item %r is not <sub>/<theme_id>" % x)
        s, t = x.split("/", 1)
        return s, t
    item = str(x.get("item") or "")
    s = x.get("sub") or (item.split("/", 1)[0] if "/" in item else None)
    t = x.get("theme_id") or x.get("case_theme") or (item.split("/", 1)[1] if "/" in item else None)
    if not s or not t:
        sys.exit("item %s names no <sub>/<theme_id>: give sub and theme_id, or item as \"sub/tNN\"" % json.dumps(x))
    return s, t


def items_packet(title, intro, items, store, siblings):
    L = ["# %s" % title, "", intro, ""]
    if siblings:
        for s in dict.fromkeys(s for s, _ in items):
            L += store.sibling(s)
    L += ["## The items", ""]
    for pos, (s, t) in enumerate(items, 1):
        L += store.item(s, t, pos)
    L += ["", END, ""]
    return "\n".join(L)


def v_scheme(a, root, out):
    rows, _ = load_scheme(out, [a.scheme] if a.scheme else ["scheme_final.jsonl"])
    fams = jl(path_in(out, a.families or "families.jsonl"))
    n = scheme_pages(root, out, a.to, rows, fams, a.exemplars)
    print("index.md and %d family pages in %s (%d themes, exemplars %s)" % (n, a.to, len(rows), "served" if a.exemplars else "withheld"))


def v03(a, root, out, store):
    if not a.round and not a.to:
        sys.exit("B2 needs --round K (or --to DIR)")
    a.round = a.round or "1"
    after = a.round in ("gold", "stab-1", "stab-2")       # on the frozen scheme (stage B2 section 5)
    rows, sname = load_scheme(out, [a.scheme] if a.scheme else (["scheme_final.jsonl"] if after else
                                                                   ["scheme_current.jsonl", "scheme.jsonl"]))
    fams = jl(path_in(out, a.families or "families.jsonl"))
    to = a.to or os.path.join(out, "_packets-B2", "round-%s" % a.round)
    scheme_pages(root, out, to, rows, fams, False)
    items = [key_of(x) for x in jl(path_in(out, a.items or "author_items.jsonl"))]
    items = list(dict.fromkeys(items))
    random.Random(a.seed).shuffle(items)
    man = {}
    name = "P03-r%s" % a.round
    intro = ("Place each second-order theme below onto the scheme, one line per item in the form the return "
             "specification gives. Items are numbered by position.")
    if a.brief:                    # a stability round: the same items under a reworded brief that changes no test
        intro = open(path_in(out, a.brief), encoding="utf-8").read().strip()
    elif a.round.startswith("stab"):
        sys.exit("a stability round needs --brief <file>: the brief reworded, changing no test (stage B2 section 5)")
    txt = items_packet("Pilot round %s" % a.round, intro, items, store, False)
    write(os.path.join(to, "%s.md" % name), txt, man, name, len(items), COUNT_04)
    save_manifest(to, man)
    print("%s: shared pages from %s, one packet of %d items" % (to, sname, len(items)))


INTRO_04 = ("Each room is introduced once by the labels of all its second-order themes (the sibling block). "
            "Then the items, interleaved across rooms, numbered by position. Place each item; return one line "
            "per item in the form the return specification gives, the prediction line first.")


def item_bytes(store, items):
    """Bytes of item text of a packet: each item's block as items_packet renders it (header, label, note,
    concepts with the participants' words), positions included; the sibling blocks and the intro are not
    item text. Returns (total, [bytes per item])."""
    per = [len(("\n".join(store.item(s, t, pos)) + "\n").encode("utf-8")) for pos, (s, t) in enumerate(items, 1)]
    return sum(per), per


def v04(a, root, out, store):
    """B3: one self-contained packet per batch line, B2's packet shape (J, 2026-10-12). Every batch is
    measured before any packet is written, so a refusal leaves the folder as it was."""
    rows, sname = load_scheme(out, [a.scheme] if a.scheme else ["scheme_final.jsonl"])
    fams = jl(path_in(out, a.families or "families.jsonl"))
    to = a.to or os.path.join(out, "_packets-B3")
    batches = jl(path_in(out, a.batches or "batches-B3.jsonl"))
    plan, over = [], []
    for b in batches:
        name = b.get("batch")
        if a.only and name not in a.only.split(","):
            continue
        items = [key_of(x) for x in b.get("items") or []]
        if not items:
            sys.exit("batch %s has no items" % name)
        ib, per = item_bytes(store, items)
        for (s, t), n in zip(items, per):
            if n > B3_ITEM_BYTES:
                sys.exit("batch %s: item %s/%s alone is %d bytes of item text, over the %d-byte cap of a B3 packet; "
                         "no item is split across packets, so this item cannot be served as the ruling stands: ask J"
                         % (name, s, t, n, B3_ITEM_BYTES))
        if len(items) > B3_ITEMS or ib > B3_ITEM_BYTES:
            over.append("%s (%d items, %d bytes of item text)" % (name, len(items), ib))
        plan.append((name, items, ib))
    if over:
        sys.exit("REFUSING: %d batches exceed a B3 packet's shape, at most %d items and %d bytes of item text "
                 "(J, 2026-10-12): %s. Redraw batches-B3.jsonl under both caps; a batch is never split into parts"
                 % (len(over), B3_ITEMS, B3_ITEM_BYTES, "; ".join(over[:8])))
    scheme_pages(root, out, to, rows, fams, a.exemplars)
    shared = sum(os.path.getsize(os.path.join(to, f)) for f in os.listdir(to) if f.endswith(".md"))
    man = {}
    for name, items, ib in plan:
        txt = items_packet("Batch %s" % name, INTRO_04, items, store, True)
        write(os.path.join(to, "%s.md" % name), txt, man, name, len(items), dict(COUNT_04, item_bytes=ib),
              ceiling=None)
    save_manifest(to, man)
    big = max((ib for _, _, ib in plan), default=0)
    print("%s: shared pages from %s (exemplars %s, %d bytes), %d batch packets, at most %d items and %d bytes of "
          "item text each (largest %d)" % (to, sname, "served" if a.exemplars else "withheld", shared, len(plan),
                                           B3_ITEMS, B3_ITEM_BYTES, big))


def v05(a, root, out, store):
    rows, sname = load_scheme(out, [a.scheme] if a.scheme else ["scheme_final.jsonl"])
    fams = jl(path_in(out, a.families or "families.jsonl"))
    to = a.to or os.path.join(out, "_packets-B4")
    scheme_pages(root, out, to, rows, fams, a.exemplars)
    items = [key_of(x) for x in jl(path_in(out, a.sample or "sample-B4.jsonl"))]
    items = list(dict.fromkeys(items))
    random.Random(a.seed).shuffle(items)
    per = a.per_packet or 25
    man = {}
    k = 0
    for i in range(0, len(items), per):
        k += 1
        name = "S05-%02d" % k
        txt = items_packet("Items %s" % name, "Place each second-order theme below onto the scheme, one line per "
                           "item in the form the return specification gives. Items are numbered by position.",
                           items[i:i + per], store, False)
        write(os.path.join(to, "%s.md" % name), txt, man, name, len(items[i:i + per]), COUNT_04)
    save_manifest(to, man)
    print("%s: shared pages from %s, %d packets of at most %d items" % (to, sname, k, per))


def v13(a, root, out, store):
    rows = jl(a.sample or os.path.join(out, "reconstruction-sample-E1.jsonl"))
    to = os.path.join(out, "_packets-E1")
    man = {}
    for r in rows:
        sub = r["sub"]
        sk = subprocess.run([sys.executable, os.path.join(HERE, "rebuild.py"), sub, "--out", out],
                            capture_output=True, text=True, cwd=root)
        if sk.returncode:
            sys.exit("rebuild.py %s failed: %s" % (sub, sk.stderr.strip()[:300]))
        cp = os.path.join(root, "package", sub, "case.md")
        case = open(cp, encoding="utf-8").read() if os.path.exists(cp) else "(no case.md in package/%s)" % sub
        L = ["# Reconstruction packet", "",
             "Score, claim by claim of the coder's account below, whether the skeleton accounts for it, "
             "with the element id or `none`, one line per claim in the form the return specification gives. "
             "State unresolved evidence or stale versions in each affected claim reason. Pending or rejected lines are not asserted support; "
             "silence is not negative evidence. Report unresolved claim counts separately from contradiction. Reproduce the skeleton current model version and local status in the summary.", "",
             "## The skeleton (the global model with supported local adaptations and explicit uncertainty)", "", sk.stdout.strip(), "",
             "## The coder's account", "", case.strip(), "",
             "## The room's second-order themes", ""]
        for t in sorted(store.by_sub.get(sub, []), key=lambda t: t["theme_id"]):
            L.append("- %s %s" % (t["theme_id"], t.get("second_order") or ""))
        L += ["", END, ""]
        write(os.path.join(to, "%s.md" % sub), "\n".join(L), man, sub, None)
    save_manifest(to, man)
    print("%s: %d reconstruction packets" % (to, len(rows)))


def v_files(a, root, out):
    if not a.stage or not a.name or not a.files:
        sys.exit("files needs --stage NN --name <packet> and the files")
    to = os.path.join(out, "_packets-%s" % a.stage)
    L = ["# Packet %s" % a.name, ""]
    for f in a.files:
        p = f if os.path.isabs(f) or os.path.exists(f) else os.path.join(out, f)
        if not os.path.exists(p):
            sys.exit("no such file: %s" % f)
        L += ["## %s" % os.path.basename(p), "", open(p, encoding="utf-8").read().strip(), ""]
    L += ["", END, ""]
    man = {}
    write(os.path.join(to, "%s.md" % a.name), "\n".join(L), man, a.name, None)
    save_manifest(to, man)
    print("%s/%s.md: %d files" % (to, a.name, len(a.files)))


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("verb", nargs="?")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--scheme"); ap.add_argument("--families")
    ap.add_argument("--to"); ap.add_argument("--exemplars", action="store_true")
    ap.add_argument("--round"); ap.add_argument("--items")
    ap.add_argument("--batches"); ap.add_argument("--only")
    ap.add_argument("--sample"); ap.add_argument("--per-packet", type=int, default=None)
    ap.add_argument("--stage"); ap.add_argument("--name"); ap.add_argument("--brief")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_intermixed_args()
    if a.verb and a.verb.upper() in ("B2", "B3", "B4", "E1"):
        a.verb = a.verb.upper()
    if a.help or a.verb not in ("scheme", "B2", "B3", "B4", "E1", "files"):
        print(__doc__)
        return 0 if a.help else 2
    root = a.root
    out = a.out or os.path.join(root, "out")
    if a.verb == "scheme":
        if not a.to:
            sys.exit("scheme needs --to DIR")
        return v_scheme(a, root, out) or 0
    if a.verb == "files":
        return v_files(a, root, out) or 0
    store = Store(root, out)
    return {"B2": v03, "B3": v04, "B4": v05, "E1": v13}[a.verb](a, root, out, store) or 0


if __name__ == "__main__":
    sys.exit(main())
