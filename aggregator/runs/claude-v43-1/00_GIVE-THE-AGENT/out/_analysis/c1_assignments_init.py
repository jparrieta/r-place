#!/usr/bin/env python3
"""C1a-01: write assignments_final.jsonl from assign_final.jsonl with J's class 2 ruling applied (J, 13 October 2026,
20:16 Berlin, through the PI's message of 18:17Z; notes-C1.md, "Class 2: J's ruling applied").

Every line of assign_final.jsonl is carried through verbatim, except the class 2 lines (source "b1_grouping_kept"):
  third_order       becomes the two B3 readers' list (b3_classes.jsonl r1; the script stops unless r1 == r2)
  support_by_theme  kept; the script stops unless its keys are the readers' list
  also_present      kept
  b1_themes_without_reader_support   kept: the flagged record J ruled (the B1 themes no reader placed); the script
                    stops unless it equals the settled themes the readers' list leaves out
  source            becomes "readers"
  moves             gains one entry as mem.py reassign writes one: from, to, stage C1, leg, t, why, support

Writes (dry run without --write): out/assignments_final.jsonl (refused if it exists), out/assign_revisions_only.jsonl
(the changed lines), out/assignments_final.count.txt (the line count), out/_analysis/c1_class2.json (the record).

    python3 out/_analysis/c1_assignments_init.py [--write]
"""
import collections, datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
SETTLED = "d3506a8871eeb106d934824e342acb374931501c2b4dd377cc277094624bcd6b"
WHY = ("J, 13 October 2026, 20:16 Berlin (the PI's message of 18:17Z), class 2: the readers' list stands as the "
       "placement; the B1 themes no reader placed are kept as a flagged record (b1_themes_without_reader_support), "
       "not as placements")


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def main():
    p = os.path.join(OUT, "assign_final.jsonl")
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != SETTLED:
        sys.exit("assign_final.jsonl is not the settled line of B4a-07")
    if os.path.exists(os.path.join(OUT, "assignments_final.jsonl")):
        sys.exit("out/assignments_final.jsonl exists")
    rows = jl("assign_final.jsonl")
    cls = {(c["sub"], c["theme_id"]): c for c in jl("b3_classes.jsonl")}
    leg = open(os.path.join(ROOT, ".leg")).read().strip()
    t = datetime.datetime.utcnow().isoformat(timespec="seconds")
    out, changed, bad = [], [], []
    flagged_n = collections.Counter()
    for r in rows:
        k = (r["sub"], r["theme_id"])
        if r.get("confidence") not in ("clear", "arguable") or r.get("read") not in ("whole", "theme-block"):
            bad.append("%s/%s: confidence %r read %r" % (k[0], k[1], r.get("confidence"), r.get("read")))
        if r.get("source") != "b1_grouping_kept":
            out.append(r)
            continue
        c = cls[k]
        if c["class"] != 2 or c["r1"] != c["r2"] or not c["r1"]:
            bad.append("%s/%s: not class 2 with equal readers' lists" % k)
            continue
        readers = list(c["r1"])
        sup = r.get("support_by_theme") or {}
        if set(sup) != set(readers) or any(not v for v in sup.values()):
            bad.append("%s/%s: support keys %s are not the readers' list %s" % (k[0], k[1], sorted(sup), readers))
            continue
        flagged = [x for x in r["third_order"] if x not in readers]
        if sorted(flagged) != sorted(r.get("b1_themes_without_reader_support") or []):
            bad.append("%s/%s: flagged %s against the record %s" % (k[0], k[1], flagged, r.get("b1_themes_without_reader_support")))
            continue
        if any(x not in r["third_order"] for x in readers):
            bad.append("%s/%s: a reader's theme is not in the settled line" % k)
            continue
        n = dict(r)
        n["third_order"] = readers
        n["source"] = "readers"
        n["moves"] = list(r.get("moves") or []) + [{"from": r["third_order"], "to": readers, "stage": "C1", "leg": leg,
                                                    "t": t, "why": WHY, "support": sup}]
        out.append(n)
        changed.append(n)
        flagged_n[len(flagged)] += 1
    print("lines %d; class 2 changed %d; flagged B1 themes per changed line %s; problems %d" % (
        len(out), len(changed), dict(sorted(flagged_n.items())), len(bad)))
    for b in bad[:20]:
        print("  PROBLEM " + b)
    if bad:
        sys.exit("stopped: %d problems" % len(bad))
    keys = {(r["sub"], r["theme_id"]) for r in out}
    if len(keys) != len(rows) or len(out) != len(rows):
        sys.exit("the key count changed")
    print("example: %s" % json.dumps({x: changed[0][x] for x in ("sub", "theme_id", "third_order", "source",
                                                               "b1_themes_without_reader_support")}, ensure_ascii=False))
    if "--write" not in sys.argv:
        return
    with open(os.path.join(OUT, "assignments_final.jsonl"), "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(OUT, "assign_revisions_only.jsonl"), "w", encoding="utf-8") as f:
        for r in changed:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(os.path.join(OUT, "assignments_final.count.txt"), "w", encoding="utf-8").write("%d\n" % len(out))
    json.dump({"rule": WHY, "leg": leg, "t": t, "lines": len(out), "class2_changed": len(changed),
               "flagged_per_line": dict(sorted(flagged_n.items())), "flagged_total": sum(k * v for k, v in flagged_n.items()),
               "settled_sha256": SETTLED,
               "assignments_final_sha256": hashlib.sha256(open(os.path.join(OUT, "assignments_final.jsonl"), "rb").read()).hexdigest(),
               "script": "out/_analysis/c1_assignments_init.py"},
              open(os.path.join(OUT, "_analysis", "c1_class2.json"), "w", encoding="utf-8"), indent=1)
    print("wrote assignments_final.jsonl (%d), assign_revisions_only.jsonl (%d), assignments_final.count.txt"
          % (len(out), len(changed)))


if __name__ == "__main__":
    main()
