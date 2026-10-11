"""B1e: check one family's draft lines before assembly.

Checks: every field of section 4 present and non-empty (gate_parts may be null); the name 2 to 5 words and none of
the four problem words; discriminator ids among the 197 themes; the family as in b1e_families.tsv; three
exemplars, each quote found in the words cite.py returns for its sub and code (whitespace made single), each
rival a code of the same room (cite.py answers for it).

usage: python3 out/_analysis/b1e_check_draft.py out/_analysis/b1e_draft_G01.jsonl
"""
import json
import re
import subprocess
import sys

PROBLEMS = ("division", "allocation", "reward", "information")
KEYS = ("id", "name", "gloss", "family", "must_show", "must_not_show", "decide_when_both", "discriminators",
        "varies", "is_not", "gate_parts", "exemplars", "two_or_half")
fam = {}
for i, x in enumerate(open("out/_analysis/b1e_families.tsv", encoding="utf-8")):
    if i == 0 or not x.strip():
        continue
    f, _, ts = x.rstrip("\n").split("\t")
    for t in ts.split(","):
        fam[t] = f
cache = {}


def words(sub, code):
    if (sub, code) not in cache:
        out = subprocess.run(["python3", "tools/cite.py", "--room", sub, "--code", code, "--stage", "B1"],
                             capture_output=True, text=True).stdout
        m = [x for x in out.splitlines() if x.startswith('"')]
        q = None
        if m:
            mm = re.match(r'^"(.*)"\s+\[%s/%s\]' % (re.escape(sub), re.escape(code)), m[0], re.I)
            q = " ".join((mm.group(1) if mm else m[0]).split())
        cache[(sub, code)] = q
    return cache[(sub, code)]


problems = 0
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
for r in rows:
    t = r.get("id")
    out = []
    for k in KEYS:
        if k not in r:
            out.append("lacks " + k)
        elif k not in ("gate_parts", "discriminators", "exemplars") and not str(r[k]).strip():
            out.append("empty " + k)
    nm = [w for w in re.split(r"[\s/,]+", r.get("name", "").strip()) if w]
    if not 2 <= len(nm) <= 5:
        out.append("name has %d words" % len(nm))
    if any(w.lower().strip(".:;()") in PROBLEMS for w in nm):
        out.append("name holds a problem word")
    if fam.get(t) != r.get("family"):
        out.append("family %s, tsv says %s" % (r.get("family"), fam.get(t)))
    for d in r.get("discriminators") or []:
        if d.get("vs") not in fam:
            out.append("discriminator vs %s unknown" % d.get("vs"))
        if not str(d.get("question", "")).strip():
            out.append("discriminator without question")
    ex = r.get("exemplars") or []
    if len(ex) < 3:
        out.append("%d exemplars" % len(ex))
    for e in ex:
        w = words(e["sub"], e["code_id"])
        if w is None:
            out.append("no words for %s/%s" % (e["sub"], e["code_id"]))
        elif " ".join(e["quote"].split()) not in w:
            out.append("quote not in %s/%s" % (e["sub"], e["code_id"]))
        for rv in e.get("rivals") or []:
            if words(e["sub"], rv) is None:
                out.append("rival %s not in %s" % (rv, e["sub"]))
    print("%s %s: %s" % (t, r.get("name"), "; ".join(out) if out else "ok"))
    problems += len(out)
print("%d lines, %d problems" % (len(rows), problems))
