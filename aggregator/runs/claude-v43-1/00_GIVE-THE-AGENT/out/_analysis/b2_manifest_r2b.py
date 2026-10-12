#!/usr/bin/env python3
"""B2b-r2: append the entry for round 2 as rebuilt in self-contained packets to out/run_manifest.json.
The B2a-r2 entry (11 parts) stays; this one supersedes it. Refuses a second rebuild entry. Dry run unless --write."""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B2" and e.get("round") == 2 and e.get("leg") == "B2b-r2" for e in d):
        sys.exit("run_manifest.json already holds the B2b-r2 rebuild entry")
    man = json.load(open(os.path.join(OUT, "_packets-B2", "round-2", "MANIFEST.json"), encoding="utf-8"))
    e = {
        "stage": "B2", "round": 2, "leg": "B2b-r2",
        "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "supersedes": "the B2a-r2 round-2 entry (one packet in 11 parts); its dispatch returned no valid reading",
        "model": "deepseek/deepseek-v4-flash-0731, on the routine reader route",
        "reader_settings": {"provider": "Relace (one provider)", "reasoning_effort": "medium"},
        "decoding": {"temperature": None, "top_p": None, "note": "set by the dispatch (fleet.py)"},
        "seeds": {"packet_order": 20261012, "cut": "consecutive cut of that order into 5 packets, largest packet minimised"},
        "n_agents": 3, "n_items": sum(v["items"] for v in man.values()),
        "packets": [{"name": k, "items": v["items"], "bytes": v["bytes"], "item_bytes": v["item_bytes"],
                     "sha256": v["sha256"]} for k, v in sorted(man.items())],
        "caps": "J, 2026-10-12: at most 15 items and 180,000 bytes of item text per packet; no item split",
        "scheme": "out/scheme.jsonl after round 1's edits, exemplars withheld (pages unchanged from B2a-r2)",
        "return_spec": "out/RETURN-B2.md with also_present, without the parts paragraph",
        "notes": "Each packet is self-contained and goes to three fresh readers. A change in agreement against round 1 is partly the reader settings.",
    }
    print(json.dumps(e, indent=1)[:1200])
    if "--write" not in sys.argv:
        return
    d.append(e)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
