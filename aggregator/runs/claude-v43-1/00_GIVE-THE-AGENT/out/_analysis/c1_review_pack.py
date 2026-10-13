#!/usr/bin/env python3
"""C1, read-only: a review packet for named lines. For each item: its label and note, its line (themes with concept
counts and concepts), its class and the readers' and my B1's placements, its also_present; then every concept, with
its label, and its words whole where the concept is counted for one of --themes or its label or words match --grep.
Writes out/_analysis/c1_rechecks/<name>.md, refusing to overwrite.

    python3 out/_analysis/c1_review_pack.py --items "evex:t04,uva:t02" --themes T3-010,T3-149 --grep "peace|truce" --name review-x
"""
import argparse, importlib.util, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
AN = os.path.join(OUT, "_analysis")
sys.path.insert(0, os.path.join(ROOT, "tools"))
spec = importlib.util.spec_from_file_location("bpf", os.path.join(AN, "b2_packets_fleet.py"))
bpf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bpf)


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True); ap.add_argument("--themes", default=""); ap.add_argument("--grep", default="")
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    fin = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("assignments_final.jsonl")}
    b3 = {"%s:%s" % (r["sub"], r["theme_id"]): r for r in jl("b3_classes.jsonl")}
    store = bpf.pk.Store(ROOT, OUT)
    rx = re.compile(a.grep, re.I) if a.grep else None
    themes = [t for t in a.themes.split(",") if t]
    L = ["# Review packet: %s" % a.items, ""]
    for it in [x.strip() for x in a.items.split(",") if x.strip()]:
        s, t = it.split(":")
        r, c, th = fin[it], b3.get(it) or {}, store.themes[(s, t)]
        sup = r.get("support_by_theme") or {}
        owner = {cid: k for k, v in sup.items() for cid in v}
        L += ["## %s/%s" % (s, t), "", "**%s** | note: %s" % (th.get("second_order"), th.get("theme_note")), "",
              "**Now placed:** %s" % "; ".join("%s (%d)=%s" % (x, len(sup.get(x) or []), ",".join(sup.get(x) or []))
                                             for x in (r.get("third_order") or [])),
              "class %s; reader 1 %s; reader 2 %s; my B1 %s; also_present %s" % (
                  c.get("class"), c.get("r1"), c.get("r2"), c.get("b1"), list((r.get("also_present") or {}).keys())), ""]
        for cid in th.get("code_ids") or []:
            cd = store.codes.get((s, cid))
            if not cd:
                continue
            lab, words = cd.get("first_order") or "", " ".join(str(cd.get("text") or "").split())
            mark = owner.get(cid, "-")
            if mark in themes or (rx and (rx.search(lab) or rx.search(words))):
                L.append("- **%s** [%s] %s | %s" % (cid, mark, lab, words))
            else:
                L.append("- %s [%s] %s" % (cid, mark, lab))
        L.append("")
    p = os.path.join(AN, "c1_rechecks", a.name + ".md")
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s: %d bytes, %d lines" % (os.path.relpath(p, ROOT), os.path.getsize(p), len(L)))


if __name__ == "__main__":
    main()
