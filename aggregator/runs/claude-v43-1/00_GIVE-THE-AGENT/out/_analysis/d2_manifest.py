#!/usr/bin/env python3
"""D2a: append stage D2's entry to out/run_manifest.json, the labelers' model and the readers' model, read from the
files that record them: the rooms' run.json copies (out/rooms/<sub>/run.json), the fleet's arm.json and DONE
(out/_fleet_raw/D2v/). The effort of the labelers is the handler's recap (the PI's message of 2026-10-16), which no
file this stage may read records. Refuses if a D2 entry exists.

    python3 out/_analysis/d2_manifest.py            print the entry
    python3 out/_analysis/d2_manifest.py --write    append it
"""
import collections, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RAW = os.path.join(OUT, "_fleet_raw", "D2v")
MP = os.path.join(OUT, "run_manifest.json")

runs = [json.load(open(os.path.join(OUT, "rooms", s, "run.json"))) for s in sorted(os.listdir(os.path.join(OUT, "rooms")))
        if os.path.exists(os.path.join(OUT, "rooms", s, "run.json"))]
arm = json.load(open(os.path.join(RAW, "arm.json")))
done = json.loads(open(os.path.join(RAW, "DONE"), encoding="utf-8").read())
entry = {
    "stage": "D2", "leg": "D2a",
    "step": "the check leg of the return: the labelers' returns (DROPS/D/) and the verdict fleet (_fleet_raw/D2v/)",
    "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "labelers_model": dict(collections.Counter(r.get("model") for r in runs)),
    "labelers_resumed_with": dict(collections.Counter(r.get("resumed_with") for r in runs)),
    "labelers_attempts": dict((str(k), v) for k, v in collections.Counter(r.get("attempts") for r in runs).items()),
    "labelers_note": "one Codex fork per room of the original case lead's verified checkpoint, resumed on gpt-5.6 at "
                     "medium effort and switched in the same fork to gpt-6.1 at medium effort before the return task "
                     "(J's ruling; the handler's recap of 2026-10-16); model and resumed_with from the 705 run.json "
                     "copies; 378 rooms had one to four same-session repairs of attempt 1 (the recap); no second "
                     "labeler set (D2L) was run",
    "readers_model": arm.get("served"),
    "readers_route": arm.get("route"), "readers_effort": arm.get("reasoning_effort"),
    "readers_served_verified": arm.get("served_verified"), "readers_per_room": arm.get("readers"),
    "readers_reissue_limit": arm.get("reissue"), "readers_max_tokens": arm.get("max_tokens"),
    "readers_return_spec_sha256": arm.get("return_spec_sha256"),
    "readers_valid_returns": done.get("valid_returns"), "readers_exhausted": done.get("exhausted"),
    "readers_cost_usd": done.get("cost_usd"), "readers_utc": [arm.get("utc"), done.get("utc")],
    "decoding": {"temperature": None, "top_p": None,
                 "note": "set by the dispatch and the Codex harness, which this session cannot read"},
    "seeds": {"sample_draw": 20261016, "note": "ten model-D.md files by random.Random(20261016), stratified on the "
                                               "room verdict (_analysis/d2_sample.py)"},
    "n_agents": {"labelers": len(runs), "readers": done.get("valid_returns")},
    "model_version": open(os.path.join(OUT, "handoff-D", "VERSION"), encoding="utf-8").read().strip(),
}
print(json.dumps(entry, indent=1))
if "--write" in sys.argv:
    man = json.load(open(MP))
    if any(isinstance(e, dict) and str(e.get("stage")) == "D2" for e in man):
        sys.exit("run_manifest.json already holds a D2 entry; not appended")
    man.append(entry)
    json.dump(man, open(MP, "w"), indent=1, ensure_ascii=False)
    print("appended; run_manifest.json holds %d entries" % len(man))
