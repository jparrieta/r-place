#!/usr/bin/env python3
"""C1, read-only: the rulings of disagreements.jsonl whose why rests on "the earlier reading" (the B4a-06 re-rule
under the lone-B1 rule: "the readers' theme takes no concept by the earlier reading, so no placement stands"), with
their class, readers, my B1 grouping, the ruling and the fresh readings of B4c where the item was in the blind sample.
Prints only.

    python3 out/_analysis/c1_earlier_reading.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    cls = {(c["sub"], c["theme_id"]): c for c in jl("b3_classes.jsonl")}
    fresh = collections.defaultdict(list)
    for name in ("reassign.jsonl", "reassign-openai-astra.jsonl", "readings-R-B4.jsonl"):
        for x in jl(name):
            fresh[(x["sub"], x["theme_id"])].append("%s%s:%s" % ("A1" if x["arm"].startswith("deepseek") else "A2",
                                                                  "R" if x.get("stratum") == "R" else "",
                                                                  ",".join(x["third_order"])))
    rows = [d for d in jl("disagreements.jsonl") if "earlier reading" in str(d.get("why") or "")]
    print("rulings resting on the earlier reading: %d; by class %s; unresolved %d" % (
        len(rows), dict(collections.Counter(cls[(d["sub"], d["theme_id"])]["class"] for d in rows)),
        sum(1 for d in rows if d.get("unresolved"))))
    for d in sorted(rows, key=lambda d: (d["sub"].lower(), d["theme_id"])):
        k = (d["sub"], d["theme_id"])
        c = cls[k]
        print("%s/%s\tclass %s\treaders %s | %s\tB1 %s\truling %s%s\tpacket %s\tfresh %s" % (
            k[0], k[1], c["class"], ",".join(c["r1"] or []), ",".join(c["r2"] or []), ",".join(c["b1"] or []),
            ",".join(d.get("ruling") or []) or "-", " (unresolved)" if d.get("unresolved") else "", d.get("packet"),
            " ".join(fresh.get(k, [])) or "-"))


if __name__ == "__main__":
    main()
