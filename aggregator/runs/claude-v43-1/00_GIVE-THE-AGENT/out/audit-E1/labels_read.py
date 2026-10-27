#!/usr/bin/env python3
"""E1 section 1, logs against claims, fifth pass (E1b-01): the uncited and item-cited quote spans of the analyst's .md
files that quotes_resolve.py resolved to a label or note (3,627 uncited and 2 item-cited at E1a). The stage counts a
quote that resolves to a label as a defect; this pass says which label field each span is, where it sits, and draws
a sample to read by hand, so that a label quoted as a label can be told from a label passed off as someone's words.
Prints JSON.

    python3 out/audit-E1/labels_read.py > out/audit-E1/labels_read.json

The rule, declared before the run (E1b-01):
- The spans, the files and the resolution are quotes_resolve.py's own (imported, not rewritten): .md files only, a span
  of five words or more or one cited by item id, not found in any concept's words and found in a label or note.
- Each span gets: the label field that holds it (first_order, second_order, note, theme_note; the first key
  found), whether it sits on a JSON line or in a json fence (unresolved_read.py's test, imported), and its file group.
- A sample of 25 spans not on a JSON line, drawn with random.Random(int(out/seed.txt, 16)), is printed with its line,
  to be read by hand: is the label named as a label (a theme or concept by name, in the analyst's voice), or set out
  as what a participant said?
"""
import collections, glob, importlib.util, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "out")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    qr, ur = load("quotes_resolve"), load("unresolved_read")
    codes = qr.jl(os.path.join(ROOT, "package", "store", "codes.jsonl"))
    themes = qr.jl(os.path.join(ROOT, "package", "store", "themes.jsonl"))
    words = qr.Index([("%s/%s" % (c["sub"], c["code_id"]), c.get("text") or "") for c in codes])
    labels = qr.Index([("%s/%s:%s" % (c["sub"], c["code_id"], f), c.get(f) or "") for c in codes
                       for f in ("first_order", "second_order", "note") if c.get(f)] +
                      [("%s/%s:theme_note" % (t["sub"], t["theme_id"]), t.get("theme_note") or "") for t in themes])
    recs = []
    for p in sorted(glob.glob(os.path.join(OUT, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, OUT)
        if qr.SKIP.match(rel):
            continue
        for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            for _s, e, span in qr.quotes(line):
                tail = qr.tail_of(line, e)
                if qr.CITE_C.match(tail):
                    continue
                mi = qr.CITE_I.match(tail)
                if not mi and len(qr.TOK.findall(span.lower())) < 5:
                    continue
                if words.find(span)[0]:
                    continue
                lvl, hits = labels.find(span)
                if not lvl:
                    continue
                field = hits[0].rsplit(":", 1)[1]
                recs.append({"file": rel, "line": n, "quote": span, "item_cited": bool(mi), "field": field,
                             "held_by": hits[:2], "json": ur.in_json(p, n),
                             "group": re.sub(r"\d+", "N", rel.split("/")[0])})
    prose = [r for r in recs if not r["json"]]
    seed = open(os.path.join(OUT, "seed.txt")).read().split()[0]
    sample = random.Random(int(seed, 16)).sample(prose, min(25, len(prose)))
    for r in sample:
        r["line_text"] = open(os.path.join(OUT, r["file"]), encoding="utf-8", errors="replace").read().split("\n")[r["line"] - 1][:700]
    by_group = collections.defaultdict(collections.Counter)
    for r in recs:
        by_group[r["group"]]["json" if r["json"] else "prose"] += 1
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "spans": len(recs), "item_cited": [r for r in recs if r["item_cited"]],
                      "by_field": dict(collections.Counter(r["field"] for r in recs)),
                      "json": sum(r["json"] for r in recs), "prose": len(prose),
                      "prose_by_field": dict(collections.Counter(r["field"] for r in prose)),
                      "by_group": {k: dict(v) for k, v in sorted(by_group.items(), key=lambda kv: -sum(kv[1].values()))},
                      "seed": seed, "sample": sample, "all": recs}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
