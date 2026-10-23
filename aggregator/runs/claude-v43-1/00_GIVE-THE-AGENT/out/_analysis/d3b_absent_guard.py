#!/usr/bin/env python3
"""D3b, G2 with G61 (3): the guard over the unruled re-check absent lines. A line is flagged for reading when
  F1  the room has an accepted or modified instantiate line on the same element, in the first return or the re-check;
  F2  the element is a candidate and the room's D3a-55 propose line in its group was accepted, or a D3a-56 verdict
      ruling's residue names it;
  F3  its observation claims an evidenced absence (observed-absent, not-needed), which G3 reads;
  F4  the room's placements carry the element: a second-order theme of the room is placed on a third-order theme
      of one of the element's fourth-order tiers (G2: where the placements carry the element, the concepts are
      read first).
An unflagged line (unobserved or not-testable) is an evidence limit under G2: accepted, kind none. With --write the
unflagged lines' rulings go to d3_rulings/recheck-absent-limits-NN.jsonl (at most 2,500 a file), and the flagged
lines' ids, with their flags, to d3_rulings/recheck-absent-flagged.jsonl for reading.

    python3 out/_analysis/d3b_absent_guard.py [--write]
"""
import argparse, collections, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
ap.add_argument("--lim-prefix", default="recheck-absent-lim2", help="limit files' prefix; a new batch takes a new one")
ap.add_argument("--flagged-name", default="recheck-absent-flagged2.jsonl", help="the flagged list's file name")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


old = jl(os.path.join(OUT, "adaptations.jsonl"))
new = jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
last = {}
for r in jl(os.path.join(OUT, "adjudications.jsonl")):
    last[r["adaptation"]] = r
shown = set()
for l in old + new:
    if l["op"] == "instantiate" and last.get(l["id"], {}).get("decision") in ("accept", "modify"):
        shown.add((l["sub"], l.get("element")))
cands = {c["class"]: c["id"] for c in json.load(open(os.path.join(RD, "propose-candidates.json")))}
led_old = {l["id"]: l for l in old}
for s in glob.glob(os.path.join(RD, "propose-spec-*.txt")):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            i, c = line.split("|")[:2]
            if c in cands and last.get(i, {}).get("decision") == "accept":
                shown.add((led_old[i]["sub"], cands[c]))
els = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
t4m = {r["id"]: set(r.get("members") or []) for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
el_t3 = {}
for i, e in els.items():
    tiers = e.get("tier") or []
    tiers = [tiers] if isinstance(tiers, str) else tiers
    el_t3[i] = set().union(*[t4m.get(t, set()) for t in tiers]) if tiers else set()
place = collections.defaultdict(set)
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    for t in r.get("third_order") or []:
        place[r["sub"]].add(t)
resid = set()
for r in jl(os.path.join(OUT, "verdicts-D.jsonl")):
    if r.get("ruled_by") == "analyst" and r.get("verdict") == "composes-with-residue":
        for c in set(re.findall(r"\b(P2[3-9]|P3[0-4]|K0[5-7])\b", r.get("reason", ""))):
            resid.add((r["sub"], c))
limits, flagged, why = [], [], collections.Counter()
for r in new:
    if r["op"] != "absent" or r["id"] in last:
        continue
    key = (r["sub"], r.get("element"))
    f = []
    if key in shown:
        f.append("F1" if not re.fullmatch(r"P2[3-9]|P3[0-4]|K0[5-7]", str(r.get("element"))) else "F1/F2")
    if key in resid:
        f.append("F2")
    if r.get("observation") in ("observed-absent", "not-needed"):
        f.append("F3")
    if el_t3.get(r.get("element")) and place.get(r["sub"], set()) & el_t3[r.get("element")]:
        f.append("F4")
    if f:
        flagged.append({"adaptation": r["id"], "sub": r["sub"], "element": r.get("element"),
                        "observation": r.get("observation"), "flags": f})
        why["flagged " + "+".join(sorted(set(f)))] += 1
        continue
    if r.get("portable") is False:
        limits.append({"adaptation": r["id"], "decision": "particular", "kind": "particular",
                       "reason": "G6 and G61 (3): absent, %s, on %s; the line is marked NONPORTABLE, so it is a "
                                 "particular by construction" % (r.get("observation"), r.get("element"))})
        why["NONPORTABLE (G6): particular"] += 1
        continue
    reason = ("G2 and G61 (3): absent, %s; no accepted line of the room, in the first return or the re-check, "
              "shows %s, and no D3a-55 proposal or D3a-56 residue of the room names it; the line marks a limit of "
              "the record, counted apart" % (r.get("observation"), r.get("element")))
    limits.append({"adaptation": r["id"], "decision": "accept", "kind": "none", "reason": reason})
    why["limit (G2): %s" % r.get("observation")] += 1
print("unruled re-check absent lines: %d" % (len(limits) + len(flagged)))
for k, n in sorted(why.items()):
    print("   %-36s %6d" % (k, n))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
for i in range(0, len(limits), 2500):
    p = os.path.join(RD, "%s-%02d.jsonl" % (a.lim_prefix, i // 2500 + 1))
    if os.path.exists(p):
        sys.exit("refused: %s exists" % p)
    with open(p, "w", encoding="utf-8") as fh:
        for x in limits[i:i + 2500]:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
p = os.path.join(RD, a.flagged_name)
if os.path.exists(p):
    sys.exit("refused: %s exists" % p)
with open(p, "w", encoding="utf-8") as fh:
    for x in flagged:
        fh.write(json.dumps(x, ensure_ascii=False) + "\n")
print("wrote %d limit files and the flagged list (%d lines)" % ((len(limits) + 2499) // 2500, len(flagged)))
