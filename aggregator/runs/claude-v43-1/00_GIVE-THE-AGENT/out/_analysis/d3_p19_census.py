#!/usr/bin/env python3
"""D3a-53: P19's census under its census rules (logged before this ran). Reads P19's six ruling files (absent v2), the
spec files for each line's class and the six tag files; a line shows P19 when its tag row holds a form (AS, PR, RU,
DI). Prints lines by op and class; rooms showing P19 with their forms and marks (HO, GU, OE, VE, CO, AC, PO); rooms
whose only form is AS beside rooms with RU; the share of RU rooms that are CO; the overlap with K04's CO rooms; and
the overlap with P08, P16, P17 and P21, each read from the element's ruling files for its ids and from
adjudications.jsonl for each id's latest line. Writes nothing.

  python3 out/_analysis/d3_p19_census.py
"""
import glob
import json
import os
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = [("instantiate", "P19-inst", "P19-inst-spec.txt", "P19-tags-inst.txt"),
       ("restrict", "P19-restrict", "P19-restrict-spec-all.txt", "P19-tags-restrict.txt"),
       ("add-condition", "P19-addcond", "P19-addcond-spec.txt", "P19-tags-addcond.txt"),
       ("add-step", "P19-addstep", "P19-addstep-spec.txt", "P19-tags-addstep.txt"),
       ("link", "P19-link", "P19-link-spec.txt", "P19-tags-link.txt"),
       ("absent", "P19-absent-v2", "P19-absent-spec-v2.txt", "P19-tags-absent-v2.txt")]
FORMS = ("AS", "PR", "RU", "DI")
MUST = ("SHOW", "S-SHOW", "S-OTHER", "E-PAIR", "PART", "REJ")


def room(aid):
    return aid.rsplit("-", 1)[0]


def tags_of(files):
    out = {}
    for f in files:
        for l in open(R + f, encoding="utf-8"):
            if l.strip():
                i, t = l.strip().split("|")
                out[i] = set(t.split(","))
    return out


lines = {}
for op, base, spec, tagf in OPS:
    rul = [json.loads(l) for l in open(R + base + ".jsonl", encoding="utf-8") if l.strip()]
    cls = {}
    for l in open(R + spec, encoding="utf-8"):
        if l.strip():
            p = l.rstrip("\n").split("|")
            cls[p[0]] = p[1]
    tg = tags_of([tagf])
    for r in rul:
        i = r["adaptation"]
        assert i not in lines, i
        c = cls.get(i)
        if c is None:
            assert op == "absent", i
            c = {"accept": "EL", "reject": "REJ", "particular": "P-G6"}[r["decision"]]
        t = tg.get(i, set())
        if c in MUST:
            assert t & set(FORMS), (i, c)
        if t & set(FORMS):
            assert c in MUST or (c == "P-G6" and "PO" in t), (i, c)
        lines[i] = {"op": op, "class": c, "decision": r["decision"], "kind": r.get("kind"), "tags": t,
                    "shown": bool(t & set(FORMS))}

print("lines: %d; rooms: %d" % (len(lines), len({room(i) for i in lines})))
byop = defaultdict(Counter)
for x in lines.values():
    byop[x["op"]][x["class"]] += 1
for op, *_ in OPS:
    print("  %-13s %4d  %s" % (op, sum(byop[op].values()), dict(sorted(byop[op].items()))))
print("decisions:", dict(Counter(x["decision"] for x in lines.values())),
      "kinds:", dict(Counter(str(x["kind"]) for x in lines.values())))

shown = {i: x for i, x in lines.items() if x["shown"]}
rooms = defaultdict(list)
for i, x in lines.items():
    rooms[room(i)].append(x)
srooms = {r: [x for x in xs if x["shown"]] for r, xs in rooms.items()}
srooms = {r: xs for r, xs in srooms.items() if xs}
print("\nlines showing P19: %d of %d; rooms showing P19: %d of %d" % (len(shown), len(lines), len(srooms), len(rooms)))
print("  shown lines by op:", dict(Counter(x["op"] for x in shown.values())))
print("  shown lines by tag:", dict(sorted(Counter(t for x in shown.values() for t in x["tags"]).items())))
marks = {r: set().union(*[x["tags"] for x in xs]) for r, xs in srooms.items()}
print("  rooms by form or mark:")
for f in FORMS + ("HO", "GU", "OE", "VE", "CO", "AC", "PO"):
    print("    %-3s %3d rooms" % (f, len({r for r, s in marks.items() if f in s})))
print("  rooms by number of forms:", dict(sorted(Counter(len(s & set(FORMS)) for s in marks.values()).items())))
asonly = sorted(r for r, s in marks.items() if (s & set(FORMS)) == {"AS"})
ru = {r for r, s in marks.items() if "RU" in s}
print("  rooms whose only form is AS: %d; rooms with RU: %d; rooms with PR and no RU: %d; with DI: %d"
      % (len(asonly), len(ru), len({r for r, s in marks.items() if "PR" in s and "RU" not in s}),
         len({r for r, s in marks.items() if "DI" in s})))
ho = {r for r, s in marks.items() if "HO" in s}
gu = {r for r, s in marks.items() if "GU" in s}
print("  HO rooms: %d; GU rooms: %d; both: %d; neither: %d" % (len(ho), len(gu), len(ho & gu),
                                                             len(set(marks) - ho - gu)))
print("  rooms with RU among HO rooms: %d; among GU rooms: %d" % (len(ru & ho), len(ru & gu)))
oe = {r for r, s in marks.items() if "OE" in s}
veonly = sorted(r for r, s in marks.items() if "VE" in s and "OE" not in s)
print("  rooms with OE: %d of %d (%.3f); VE only: %d" % (len(oe), len(marks), len(oe) / len(marks), len(veonly)))
aconly = sorted(r for r, xs in srooms.items() if all("AC" in x["tags"] for x in xs))
poonly = sorted(r for r, xs in srooms.items() if all("PO" in x["tags"] for x in xs))
print("  AC-only rooms: %d %s; PO-only rooms: %d %s" % (len(aconly), aconly, len(poonly), poonly))
print("  shown rooms whose shown lines are all absent rejections: %d"
      % len([r for r, xs in srooms.items() if all(x["op"] == "absent" for x in xs)]))

co = {r for r, s in marks.items() if "CO" in s}
print("\nthe colour faith: rooms with CO: %d of %d; RU rooms with CO: %d of %d (%.3f); HO rooms with CO: %d"
      % (len(co), len(marks), len(ru & co), len(ru), len(ru & co) / len(ru), len(co & ho)))
k04 = tags_of(["K04-tags-inst-v3.txt", "K04-tags-restrict.txt", "K04-tags-addcond.txt", "K04-tags-addstep.txt",
               "K04-tags-link.txt", "K04-tags-absent-v2.txt"])
k04co = {room(i) for i, t in k04.items() if "CO" in t}
print("  K04's CO rooms: %d; of them showing P19: %d; with P19's CO: %d; P19 HO rooms among them: %s"
      % (len(k04co), len(k04co & set(marks)), len(k04co & co), sorted(k04co & ho)))
print("  P19 CO rooms that K04 marks CO: %d of %d" % (len(co & k04co), len(co)))

latest = {}
for l in open("out/adjudications.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        latest[r["adaptation"]] = r
print("\noverlap with neighbouring elements (rooms shown by the element; of them showing P19):")
for el in ("P08", "P16", "P17", "P21"):
    ids, absent_ids = set(), set()
    for f in sorted(glob.glob(R + el + "-*.jsonl")):
        for l in open(f, encoding="utf-8"):
            if l.strip():
                i = json.loads(l)["adaptation"]
                ids.add(i)
                if "absent" in os.path.basename(f):
                    absent_ids.add(i)
    er = set()
    nullacc = 0
    for i in ids:
        x = latest.get(i)
        if x is None:
            continue
        if x["decision"] == "accept" and x.get("kind") not in (None, "none"):
            er.add(room(i))
        elif x["decision"] == "accept" and x.get("kind") is None:
            nullacc += 1
        elif x["decision"] == "reject" and i in absent_ids:
            er.add(room(i))
    print("  %s: ids %d; rooms shown %d; showing P19 %d (%.3f of P19's %d); accepts with no kind %d"
          % (el, len(ids), len(er), len(er & set(marks)), len(er & set(marks)) / len(marks), len(marks), nullacc))
    print("      P19 AS-only rooms it shows: %d of %d; P19 RU rooms it shows: %d of %d"
          % (len(er & set(asonly)), len(asonly), len(er & ru), len(ru)))

print("\nlines not showing P19, by class:", dict(Counter(x["class"] for x in lines.values() if not x["shown"])))
part = [i for i, x in lines.items() if x["decision"] == "particular"]
print("particulars: %d, of which P19 shown (PO or PART): %d" % (len(part), sum(1 for i in part if lines[i]["shown"])))
nos = sorted(r for r in rooms if r not in srooms)
lim = [r for r in nos if all(x["decision"] == "accept" and x["kind"] == "none" for x in rooms[r])]
print("rooms not showing P19: %d; of them, rooms whose lines are all evidence limits: %d" % (len(nos), len(lim)))
print("rooms with an EL-NOT or NOT line: %d, of them showing P19 elsewhere: %d"
      % (len({r for r, xs in rooms.items() if any(x["class"] in ("NOT", "EL-NOT") for x in xs)}),
         len({r for r, xs in rooms.items() if any(x["class"] in ("NOT", "EL-NOT") for x in xs)} & set(srooms))))
for name in ("thebluecorner", "orderofthebluecorner", "greenlattice", "ainbowroad", "placestart", "day9"):
    print("  %-22s lines %d; shown %d; marks %s" % (name, len(rooms.get(name, [])), len(srooms.get(name, [])),
                                                 sorted(marks.get(name, set()))))
