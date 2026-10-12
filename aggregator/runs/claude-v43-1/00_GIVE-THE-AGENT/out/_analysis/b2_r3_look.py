#!/usr/bin/env python3
"""B2b-r3: (1) the round-3 items where readers differ or pairwise fell since round 2, from b2_r3_items.tsv;
(2) fleet.py's counts for round 3 from _fleet_raw/B2/round-3/log.jsonl: calls, reissues, durations, cost, per
packet, and the kept readers' own rows (RESCUE-2026-10-12.json). Reads only."""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rows = [x.split("\t") for x in open(os.path.join(OUT, "_analysis", "b2_r3_items.tsv"), encoding="utf-8").read().splitlines()]
h = rows[0]
for r in rows[1:]:
    d = dict(zip(h, r))
    if d["disagree"] == "yes" or float(d["pairwise_change"]) < 0:
        print("%s | %s %s | mine %s | rech %s | r3: %s | pw %s | r2: %s | r2pw %s | %s" % (
            d["item"], d["source"], d["author_conf"], d["author"], d["rechecked"], d["readers"], d["pairwise"],
            d["r2_readers"], d["r2_pairwise"], d["pairwise_change"]))
raw = os.path.join(OUT, "_fleet_raw", "B2", "round-3")
L = [json.loads(x) for x in open(os.path.join(raw, "log.jsonl"), encoding="utf-8") if x.strip()]
kept = {pk: v["kept"] for pk, v in json.load(open(os.path.join(raw, "RESCUE-2026-10-12.json"), encoding="utf-8"))["packets"].items()}
print("\ncalls %d; valid at dispatch %d; cost %.4f USD; elapsed sum %.0f s" % (
    len(L), sum(1 for x in L if x["valid"]), sum((x.get("usage") or {}).get("cost") or 0 for x in L), sum(x.get("elapsed_s") or 0 for x in L)))
print("reissue values:", collections.Counter(x["reissue"] for x in L))
print("refusal reasons:", collections.Counter(("cites T3-" in (x.get("why") or "")) for x in L if not x["valid"]))
for pk in sorted(kept):
    xs = [x for x in L if x["packet"] == pk]
    ks = [x for x in xs if x["reader"] in kept[pk]]
    print("%s: calls %d; kept %s; kept elapsed %s s; kept output tokens %s; kept reissue %s" % (
        pk, len(xs), ",".join(kept[pk]), ",".join("%.0f" % x["elapsed_s"] for x in ks),
        ",".join(str(x["usage"]["output_tokens"]) for x in ks), ",".join(str(x["reissue"]) for x in ks)))
other = [x for x in L if not x["valid"] and "cites T3-" not in (x.get("why") or "")]
for x in other:
    print("  refused for another reason: %s %s %s" % (x["packet"], x["reader"], x.get("why")))
