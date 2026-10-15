#!/usr/bin/env python3
"""C5c-11, problem 2 (the reason test): append F-023 (replies to calls to place, and what of the replies survives in the
coded record) and a superseding F-014 line (the asymmetry scoped to written, coded replies) to out/findings.jsonl.
Counts from c5c11_survival.py and c5c11_place_tally.py. Refuses if F-023 exists or F-014 has a line from this leg.

    python3 out/_analysis/c5c11_findings.py
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, "out", "findings.jsonl")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
rows = [json.loads(l) for l in open(F, encoding="utf-8") if l.strip()]
if any(r["id"] == "F-023" for r in rows) or any(r["id"] == "F-014" and r.get("leg") == LEG for r in rows):
    sys.exit("F-023 exists, or F-014 already has a line from this leg")
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
f23 = {"stage": "C5", "leg": LEG, "id": "F-023", "tier": "arrow", "warrant": "read", "status": "standing", "t": T,
       "statement": "Written replies to calls to place show the same asymmetry as replies to attack calls, on few "
                    "refusals, and most calls get no written reply at all. Of 80 seeded first coded replies to calls to "
                    "place, 63 answer a call: 31 accept, 3 refuse, 2 are mixed and 27 take no stance. Refusals gave a "
                    "reason in 3 of 3 ('I've seen too much /r/place spam today already. So...no thanks.' "
                    "[polyamory/c0002]) and acceptances in 6 of 31 (one-sided Fisher p 0.014); 25 acceptances came bare "
                    "('I'll help.' [PUBATTLEGROUNDS/c0050]). In the record, 1,029 of 1,949 calls to place (0.53) and 883 "
                    "of 1,565 attack calls (0.56) carry no direct reply by another member; of the direct replies written, "
                    "0.21 and 0.26 carry no coded text, and about 0.01 have a deleted author.",
       "evidence": ["out/_analysis/c5c11_survival.py", "out/_analysis/c5c11_survival.json",
                    "out/_analysis/c5c11_place_pairs.py", "out/_analysis/c5c11_place_sample.json",
                    "out/_analysis/c5c11_place_codes.json", "out/_analysis/c5c11_place_tally.py",
                    "polyamory:c0002", "PUBATTLEGROUNDS:c0050", "sbu:c0009", "ScottPilgrim:c0002"],
       "bound": "Coded by the analyst alone under rules written before reading; first coded direct replies only, one per "
                "room. Only what was written and coded can be read: an acceptance done by placing leaves no reply, a "
                "silent refusal leaves none either, and a reply that left no coded text cannot be read for its stance. "
                "So the ratio of stances in writing is not the room's, and the refusal side rests on 3 replies.",
       "refuted_by": ["a larger draw of written refusals to calls to place in which they give a reason no more often than "
                      "acceptances"],
       "literature": ["Okhuysen and Bechky 2009"], "abductive": True,
       "prompted_by": "J's framing (C5c-07, C5c-11): omission against commission; what is heard less may have survived "
                      "less in the record",
       "why": "problem 2 of the serial work: F-014 was counted on attack calls only, with its ratio set by its draw; this "
              "reads calls to place, and counts what of the replies survives in the coded record before the asymmetry "
              "is read"}
f14 = dict([r for r in rows if r["id"] == "F-014"][-1])
old = "Refusals of a call carry a reason; acceptances come bare."
if not f14["statement"].startswith(old):
    sys.exit("F-014's statement does not begin as expected")
f14["statement"] = f14["statement"].replace(old, "In written, coded replies to attack calls, refusals mostly carry a "
                                                 "reason and acceptances mostly come bare.", 1)
f14["bound"] = f14["bound"] + (" At C5c-11: the 38 refusals against 14 acceptances were set by the draw (up to 40 rooms "
                               "per kind), not by the rooms; more than half of all calls carry no written reply, and a "
                               "quarter of the written replies to attack calls carry no coded text, so the asymmetry is a "
                               "fact about written, coded replies. Replies to calls to place show it too, on 3 refusals "
                               "(F-023).")
f14.update({"stage": "C5", "leg": LEG, "status": "bounded", "supersedes": "F-014", "t": T})
with open(F, "a", encoding="utf-8") as f:
    f.write(json.dumps(f23, ensure_ascii=False) + "\n")
    f.write(json.dumps(f14, ensure_ascii=False) + "\n")
print("appended F-023 and a superseding F-014; findings.jsonl now %d lines" % (len(rows) + 2))
