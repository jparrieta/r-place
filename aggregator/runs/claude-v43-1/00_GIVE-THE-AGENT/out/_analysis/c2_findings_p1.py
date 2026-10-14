#!/usr/bin/env python3
"""C2, pass 1: write the findings the model's elements cite (rule 14) and correct C01's evidence.

The elements written at C2a-01 cite F-002 to F-005, and C01 cites F-001, but at the leg's close findings.jsonl held
only F-001, the stage B1 claim about the 197 kinds. The pass 1 findings were planned and never written. This script
appends F-002 to F-006 (every number recomputed from out/_analysis/c2_arrow_evidence-p1a/b/c.txt and the placements),
points C01 at F-006 (decided order is rare) instead of the unrelated F-001, rewrites model/elements.jsonl in place
with that one change, and appends one model/history.jsonl line for it. Refuses to run twice.

    python3 out/_analysis/c2_findings_p1.py
"""
import collections, datetime, json, os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jl(p):
    with open(os.path.join(OUT, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


fin = jl("findings.jsonl")
if any(r.get("id") in ("F-002", "F-006") for r in fin):
    sys.exit("findings F-002 or F-006 already written")
t4 = jl(os.path.join("fourth", "fourth.jsonl"))
owner = dict((m, r["id"]) for r in t4 for m in r["members"])
rooms = collections.defaultdict(set)
for r in jl("assignments_final.jsonl"):
    for t in r.get("third_order") or []:
        if t in owner:
            rooms[owner[t]].add(r["sub"])
n_dec, n_rep, n_cel = len(rooms["T4-011"]), len(rooms["T4-013"]), len(rooms["T4-026"])
base = {"stage": "C2", "leg": "C2a-01", "status": "standing", "refuted_by": []}
new = [
    dict(base, id="F-002", tier="element", warrant="inferred",
         statement="After a room moves its work, calls and build reports come later less often than a shuffle of the room's "
                   "own concepts predicts: some call follows the first move in 57 of 79 rooms carrying both (0.722, null "
                   "mean 0.962) and some build report in 49 of 65 (0.754, null mean 0.939). A move returns a room to "
                   "choosing a spot more than to recruiting.",
         evidence=["out/_analysis/c2_arrow_evidence-p1c.txt", "day9:c0023", "day9:c0027"],
         bound="A corpus rate, not a claim about each room: four of the twenty pass 1 story rooms (day9, texas, scp, "
               "worldoftanks) called members in again after a loss; open in out/_questions/relocation-renewed-calls.md."),
    dict(base, id="F-003", tier="room", warrant="read",
         statement="day9 stopped organizing early, its last coordinating turn at h53.3, because its second work was "
                   "finished and held after a move ('The new location is finished!', h53.1), not because the room gave "
                   "up; a member named a diplomat at h55 and another recounted the week at the close.",
         evidence=["out/within_case.md", "day9:c0031", "day9:c0033", "day9:c0036"],
         bound="One room; the stop is read from its forest and the A1 organizing end."),
    dict(base, id="F-004", tier="element", warrant="inferred",
         statement="The close runs in order: a reported build comes before the first celebration in 182 of 282 rooms "
                   "carrying both (0.645, null mean 0.433), a celebration before the first record in 225 of 289 (0.779, "
                   "null 0.565), and a record before the first plan to carry on in 113 of 145 (0.779, null 0.563).",
         evidence=["out/_analysis/c2_arrow_evidence-p1b.txt", "out/model/arrows.jsonl"],
         bound="On the late side the record often comes first (8 of 15 rooms hold for celebration then record); "
               "carrying on can begin while the work stands (texans)."),
    dict(base, id="F-005", tier="element", warrant="inferred",
         statement="Machine hands arrive under strain: in rooms carrying both, upkeep comes before the first script or "
                   "spare account in 160 of 203 (0.788, null mean 0.603), and the reverse order holds in 41 of 203 "
                   "(0.202, null mean 0.375).",
         evidence=["out/_analysis/c2_arrow_evidence-p1b.txt", "out/_analysis/c2_arrow_evidence-p1c.txt", "ubc:c0090"],
         bound="Where a room scripted the building or an attack from the start, machine hands come first "
               "(canucks, empiredidnothingwrong)."),
    dict(base, id="F-006", tier="fourth", warrant="read",
         statement="Decided order is rare: a decided element of order (a leader, a vote, an oath, a sanction, a division "
                   "of the work; Decided order) is placed in %d of 705 rooms, against %d for repair work and %d for the "
                   "completion ritual." % (n_dec, n_rep, n_cel),
         evidence=["out/assignments_final.jsonl", "out/fourth/fourth.jsonl", "out/form_pass-C1.md"],
         bound="Counts placed themes; votes and divisions of work also appear in rooms not placed on it (sweden, "
               "ripcity, edmontonoilers, empiredidnothingwrong in the pass 1 story rooms)."),
]
with open(os.path.join(OUT, "findings.jsonl"), "a", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
els = jl(os.path.join("model", "elements.jsonl"))
was = None
for e in els:
    if e["id"] == "C01":
        was = json.loads(json.dumps(e))
        e["evidence"]["findings"] = ["F-006"]
with open(os.path.join(OUT, "model", "elements.jsonl"), "w", encoding="utf-8") as f:
    for e in els:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
reads = jl("_mem_reads-C2.jsonl")
read_rooms = sorted(set(str(x) for r in reads if r.get("verb") in ("room", "forest") for x in (r.get("args") or [])[:1]))
hist = {"t": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "stage": "C2", "leg": "C2a-01",
        "id": "C01", "event": "evidence corrected", "move": "relating",
        "why": "C01 cited F-001, the stage B1 claim about the 197 kinds; it now cites F-006, decided order is rare, "
               "written at this leg with the count recomputed from the placements.",
        "was": was,
        "stamp": {"leg": "C2a-01", "rooms_read": read_rooms, "n_rooms_read": len(read_rooms), "reads_so_far": len(reads),
                  "tokens_read": "not recorded in the read log", "prompted_by": {"room": None, "theme": "C01"}}}
with open(os.path.join(OUT, "model", "history.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(hist, ensure_ascii=False) + "\n")
print("findings appended: %s" % ", ".join(r["id"] for r in new))
print("decided order %d, repair %d, completion ritual %d rooms" % (n_dec, n_rep, n_cel))
print("C01 evidence now F-006; history line appended; rooms read so far %d" % len(read_rooms))
