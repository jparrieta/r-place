#!/usr/bin/env python3
"""B4b-p3: stratum R becomes all 185 unresolved rulings (J, 17:10 Berlin; notes-B4.md, "Stratum R, all 185 unresolved
items"). No draw: every unresolved item is taken.

  the 18 drawn at B4b-p2   kept as they are, orders 501..518, read in S05-35 and S05-36
  the 149 added            the unresolved items neither sample-B4-R.jsonl nor sample-B4.jsonl holds, sorted by
                           (room, theme id), served in the order random.Random("20261013:R-all-order").shuffle gives,
                           orders 519..667
  the 18 in U and A        counted in R from the same readings (the PI's reading): order null, read_in "U" or "A"

On --write: out/sample-B4-R.jsonl is first kept as out/sample-B4-R.superseded-B4b-p2.jsonl (refused if that copy
exists), then rewritten with the 185 members; out/_analysis/b4b_sample_R_all.json records the order stream, the counts
and the sha256. sample-B4.jsonl is read and left as it stands.

    python3 out/_analysis/b4b_R_all.py [--write]
"""
import argparse, collections, hashlib, json, os, random, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STREAM = "20261013:R-all-order"


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    s0 = jl("sample-B4.jsonl")
    r0 = jl("sample-B4-R.jsonl")
    if len(s0) != 500 or len(r0) != 18 or sorted(x["order"] for x in r0) != list(range(501, 519)):
        sys.exit("sample-B4.jsonl or sample-B4-R.jsonl is not as B4b and B4b-p2 left them")
    st0 = {(x["sub"], x["theme_id"]): x["stratum"] for x in s0}
    inr = {(x["sub"], x["theme_id"]): x for x in r0}
    dg = jl("disagreements.jsonl")
    unres = {(x["sub"], x["theme_id"]): x for x in dg if x.get("unresolved")}
    if len(unres) != 185 or not set(inr) <= set(unres):
        sys.exit("expected 185 unresolved rulings holding the 18 of R")
    in_ua = sorted(k for k in unres if k in st0)
    added = sorted(k for k in unres if k not in st0 and k not in inr)
    if len(in_ua) != 18 or len(added) != 149:
        sys.exit("expected 18 unresolved in U and A and 149 to add; found %d and %d" % (len(in_ua), len(added)))
    random.Random(STREAM).shuffle(added)
    cls = {(x["sub"], x["theme_id"]): x.get("class") for x in jl("assign_final.jsonl")}
    gold = {(x["sub"], x["theme_id"]) for x in jl("gold_items.jsonl")}
    pilot = {(x["sub"], x["theme_id"]) for x in jl("author_items.jsonl")}

    def line(k, order, read_in, joined):
        d = unres[k]
        return {"sub": k[0], "theme_id": k[1], "item": "%s/%s" % k, "stratum": "R", "order": order, "read_in": read_in,
                "joined": joined, "class": cls[k], "ruled": True, "unresolved": True, "gold": k in gold, "pilot": k in pilot,
                "taxonomy": d.get("taxonomy"), "adjudication_packet": d.get("packet")}
    rows = [line(k, inr[k]["order"], "R", "drawn at B4b-p2") for k in sorted(inr, key=lambda k: inr[k]["order"])]
    rows += [line(k, 518 + i, "R", "added at B4b-p3") for i, k in enumerate(added, 1)]
    rows += [line(k, None, st0[k], "in %s at B4b; counted in R from the same readings" % st0[k]) for k in in_ua]
    if len({(x["sub"], x["theme_id"]) for x in rows}) != 185:
        sys.exit("R does not hold 185 distinct items")
    c = collections.Counter
    print("R: %d items; read in R packets %d (drawn %d, added %d); read in U %d, in A %d" % (
        len(rows), sum(x["read_in"] == "R" for x in rows), len(inr), len(added),
        sum(x["read_in"] == "U" for x in rows), sum(x["read_in"] == "A" for x in rows)))
    print("by class %s; by taxonomy %s; gold %d; pilot %d; by adjudication packet %s" % (
        dict(sorted(c(x["class"] for x in rows).items())), dict(c(x["taxonomy"] for x in rows)),
        sum(x["gold"] for x in rows), sum(x["pilot"] for x in rows),
        dict(sorted(c(x["adjudication_packet"] for x in rows).items()))))
    print("added: orders 519 to %d; first five %s" % (518 + len(added), ", ".join("%s/%s" % k for k in added[:5])))
    print("leagueoflegends/t02 among the added: %s" % (("leagueoflegends", "t02") in set(added)))
    if not a.write:
        return
    keep = os.path.join(OUT, "sample-B4-R.superseded-B4b-p2.jsonl")
    if os.path.exists(keep):
        sys.exit("out/sample-B4-R.superseded-B4b-p2.jsonl exists")
    shutil.copyfile(os.path.join(OUT, "sample-B4-R.jsonl"), keep)
    with open(os.path.join(OUT, "sample-B4-R.jsonl"), "w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    meta = {"stratum": "R, all 185 unresolved rulings (J, 17:10 Berlin)", "draw": "none: every unresolved item taken",
            "order_stream": STREAM, "order_frame": "the 149 added, sorted by (room, theme id), then shuffled",
            "counts": {"drawn_B4b_p2": len(inr), "added_B4b_p3": len(added), "in_U": sum(x["read_in"] == "U" for x in rows),
                       "in_A": sum(x["read_in"] == "A" for x in rows)},
            "orders": {"drawn_B4b_p2": [501, 518], "added_B4b_p3": [519, 518 + len(added)]},
            "superseded": "out/sample-B4-R.superseded-B4b-p2.jsonl, sha256 %s" % sha("sample-B4-R.superseded-B4b-p2.jsonl"),
            "sample_R_sha256": sha("sample-B4-R.jsonl"), "sample_B4_sha256": sha("sample-B4.jsonl"),
            "disagreements_sha256": sha("disagreements.jsonl"), "assign_final_sha256": sha("assign_final.jsonl"),
            "script": "out/_analysis/b4b_R_all.py"}
    json.dump(meta, open(os.path.join(OUT, "_analysis", "b4b_sample_R_all.json"), "w", encoding="utf-8"), indent=1)
    print("wrote out/sample-B4-R.jsonl (%d lines); the B4b-p2 record kept as out/sample-B4-R.superseded-B4b-p2.jsonl" % len(rows))


if __name__ == "__main__":
    main()
