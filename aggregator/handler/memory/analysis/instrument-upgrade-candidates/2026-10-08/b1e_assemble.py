#!/usr/bin/env python3
"""B1e: assemble scheme.jsonl, families.jsonl and scheme.md from the family drafts.

Inputs: out/_analysis/b1e_draft_G01.jsonl ... G21 (one line per theme, with old_label and
two_or_half, which do not ship), out/_analysis/b1e_families.tsv, out/_analysis/b1e_floor.tsv.
The floor TSV gives tier and a size floor; FORM below gives the hand-chosen floors where no pair
of rooms is twice apart in size. Counts of rule 0 lines written into a gate during drafting are
cut, since the stranger is not given them (section 3: no counts; refer to nothing not given).

Dry run by default: prints what it would write and every flag. --write writes out/scheme.jsonl,
out/families.jsonl, out/scheme.md and out/_analysis/b1e_two_or_half.md (for notes-B1.md).
"""
import collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")

FORM = {
    "T3-173": {"rooms": ["GreenCorner", "AprilKnights"], "unlike": "form",
               "why": "GreenCorner is a sub made on the canvas for a colour faction, AprilKnights an order carried over from the 2015 Button event"},
    "T3-189": {"rooms": ["scp", "parahumans"], "unlike": "form",
               "why": "scp is a sub whose members write the fiction together, parahumans the fan sub of one author's web serial"},
}
FIELDS = ("name", "gloss", "must_show", "must_not_show", "decide_when_both", "varies", "is_not")
COUNT = re.compile(r"\s*\((?:[^()]*\b(?:rule 0 lines?|\d+ (?:bag )?lines?)\b[^()]*|\d+)\)")
FLAG = re.compile(r"B1[a-e]|\bhead\b|\bPI\b|\bnotes\b(?<!patch notes)|\bt\d\d\b|c\d{4}|\d+ (?:bag )?lines?\b|bag line")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def tsv(p):
    with open(p, encoding="utf-8") as f:
        rows = [x.rstrip("\n").split("\t") for x in f if x.strip()]
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def main():
    write = "--write" in sys.argv
    fams = tsv(os.path.join(AN, "b1e_families.tsv"))
    fam_of = {t: f["family"] for f in fams for t in f["themes"].split(",")}
    floor = {r["id"]: r for r in tsv(os.path.join(AN, "b1e_floor.tsv"))}
    cur = {r["theme"]: r for r in jl(os.path.join(OUT, "scheme", "scheme_current.jsonl"))}
    drafts = {}
    for p in sorted(glob.glob(os.path.join(AN, "b1e_draft_G*.jsonl"))):
        for r in jl(p):
            if r["id"] in drafts:
                print("FLAG %s drafted twice" % r["id"])
            drafts[r["id"]] = r
    missing = sorted(set(cur) - set(drafts))
    extra = sorted(set(drafts) - set(cur))
    if missing or extra:
        print("FLAG missing from drafts %s; drafted but not current %s" % (missing, extra))
    rows, cut, flags, relabels = [], [], [], []
    for f in fams:
        for tid in f["themes"].split(","):
            d = drafts[tid]
            if d["family"] != f["family"]:
                flags.append("%s family %s in draft, %s in TSV" % (tid, d["family"], f["family"]))
            r = {"id": tid}
            for k in FIELDS:
                v = d[k]
                v2 = COUNT.sub("", v)
                if v2 != v:
                    cut.append((tid, k, v[:0] + ", ".join(m.group(0).strip() for m in COUNT.finditer(v))))
                r[k] = v2
                if FLAG.search(v2):
                    flags.append("%s %s: %r" % (tid, k, FLAG.findall(v2)))
            r["family"] = f["family"]
            fl = floor[tid]
            r["tier"] = "rare" if fl["tier"] == "rare" else "main"
            if r["tier"] == "main":
                r["floor"] = FORM[tid] if tid in FORM else {"rooms": [fl["room_a"], fl["room_b"]], "unlike": "size", "why": fl["why"]}
            disc = []
            for x in d["discriminators"]:
                q = COUNT.sub("", x["question"])
                if FLAG.search(q):
                    flags.append("%s disc %s: %r" % (tid, x["vs"], FLAG.findall(q)))
                disc.append({"vs": x["vs"], "question": q})
            r["discriminators"] = disc
            r["gate_parts"] = d["gate_parts"]
            r["exemplars"] = [{"sub": e["sub"], "quote": e["quote"], "code_id": e["code_id"], "rivals": e.get("rivals") or []}
                              for e in d["exemplars"]]
            order = ("id", "name", "gloss", "family", "tier", "floor", "must_show", "must_not_show", "decide_when_both",
                     "discriminators", "varies", "is_not", "gate_parts", "exemplars")
            rows.append({k: r[k] for k in order if k in r})
            if d["name"] != cur[tid]["label"]:
                relabels.append((tid, cur[tid]["label"], d["name"]))
            if d.get("old_label") != cur[tid]["label"]:
                flags.append("%s old_label %r is not the current label %r" % (tid, d.get("old_label"), cur[tid]["label"]))
    print("themes %d (main %d, rare %d); families %d; relabelled %d; rule 0 counts cut in %d fields" % (
        len(rows), sum(r["tier"] == "main" for r in rows), sum(r["tier"] == "rare" for r in rows), len(fams),
        len(relabels), len(cut)))
    for x in flags:
        print("FLAG", x)
    if not write:
        return
    with open(os.path.join(OUT, "scheme.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "families.jsonl"), "w", encoding="utf-8") as f:
        for x in fams:
            f.write(json.dumps({"family": x["family"], "name": x["name"], "themes": x["themes"].split(",")}, ensure_ascii=False) + "\n")
    by_fam = collections.defaultdict(list)
    for r in rows:
        by_fam[r["family"]].append(r)
    L = []
    L.append("# The third-order scheme, B1e")
    L.append("")
    L.append("Written at stage B1, leg B1e, 2026-10-11. %d themes in %d families; %d are on the rare tier (seen in one room, "
             "or in rooms that tell one episode). Not frozen: stage B2 tightens it against fresh readers." % (
                 len(rows), len(fams), sum(r["tier"] == "rare" for r in rows)))
    L.append("")
    L.append("How to read a theme. Place each second-order theme on one theme. Add a second or a third only where a concept "
             "of its own supports it, and say why one does not carry it. The gate is must show, must not show and decide "
             "when both. A discriminator is the question that separates a theme from a near neighbour. A family is an index "
             "of themes a reader would confuse, and nothing else. Exemplars are participants' words, with the room and the "
             "concept id; rivals are other concepts of the same room that also pass the gate.")
    L.append("")
    L.append("## Index")
    L.append("")
    for x in fams:
        L.append("**%s %s**" % (x["family"], x["name"]))
        L.append("")
        for r in by_fam[x["family"]]:
            L.append("- %s %s%s: %s" % (r["id"], r["name"], " (rare)" if r["tier"] == "rare" else "", r["gloss"]))
        L.append("")
    for x in fams:
        L.append("## %s %s" % (x["family"], x["name"]))
        L.append("")
        for r in by_fam[x["family"]]:
            L.append("### %s %s" % (r["id"], r["name"]))
            L.append("")
            if r["tier"] == "rare":
                L.append("Rare tier. %s" % r["gloss"])
            else:
                L.append("%s Floor: %s and %s, unlike in %s (%s)." % (r["gloss"], r["floor"]["rooms"][0], r["floor"]["rooms"][1],
                                                                     r["floor"]["unlike"], r["floor"]["why"]))
            L.append("")
            L.append("- Must show: %s" % r["must_show"])
            L.append("- Must not show: %s" % r["must_not_show"])
            L.append("- Decide when both: %s" % r["decide_when_both"])
            for dsc in r["discriminators"]:
                L.append("- Against %s: %s" % (dsc["vs"], dsc["question"]))
            L.append("- Varies: %s" % r["varies"])
            L.append("- Is not: %s" % r["is_not"])
            ex = "; ".join('"%s" (%s %s%s)' % (e["quote"], e["sub"], e["code_id"],
                                              ", rivals " + " ".join(e["rivals"]) if e["rivals"] else "") for e in r["exemplars"])
            L.append("- Exemplars: %s" % ex)
            L.append("")
    with open(os.path.join(OUT, "scheme.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    T = ["### The strongest argument that each theme is two, or half of another (section 7)", ""]
    for x in fams:
        for r in by_fam[x["family"]]:
            T.append("- %s %s: %s" % (r["id"], r["name"], drafts[r["id"]]["two_or_half"]))
    T.append("")
    with open(os.path.join(AN, "b1e_two_or_half.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(T))
    with open(os.path.join(AN, "b1e_relabels.tsv"), "w", encoding="utf-8") as f:
        f.write("id\twas\tnow\n")
        for t, a, b in relabels:
            f.write("%s\t%s\t%s\n" % (t, a, b))
    print("wrote out/scheme.jsonl, out/families.jsonl, out/scheme.md, out/_analysis/b1e_two_or_half.md, out/_analysis/b1e_relabels.tsv")


if __name__ == "__main__":
    main()
