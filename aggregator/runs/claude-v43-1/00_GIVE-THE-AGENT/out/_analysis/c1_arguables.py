#!/usr/bin/env python3
"""C1 section 6, the arguables against stage B1's written prediction (confusions.md).

An arguable line is a line of assignments_final.jsonl with confidence "arguable". The readers' confusion on it is read
from b3_classes.jsonl: a split pair is an unordered pair (a, b) with a placed by one B3 reader and not the other, and b
placed by the other and not the first. Class 4 lines (the readers agree, my B1 differs) are counted apart, as
reader-against-B1 splits. The 19 predicted pairs are parsed from confusions.md's numbered list.

    python3 out/_analysis/c1_arguables.py                 the comparison
    python3 out/_analysis/c1_arguables.py --list           writes c1_arguables_list.md, every arguable line, grouped
"""
import argparse, collections, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "out")


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def predicted():
    txt = open(os.path.join(OUT, "confusions.md"), encoding="utf-8").read()
    pairs = []
    for m in re.finditer(r"^(\d+)\. \*\*(T3-\d{3}) [^/*]*/ (T3-\d{3})", txt, re.M):
        pairs.append((int(m.group(1)), tuple(sorted((m.group(2), m.group(3))))))
    return pairs


def splits(x, y):
    a, b = set(x or []), set(y or [])
    return set(tuple(sorted((p, q))) for p in a - b for q in b - a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    rows = jl(os.path.join(OUT, "assignments_final.jsonl"))
    b3 = dict(((r["sub"], r["theme_id"]), r) for r in jl(os.path.join(OUT, "b3_classes.jsonl")))
    names = dict((t["id"], t["name"]) for t in jl(os.path.join(OUT, "scheme_v2.jsonl")))
    pred = predicted()
    pset = dict((p, n) for n, p in pred)

    placed = [r for r in rows if r.get("third_order")]
    arg = [r for r in rows if r.get("confidence") == "arguable"]
    argp = [r for r in arg if r.get("third_order")]
    print("lines %d; placed %d; arguable %d (placed %d, empty %d); arguable rate among placed %.3f" % (
        len(rows), len(placed), len(arg), len(argp), len(arg) - len(argp), len(argp) / float(len(placed))))
    print("arguable by class: " + json.dumps(dict(sorted(collections.Counter(str((b3.get((r["sub"], r["theme_id"])) or {}).get("class")) for r in arg).items()))))

    rr = collections.Counter()
    rb = collections.Counter()
    per = collections.defaultdict(list)
    no_split = 0
    for r in arg:
        c = b3.get((r["sub"], r["theme_id"])) or {}
        s = splits(c.get("r1"), c.get("r2"))
        for p in s:
            rr[p] += 1
            per[p].append(r)
        if not s:
            no_split += 1
            readers = sorted(set((c.get("r1") or []) + (c.get("r2") or [])))
            for p in splits(readers, c.get("b1")):
                rb[p] += 1
    lines_with_split = len(arg) - no_split
    print("arguable lines where the two readers split: %d; where they agree (split only against my B1, or none): %d" % (
        lines_with_split, no_split))
    covered = sum(1 for r in arg if any(p in pset for p in splits((b3.get((r["sub"], r["theme_id"])) or {}).get("r1"),
                                                                     (b3.get((r["sub"], r["theme_id"])) or {}).get("r2"))))
    print("lines whose reader split crosses a predicted pair: %d of %d (%.1f%%)" % (covered, lines_with_split,
                                                                                    100.0 * covered / max(1, lines_with_split)))
    ranked = [p for p, _ in rr.most_common()]
    print("\npredicted pairs (confusions.md order): reader-split lines, rank among %d split pairs; reader-against-B1 lines" % len(ranked))
    for n, p in pred:
        rk = ranked.index(p) + 1 if p in rr else None
        print("%2d %s | %s  %4d  rank %s   %d" % (n, p[0], p[1], rr.get(p, 0), rk, rb.get(p, 0)))
    print("\ntop 30 reader-split pairs: lines, predicted?")
    for p, k in rr.most_common(30):
        print("%s | %s  %4d  %s   %s / %s" % (p[0], p[1], k, ("predicted #%d" % pset[p]) if p in pset else "-",
                                          names.get(p[0], ""), names.get(p[1], "")))
    top20 = [p for p, _ in rr.most_common(20)]
    print("\npredicted among the top 10: %d; top 20: %d; top 30: %d" % (
        sum(1 for p in ranked[:10] if p in pset), sum(1 for p in top20 if p in pset), sum(1 for p in ranked[:30] if p in pset)))
    print("top 15 reader-against-B1 pairs (readers agree): " + "; ".join("%s|%s %d%s" % (p[0], p[1], k, "*" if p in pset else "")
                                                                          for p, k in rb.most_common(15)))

    # Added-theme pairs: both readers place y, one of them also places x (x in the symmetric difference).
    ad = collections.Counter()
    add_lines = 0
    for r in arg:
        c = b3.get((r["sub"], r["theme_id"])) or {}
        s1, s2 = set(c.get("r1") or []), set(c.get("r2") or [])
        ps = set(tuple(sorted((x, y))) for x in (s1 ^ s2) for y in (s1 & s2))
        if ps:
            add_lines += 1
        for p in ps:
            ad[p] += 1
    aranked = [p for p, _ in ad.most_common()]
    print("\narguable lines where the readers share a theme and one adds another: %d" % add_lines)
    print("predicted pairs as added-theme pairs: lines, rank among %d" % len(aranked))
    print("; ".join("#%d %s|%s %d (rank %s)" % (n, p[0], p[1], ad.get(p, 0), (aranked.index(p) + 1) if p in ad else "-")
                    for n, p in pred))
    print("top 20 added-theme pairs: " + "; ".join("%s|%s %d%s" % (p[0], p[1], k, ("*#%d" % pset[p]) if p in pset else "")
                                                   for p, k in ad.most_common(20)))
    both = collections.Counter()
    for p in set(rr) | set(ad):
        both[p] = rr.get(p, 0) + ad.get(p, 0)
    branked = [p for p, _ in both.most_common()]
    print("\nboth forms together: predicted pairs' ranks among %d pairs: %s" % (
        len(branked), ", ".join("#%d:%s" % (n, (branked.index(p) + 1) if p in both else "-") for n, p in pred)))
    print("predicted among the top 10: %d; top 20: %d; top 30: %d" % tuple(sum(1 for p in branked[:k] if p in pset) for k in (10, 20, 30)))
    print("top 30, both forms: " + "; ".join("%s|%s %d%s" % (p[0], p[1], k, ("*#%d" % pset[p]) if p in pset else "")
                                             for p, k in both.most_common(30)))

    if a.list:
        spec = importlib.util.spec_from_file_location("bpf", os.path.join(HERE, "b2_packets_fleet.py"))
        bpf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bpf)
        store = bpf.pk.Store(ROOT, OUT)
        done = set()

        def line(r):
            c = b3.get((r["sub"], r["theme_id"])) or {}
            sup = r.get("support_by_theme") or {}
            th = store.themes.get((r["sub"], r["theme_id"])) or {}
            return "- %s:%s c%s | %s | r1 %s r2 %s B1 %s | %s" % (
                r["sub"], r["theme_id"], c.get("class"),
                ", ".join("%s(%d)" % (z, len(sup.get(z) or [])) for z in r.get("third_order") or []) or "EMPTY",
                ",".join(c.get("r1") or []), ",".join(c.get("r2") or []), ",".join(c.get("b1") or []), th.get("second_order"))

        L = ["# Every arguable line, grouped (C1a-08)", "",
             "Each line: item, class | the line's themes (concepts) | B3 readers and my B1 | the second-order label.", ""]
        order = [p for _, p in pred] + [p for p in ranked if p not in pset]
        for p in order:
            items = [r for r in per.get(p, []) if (r["sub"], r["theme_id"]) not in done]
            if not items:
                continue
            tag = ("predicted #%d" % pset[p]) if p in pset else "not predicted"
            L.append("## %s | %s (%s; %d lines split here, %d new in this list)" % (p[0], p[1], tag, rr[p], len(items)))
            for r in sorted(items, key=lambda r: (r["sub"].lower(), r["theme_id"])):
                L.append(line(r))
                done.add((r["sub"], r["theme_id"]))
            L.append("")
        rest = [r for r in arg if (r["sub"], r["theme_id"]) not in done]
        by = collections.defaultdict(list)
        for r in rest:
            by[(r.get("third_order") or ["EMPTY"])[0]].append(r)
        L.append("# Arguable lines where the readers did not split, by the line's first theme")
        L.append("")
        for k in sorted(by):
            L.append("## %s %s (%d)" % (k, names.get(k, ""), len(by[k])))
            for r in sorted(by[k], key=lambda r: (r["sub"].lower(), r["theme_id"])):
                L.append(line(r))
            L.append("")
        pth = os.path.join(HERE, "c1_arguables_list.md")
        if os.path.exists(pth):
            sys.exit("%s exists" % pth)
        open(pth, "w", encoding="utf-8").write("\n".join(L) + "\n")
        print("wrote %s: %d bytes, %d lines" % (os.path.relpath(pth, ROOT), os.path.getsize(pth), len(L)))


if __name__ == "__main__":
    main()
