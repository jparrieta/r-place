#!/usr/bin/env python3
"""C1 section 7, the form pass, read-only: patterns over the participants' quoted words.

Every count goes through `mem.py codes --grep <re> --json` (one logged read per pattern, no limit on the count).
mem.py matches the words, the coder's label and the coder's note, case-insensitively; this helper reports that count
and then keeps the concepts whose quoted words (`text`) match, the count the form pass reads. Placements are joined
from assignments_final.jsonl by (sub, theme_id): a concept's line theme is the first theme of its line; it is cited
when a placed theme's support lists it. Depth is the forest coordinate's segment count (0 the submission, 1 a
top-level comment, 2 or more a reply). A coded reply is a coded concept by another author, in the same thread, whose
coordinate lies below the concept's item; replies the coders dropped (no code, no coded descendant) are not seen.

    python3 out/_analysis/c1_form_pass.py count --re RE [--show K] [--seed S] [--parents]
    python3 out/_analysis/c1_form_pass.py sweep form|register|unsaid [--show K]   every pattern of that sweep in
                                                                    c1_form_patterns.json, one mem.py read each
    python3 out/_analysis/c1_form_pass.py shape [--top K]            the form of every concept (one read, re ".")
    python3 out/_analysis/c1_form_pass.py questions [--re RE] [--top K] [--show K]
                                                                     question concepts (words hold "?"), answered or
                                                                     not by a coded reply; --re narrows them
"""
import argparse, collections, json, os, random, re, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ROOT = os.path.dirname(OUT)


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def fetch(rx):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", rx, "--json",
                        "--limit", "10000000"], cwd=ROOT, capture_output=True, text=True)
    rows = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
    if p.returncode or not p.stdout.strip():
        sys.exit("mem.py refused /%s/: %s" % (rx, (p.stdout + p.stderr).strip()[-400:]))
    return rows


LINES = {}
NAMES = {}


def placements():
    if not LINES:
        for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
            LINES[(r["sub"], r["theme_id"])] = r
        for t in jl(os.path.join(OUT, "scheme_v2.jsonl")):
            NAMES[t["id"]] = t["name"]
    return LINES


def owner(c):
    r = placements().get((c["sub"], c["theme_id"])) or {}
    th = r.get("third_order") or []
    cited = [t for t in th if c["code_id"] in ((r.get("support_by_theme") or {}).get(t) or [])]
    return (th[0] if th else "EMPTY"), cited


def depth(c):
    k = str(c.get("coord") or "")
    if k in ("", "-", "None"):
        return None
    return 0 if k == "0" else len(k.split("."))


def words(c):
    return len(str(c.get("text") or "").split())


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s?!+<3]", "", t.lower())).strip()


def pct(a, b):
    return "%.1f%%" % (100.0 * a / b) if b else "-"


def quart(xs):
    if not xs:
        return "-"
    xs = sorted(xs)
    q = lambda f: xs[min(len(xs) - 1, int(f * len(xs)))]
    return "%s/%s/%s" % (q(0.25), q(0.5), q(0.75))


def tree(rows):
    by = collections.defaultdict(list)
    for c in rows:
        by[(c["sub"], c.get("thread_id"))].append(c)
    return by


def answered(c, by):
    k = str(c.get("coord") or "")
    if k in ("", "-", "None"):
        return None
    pre = "" if k == "0" else k + "."
    for d in by.get((c["sub"], c.get("thread_id")), []):
        dk = str(d.get("coord") or "")
        if d is c or d.get("author") == c.get("author") or dk == k:
            continue
        if (k == "0" and dk != "0") or (pre and dk.startswith(pre)):
            return True
    return False


def parent_items(c, by):
    k = str(c.get("coord") or "")
    if k in ("", "-", "None", "0"):
        return None
    pk = "0" if "." not in k else k.rsplit(".", 1)[0]
    return [d for d in by.get((c["sub"], c.get("thread_id")), []) if str(d.get("coord") or "") == pk]


def describe(name, rx, rows, show=0, seed=9, parents=False, by=None, trx=None):
    allm = len(rows)
    allrooms = len(set(c["sub"] for c in rows))
    crx = re.compile(trx or rx, re.I)
    tx = [c for c in rows if crx.search(str(c.get("text") or ""))]
    rooms = collections.Counter(c["sub"] for c in tx)
    L = ["## %s  /%s/%s" % (name, rx, "  words: /%s/" % trx if trx else ""),
         "mem.py codes --grep: %d concepts in %d rooms; in the quoted words: %d concepts in %d rooms" % (
             allm, allrooms, len(tx), len(rooms))]
    if not tx:
        return L
    dp = collections.Counter(depth(c) for c in tx)
    L.append("depth: submission %d, top-level %d, reply %d, unknown %d; item kinds %s" % (
        dp.get(0, 0), dp.get(1, 0), sum(v for k, v in dp.items() if k and k >= 2), dp.get(None, 0),
        json.dumps(dict(collections.Counter(c.get("item_kind") for c in tx).most_common()))))
    L.append("words per concept (q1/median/q3) %s; hour (q1/median/q3) %s; rooms with 3 or more: %d; top rooms %s" % (
        quart([words(c) for c in tx]), quart([round(c["hour"]) for c in tx if c.get("hour") is not None]),
        sum(1 for v in rooms.values() if v >= 3), ", ".join("%s %d" % kv for kv in rooms.most_common(6))))
    own = collections.Counter()
    cited = 0
    for c in tx:
        o, ci = owner(c)
        own[o] += 1
        cited += bool(ci)
    L.append("line themes: %d distinct; top %s; empty lines %d; concepts cited as a placed theme's support %d (%s)" % (
        len(own) - (1 if "EMPTY" in own else 0),
        "; ".join("%s %s %d (%s)" % (t, NAMES.get(t, "")[:34], n, pct(n, len(tx))) for t, n in own.most_common(5)
                  if t != "EMPTY"), own.get("EMPTY", 0), cited, pct(cited, len(tx))))
    if parents and by is not None:
        po = collections.Counter()
        seen = coded = 0
        for c in tx:
            ps = parent_items(c, by)
            if ps is None:
                continue
            seen += 1
            if ps:
                coded += 1
                po[owner(ps[0])[0]] += 1
        L.append("replies and comments %d; parent item coded %d (%s); parents' line themes: %s" % (
            seen, coded, pct(coded, seen), "; ".join("%s %s %d" % (t, NAMES.get(t, "")[:30], n)
                                                     for t, n in po.most_common(6))))
        known = [c for c in tx if depth(c) is not None]
        ans = sum(1 for c in known if answered(c, by))
        L.append("with a coded reply by another author below them: %d of %d (%s)" % (ans, len(known), pct(ans, len(known))))
    if show:
        rnd = random.Random(seed)
        pick = rnd.sample(tx, min(show, len(tx)))
        for c in sorted(pick, key=lambda c: (c["sub"].lower(), c["code_id"])):
            L.append("  %s/%s %s d%s h%s | %s" % (c["sub"], c["code_id"], c["theme_id"], depth(c),
                                                 "%.0f" % c["hour"] if c.get("hour") is not None else "?",
                                                 " ".join(str(c.get("text") or "").split())[:240]))
    return L


def shape(a):
    rows = fetch(".")
    placements()
    n = len(rows)
    print("concepts read: %d in %d rooms (mem.py codes --grep '.')" % (n, len(set(c["sub"] for c in rows))))
    bins = [(1, 1), (2, 2), (3, 3), (4, 5), (6, 10), (11, 20), (21, 50), (51, 10 ** 9)]
    w = [words(c) for c in rows]
    print("words per concept: " + "; ".join("%s %d (%s)" % ("%d" % lo if lo == hi else "%d-%s" % (lo, hi if hi < 10 ** 9 else "up"),
                                                         sum(1 for x in w if lo <= x <= hi),
                                                         pct(sum(1 for x in w if lo <= x <= hi), n)) for lo, hi in bins))
    dp = collections.Counter(depth(c) for c in rows)
    print("depth: " + "; ".join("%s %d (%s)" % (k, v, pct(v, n)) for k, v in sorted(dp.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))[:12]))
    for d in (0, 1, 2, 3):
        ws = [words(c) for c in rows if (depth(c) or 0) == d if depth(c) is not None]
        print("  depth %d: words q1/median/q3 %s" % (d, quart(ws)))
    print("item kinds: " + json.dumps(dict(collections.Counter(c.get("item_kind") for c in rows).most_common())))
    hb = collections.Counter(min(8, int(c["hour"] // 12)) if c.get("hour") is not None and c["hour"] >= 0 else -1 for c in rows)
    print("hour, 12-hour bins (-1 before open, 8 = 96 and after): " + "; ".join("%d %d" % kv for kv in sorted(hb.items())))
    short = [c for c in rows if words(c) <= 3]
    sr = collections.Counter(c["sub"] for c in short)
    print("\nconcepts of three words or fewer: %d (%s) in %d rooms" % (len(short), pct(len(short), n), len(sr)))
    sd = collections.Counter(depth(c) for c in short)
    print("  depth: submission %d, top-level %d, reply %d" % (sd.get(0, 0), sd.get(1, 0), sum(v for k, v in sd.items() if k and k >= 2)))
    own = collections.Counter(owner(c)[0] for c in short)
    allown = collections.Counter(owner(c)[0] for c in rows)
    print("  line themes, short concepts against all concepts (share of short, share of all):")
    for t, k in own.most_common(a.top):
        print("    %s %-40s %5d %6s  %6s" % (t, NAMES.get(t, "")[:40], k, pct(k, len(short)), pct(allown[t], n)))
    tc = collections.Counter(norm(str(c.get("text") or "")) for c in short)
    trooms = collections.defaultdict(set)
    for c in short:
        trooms[norm(str(c.get("text") or ""))].add(c["sub"])
    print("  the most frequent short texts (lowercased, punctuation dropped): text, concepts, rooms")
    print("    " + "; ".join("'%s' %d/%d" % (t, k, len(trooms[t])) for t, k in tc.most_common(a.top * 3)))
    by = tree(rows)
    for lo, hi, lab in ((1, 3, "1-3 words"), (4, 10, "4-10 words"), (11, 10 ** 9, "11 words and more")):
        sel = [c for c in rows if lo <= words(c) <= hi and depth(c) is not None]
        ans = sum(1 for c in sel if answered(c, by))
        print("  %s: %d concepts; with a coded reply by another author below them %d (%s)" % (lab, len(sel), ans, pct(ans, len(sel))))


def questions(a):
    rows = fetch(".")
    placements()
    by = tree(rows)
    if a.re:
        crx = re.compile(a.text or a.re, re.I)
        q = [c for c in fetch(a.re) if "?" in str(c.get("text") or "") and crx.search(str(c.get("text") or ""))]
        ids = set((c["sub"], c["code_id"]) for c in q)
        q = [c for c in rows if (c["sub"], c["code_id"]) in ids]
    else:
        q = [c for c in rows if "?" in str(c.get("text") or "")]
    q = [c for c in q if depth(c) is not None]
    ans = [c for c in q if answered(c, by)]
    un = [c for c in q if not answered(c, by)]
    print("question concepts (quoted words hold '?')%s: %d in %d rooms; answered by a coded reply %d (%s); not %d (%s)" % (
        " matching /%s/" % a.re if a.re else "", len(q), len(set(c["sub"] for c in q)), len(ans), pct(len(ans), len(q)),
        len(un), pct(len(un), len(q))))
    for lab, sel in (("answered", ans), ("not answered", un)):
        dp = collections.Counter(depth(c) for c in sel)
        own = collections.Counter(owner(c)[0] for c in sel)
        print("  %s: depth submission %d, top-level %d, reply %d; words median %s; rooms %d; line themes %s" % (
            lab, dp.get(0, 0), dp.get(1, 0), sum(v for k, v in dp.items() if k and k >= 2),
            quart([words(c) for c in sel]).split("/")[1] if sel else "-", len(set(c["sub"] for c in sel)),
            "; ".join("%s %s %d" % (t, NAMES.get(t, "")[:30], n) for t, n in own.most_common(a.top))))
    for d in (0, 1, 2):
        s = [c for c in q if (depth(c) if depth(c) < 2 else 2) == d]
        k = sum(1 for c in s if answered(c, by))
        print("  at depth %s: %d questions in %d rooms, answered %d (%s); not answered in %d rooms" % (
            {0: "0 (submission)", 1: "1 (top-level)", 2: "2+ (reply)"}[d], len(s), len(set(c["sub"] for c in s)), k,
            pct(k, len(s)), len(set(c["sub"] for c in s if not answered(c, by)))))
    if a.show:
        rnd = random.Random(a.seed)
        for c in sorted(rnd.sample(un, min(a.show, len(un))), key=lambda c: (c["sub"].lower(), c["code_id"])):
            print("  un %s/%s %s d%s | %s" % (c["sub"], c["code_id"], c["theme_id"], depth(c), " ".join(str(c.get("text") or "").split())[:240]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["count", "sweep", "shape", "questions"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--re", default="")
    ap.add_argument("--text", default="", help="a stricter pattern for the quoted words alone (anchors work here)")
    ap.add_argument("--name", default="")
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--seed", type=int, default=9)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--parents", action="store_true")
    a = ap.parse_args()
    if a.mode == "shape":
        return shape(a)
    if a.mode == "questions":
        return questions(a)
    placements()
    by = tree(fetch(".")) if a.parents else None
    if a.mode == "count":
        print("\n".join(describe(a.name or "pattern", a.re, fetch(a.re), a.show, a.seed, a.parents, by, a.text)))
        return
    pats = json.load(open(os.path.join(HERE, "c1_form_patterns.json"), encoding="utf-8"))
    if a.arg not in pats:
        sys.exit("no sweep %s in c1_form_patterns.json: %s" % (a.arg, ", ".join(k for k in pats if not k.startswith("_"))))
    for p in pats[a.arg]:
        print("\n".join(describe(p["name"], p["re"], fetch(p["re"]), a.show, a.seed, a.parents, by, p.get("text"))))
        print()


if __name__ == "__main__":
    main()
