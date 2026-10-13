#!/usr/bin/env python3
"""B4b-p2: append a run_manifest.json entry that supersedes entry 13 (B4b) and adds stratum R: J's "draw other 18"
(16:43 Berlin), 18 unresolved items not in sample-B4.jsonl, seed 20261013 with streams ":R" and ":R-order", two more
packets (S05-35, S05-36) read by both arms, 518 items in 36 packets. Entry 13 stays in the file. Refuses if an entry
naming stratum R already exists. Dry run unless --write.

    python3 out/_analysis/b4b_manifest3.py [--write]
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
    if any("R" in (e.get("sample") or {}).get("strata", {}) for e in b4):
        sys.exit("an entry naming stratum R exists")
    last = b4[-1]
    if last.get("n_agents") != 2 or last.get("packets") != 34:
        sys.exit("the last B4 entry is not entry 13 of B4b")
    man = json.load(open(os.path.join(OUT, "_packets-B4", "MANIFEST.json"), encoding="utf-8"))
    smr = json.load(open(os.path.join(OUT, "_analysis", "b4b_sample_R.json"), encoding="utf-8"))
    e = copy.deepcopy(last)
    n_pk = len(man)
    e["leg"] = "B4b-p2"
    e["written_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    e["supersedes"] = ("the B4b entry written %s (34 packets, strata U and A); this one adds stratum R and its two packets"
                       % last["written_utc"])
    e["packets"] = n_pk
    e["lines_due_per_reader_set"] = sum(v["items"] for v in man.values())
    e["packet_bytes"] = {"min": min(v["bytes"] for v in man.values()), "max": max(v["bytes"] for v in man.values())}
    e["items_per_packet"] = {"min": min(v["items"] for v in man.values()), "max": max(v["items"] for v in man.values())}
    e["seeds"]["streams_R"] = smr["streams"]
    e["sample"]["items"] = 518
    e["sample"]["strata"]["R"] = ("18 uniform without replacement from the %d unresolved rulings not in sample-B4.jsonl "
                                  "(J, 16:43 Berlin: 'draw other 18'); diagnostic, reported apart, never pooled with U or A"
                                  % smr["frame_size"])
    e["sample"]["file_R"] = "out/sample-B4-R.jsonl, sha256 %s (never served)" % smr["sample_R_sha256"]
    e["sample"]["unresolved_already_drawn"] = {"U": 3, "A": 15}
    e["comparisons_per_arm"] = 1000
    e["comparisons_note"] = ("1,000 readings of U and A against the settled line (their unresolved items excluded and "
                             "counted at the check); R's 36 readings an arm have no settled line: the readers' agreement "
                             "with each other, whether primaries meet, and whether placements fall among the item's "
                             "earlier placements")
    for k in e["arms"]:
        e["arms"][k]["n_agents"] = 2 * n_pk
    e["n_agents_note"] = "two fresh readers per item in each arm (section 10); %d reader sessions an arm, %d packets x 2" % (2 * n_pk, n_pk)
    e["build"] = e["build"] + "; B4b-p2: b4b_sample_R.py, b4b_packets_R.py, b4b_packets_check2.py; S05-35 and S05-36"
    e["return_spec"] = "out/RETURN-B4.md, sha256 %s" % sha("RETURN-B4.md")
    print(json.dumps({k: e[k] for k in ("stage", "leg", "supersedes", "packets", "lines_due_per_reader_set", "packet_bytes",
                                          "items_per_packet", "n_agents", "n_agents_note", "comparisons_note")}, ensure_ascii=False))
    print(json.dumps(e["sample"], ensure_ascii=False)[:900])
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
