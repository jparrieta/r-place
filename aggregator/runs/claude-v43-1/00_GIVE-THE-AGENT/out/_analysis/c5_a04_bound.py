#!/usr/bin/env python3
"""C5a-02: add to A04's bound the result of the P08 test (c5_p08_codes.json, c5_p08_tally.py): in the rooms where
border talk comes first, the first border talk mostly offers terms before any damage. Appends a sentence to A04's
`bound` in model/arrows.jsonl, in place, and writes one model/history.jsonl line with the old row as `was`. The count,
the strength and the order statement do not change. Refuses if A04 already carries the sentence.

    python3 out/_analysis/c5_a04_bound.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "out", "model")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
ADD = (" At C5a-02, the first border talk in a seeded sample of 40 of the 166 rooms where border talk comes first was "
       "read: in 34 of the 38 that bear on it, members propose or ask a border, space, a truce or a deal and name no "
       "damage to their own work (28 of 38 if every doubtful code is turned); 4 answer damage. Where border talk comes "
       "first, it mostly offers terms before any damage.")
af, hf = os.path.join(M, "arrows.jsonl"), os.path.join(M, "history.jsonl")
rows = [json.loads(l) for l in open(af, encoding="utf-8") if l.strip()]
a = [r for r in rows if r["id"] == "A04"]
if len(a) != 1 or "At C5a-02" in (a[0].get("bound") or ""):
    sys.exit("A04 not found once, or it already carries the C5a-02 sentence")
was = dict(a[0])
a[0]["bound"] = (a[0].get("bound") or "") + ADD
with open(af, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(hf, "a", encoding="utf-8") as f:
    f.write(json.dumps({"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "stage": "C5", "leg": LEG, "id": "A04", "event": "bounded", "move": "relating or contrasting",
                        "why": "the sketches put P08 in two places (terms offered before damage, talk after it); a test "
                               "with rules written first read the first border talk in 40 of the 166 rooms where A04's "
                               "order fails; the result bounds A04 with a count; no new element (forbidden at C5) and no "
                               "recut, since the two differ in time and not in kind",
                        "evidence": ["out/_analysis/c5_p08_sample.py", "out/_analysis/c5_p08_sample.json",
                                     "out/_analysis/c5_p08_codes.json", "out/_analysis/c5_p08_tally.py"],
                        "was": was}, ensure_ascii=False) + "\n")
print("A04 bound extended; history line appended")
