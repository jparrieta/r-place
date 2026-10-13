#!/usr/bin/env python3
"""C1, the pair test's reading (section 5), as declared in the diary at C1a-06: the 76 pairs materially above the
corpus arguable rate (c1_pair_test.json), numbered in order of n (ties by the pair's ids); for each, every item when
twelve or fewer carry it, else twelve drawn by random.Random(20261014).sample from the sorted items. For each item: its
label and note, class, confidence, the readers' and my B1's placements, the line's themes with counts, and the concepts
counted for each theme of the pair (id | label). Writes out/_analysis/c1_pair_packs/pairs-AA-BB.md, refusing to
overwrite. --list prints the numbered pairs.

    python3 out/_analysis/c1_pair_pack.py --from 1 --to 8 | --list
"""
import argparse, importlib.util, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")


def pairs_in_order():
    d = json.load(open(os.path.join(AN, "c1_pair_test.json"), encoding="utf-8"))
    ps = [p for p in d["pairs"] if p["material"]]
    ps.sort(key=lambda p: (-p["n"], p["pair"]))
    return ps


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--from", dest="a", type=int); ap.add_argument("--to", dest="b", type=int)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    ps = pairs_in_order()
    if a.list:
        for i, p in enumerate(ps, 1):
            print("%2d %s|%s n=%d rate %.3f  %s | %s" % (i, p["pair"][0], p["pair"][1], p["n"], p["rate"], p["names"][0], p["names"][1]))
        return
    spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
    bpf = importlib.util.module_from_spec(spec); spec.loader.exec_module(bpf)
    store = bpf.pk.Store(ROOT, OUT)
    rows = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in map(json.loads, open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"))}
    b3 = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in map(json.loads, open(os.path.join(OUT, "b3_classes.jsonl"), encoding="utf-8"))}
    L = ["# Pair test reading, pairs %d to %d (declared at C1a-06; seed 20261014)" % (a.a, a.b), ""]
    for i in range(a.a, a.b + 1):
        p = ps[i - 1]
        x, y = p["pair"]
        items = sorted(k for k, r in rows.items() if x in (r.get("third_order") or []) and y in (r.get("third_order") or []))
        if len(items) != p["n"]:
            sys.exit("pair %d: %d items now, %d at the test" % (i, len(items), p["n"]))
        pick = items if len(items) <= 12 else sorted(random.Random(20261014).sample(items, 12))
        L += ["## Pair %d. %s %s | %s %s  (n=%d, arguable %d, clear %d; read %d)" % (i, x, p["names"][0], y, p["names"][1], p["n"],
              p["arguable"], p["clear"], len(pick)), ""]
        for it in pick:
            s, t = it.split(":")
            r, c, th = rows[it], b3.get(it) or {}, store.themes[(s, t)]
            sup = r.get("support_by_theme") or {}
            L += ["### %s/%s  (class %s, %s)" % (s, t, c.get("class"), r.get("confidence")),
                  "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")),
                  "line: %s; reader 1 %s; reader 2 %s; my B1 %s" % (", ".join("%s (%d)" % (z, len(sup.get(z) or [])) for z in r.get("third_order") or []),
                                                               c.get("r1"), c.get("r2"), c.get("b1"))]
            for z in (x, y):
                labs = []
                for cid in sup.get(z) or []:
                    cd = store.codes.get((s, cid)) or {}
                    labs.append("%s %s" % (cid, cd.get("first_order") or ""))
                L.append("- %s: %s" % (z, " / ".join(labs) or "-"))
            L.append("")
    os.makedirs(os.path.join(AN, "c1_pair_packs"), exist_ok=True)
    pth = os.path.join(AN, "c1_pair_packs", "pairs-%02d-%02d.md" % (a.a, a.b))
    if os.path.exists(pth):
        sys.exit("%s exists" % pth)
    open(pth, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d bytes, %d lines" % (os.path.relpath(pth, ROOT), os.path.getsize(pth), len(L)))


if __name__ == "__main__":
    main()
