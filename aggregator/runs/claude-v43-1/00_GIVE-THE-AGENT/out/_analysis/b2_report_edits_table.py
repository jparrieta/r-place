#!/usr/bin/env python3
"""B2d: the edit table for pilot_report.md, written to out/_analysis/b2_report_edits_table.md: one row per theme
edited (the 202 word-for-word mirrors of kind gate-check counted apart), with its lines by field, the rounds, the
kinds and what caused them (items of the hard set, or "gates: A|B" for a pair read without a reader's split)."""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ed = [json.loads(x) for x in open(os.path.join(OUT, "scheme_edits.jsonl"), encoding="utf-8") if x.strip()]
mirrors = collections.Counter(e["theme"] for e in ed if e.get("kind") == "gate-check")
by = collections.defaultdict(list)
for e in ed:
    if e.get("kind") != "gate-check":
        by[e["theme"]].append(e)
L = ["| theme | lines by field | rounds | kind | caused by | mirrors |", "|---|---|---|---|---|---|"]
for t in sorted(set(by) | set(mirrors)):
    es = by.get(t, [])
    f = ", ".join("%s %d" % kv for kv in sorted(collections.Counter(e["field"].replace("_", " ") for e in es).items()))
    cb = sorted({c.replace("gates:", "pair ") for e in es for c in (e.get("caused_by") or [])})
    L.append("| %s | %s | %s | %s | %s | %d |" % (t, f or "-", ", ".join(sorted({str(e.get("round")) for e in es})) or "-",
             ", ".join(sorted({e.get("kind") for e in es})) or "-", ", ".join(cb).replace("|", "/") or "-", mirrors.get(t, 0)))
open(os.path.join(OUT, "_analysis", "b2_report_edits_table.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("%d rows; edits %d, mirrors %d" % (len(L) - 2, sum(len(v) for v in by.values()), sum(mirrors.values())))
