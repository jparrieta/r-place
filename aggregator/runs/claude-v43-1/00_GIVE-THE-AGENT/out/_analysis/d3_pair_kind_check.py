#!/usr/bin/env python3
"""D3: for every adaptation whose latest ruling is an accepted elaboration, check that its pair's latest ruling is
still an accepted elaboration. A pair whose latest ruling has become a specification (or anything else) no longer
shows the same elaboration, so the line needs a new pair, a particular ruling, or a ruling of its own kind.
Reads adjudications.jsonl in order (the last line per id is the latest) and adaptations.jsonl for the element ids.

  python3 out/_analysis/d3_pair_kind_check.py [--elements R01,P01,...]
"""
import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--elements", default="", help="limit the report to lines touching these elements")
    a = ap.parse_args()
    els = {e for e in a.elements.split(",") if e}
    meta = {}
    for ln in open("out/adaptations.jsonl", encoding="utf-8"):
        if ln.strip():
            x = json.loads(ln)
            meta[x["id"]] = (x.get("element"), x.get("op"))
    latest = {}
    for ln in open("out/adjudications.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            latest[r["adaptation"]] = r
    bad = []
    n = 0
    for i, r in latest.items():
        if r.get("decision") != "accept" or r.get("kind") != "elaboration":
            continue
        el, op = meta.get(i, (None, None))
        if els and el not in els:
            continue
        n += 1
        p = r.get("pair")
        pr = latest.get(p)
        if not p or pr is None:
            bad.append((i, el, op, p, "pair not ruled"))
        elif not (pr.get("decision") == "accept" and pr.get("kind") == "elaboration"):
            pel, pop = meta.get(p, (None, None))
            bad.append((i, el, op, p, f"pair now {pr.get('decision')}/{pr.get('kind')} ({pel} {pop}, ruled {pr.get('leg')})"))
    print(f"accepted elaborations checked: {n}; with a pair that is no longer an accepted elaboration: {len(bad)}")
    for b in sorted(bad, key=lambda b: (str(b[1]), b[0])):
        print(" | ".join(str(x) for x in b))


if __name__ == "__main__":
    main()
