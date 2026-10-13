#!/usr/bin/env python3
"""B4b: append the stage B4 blind sample's entry to out/run_manifest.json on stage A1's schema (readers' model, seed,
decoding, reader count), declaring both arms (J's rulings in the PI's message of 14:22Z, 13 October), before the first
packet leaves. Refuses a second B4b entry. Dry run unless --write.

    python3 out/_analysis/b4b_manifest.py [--write]
"""
import datetime, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")


def sha(p):
    return hashlib.sha256(open(os.path.join(OUT, p), "rb").read()).hexdigest()


def main():
    p = os.path.join(OUT, "run_manifest.json")
    d = json.load(open(p, encoding="utf-8"))
    if any(e.get("stage") == "B4" and e.get("leg") == "B4b" for e in d):
        sys.exit("run_manifest.json already holds the B4b entry")
    man = json.load(open(os.path.join(OUT, "_packets-B4", "MANIFEST.json"), encoding="utf-8"))
    smp = json.load(open(os.path.join(OUT, "_analysis", "b4b_sample.json"), encoding="utf-8"))
    rows = [json.loads(x) for x in open(os.path.join(OUT, "sample-B4.jsonl"), encoding="utf-8") if x.strip()]
    n_pk = len(man)
    e = {"stage": "B4", "leg": "B4b", "step": "the blind sample's build (stage B4 section 10)",
         "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "measures": "transmission after revision (FLEET.md): fresh readers against the settled line; not reliability",
         "model": "two arms on the same packets, reported apart and never pooled; no Claude reader",
         "arms": {
             "1": {"model": "DeepSeek V4.1 Flash (deepseek/deepseek-v4.1-flash), the routine readers of B2 and B3, for comparability",
                   "route": "the reader route arm.json sets for B4 (PLATFORM-claude.md: @preset/cheap x2 via gateway); the served model, route and provider as the dispatch records them in out/_fleet_raw/B4/arm.json",
                   "readers_per_item": 2, "replications": 2, "dispatch": "one dispatch by the operator's fleet.py; each packet to two fresh readers, never the same reader for both readings of an item",
                   "reasoning_effort": "as arm.json sets for B4 (B3's arm: medium, max_tokens 128000)",
                   "n_agents": 2 * n_pk},
             "2": {"model": "OpenAI gpt-6-astra", "reasoning_effort": "medium", "replications": 2, "readers_per_item": 2,
                   "run_by": "the Codex orchestrator on J's computer, from a copy of out/_packets-B4/, under the same RETURN-B4.md",
                   "n_agents": 2 * n_pk}},
         "decoding": {"temperature": None, "top_p": None, "note": "set by each arm's dispatch (fleet.py for arm 1, the Codex orchestrator for arm 2)"},
         "seeds": {"sample": smp["seed"], "streams": smp["streams"], "frame_order": smp["frame_order"],
                   "packets": "cut consecutively from the serving order, the largest packet as small as the caps allow (deterministic)"},
         "sample": {"items": len(rows), "strata": {"U": "250 uniform without replacement from the analysed set (7,844)",
                                                   "A": "250 uniform without replacement from the 3,288 ruled items U did not take"},
                    "strata_reported": "apart, never pooled", "ruling": "J, 12 October (replaces section 10's fifty and fifty)",
                    "unresolved_in_A": sum(1 for r in rows if r["stratum"] == "A" and r["unresolved"]),
                    "unresolved_in_U": sum(1 for r in rows if r["stratum"] == "U" and r["unresolved"]),
                    "file": "out/sample-B4.jsonl, sha256 %s (never served)" % smp["sample_sha256"]},
         "settled_line": "out/assign_final.jsonl, sha256 %s (never served)" % smp["assign_final_sha256"],
         "R": 2, "packets": n_pk, "lines_due_per_reader_set": sum(v["items"] for v in man.values()),
         "comparisons_per_arm": 2 * len(rows),
         "caps": "at most 15 items a packet (J's cap at B2 and B3) and every packet file under 50 KB (section 10); no parts",
         "packet_bytes": {"min": min(v["bytes"] for v in man.values()), "max": max(v["bytes"] for v in man.values())},
         "items_per_packet": {"min": min(v["items"] for v in man.values()), "max": max(v["items"] for v in man.values())},
         "exemplars": "none served", "bag_flags": "none served", "sibling_blocks": "none served",
         "shared_pages": "index.md and G01.md to G21.md, byte for byte the pages served at B3",
         "scheme": "out/scheme_final.jsonl, sha256 %s" % sha("scheme_final.jsonl"),
         "return_spec": "out/RETURN-B4.md, sha256 %s" % sha("RETURN-B4.md"),
         "ids": "fleet ids only (out/fleet_ids.jsonl); codes_by_item in each MANIFEST entry",
         "agreement": "stage B2's definition, unchanged (notes-B2.md): Jaccard on sets, alpha with distance 1 - Jaccard and chance over pooled sets, primary beside; pass 1 only",
         "build": "out/_analysis/b4b_sample.py, b4b_packets.py, b4b_packets_check.py; out/_packets-B4/"}
    print(json.dumps(e, ensure_ascii=False)[:1500])
    if "--write" in sys.argv:
        d.append(e)
        json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("run_manifest.json now holds %d entries" % len(d))


if __name__ == "__main__":
    main()
