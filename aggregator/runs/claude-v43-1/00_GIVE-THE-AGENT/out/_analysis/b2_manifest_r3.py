#!/usr/bin/env python3
"""B2a-r3: append round 3's entry to out/run_manifest.json. Refuses a second round-3 entry. Dry run unless --write."""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B2" and e.get("round") == 3 for e in d):
        sys.exit("run_manifest.json already holds a B2 round-3 entry")
    man = json.load(open(os.path.join(OUT, "_packets-B2", "round-3", "MANIFEST.json"), encoding="utf-8"))
    e = {
        "stage": "B2", "round": 3, "leg": "B2a-r3",
        "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": "deepseek/deepseek-v4.1-flash, called directly, the same readers as round 2 (J, QB2-007)",
        "reader_settings": {"route": "direct, not @preset/cheap", "reasoning_effort": "medium", "max_tokens": 128000},
        "decoding": {"temperature": None, "top_p": None, "note": "set by the dispatch (fleet.py)"},
        "seeds": {"packet_order": 20261013, "cut": "consecutive cut of the seeded order, largest packet minimised"},
        "n_agents": 3, "n_items": sum(v["items"] for v in man.values()),
        "packets": [{"name": k, "items": v["items"], "bytes": v["bytes"], "item_bytes": v["item_bytes"],
                     "sha256": v["sha256"]} for k, v in sorted(man.items())],
        "ids": "fleet ids only (out/fleet_ids.jsonl): C and seven digits for concepts, T2- and five digits for second-order themes; each MANIFEST entry carries codes_by_item for fleet.py's citation check",
        "caps": "at most 15 items and 180,000 bytes of item text a packet; no item split (J, 2026-10-12)",
        "scheme": "out/scheme.jsonl after round 2's edits (scheme_edits 295 lines), exemplars withheld",
        "items": "the 44 unsplit hard items and the 54 children of the six split bags (QB2-010); the six parents are not served",
        "return_spec": "out/RETURN-B2.md with fleet ids and the three-concept floor for also_present (QB2-008)",
        "notes": "Pilot round 3, the first round in which only the scheme changes (QB2-007) and the first with fleet ids.",
    }
    print(json.dumps(e, indent=1)[:900])
    if "--write" not in sys.argv:
        return
    d.append(e)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
