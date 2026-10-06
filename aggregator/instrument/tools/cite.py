#!/usr/bin/env python3
"""cite.py, v38: the only way a quote enters an output (rule 3). Every call is logged.

    python3 tools/cite.py --room <sub> --code <id>                one code's words, verbatim
    python3 tools/cite.py --room <sub> --theme <tNN> [--n K]       K quotes from a second-order theme
    python3 tools/cite.py --tier 3rd|4th|dim --id <T3-..|T4-..|D..> [--n K] [--room <sub>]
                                                                   K quotes under a tier, across rooms
    python3 tools/cite.py --resolve "<words>" [--room <sub>]       which code these words are cut
                                                                   from; the close-check's verb
    python3 tools/cite.py --grep <re> [--room <sub>] [--n K]       codes whose words match; grounds
                                                                   a claim, never chooses a reading
    python3 tools/cite.py --room <sub> --code <id> --context K     the quote with its parent and the
                                                                   K items before and after it in the
                                                                   thread: their coded passages and
                                                                   the forest's labels (the store
                                                                   holds no uncoded body)
    options: --root . --out out --stage NN --seed 0 --json

Every header says how many codes match and how many are shown (`39 match; 5 shown`). A room is
named bare, as r/<sub> or <sub>/, in any case; a wrong room is refused with the nearest name.

A quote is the participant's words as the coder cut them (`codes.jsonl`: `text`, `start`, `end`),
never the coder's label (`first_order`), the theme's label (`second_order`) or a `note`. `--resolve`
says which code holds the words, or refuses: `no code holds these words` when nothing does, and
`REJECT: matches a label or a note, not a participant's words` when only a label or note does.
The close-check at B1 runs `--resolve` on every exemplar (rule 3).

Each returned quote carries its citation, `[sub/code_id]`, plus item, thread, hour, author and
the second-order theme; an output that quotes writes the citation beside the words. With `--n K`
and more than K candidates, K are drawn at random under `--seed` (default 0, so a rerun draws the
same), never the first K by id: the first K are the coder's early passages, not a sample.

Log: out/_cite_reads-NN.jsonl, one line per call, harness-stamped stage as mem.py.
"""
import argparse, datetime, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mem  # noqa: E402  (Store, overlay, jl, clip)


def line(c):
    return ('"%s"  [%s/%s]  item %s  thread %s  h%+.2f  %s  %s %s'
            % (" ".join(str(c.get("text") or "").split()), c["sub"], c["code_id"], c.get("item_id"),
               c.get("thread_id"), c["hour"] if c.get("hour") is not None else float("nan"),
               c.get("author") or "?", c.get("theme_id"), mem.clip(c.get("second_order") or "", 50)))


def pick(rows, n, seed):
    if n is None or len(rows) <= n:
        return rows
    rnd = random.Random(seed)
    return sorted(rnd.sample(rows, n), key=lambda c: (c["sub"], c["code_id"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--room"); ap.add_argument("--code"); ap.add_argument("--theme")
    ap.add_argument("--tier", choices=["3rd", "4th", "dim"]); ap.add_argument("--id")
    ap.add_argument("--resolve"); ap.add_argument("--grep")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--context", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--root", default="."); ap.add_argument("--out", default=None)
    ap.add_argument("--stage", default=None); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    out = a.out or os.path.join(a.root, "out")
    if not a.stage:
        sp = os.path.join(a.root, ".stage")
        a.stage = (open(sp).read().strip() if os.path.exists(sp) else "") or os.environ.get("STAGE") or "xx"
    st = mem.Store(a.root, out)
    codes = st.rows("codes")
    ctx_lines = []
    if a.room:
        try:
            a.room = st.room(a.room)
        except mem.Refuse as e:
            print(e)
            log(out, a, str(e), [])
            return 1
        codes = [c for c in codes if c["sub"] == a.room]
    sel, verdict = [], None

    if a.resolve:
        want = " ".join(a.resolve.split())
        hits = [c for c in codes if want and want in " ".join(str(c.get("text") or "").split())]
        if hits:
            sel = pick(hits, a.n, a.seed)
            verdict = "resolved: %d code(s) hold these words; %s" % (len(hits), "%d shown" % len(sel) if len(sel) < len(hits) else "all shown")
        else:
            lab = [c for c in codes if want and (want in " ".join(str(c.get("first_order") or "").split())
                                                 or want in " ".join(str(c.get("note") or "").split())
                                                 or want in " ".join(str(c.get("second_order") or "").split()))]
            verdict = ("REJECT: matches a label or a note, not a participant's words (%s)"
                       % ", ".join("%s/%s" % (c["sub"], c["code_id"]) for c in lab[:5])
                       if lab else "no code holds these words")
    elif a.code:
        if not a.room:
            sys.exit("--code needs --room")
        sel = [c for c in codes if c["code_id"] == a.code]
        verdict = None if sel else "no such code: %s/%s%s" % (a.room, a.code, mem.mean_hint(a.code, [c["code_id"] for c in codes]))
        if sel and a.context is not None:
            ctx_lines = context(st, sel[0], a.context)
    elif a.theme:
        if not a.room:
            sys.exit("--theme needs --room")
        pool = [c for c in codes if c.get("theme_id") == a.theme]
        sel = pick(pool, a.n, a.seed)
        verdict = ("%s/%s: %s" % (a.room, a.theme, shown(len(pool), len(sel))) if sel else
                   "no codes on %s/%s%s" % (a.room, a.theme, mem.mean_hint(a.theme, {c.get("theme_id") for c in codes})))
    elif a.tier:
        if not a.id:
            sys.exit("--tier needs --id")
        ov = st.overlay()
        if a.tier == "3rd":
            keys = {k for k, so in ov["placed"].items() if a.id in so}
        elif a.tier == "4th":
            members = set(ov["chunks"].get(a.id, {}).get("members", []))
            keys = {k for k, so in ov["placed"].items() if members & set(so)}
        else:
            t4 = set(ov["dims"].get(a.id, {}).get("members", []))
            members = {s for s, c in ov["chunk_of"].items() if c in t4}
            keys = {k for k, so in ov["placed"].items() if members & set(so)}
        pool = [c for c in codes if (c["sub"], c.get("theme_id")) in keys]
        sel = pick(pool, a.n, a.seed)
        verdict = ("%s: %s" % (a.id, shown(len(pool), len(sel))) if sel else
                   "nothing placed under %s (%s)" % (a.id, ov["assign_file"] or "no placements yet"))
    elif a.grep:
        rx = re.compile(a.grep, re.I)
        pool = [c for c in codes if rx.search(str(c.get("text") or ""))]
        sel = pick(pool, a.n, a.seed)
        verdict = "%s; a grep grounds a claim and never chooses a reading (rule 2)" % shown(len(pool), len(sel))
    else:
        ap.print_help()
        return 2

    if a.json:
        print(json.dumps({"verdict": verdict, "quotes": sel, "context": ctx_lines}, ensure_ascii=False))
    else:
        if verdict:
            print(verdict)
        for c in sel:
            print(line(c))
        for l in ctx_lines:
            print(l)
        if sel:
            print("rooms: %d  quotes: %d" % (len({c["sub"] for c in sel}), len(sel)))
        print("[end]")
    log(out, a, verdict, sel)
    return 0 if not (verdict or "").startswith(("REJECT", "no ", "nothing")) else 1


def shown(n, k):
    return "%d match; %d shown" % (n, k) if k < n else "%d match; all shown" % n


def log(out, a, verdict, sel):
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "_cite_reads-%s.jsonl" % a.stage), "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                            "stage": a.stage,
                            "opts": {k: v for k, v in vars(a).items()
                                     if k not in ("root", "out", "stage") and v not in (None, False)},
                            "verdict": verdict,
                            "cited": ["%s/%s" % (c["sub"], c["code_id"]) for c in sel]}, ensure_ascii=False) + "\n")


def context(st, c, k):
    """The thread around one quote: its parent, then the k items before and after it by time, each
    with its coded passages and the forest's labels. Bodies of uncoded items are not in the store."""
    items = [i for i in st.rows("items") if i["sub"] == c["sub"] and i.get("thread_id") == c.get("thread_id")]
    if not items:
        return ["context: the store holds no items for thread %s of r/%s" % (c.get("thread_id"), c["sub"])]
    items.sort(key=lambda i: (i.get("created_utc") or 0, i.get("coord") or ""))
    idx = next((n for n, i in enumerate(items) if i.get("item_id") == c.get("item_id")), None)
    if idx is None:
        return ["context: item %s is not in the store's items for thread %s" % (c.get("item_id"), c.get("thread_id"))]
    me = items[idx]
    codes = {x["code_id"]: x for x in st.rows("codes") if x["sub"] == c["sub"] and x.get("thread_id") == c.get("thread_id")}
    by_id = {i.get("item_id"): i for i in items}
    win = list(range(max(0, idx - k), min(len(items), idx + k + 1)))
    parent = by_id.get(me.get("parent_id"))
    L = ["", "context: thread %s of r/%s, %d items in the store; the item, its parent and %d on each side by time"
         % (c.get("thread_id"), c["sub"], len(items), k)]

    def show(i, tag):
        L.append("  %-7s [%s] %s h%+.2f%s" % (tag, i.get("coord"), i.get("author") or "?",
                                            i.get("hour") if i.get("hour") is not None else float("nan"),
                                            "  reply to [%s]" % by_id[i["parent_id"]].get("coord") if i.get("parent_id") in by_id else ""))
        cs = [codes[x] for x in i.get("codes") or [] if x in codes]
        if not cs:
            L.append("          (%s; no body in the store)" % (i.get("state") or "uncoded"))
        for x in cs:
            L.append("          %s %s | \"%s\"" % (x["code_id"], mem.clip(x.get("first_order"), 70),
                                                 " ".join(str(x.get("text") or "").split())))
    if parent is not None and items.index(parent) not in win:
        show(parent, "parent")
    for n in win:
        i = items[n]
        tag = "QUOTE" if n == idx else "parent" if i is parent else "reply" if i.get("parent_id") == me.get("item_id") else "before" if n < idx else "after"
        show(i, tag)
    return L


if __name__ == "__main__":
    sys.exit(main())
