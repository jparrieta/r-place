#!/usr/bin/env python3
"""C2d-01, pass 4 declaration 6: write out/_analysis/c2d_enrol_drop.txt, the concepts cited under P01's themes that
c2c_t3002_enrolments.py's pattern (C2c, unchanged) reads as a joining line, one sub:code a line, for
c2_arrow_evidence.py --drop. The pattern over-reads (it also takes short calls), so P01 without these is stricter than
the true call. Refuses to overwrite.

    python3 out/_analysis/c2d_enrol_drop.py
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
DEST = os.path.join(OUT, "_analysis", "c2d_enrol_drop.txt")
if os.path.exists(DEST):
    sys.exit("c2d_enrol_drop.txt exists; not overwritten")
LAB = re.compile(r"^(joining|volunteering|agreeing|offering|committing|signing up|pledging|promising to help|accepting|"
                 r"answering .* with|counting (themself|themselves|oneself|himself|herself) in|saying (they|he|she) "
                 r"(is|are|am|will) (in|on it|help)|heading over|coming to help|enlisting|reporting joining)", re.I)
SHORT = re.compile(r"\b(in|on it|game|help|coming|sword|down|count me)\b", re.I)
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "mem.py"), "codes", "--grep", ".", "--json", "--limit",
                    "10000000"], cwd=ROOT, capture_output=True, text=True)
codes = dict(((c["sub"], c["code_id"]), c) for c in (json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")))
els = dict((e["id"], e) for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_p4.json"), encoding="utf-8"))["elements"])
p01 = set(els["P01"]["themes"])
keys = set()
for l in open(os.path.join(OUT, "assignments_final.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    for t, cs in (r.get("support_by_theme") or {}).items():
        if t in p01:
            keys.update((r["sub"], c) for c in cs if (r["sub"], c) in codes)


def enrol(k):
    c = codes[k]
    txt = " ".join(str(c.get("text") or "").split())
    return bool(LAB.search(str(c.get("first_order") or ""))) or (len(txt.split()) <= 5 and bool(SHORT.search(txt)))


drop = sorted("%s:%s" % k for k in keys if enrol(k))
open(DEST, "w", encoding="utf-8").write("\n".join(drop) + "\n")
print("P01 concepts %d; read as joining and dropped %d; written %s" % (len(keys), len(drop), os.path.relpath(DEST, ROOT)))
