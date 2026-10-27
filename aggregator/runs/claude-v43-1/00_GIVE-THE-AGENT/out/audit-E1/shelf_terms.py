#!/usr/bin/env python3
"""E1 section 7, the critique shelf (E1b-08): the passages of the two longer critique files that name the stage's five
objections, with their pages, so that each can be cited by file and page. Prints JSON.

    python3 out/audit-E1/shelf_terms.py > out/audit-E1/shelf_terms.json

The rule, declared before the run (E1b-08): the files are shelves/read/osullivan-ravasi-2026.md and schildt-2026.md
(Jowsey et al. 2025 and the call for papers were read whole). For each objection, its terms: invented quotes
(hallucinat, fabricat, invent, made-up, confabul); reasoning handed to the machine (outsourc, delegat, offload,
automat, replace the researcher); an opaque process (opaque, black box, transparen, audit trail, traceab); craft and
reflexivity (reflexiv, craft, tacit, positionality, intuition); more output instead of better (volume, productivity,
faster, more papers, scale). The first three hits per term group per file, each with its page (the extraction's
'--- page N ---' marks) and 240 characters around it, white space collapsed.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GROUPS = {"invented quotes": r"hallucinat|fabricat|invent|made-up|confabul",
          "reasoning handed to the machine": r"outsourc|delegat|offload|automat|replace the researcher",
          "an opaque process": r"opaque|black box|transparen|audit trail|traceab",
          "craft and reflexivity": r"reflexiv|craft|tacit|positionality|intuition",
          "more output instead of better": r"volume|productivity|faster|more papers|at scale"}


def main():
    out = {}
    for f in ("osullivan-ravasi-2026.md", "schildt-2026.md"):
        t = open(os.path.join(ROOT, "shelves", "read", f), encoding="utf-8", errors="replace").read()
        pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"--- page (\d+) ---", t)]
        def page(i):
            p = 0
            for s, n in pages:
                if s <= i:
                    p = n
            return p
        res = {}
        for g, pat in GROUPS.items():
            hits = []
            for m in re.finditer(pat, t, re.I):
                w = " ".join(t[max(0, m.start() - 120):m.end() + 120].split())
                hits.append({"page": page(m.start()), "text": w})
                if len(hits) == 3:
                    break
            res[g] = {"count": len(re.findall(pat, t, re.I)), "first": hits}
        out[f] = res
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
