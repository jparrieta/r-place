#!/usr/bin/env python3
"""B4a-05: print, for the bags that J's also_present ruling (13 October, 09:09 Berlin) leaves with no also_present
theme, the item's blind chunk section whole (concepts, readings A and B, my B1 grouping) and the old ruled line
(ruling, concepts per theme, also_present, taxonomy, why). Read-only.

    python3 out/_analysis/b4_ap_emptied_show.py --packet 3 [--items 42,144]
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--items")
    a = ap.parse_args()
    ep = os.path.join(OUT, "_adjudication-B4", "rerule-ap-B4a-05", "emptied-ap%02d.jsonl" % a.packet)
    want = [d["n"] for d in jl(ep)]
    if a.items:
        want = [int(x) for x in a.items.split(",")]
    old = {d["n"]: d for d in jl(os.path.join(OUT, "disagreements.jsonl")) if d.get("packet") == a.packet}
    pdir = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet)
    for n in want:
        ch = os.path.join(pdir, "chunk-%02d.md" % ((n - 1) // 25 + 1))
        lines = open(ch, encoding="utf-8").read().splitlines()
        head = "### %d. " % n
        sec, on = [], False
        for ln in lines:
            if ln.startswith("### "):
                on = ln.startswith(head)
            if on:
                sec.append(ln)
        print("\n".join(sec).rstrip())
        d = old[n]
        print("\n**Old ruling (%s, leg %s):** %s | %s | named_neither %s" % (
            d["taxonomy"], d.get("leg"), d["ruling"], d.get("boundary_ruling"), d["named_neither"]))
        for t, v in d["support_by_theme"].items():
            print("- support %s: %s" % (t, " ".join(v)))
        for t, v in (d.get("also_present") or {}).items():
            print("- also_present %s: %s" % (t, " ".join(v)))
        print("- quote: %s" % d.get("quote"))
        print("- why: %s\n" % d.get("why"))


if __name__ == "__main__":
    main()
