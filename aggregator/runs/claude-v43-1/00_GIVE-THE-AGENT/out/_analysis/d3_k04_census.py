#!/usr/bin/env python3
"""D3a-52: K04's census under its census rules (logged before this ran). Reads the six ruling files (instantiate v3,
absent v2), the spec files for each line's class and the six tag files; a line shows K04 when it has a tag row. Prints
lines by op and class, rooms showing K04 with their forms (NA, CU, QU, CO), the BE elaboration, the marks (OE, VE,
FT, AC, PO, BT, CX), how the colour faith sits beside the bodies from before, the overlap with K03's tag files and
with C02's accepted or rejected-absent lines, and the rooms not showing K04. Writes nothing.

  python3 out/_analysis/d3_k04_census.py
"""
import json
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = [("instantiate", "K04-inst-v3", "K04-inst-spec-v3.txt", "K04-tags-inst-v3.txt"),
       ("restrict", "K04-restrict", "K04-restrict-spec.txt", "K04-tags-restrict.txt"),
       ("add-condition", "K04-addcond", "K04-addcond-spec.txt", "K04-tags-addcond.txt"),
       ("add-step", "K04-addstep", "K04-addstep-spec.txt", "K04-tags-addstep.txt"),
       ("link", "K04-link", "K04-link-spec.txt", "K04-tags-link.txt"),
       ("absent", "K04-absent-v2", "K04-absent-spec-v2.txt", "K04-tags-absent-v2.txt")]
FORMS = ("NA", "CU", "QU", "CO")
BODY = {"NA", "CU", "QU"}
MUST = ("SHOW", "ELAB", "S-SHOW", "S-OTHER", "REJ", "PART")


def room(aid):
    return aid.rsplit("-", 1)[0]


def tagrooms(files):
    out = set()
    for f in files:
        for l in open(R + f, encoding="utf-8"):
            if l.strip():
                out.add(room(l.split("|")[0]))
    return out


lines = {}
for op, base, spec, tags in OPS:
    rul = [json.loads(l) for l in open(R + base + ".jsonl", encoding="utf-8") if l.strip()]
    cls = {}
    for l in open(R + spec, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|")
            cls[p[0]] = p[1]
    tg = {}
    for l in open(R + tags, encoding="utf-8"):
        if l.strip():
            i, t = l.strip().split("|")
            tg[i] = set(t.split(","))
    for r in rul:
        i = r["adaptation"]
        assert i not in lines, i
        c = cls.get(i)
        if c is None:
            assert op == "absent", i
            c = {"accept": "EL", "reject": "REJ", "particular": "P-G6"}[r["decision"]]
        if c in MUST:
            assert i in tg, i
        if i in tg:
            assert c in MUST or (c == "P-G6" and "PO" in tg[i]), (i, c)
        lines[i] = {"op": op, "class": c, "decision": r["decision"], "kind": r.get("kind"), "tags": tg.get(i)}

print("lines: %d; rooms: %d" % (len(lines), len({room(i) for i in lines})))
byop = defaultdict(Counter)
for i, x in lines.items():
    byop[x["op"]][x["class"]] += 1
for op, *_ in OPS:
    print("  %-13s %4d  %s" % (op, sum(byop[op].values()), dict(sorted(byop[op].items()))))
print("decisions:", dict(Counter(x["decision"] for x in lines.values())),
      "kinds:", dict(Counter(str(x["kind"]) for x in lines.values())))

shown = {i: x for i, x in lines.items() if x["tags"]}
rooms = defaultdict(list)
for i, x in lines.items():
    rooms[room(i)].append(x)
srooms = {r: [x for x in xs if x["tags"]] for r, xs in rooms.items()}
srooms = {r: xs for r, xs in srooms.items() if xs}
print("\nlines showing K04: %d of %d; rooms showing K04: %d of %d" % (len(shown), len(lines), len(srooms), len(rooms)))
print("  shown lines by tag:", dict(sorted(Counter(t for x in shown.values() for t in x["tags"]).items())))
marks = {r: set().union(*[x["tags"] for x in xs]) for r, xs in srooms.items()}
oe = {r for r, s in marks.items() if "OE" in s}
veonly = sorted(r for r, s in marks.items() if "VE" in s and "OE" not in s)
aconly = sorted(r for r, xs in srooms.items() if all("AC" in x["tags"] for x in xs))
poonly = sorted(r for r, xs in srooms.items() if all("PO" in x["tags"] for x in xs))
print("  rooms with OE: %d of %d (%.3f); VE only: %d %s" % (len(oe), len(srooms), len(oe) / len(srooms), len(veonly),
                                                          veonly))
print("  AC-only rooms: %d; PO-only rooms: %d" % (len(aconly), len(poonly)))
print("  rooms by form or mark:")
for f in FORMS + ("BE", "FT", "BT", "CX", "VE", "AC", "PO"):
    print("    %-3s %3d rooms" % (f, len({r for r, s in marks.items() if f in s})))
print("  rooms by number of forms (BE not counted):",
      dict(sorted(Counter(len(s & set(FORMS)) for s in marks.values()).items())))
beonly = sorted(r for r, s in marks.items() if not (s & set(FORMS)) and "BE" in s)
print("  rooms whose only form is BE: %d %s" % (len(beonly), beonly))

print("\nthe colour faith:")
co = {r for r, s in marks.items() if "CO" in s}
coalone = sorted(r for r in co if not (marks[r] & BODY))
cobody = sorted(r for r in co if marks[r] & BODY)
print("  rooms with CO: %d; CO with no body form (NA, CU, QU): %d %s" % (len(co), len(coalone), coalone))
print("  CO beside a body form: %d %s" % (len(cobody), cobody))
print("  rooms with CX (a member's outside colour allegiance) among rooms showing K04: %d %s"
      % (len({r for r, s in marks.items() if "CX" in s}), sorted(r for r, s in marks.items() if "CX" in s)))

k03 = tagrooms(["K03-tags-inst.txt", "K03-tags-restrict.txt", "K03-tags-addcond.txt", "K03-tags-absent-v2.txt"])
qu = {r for r, s in marks.items() if "QU" in s}
quonly = {r for r, s in marks.items() if (s & set(FORMS)) == {"QU"} and "BE" not in s}
print("\nthe overlap with K03 (rooms in K03's tag files: %d):" % len(k03))
print("  rooms showing K04: %d, of which K03 shows %d" % (len(srooms), len(set(srooms) & k03)))
print("  rooms with QU: %d, of which K03 shows %d; not shown by K03: %d" % (len(qu), len(qu & k03), len(qu - k03)))
print("  rooms whose only K04 form is QU: %d, of which K03 shows %d; not shown by K03: %s"
      % (len(quonly), len(quonly & k03), sorted(quonly - k03)))
print("  rooms showing K04 without QU: %d, of which K03 shows %d" % (len(set(srooms) - qu), len((set(srooms) - qu) & k03)))

c02 = set()
for f in ("C02-inst-000", "C02-inst-100", "C02-restrict", "C02-addcond", "C02-absent"):
    for l in open(R + f + ".jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if (f != "C02-absent" and r["decision"] == "accept" and r.get("kind") == "specification") or \
                    (f == "C02-absent" and r["decision"] == "reject"):
                c02.add(room(r["adaptation"]))
print("\nthe overlap with C02 (rooms with a C02 specification or a rejected absent line: %d):" % len(c02))
print("  rooms showing K04 that C02 shows: %d; with QU: %d; with NA: %d; with CO: %d"
      % (len(set(srooms) & c02), len(qu & c02), len({r for r in set(srooms) & c02 if "NA" in marks[r]}),
         len(co & c02)))
print("  C02 rooms not showing K04: %d" % len(c02 - set(srooms)))

print("\nlines not showing K04, by class:", dict(Counter(x["class"] for x in lines.values() if not x["tags"])))
part = [i for i, x in lines.items() if x["decision"] == "particular"]
print("particulars: %d, of which K04 shown (PO or PART): %d" % (len(part), sum(1 for i in part if lines[i]["tags"])))
nos = sorted(r for r in rooms if r not in srooms)
lim = [r for r in nos if all(x["decision"] == "accept" and x["kind"] == "none" for x in rooms[r])]
print("rooms not showing K04: %d; of them, rooms whose lines are all evidence limits: %d" % (len(nos), len(lim)))
print("rooms not showing K04 with a NOT or EL-NOT line: %d" % len([r for r in nos if any(
    x["class"] in ("NOT", "EL-NOT") for x in rooms[r])]))
