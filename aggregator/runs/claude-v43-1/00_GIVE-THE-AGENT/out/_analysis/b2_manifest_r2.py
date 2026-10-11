#!/usr/bin/env python3
"""B2a-r2: append round 2's entry to out/run_manifest.json (a JSON list). Refuses a second round-2 entry.
Part sizes and hashes are read from out/_packets-B2/round-2/MANIFEST.json. Dry run unless --write."""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B2" and e.get("round") == 2 for e in d):
        sys.exit("run_manifest.json already holds a B2 round-2 entry")
    man = json.load(open(os.path.join(OUT, "_packets-B2", "round-2", "MANIFEST.json"), encoding="utf-8"))
    parts = sorted(man.items(), key=lambda kv: kv[1]["part"])
    order = json.load(open(os.path.join(OUT, "_analysis", "b2_order_r2.json"), encoding="utf-8"))
    n_items = sum(1 for x in open(os.path.join(OUT, "author_items.jsonl"), encoding="utf-8") if x.strip())
    e = {
        "stage": "B2", "round": 2, "leg": "B2a-r2",
        "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": "deepseek/deepseek-v4-flash-0731, the model that served round 1, on the routine reader route",
        "reader_settings": {"provider": "Relace (one provider)", "reasoning_effort": "medium",
                            "round_1_was": "high effort on mixed providers"},
        "decoding": {"temperature": None, "top_p": None,
                     "note": "set by the dispatch (fleet.py); the reader settings above are J's for round 2 on"},
        "seeds": {"hard_set": "b2a-r1:hard, plus the ten biggest bags of notes-B1.md (no draw)",
                  "packet_order": order["seed"]},
        "n_agents": 3, "n_items": n_items,
        "packet": "out/_packets-B2/round-2/, P03-r2 in %d parts for one reader (QB2-001)" % len(parts),
        "parts": [{"name": k, "bytes": v["bytes"], "sha256": v["sha256"], "positions": v["positions"],
                   "items": v["items"]} for k, v in parts],
        "scheme": "out/scheme.jsonl after round 1's edits (scheme_edits.jsonl 286 lines), exemplars withheld",
        "return_spec": "out/RETURN-B2.md with the also_present clause and the parts paragraph",
        "notes": ("Pilot round 2. The reader settings changed from round 1 (one provider, Relace; medium "
                  "effort), so a change in agreement is partly the settings, not only the edits. Fidelity is "
                  "reported against author_items.jsonl and against the rechecked placements. MANIFEST.json "
                  "follows QB2-004's assumption until it is answered."),
    }
    print(json.dumps(e, indent=1)[:1500])
    if "--write" not in sys.argv:
        return
    d.append(e)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
