#!/usr/bin/env python3
"""B2b-r3-p3: every gate pair that touches an edited theme and is not confirmed against the current sentences of
out/scheme.jsonl, written side by side for reading (vlib.pair_lines), numbered, to out/_analysis/b2_pairs_read.txt.
Each pair is headed by its kind:
  SAME   both gates carry a question against the other, word for word the same
  DIFF   both gates carry a question against the other, worded differently
  NONE   no question either way (the pair is named only in must_not_show, decide_when_both or is_not)
Writes the file and out/_analysis/b2_pairs_list.json ([[n, a, b, kind, question-or-null]]). Reads only otherwise."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vlib

rows, name = vlib.gate_scheme(OUT)
edited = {json.loads(x).get("theme") for x in open(os.path.join(OUT, "scheme_edits.jsonl"), encoding="utf-8") if x.strip()}
rep = vlib.gate_report(rows, vlib.family_ids(OUT))
conf = vlib.gate_confirmations(OUT, rows)
pairs = sorted((sorted(p) for p in rep["pairs"] if p & edited and conf.get(p, ("none",))[0] != "confirmed"))
L, lst, kinds = [], [], {"SAME": 0, "DIFF": 0, "NONE": 0}
for n, (a, b) in enumerate(pairs, 1):
    qa = [q for v, q in vlib.discriminators(rows[a]) if v == b]
    qb = [q for v, q in vlib.discriminators(rows[b]) if v == a]
    kind = "SAME" if qa and qb and qa[0] == qb[0] else "DIFF" if qa and qb else "NONE"
    kinds[kind] += 1
    lst.append([n, a, b, kind, qa[0] if kind == "SAME" else None])
    L.append("#%d %s|%s %s" % (n, a, b, kind))
    L += vlib.pair_lines(rows, a, b)
open(os.path.join(OUT, "_analysis", "b2_pairs_read.txt"), "w", encoding="utf-8").write("\n".join(L) + "\nEND\n")
json.dump(lst, open(os.path.join(OUT, "_analysis", "b2_pairs_list.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
print("%s: %d pairs unconfirmed on edited themes; %s; %d lines written" % (name, len(pairs), kinds, len(L)))
