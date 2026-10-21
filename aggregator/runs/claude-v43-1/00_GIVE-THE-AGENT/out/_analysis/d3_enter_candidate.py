#!/usr/bin/env python3
"""D3a-55: enter one candidate element from the propose lines (stage section 3; SCHEMA section 1).

Reads the candidate's definition from d3_rulings/propose-candidates.json and its lines from the propose
spec files (rows whose class is the candidate's class). Refuses on any failure: the id already in
elements.jsonl; a tier or dimension id unknown; an evidence code not in the store; a line not a propose
line of the ledger; fewer than two rooms. With --write, appends one elements.jsonl line (status candidate,
since D3) and one history.jsonl line (event entered, move developing working hypotheses), then prints the
two ledgers' line counts. Without --write it prints what it would append.

    python3 out/_analysis/d3_enter_candidate.py --id P23 [--write]
"""
import argparse, datetime, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
ap.add_argument("--write", action="store_true")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


cands = json.load(open(os.path.join(OUT, "_analysis", "d3_rulings", "propose-candidates.json"), encoding="utf-8"))
c = [x for x in cands if x["id"] == a.id]
if len(c) != 1:
    sys.exit("refused: %s is not defined once in propose-candidates.json" % a.id)
c = c[0]
errs = []
els = jl(os.path.join(OUT, "model", "elements.jsonl"))
if any(e["id"] == a.id for e in els):
    errs.append("%s is already in elements.jsonl" % a.id)
t4 = {r["id"] for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
dims = {r["id"] for r in jl(os.path.join(OUT, "dimensions.jsonl"))}
errs += ["tier %s unknown" % t for t in c["tier"] if t not in t4]
errs += ["dimension %s unknown" % d for d in c["dimension"] if d not in dims]
codes = set()
for l in open(os.path.join(ROOT, "package", "store", "codes.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    codes.add("%s:%s" % (r["sub"], r["code_id"]))
errs += ["evidence code %s not in the store" % k for k in c["codes"] if k not in codes]
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl"))}
ids = []
for s in sorted(glob.glob(os.path.join(OUT, "_analysis", "d3_rulings", "propose-spec-*.txt"))):
    for line in open(s, encoding="utf-8"):
        line = line.rstrip("\n")
        if line and line.split("|")[1] == c["class"]:
            ids.append(line.split("|")[0])
for i in ids:
    if i not in led or led[i].get("op") != "propose":
        errs.append("%s is not a propose line of the ledger" % i)
rooms = sorted({led[i]["sub"] for i in ids if i in led})
if len(rooms) < 2:
    errs.append("%s rests on %d room(s); a candidate needs a second room" % (a.id, len(rooms)))
if errs:
    print("\n".join(errs))
    sys.exit("refused: nothing written")
leg = open(os.path.join(ROOT, ".leg")).read().strip()
t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
el = {"id": a.id, "kind": c["kind"], "origin": "propose", "status": "candidate", "statement": c["statement"],
      "tier": c["tier"], "dimension": c["dimension"], "range": c["range"],
      "evidence": {"findings": [], "codes": c["codes"], "propose_lines": len(ids), "rooms": len(rooms)},
      "since": "D3", "leg": leg}
hi = {"t": t, "stage": "D3", "leg": leg, "id": a.id,
      "event": "entered as a candidate (since D3) from the propose lines: %s" % c["name"],
      "move": "developing working hypotheses",
      "why": "%s %d propose lines in %d rooms show it; each is accepted as a proposal for %s, its pair a line of another room."
             % (c["why"], len(ids), len(rooms), a.id),
      "adaptations": ids, "rooms": rooms}
print("%s (%s): %d lines in %d rooms; tier %s; dimension %s" % (a.id, c["class"], len(ids), len(rooms), c["tier"], c["dimension"]))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
with open(os.path.join(OUT, "model", "elements.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(el, ensure_ascii=False) + "\n")
with open(os.path.join(OUT, "model", "history.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(hi, ensure_ascii=False) + "\n")
n_el = sum(1 for _ in open(os.path.join(OUT, "model", "elements.jsonl"), encoding="utf-8"))
n_hi = sum(1 for _ in open(os.path.join(OUT, "model", "history.jsonl"), encoding="utf-8"))
print("appended: elements.jsonl now %d lines, history.jsonl now %d lines" % (n_el, n_hi))
