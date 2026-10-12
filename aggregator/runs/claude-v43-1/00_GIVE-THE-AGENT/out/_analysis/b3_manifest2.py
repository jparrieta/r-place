#!/usr/bin/env python3
"""B3a: append the stage B3 entry for the build in B2's packet shape (J, QB3-001) to out/run_manifest.json; it
supersedes the first B3 entry (whole-room batches in parts). Refuses a second entry of this shape. Dry run unless
--write."""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B3" and e.get("shape") == "B2 packets" for e in d):
        sys.exit("run_manifest.json already holds the B2-shape B3 entry")
    b = [json.loads(x) for x in open(os.path.join(OUT, "batches-B3.jsonl"), encoding="utf-8") if x.strip()]
    man = json.load(open(os.path.join(OUT, "_packets-B3", "MANIFEST.json"), encoding="utf-8"))
    order = json.load(open(os.path.join(OUT, "_analysis", "b3_dispatch_order.json"), encoding="utf-8"))
    sha = lambda f: hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest()
    e = {"stage": "B3", "leg": "B3a", "shape": "B2 packets",
         "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "supersedes": "the first B3 entry (whole-room batches served in parts), superseded under J at QB3-001",
         "model": "deepseek/deepseek-v4.1-flash, called directly: the readers of B2's rounds 2 and 3 and the gold round (J)",
         "reader_settings": {"route": "direct, not @preset/cheap", "reasoning_effort": "medium", "max_tokens": 128000},
         "decoding": {"temperature": None, "top_p": None, "note": "set by the dispatch (fleet.py)"},
         "seeds": {"allocation": order["seed"], "suffix": order["suffix"], "redraws": order["redraws"],
                   "dispatch_order": "seeded shuffle, out/_analysis/b3_dispatch_order.json"},
         "R": 2, "n_agents": len(b), "batches": len(b), "packets": len(man),
         "positions": sum(x["n_items"] for x in b), "items": 7844, "rooms": 705,
         "gold_copies": sum(len(x["gold_items"]) for x in b), "duplicates": sum(len(x["duplicate_items"]) for x in b),
         "caps": "at most 15 items and 180,000 bytes of item text a packet; no parts (J, QB3-001)",
         "max_item_bytes": max(v["item_bytes"] for v in man.values()),
         "groups": {k: len(v) for k, v in order["groups"].items()},
         "exemplars": "none served", "warmup": "in reserve",
         "scheme": "out/scheme_final.jsonl, sha256 %s" % sha("scheme_final.jsonl"),
         "return_spec": "out/RETURN-B3.md, sha256 %s" % sha("RETURN-B3.md"),
         "ids": "fleet ids only (out/fleet_ids.jsonl); codes_by_item in each MANIFEST entry",
         "build": "out/_analysis/b3_allocate2.py and b3_packets_fleet2.py; out/_packets-B3/"}
    print(json.dumps(e)[:700])
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
