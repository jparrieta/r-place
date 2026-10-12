#!/usr/bin/env python3
"""B2b-r2-p2: write out/return_waivers.jsonl from out/_analysis/b2_r2_return_problems.txt (J, QB2-009,
2026-10-12 09:27 Berlin: no reissue of round 2; the 16 listed lines are waived by name). One waiver per
return line: round_dir, file, item (as the line writes it), reason (the problem as listed), ruled_by.
Refuses to write over an existing waiver file. Dry run unless --write."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
rows = []
for line in open(os.path.join(OUT, "_analysis", "b2_r2_return_problems.txt"), encoding="utf-8"):
    m = re.match(r"^(P03-r2-\d/r\d\.jsonl) line (\d+) (\S+/t\d+): (.*)$", line.rstrip("\n"))
    if m:
        rows.append({"round_dir": "_fleet_raw/B2/round-2", "file": m.group(1), "item": m.group(3),
                     "line": int(m.group(2)), "reason": m.group(4),
                     "ruled_by": "J 2026-10-12 QB2-009"})
print("%d waivers" % len(rows))
for r in rows:
    print("  %s %s line %d: %s" % (r["file"], r["item"], r["line"], r["reason"][:90]))
if len(rows) != 16:
    sys.exit("expected the 16 lines of the list")
p = os.path.join(OUT, "return_waivers.jsonl")
if "--write" in sys.argv:
    if os.path.exists(p):
        sys.exit("%s exists" % p)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote %s" % p)
