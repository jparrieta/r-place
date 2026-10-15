#!/usr/bin/env python3
"""C5b: the sentences of the amended declarations that the declaration prose rule puts in question (the rule's word
lists: universal, comparative, causal, cyclic), read from fourth/fourth.jsonl (prose, changed, mistaken_for) and
dimensions.jsonl (construct changed and mistaken_for, the C5a-02 extension). Prints the count and bytes per
declaration; with --json writes them to out/_analysis/c5b_in_question.json. A measure for the packet budget; it
judges nothing.

    python3 out/_analysis/c5b_in_question.py [--json]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
WORDS = {
    "universal": ["every", "all", "no one", "nothing", "never", "always", "any", "only"],
    "comparative": ["more", "most", "less", "fewer", "strongest", "than", "as much as"],
    "causal": ["because", "so", "makes", "brings", "turns into", "leads to", "keeps alive", "why", "explains"],
    "cyclic": ["again", "each time", "returns", "renews", "a loop"],
}
PAT = {k: re.compile(r"\b(%s)\b" % "|".join(re.escape(w) for w in v), re.I) for k, v in WORDS.items()}


def sentences(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'\[(])", t) if s]


def kinds(s):
    bare = re.sub(r"\"[^\"]*\"|'[^']*'|\[[^\]]*\]", " ", s)   # members' quotes and citations are not the claim
    return [k for k, p in PAT.items() if p.search(bare)]


rows = []
for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        rows.append((r["id"], r.get("name"), {"prose": r.get("prose"), "changed": r.get("changed"),
                                               "mistaken_for": r.get("mistaken_for")}))
for l in open(os.path.join(OUT, "dimensions.jsonl"), encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        c = r.get("construct") or {}
        rows.append((r["id"], r.get("label"), {"changed": c.get("changed"), "mistaken_for": c.get("mistaken_for")}))
out, tot_n, tot_b = [], 0, 0
for i, name, fields in rows:
    hit = []
    for f, t in fields.items():
        if isinstance(t, str):
            for s in sentences(t):
                k = kinds(s)
                if k:
                    hit.append({"field": f, "kinds": k, "sentence": s})
    b = sum(len(h["sentence"].encode("utf-8")) for h in hit)
    tot_n += len(hit)
    tot_b += b
    out.append({"id": i, "name": name, "in_question": hit})
    print("%-7s %-30s %2d sentences %5d bytes" % (i, (name or "")[:30], len(hit), b))
print("total: %d sentences, %d bytes" % (tot_n, tot_b))
if "--json" in sys.argv:
    json.dump(out, open(os.path.join(OUT, "_analysis", "c5b_in_question.json"), "w"), indent=1, ensure_ascii=False)
