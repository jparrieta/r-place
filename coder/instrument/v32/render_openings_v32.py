#!/usr/bin/env python3
"""render_openings_v32.py — the openings file the case lead reads before anything else.

One block per thread of the record, in time order of the thread's opening post: a metadata line,
a line of counts over the whole thread, the title, and the opening post's text cut at 500
words. It is the room's table of contents with the shape of every thread beside its title, so
that a lead who never reads the raw threads still knows what was posted when and how big each
thread grew. It is orientation, not material: the lead's contract says what may and may not be
done with it.

    python3 render_openings_v32.py coder_corpus.jsonl <sub> [--out-dir DIR]

writes openings.md and, when the record holds more than TITLES_ABOVE threads, also
openings_titles.md (the metadata and counts lines and the title, no text) and
openings_digest.md (counts per hour, every stickied or moderator-distinguished post, the ten
highest-scored titles per hour). The counts per thread:

  comments      replies in the window / replies in the thread (context items included)
  branches      top-level replies, i.e. direct replies to the opening post: the branches of
                the thread's tree at its root
  depth         the longest reply chain, the opening post at depth 0
  authors       distinct accounts in the thread, [deleted] not counted
  score (all)   the sum of `score` over the opening post and every reply the record carries a
                score for, with the count of items whose score the record lacks

`score` is the net vote as of retrieval, weeks after the event: a snapshot, not a fact about
the week. So is `stickied`. `distinguished` is reliable.
"""
import argparse, collections, datetime, json, os, sys

OPEN = 1490976000
END = OPEN + 97 * 3600
TITLES_ABOVE = 1500
OP_WORDS = 500


def thread_of(r):
    if r.get("kind") == "post":
        return r["id"]
    li = r.get("link_id") or ""
    return li[3:] if li.startswith("t3_") else (li or "?")


def strip_prefix(x):
    if isinstance(x, str) and len(x) > 3 and x[0] == "t" and x[1].isdigit() and x[2] == "_":
        return x[3:]
    return x


def hour(t):
    return (t - OPEN) / 3600.0


def clock(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%m-%d %H:%M")


def clip(s, n=28):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + "…"


def load(record):
    items = []
    import gzip
    opener = gzip.open if record.endswith(".gz") else open
    with opener(record, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if "id" in r:
                items.append(r)
    return items


def measure(items):
    """per thread: the opening post and the counts."""
    by = collections.defaultdict(list)
    for r in items:
        by[thread_of(r)].append(r)
    out = []
    for tid, rs in by.items():
        post = next((r for r in rs if r.get("kind") == "post"), None)
        comments = [r for r in rs if r.get("kind") != "post"]
        n_win = sum(1 for r in comments if OPEN <= (r.get("created_utc") or 0) <= END)
        branches = sum(1 for r in comments if strip_prefix(r.get("parent_id") or "") == tid)
        # depth: parent chains
        parent = {r["id"]: strip_prefix(r.get("parent_id") or "") for r in comments}
        depth_of = {}
        for r in comments:
            chain = []
            i = r["id"]
            while i in parent and i not in depth_of and i not in chain:
                chain.append(i)
                p = parent[i]
                if p == tid or p not in parent:
                    break
                i = p
            # the last of the chain hangs on the root or on a known depth
            base = depth_of.get(parent.get(chain[-1]), 0) if chain else 0
            for k, cid in enumerate(reversed(chain)):
                depth_of[cid] = base + k + 1
        maxdepth = max(depth_of.values(), default=0)
        authors = {r.get("author") for r in rs if r.get("author") and r.get("author") not in ("[deleted]", "[removed]")}
        scored = [r.get("score") for r in rs if isinstance(r.get("score"), (int, float)) and not isinstance(r.get("score"), bool)]
        opened = post.get("created_utc") if post else min(r.get("created_utc") or 0 for r in rs)
        out.append({"thread_id": tid, "post": post, "opened_utc": opened,
                    "n_comments_window": n_win, "n_comments": len(comments),
                    "branches": branches, "depth": maxdepth, "authors": len(authors),
                    "score_sum": int(sum(scored)), "unscored": len(rs) - len(scored),
                    "in_window": OPEN <= (opened or 0) <= END})
    out.sort(key=lambda t: (t["opened_utc"] or 0, t["thread_id"]))
    return out


def head_line(t):
    p = t["post"] or {}
    op = t["opened_utc"] or 0
    who = p.get("author") or "[submission outside the record]"
    fl = p.get("author_flair_text")
    if fl:
        who += " ⟨%s⟩" % clip(fl)
    marks = []
    if p.get("link_flair_text"):
        marks.append("{%s}" % clip(p["link_flair_text"]))
    if p.get("stickied"):
        marks.append("[sticky@retrieval]")
    if p.get("distinguished"):
        marks.append("[moderator]" if p["distinguished"] == "moderator" else "[%s]" % p["distinguished"])
    if p.get("edited"):
        marks.append("[edited]")
    if p.get("gilded"):
        marks.append("[gilded]")
    ctx = "" if t["in_window"] else "  [opened outside the window]"
    return "=== %s  H%+.2f  %s  by %s  %s%s" % (t["thread_id"], hour(op), clock(op), who, " ".join(marks), ctx)


def counts_line(t):
    p = t["post"] or {}
    sc = p.get("score")
    ops = "↑%d" % sc if isinstance(sc, (int, float)) and not isinstance(sc, bool) else "↑?"
    uns = ", %d unscored" % t["unscored"] if t["unscored"] else ""
    return ("    OP %s | comments %d in window (%d in thread) | branches %d | depth %d | authors %d | "
            "↑ all items %d%s" % (ops, t["n_comments_window"], t["n_comments"], t["branches"],
                                  t["depth"], t["authors"], t["score_sum"], uns))


def op_text(t):
    p = t["post"] or {}
    title = (p.get("title") or "[no title in the record]").strip()
    s = (p.get("selftext") or "").strip()
    if not s:
        url = p.get("url") or p.get("domain")
        body = "(link post, no text%s)" % (": " + str(url) if url else "")
    else:
        words = s.split()
        body = " ".join(words[:OP_WORDS])
        if len(words) > OP_WORDS:
            body += " […%d more words]" % (len(words) - OP_WORDS)
    return title, body


def render(record, sub):
    items = load(record)
    threads = measure(items)
    n_win = sum(1 for t in threads if t["in_window"])
    header = ["# r/%s — openings" % sub,
              "# %d threads, %d opened inside the window; in time order of the opening post."
              % (len(threads), n_win),
              "# Each block: the thread's id, hour since the canvas opened, clock (UTC), author with flair,",
              "# the submission's flair and marks; then counts over the whole thread (comments in the window",
              "# and in all, branches = direct replies to the opening post, depth = the longest reply chain,",
              "# distinct authors, the sum of scores over every item the record scores); then the title",
              "# and the opening post's text cut at %d words." % OP_WORDS,
              "# score and stickied are snapshots at retrieval, weeks after the event, not facts about the week.",
              "# This file is orientation. Code nothing from it; cite titles only; see CONTRACT-case-lead.md.",
              ""]
    full, titles = list(header), list(header)
    for t in threads:
        title, body = op_text(t)
        h, c = head_line(t), counts_line(t)
        full += [h, c, "    " + title, "    " + body.replace("\n", "\n    "), ""]
        titles += [h, c, "    " + title, ""]
    # digest
    per_hour = collections.defaultdict(list)
    for t in threads:
        if t["in_window"]:
            per_hour[int(hour(t["opened_utc"]))].append(t)
    digest = ["# r/%s — openings digest" % sub,
              "# %d threads opened in the window. Per hour: how many, then the ten with the highest OP score." % n_win,
              "# Then every stickied or moderator-distinguished post in the record.", ""]
    for hh in range(0, 98):
        ts = per_hour.get(hh, [])
        if not ts:
            continue
        digest.append("## H+%d  (%d threads, %d comments in window)" % (hh, len(ts), sum(t["n_comments_window"] for t in ts)))
        top = sorted(ts, key=lambda t: -((t["post"] or {}).get("score") or 0))[:10]
        for t in top:
            p = t["post"] or {}
            digest.append("- %s ↑%s c%d b%d  %s" % (t["thread_id"], p.get("score", "?"), t["n_comments_window"],
                                                    t["branches"], clip(op_text(t)[0], 110)))
        digest.append("")
    digest.append("## stickied or moderator-distinguished posts")
    n_sm = 0
    for t in threads:
        p = t["post"] or {}
        if p.get("stickied") or p.get("distinguished"):
            n_sm += 1
            digest.append("- %s  H%+.2f  %s  %s  %s" % (t["thread_id"], hour(t["opened_utc"] or 0),
                                                    "[sticky]" if p.get("stickied") else "",
                                                    "[%s]" % p["distinguished"] if p.get("distinguished") else "",
                                                    clip(op_text(t)[0], 110)))
    if not n_sm:
        digest.append("- none in the record")
    stats = {"threads": len(threads), "threads_in_window": n_win,
             "chars_full": sum(len(x) + 1 for x in full), "chars_titles": sum(len(x) + 1 for x in titles),
             "chars_digest": sum(len(x) + 1 for x in digest),
             "stickied_or_moderator_posts": n_sm}
    return "\n".join(full) + "\n", "\n".join(titles) + "\n", "\n".join(digest) + "\n", stats


def write(record, sub, out_dir):
    full, titles, digest, stats = render(record, sub)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "openings.md"), "w", encoding="utf-8").write(full)
    stats["files"] = ["openings.md"]
    if stats["threads"] > TITLES_ABOVE:
        open(os.path.join(out_dir, "openings_titles.md"), "w", encoding="utf-8").write(titles)
        open(os.path.join(out_dir, "openings_digest.md"), "w", encoding="utf-8").write(digest)
        stats["files"] += ["openings_titles.md", "openings_digest.md"]
    return stats


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("record")
    ap.add_argument("sub")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    print(json.dumps(write(a.record, a.sub, a.out_dir), indent=1))
