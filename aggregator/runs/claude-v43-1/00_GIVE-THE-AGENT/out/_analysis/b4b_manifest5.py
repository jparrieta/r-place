#!/usr/bin/env python3
"""B4b-p4: append a run_manifest.json entry that supersedes entry 15 (B4b-p3): the 18 unresolved items of U and A join
stratum R as R's own items, read again in S05-47 and S05-48 (J, 17:21 Berlin: "We should have 685 in total"). 685 lines
due in 48 packets, 667 distinct items. Entry 15 stays in the file. Refuses if an entry for leg B4b-p4 exists. Dry run
unless --write.

    python3 out/_analysis/b4b_manifest5.py [--write]
"""
import copy, datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    b4 = [e for e in d if e.get("stage") == "B4"]
    if any(e.get("leg") == "B4b-p4" for e in b4):
        sys.exit("an entry for leg B4b-p4 exists")
    last = b4[-1]
    if last.get("leg") != "B4b-p3" or last.get("packets") != 46:
        sys.exit("the last B4 entry is not entry 15 of B4b-p3")
    man = json.load(open(os.path.join(OUT, "_packets-B4", "MANIFEST.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(OUT, "_analysis", "b4b_sample_R_ua.json"), encoding="utf-8"))
    if meta["sample_R_sha256"] != sha("sample-B4-R.jsonl"):
        sys.exit("sample-B4-R.jsonl is not as b4b_R_ua.py wrote it")
    e = copy.deepcopy(last)
    n_pk = len(man)
    e["leg"] = "B4b-p4"
    e["written_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    e["supersedes"] = ("the B4b-p3 entry written %s (46 packets, 667 lines; the 18 unresolved items of U and A counted "
                       "in R from the same readings); those 18 are now R's own items, read again in R packets"
                       % last["written_utc"])
    e["packets"] = n_pk
    e["lines_due_per_reader_set"] = sum(v["items"] for v in man.values())
    e["packet_bytes"] = {"min": min(v["bytes"] for v in man.values()), "max": max(v["bytes"] for v in man.values())}
    e["items_per_packet"] = {"min": min(v["items"] for v in man.values()), "max": max(v["items"] for v in man.values())}
    e["seeds"]["stream_R_ua_order"] = meta["order_stream"]
    e["sample"]["items"] = e["lines_due_per_reader_set"]
    e["sample"]["distinct_items"] = 667
    e["sample"]["strata"]["R"] = ("all 185 unresolved rulings, each read in R packets (J, 17:10 and 17:21 Berlin): 18 drawn "
                                  "at B4b-p2 (S05-35, S05-36), 149 added at B4b-p3 (S05-37 to S05-46), and the 18 also in "
                                  "U (3) and A (15) read again at B4b-p4 (S05-47, S05-48); each reading counts only in "
                                  "its packet's stratum; diagnostic, reported apart, never pooled")
    e["sample"]["file_R"] = "out/sample-B4-R.jsonl, 185 lines, sha256 %s (never served)" % meta["sample_R_sha256"]
    e["sample"]["file_R_superseded"] = meta["superseded"]
    e["comparisons_note"] = ("1,000 readings of U and A against the settled line (their unresolved items excluded and "
                             "counted at the check); R's 370 readings an arm, all from R packets, have no settled line: "
                             "the readers' agreement with each other, whether primaries meet, and whether placements fall "
                             "among the item's earlier placements; on the 18 also in U and A, R's readings beside the same "
                             "arm's U or A readings, a side note reported apart")
    for k in e["arms"]:
        e["arms"][k]["n_agents"] = 2 * n_pk
    e["n_agents_note"] = "two fresh readers per item in each arm (section 10); %d reader sessions an arm, %d packets x 2" % (2 * n_pk, n_pk)
    e["build"] = e["build"] + "; B4b-p4: b4b_R_ua.py, b4b_packets_R_ua.py, b4b_packets_check4.py; S05-47, S05-48"
    e["return_spec"] = "out/RETURN-B4.md, sha256 %s" % sha("RETURN-B4.md")
    print(json.dumps({k: e[k] for k in ("stage", "leg", "supersedes", "packets", "lines_due_per_reader_set", "packet_bytes",
                                          "items_per_packet", "n_agents", "n_agents_note")}, ensure_ascii=False))
    print(json.dumps(e["sample"]["strata"]["R"], ensure_ascii=False))
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
