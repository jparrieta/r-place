#!/usr/bin/env python3
"""B3a: append stage B3's entry to out/run_manifest.json (stage B3 section 1.2, on stage A1's schema): the readers'
model, the seed, the decoding, n_agents at R, and the build's counts from batches-B3.jsonl and the packets'
MANIFEST. Refuses a second B3 entry. Dry run unless --write."""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B3" for e in d):
        sys.exit("run_manifest.json already holds a B3 entry")
    b = [json.loads(x) for x in open(os.path.join(OUT, "batches-B3.jsonl"), encoding="utf-8") if x.strip()]
    man = json.load(open(os.path.join(OUT, "_packets-B3", "MANIFEST.json"), encoding="utf-8"))
    order = json.load(open(os.path.join(OUT, "_analysis", "b3_dispatch_order.json"), encoding="utf-8"))
    sha = lambda f: hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest()
    e = {"stage": "B3", "leg": "B3a", "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "model": "deepseek/deepseek-v4.1-flash, called directly: the readers of B2's rounds 2 and 3 and the gold round (J)",
         "reader_settings": {"route": "direct, not @preset/cheap", "reasoning_effort": "medium", "max_tokens": 128000},
         "decoding": {"temperature": None, "top_p": None, "note": "set by the dispatch (fleet.py)"},
         "seeds": {"allocation": order["seed"], "suffix": order["suffix"], "redraws": order["redraws"],
                   "dispatch_order": "seeded shuffle, out/_analysis/b3_dispatch_order.json"},
         "R": 2, "n_agents": len(b), "batches": len(b), "packet_files": len(man),
         "batches_in_parts": len({v["group"] for v in man.values() if "group" in v}),
         "positions": sum(x["n_items"] for x in b), "items": 7844, "rooms": 705,
         "gold_copies": sum(len(x["gold_items"]) for x in b), "duplicates": sum(len(x["duplicate_items"]) for x in b),
         "groups": {k: len(v) for k, v in order["groups"].items()},
         "exemplars": "none served", "warmup": "in reserve",
         "scheme": "out/scheme_final.jsonl, sha256 %s" % sha("scheme_final.jsonl"),
         "return_spec": "out/RETURN-B3.md, sha256 %s" % sha("RETURN-B3.md"),
         "ids": "fleet ids only (out/fleet_ids.jsonl); codes_by_item in each MANIFEST entry",
         "packets": "out/_packets-B3/ (out/_analysis/b3_packets_fleet.py); every file under 50 KB",
         "notes": "stage B3 build; design points under QB3-001"}
    print(json.dumps(e)[:900])
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
