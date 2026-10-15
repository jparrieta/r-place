#!/usr/bin/env python3
"""C5c-09, A10's rule 6 check and its tally. Rooms carrying K02 (doubt about the room's numbers or room) and P10 (the
move), by cited concepts as in the order tests (c2_elements_c5c2.json, assignments_final.jsonl support_by_theme); their
work_remained (organizing_end-A1.jsonl): how many rooms could have carried a loss and a move, and how many judged their
hands too few and did not move. Then the tally of c5c9_a10_codes.json under the rule logged first. Writes nothing.

    python3 out/_analysis/c5c9_a10_rule6.py
"""
import collections, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
end = {json.loads(l)["sub"]: json.loads(l) for l in open(os.path.join(OUT, "organizing_end-A1.jsonl"))}
carry = collections.defaultdict(set)
for l in open(os.path.join(OUT, "assignments_final.jsonl")):
    r = json.loads(l)
    for t3, codes in (r.get("support_by_theme") or {}).items():
        if codes:
            carry[t3].add(r["sub"])
els = {e["id"]: e for e in json.load(open(os.path.join(OUT, "_analysis", "c2_elements_c5c2.json")))["elements"]}


def rooms(eid):
    s = set()
    for t in els[eid].get("themes") or []:
        s |= carry.get(t, set())
    return s


k, p = rooms("K02"), rooms("P10")
lost = {s for s in end if end[s]["work_remained"] == "lost"}
wr = lambda S: dict(collections.Counter(end[s]["work_remained"] for s in S if s in end))
print("rooms: K02 %d, P10 %d, both %d; K02 without P10 %d; P10 without K02 %d" % (len(k), len(p), len(k & p),
                                                                                  len(k - p), len(p - k)))
print("work_remained: all %s" % wr(set(end)))
print("  K02 and P10: %s" % wr(k & p))
print("  K02 without P10: %s" % wr(k - p))
print("  P10 without K02: %s" % wr(p - k))
print("rooms whose record says the work was lost: %d; of them carrying K02 %d, P10 %d, both %d, K02 without P10 %d" % (
    len(lost), len(lost & k), len(lost & p), len(lost & k & p), len(lost & (k - p))))
c = json.load(open(os.path.join(OUT, "_analysis", "c5c9_a10_codes.json"), encoding="utf-8"))
assert set(c["codes"]) == k & p, "coded rooms differ from the rooms carrying both"
t = collections.Counter(v["code"] for v in c["codes"].values())
j, base = t["J"], t["J"] + t["M"] + t["C"]
print("codes: %s; J of J+M+C %d of %d (%.2f); rule: stands if at least half, bounded if under a third, dropped if J <= 2"
      % (dict(t), j, base, j / base))
print("J voice: %s" % dict(collections.Counter(v["voice"] for v in c["codes"].values() if v["code"] == "J")))
print("judgment said inside a move turn: %s" % ", ".join(c["judgment_inside_move_turn"]))
