#!/usr/bin/env python3
"""C2 section 4, read-only: the evidence for candidate arrows between elements of c2_elements_p1.json.

An element stands for the concepts cited under its third-order themes (`support_by_theme` on assignments_final.jsonl
lines). The connection statement, written before any count: "in a room carrying both elements, the first concept of
FROM comes before the first concept of TO" (the forest's hours since open). Per arrow the helper reports:
- rooms carrying both, and the share where the statement holds;
- the null: in each such room the FROM and TO labels are permuted over the room's pooled concepts (counts kept),
  500 times (seed 20261014); the null share's mean and 95th percentile (base rate beaten when observed > p95);
- the onset contrast: the statement's hold count among early-side and late-side rooms (contrast.md);
- rooms with FROM only and TO only;
- transitions: a TO concept on an item that replies, at any depth, to the item of a FROM concept in the same thread,
  by another author, later in time; the shortest interval per room first;
- sampled rooms: a seeded draw of rooms carrying both outside --subs, each with its two first hours and holds|fails.
The concepts are read once through `mem.py codes --grep . --json` (one logged read).

    python3 out/_analysis/c2_arrow_evidence.py P01:P03 P02:P04 ... [--subs a,b] [--show 5] [--sample 4] [--mode after]

--mode after uses a second connection statement, also written before any count: "in a room carrying both, some
concept of TO comes after the first concept of FROM" (for a return or a sequel, where TO may also come earlier);
the null permutes labels the same way.
"""
import argparse, collections, json, os, random, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ap = argparse.ArgumentParser()
ap.add_argument("pairs", nargs="+")
ap.add_argument("--subs", default="")
ap.add_argument("--show", type=int, default=5)
ap.add_argument("--sample", type=int, default=4)
ap.add_argument("--perm", type=int, default=500)
ap.add_argument("--mode", default="first", choices=["first", "after"])
ap.add_argument("--elements", default="c2_elements_p1.json", help="element file in out/_analysis (pass 2: c2_elements_p2.json)")
ap.add_argument("--before", type=float, default=None,
                help="pass 4: count only concepts placed before this hour (both ends), e.g. 73 for while the canvas runs")
ap.add_argument("--drop", default="",
                help="pass 4: a file in out/_analysis listing sub:code concepts to leave out of every element (one a line)")
a = ap.parse_args()
DROP = set()
if a.drop:
    DROP = set(l.strip() for l in open(os.path.join(OUT, "_analysis", a.drop), encoding="utf-8") if l.strip())


def stat(hf, ht):
    """The connection statement on two lists of hours: first-first order, or some TO after the first FROM."""
    if a.mode == "after":
        return max(ht) > min(hf)
    return min(hf) < min(ht)

els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", a.elements), encoding="utf-8"))["elements"])
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
rows = jl("assignments_final.jsonl")
contrast = open(os.path.join(OUT, "contrast.md"), encoding="utf-8").read()
early = set(x.strip() for x in contrast.split("## Members, early side (131)")[1].split("##")[0].replace("\n", " ").split(",") if x.strip())
early.add("italy")
late = set(x.strip() for x in contrast.split("## Members, late side (61)")[1].split("##")[0].replace("\n", " ").split(",") if x.strip())
subs = set(x for x in a.subs.split(",") if x)


def cited(el):
    out = collections.defaultdict(set)
    for r in rows:
        for t, ids in (r.get("support_by_theme") or {}).items():
            if t in el["themes"]:
                keep = [i for i in ids if "%s:%s" % (r["sub"], i) not in DROP]
                if a.before is not None:
                    keep = [i for i in keep if (r["sub"], i) in codes and codes[(r["sub"], i)].get("hour") is not None
                            and codes[(r["sub"], i)]["hour"] < a.before]
                if keep:
                    out[r["sub"]].update(keep)
    return out


def hours(sub, ids):
    return [codes[(sub, i)]["hour"] for i in ids if (sub, i) in codes and codes[(sub, i)].get("hour") is not None]


def one(frm, to):
    F, T = els[frm], els[to]
    if not F["themes"] or not T["themes"]:
        print("%s -> %s: an element with no themes (a form-pass finding) is never counted" % (frm, to))
        return
    side = {"F": cited(F), "T": cited(T)}
    first, holds = {}, set()
    for s in sorted(set(side["F"]) & set(side["T"])):
        hf, ht = hours(s, side["F"][s]), hours(s, side["T"][s])
        if hf and ht:
            first[s] = (min(hf), min(ht))
            if stat(hf, ht):
                holds.add(s)
    both = sorted(first)
    obs = len(holds) / float(len(both)) if both else 0.0
    rnd = random.Random(20261014)
    pooled = dict((s, (hours(s, side["F"][s]) + hours(s, side["T"][s]), len(hours(s, side["F"][s])))) for s in both)
    null = []
    for _ in range(a.perm):
        k = 0
        for s in both:
            hs, nf = pooled[s]
            idx = list(range(len(hs)))
            rnd.shuffle(idx)
            k += stat([hs[i] for i in idx[:nf]], [hs[i] for i in idx[nf:]])
        null.append(k / float(len(both)) if both else 0.0)
    null.sort()
    mean = sum(null) / len(null) if null else 0.0
    p95 = null[int(0.95 * len(null)) - 1] if null else 0.0
    eb, lb = [s for s in both if s in early], [s for s in both if s in late]
    print("\n== %s -> %s, statement %s (%s -> %s)" % (frm, to, a.mode, F["statement"][:60], T["statement"][:60]))
    print("rooms carrying %s %d, %s %d, both %d; holds in %d (%.3f); null mean %.3f, p95 %.3f; base rate beaten: %s"
          % (frm, len(side["F"]), to, len(side["T"]), len(both), len(holds), obs, mean, p95, obs > p95))
    print("early side: holds %d of %d; late side: holds %d of %d" % (
        sum(1 for s in eb if s in holds), len(eb), sum(1 for s in lb if s in holds), len(lb)))
    print("rooms with %s only %d; with %s only %d" % (frm, len(set(side["F"]) - set(side["T"])), to,
                                                  len(set(side["T"]) - set(side["F"]))))
    bythread = collections.defaultdict(list)
    for s in both:
        for k in ("F", "T"):
            for i in side[k][s]:
                c = codes.get((s, i))
                if c and c.get("thread_id") and c.get("coord") not in (None, "", "-"):
                    bythread[(s, c["thread_id"])].append((k, c))
    inst = []
    for (s, th), cs in bythread.items():
        fs = [c for k, c in cs if k == "F"]
        ts = [c for k, c in cs if k == "T"]
        for f in fs:
            fc = str(f["coord"])
            for t in ts:
                tc = str(t["coord"])
                below = (fc == "0" and tc != "0") or (fc != "0" and tc.startswith(fc + "."))
                if below and t.get("author") != f.get("author") and t["hour"] > f["hour"]:
                    inst.append((round((t["hour"] - f["hour"]) * 60), s, th, f, t))
    inst.sort(key=lambda x: x[0])
    print("transitions: %d in %d rooms" % (len(inst), len(set(x[1] for x in inst))))
    seen = set()
    for m, s, th, f, t in inst:
        if s in seen:
            continue
        seen.add(s)
        print("  %s thread %s: %s %s (%s, h%.2f) -> %s %s (%s, h%.2f), %d min | %s || %s" % (
            s, th, f["code_id"], f["item_id"], f["coord"], f["hour"], t["code_id"], t["item_id"], t["coord"], t["hour"], m,
            " ".join(str(f.get("text") or "").split())[:100], " ".join(str(t.get("text") or "").split())[:100]))
        if len(seen) >= a.show:
            break
    pool = [s for s in both if s not in subs]
    rs = random.Random(20261014)
    for s in rs.sample(pool, min(a.sample, len(pool))):
        print("  sampled %s: first %s h%.2f, first %s h%.2f: %s" % (s, frm, first[s][0], to, first[s][1],
                                                                "holds" if s in holds else "fails"))


for pr in a.pairs:
    f, t = pr.split(":")
    one(f, t)
