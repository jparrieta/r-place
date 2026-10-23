#!/usr/bin/env python3
"""D3b: one page of the re-check's split rooms for the verdict rulings (G62, which applies G60 and G60a to the
revised model). The split rooms are the rooms of verdicts-recheck-D.jsonl whose two readers differ, in the order
(pair, then room). For each room: its figures against prior.md section 8 (concepts, themes, off-platform pointers;
the floor and the threshold flagged), the room's verdict before (my D3a-56 ruling where the first readers split,
else their agreed verdict), both re-check readers' lines whole (verdict, cannot_tell_under, sentence, and each named
theme or concept with its label), and the room's re-check rulings that bear on residue: every propose line with its
last ruling whole; every accepted correction and every particular, on any op, whole; and the paired elaborations
(element and codes). No canvas measure is printed (rule 7). Writes the page to --out; nothing else is written.

    python3 out/_analysis/d3b_verdict_packet.py --offset 0 --limit 20 --out out/_analysis/d3b2_vp_000.txt
"""
import argparse, collections, json, os

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


rv = jl(os.path.join(OUT, "verdicts-recheck-D.jsonl"))
split = []
for r in rv:
    vs = sorted({e["verdict"] for e in r["readers"]})
    if len(vs) > 1:
        split.append({"sub": r["sub"], "pair": vs})
order = sorted(split, key=lambda r: (r["pair"], r["sub"].lower()))
page = order[a.offset:a.offset + a.limit]
want = {r["sub"] for r in page}
rec = {r["sub"]: r for r in rv if r["sub"] in want}
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
before = {}
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("sub") not in want or r.get("recheck"):
        continue
    if r.get("ruled_by") == "analyst":
        before[r["sub"]] = "%s (my D3a-56 ruling)" % r["verdict"]
    elif r["sub"] not in before:
        vs = sorted({e["verdict"] for e in r["readers"]})
        before[r["sub"]] = vs[0] if len(vs) == 1 else "split %s (unruled)" % "/".join(vs)
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations-recheck.jsonl")) if l["sub"] in want}
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    if r.get("adaptation") in led:
        last[r["adaptation"]] = r


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
    w.append("before: %s; labeler's grade now: %s" % (before.get(sub, "?"), rec[sub].get("grade")))
    named = []
    for e in rec[sub]["readers"]:
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
    prop, corr, part, elab = [], [], [], []
    for i in sorted(led):
        l = led[i]
        if l["sub"] != sub:
            continue
        d = last.get(i, {})
        dk = "%s/%s" % (d.get("decision"), d.get("kind"))
        if l.get("op") == "propose":
            prop.append("    %s %s: %s" % (i, dk, d.get("reason")))
        elif d.get("kind") == "correction":
            corr.append("    %s on %s %s: %s" % (i, l.get("element"), l.get("op"), d.get("reason")))
        elif d.get("decision") == "particular":
            part.append("    %s on %s %s: %s" % (i, l.get("element"), l.get("op"), d.get("reason")))
        elif d.get("kind") == "elaboration":
            elab.append("%s on %s %s" % (i, l.get("element"), l.get("op")))
    if prop:
        w.append("  re-check propose lines:")
        w += prop
    if corr:
        w.append("  re-check accepted corrections:")
        w += corr
    if part:
        w.append("  re-check particulars:")
        w += part
    if elab:
        w.append("  re-check paired elaborations: " + "; ".join(elab))
    w.append("")
open(a.out, "w", encoding="utf-8").write("\n".join(w) + "\n")
print("wrote %s: rooms %d to %d of %d split rooms" % (a.out, a.offset, a.offset + len(page) - 1, len(order)))
