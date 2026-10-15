#!/usr/bin/env python3
"""D1a: write out/EXPECTATIONS-D1.jsonl, one line per room of the analysed set, by the rules R1 to R6 written in
notes-D1.md before this script ran. Sources: the frozen model (model/elements.jsonl, model/arrows.jsonl), the order
tests' element themes (_analysis/c2_elements_c5c2.json), the placements (assignments_final.jsonl, third_order), the
store's concept counts (rooms.jsonl, codes), the empty pre-event weeks (_analysis/c2_empty_brief-p3.json), and
fourth/fourth.jsonl for the colour factions (T4-023's members). Prints the counts by element.

    python3 out/_analysis/d1_expectations.py            counts only
    python3 out/_analysis/d1_expectations.py --write    write out/EXPECTATIONS-D1.jsonl (refuses if it exists)
"""
import ast, collections, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out")
A_ = os.path.join(OUT, "_analysis")
DEST = os.path.join(OUT, "EXPECTATIONS-D1.jsonl")
FLOOR = 10


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def lst(v):
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.strip():
        return ast.literal_eval(v)
    return []


E = {e["id"]: e for e in jl(os.path.join(OUT, "model", "elements.jsonl"))}
AR = {a["id"]: a for a in jl(os.path.join(OUT, "model", "arrows.jsonl")) if a.get("status") == "standing"}
standing = {i for i, e in E.items() if e["status"] == "standing"}
els = {e["id"]: set(e.get("themes") or []) for e in json.load(open(os.path.join(A_, "c2_elements_c5c2.json")))["elements"]
       if e["id"] in standing}
rooms = {r["sub"]: r for r in jl(os.path.join(ROOT, "package", "store", "rooms.jsonl"))}
empty = set(json.load(open(os.path.join(A_, "c2_empty_brief-p3.json")))["empty"])
fourth = {r["id"]: r for r in jl(os.path.join(OUT, "fourth", "fourth.jsonl"))}
colour = set(fourth["T4-023"]["members"])
host = {"T3-035", "T3-094", "T3-099", "T3-162"}           # P19's themes, a candidate: hosts ruling on guests
place = collections.defaultdict(lambda: collections.defaultdict(list))   # sub -> T3 -> [theme ids]
for r in jl(os.path.join(OUT, "assignments_final.jsonl")):
    for t3 in lst(r.get("third_order")):
        place[r["sub"]][t3].append(r["theme_id"])
MARK = {"R01", "P02", "P03", "P05"}
NO_MARK = ["P05", "P14", "A03", "A04", "A06", "A13", "A19"]
NO_CALL = ["P15", "A01", "A12", "A15", "A20"]
ARROW_WHY = {"A11": "theorised", "A05": "thin; its mechanism theorised", "A10": "thin", "A14": "thin", "A19": "thin"}

lines, inst_n, abs_n, nt_rooms, nt_n = [], collections.Counter(), collections.Counter(), 0, collections.Counter()
for sub in sorted(rooms):
    n_codes = rooms[sub].get("codes") or 0
    p = place.get(sub, {})
    carried = {}
    for eid, ths in els.items():
        hit = sorted({t for t3 in ths & set(p) for t in p[t3]})
        if hit:
            carried[eid] = hit
    inst, absent, nt, why, frm = [], [], [], [], ["placements"]
    for eid in sorted(carried):
        inst.append(eid)
        why.append("%s: the room's themes %s are placed on it" % (eid, ", ".join(carried[eid][:4]) +
                                                                  (" and more" if len(carried[eid]) > 4 else "")))
    arrows_in = [a for a in sorted(AR) if AR[a]["from"] in carried and AR[a]["to"] in carried]
    for a in arrows_in:
        inst.append(a)
        why.append("%s: both ends are carried, so the order it states is expected%s" % (
            a, " (%s)" % ARROW_WHY[a] if a in ARROW_WHY else ""))
    if arrows_in:
        frm.append("implications-C5 expectations 1-4 and 6-8; propositions")
    above = n_codes >= FLOOR
    if above and "P01" in carried:
        inst.append("P15")
        why.append("P15: the room calls for hands, so written acceptances are expected to come bare (expectation 12)")
        frm.append("implications-C5 expectation 12")
        t3s = set(p)
        if "C01" not in carried:
            if t3s & (colour | host):
                why.append("C01: not expected absent, since the room carries a colour faction's or a host's theme, "
                           "where decided order is coded more often (expectation 5)")
            else:
                absent.append("C01")
                why.append("C01: the room calls for hands and is neither a colour faction nor a host ruling on "
                           "guests, so decided order is expected absent (expectation 5; F-006)")
                frm.append("implications-C5 expectation 5")
        if "P20" not in carried and sub in empty:
            absent.append("P20")
            why.append("P20: the room had no posts in the week before the canvas, so the host's line is expected weak "
                       "or absent (expectation 6; the empty week stands in for a sub opened for the canvas)")
            frm.append("implications-C5 expectation 6")
    if not above:
        nt = sorted(x for x in list(standing) + list(AR) if x not in carried and x not in inst)
        why.append("the room holds %d concepts, below the floor of %d, so what it does not carry is not testable "
                   "here (rule 6)" % (n_codes, FLOOR))
    else:
        if not (MARK & set(carried)):
            nt += [x for x in NO_MARK if x not in inst]
            why.append("%s: the room carries no mark of its own, so upkeep and what follows it are not testable "
                       "here (rule 6)" % ", ".join(x for x in NO_MARK if x not in inst))
        if "P01" not in carried:
            nt += [x for x in NO_CALL if x not in inst and x not in nt]
            why.append("%s: the room carries no call, so the answer to a call is not testable here (rule 6)" %
                       ", ".join(x for x in NO_CALL if x not in inst))
    if set(p) & (colour | host):
        why.append("the model expects this room to compose with a residue: a faith in a colour or a host's rule picks "
                   "rivals and guests, and no element does (expectation 13)")
        frm.append("implications-C5 expectation 13")
    line = {"sub": sub, "expect_instantiate": inst, "expect_absent": absent, "from": sorted(set(frm)),
            "why": "; ".join(why) if why else "the room's themes are placed on no element of the model"}
    if nt:
        line["not_testable_here"] = sorted(set(nt))
        nt_rooms += 1
        nt_n.update(set(nt))
    inst_n.update(inst)
    abs_n.update(absent)
    lines.append(line)

print("lines %d; rooms with not_testable_here %d; rooms below the floor %d" % (
    len(lines), nt_rooms, sum(1 for s in rooms if (rooms[s].get("codes") or 0) < FLOOR)))
print("instantiate by id: %s" % dict(sorted(inst_n.items())))
print("absent by id: %s" % dict(sorted(abs_n.items())))
print("not testable by id: %s" % dict(sorted(nt_n.items())))
print("rooms with an empty instantiate list: %d" % sum(1 for l in lines if not l["expect_instantiate"]))
if "--write" in sys.argv:
    if os.path.exists(DEST):
        sys.exit("EXPECTATIONS-D1.jsonl exists; not overwritten")
    with open(DEST, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    print("wrote %s" % DEST)
