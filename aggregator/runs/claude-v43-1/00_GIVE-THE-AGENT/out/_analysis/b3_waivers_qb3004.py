#!/usr/bin/env python3
"""B3b: J's waiver at QB3-004 (22:30 Berlin): one line in out/return_waivers.jsonl per accepted B3 return without a
prediction line, in the form J gave. Finds them from the returns (an accepted r*.jsonl whose meta says valid and
which holds no predicted_confusion line); refuses unless they are the 32 named in the question. Dry run unless --write."""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
NAMED = ("B0011/r6 B0140/r6 B0170/r6 B0225/r6 B0247/r6 B0271/r6 B0326/r6 B0356/r6 B0382/r1 B0440/r6 B0444/r6 B0471/r6 "
         "B0488/r6 B0515/r6 B0525/r6 B0581/r6 B0582/r6 B0666/r6 B0701/r6 B0725/r6 B0749/r6 B0759/r6 B0803/r6 B0819/r6 "
         "B0824/r6 B0916/r6 B0954/r6 B0961/r6 B1015/r6 B1041/r6 B1162/r6 B1181/r6").split()
REASON = ("the reader wrote no predicted_confusion line; its item lines are whole and valid and are scored as given; "
          "agent_report-B3.md names the return as without a prediction")


def main():
    found = []
    for f in sorted(glob.glob(os.path.join(OUT, "_fleet_raw", "B3", "B*", "r*.jsonl"))):
        if not json.load(open(f[:-6] + ".meta.json", encoding="utf-8")).get("valid"):
            continue
        if not any("predicted_confusion" in ln for ln in open(f, encoding="utf-8")):
            found.append("%s/%s" % (os.path.basename(os.path.dirname(f)), os.path.basename(f)[:-6]))
    if found != sorted(NAMED):
        sys.exit("the returns without a prediction are not the 32 named: %s" % sorted(set(found) ^ set(NAMED)))
    p = os.path.join(OUT, "return_waivers.jsonl")
    have = {(w.get("stage"), w.get("file"), w.get("check")) for w in (json.loads(x) for x in open(p, encoding="utf-8") if x.strip())}
    rows = [{"stage": "B3", "file": "%s.jsonl" % k, "check": "no_prediction", "reason": REASON,
             "ruled_by": "J, 2026-10-12, QB3-004"} for k in NAMED if ("B3", "%s.jsonl" % k, "no_prediction") not in have]
    print("%d waivers to write" % len(rows))
    if "--write" in sys.argv:
        with open(p, "a", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("return_waivers.jsonl now %d lines" % sum(1 for x in open(p, encoding="utf-8") if x.strip()))


if __name__ == "__main__":
    main()
