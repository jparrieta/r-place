#!/usr/bin/env python3
"""C3b, stage C3 section 4a: rewrite the mechanisms of A12 (the one-line answer to a call) and A16 (an attack call
refused inside the room) from conversation analysis (adjacency pairs and preference organization; recalled: Schegloff
and Sacks 1973, Pomerantz 1984, Levinson 1983), which the abductive read of C3b tested (c3b_ca_tally.txt).

On each arrow line of model/arrows.jsonl: `mechanism` rewritten, the stage C2 sentence kept as `mechanism_C2`;
`mechanism_fails_if` re-read and extended, the stage C2 clause kept as `mechanism_fails_if_C2`; `mechanism_source`
from-literature; `work`; `mechanism_test`; `abductive` and `prompted_by`. Strength, counts, instances and the order
clause are untouched. One model/history.jsonl line per arrow (stage C3, the old line as `was`). Refuses to run twice.

    python3 out/_analysis/c3b_arrows_rewrite.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
AP = os.path.join(OUT, "model", "arrows.jsonl")
HP = os.path.join(OUT, "model", "history.jsonl")
WORK = "conversation analysis: Schegloff and Sacks 1973; Pomerantz 1984; Levinson 1983 (recalled)"
PROMPT = "Schegloff and Sacks 1973"
TEST = ("C3b abductive read (c3b_ca_pairs.py, c3b_ca_codes.json, c3b_ca_tally.txt): 57 seeded pairs whose first part "
        "calls for or proposes an attack, read whole by the analyst alone. Refusals gave a reason in 23 of 38, acceptances "
        "in 2 of 14 (one-sided Fisher p 0.003). Refusals were not longer (median 9.5 words against 11.5). The theme a "
        "reply sits under does not track its stance.")
NEW = {
    "A12": {
        "mechanism": ("A call is the first part of a pair: posted to a thread, it makes an answer from each reader the next "
                      "thing due. Joining is the answer the call prefers, so it comes bare, one line that commits and gives "
                      "no reason ('I'm in'); declining is the dispreferred answer and comes with a reason. A bare one-line "
                      "join is the ordinary way a call is accepted."),
        "fails_add": (" Or joins answer a call with reasons as often as refusals do, or refusals come as bare as joins. "
                      "Tested on attack calls only (C3b); on calls to place this clause is not addressed."),
    },
    "A16": {
        "mechanism": ("A call to attack makes an answer from the room due in its thread. Members who do not want the attack "
                      "refuse it, rein in the attackers or apologise to the target; refusing is the dispreferred answer, so "
                      "it comes with a reason, and the reason states the room's norm or the attack's cost ('Nah, keep "
                      "/r/place neutral.'; 'Why? That'll just cause them to want to attack us')."),
        "fails_add": " Or refusals of attack calls come as bare as acceptances.",
    },
}
hist = [json.loads(l) for l in open(HP, encoding="utf-8") if l.strip()]
if any(h.get("leg") == LEG and h.get("id") in NEW for h in hist):
    sys.exit("a %s history line exists for %s; not written again" % (LEG, ", ".join(NEW)))
rows = [json.loads(l) for l in open(AP, encoding="utf-8") if l.strip()]
lines = []
for r in rows:
    if r["id"] not in NEW:
        continue
    was = dict(r)
    n = NEW[r["id"]]
    r["mechanism_C2"] = r["mechanism"]
    r["mechanism"] = n["mechanism"]
    r["mechanism_fails_if_C2"] = r["mechanism_fails_if"]
    r["mechanism_fails_if"] = r["mechanism_fails_if"].rstrip() + n["fails_add"]
    r["mechanism_source"] = "from-literature"
    r["work"] = WORK
    r["mechanism_test"] = TEST
    r["abductive"] = True
    r["prompted_by"] = PROMPT
    lines.append({"t": T, "stage": "C3", "leg": LEG, "id": r["id"], "event": "mechanism rewritten",
                  "move": "relating or contrasting",
                  "why": "stage C3 section 4a: the mechanism taken from conversation analysis (adjacency pairs, preference "
                         "organization), the distant field that fits this move; tested on attack calls at C3b, the "
                         "account half holding and the length half not; the order count and strength are unchanged",
                  "was": was, "abductive": True, "prompted_by": PROMPT,
                  "stamp": {"leg": LEG, "prompted_by": {"work": WORK, "theme": "T4-020, T4-015"}}})
if len(lines) != len(NEW):
    sys.exit("not every arrow was found")
with open(AP, "w", encoding="utf-8") as f:
    f.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with open(HP, "a", encoding="utf-8") as f:
    f.write("".join(json.dumps(h, ensure_ascii=False) + "\n" for h in lines))
print("rewritten: %s; history lines appended: %d" % (", ".join(h["id"] for h in lines), len(lines)))
