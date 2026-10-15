#!/usr/bin/env python3
"""C5a-01, the declaration prose pass: for each given fourth-order theme, print its construct block from
fourth/fourth.jsonl (gloss, declared, source, prose, changed, mistaken_for, disconfirm), with every sentence of prose,
changed and mistaken_for numbered and flagged by the rule's word classes (universal, comparative, causal, cyclic),
then each member's rule 5 line and exemplar quotes, and the theme's material quotes, all read from structure-C4.md.
The flags only point; the rule is applied by reading. Writes nothing.

    python3 out/_analysis/c5_decl_view.py T4-xxx [T4-yyy ...]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
txt = open(os.path.join(OUT, "structure-C4.md"), encoding="utf-8").read()
t4 = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(OUT, "fourth", "fourth.jsonl"), encoding="utf-8"))}
FLAGS = {
    "universal": r"\b(every|all|no one|nobody|nothing|never|always|any|only|none|whole)\b",
    "comparative": r"\b(more|most|less|fewer|least|strongest|stronger|than|rarer|rare|as much)\b|\w+est\b",
    "causal": r"\b(because|so|makes?|made|brings?|turns?|leads?|keeps?|why|explains?|causes?|lets?|forces?|drives?|"
              r"therefore|thus|hence|until|without)\b",
    "cyclic": r"\b(again|each time|returns?|renews?|loop|cycle|repeated)\b",
}


def section(head):
    i = txt.find(head)
    j = txt.find("\n### ", i + len(head))
    return txt[i:j if j > 0 else len(txt)]


def sentences(s):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", s or "") if x.strip()]


for tid in sys.argv[1:]:
    r = t4[tid]
    print("=" * 100)
    print("%s %s | declared %s | source: %s" % (tid, r["name"], r.get("declared"), r.get("source")))
    print("gloss: %s [%s]" % (r.get("gloss"), r.get("gloss_from")))
    for f in ("prose", "changed", "mistaken_for"):
        for k, s in enumerate(sentences(r.get(f)), 1):
            fl = [n for n, pat in FLAGS.items() if re.search(pat, s, re.I)]
            print("  %s.%d [%s] %s" % (f, k, ",".join(fl) or "-", s))
    print("  disconfirm: %s" % r.get("disconfirm"))
    sec = section("### %s %s\n" % (tid, r["name"]))
    m = re.search(r"- \*\*Members:\*\* (.*)", sec)
    print("  members: %s" % (m.group(1) if m else "?"))
    for q in re.findall(r'"quote": "((?:[^"\\]|\\.)*)"', sec):
        print("    material: %s" % q)
    for mem in r["members"]:
        s3 = section("### %s " % mem)
        name = s3.splitlines()[0][4:]
        n5 = re.search(r"Three numbers \(rule 5\), gate (\w+):\*\* carries (\d+)", s3)
        print("  -- %s | gate %s, carries %s" % (name, n5.group(1) if n5 else "?", n5.group(2) if n5 else "?"))
        for js in re.findall(r'^\{"third".*\}$', s3, re.M):
            e = json.loads(js)
            print("      %s/%s h%.1f: %s" % (e["sub"], e["code_id"], e["hour_since_open"], e["quote"].replace("\n", " ")))
