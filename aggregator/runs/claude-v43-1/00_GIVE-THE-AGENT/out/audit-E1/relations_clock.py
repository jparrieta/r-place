#!/usr/bin/env python3
"""E1 section 1, the clocks, the second check (E1b-01): two rooms' records of one encounter, against each other.
tools/relations.py builds the mention graph and checks no clock, so the check is a script that sets out the pairs
and a reading by hand of a seeded draw. Prints JSON.

    python3 out/audit-E1/relations_clock.py > out/audit-E1/relations_clock.json

The rule, declared before the run (E1b-01):
- Pairs: reciprocated pairs of relations.jsonl between two rooms of the study (each room's coder recorded the other),
  taken once, where the two sides carry one act from both ends: attacked and attacked-by, gave-help-to and
  asked-help-from, negotiated on both sides, or allied on both sides (a side's `labels`, any count).
- For each pair, the hours of the concepts each side's coder tied to the other room (`code_ids`, hours from
  codes.jsonl), and the smallest gap in hours between a concept of one side and a concept of the other. Two records
  of one encounter should date it close together; the gap is reported within 1, 6 and 24 hours, and beyond.
- Ten pairs drawn with random.Random(int(out/seed.txt, 16)) from the pairs, each with the two concepts that give the
  smallest gap, to be read by hand with cite.py: do the two concepts speak of the same encounter, and do their hours
  agree with what each says.
"""
import collections, json, os, random, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "out")
ST = os.path.join(ROOT, "package", "store")
ACTS = [("attacked", "attacked-by"), ("attacked-by", "attacked"), ("gave-help-to", "asked-help-from"),
        ("asked-help-from", "gave-help-to"), ("negotiated", "negotiated"), ("allied", "allied")]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    hour = {(c["sub"], c["code_id"]): c.get("hour") for c in jl(os.path.join(ST, "codes.jsonl"))}
    rel = {(r["sub"], r["other"]): r for r in jl(os.path.join(ST, "relations.jsonl"))
           if r.get("other") and r.get("other_in_frame")}
    pairs = []
    for (a, b), ra in sorted(rel.items()):
        if a >= b or (b, a) not in rel:
            continue
        rb = rel[(b, a)]
        la, lb = set(ra.get("labels") or {}), set(rb.get("labels") or {})
        acts = sorted({"%s / %s" % (x, y) for x, y in ACTS if x in la and y in lb})
        if not acts:
            continue
        ha = [(c, hour.get((a, c))) for c in ra.get("code_ids") or [] if hour.get((a, c)) is not None]
        hb = [(c, hour.get((b, c))) for c in rb.get("code_ids") or [] if hour.get((b, c)) is not None]
        if not ha or not hb:
            continue
        gap, ca, cb = min((abs(x[1] - y[1]), x, y) for x in ha for y in hb)
        pairs.append({"a": a, "b": b, "acts": acts, "gap_hours": round(gap, 2),
                      "a_code": "%s/%s" % (a, ca[0]), "a_hour": ca[1], "b_code": "%s/%s" % (b, cb[0]), "b_hour": cb[1],
                      "a_codes": len(ha), "b_codes": len(hb)})
    def band(g):
        return "within 1 h" if g <= 1 else "within 6 h" if g <= 6 else "within 24 h" if g <= 24 else "beyond 24 h"
    bands = collections.Counter(band(p["gap_hours"]) for p in pairs)
    by_act = collections.defaultdict(collections.Counter)
    for p in pairs:
        for act in p["acts"]:
            by_act[act][band(p["gap_hours"])] += 1
    seed = open(os.path.join(OUT, "seed.txt")).read().split()[0]
    draw = random.Random(int(seed, 16)).sample(pairs, min(10, len(pairs)))
    print(json.dumps({"rule": __doc__.split("The rule, declared before the run (E1b-01):")[1].strip(),
                      "reciprocal_in_frame_pairs_with_one_act": len(pairs), "gap_bands": dict(bands),
                      "gap_bands_by_act": {k: dict(v) for k, v in sorted(by_act.items())},
                      "seed": seed, "draw": draw, "pairs": pairs}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
