#!/usr/bin/env python3
"""C5a-01: fill the tentative arrow A21's `negative_check` (entered at C4a without it). A21 is not counted, so its
negative check is 'not-addressed'. Writes the field in model/arrows.jsonl in place and one model/history.jsonl line
with the old row as `was`. Refuses if A21 already carries a negative_check.

    python3 out/_analysis/c5_a21_negcheck.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = os.path.join(ROOT, "out", "model")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
af, hf = os.path.join(M, "arrows.jsonl"), os.path.join(M, "history.jsonl")
rows = [json.loads(l) for l in open(af, encoding="utf-8") if l.strip()]
a = [r for r in rows if r["id"] == "A21"]
if len(a) != 1 or a[0].get("negative_check"):
    sys.exit("A21 not found once, or it already carries a negative_check")
was = dict(a[0])
a[0]["negative_check"] = "not-addressed"
with open(af, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(hf, "a", encoding="utf-8") as f:
    f.write(json.dumps({"t": T, "stage": "C5", "leg": LEG, "id": "A21", "event": "field filled",
                        "move": "developing or dropping working hypotheses",
                        "why": "the tentative arrow entered at C4a lacked negative_check, which the arrow checks require; "
                               "it is not counted, so its negative check is not addressed", "was": was},
                       ensure_ascii=False) + "\n")
print("A21 negative_check set to not-addressed; history line appended")
