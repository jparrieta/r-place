#!/usr/bin/env python3
"""B4b-p4: the 18 unresolved items in U (3) and A (15) join stratum R as R's own items and are read again in R packets
(J, 17:21 Berlin: "We should have 685 in total"; notes-B4.md, "Stratum R, the 18 from U and A read again in R packets").
No draw: the 18 are sorted by (room, theme id), then served in the order random.Random("20261013:R-ua-order").shuffle
gives, orders 668..685. The other 167 R lines keep their orders 501..667.

Every line gains also_in: "U" or "A" for the 18, null for the 167. The 18 lines get their order, read_in "R" and a new
joined text; the 167 change in nothing else.

On --write: out/sample-B4-R.jsonl is first kept as out/sample-B4-R.superseded-B4b-p3.jsonl (refused if that copy
exists), then rewritten in order 501..685; out/_analysis/b4b_sample_R_ua.json records the order stream, the counts and
the sha256. sample-B4.jsonl is read and left as it stands.

    python3 out/_analysis/b4b_R_ua.py [--write]
"""
import argparse, collections, hashlib, json, os, random, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
STREAM = "20261013:R-ua-order"


def jl(p):
    return [json.loads(x) for x in open(os.path.join(OUT, p), encoding="utf-8") if x.strip()]


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    meta0 = json.load(open(os.path.join(OUT, "_analysis", "b4b_sample_R_all.json"), encoding="utf-8"))
    if sha("sample-B4-R.jsonl") != meta0["sample_R_sha256"] or sha("sample-B4.jsonl") != meta0["sample_B4_sha256"]:
        sys.exit("sample-B4-R.jsonl or sample-B4.jsonl is not as B4b-p3 left it")
    s0 = jl("sample-B4.jsonl")
    r0 = jl("sample-B4-R.jsonl")
    st0 = {(x["sub"], x["theme_id"]): x["stratum"] for x in s0}
    rin = [x for x in r0 if x["read_in"] == "R"]
    rua = [x for x in r0 if x["read_in"] in ("U", "A")]
    if len(r0) != 185 or len(rin) != 167 or len(rua) != 18 or sorted(x["order"] for x in rin) != list(range(501, 668)):
        sys.exit("the R record is not 167 lines in orders 501-667 and 18 read in U and A")
    if any(st0.get((x["sub"], x["theme_id"])) != x["read_in"] or x["order"] is not None for x in rua):
        sys.exit("an R line read in U or A is not that stratum's item, or carries an order")
    ua = sorted((x["sub"], x["theme_id"]) for x in rua)
    random.Random(STREAM).shuffle(ua)
    by = {(x["sub"], x["theme_id"]): x for x in rua}
    rows = []
    for x in sorted(rin, key=lambda x: x["order"]):
        y = dict(x)
        y["also_in"] = None
        rows.append(y)
    for i, k in enumerate(ua, 668):
        y = dict(by[k])
        y["also_in"] = y["read_in"]
        y["order"] = i
        y["joined"] = "in %s at B4b; read again in R at B4b-p4" % y["also_in"]
        y["read_in"] = "R"
        rows.append(y)
    if [x["order"] for x in rows] != list(range(501, 686)) or len({(x["sub"], x["theme_id"]) for x in rows}) != 185:
        sys.exit("R does not hold 185 distinct items in orders 501 to 685")
    old = {(x["sub"], x["theme_id"]): x for x in rin}
    for x in rows[:167]:
        y = dict(x); del y["also_in"]
        if y != old[(x["sub"], x["theme_id"])]:
            sys.exit("a line of the 167 changed: %s" % x["item"])
    c = collections.Counter
    print("R: %d items, all read in R packets; also in U %d, in A %d" % (
        len(rows), sum(x["also_in"] == "U" for x in rows), sum(x["also_in"] == "A" for x in rows)))
    print("the 18 by class %s; by taxonomy %s; gold %d; pilot %d" % (
        dict(sorted(c(x["class"] for x in rows[167:]).items())), dict(c(x["taxonomy"] for x in rows[167:])),
        sum(x["gold"] for x in rows[167:]), sum(x["pilot"] for x in rows[167:])))
    for x in rows[167:]:
        print("  %d %s (also in %s)" % (x["order"], x["item"], x["also_in"]))
    if not a.write:
        return
    keep = os.path.join(OUT, "sample-B4-R.superseded-B4b-p3.jsonl")
    if os.path.exists(keep):
        sys.exit("out/sample-B4-R.superseded-B4b-p3.jsonl exists")
    shutil.copyfile(os.path.join(OUT, "sample-B4-R.jsonl"), keep)
    with open(os.path.join(OUT, "sample-B4-R.jsonl"), "w", encoding="utf-8") as f:
        for x in rows:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    meta = {"stratum": "R, all 185 unresolved rulings, each read in R packets (J, 17:21 Berlin: 685 in total)",
            "draw": "none: the 18 unresolved items in U and A join R and are read again",
            "order_stream": STREAM, "order_frame": "the 18 in U and A, sorted by (room, theme id), then shuffled",
            "counts": {"read_in_R": len(rows), "also_in_U": sum(x["also_in"] == "U" for x in rows),
                       "also_in_A": sum(x["also_in"] == "A" for x in rows)},
            "orders": {"drawn_B4b_p2": [501, 518], "added_B4b_p3": [519, 667], "from_U_and_A_B4b_p4": [668, 685]},
            "superseded": ["out/sample-B4-R.superseded-B4b-p2.jsonl, sha256 %s" % sha("sample-B4-R.superseded-B4b-p2.jsonl"),
                           "out/sample-B4-R.superseded-B4b-p3.jsonl, sha256 %s" % sha("sample-B4-R.superseded-B4b-p3.jsonl")],
            "sample_R_sha256": sha("sample-B4-R.jsonl"), "sample_B4_sha256": sha("sample-B4.jsonl"),
            "disagreements_sha256": sha("disagreements.jsonl"), "assign_final_sha256": sha("assign_final.jsonl"),
            "script": "out/_analysis/b4b_R_ua.py"}
    json.dump(meta, open(os.path.join(OUT, "_analysis", "b4b_sample_R_ua.json"), "w", encoding="utf-8"), indent=1)
    print("wrote out/sample-B4-R.jsonl (%d lines); the B4b-p3 record kept as out/sample-B4-R.superseded-B4b-p3.jsonl" % len(rows))


if __name__ == "__main__":
    main()
