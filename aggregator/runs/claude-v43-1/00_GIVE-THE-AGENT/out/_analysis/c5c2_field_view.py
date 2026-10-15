#!/usr/bin/env python3
"""C5c-02: read the field analyst's return (sources-from-J/RETURN-field-C5.jsonl) declaration by declaration. For each
declaration given: every sentence it marked as not standing, with the sentence's text as the package served it
(field-packages-C5/, built at C5c-01, before Stigmergy's recut), its kind, what it rests on and why; then its note on
the declaration. Also marks the sentences the fleet readers judged (c5b_in_question.json texts, matched by text).
Reads only; writes nothing.

    python3 out/_analysis/c5c2_field_view.py T4-007 D02 ...   [--all] (--all shows standing sentences too)
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
text = {}
for p in glob.glob(os.path.join(OUT, "field-packages-C5", "0[2-9]-*.md")):
    for l in open(p, encoding="utf-8"):
        m = re.match(r"- `([A-Z0-9-]+\.[a-z_]+\.\d+)` (.*)$", l.rstrip("\n"))
        if m:
            text[m.group(1)] = m.group(2)
fleet = []
for k in (1, 2, 3):
    r = json.loads(open(os.path.join(OUT, "readers-C5", "C5-reader-%d.jsonl" % k)).read().strip().splitlines()[0])
    fleet += r["declarations"]
rows = [json.loads(l) for l in open(os.path.join(OUT, "sources-from-J", "RETURN-field-C5.jsonl"), encoding="utf-8")
        if l.strip().startswith("{")]
want = [a for a in sys.argv[1:] if not a.startswith("--")]
for d in want:
    print("=" * 8, d)
    for r in rows:
        if "sentence" in r and r["sentence"].split(".")[0] == d and ("--all" in sys.argv or not r["stands"]):
            t = text.get(r["sentence"], "?")
            fl = [f for f in fleet if f["sentence"].strip()[:60] in t or t[:60] in f["sentence"]]
            tag = (" [fleet: %s]" % ("stands" if fl[0]["stands"] else "does not stand")) if fl else ""
            print("- %s (%s, %s)%s: %s" % (r["sentence"], r["kind"], "stands" if r["stands"] else "NOT", tag, t))
            print("    rests_on %s | why: %s" % (r.get("rests_on"), r["why"]))
    for r in rows:
        if r.get("declaration") == d:
            print("  NOTE: %s" % r["note"])
