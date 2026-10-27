#!/usr/bin/env python3
"""E1 section 1, the store's figures recomputed: README-store.md's build figures, stage A1's recomputation
(out/notes-A1.md, "The store against the package" and the paragraphs before it), and a recomputation now from the
store's files and the forest headers of trees/. Three columns; a difference is a defect.

    python3 out/audit-E1/store_figures.py > out/audit-E1/store_figures.tsv

The README and A1 figures are read from the two texts by the patterns below (never typed); "-" where a text gives none.
"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ST = os.path.join(ROOT, "package", "store")


def n(s):
    return int(s.replace(",", "")) if s else None


def grab(text, pat, k=1):
    m = re.search(pat, text, re.S)
    return n(m.group(k)) if m else None


def lines(p):
    return sum(1 for l in open(p, encoding="utf-8") if l.strip())


def main():
    rd = open(os.path.join(ST, "README-store.md"), encoding="utf-8").read()
    a1 = open(os.path.join(ROOT, "out", "notes-A1.md"), encoding="utf-8").read()
    codes = [json.loads(l) for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8")]
    items, item_lines, states = set(), 0, {}
    for l in open(os.path.join(ST, "items.jsonl"), encoding="utf-8"):
        if not l.strip():
            continue
        r = json.loads(l)
        items.add((r["sub"], r["item_id"]))
        item_lines += 1
        states[r.get("state")] = states.get(r.get("state"), 0) + 1
    forest = {"threads": 0, "items": 0, "coded": 0, "bridge": 0, "removed": 0, "dropped": 0}
    for p in glob.glob(os.path.join(ROOT, "trees", "*.md")):
        head = "".join(open(p, encoding="utf-8").readlines()[:5])
        m = re.search(r"# threads given (\d+)", head)
        forest["threads"] += int(m.group(1)) if m else 0
        m = re.search(r"# items (\d+): coded (\d+), bridge (\d+), removed (\d+), dropped (\d+)", head)
        if m:
            for k, v in zip(("items", "coded", "bridge", "removed", "dropped"), m.groups()):
                forest[k] += int(v)
    build = json.load(open(os.path.join(ST, "_build.json"), encoding="utf-8"))
    unjoined_now = sum(1 for c in codes if (c["sub"], c["item_id"]) not in items)
    a1b = re.search(r"Communities (\d+), codes ([\d,]+), themes ([\d,]+), threads ([\d,]+), items ([\d,]+), coded items "
                    r"([\d,]+), bridge items ([\d,]+), pointers ([\d,]+), briefs (\d+)", a1)
    a1f = re.search(r"Items ([\d,]+): coded ([\d,]+), bridge ([\d,]+), removed ([\d,]+), dropped ([\d,]+)", a1)
    rows = [
        ("rooms", grab(rd, r"room \((\d+)\)"), grab(a1, r"N = (\d+)"),
         len({c["sub"] for c in codes}), "distinct rooms in codes.jsonl; rooms.jsonl lines %d" % lines(os.path.join(ST, "rooms.jsonl"))),
        ("concepts", grab(rd, r"first-order concept \((\d+);"), grab(a1, r"`store/codes.jsonl` has ([\d,]+) lines"),
         len(codes), "codes.jsonl lines"),
        ("retracted, dropped", grab(rd, r"(\d+) retracted by the coder and dropped"), grab(a1, r"`store/_retracted.jsonl` has (\d+) lines"),
         lines(os.path.join(ST, "_retracted.jsonl")), "_retracted.jsonl lines; _build.json %s" % build.get("codes_retracted_dropped")),
        ("second-order themes", grab(rd, r"second-order theme \((\d+)\)"), grab(a1, r"Second-order themes: ([\d,]+) in total"),
         lines(os.path.join(ST, "themes.jsonl")), "themes.jsonl lines"),
        ("unjoined concepts", grab(rd, r"forest does not hold \((\d+)\)"), grab(a1, r"`_unjoined.jsonl` holds (\d+) lines"),
         unjoined_now, "concepts whose item items.jsonl lacks; _unjoined.jsonl lines %d" % lines(os.path.join(ST, "_unjoined.jsonl"))),
        ("items in the store", grab(rd, r"item of a coded thread \((\d+);"), n(a1b.group(5)) if a1b else None,
         item_lines, "items.jsonl lines (%d distinct sub and item id); states %s" % (len(items), json.dumps(states, sort_keys=True))),
        ("threads in the store", grab(rd, r"coded thread \((\d+)\)"), n(a1b.group(4)) if a1b else None,
         lines(os.path.join(ST, "threads.jsonl")), "threads.jsonl lines"),
        ("pointers", grab(rd, r"pointer the coder wrote \((\d+)\)"), n(a1b.group(8)) if a1b else None,
         lines(os.path.join(ST, "pointers.jsonl")), "pointers.jsonl lines"),
        ("briefs", grab(rd, r"pre-event brief \((\d+) present\)"), n(a1b.group(9)) if a1b else None,
         len(glob.glob(os.path.join(ROOT, "package", "*", "brief.md"))), "package/<sub>/brief.md files"),
        ("transitions", grab(rd, r"coded turn: (\d+) lines"), None,
         lines(os.path.join(ST, "transitions.jsonl")), "transitions.jsonl lines"),
        ("forest: threads given", None, grab(a1, r"([\d,]+) threads given"), forest["threads"], "sum of trees/ headers"),
        ("forest: items", None, n(a1f.group(1)) if a1f else None, forest["items"], "sum of trees/ headers"),
        ("forest: coded", None, n(a1f.group(2)) if a1f else None, forest["coded"], "sum of trees/ headers"),
        ("forest: bridge", None, n(a1f.group(3)) if a1f else None, forest["bridge"], "sum of trees/ headers"),
        ("forest: removed", None, n(a1f.group(4)) if a1f else None, forest["removed"], "sum of trees/ headers"),
        ("forest: dropped", None, n(a1f.group(5)) if a1f else None, forest["dropped"], "sum of trees/ headers"),
    ]
    print("figure\tREADME-store.md\tA1 (notes-A1.md)\tnow\tagree\thow now is computed")
    for name, r, a, now, how in rows:
        given = [x for x in (r, a) if x is not None]
        agree = "yes" if given and all(x == now for x in given) else ("-" if not given else "NO")
        print("%s\t%s\t%s\t%s\t%s\t%s" % (name, "-" if r is None else r, "-" if a is None else a, now, agree, how))


if __name__ == "__main__":
    sys.exit(main())
