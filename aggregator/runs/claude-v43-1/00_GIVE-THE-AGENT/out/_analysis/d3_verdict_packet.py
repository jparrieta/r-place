#!/usr/bin/env python3
"""D3a-56: one page of split rooms for the verdict rulings (G60). For each room, in the order of
_analysis/d2_verdict_rooms.json's split list (pair, then room): the room's figures against prior.md section 8
(concepts, themes, off-platform pointers; the floor and the threshold flagged), both readers' lines whole
(verdict, cannot_tell_under, sentence, and each named theme or concept with its label), and the room's D3 rulings
on its propose, add-step, add-condition and link lines (the last ruling per line; for propose lines the spec class
of D3a-55). No canvas measure is printed (rule 7). Writes the page to --out.

    python3 out/_analysis/d3_verdict_packet.py --offset 0 --limit 20 --out out/_analysis/d3_vp_000.txt
"""
import argparse, collections, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--offset", type=int, required=True)
ap.add_argument("--limit", type=int, required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


split = json.load(open(os.path.join(OUT, "_analysis", "d2_verdict_rooms.json")))["split"]
order = sorted(split, key=lambda r: (r["pair"], r["sub"].lower()))
page = order[a.offset:a.offset + a.limit]
want = {r["sub"] for r in page}
rooms = {r["sub"]: r for r in jl(os.path.join(ST, "rooms.jsonl")) if r["sub"] in want}
tl, cl = {}, {}
for r in jl(os.path.join(ST, "themes.jsonl")):
    if r["sub"] in want:
        tl[(r["sub"], r["theme_id"])] = r.get("second_order")
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    if r["sub"] in want:
        cl[(r["sub"], r["code_id"])] = (r.get("first_order"), r.get("hour"))
place = {}
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    if r.get("sub") in want:
        place[(r["sub"], r.get("theme_id"))] = ",".join(r.get("third_order") or []) or "nowhere"
verd = {r["sub"]: r for r in jl(os.path.join(OUT, "verdicts-D.jsonl")) if r.get("sub") in want and not r.get("ruled_by")}
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) if l["sub"] in want}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r.get("adaptation") in led:
        last[r["adaptation"]] = r
cls = {}
for s in glob.glob(os.path.join(OUT, "_analysis", "d3_rulings", "propose-spec-*.txt")):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, c = line.split("|")[:2]
            cls[i] = c


def item(sub, x):
    x = str(x).split(":")[-1]
    if x.startswith("t"):
        return "%s [theme] %s (placed %s)" % (x, tl.get((sub, x)), place.get((sub, x)))
    lab = cl.get((sub, x))
    return "%s %s (h%s)" % (x, lab[0] if lab else None, lab[1] if lab else "?")


w = []
for n, r in enumerate(page, a.offset):
    sub = r["sub"]
    f = rooms.get(sub, {})
    codes, off = f.get("codes") or 0, f.get("n_off_platform") or 0
    flags = []
    if codes < 10:
        flags.append("below the concept floor")
    if off >= 20 or (off >= 3 and off * 4 >= codes):
        flags.append("past the off-platform threshold")
    w.append("#### %d. %s  (%s against %s)" % (n, sub, r["pair"][0], r["pair"][1]))
    w.append("figures: concepts %s, themes %s, off-platform pointers %s, threads coded %s%s"
             % (codes, f.get("themes"), off, f.get("threads_coded"), ("; " + ", ".join(flags)) if flags else ""))
    named = []
    for e in verd.get(sub, {}).get("readers", []):
        w.append("  %s: %s%s" % (e.get("reader"), e.get("verdict"),
                                 (" under " + str(e.get("cannot_tell_under"))) if e.get("cannot_tell_under") else ""))
        w.append("     sentence: %s" % e.get("sentence"))
        if e.get("residue"):
            w.append("     residue:")
            for x in e["residue"]:
                w.append("       - " + item(sub, x))
        extra = [c for c in (e.get("concepts") or []) if c not in (e.get("residue") or [])]
        if extra:
            w.append("     concepts named, not as residue: " + ", ".join(str(c) for c in extra))
            named += [c for c in extra if c not in named]
    if named:
        w.append("  named concepts: " + "; ".join(item(sub, c) for c in named))
    ops = collections.defaultdict(list)
    held = collections.Counter()
    for i, l in led.items():
        if l["sub"] != sub or l.get("op") not in ("propose", "add-step", "add-condition", "link"):
            continue
        d = last.get(i, {})
        if l["op"] == "propose":
            ops["propose"].append("%s %s" % (i, cls.get(i, "?")))
        elif d.get("kind") == "elaboration" or d.get("decision") == "particular":
            ops[l["op"]].append("%s on %s %s/%s" % (i, l.get("element"), d.get("decision"), d.get("kind")))
        else:
            held[l["op"]] += 1
    for op in ("propose", "add-step", "add-condition", "link"):
        if ops[op] or held[op]:
            w.append("  D3 %s: %s%s" % (op, "; ".join(sorted(ops[op])),
                                         ("  [+%d held as specification or limit]" % held[op]) if held[op] else ""))
    w.append("")
open(a.out, "w", encoding="utf-8").write("\n".join(w) + "\n")
print("wrote %s: rooms %d to %d of %d" % (a.out, a.offset, a.offset + len(page) - 1, len(order)))
