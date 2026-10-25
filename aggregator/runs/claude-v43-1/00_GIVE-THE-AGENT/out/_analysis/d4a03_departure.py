#!/usr/bin/env python3
"""D4a-03: append one line to out/departures.jsonl (contract rule 10: a departure is declared before the act),
recording that stage D4's comparison runs on chunk-comparison-v1.1, the engine J had patched for QD4-002, not on
the chunk-comparison-v1 the stage file names. Checks that the engine's VERSION is v1.1 and records its sha256.
Without --write it prints the line.

    python3 out/_analysis/d4a03_departure.py [--write]
"""
import argparse, hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
eng = os.path.join(ROOT, "tools", "chunk_compare.py")
src = open(eng, encoding="utf-8").read()
ver = re.search(r"VERSION='([^']+)'", src).group(1)
assert ver == "chunk-comparison-v1.1", ver
sha = hashlib.sha256(open(eng, "rb").read()).hexdigest()
line = {"stage": "D4", "leg": "D4a-03",
        "provision": "stage D4 section 5: the comparison by 'this versioned engine' (chunk-comparison-v1), "
                     "python3 tools/chunk_compare.py --out out --store package/store",
        "why": ("QD4-002 (J, 25 October, 19:48 and 19:54 Berlin, option a): v1 raised on the 335 second-order themes "
                "placed only on the two third-order residue themes that no fourth-order theme gathers (T3-017, "
                "T3-133), while the stage file counts unplaced concepts apart. The harness owner patched the engine "
                "and its trusted copy identically to %s (sha256 %s): a theme placed only on residue is counted with "
                "the unplaced concepts and reported apart (residue_themes, residue_concepts); a theme also placed on "
                "a gathered node keeps that node. The change is recorded in the harness's own record. I run the "
                "patched engine with the stage file's defaults and report each room's residue share beside the "
                "comparison." % (ver, sha)),
        "what_following_it_would_have_cost": ("Under v1 the comparison could not run at all, so stage D4 could not "
                                              "close; the projections, the handback and the interview wait on it."),
        "engine_version": ver, "engine_sha256": sha}
print(json.dumps(line, ensure_ascii=False))
if not a.write:
    print("dry run: nothing written")
    raise SystemExit(0)
p = os.path.join(ROOT, "out", "departures.jsonl")
with open(p, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
print("departures.jsonl now %d lines" % sum(1 for l in open(p, encoding="utf-8") if l.strip()))
