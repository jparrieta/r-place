#!/usr/bin/env python3
"""A21's order test, part 2 (D3a-27), version 2: the census of my rulings, by room, with the
correction families named by id as ruled (the pair rings in A21-restrict.jsonl and the instantiate
rejects by their reasons). Supersedes d3_a21_census.py, whose phrase search missed dbz-066 and moved
two lines between families.

  python3 out/_analysis/d3_a21_census_v2.py
"""
import json

R = "out/_analysis/d3_rulings/"
F1_RESTRICT = ["ScottPilgrim-031", "TsundereSharks-058", "argentina-067", "asexuality-033", "buffalobills-037",
               "croatia-060", "dallasstars-029", "destiny-022", "dota2-039", "funhaus-051", "gravityfalls-028",
               "greece-034", "jerma985-036", "katawashoujo-051", "lakers-081", "maryland-019", "masseffect-056",
               "newzealand-057", "rit-029", "straya-057", "telegram-025", "thepointing-053", "transformers-056",
               "uoft-036", "uva-052", "weezer-063"]
F2_RESTRICT = ["FloydVsVoid-033", "PlaceNL-037", "adventuretime-051", "denmark-067", "italy-051", "rainbowgrid-023",
               "singapore-035", "switzerland-056", "turkey-029", "uiuc-031"]
F1_INST = ["AMD-032", "Goodboye-066", "Peru-029", "canada-028", "dbz-066", "finland-056", "polska-064",
           "splatoon-055", "theitalyplace-064", "ukraine-045"]
F2_INST = ["detroitredwings-043", "norge-030", "texas-052"]


def load(name):
    return [json.loads(l) for l in open(R + name) if l.strip()]


def room(aid):
    return aid.rsplit("-", 1)[0]


rul = {}
for f in ("A21-inst.jsonl", "A21-restrict.jsonl", "A21-addstep.jsonl", "A21-absent.jsonl"):
    for r in load(f):
        rul[r["adaptation"]] = r
for i in F1_RESTRICT + F2_RESTRICT:
    assert rul[i]["decision"] == "accept" and rul[i]["kind"] == "correction", i
for i in F1_INST + F2_INST:
    assert rul[i]["decision"] == "reject", i
corr = [i for i, r in rul.items() if r.get("kind") == "correction"]
assert sorted(corr) == sorted(F1_RESTRICT + F2_RESTRICT), "a correction outside the two rings"

order = set()
for i, r in rul.items():
    op_absent = i in {x["adaptation"] for x in load("A21-absent.jsonl")}
    if r["decision"] == "accept" and r.get("kind") == "specification" and not op_absent:
        order.add(room(i))
    if r["decision"] == "reject" and op_absent:
        order.add(room(i))
f1 = {room(i) for i in F1_RESTRICT + F1_INST}
f2 = {room(i) for i in F2_RESTRICT + F2_INST}
reverse = f1 | f2
print("rooms showing A21's order:", len(order))
print("rooms with the P21 form first:", len(reverse), "(F1 at the making %d, F2 no agreement %d, in both families %d)"
      % (len(f1), len(f2), len(f1 & f2)))
both = order & reverse
print("rooms in both the order and the reverse:", len(both), sorted(both))
print("rooms with an episode:", len(order | reverse), " holds:", len(order),
      " share: %.3f" % (len(order) / len(order | reverse)))
