#!/usr/bin/env python3
"""D3b, G61 (3) and its reading 5: the rulings for one packet of unruled re-check lines of one element and op, read in
the packet d3b_packet.py printed (rebuilt here: unruled lines of the element and op, room order, offset 0, limit 100).
A rows file gives the lines whose reading sets the ruling, one a line, 'id|CLASS|evidence', CLASS one of:
  SPEC          accept, specification (the concepts show the element as stated, or a statement G4a names holds it)
  ELAB:<pair>   accept, elaboration, paired with another room's accepted line meeting the same addition (G4, G5)
  CORR:<pair>   accept, correction, paired (G9; a correction met twice goes to section 2 as a held proposal)
  LIM           accept, kind none: an evidence limit (a restriction or addition whose concepts show nothing to rule)
  REJ           reject: the concepts do not show what the line claims
  PART          particular: shown in this room only (G4, G5) or naming the room itself
  PEND          pending: unresolved
For instantiate lines every line not named takes the default of G1b as read: accept, specification, the reason
naming the cited concepts by label. For every other op each portable line must be named. NONPORTABLE lines are
particulars by G6 and take no rows line. Writes d3_rulings/<name>.jsonl; never overwrites.

    python3 out/_analysis/d3b_op_rows.py --element R01 --op instantiate --packet d3b_pk_R01_inst_000.txt \
        --rows out/_analysis/d3_rulings/R01-inst-000-rows.txt --name recheck-R01-inst-000 [--write]
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
RD = os.path.join(OUT, "_analysis", "d3_rulings")
ST = os.path.join(ROOT, "package", "store")
ap = argparse.ArgumentParser()
ap.add_argument("--element", required=True)
ap.add_argument("--op", required=True)
ap.add_argument("--packet", required=True)
ap.add_argument("--rows")
ap.add_argument("--name", required=True)
ap.add_argument("--write", action="store_true")
ap.add_argument("--rows-any-op", action="store_true",
                help="skip rows of the same element on another op, so one rows file can serve several ops")
a = ap.parse_args()


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def codes(r):
    ev = r.get("evidence") or []
    if isinstance(ev, dict):
        ev = ev.get("codes") or []
    return [str(c).split(":")[-1] for c in ev]


ruled = {r["adaptation"] for r in jl(os.path.join(OUT, "adjudications.jsonl"))}
led = {l["id"]: l for l in jl(os.path.join(OUT, "adaptations.jsonl")) + jl(os.path.join(OUT, "adaptations-recheck.jsonl"))}
new = [r for r in jl(os.path.join(OUT, "adaptations-recheck.jsonl"))
       if r.get("element") == a.element and r["op"] == a.op and r["id"] not in ruled]
new.sort(key=lambda r: (r["sub"].lower(), r["op"], r["id"]))
page = new[:100]
ids = {r["id"] for r in page}
subs = {r["sub"] for r in page}
lab = {}
for l in open(os.path.join(ST, "codes.jsonl"), encoding="utf-8"):
    c = json.loads(l)
    if c["sub"] in subs:
        lab[(c["sub"], c["code_id"])] = c.get("first_order")
ov = {}
if a.rows:
    for n, l in enumerate(open(a.rows, encoding="utf-8"), 1):
        l = l.rstrip("\n")
        if not l.strip():
            continue
        i, cls, ev = l.split("|", 2)
        if i not in ids:
            if a.rows_any_op and i in led and led[i].get("element") == a.element and led[i]["op"] != a.op:
                continue
            sys.exit("rows line %d: %s is not in this packet" % (n, i))
        base, _, pair = cls.partition(":")
        if base not in ("SPEC", "ELAB", "CORR", "LIM", "REJ", "PART", "PEND") or not ev.strip() or i in ov:
            sys.exit("rows line %d: bad class, no evidence, or the id twice" % n)
        if base in ("ELAB", "CORR"):
            if pair not in led or led[pair]["sub"] == led[i]["sub"]:
                sys.exit("rows line %d: %s needs a pair, a ledger line of another room" % (n, base))
        ov[i] = (base, pair, ev.strip())
KIND = {"SPEC": ("accept", "specification"), "ELAB": ("accept", "elaboration"), "CORR": ("accept", "correction"),
        "LIM": ("accept", "none"), "REJ": ("reject", None), "PART": ("particular", "particular"),
        "PEND": ("pending", None)}
out, tally = [], {}
for r in page:
    i, s, e = r["id"], r["sub"], a.element
    seen = "; ".join("%s %s" % (c, lab.get((s, c), "?")) for c in codes(r)) or "no concept cited"
    if r.get("portable") is False:
        if i in ov:
            sys.exit("%s is NONPORTABLE; G6 rules it first" % i)
        row = {"adaptation": i, "decision": "particular", "kind": "particular",
               "reason": "G6 and G61 (3), read in %s: %s on %s; the line is marked NONPORTABLE (%s), so it is a "
                         "particular by construction" % (a.packet, a.op, e, ", ".join(r.get("nonportable_hits") or []))}
    elif i in ov:
        base, pair, ev = ov[i]
        d, k = KIND[base]
        row = {"adaptation": i, "decision": d, "kind": k,
               "reason": "G61 (3) and its reading 5, read in %s: %s on %s; %s" % (a.packet, a.op, e, ev)}
        if pair:
            row["pair"] = pair
    elif a.op == "instantiate":
        row = {"adaptation": i, "decision": "accept", "kind": "specification",
               "reason": "G1b and G61's reading 5, read in %s: instantiate; the cited concepts (%s) show %s as stated, "
                         "a specification" % (a.packet, seen, e)}
    else:
        sys.exit("%s (%s) must be named in the rows file" % (i, a.op))
    out.append({k: v for k, v in row.items() if v is not None})
    t = "%s/%s" % (row["decision"], row.get("kind"))
    tally[t] = tally.get(t, 0) + 1
print("%s %s %s packet: %d rulings; %s" % (a.name, a.element, a.op, len(out), tally))
if not a.write:
    print("dry run: nothing written")
    sys.exit(0)
p = os.path.join(RD, a.name + ".jsonl")
if os.path.exists(p):
    sys.exit("refused: %s exists" % p)
with open(p, "w", encoding="utf-8") as f:
    for x in out:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")
print("wrote %s" % p)
