#!/usr/bin/env python3
"""B4a-06, after J's answer to QB4-003 (11:29 Berlin): themes a reader listed under its own also_present count in
the bag test. Read-only view of the ruled lines b4_bag_named_check.py lists, for re-ruling them by hand.

    python3 out/_analysis/b4_bag_view.py --packet 5 --items 3,44,51

For each item: the chunk's heading, the readings and my B1 as the packet shows them, the ruling now in
disagreements.jsonl (themes, concepts, also_present), each named-only theme with the concepts its readers listed
that the ruling does not use (label and words), and the item's other concepts the ruling does not use (label only).
"""
import argparse
import collections
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", type=int, required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--brief", action="store_true", help="omit the unused concepts' labels")
    a = ap.parse_args()
    want = [int(x) for x in a.items.split(",") if x.strip()]
    pdir = os.path.join(OUT, "_adjudication-B4", "packet-%02d" % a.packet)
    idx = {}
    for ln in open(os.path.join(pdir, "index.tsv"), encoding="utf-8").read().splitlines()[1:]:
        n, key, cl, ch, arep = ln.split("\t")
        idx[int(n)] = (key, int(ch))
    raw = collections.defaultdict(lambda: collections.defaultdict(set))
    for x in jl(os.path.join(OUT, "assign_raw.jsonl")):
        if x.get("copy_kind") != "corpus":
            continue
        apd = x.get("also_present") or {}
        if isinstance(apd, dict):
            for t, cs in apd.items():
                raw["%s/%s" % (x["sub"], x["theme_id"])][t] |= set(cs or [])
    led = {}
    for d in jl(os.path.join(OUT, "disagreements.jsonl")):
        if d.get("packet") == a.packet:
            led[d["n"]] = d
    chunks = {}
    for n in want:
        key, ch = idx[n]
        if ch not in chunks:
            chunks[ch] = open(os.path.join(pdir, "chunk-%02d.md" % ch), encoding="utf-8").read()
        text = chunks[ch]
        m = re.search(r"^### %d\. .*?(?=^### |\Z)" % n, text, re.S | re.M)
        block = m.group(0) if m else ""
        concepts = {}
        other = []
        for ln in block.splitlines():
            mm = re.match(r"- (c\d{4}) \| (.*?) \| (.*)$", ln)
            if mm:
                concepts[mm.group(1)] = (mm.group(2), mm.group(3))
            elif ln.strip() and not ln.startswith("- c"):
                other.append(ln)
        d = led.get(n)
        print("=" * 20)
        print(other[0] if other else "### %d" % n)
        for ln in other[1:]:
            print(ln)
        if not d:
            print("NOT IN LEDGER")
            continue
        placed = set(d["readers"][0]) | set(d["readers"][1]) | set(d.get("b1") or [])
        sup = d.get("support_by_theme") or {}
        apd = d.get("also_present") or {}
        used = set()
        for cs in list(sup.values()) + list(apd.values()):
            used |= set(cs)
        print("LEDGER: taxonomy %s | ruling %s | sup %s | ap %s" % (d["taxonomy"], d["ruling"],
              {t: len(v) for t, v in sup.items()}, {t: len(v) for t, v in apd.items()}))
        print("SUP:", json.dumps(sup))
        if apd:
            print("AP:", json.dumps(apd))
        print("BR: %s | Q: %s | CONF: %s" % (d.get("boundary_ruling"), d.get("quote"), d.get("confidence")))
        print("WHY:", d.get("why"))
        for t, cs in sorted(raw[key].items()):
            if t in placed or t in apd:
                continue
            free = sorted(set(cs) - used)
            print("NAMED-ONLY %s: reader-listed %d, free %d" % (t, len(cs), len(free)))
            for c in free:
                lab, q = concepts.get(c, ("?", "?"))
                print("   %s | %s | %s" % (c, lab, q))
        rest = [c for c in sorted(concepts) if c not in used]
        print("UNUSED (%d)%s" % (len(rest), ":" if not a.brief else ""))
        if not a.brief:
            for c in rest:
                print("   %s | %s" % (c, concepts[c][0]))


if __name__ == "__main__":
    main()
