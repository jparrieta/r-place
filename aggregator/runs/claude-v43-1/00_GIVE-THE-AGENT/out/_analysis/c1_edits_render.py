#!/usr/bin/env python3
"""C1, read-only: scheme_edits.jsonl rendered one line per edit, for reading whole (notes-C1.md, "How
scheme_edits.jsonl is read"). Each line: number, round, leg, theme, field, kind, the items that caused it, the asks
named, the sentence added (or, where a line has no `added`, the field as it now reads, marked "now:"), and the why.
The duplicated "was" copy of the whole field is left out. Prints a page.

    python3 out/_analysis/c1_edits_render.py [--from N] [--to M]
"""
import argparse, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def show(v):
    if isinstance(v, dict):
        return "vs %s: %s" % (v.get("vs"), v.get("question")) if "vs" in v else json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return " || ".join(show(x) for x in v)
    return " ".join(str(v).split())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--from", dest="lo", type=int, default=1)
    ap.add_argument("--to", dest="hi", type=int, default=10**6)
    a = ap.parse_args()
    rows = [json.loads(x) for x in open(os.path.join(OUT, "scheme_edits.jsonl"), encoding="utf-8") if x.strip()]
    for r in rows:
        if not a.lo <= r.get("n", 0) <= a.hi:
            continue
        body = ("added: " + show(r["added"])) if "added" in r else ("now: " + show(r.get("now")))
        print("%s r%s %s %s.%s [%s] by %s%s | %s | why: %s" % (
            r.get("n"), r.get("round"), r.get("leg"), r.get("theme"), r.get("field"), r.get("kind"),
            ",".join(r.get("caused_by") or []) or "-", (" asks " + ",".join(r["asks"])) if r.get("asks") else "",
            body, " ".join(str(r.get("why") or "").split())))
    print("[lines %d to %d of %d]" % (a.lo, min(a.hi, len(rows)), len(rows)))


if __name__ == "__main__":
    main()
