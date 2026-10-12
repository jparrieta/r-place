#!/usr/bin/env python3
"""B2c: append run_manifest.json entries for the gold round and the two stability rounds, built on the frozen
scheme by b2_packets_fleet2.py. Refuses a second B2c entry for a round. Dry run unless --write."""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
BRIEF = {"gold": "the builder's brief (BRIEF in out/_analysis/b2_packets_fleet2.py)",
         "stab-1": "out/brief-stab-1.md, the brief reworded, no test changed",
         "stab-2": "out/brief-stab-2.md, the brief reworded, no test changed"}


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    sha = hashlib.sha256(open(os.path.join(OUT, "scheme_final.jsonl"), "rb").read()).hexdigest()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new = []
    for rnd in ("gold", "stab-1", "stab-2"):
        if any(e.get("stage") == "B2" and str(e.get("round")) == rnd for e in d):
            sys.exit("run_manifest.json already holds a B2 %s entry" % rnd)
        man = json.load(open(os.path.join(OUT, "_packets-B2", "round-%s" % rnd, "MANIFEST.json"), encoding="utf-8"))
        new.append({
            "stage": "B2", "round": rnd, "leg": "B2c", "written_utc": now,
            "model": "deepseek/deepseek-v4.1-flash, called directly: the readers of rounds 2 and 3 (QB2-007)",
            "reader_settings": {"route": "direct, not @preset/cheap", "reasoning_effort": "medium", "max_tokens": 128000},
            "decoding": {"temperature": None, "top_p": None, "note": "set by the dispatch (fleet.py)"},
            "seeds": {"packet_order": 20261014, "cut": "the same seed and cut in all three B2c rounds, so the same items fall in the same packets in the same order"},
            "n_agents": 3, "n_items": sum(v["items"] for v in man.values()),
            "packets": [{"name": k, "items": v["items"], "bytes": v["bytes"], "item_bytes": v["item_bytes"],
                         "sha256": v["sha256"]} for k, v in sorted(man.items())],
            "scheme": "out/scheme_final.jsonl (frozen at B2b-r3-p3; tier main/rare, J at QB2-014), sha256 %s; exemplars withheld" % sha,
            "items": "gold_items.jsonl's 40 items (placements never shown)",
            "brief": BRIEF[rnd],
            "ids": "fleet ids only (out/fleet_ids.jsonl); codes_by_item in each MANIFEST entry; 0 room ids in any file",
            "caps": "at most 15 items and 180,000 bytes of item text a packet; no item split (J, 2026-10-12)",
            "return_spec": "out/RETURN-B2.md: fleet ids, the three-concept floor, a bag with no other theme at the floor not flagged, 'twenty themes at most'",
            "notes": ("stage B2 section 5: the gold round on the frozen scheme" if rnd == "gold" else
                      "stage B2 section 5: the stability check, the gold set under a reworded brief")})
    for e in new:
        print(e["round"], e["n_items"], [x["name"] for x in e["packets"]])
    if "--write" not in sys.argv:
        return
    d += new
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
