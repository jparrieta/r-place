#!/usr/bin/env python3
"""links.py, v38: every id named in _head.md and _questions/*.md resolves to something that exists.

    python3 tools/links.py [--root .] [--out out]

What it resolves:
  a third- or fourth-order theme, a dimension, an element, an arrow, a finding, a family, a branch,
  an adaptation id, a question slug                          against out/
  a room, written r/<sub> or <sub>/...                       against the store's rooms.jsonl; a
                                                             room the rooms named (pointers,
                                                             relations) and r/place also resolve
  a first-order concept, <sub>/cNNNN or <sub>:cNNNN          against the store's codes.jsonl
  a second-order theme, <sub>/tNN                            against the store's themes.jsonl

Exit 1 and list the unresolved ids otherwise. validate.py --open runs it at every leg's open.
"""
import argparse, json, os, re, sys

IDS = re.compile(r"\b(T3-\d{3}|T4-\d{3}|D\d{1,2}|P\d{2,3}|K\d{2,3}|C\d{2,3}|R\d{2,3}|A\d{2,3}|F\d{2,3}|F-\d{3}|FP-\d{2,3}|N\d{2,3})\b")
ROOM = re.compile(r"(?<![\w/.])/?r/([A-Za-z0-9_]{2,})\b")
CONCEPT = re.compile(r"(?<![\w/.])([A-Za-z0-9_]{2,})[/:](c\d{4})\b")
THEME = re.compile(r"(?<![\w/.])([A-Za-z0-9_]{2,})/(t\d{2,3})\b")


def jl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def known(root, out):
    S = os.path.join(root, "package", "store")
    rooms = {r["sub"] for r in jl(os.path.join(S, "rooms.jsonl"))}
    named = {"place"}
    for p in jl(os.path.join(S, "pointers.jsonl")):
        n = (p.get("normalised") or "").strip()
        if n.lower().startswith("r/"):
            named.add(n[2:])
    for r in jl(os.path.join(S, "relations.jsonl")):
        if r.get("other"):
            named.add(r["other"])
    codes = {(c["sub"], c["code_id"]) for c in jl(os.path.join(S, "codes.jsonl"))}
    themes = {(t["sub"], t["theme_id"]) for t in jl(os.path.join(S, "themes.jsonl"))}
    ids = set()
    for d in ("", "scheme"):
        for f in ("scheme_v2.jsonl", "scheme_final.jsonl", "scheme.jsonl", "scheme_current.jsonl"):
            ids |= {r.get("id") or r.get("theme") for r in jl(os.path.join(out, d, f))}
    for f in ("assignments_final.jsonl", "assign_final.jsonl"):
        for r in jl(os.path.join(out, f)):
            so = r.get("third_order")
            ids |= set(so if isinstance(so, list) else [so])
    for f in (("fourth", "fourth.jsonl"), ("dimensions.jsonl",), ("model", "elements.jsonl"),
              ("model", "arrows.jsonl"), ("findings.jsonl",), ("adaptations.jsonl",), ("branches.jsonl",)):
        ids |= {r.get("id") for r in jl(os.path.join(out, *f))}
    ids |= {r.get("family") for r in jl(os.path.join(out, "families.jsonl"))}
    ids |= {r.get("theme") for r in jl(os.path.join(out, "theme_discovery.jsonl"))}
    qd = os.path.join(out, "_questions")
    ids |= {f[:-3] for f in os.listdir(qd)} if os.path.isdir(qd) else set()
    ids.discard(None)
    return rooms, named, codes, themes, ids


def run(root=".", out=None, quiet=False):
    out = out or os.path.join(root, "out")
    rooms, named, codes, themes, ids = known(root, out)
    low_rooms = {r.lower(): r for r in rooms}
    low_named = {n.lower() for n in named} | set(low_rooms)
    files = []
    hp = os.path.join(out, "_head.md")
    if os.path.exists(hp):
        files.append(hp)
    qd = os.path.join(out, "_questions")
    if os.path.isdir(qd):
        files += sorted(os.path.join(qd, f) for f in os.listdir(qd) if f.endswith(".md"))
    bad = {}
    for f in files:
        txt = open(f, encoding="utf-8").read()
        miss = bad.setdefault(os.path.relpath(f, out), set())
        for m in IDS.findall(txt):
            if m not in ids:
                miss.add(m)
        if rooms:
            for m in ROOM.findall(txt):
                if m.lower() not in low_named:
                    miss.add("r/" + m)
            for sub, cid in CONCEPT.findall(txt):
                if sub.lower() in low_rooms and (low_rooms[sub.lower()], cid) not in codes:
                    miss.add("%s/%s" % (sub, cid))
                elif sub.lower() not in low_rooms and sub.lower() not in ("r", "http", "https"):
                    miss.add("%s/%s (no such room)" % (sub, cid))
            for sub, tid in THEME.findall(txt):
                if sub.lower() in low_rooms and (low_rooms[sub.lower()], tid) not in themes:
                    miss.add("%s/%s" % (sub, tid))
                elif sub.lower() not in low_rooms:
                    miss.add("%s/%s (no such room)" % (sub, tid))
    bad = {k: v for k, v in bad.items() if v}
    if bad:
        for f, s in sorted(bad.items()):
            print("%s: unresolved %s" % (f, ", ".join(sorted(s))))
        return 1
    if not quiet:
        print("links: %d files checked, all ids resolve%s" % (
            len(files), "" if rooms else " (no rooms.jsonl: room and concept names were not checked)"))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    return run(a.root, a.out)


if __name__ == "__main__":
    sys.exit(main())
