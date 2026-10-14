#!/usr/bin/env python3
"""C2c: copy the reviewer's validated return into out/review-C2.md below the instruction (stage C2 section 6), the
line verbatim in a code block, then the same errors and partition rendered for reading. Refuses if the return is
already there.

    python3 out/_analysis/c2c_copy_return.py [--write]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RV = os.path.join(OUT, "review-C2.md")
SRC = os.path.join(OUT, "_fleet_raw", "C2", "C2-reviewer", "r1.jsonl")

text = open(RV, encoding="utf-8").read()
if "## The return" in text:
    sys.exit("review-C2.md already carries the return; not copied again")
lines = [l for l in open(SRC, encoding="utf-8") if l.strip()]
if len(lines) != 1:
    sys.exit("expected one return line in r1.jsonl, found %d" % len(lines))
r = json.loads(lines[0])
L = ["", "## The return", "",
     "Copied from `_fleet_raw/C2/C2-reviewer/r1.jsonl` (reader r1, reissue 0, served claude-opus-5-5 through the "
     "CLI; the dispatch marked it valid). The line, verbatim:", "",
     "```json", lines[0].rstrip("\n"), "END-OF-RETURN", "```", "",
     "### The errors, as the reader wrote them", ""]
for i, e in enumerate(r["errors"], 1):
    L.append("%d. **%s**, %s. %s" % (i, e["kind"], e["where"], e["what"]))
L += ["", "### The partition, as the reader wrote it", ""]
for g in r["partition"]:
    L.append("- **%s** (%d): %s. Holds: %s" % (g["label"], len(g["members"]), ", ".join(g["members"]), g["holds"]))
L += ["", "Unplaced: %s." % "; ".join("%s (%s)" % (u["id"], u["why"]) for u in r["unplaced"]), "",
      "Differs: %s" % r["differs"], "",
      "The answers to every item are in `notes-C2.md`, under the reviewer's check (C2c).", ""]
print("\n".join(L)[:1500])
if "--write" in sys.argv:
    open(RV, "w", encoding="utf-8").write(text.rstrip("\n") + "\n" + "\n".join(L))
    print("appended to review-C2.md: %d errors, %d groups" % (len(r["errors"]), len(r["partition"])))
