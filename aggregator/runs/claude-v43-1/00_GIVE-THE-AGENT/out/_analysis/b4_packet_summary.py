#!/usr/bin/env python3
"""B4a: the figures of one ruled adjudication packet, for notes-B4.md and adjudication_report.md (section 9).

    python3 out/_analysis/b4_packet_summary.py --packet 1 [--write]

Reads out/disagreements.jsonl (this packet's lines), out/confusions.md (stage B2's nineteen predicted pairs) and
out/_adjudication-B4/boundaries.md (to say which boundary pairs have a paragraph there). Prints, and with --write
writes out/_adjudication-B4/packet-NN/summary.md:
  the taxonomy split, overall and by class; the unresolved, named_neither, author-error and author-disagrees counts;
  fields by ambiguity (four numbers); third-order themes by ambiguity, ranked; every boundary_ruling pair with its
  item list; agreement before (reader against reader) and after (each reader against the ruling, unresolved items
  left out), by mean Jaccard on placement sets and by primary match; and the readers' primary splits on the
  predicted pairs.
"""
import argparse, collections, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
TAX = ("scheme-ambiguous", "item-is-a-bag", "reader-error", "author-error", "genuine-joint", "author-disagrees")
FIELDS = ("must_show", "must_not_show", "decide_when_both", "discriminators")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def jac(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    rows = [d for d in jl(os.path.join(OUT, "disagreements.jsonl")) if d.get("packet") == a.packet]
    rows.sort(key=lambda d: d["n"])
    n = len(rows)
    tax = collections.Counter(d["taxonomy"] for d in rows)
    by_class = collections.defaultdict(collections.Counter)
    for d in rows:
        by_class[d["class"]][d["taxonomy"]] += 1
    unres = [d for d in rows if d["unresolved"]]
    nn = [d for d in rows if d["named_neither"]]
    revised = [d for d in rows if d.get("revised")]
    amb = [d for d in rows if d["taxonomy"] == "scheme-ambiguous"]
    fields = collections.Counter(d["field"] for d in amb)
    themes = collections.Counter(d["theme"] for d in amb)
    th_field = collections.defaultdict(collections.Counter)
    for d in amb:
        th_field[d["theme"]][d["field"]] += 1
    pairs = collections.defaultdict(list)
    for d in rows:
        if d.get("boundary_ruling"):
            pairs[d["boundary_ruling"]].append(d)
    btxt = open(os.path.join(OUT, "_adjudication-B4", "boundaries.md"), encoding="utf-8").read()
    # agreement before and after
    before_j, before_p, after_j, after_p = [], [], [], []
    for d in rows:
        r1, r2 = d["readers"]
        before_j.append(jac(r1, r2))
        before_p.append(1.0 if (r1[:1] == r2[:1] and r1) else 0.0)
        if d["unresolved"]:
            continue
        for r in (r1, r2):
            after_j.append(jac(r, d["ruling"]))
            after_p.append(1.0 if (r[:1] == d["ruling"][:1]) else 0.0)
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")
    # predicted pairs (confusions.md, numbered bold lines)
    pred = []
    for ln in open(os.path.join(OUT, "confusions.md"), encoding="utf-8"):
        m = re.match(r"\s*(\d+)\.\s+\*\*(T3-\d{3})[^/]*/\s*(T3-\d{3})", ln)
        if m:
            pred.append((int(m.group(1)), tuple(sorted((m.group(2), m.group(3))))))
    splits = collections.Counter()
    for d in rows:
        r1, r2 = d["readers"]
        if r1 and r2 and r1[0] != r2[0]:
            splits[tuple(sorted((r1[0], r2[0])))] += 1
    lines = []
    w = lines.append
    w("# Packet %d, the figures (stage B4 section 9)" % a.packet)
    w("")
    w("Written by `out/_analysis/b4_packet_summary.py` from `disagreements.jsonl`. Items ruled: %d." % n)
    w("")
    w("## The taxonomy split")
    w("")
    w("The next table counts the packet's rulings by taxonomy value, overall and by J's class of the item.")
    w("")
    cls = sorted(by_class)
    w("| taxonomy | all | " + " | ".join("class %s" % c for c in cls) + " |")
    w("|---|---|" + "---|" * len(cls))
    for t in TAX:
        w("| %s | %d | " % (t, tax.get(t, 0)) + " | ".join(str(by_class[c].get(t, 0)) for c in cls) + " |")
    w("| total | %d | " % n + " | ".join(str(sum(by_class[c].values())) for c in cls) + " |")
    w("")
    w("- unresolved: %d (%.1f%%)" % (len(unres), 100.0 * len(unres) / n))
    w("- named_neither: %d (%.1f%%)" % (len(nn), 100.0 * len(nn) / n))
    w("- author-error: %d; author-disagrees: %d" % (tax.get("author-error", 0), tax.get("author-disagrees", 0)))
    w("- rulings corrected in place after writing: %d (%s)" % (len(revised), ", ".join("%s %s" % (d["sub"], d["theme_id"]) for d in revised) or "none"))
    w("")
    w("## Fields by ambiguity")
    w("")
    w("The next list counts the scheme-ambiguous rulings by the field whose sentence failed to decide.")
    w("")
    for f in FIELDS:
        w("- %s: %d" % (f, fields.get(f, 0)))
    w("")
    w("## Third-order themes by ambiguity")
    w("")
    w("The next table ranks the themes whose sentence failed to decide, with the fields.")
    w("")
    w("| theme | rulings | " + " | ".join(FIELDS) + " |")
    w("|---|---|" + "---|" * len(FIELDS))
    for t, c in themes.most_common():
        w("| %s | %d | " % (t, c) + " | ".join(str(th_field[t].get(f, 0)) for f in FIELDS) + " |")
    w("")
    w("## Boundary pairs and their items")
    w("")
    w("Each pair below is carried in `boundary_ruling` on the items listed. \"Paragraph\" says whether "
      "`boundaries.md` holds the pair's paragraph.")
    w("")
    for p in sorted(pairs, key=lambda k: -len(pairs[k])):
        x, y = p.split("|")
        has = ("%s|%s" % (x, y)) in btxt or ("%s|%s" % (y, x)) in btxt
        items = ", ".join("%s %s" % (d["sub"], d["theme_id"]) for d in pairs[p])
        tc = collections.Counter(d["taxonomy"] for d in pairs[p])
        w("- **%s** (%d items; paragraph %s; %s): %s" % (p, len(pairs[p]), "yes" if has else "no",
                                                          ", ".join("%s %d" % kv for kv in tc.most_common()), items))
    w("")
    w("## Agreement before and after")
    w("")
    w("Before is the two readers against each other over the packet's %d items. After is each reader against the "
      "ruling over the %d items not unresolved. The figure after is not a reliability figure: it is agreement "
      "with an adjudication I performed." % (n, n - len(unres)))
    w("")
    w("| | mean Jaccard | primary match |")
    w("|---|---|---|")
    w("| before (reader against reader) | %.3f | %.3f |" % (mean(before_j), mean(before_p)))
    w("| after (each reader against the ruling) | %.3f | %.3f |" % (mean(after_j), mean(after_p)))
    w("")
    w("## Stage B2's predicted pairs")
    w("")
    w("The next list gives, for each of `confusions.md`'s nineteen pairs, the packet's items whose two readers "
      "put the pair's themes as their primaries.")
    w("")
    for k, pr in pred:
        w("- pair %d, %s|%s: %d" % (k, pr[0], pr[1], splits.get(pr, 0)))
    w("")
    w("The packet's ten commonest primary splits, predicted or not:")
    w("")
    pset = {pr for _, pr in pred}
    for pr, c in splits.most_common(10):
        w("- %s|%s: %d%s" % (pr[0], pr[1], c, " (predicted)" if pr in pset else ""))
    w("")
    w("## Unresolved items")
    w("")
    for d in unres:
        w("- %s %s: %s, %s %s" % (d["sub"], d["theme_id"], d["taxonomy"], d.get("theme") or "", d.get("field") or ""))
    w("")
    txt = "\n".join(lines)
    print(txt)
    if a.write:
        p = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet, "summary.md")
        open(p, "w", encoding="utf-8").write(txt + "\n")
        print("wrote %s" % os.path.relpath(p, ROOT))


if __name__ == "__main__":
    main()
