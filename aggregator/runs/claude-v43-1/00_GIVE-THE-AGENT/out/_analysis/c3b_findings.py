#!/usr/bin/env python3
"""C3b: append the two findings the abductive reads of this leg produced, with literature ids. Numbers are read from
c3b_ca_tally.txt and c3b_threshold_codes.json, not typed. Refuses to run if F-014 or F-015 exists.

  F-014  refusals of a call carry a reason, acceptances come bare (conversation analysis); evidence for the rewritten
         mechanisms of A12 and A16 and for the concept's form.
  F-015  the rooms' judgments of their own numbers do not rest on who answered (threshold models); bounds the concept.

    python3 out/_analysis/c3b_findings.py
"""
import collections, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
A = os.path.join(OUT, "_analysis")
LEG = open(os.path.join(ROOT, ".leg")).read().strip()
T = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
FP = os.path.join(OUT, "findings.jsonl")
rows = [json.loads(l) for l in open(FP, encoding="utf-8") if l.strip()]
if any(r["id"] in ("F-014", "F-015") for r in rows):
    sys.exit("F-014 or F-015 exists; not written again")
tally = open(os.path.join(A, "c3b_ca_tally.txt"), encoding="utf-8").read()
m = re.search(r"sampled (\d+); counted .*? (\d+); set aside (\d+)", tally)
acc = re.search(r"accounts, refusals (\d+) of (\d+) against acceptances (\d+) of (\d+); one-sided Fisher p ([\d.]+)", tally)
wa = re.search(r"accept\s+\d+ pairs, account\s+\d+ \([\d.]+\), median words ([\d.]+)", tally)
wr = re.search(r"refuse\s+\d+ pairs, account\s+\d+ \([\d.]+\), median words ([\d.]+)", tally)
if not (m and acc and wa and wr):
    sys.exit("could not read c3b_ca_tally.txt")
th = json.load(open(os.path.join(A, "c3b_threshold_codes.json"), encoding="utf-8"))["codes"]
cnt = [c for c in th if c["counted"]]
g = collections.Counter(c["ground"] for c in cnt)
thread = sum(v for k, v in g.items() if "thread" in k)
f14 = {"stage": "C3", "leg": LEG, "id": "F-014", "tier": "arrow", "warrant": "read", "status": "standing", "t": T,
       "statement": ("Refusals of a call carry a reason; acceptances come bare. Of %s seeded reply pairs, %s had a first "
                     "part that calls for or proposes an attack. Read for stance, refusals gave a reason in %s of %s and "
                     "acceptances in %s of %s (one-sided Fisher p %s). Refusals were not longer (median %s words against "
                     "%s). In a refusal the reason states the room's norm or the attack's cost: 'Why? That'll just cause "
                     "them to want to attack us' (uoft/c0115)." % (m.group(1), m.group(2), acc.group(1), acc.group(2),
                                                                    acc.group(3), acc.group(4), acc.group(5), wr.group(1),
                                                                    wa.group(1))),
       "evidence": ["out/_analysis/c3b_ca_pairs.py", "out/_analysis/c3b_ca_sample.json", "out/_analysis/c3b_ca_codes.json",
                    "out/_analysis/c3b_ca_tally.txt", "uoft:c0115", "nyjets:c0087", "placestart:c0117",
                    "DestinyTheGame:c0008"],
       "bound": ("Coded by the analyst alone under rules written before reading. First parts are attack calls only; calls "
                 "to place were not tested. The theme a reply sits under does not track its stance, so the pairs were drawn "
                 "by theme and coded by reading. Reply intervals were not read as conversation analysis's delay, since "
                 "posting latency is not turn-internal delay."),
       "refuted_by": ["a second coder, reading the same pairs under the same rules, finding reasons about as often in "
                      "acceptances as in refusals"],
       "literature": ["Schegloff and Sacks 1973", "Pomerantz 1984", "Levinson 1983"], "abductive": True,
       "prompted_by": "Schegloff and Sacks 1973",
       "why": "stage C3b, section 4a: the distant field's prediction for the call and its answers, tested"}
f15 = {"stage": "C3", "leg": LEG, "id": "F-015", "tier": "concept", "warrant": "read", "status": "standing", "t": T,
       "statement": ("The rooms do not read their numbers off the replies to a call (weak: an absence claim). Of %d seeded "
                     "first turns on the doubt-about-numbers theme, %d judge the room's own hands, and %d of them rest on "
                     "who answered or is present in the thread. %d rest on the size of the sub, fan base or game, %d on "
                     "the canvas, %d on both, and %d on nothing: 'Sadly I don't think we have enough people to make "
                     "anything :(' (sabres/c0008)." % (len(th), len(cnt), thread, g.get("readership", 0),
                                                       g.get("canvas", 0), g.get("readership and canvas", 0),
                                                       g.get("none", 0))),
       "evidence": ["out/_analysis/c3b_threshold_sample.py", "out/_analysis/c3b_threshold_sample.json",
                    "out/_analysis/c3b_threshold_codes.json", "sabres:c0008", "MiamiHurricanes:c0009", "planetside:c0059",
                    "torontoraptors:c0060"],
       "bound": ("Coded by the analyst alone; one theme, one sample of 40 rooms. The readership ground was not foreseen "
                 "when the rules were written and is coded apart. A thread ground does appear outside the sample: 'I mean "
                 "I want to but nobody's here' (torontoraptors/c0060), in reply to an attack call. The claim is about "
                 "small rooms writing in public and is marked weak."),
       "refuted_by": ["a wider read of judgments of numbers in which a clear share cite the replies or the people present"],
       "literature": ["Granovetter 1978"], "abductive": True, "prompted_by": "Granovetter 1978",
       "why": "stage C3b, section 4b: the concept's claimed function (the replies as the room's head count) tested against "
              "the threshold models' prediction"}
with open(FP, "a", encoding="utf-8") as f:
    f.write(json.dumps(f14, ensure_ascii=False) + "\n" + json.dumps(f15, ensure_ascii=False) + "\n")
print(f14["statement"])
print(f15["statement"])
