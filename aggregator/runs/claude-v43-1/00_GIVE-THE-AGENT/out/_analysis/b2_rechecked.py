#!/usr/bin/env python3
"""B2 check legs: the author's placements after the rechecks, for fidelity's second figure.

For each item of author_items.jsonl: the `now` of its latest record in rechecks-B2.jsonl (by time), else
its own third_order. Reports items whose records disagree with each other (one decision per item is the
rule). Writes out/_analysis/b2_rechecked_author.jsonl (sub, theme_id, item, third_order, moved, from).
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


def main():
    recs = collections.defaultdict(list)
    for r in jl(os.path.join(OUT, "rechecks-B2.jsonl")):
        if r.get("source") == "author_items.jsonl":
            recs["%s/%s" % (r["sub"], r["theme_id"])].append(r)
    rows, moved, mixed = [], 0, []
    for a in jl(os.path.join(OUT, "author_items.jsonl")):
        it = a["item"]
        rs = sorted(recs.get(it, []), key=lambda r: r["t"])
        now = rs[-1]["now"] if rs else a["third_order"]
        if len({tuple(r["now"]) for r in rs}) > 1:
            mixed.append((it, sorted({",".join(r["now"]) for r in rs})))
        m = set(now) != set(a["third_order"])
        moved += m
        rows.append({"sub": a["sub"], "theme_id": a["theme_id"], "item": it, "third_order": now, "moved": m,
                     "from": a["third_order"], "records": len(rs)})
    with open(os.path.join(OUT, "_analysis", "b2_rechecked_author.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("%d items, %d moved by their rechecks, %d with records that disagree%s" % (
        len(rows), moved, len(mixed), (": %s" % mixed) if mixed else ""))


if __name__ == "__main__":
    main()
