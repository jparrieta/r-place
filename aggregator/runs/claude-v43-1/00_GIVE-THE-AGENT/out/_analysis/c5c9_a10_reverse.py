#!/usr/bin/env python3
"""C5c-09, A10's added read (codes logged first, diary C5c-09): the rooms that voice doubt about their hands (K02), whose
record says the work was lost (work_remained), and that carry no move (P10). Writes their first two K02 concepts, whole,
through c2_first_concepts.py, to c5c9_a10_reverse_read.txt; prints the rooms and the file's size.

    python3 out/_analysis/c5c9_a10_reverse.py
"""
import collections, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
A = os.path.join(OUT, "_analysis")
end = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"))}
carry = collections.defaultdict(set)
for l in open(os.path.join(OUT, "assignments_final.jsonl")):
    r = json.loads(l)
    for t3, codes in (r.get("support_by_theme") or {}).items():
        if codes:
            carry[t3].add(r["sub"])
els = {e["id"]: e for e in json.load(open(os.path.join(A, "c2_elements_c5c2.json")))["elements"]}


def rooms(eid):
    s = set()
    for t in els[eid].get("themes") or []:
        s |= carry.get(t, set())
    return s


x = sorted(s for s in rooms("K02") - rooms("P10") if end.get(s, {}).get("work_remained") == "lost")
p = subprocess.run([sys.executable, os.path.join(A, "c2_first_concepts.py"), "--elements", "c2_elements_c5c2.json",
                    "--pair", "K02:P10", "--rooms", ",".join(x), "--n", "2"], cwd=ROOT, capture_output=True, text=True)
open(os.path.join(A, "c5c9_a10_reverse_read.txt"), "w", encoding="utf-8").write(p.stdout)
print("%d rooms: %s" % (len(x), ", ".join(x)))
print("c5c9_a10_reverse_read.txt: %d bytes" % len(p.stdout.encode("utf-8")))
