#!/usr/bin/env python3
"""E1e: run_manifest.json with stage E1's two entries appended, printed whole (the manifest is one JSON list).

    python3 out/audit-E1/manifest_E1.py > out/audit-E1/run_manifest.e1e.json

Then the analyst copies the printed list over out/run_manifest.json, after keeping the list as it stood in
out/audit-E1/run_manifest.before-E1e.json. The script stops if the manifest already holds a stage-E1 entry.

The two entries, in order:
- the reconstruction readers of E1c's dispatch, from _fleet_raw/E1/arm.json and DONE: model, route, effort, readers,
  reissues, packets, the return specification's hash, the draw seed (out/seed.txt), cost and tokens. The arm file
  records no temperature or top_p, and the entry says so;
- the experience, the stage's last line: experience-E1.md, its sha256 as it stands, and the model that wrote it.
"""
import datetime, hashlib, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")


def main():
    man = json.load(open(os.path.join(OUT, "run_manifest.json"), encoding="utf-8"))
    if any(str(e.get("stage")) == "E1" for e in man):
        sys.exit("run_manifest.json already holds a stage-E1 entry")
    arm = json.load(open(os.path.join(OUT, "_fleet_raw", "E1", "arm.json"), encoding="utf-8"))
    done = json.load(open(os.path.join(OUT, "_fleet_raw", "E1", "DONE"), encoding="utf-8"))
    seed = open(os.path.join(OUT, "seed.txt"), encoding="utf-8").read().split()[0]
    pkg = man[0].get("package_sha256")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fleet = {"stage": "E1", "leg": "E1c-dispatch",
             "step": "the reconstruction readers (stage E1 section 4): one reader per sampled room, sent by the dispatch",
             "written_utc": now, "package_sha256": pkg,
             "model": arm.get("served"), "route": arm.get("route"), "reasoning_effort": arm.get("reasoning_effort"),
             "served_verified": arm.get("served_verified"), "max_tokens": arm.get("max_tokens"),
             "decoding": {"temperature": None, "top_p": None,
                          "note": "not recorded in _fleet_raw/E1/arm.json; set by the dispatch, which this session cannot read"},
             "seeds": {"draw": seed, "draw_rule": "audit-E1/reconstruction_draw.py"},
             "n_agents": done.get("packets"), "readers_per_room": arm.get("readers"), "reissue": arm.get("reissue"),
             "return_spec_sha256": arm.get("return_spec_sha256"),
             "dispatch_utc": [arm.get("utc"), done.get("utc")], "cost_usd": done.get("cost_usd"),
             "input_tokens": done.get("input_tokens"), "output_tokens": done.get("output_tokens"),
             "notes": "fleet.py judged 0 returns valid and 30 exhausted (each return ended with a marker line the "
                      "specification did not name, defects.jsonl line 121); validated at E1d from the newest raw file "
                      "per room by audit-E1/reconstruction_validate.py, 30 valid (25 under the rule as first written)"}
    sha = hashlib.sha256(open(os.path.join(OUT, "experience-E1.md"), "rb").read()).hexdigest()
    exp = {"stage": "E1", "leg": "E1e", "step": "the experience (stage E1 section 9), the stage's last manifest line",
           "written_utc": now, "package_sha256": pkg, "model": "claude-opus-5-5",
           "decoding": {"temperature": None, "top_p": None, "note": "the platform's; the analyst's session cannot read them"},
           "seeds": {}, "n_agents": None,
           "file": "experience-E1.md", "sha256": sha,
           "notes": "experience-E1.md, written once by the analyst (claude-opus-5-5) at E1e; sha256 of the file as it stands"}
    print(json.dumps(man + [fleet, exp], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
