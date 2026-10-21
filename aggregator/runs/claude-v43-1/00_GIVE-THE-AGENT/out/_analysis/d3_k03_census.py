#!/usr/bin/env python3
"""D3a-51: K03's census under G55's census rules (logged before this ran). Reads the four ruling files (the absent
file is version 2), the spec files for each line's class and the four tag files; a line shows K03 when it has a tag
row. Prints lines by op and class, rooms showing K03 with their forms (NR, AT, TA, ST), sides (OE, VE), AC and PO
marks, the rooms whose only form is AT, rooms by number of forms, the lines not shown by class, the particulars and
the rooms not showing K03. Writes nothing.

  python3 out/_analysis/d3_k03_census.py
"""
import json
from collections import Counter, defaultdict

R = "out/_analysis/d3_rulings/"
OPS = [("instantiate", "K03-inst", "K03-inst-spec.txt", "K03-tags-inst.txt"),
       ("restrict", "K03-restrict", "K03-restrict-spec.txt", "K03-tags-restrict.txt"),
       ("add-condition", "K03-addcond", "K03-addcond-spec.txt", "K03-tags-addcond.txt"),
       ("absent", "K03-absent-v2", "K03-absent-spec-v2.txt", "K03-tags-absent-v2.txt")]
FORMS = ("NR", "AT", "TA", "ST")
SHOWING = ("SHOW", "P-G6", "S-SHOW", "S-OTHER", "REJ")


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
        shown = i in tg
        assert shown == (c in SHOWING and not (op == "absent" and c == "P-G6")), i
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
print("\nlines showing K03: %d of %d; rooms showing K03: %d of %d" % (len(shown), len(lines), len(srooms), len(rooms)))
print("  shown lines by tag:", dict(sorted(Counter(t for x in shown.values() for t in x["tags"]).items())))
marks = {r: set().union(*[x["tags"] for x in xs]) for r, xs in srooms.items()}
oe = {r for r, s in marks.items() if "OE" in s}
veonly = {r for r, s in marks.items() if "VE" in s and "OE" not in s}
aconly = {r for r, xs in srooms.items() if all("AC" in x["tags"] for x in xs)}
poonly = {r for r, xs in srooms.items() if all("PO" in x["tags"] for x in xs)}
print("  rooms with OE: %d of %d (%.3f); VE only: %d" % (len(oe), len(srooms), len(oe) / len(srooms), len(veonly)))
print("  AC-only rooms: %d; PO-only rooms: %d" % (len(aconly), len(poonly)))
print("  rooms by form:")
for f in FORMS:
    rs = {r for r, s in marks.items() if f in s}
    print("    %-3s %3d rooms" % (f, len(rs)))
atonly = {r for r, s in marks.items() if (s & set(FORMS)) == {"AT"}}
beyond = {r for r, s in marks.items() if s & {"NR", "TA", "ST"}}
print("  rooms whose only form is AT: %d; rooms with NR, TA or ST: %d" % (len(atonly), len(beyond)))
print("  rooms with ST: %d, of which with AT too: %d" % (len({r for r, s in marks.items() if "ST" in s}),
                                                       len({r for r, s in marks.items() if {"ST", "AT"} <= s})))
print("  rooms by number of forms:", dict(sorted(Counter(len(s & set(FORMS)) for s in marks.values()).items())))

print("\nlines not showing K03, by class:", dict(Counter(x["class"] for x in lines.values() if not x["tags"])))
part = [i for i, x in lines.items() if x["decision"] == "particular"]
print("particulars: %d, of which PO (K03 shown): %d" % (len(part), sum(1 for i in part if lines[i]["tags"])))
nos = sorted(r for r in rooms if r not in srooms)
lim = [r for r in nos if all(x["decision"] == "accept" and x["kind"] == "none" for x in rooms[r])]
print("rooms not showing K03: %d; of them, rooms whose lines are all evidence limits: %d" % (len(nos), len(lim)))
print("rooms not showing K03 with a NOT or EL-NOT line: %s"
      % [r for r in nos if any(x["class"] in ("NOT", "EL-NOT") for x in rooms[r])])
