#!/usr/bin/env python3
"""E1 section 1, logs against claims (E1b-01): every id in the views, resolved as links.py resolves the head's and the
questions' ids. links.py reads only _head.md and _questions/*.md, so this applies its own resolver (tools/links.py's
known() and its patterns, imported, not rewritten) to every text file of out/_views/. Prints JSON.

    python3 out/audit-E1/links_views.py > out/audit-E1/links_views.json

The rule, declared before the run (E1b-01): the files are out/_views/* with the endings .md, .tsv, .txt, .json, .nwk;
for each, the ids links.py's patterns find (element, arrow, theme, dimension, finding, family, branch, proposition
ids; r/ rooms; <sub>/cNNNN concepts; <sub>/tNN themes), counted, and those that do not resolve listed with their
counts. An id links.py's patterns catch that is not an id of the model (a stage name such as D3 written bare) is listed
as unresolved and read in the audit section.
"""
import collections, glob, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "out")


def main():
    spec = importlib.util.spec_from_file_location("links", os.path.join(ROOT, "tools", "links.py"))
    L = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(L)
    rooms, named, codes, themes, ids = L.known(ROOT, OUT)
    low_rooms = {r.lower(): r for r in rooms}
    low_named = {n.lower() for n in named} | set(low_rooms)
    res = {}
    for p in sorted(glob.glob(os.path.join(OUT, "_views", "**", "*"), recursive=True)):
        if not os.path.isfile(p) or not p.endswith((".md", ".tsv", ".txt", ".json", ".nwk")):
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        found, miss = 0, collections.Counter()
        for m in L.IDS.findall(txt):
            found += 1
            if m not in ids:
                miss[m] += 1
        for m in L.ROOM.findall(txt):
            found += 1
            if m.lower() not in low_named:
                miss["r/" + m] += 1
        for sub, cid in L.CONCEPT.findall(txt):
            found += 1
            if sub.lower() in low_rooms and (low_rooms[sub.lower()], cid) not in codes:
                miss["%s/%s" % (sub, cid)] += 1
            elif sub.lower() not in low_rooms and sub.lower() not in ("r", "http", "https"):
                miss["%s/%s (no such room)" % (sub, cid)] += 1
        for sub, tid in L.THEME.findall(txt):
            found += 1
            if sub.lower() in low_rooms and (low_rooms[sub.lower()], tid) not in themes:
                miss["%s/%s" % (sub, tid)] += 1
            elif sub.lower() not in low_rooms:
                miss["%s/%s (no such room)" % (sub, tid)] += 1
        res[os.path.relpath(p, OUT)] = {"ids_found": found, "unresolved": sum(miss.values()),
                                        "unresolved_ids": dict(miss.most_common(15))}
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "files": len(res), "ids_found": sum(r["ids_found"] for r in res.values()),
                      "unresolved": sum(r["unresolved"] for r in res.values()),
                      "files_with_unresolved": {k: v for k, v in res.items() if v["unresolved"]},
                      "per_file": res}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
