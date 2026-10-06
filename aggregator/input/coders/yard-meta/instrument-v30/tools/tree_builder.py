#!/usr/bin/env python3
"""tree_builder.py — the conversational code forest, instrument v30.

Deterministic. No model runs here. Joins the coders' first-order codes onto the
reply tree of every coded thread and writes three files:

  trees/<sub>.md           the rendered forest, for a reader
  package/forest.jsonl     one line per coded thread, the tree serialised
  package/tree_index.json  coordinate -> item id and metadata, for drill-down

Coordinates are pure Dewey. The submission is "0". Its replies are "1", "2", ...
in time order; their replies "1.1", "1.2", ...; and so on to any depth. Depth is
the number of segments; two coordinates are siblings when they share every
segment but the last. There is no special case for the top level.

Node states, and the counts that go with them:
  coded      carries at least one code id
  bridge     no code, but a coded descendant. Kept, so the distance between two
             coded turns stays visible.
  removed    a platform removal notice (a moderator-distinguished item whose
             body says the post was removed). The platform speaking, not a
             participant; kept as its own state, never as a bridge.
  pruned     no code and no coded descendant. Dropped from the render.
  collapsed  a run of pruned siblings, replaced by one summary node.
An item whose parent is not in the record is hung on the submission, marked
[parent outside the record], and counted in the header; no coded turn vanishes.

Every pruned item is counted per thread and per community. A forest that drops
material without saying how much would let a reader mistake what was not coded
for what was not said.

Metadata travels with each node when the record carries it: distinguished,
stickied, edited, gilded, score, link_flair, author_flair, plus retrieved_on.
Every rendered line shows it: `↑N` is the score at retrieval (0 and negative
scores kept; `↑?` when the record has none), `⟨…⟩` after an author is their
flair in this community, `{…}` on a submission is its flair, and the marks
[moderator], [sticky@retrieval], [edited], [gilded] say what kind of item it
was. `stickied` and the score are snapshots taken at retrieval, weeks after
the event: lower bounds with no timing. `distinguished` is reliable. Every
meta block carries `retrieved_on` so nobody reads a May snapshot as an April
fact.

Input threads: one JSON object per thread with "thread_id", "title", "selftext",
"author", "created_utc", optional "hours_since_open", optional "retrieved_on",
optional meta keys, and "comments": a list of {"item_id", "parent_id", "author",
"created_utc", "body", optional meta keys}. parent_id may carry the t1_/t3_
prefix or not. Codes: {"code_id", "item_id", "label"}.
"""
import argparse, json, os, re, sys, tempfile
from collections import defaultdict

META_KEYS = ("distinguished", "stickied", "edited", "gilded", "score",
             "link_flair_text", "author_flair_text", "retrieved_on")
REMOVAL_RE = re.compile(r"\b(this (post|comment) (was|has been) removed|removed because)\b", re.I)


def strip_prefix(x):
    """'t3_62pyj5' -> '62pyj5', 't1_dfoey5e' -> 'dfoey5e'; anything else unchanged."""
    if isinstance(x, str) and len(x) > 3 and x[0] == "t" and x[1].isdigit() and x[2] == "_":
        return x[3:]
    return x


def fmt_dt(sec):
    if sec is None:
        return "?"
    if sec < 60:
        return "+%.0fs" % sec
    if sec < 3600:
        return "+%.1fm" % (sec / 60.0)
    return "+%.1fh" % (sec / 3600.0)


class Node:
    __slots__ = ("item_id", "parent_id", "author", "created_utc", "body", "coord",
                 "dt_parent", "dt_thread", "code_ids", "labels", "children",
                 "keep", "state", "collapsed_n", "meta", "sequence", "coverage", "n_na")

    def __init__(self, item_id, parent_id, author, created_utc, body, meta):
        self.item_id = item_id
        self.parent_id = parent_id
        self.author = author
        self.created_utc = created_utc
        self.body = body or ""
        self.coord = ""
        self.dt_parent = 0.0
        self.dt_thread = 0.0
        self.code_ids = []
        self.labels = []
        self.children = []
        self.keep = False
        self.state = "pruned"
        self.collapsed_n = 0
        self.meta = meta
        self.sequence = []      # code ids in text order, with "na" for an uncoded stretch
        self.coverage = None    # share of the body's characters under a code
        self.n_na = 0


def pick_meta(rec):
    """The meta keys the forest carries. A score of 0 is a fact and is kept; the other
    keys are kept only when set (an unedited, unstickied item carries nothing)."""
    m = {}
    for k in META_KEYS:
        v = rec.get(k)
        if k == "score":
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                m[k] = int(v)
        elif v not in (None, "", False, 0):
            m[k] = v
    return m


FLAIR_MAX = 28


def clip(s, n=FLAIR_MAX):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + "…"


def who(node):
    """author, with their flair in this community when the record has it."""
    fl = node.meta.get("author_flair_text")
    return "%s ⟨%s⟩" % (node.author, clip(fl)) if fl else node.author


def score(node):
    s = node.meta.get("score")
    return "↑?" if s is None else "↑%d" % s


def label_of(c):
    """build_store.py hands codes with `label`; emit writes `first_order`."""
    return c.get("label") or c.get("first_order") or ""


NA_MIN_CHARS = 40   # an uncovered stretch shorter than this is punctuation or a fragment, not na


def attach_codes(node, codes):
    """Hang a node's codes on it in TEXT order and compute the coded sequence.

    Every code is a cited chunk of the item (start, end, text). The sequence is the code ids
    in the order their chunks sit in the body, with `na` wherever a stretch of at least
    NA_MIN_CHARS characters carries no code: [c0012, na, c0015, c0016]. So a reader sees, for
    each turn, what was coded and what the coder passed over, in order. Coverage is the share
    of the body's characters under some code. Offsets are used where they match the body;
    otherwise the code's text is searched for, since a post's offsets may be against the
    title, the selftext or their join."""
    body = node.body or ""
    spans = []
    for c in codes:
        text = c.get("text") or ""
        a, b = c.get("start"), c.get("end")
        pos = None
        if isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(body) and body[a:b] == text:
            pos = (a, b)
        elif text:
            i = body.find(text)
            if i >= 0:
                pos = (i, i + len(text))
        spans.append((pos if pos else (10 ** 9, 10 ** 9), c))
    spans.sort(key=lambda x: (x[0][0], x[0][1]))
    node.code_ids = [c["code_id"] for _, c in spans]
    node.labels = [label_of(c) for _, c in spans]
    seq, covered, cursor = [], 0, 0
    located = any(a < 10 ** 9 for (a, _), _ in spans)
    if not located:
        # codes without a cited chunk (an older store): the ids, no na, no coverage
        node.sequence = list(node.code_ids); node.n_na = 0; node.coverage = None
        return
    for (a, b), c in spans:
        if a >= 10 ** 9:
            seq.append(c["code_id"]); continue
        if a - cursor >= NA_MIN_CHARS and (not seq or seq[-1] != "na"):
            seq.append("na")
        seq.append(c["code_id"])
        if b > cursor:
            covered += b - max(a, cursor); cursor = b
    if len(body) - cursor >= NA_MIN_CHARS and (not seq or seq[-1] != "na"):
        seq.append("na")
    node.sequence = seq
    node.n_na = seq.count("na")
    node.coverage = round(covered / len(body), 2) if body and codes else None


def is_removal(rec):
    return bool(rec.get("distinguished")) and bool(REMOVAL_RE.search(rec.get("body", "") or ""))


def build(thread, codes_by_item):
    t0 = thread.get("created_utc", 0.0)
    root = Node(strip_prefix(thread["thread_id"]), None, thread.get("author", "[unknown]"), t0,
                (thread.get("title", "") + " " + thread.get("selftext", "")).strip(),
                pick_meta(thread))
    nodes = {root.item_id: root}
    root_codes = codes_by_item.get(root.item_id, [])
    if root_codes:
        # cite's join for a post is title + blank line + selftext; the node body follows it
        root.body = (thread.get("title", "") + "\n\n" + thread.get("selftext", "")).strip()
        attach_codes(root, root_codes)
    removed = set()
    for it in thread.get("comments", []):
        iid = strip_prefix(it["item_id"])
        n = Node(iid, strip_prefix(it.get("parent_id")), it.get("author", "[unknown]"),
                 it.get("created_utc", t0), it.get("body", ""), pick_meta(it))
        n.dt_thread = max(0.0, n.created_utc - t0)
        if codes_by_item.get(iid):
            attach_codes(n, codes_by_item[iid])
        if is_removal(it):
            removed.add(iid)
        nodes[iid] = n
    orphans = 0
    for n in list(nodes.values()):
        if n.parent_id is None:
            continue
        p = nodes.get(n.parent_id)
        if p is None:
            # the parent is outside the record (before the window, or removed before retrieval).
            # The turn is kept, hung on the submission and marked, so no coded turn vanishes.
            orphans += 1
            n.meta = dict(n.meta, parent_missing=True)
            p = root
        p.children.append(n)
    for n in nodes.values():
        n.children.sort(key=lambda x: x.created_utc)
        for ch in n.children:
            ch.dt_parent = max(0.0, ch.created_utc - n.created_utc)
    return root, nodes, orphans, removed


def mark(node, removed):
    keep_below = False
    for ch in node.children:
        if mark(ch, removed):
            keep_below = True
    coded = bool(node.code_ids)
    if coded:
        node.state = "coded"
    elif node.item_id in removed:
        node.state = "removed"
    elif keep_below:
        node.state = "bridge"
    else:
        node.state = "pruned"
    node.keep = node.state != "pruned"
    return node.keep


def count_all(node):
    return sum(1 + count_all(c) for c in node.children)


def collapse(node, min_run):
    dropped = [c for c in node.children if not c.keep]
    kept = [c for c in node.children if c.keep]
    n_drop = sum(1 + count_all(d) for d in dropped)
    node.children = kept
    if n_drop >= min_run:
        s = Node("(collapsed)", node.item_id, "", node.created_utc, "", {})
        s.state = "collapsed"; s.collapsed_n = n_drop; s.keep = True
        node.children.append(s)
    for ch in kept:
        n_drop += collapse(ch, min_run)
    return n_drop


def coords(node, prefix="0"):
    node.coord = prefix
    for i, ch in enumerate(node.children, start=1):
        coords(ch, ("%s.%s" % (prefix, i)) if prefix != "0" else str(i))


def marks(node):
    m = node.meta
    out = []
    if m.get("distinguished"):
        out.append("[%s]" % m["distinguished"])
    if m.get("stickied"):
        out.append("[sticky@retrieval]")
    if m.get("edited") not in (None, False):
        out.append("[edited]")
    if m.get("gilded"):
        out.append("[gilded]")
    if m.get("parent_missing"):
        out.append("[parent outside the record]")
    if m.get("link_flair_text"):
        out.append("{%s}" % clip(m["link_flair_text"]))
    return (" " + " ".join(out)) if out else ""


def render(node, prefix="", last=True, out=None):
    out = [] if out is None else out
    if node.coord == "0":
        head = ("-> [%s] %s" % (" ".join(node.sequence), " | ".join(node.labels))
                if node.code_ids else "-> [na]")
        out.append("[0] OP (%s) %s%s %s" % (who(node), score(node), marks(node), head))
        child_prefix = ""
    else:
        conn = "\\-- " if last else "|-- "
        if node.state == "collapsed":
            out.append("%s%s[...] (%d un-coded items)" % (prefix, conn, node.collapsed_n))
            return out
        if node.state == "removed":
            body = "[removed by platform]"
        elif node.code_ids:
            body = "[%s] %s" % (" ".join(node.sequence), " | ".join(node.labels))
        else:
            snip = " ".join(node.body.split())[:38]
            body = '[na] "%s"' % (snip + ".." if len(node.body) > 40 else snip)
        out.append("%s%s[%s] (%s | %s) %s%s -> %s" % (prefix, conn, node.coord, who(node),
                                                     fmt_dt(node.dt_parent), score(node),
                                                     marks(node), body))
        child_prefix = prefix + ("    " if last else "|   ")
    for i, ch in enumerate(node.children):
        render(ch, child_prefix, i == len(node.children) - 1, out)
    return out


def index(node, thread_id, d):
    if node.state != "collapsed":
        d[node.coord] = {"thread_id": thread_id, "item_id": node.item_id,
                         "parent_id": node.parent_id, "author": node.author,
                         "created_utc": node.created_utc,
                         "dt_parent_sec": round(node.dt_parent, 1),
                         "dt_thread_sec": round(node.dt_thread, 1),
                         "state": node.state, "code_ids": node.code_ids,
                         "labels": node.labels, "sequence": node.sequence,
                         "coverage": node.coverage, "meta": node.meta}
    for ch in node.children:
        index(ch, thread_id, d)


def dag(node):
    return {"coord": node.coord, "item_id": node.item_id, "parent_id": node.parent_id,
            "author": node.author, "state": node.state, "collapsed_n": node.collapsed_n,
            "dt_parent_sec": round(node.dt_parent, 1), "dt_thread_sec": round(node.dt_thread, 1),
            "code_ids": node.code_ids, "labels": node.labels, "sequence": node.sequence,
            "coverage": node.coverage, "meta": node.meta,
            "children": [dag(c) for c in node.children]}


OPEN_UTC = 1490976000      # 2017-03-31 16:00:00 UTC, hour 0 of the window


def threads_from_record(path, codes):
    """A coder run's record (coder_corpus.jsonl: one item per line, posts and comments,
    [CONTEXT] items included) -> the builder's threads, for every thread that carries at
    least one code. The record's own fields are the meta."""
    by = defaultdict(list)
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if "id" not in r:
            continue
        tid = r["id"] if r.get("kind") == "post" else strip_prefix(r.get("link_id") or "?")
        by[tid].append(r)
    coded = {strip_prefix(c["thread_id"]) for c in codes if not c.get("retracted")}
    out = []
    for tid in sorted(by, key=lambda t: min(r.get("created_utc") or 0 for r in by[t])):
        if tid not in coded:
            continue
        rs = sorted(by[tid], key=lambda r: (r.get("created_utc") or 0, r.get("id") or ""))
        post = next((r for r in rs if r.get("kind") == "post"), None)
        if post is None:
            post = {"id": tid, "kind": "post", "author": "[submission outside the record]",
                    "created_utc": rs[0].get("created_utc"),
                    "title": "[submission outside the record]", "selftext": "", "synthetic": True}
        utc = post.get("created_utc") or 0
        th = {"thread_id": tid, "title": post.get("title") or "",
              "selftext": post.get("selftext") or post.get("body") or "",
              "author": post.get("author") or "[unknown]", "created_utc": utc,
              "hours_since_open": round((utc - OPEN_UTC) / 3600.0, 2), "comments": []}
        th.update(pick_meta(post))
        for r in rs:
            if r is post:
                continue
            c = {"item_id": r["id"], "parent_id": r.get("parent_id"),
                 "author": r.get("author") or "[unknown]", "created_utc": r.get("created_utc"),
                 "body": r.get("body") or r.get("selftext") or ""}
            c.update(pick_meta(r))
            th["comments"].append(c)
        out.append(th)
    return out


def from_package_thread(t):
    """A package/threads line (items with `id`, `parent_id`, `meta`) -> the builder's shape
    (a post with `comments`). A line already in the builder's shape passes through. The
    submission outside the record gets a synthetic root, as build_store.py gives it."""
    if "items" not in t or "comments" in t:
        return t
    items = t["items"]
    post = next((it for it in items if it.get("kind") == "post" or it["id"] == t["thread_id"]),
                None)
    if post is None:
        post = {"id": t["thread_id"], "kind": "post", "author": "[submission outside the record]",
                "created_utc": t.get("first_utc"), "title": "[submission outside the record]",
                "body": "", "synthetic": True}
    utc = post.get("created_utc") or t.get("first_utc") or 0
    th = {"thread_id": t["thread_id"], "title": post.get("title") or "",
          "selftext": post.get("body") or "", "author": post.get("author") or "[unknown]",
          "created_utc": utc, "hours_since_open": round((utc - OPEN_UTC) / 3600.0, 2),
          "comments": []}
    if post.get("score") is not None:
        th["score"] = post["score"]
    th.update(post.get("meta") or {})
    for it in items:
        if it is post:
            continue
        c = {"item_id": it["id"], "parent_id": it.get("parent_id"),
             "author": it.get("author") or "[unknown]", "created_utc": it.get("created_utc"),
             "body": it.get("body") or ""}
        if it.get("score") is not None:
            c["score"] = it["score"]
        c.update(it.get("meta") or {})
        th["comments"].append(c)
    return th


def run(sub, threads, codes, out_dir, min_run=3, threads_total=None, shared=True):
    """Build one community's forest. Writes trees/<sub>.md always. With shared=True
    (the default, one community at a time) it also appends to package/forest.jsonl
    and merges into package/tree_index.json. A caller building many communities
    passes shared=False and writes those two files once from what is returned:
    (path_md, dags, idx, counts)."""
    by_item = defaultdict(list)
    for c in codes:
        if c.get("retracted"):
            continue                       # a retracted code is not a code
        by_item[strip_prefix(c["item_id"])].append(c)
    md, dags, idx = [], [], {}
    tot = {"threads_given": len(threads), "threads_with_codes": 0, "items": 0, "coded": 0,
           "bridge": 0, "removed": 0, "dropped": 0, "orphans": 0,
           "na_stretches": 0, "coverage_of_coded_items": None,
           "threads_total_in_window": threads_total}
    cov = []
    for th in sorted(threads, key=lambda t: t.get("created_utc", 0)):
        root, nodes, orph, removed = build(th, by_item)
        tot["items"] += len(nodes); tot["orphans"] += orph
        if not mark(root, removed):
            tot["dropped"] += len(nodes)
            continue
        tot["threads_with_codes"] += 1
        n_drop = collapse(root, min_run)
        tot["dropped"] += n_drop
        coords(root)
        for n in nodes.values():
            if n.state in ("coded", "bridge", "removed"):
                tot[n.state] += 1
            if n.state == "coded":
                tot["na_stretches"] += n.n_na
                if n.coverage is not None:
                    cov.append(n.coverage)
        tid = strip_prefix(th["thread_id"])
        n_coded = sum(1 for n in nodes.values() if n.state == "coded")
        md.append('=== THREAD %s: "%s" (H%.2f)  items %d, coded %d, dropped %d ==='
                  % (tid, th.get("title", ""), th.get("hours_since_open", 0.0), len(nodes),
                     n_coded, n_drop))
        md += render(root); md.append("")
        d = {}; index(root, tid, d); idx[tid] = d
        dags.append({"thread_id": tid, "community": sub, "title": th.get("title", ""),
                     "hours_since_open": th.get("hours_since_open", 0.0),
                     "n_items": len(nodes), "n_coded": n_coded, "n_dropped": n_drop,
                     "retrieved_on": th.get("retrieved_on"),
                     "tree": dag(root)})
    if cov:
        tot["coverage_of_coded_items"] = round(sum(cov) / len(cov), 2)
    os.makedirs(os.path.join(out_dir, "trees"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "package"), exist_ok=True)
    header = ["# forest — %s" % sub,
              "# threads given %(threads_given)d, with at least one code %(threads_with_codes)d"
              % tot,
              "# threads in the window in all: %s" % (threads_total if threads_total is not None
                                                     else "not supplied"),
              "# items %(items)d: coded %(coded)d, bridge %(bridge)d, removed %(removed)d, "
              "dropped %(dropped)d" % tot,
              "# items whose parent falls outside the record, hung on the submission and marked: "
              "%(orphans)d" % tot,
              "# coded items: %(na_stretches)d uncoded stretches of %%d+ characters (na); mean share of "
              "text under a code %(coverage_of_coded_items)s" % tot % NA_MIN_CHARS,
              "# on a coded line, [c0012 na c0015] is the item's chunks in text order: a code id where "
              "the chunk was coded, na where a stretch was passed over; the labels follow in the same order.",
              "# coordinates are Dewey: 0 is the submission; depth is the segment count.",
              "# a dropped item carried no code and had no coded descendant.",
              "# ↑ is the item's score at retrieval and [sticky@retrieval] its sticky flag then: "
              "snapshots weeks after the event, not facts about the week. ↑? means the record "
              "holds no score.",
              "# ⟨…⟩ after an author is their flair in this community; {…} on a submission is "
              "its flair; [moderator] marks a distinguished item.", ""]
    p_md = os.path.join(out_dir, "trees", "%s.md" % sub)
    with open(p_md, "w", encoding="utf-8") as f:
        f.write("\n".join(header + md))
    if not shared:
        return p_md, dags, idx, tot
    p_ix = os.path.join(out_dir, "package", "tree_index.json")
    existing = {}
    if os.path.exists(p_ix):
        try:
            existing = json.load(open(p_ix, encoding="utf-8"))
        except Exception:
            existing = {}
    existing[sub] = {"counts": tot, "index": idx}
    with open(p_ix, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=1)
    p_dg = os.path.join(out_dir, "package", "forest.jsonl")
    keep = []
    if os.path.exists(p_dg):
        for line in open(p_dg, encoding="utf-8"):
            if line.strip() and json.loads(line).get("community") != sub:
                keep.append(line.rstrip("\n"))
    with open(p_dg, "w", encoding="utf-8") as f:
        for line in keep:
            f.write(line + "\n")
        for d in dags:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    return p_md, p_ix, p_dg, tot


def demo():
    t = [{"thread_id": "t3_a", "title": "void is at the beak", "selftext": "hold (450,120)",
          "author": "lead", "created_utc": 0, "hours_since_open": 14.2, "retrieved_on": 1492000000,
          "edited": 1200, "score": 41, "stickied": True, "link_flair_text": "Orders",
          "author_flair_text": "Grandmaster of the Order", "comments": [
              {"item_id": "c1", "parent_id": "t3_a", "author": "u1", "created_utc": 180,
               "body": "what colour are we using?", "score": 0},
              {"item_id": "c2", "parent_id": "t1_c1", "author": "u2", "created_utc": 360,
               "body": "script link here", "score": -3, "author_flair_text": "Knight"},
              {"item_id": "c3", "parent_id": "c2", "author": "u3", "created_utc": 840,
               "body": "bot is up on the perimeter"},
              {"item_id": "c4", "parent_id": "c1", "author": "u4", "created_utc": 400,
               "body": "second reply to the same parent"},
              {"item_id": "c5", "parent_id": "t3_a", "author": "u5", "created_utc": 300,
               "body": "scripts will get us banned"},
              {"item_id": "c6", "parent_id": "c5", "author": "u6", "created_utc": 720,
               "body": "taking this to discord"},
              {"item_id": "c7", "parent_id": "c6", "author": "mod", "created_utc": 1000,
               "body": "This post was removed because you have a new account", "distinguished": "moderator"},
              {"item_id": "c8", "parent_id": "t3_a", "author": "u8", "created_utc": 420, "body": "rip duck"},
              {"item_id": "c9", "parent_id": "c8", "author": "u9", "created_utc": 500, "body": "F"},
              {"item_id": "c10", "parent_id": "t3_a", "author": "u10", "created_utc": 430, "body": "placed"},
              {"item_id": "c11", "parent_id": "t3_a", "author": "u11", "created_utc": 440, "body": "done"}]}]
    c = [{"code_id": "C01", "item_id": "t3_a", "label": "sounding the alarm on the void"},
         {"code_id": "C04", "item_id": "c2", "label": "handing round the overlay script"},
         {"code_id": "C07", "item_id": "c3", "label": "confirming the bot is on the perimeter"},
         {"code_id": "C05", "item_id": "c5", "label": "warning the script risks a ban"},
         {"code_id": "C08", "item_id": "c6", "label": "moving the argument to discord"}]
    out = os.path.join(tempfile.gettempdir(), "forest_demo")
    for p in ("package/forest.jsonl", "package/tree_index.json"):
        fp = os.path.join(out, p)
        if os.path.exists(fp):
            os.remove(fp)
    p_md, p_ix, p_dg, tot = run("demo", t, c, out, threads_total=1)
    print(open(p_md, encoding="utf-8").read())
    print("counts:", json.dumps(tot))
    ix = json.load(open(p_ix, encoding="utf-8"))["demo"]["index"]["a"]
    print("coord 1.1 ->", json.dumps(ix.get("1.1")))
    print("coord 2.1.1 ->", json.dumps(ix.get("2.1.1")))
    assert ix["1.1"]["item_id"] == "c2" and ix["1.1.1"]["item_id"] == "c3", "coordinate bug"
    assert ix["2.1.1"]["state"] == "removed", "removal state bug"
    assert ix["1.1"]["meta"]["score"] == -3 and ix["1"]["meta"]["score"] == 0, "score lost"
    md = open(p_md, encoding="utf-8").read()
    assert "[0] OP (lead ⟨Grandmaster of the Order⟩) ↑41 [sticky@retrieval] [edited] {Orders}" in md, "OP line"
    assert "[1.1] (u2 ⟨Knight⟩ | +3.0m) ↑-3 -> [C04]" in md and "[1] (u1 | +3.0m) ↑0 -> [na]" in md, "comment line"
    assert "(u3 | +8.0m) ↑? -> [C07]" in md, "unknown score"
    print("assertions passed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sub"); ap.add_argument("--threads-file"); ap.add_argument("--codes-file")
    ap.add_argument("--record", help="a coder run's coder_corpus.jsonl; the forest is built "
                                     "for every thread the codes file touches")
    ap.add_argument("--out-dir", default="."); ap.add_argument("--min-collapse", type=int, default=3)
    ap.add_argument("--threads-total", type=int, default=None,
                    help="threads in the window in all, coded or not, for the header; "
                         "read from corpus_manifest.json beside --record when absent")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        demo()
    elif not (a.sub and a.codes_file and (a.threads_file or a.record)):
        ap.print_usage()
        sys.exit("tree_builder: --sub, --codes-file and one of --record/--threads-file are "
                 "required (--demo runs the self-check instead)")
    else:
        cd = [c for c in (json.loads(l) for l in open(a.codes_file, encoding="utf-8") if l.strip())
              if c.get("sub") in (None, a.sub)]
        total = a.threads_total
        if a.record:
            th = threads_from_record(a.record, cd)
            cm = os.path.join(os.path.dirname(os.path.abspath(a.record)), "corpus_manifest.json")
            if total is None and os.path.exists(cm):
                total = json.load(open(cm, encoding="utf-8")).get("threads_with_inwindow_items")
        else:
            th = [from_package_thread(json.loads(l)) for l in open(a.threads_file, encoding="utf-8") if l.strip()]
        p = run(a.sub, th, cd, a.out_dir, a.min_collapse, total)
        print(json.dumps(p[3]))
