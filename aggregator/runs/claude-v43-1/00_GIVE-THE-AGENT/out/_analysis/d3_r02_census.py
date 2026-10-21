#!/usr/bin/env python3
"""D3a-49: R02's census under G54's census rules (logged before this ran). Reads the four ruling files, the spec files
for each line's class and the four tag files; a line shows R02 when it has a tag row. Prints lines by op and class,
rooms showing R02 with their forms (CA, NA, CO), sides (OE, VE) and AC and PO marks, rooms by number of forms, the
lines not shown by class, the particulars, and the rooms not showing R02. Writes nothing.

  python3 out/_analysis/d3_r02_census.py
"""
import json
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = [("instantiate", "R02-inst", "R02-inst-spec.txt", "R02-tags-inst.txt"),
       ("restrict", "R02-restrict", "R02-restrict-spec.txt", "R02-tags-restrict.txt"),
       ("add-condition", "R02-addcond", "R02-addcond-spec.txt", "R02-tags-addcond.txt"),
       ("absent", "R02-absent", "R02-absent-spec.txt", "R02-tags-absent.txt")]
FORMS = ("CA", "NA", "CO")


def room(aid):
    return aid.rsplit("-", 1)[0]


lines = {}
for op, base, spec, tags in OPS:
    rul = [json.loads(l) for l in open(R + base + ".jsonl", encoding="utf-8") if l.strip()]
    cls = {}
    for l in open(R + spec, encoding="utf-8"):
        if l.strip():
            p = [x.strip() for x in l.rstrip("\n").split("|")]
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
        assert (i in tg) == (c in ("SHOW", "P-G6", "S-SHOW", "REJ")), i
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
print("\nlines showing R02: %d of %d; rooms showing R02: %d of %d" % (len(shown), len(lines), len(srooms), len(rooms)))
print("  shown lines by tag:", dict(sorted(Counter(t for x in shown.values() for t in x["tags"]).items())))
marks = {r: set().union(*[x["tags"] for x in xs]) for r, xs in srooms.items()}
oe = {r for r, s in marks.items() if "OE" in s}
veonly = {r for r, s in marks.items() if "VE" in s and "OE" not in s}
neither = {r for r, s in marks.items() if not s & {"OE", "VE"}}
aconly = {r for r, xs in srooms.items() if all("AC" in x["tags"] for x in xs)}
poonly = {r for r, xs in srooms.items() if all("PO" in x["tags"] for x in xs)}
print("  rooms with OE: %d of %d (%.3f); VE only: %d; neither side marked: %d"
      % (len(oe), len(srooms), len(oe) / len(srooms), len(veonly), len(neither)))
print("  AC-only rooms: %d; PO-only rooms: %d" % (len(aconly), len(poonly)))
print("  rooms by form, and the share of them with OE:")
for f in FORMS:
    rs = {r for r, s in marks.items() if f in s}
    if rs:
        print("    %-3s %3d rooms; OE in %3d (%.3f)" % (f, len(rs), len(rs & oe), len(rs & oe) / len(rs)))
print("  rooms by number of forms:", dict(sorted(Counter(len(s & set(FORMS)) for s in marks.values()).items())))
naonly = {r for r, s in marks.items() if (s & set(FORMS)) == {"NA"}}
print("  rooms whose only form is NA: %d; with OE: %d" % (len(naonly), len(naonly & oe)))

print("\nlines not showing R02, by class:", dict(Counter(x["class"] for x in lines.values() if not x["tags"])))
part = [i for i, x in lines.items() if x["decision"] == "particular"]
print("particulars: %d, of which PO (R02 shown): %d" % (len(part), sum(1 for i in part if lines[i]["tags"])))
nos = sorted(r for r in rooms if r not in srooms)
lim = [r for r in nos if all(x["decision"] == "accept" and x["kind"] == "none" for x in rooms[r])]
print("rooms not showing R02: %d; of them, rooms whose lines are all evidence limits: %d" % (len(nos), len(lim)))
print("rooms not showing R02 with a NOT line: %s" % [r for r in nos if any(x["class"] == "NOT" for x in rooms[r])])
