#!/usr/bin/env python3
"""B4b: supersede the first B4b entry of out/run_manifest.json, which carried the reader count only inside each arm,
with an entry that also carries n_agents at the top (two fresh readers per item, section 10). The first entry stays
in the file; the new one names it under "supersedes". Refuses if a superseding B4b entry already exists. Dry run
unless --write.

    python3 out/_analysis/b4b_manifest2.py [--write]
"""
import copy, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    b4 = [e for e in d if e.get("stage") == "B4" and e.get("leg") == "B4b"]
    if len(b4) != 1:
        sys.exit("expected one B4b entry, found %d" % len(b4))
    e = copy.deepcopy(b4[0])
    e["written_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    e["supersedes"] = "the first B4b entry (written %s), which carried the reader count only inside each arm" % b4[0]["written_utc"]
    e["n_agents"] = 2
    e["n_agents_note"] = ("two fresh readers per item in each arm (section 10); %d reader sessions an arm, %d packets x 2"
                          % (2 * e["packets"], e["packets"]))
    print(json.dumps({k: e[k] for k in ("stage", "leg", "written_utc", "supersedes", "n_agents", "n_agents_note")}))
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
